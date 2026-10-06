"""Freeze only admitted development labels; preserve all original split designs."""
import hashlib,json,sqlite3,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
RUN=ROOT/'artifacts/development_comparison_20261005'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,data):
 path.write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def percentile(a,q):
 a=sorted(a);p=(len(a)-1)*q;lo=int(p);hi=min(lo+1,len(a)-1);return a[lo]+(a[hi]-a[lo])*(p-lo)
def main():
 RUN.mkdir(exist_ok=False)
 db=sqlite3.connect('file:'+str(ROOT/'data_runs/dataset_v2_100k/dataset_manifest.sqlite')+'?mode=ro',uri=True)
 records=db.execute('select id,split,item,metadata from labels where split in ("train","validation") order by split,id').fetchall();db.close()
 files=[];groups={'train':[],'validation':[]};seen=set();tuples=set();families={}
 for sid,split,item,metadata in records:
  it=json.loads(item);m=json.loads(metadata)
  assert it['sample_id']==sid and it['split']==split and sid not in seen
  assert m['history_valid'] and m['tau_valid'];seen.add(sid)
  key=tuple(sorted(m['physical_parameters'].items()))
  if key in tuples:raise ValueError('Duplicate physical point in development snapshot')
  tuples.add(key);files.append(it);groups[split].append(m)
  raw=json.loads((ROOT/it['path']).read_text());family=raw['family_id']
  if family in families and families[family]!=split:raise ValueError('Family crosses frozen splits')
  families[family]=split
 if len(groups['train'])<8000 or len(groups['validation'])<1000:raise ValueError('Insufficient snapshot labels')
 snapshot={'role':'development','schema_version':'v2_explicit_snapshot','files':files,'split_frozen':True,'frozen_unix':time.time(),'validation_definition':'all qualified independent v2 Validation available at snapshot; v1 Validation excluded','no_sealed_access':True,'sampling_order':'deterministic sample_id; qualification-conditioned development snapshot; report failures separately'}
 write(RUN/'snapshot.json',snapshot)
 plan={'snapshot_sha256':sha(RUN/'snapshot.json'),'training_config_sha256':sha(ROOT/'configs/training.json'),'model_implementation_sha256':sha(ROOT/'maintenance/v2/models.py'),'baseline_implementation_sha256':sha(ROOT/'maintenance/v2/baseline.py'),'driver_sha256':sha(ROOT/'maintenance/v2/run_curve.py'),'N':len(groups['train']),'validation_n':len(groups['validation']),'reuse_direct_run':None,'all_five_seeds_retained':True,'production_accepted':False,'additional_complete_simulations':0}
 write(RUN/'plan.json',plan)
 science=json.loads((ROOT/'contracts/science_contract.json').read_text());coverage={}
 for split,rows in groups.items():
  zs=science['redshift_grid'];i5=zs.index(5);i35=zs.index(35)
  def distribution(values):return {**{'q'+str(int(q*100)):percentile(values,q) for q in [.5,.68,.9,.95]},'min':min(values),'max':max(values)}
  low=[m['global_xHI'][i5] for m in rows];high=[m['global_xHI'][i35] for m in rows]
  coverage[split]={'count':len(rows),'classifier_positive':sum(m['classifier_label'] for m in rows),'LF_invalid_history_valid':sum(not m['lf_valid'] for m in rows),'xHI_z5':distribution(low),'xHI_z35':distribution(high),'z5_threshold_counts':{str(t):sum(x>t for x in low) for t in [.01,.05,.1,.2]},'transition_trajectories':sum(any(.1<x<.9 for x in m['global_xHI']) for m in rows),'exact_all_zero':sum(all(x==0 for x in m['global_xHI']) for m in rows),'exact_all_one':sum(all(x==1 for x in m['global_xHI']) for m in rows),'parameter_ranges':{k:{'min':min(m['physical_parameters'][k] for m in rows),'max':max(m['physical_parameters'][k] for m in rows)} for k in science['parameter_order']}}
 write(RUN/'coverage.json',{'split_statistics':coverage,'sampling_unit':'parameter trajectory','endpoint_flags_are_warnings':True,'native':science['native_sha256'],'failure_denominator_report':'results/dataset_progress.json; this is an admitted-label snapshot, not entire prior unconditional performance','sealed_access':False})
 for n in [1024,2048,4096,8192]:
  ids=[m['sample_id'] for m in groups['train'][:n]]
  write(RUN/('nested_development_%06d.json'%n),{'sample_ids':ids,'split':'train','parent_snapshot_sha256':plan['snapshot_sha256'],'role':'new development comparison series; does not replace v1/v2 frozen learning curves','validation_sample_ids':[m['sample_id'] for m in groups['validation']]})
 write(RUN/'status.json',{'status':'SNAPSHOT_FROZEN','counts':{k:len(v) for k,v in groups.items()},'sealed_access':False})
 cmd=['sbatch','--parsable','--account=tkcastrosim','--partition=chpc','--qos=tkcastrosim','--reservation=tkcastrosim1','--cpus-per-task=1','--mem=8G','--time=480','--job-name=bt_development_comparison','--output='+str(RUN/'training_%j.log'),str(ROOT/'maintenance/development_snapshot/train.sbatch'),str(RUN)]
 r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True,timeout=30)
 write(RUN/'submission.json',{'command':cmd,'job_id':r.stdout.strip(),'exit_code':r.returncode,'stderr':r.stderr})
 if r.returncode:raise RuntimeError(r.stderr)
 write(RUN/'status.json',{'status':'TRAINING_SUBMITTED','job_id':r.stdout.strip(),'counts':{k:len(v) for k,v in groups.items()},'sealed_access':False})
 print(json.dumps({'counts':{k:len(v) for k,v in groups.items()},'job_id':r.stdout.strip()}))
if __name__=='__main__':main()
