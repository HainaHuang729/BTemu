"""Bounded subprocess execution; isolated logs; explicit public-key test sealing."""
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import time
from .contracts import digest,file_hash
from .data_control import AttemptLedger,check_execution_gate,read_json,verify_design,write_json


def prepare_key(policy,directory):
    if not policy.get('isolation_approved') or not policy.get('isolation_approval_reference'):raise PermissionError('Sealed worker/key custody isolation unapproved')
    gpg=shutil.which('gpg')
    if not gpg:raise RuntimeError('GPG unavailable; no plaintext fallback')
    home=Path(directory)/'gnupg';home.mkdir(mode=0o700)
    subprocess.run([gpg,'--homedir',str(home),'--batch','--import',policy['public_key_file']],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    if subprocess.run([gpg,'--homedir',str(home),'--batch','--with-colons','--list-secret-keys'],check=True,capture_output=True,text=True).stdout.strip():raise PermissionError('Sealing worker must have no private key')
    listing=subprocess.run([gpg,'--homedir',str(home),'--batch','--with-colons','--list-keys'],check=True,capture_output=True,text=True).stdout
    fingerprints=[x.split(':')[9] for x in listing.splitlines() if x.startswith('fpr:')]
    if policy['public_key_fingerprint'] not in fingerprints:raise PermissionError('Wrong sealing key')
    return gpg,home

def seal_directory(work,destination,policy,key):
    gpg,home=key;destination=Path(destination)
    with tempfile.TemporaryDirectory(prefix='seal_',dir=work.parent) as tmp:
        archive=Path(tmp)/'payload.tar'
        with tarfile.open(archive,'w') as tar:
            for p in sorted(work.iterdir()):tar.add(p,arcname=p.name)
        encrypted=Path(tmp)/'payload.gpg'
        subprocess.run([gpg,'--homedir',str(home),'--batch','--yes','--trust-model','always','--recipient',policy['public_key_fingerprint'],'--output',str(encrypted),'--encrypt',str(archive)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        destination.parent.mkdir(parents=True,exist_ok=True)
        # Hard-link/exclusive publication: never overwrite a sealed attempt.
        with destination.open('xb') as f,encrypted.open('rb') as source:shutil.copyfileobj(source,f)
    return {'ciphertext_sha256':file_hash(destination),'ciphertext_bytes':destination.stat().st_size}

def run(project,manifest,index,budget,stage):
    project=Path(project).resolve();manifest=Path(manifest).resolve()
    c,spec,b=check_execution_gate(project,stage,budget,manifest)
    rows=verify_design(project,manifest)
    if not 0<=index<len(rows):raise ValueError('Index outside frozen manifest')
    row=rows[index]
    if row['split']!=stage:raise ValueError('Stage/split mismatch')
    if 'allowed_indices' in spec and index not in spec['allowed_indices']:raise PermissionError('Index outside authorized batch')
    root=project/'data_runs'/b['budget_id'];ledger=AttemptLedger(root)
    sealed=stage=='sealed_test';policy=read_json(project/'contracts/sealed_test_policy.json') if sealed else None
    old_umask=os.umask(0o077)
    try:
        with tempfile.TemporaryDirectory(prefix='bt_label_',dir=os.environ.get('SLURM_TMPDIR',os.environ.get('TMPDIR','/tmp'))) as temp:
            tmp=Path(temp);work=tmp/'payload';work.mkdir(mode=0o700)
            key=prepare_key(policy,tmp) if sealed else None  # key gate BEFORE reserving/simulating
            previous=[x for x in ledger.entries() if x['sample_id']==row['sample_id']]
            if previous:
                rp=ledger.root/'receipts'/(previous[-1]['attempt_id']+'.json')
                if rp.exists():
                    rec=read_json(rp)
                    if rec.get('qualified') or rec.get('mechanical_qualified'):
                        artifact=project/rec['artifact_path']
                        payload=artifact if sealed else artifact/'label.json'
                        expected=rec['ciphertext_sha256'] if sealed else rec['label_sha256']
                        if not payload.is_file() or file_hash(payload)!=expected:raise ValueError('Accepted artifact damaged; quarantine/manual reconciliation required')
            attempt=ledger.reserve(row,stage,spec,budget_hash=file_hash(budget),contract_hash=digest(c))
            if attempt is None:return {'sample_id':row['sample_id'],'status':'already_qualified_skipped'}
            if not sealed:
                work=root/'workspaces'/attempt['attempt_id'];work.mkdir(parents=True,exist_ok=False)
            start=time.perf_counter();stdout=work/'stdout.log';stderr=work/'stderr.log'
            command=[sys.executable,str(project/'scripts/generate_history_label.py'),'--internal-worker','--project',str(project),'--manifest',str(manifest),'--index',str(index),'--budget',str(Path(budget).resolve()),'--stage',stage,'--attempt-id',attempt['attempt_id'],'--ledger-root',str(root),'--workspace',str(work)]
            env=dict(os.environ);env.update(OMP_NUM_THREADS=str(spec['cpus']),PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
            code=None;failure=None
            try:
                with stdout.open('wb') as out,stderr.open('wb') as err:
                    proc=subprocess.Popen(command,stdout=out,stderr=err,env=env,start_new_session=True)
                    try:code=proc.wait(timeout=max(1,spec['wall_seconds']-60))
                    except subprocess.TimeoutExpired:
                        os.killpg(proc.pid,signal.SIGTERM)
                        try:proc.wait(timeout=10)
                        except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
                        code=124;failure='timeout'
            except OSError as error:
                from .label_quality import classify_failure
                code=1;failure=classify_failure(error)
            if code and not failure and spec.get('recover_history_on_LF_grid_error'):
                try:
                    recovery=subprocess.run([sys.executable,str(project/'maintenance/recover_worker_label.py'),str(project),str(work),str(manifest),str(index)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=30,env=env)
                    (work/'history_recovery_stdout.log').write_text(recovery.stdout);(work/'history_recovery_stderr.log').write_text(recovery.stderr)
                    if recovery.returncode==0:code=0
                except (OSError,subprocess.TimeoutExpired) as error:
                    (work/'history_recovery_stderr.log').write_text(repr(error))
            elapsed=time.perf_counter()-start
            receipt=read_json(work/'worker_receipt.json') if (work/'worker_receipt.json').exists() else {'sample_id':row['sample_id'],'attempt_id':attempt['attempt_id'],'split':stage,'qualified':False,'simulation_status':failure or 'schema_provenance_failure','exit_code':code}
            if failure:receipt.update(simulation_status=failure,qualified=False,exit_code=code)
            receipt.update(wall_seconds=elapsed,allocation_core_hours=spec['cpus']*elapsed/3600)
            quarantine=stage=='train' and spec.get('quarantined_generation_authorized',False)
            if quarantine:
                receipt.update(mechanical_qualified=receipt.get('qualified',False),qualified=False,admission_status='QUARANTINED_PENDING_NATIVE_QUALIFICATION')
            if sealed:
                dest=project/'sealed_store'/b['budget_id']/(attempt['attempt_id']+'.tar.gpg')
                receipt.update(seal_directory(work,dest,policy,key))
                receipt['artifact_path']=str(dest.relative_to(project))
            else:
                dest=root/('quarantine_pending_native' if quarantine else 'labels')/row['sample_id']/attempt['attempt_id'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(work,dest)
                receipt['artifact_path']=str(dest.relative_to(project))
                if (dest/'label.json').exists():receipt['label_sha256']=file_hash(dest/'label.json')
            ledger.finish(attempt,receipt)
            if not sealed:shutil.rmtree(work)
            return {k:receipt[k] for k in ['sample_id','attempt_id','split','simulation_status','qualified','exit_code','mechanical_qualified','admission_status'] if k in receipt}
    finally:os.umask(old_umask)
