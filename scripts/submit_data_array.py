"""Existing bounded submission entry; queue reservations released only by sacct."""
import argparse,json,shlex,subprocess,sys,time,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from bt_history.data_control import read_json,verify_design,check_execution_gate,AttemptLedger,locked,write_json,retry_authorized,core_hour_limit
from bt_history.submission_accounting import submission_charges
p=argparse.ArgumentParser();p.add_argument('--project',default=str(Path(__file__).resolve().parents[1]));p.add_argument('--manifest',required=True);p.add_argument('--stage',required=True);p.add_argument('--budget',required=True);p.add_argument('--indices',required=True);p.add_argument('--dependency');p.add_argument('--submit',action='store_true');a=p.parse_args()
root=Path(a.project).resolve();b=read_json(a.budget);s=b['stages'][a.stage];rows=verify_design(root,a.manifest);indices=[int(x) for x in a.indices.split(',')]
if len(set(indices))!=len(indices) or any(i<0 or i>=len(rows) or rows[i]['split']!=a.stage for i in indices):raise ValueError('Invalid indices/split')
if 'allowed_indices' in s and not set(indices)<=set(s['allowed_indices']):raise PermissionError('Indices outside authorized batch')
array_indices=list(range(len(indices))) if b.get('compact_array_indices') else indices
array_spec=','.join(map(str,array_indices))
logs=root/'data_runs'/b['budget_id']/'scheduler_logs'
cmd=['sbatch','--parsable','--no-requeue','--nodes=1','--ntasks=1',f'--array={array_spec}%{s["max_concurrent"] or 1}',f'--cpus-per-task={s["cpus"]}',f'--mem={s["memory_MiB"]}M',f'--time={max(1,s["wall_seconds"]//60)}',f'--partition={b["allowed_partition"] or "CONFIRM_PARTITION"}',f'--account={b["allowed_account"] or "CONFIRM_ACCOUNT"}',f'--output={logs}/%A_%a.out',f'--error={logs}/%A_%a.err']
if b.get('allowed_qos'):cmd+=['--qos='+b['allowed_qos']]
if s.get('allowed_nodelist',b.get('allowed_nodelist')):cmd+=['--nodelist='+s.get('allowed_nodelist',b.get('allowed_nodelist'))]
if s.get('allowed_reservation'):cmd+=['--reservation='+s['allowed_reservation']]
if s.get('allowed_constraint'):cmd+=['--constraint='+s['allowed_constraint']]
if a.dependency:
    if not a.dependency.startswith('afterany:') or not all(x.replace('_','').isdigit() for x in a.dependency.split(':')[1:]):raise ValueError('Invalid explicit dependency')
    cmd+=['--dependency='+a.dependency]
cmd += [str(root/b.get('worker_script','scripts/generate.sbatch')),str(root),str(Path(a.manifest).resolve()),str(Path(a.budget).resolve()),a.stage]
if b.get('compact_array_indices'):cmd.append(','.join(map(str,indices)))
if not a.submit:print('UNSUBMITTED\n'+shlex.join(cmd));sys.exit(0)
check_execution_gate(root,a.stage,a.budget,a.manifest,require_runtime=False)
if not 0<s['max_concurrent']<=b['max_concurrent_tasks']:raise PermissionError('Concurrency not approved')
submission_root=root/'data_runs'/b['budget_id'];submission_root.mkdir(parents=True,exist_ok=True)
with locked(submission_root/'submissions.lock'):
    path=submission_root/'submissions.jsonl';previous=[json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
    attempts=AttemptLedger(submission_root).entries();charges=submission_charges(submission_root,previous,b)
    write_json(submission_root/'submission_accounting.json',{'rows':charges,'as_of_unix':time.time()})
    # Every submitted slot counts conservatively, including cancelled/rejected slots.
    if sum(len(x['indices']) for x in previous)+len(indices)>b['max_evaluations'] or sum(len(x['indices']) for x in previous if x['stage']==a.stage)+len(indices)>s['max_attempts']:raise PermissionError('Submitted attempts exhaust stage/global cap')
    cost=len(indices)*s['cpus']*s['wall_seconds']/3600
    if cost+sum(v['charged_core_hours'] for v in charges if v['stage']==a.stage)>core_hour_limit(b,a.stage):raise PermissionError('Spent plus running/queued reservations exceeds stage core-hour cap')
    if cost+sum(v['charged_core_hours'] for v in charges)+b.get('runtime_probes',{}).get('max_core_hours',0)>core_hour_limit(b):raise PermissionError('Global allocation cap exhausted')
    for ix in indices:
        earlier=[x for x in attempts if x['sample_id']==rows[ix]['sample_id']]
        submitted=any(x['manifest']==str(Path(a.manifest).resolve()) and ix in x['indices'] for x in previous)
        if submitted and not earlier:
            slots=[v for v in charges if v['stage']==a.stage and v['index']==ix]
            if not slots or not all(v.get('terminal') and v.get('state') in ['CANCELLED','SUBMISSION_REJECTED'] and v.get('actual_core_hours')==0 for v in slots):raise PermissionError('Previous submission not reconciled; no duplicate')
        if earlier:
            if 'retry_sample_allowlist' in s and rows[ix]['sample_id'] not in s['retry_sample_allowlist']:raise PermissionError('Sample retry not explicitly authorized')
            receipt=submission_root/'receipts'/(earlier[-1]['attempt_id']+'.json')
            if not receipt.exists():raise PermissionError('Previous attempt unsettled')
            r=read_json(receipt)
            if not retry_authorized(s,earlier[-1],r) or len(earlier)>s['max_retries_per_sample']:raise PermissionError('Nonretryable or exhausted sample')
    retry_count=sum(max(0,sum(v['sample_id']==sid for v in attempts)-1) for sid in {v['sample_id'] for v in attempts if v['stage']==a.stage})
    new_retries=sum(any(v['sample_id']==rows[ix]['sample_id'] for v in attempts) for ix in indices)
    if retry_count+new_retries>s['max_retry_attempts']:raise PermissionError('Stage retry cap exhausted')
    registration={'submission_id':str(time.time_ns()),'stage':a.stage,'manifest':str(Path(a.manifest).resolve()),'indices':indices,'slurm_array_indices':array_indices,'command':cmd,'state':'reserved_before_sbatch'}
    with path.open('a') as stream:stream.write(json.dumps(registration)+'\n');stream.flush();os.fsync(stream.fileno())
    logs.mkdir(parents=True,exist_ok=True)
    r=subprocess.run(cmd,capture_output=True,text=True)
    write_json(submission_root/(registration['submission_id']+'_slurm.json'),{'response':r.stdout.strip(),'submitted':r.returncode==0,'exit_code':r.returncode,'stderr':r.stderr},exclusive=True)
    if r.returncode:raise RuntimeError('sbatch failed; reservation retained for explicit reconciliation: '+r.stderr)
    print(r.stdout.strip())
