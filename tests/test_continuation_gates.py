import importlib.util,json,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from bt_history.contracts import file_hash
from bt_history.data_control import write_json,read_design
spec=importlib.util.spec_from_file_location('advance',ROOT/'scripts/advance_batch1.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class ContinuationTests(unittest.TestCase):
 def fixture(self,n):
  tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);p=Path(tmp.name)
  for d in ['contracts','configs','results','manifests','data_runs/test/receipts','data_runs/test/labels']:(p/d).mkdir(parents=True,exist_ok=True)
  pre=read_design(ROOT/'manifests/preflight.jsonl');train=read_design(ROOT/'manifests/train_initial_448.jsonl')
  for name,rows in [('preflight',pre),('train_initial_448',train)]:
   f=p/'manifests'/(name+'.jsonl');f.write_text(''.join(json.dumps(r)+'\n' for r in rows))
  write_json(p/'contracts/dataset_design.json',{'manifest_sha256':{str(f.relative_to(p)):file_hash(f) for f in (p/'manifests').iterdir()}})
  b={'budget_id':'test','stages':{'preflight':{'cpus':16,'wall_seconds':7200},'train':{'quarantined_generation_authorized':False,'max_concurrent':8}}};write_json(p/'configs/budget.json',b);write_json(p/'configs/data_stage_budgets.json',b);write_json(p/'configs/batch1_execution.json',{'enabled':True,'budget_id':'test'})
  attempts=[]
  for i,row in enumerate(pre[:n]):
   aid='a'+str(i);attempt={'sample_id':row['sample_id'],'attempt_id':aid,'stage':'preflight','slurm_job_id':str(100+i),'slurm_array_task_id':str(i),'ordinal_for_sample':1};attempts.append(attempt)
   directory=p/'data_runs/test/labels'/aid;directory.mkdir();record={k:[.2] for k in mod.PARITY_KEYS};record['sample_id']=row['sample_id'];write_json(directory/'label.json',record)
   write_json(p/'data_runs/test/receipts'/(aid+'.json'),{**attempt,'simulation_status':'success','qualified':True,'artifact_path':str(directory.relative_to(p)),'label_sha256':file_hash(directory/'label.json')})
  (p/'data_runs/test/attempts.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in attempts))
  return p
 def invoke(self,p):
  class Result:returncode=0;stdout='999';stderr=''
  with patch('bt_history.data_status.collect',return_value=[]),patch.object(sys,'argv',['advance','--project',str(p),'--budget',str(p/'configs/budget.json')]),patch.object(mod.subprocess,'run',return_value=Result()) as run:
   rc=mod.main();return rc,run.call_args_list
 def test_one_next_preflight_only(self):
  p=self.fixture(1);rc,calls=self.invoke(p);self.assertEqual(rc,0);self.assertEqual(len(calls),1)
  cmd=calls[0].args[0];self.assertIn('preflight',cmd);self.assertEqual(cmd[cmd.index('--indices')+1],'1');self.assertNotIn('train',cmd)
 def test_parity_mismatch_halts_without_submission(self):
  p=self.fixture(2);f=p/'data_runs/test/labels/a1/label.json';r=json.loads(f.read_text());r['global_xHI']=[.3];write_json(f,r)
  rp=p/'data_runs/test/receipts/a1.json';receipt=json.loads(rp.read_text());receipt['label_sha256']=file_hash(f);write_json(rp,receipt)
  rc,calls=self.invoke(p);self.assertEqual(rc,1);self.assertEqual(calls,[])
 def test_false_scientific_qualification_never_submits_train(self):
  p=self.fixture(12);write_json(p/'results/native_qualification.json',{'qualified_for_batch1':False});rc,calls=self.invoke(p)
  self.assertEqual(rc,1);self.assertEqual(len(calls),1);self.assertTrue(calls[0].args[0][1].endswith('qualify_native.py'))
 def test_native_load_failure_stops_preflight(self):
  p=self.fixture(1);f=p/'data_runs/test/receipts/a0.json';r=json.loads(f.read_text());r.update(qualified=False,simulation_status='runtime_native_load_failure');write_json(f,r)
  rc,calls=self.invoke(p);self.assertEqual(rc,1);self.assertEqual(calls,[])

 def test_authorized_quarantine_can_submit_without_native_admission(self):
  p=self.fixture(1)
  f=p/'configs/budget.json';b=json.loads(f.read_text());b['stages']['train'].update(quarantined_generation_authorized=True,max_retry_attempts=32);write_json(f,b);write_json(p/'configs/data_stage_budgets.json',b)
  with patch.object(mod,'admit_completed',side_effect=AssertionError('Must not admit')):
   rc,calls=self.invoke(p)
  self.assertEqual(rc,0);commands=[c.args[0] for c in calls];self.assertEqual(len(commands),2)
  train=[cmd for cmd in commands if 'train' in cmd][0];self.assertEqual(train[train.index('--indices')+1],'0,1')

if __name__=='__main__':unittest.main()

class IsolatedFailureTests(ContinuationTests):
 def test_isolated_schema_failure_does_not_block_next_train_points(self):
  p=self.fixture(1)
  b=json.loads((p/'configs/budget.json').read_text());b['stages']['train'].update(quarantined_generation_authorized=True,max_retry_attempts=32)
  write_json(p/'configs/budget.json',b);write_json(p/'configs/data_stage_budgets.json',b)
  row=read_design(p/'manifests/train_initial_448.jsonl')[0]
  attempt={'sample_id':row['sample_id'],'attempt_id':'train_failed','stage':'train','slurm_job_id':'200','slurm_array_task_id':'0','ordinal_for_sample':1}
  with (p/'data_runs/test/attempts.jsonl').open('a') as f:f.write(json.dumps(attempt)+'\n')
  write_json(p/'data_runs/test/receipts/train_failed.json',{**attempt,'qualified':False,'simulation_status':'schema_provenance_failure','failure_reason':'LF grid boundary'})
  rc,calls=self.invoke(p);self.assertEqual(rc,0)
  commands=[c.args[0] for c in calls];cmd=[c for c in commands if 'train' in c][0]
  self.assertEqual(cmd[cmd.index('--indices')+1],'1,2')
  self.assertEqual(json.loads((p/'data_runs/test/train_error_summary.json').read_text())['failed_unique'],1)

class EightWaveTests(ContinuationTests):
 def test_after_first8_submits_eight_new_points(self):
  p=self.fixture(1)
  b=json.loads((p/'configs/budget.json').read_text());b['stages']['train'].update(quarantined_generation_authorized=True,max_retry_attempts=32)
  write_json(p/'configs/budget.json',b);write_json(p/'configs/data_stage_budgets.json',b)
  write_json(p/'configs/batch1_execution.json',{'enabled':True,'budget_id':'test','subsequent_wave_size':8})
  write_json(p/'data_runs/test/first8_quality.json',{'mechanical_passed':True})
  for i,row in enumerate(read_design(p/'manifests/train_initial_448.jsonl')[:8]):
   aid='t'+str(i);attempt={'sample_id':row['sample_id'],'attempt_id':aid,'stage':'train','slurm_job_id':str(200+i),'slurm_array_task_id':str(i),'ordinal_for_sample':1}
   with (p/'data_runs/test/attempts.jsonl').open('a') as f:f.write(json.dumps(attempt)+'\n')
   write_json(p/'data_runs/test/receipts'/(aid+'.json'),{**attempt,'qualified':False,'mechanical_qualified':True,'simulation_status':'success'})
  rc,calls=self.invoke(p);self.assertEqual(rc,0)
  cmd=[c.args[0] for c in calls if 'train' in c.args[0]][0]
  self.assertEqual(cmd[cmd.index('--indices')+1],'8,9,10,11,12,13,14,15')
