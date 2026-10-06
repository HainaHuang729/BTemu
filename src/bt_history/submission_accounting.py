"""Conservative charge for every submitted allocation, including queued workers."""
import subprocess
from .data_control import read_json

TERMINAL={'COMPLETED','FAILED','TIMEOUT','OUT_OF_MEMORY','CANCELLED','NODE_FAIL','BOOT_FAIL','PREEMPTED','DEADLINE','REVOKED'}

def confirmed_array_rejection(root,sub):
    path=root/(sub['submission_id']+'_slurm.json')
    if not path.exists():return False
    r=read_json(path)
    return r.get('submitted') is False and r.get('exit_code',0)!=0 and not r.get('response','').strip() and 'Batch job submission failed: Invalid job array specification' in r.get('stderr','')

def submission_charges(root, submissions, budget):
    def query(job):
        return subprocess.run(['sacct','-j',str(job),'--array','--noheader','--parsable2','--format=JobID,State,ElapsedRaw,AllocCPUS'],check=True,capture_output=True,text=True,timeout=30).stdout
    cache_path=root/'submission_accounting.json'
    cached={(r['submission_id'],r['index']):r for r in read_json(cache_path).get('rows',[]) if r.get('terminal')} if cache_path.exists() else {}
    result=[]
    for sub in submissions:
        spec=budget['stages'][sub['stage']]
        reservation=spec['cpus']*spec['wall_seconds']/3600
        response=root/(sub['submission_id']+'_slurm.json')
        job=read_json(response)['response'].split(';')[0] if response.exists() else None
        lines={}
        rejected=confirmed_array_rejection(root,sub)
        if job and not all((sub['submission_id'],ix) in cached for ix in sub['indices']):
            try:
                for line in query(job).splitlines():
                    v=line.strip().split('|')
                    if len(v)>=4 and '.' not in v[0]:lines[v[0]]=v
            except (OSError,subprocess.SubprocessError):pass
        for position,ix in enumerate(sub['indices']):
            if rejected:
                result.append({'submission_id':sub['submission_id'],'stage':sub['stage'],'index':ix,'job_id':None,'state':'SUBMISSION_REJECTED','terminal':True,'charged_core_hours':0,'reserved_core_hours':0,'actual_core_hours':0});continue
            if (sub['submission_id'],ix) in cached:
                result.append(cached[(sub['submission_id'],ix)]);continue
            name=str(job)+'_'+str(sub.get('slurm_array_indices',sub['indices'])[position]);v=lines.get(name)
            state=v[1].split()[0].split('+')[0] if v else 'ACCOUNTING_UNRESOLVED'
            terminal=state in TERMINAL
            charge=int(v[2])*int(v[3])/3600 if terminal else reservation
            result.append({'submission_id':sub['submission_id'],'stage':sub['stage'],'index':ix,'job_id':name if job else None,'state':state,'terminal':terminal,'charged_core_hours':charge,'reserved_core_hours':0 if terminal else reservation,'actual_core_hours':charge if terminal else None})
    return result
