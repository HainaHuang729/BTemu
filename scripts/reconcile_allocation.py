"""Read-only sacct reconciliation for own recorded attempts; never changes jobs."""
import argparse,json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from bt_history.data_control import AttemptLedger,read_json,write_json
p=argparse.ArgumentParser();p.add_argument('--project',default=str(Path(__file__).resolve().parents[1]));p.add_argument('--budget-id',required=True);a=p.parse_args();root=Path(a.project);ledger=AttemptLedger(root/'data_runs'/a.budget_id);out=[]
terminal={'COMPLETED','FAILED','TIMEOUT','OUT_OF_MEMORY','CANCELLED','NODE_FAIL','BOOT_FAIL','PREEMPTED'}
for attempt in ledger.entries():
    job=attempt['slurm_job_id'];result=subprocess.run(['sacct','-j',str(job),'--noheader','--parsable2','--format=JobIDRaw,State,ExitCode,ElapsedRaw,AllocCPUS,MaxRSS,TotalCPU'],check=True,capture_output=True,text=True)
    candidates=[line.split('|') for line in result.stdout.splitlines() if line and '.' not in line.split('|')[0]]
    matches=[v for v in candidates if v[0]==str(job)]
    if len(matches)!=1:out.append({'attempt_id':attempt['attempt_id'],'status':'accounting_unresolved'});continue
    v=matches[0];state=v[1].split()[0].split('+')[0];elapsed=int(v[3]);cpus=int(v[4]);done=state in terminal
    entry={'attempt_id':attempt['attempt_id'],'job_id':job,'state':state,'elapsed_seconds':elapsed,'allocated_cpus':cpus,'allocation_core_hours':elapsed*cpus/3600,'terminal':done,'max_RSS_raw':v[5],'total_CPU_raw':v[6]};out.append(entry)
    receipt=ledger.root/'receipts'/(attempt['attempt_id']+'.json')
    if done and not receipt.exists():
        # A completed scheduler job without a receipt has unknown label integrity.
        category='timeout' if state=='TIMEOUT' else 'out_of_memory' if state=='OUT_OF_MEMORY' else 'infrastructure_failure'
        ledger.finish(attempt,{'sample_id':attempt['sample_id'],'split':attempt['stage'],'simulation_status':category,'qualified':False,'exit_code':v[2],'accounting_confirmed':True,'allocation_core_hours':entry['allocation_core_hours'],'wall_seconds':elapsed,'reason':'terminal allocation without complete publication receipt; no label inferred'})
write_json(ledger.root/'allocation_accounting.json',{'rows':out,'scope':'own recorded attempts only; no job mutations'})
print('Reconciled',len(out),'recorded allocations; no scientific values read.')
