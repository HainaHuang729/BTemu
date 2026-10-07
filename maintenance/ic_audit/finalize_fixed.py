"""Admit drained fixed-IC workers without classifying user cancellations as failures."""
import sys,json,sqlite3,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'maintenance/v2'))
from bt_history.data_control import read_json,write_json,locked
from bt_history.contracts import file_hash
import importlib.util
module_spec=importlib.util.spec_from_file_location('fixed_ic_original_advance',ROOT/'maintenance/v2/advance.py');module=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(module);attach=module.attach

def main():
 run=ROOT/'data_runs/dataset_v2_100k'
 with locked(run/'controller.lock'):
  db=sqlite3.connect(str(run/'dataset_manifest.sqlite'));admitted=0
  for line in (run/'attempts.jsonl').read_text().splitlines()[-512:]:
   at=json.loads(line);rp=run/'receipts'/(at['attempt_id']+'.json')
   if not rp.exists():continue
   rr=read_json(rp)
   if not rr.get('qualified'):continue
   it={'sample_id':at['sample_id'],'split':at['stage'],'path':str(Path(rr['artifact_path'])/'label.json'),'sha256':rr['label_sha256'],'receipt':str(rp.relative_to(ROOT))}
   before=db.total_changes;attach(db,it,rr);admitted+=int(db.total_changes>before)
  db.commit();p=read_json(ROOT/'results/dataset_progress.json');snapshot=read_json(ROOT/'results/fixed_ic_transition_snapshot.json')
  for split in ['train','validation']:
   count,pos=db.execute('select count(*),coalesce(sum(positive),0) from labels where split=?',(split,)).fetchone()
   p['datasets'][split].update(qualified=count,positive_fraction=pos/count,negative_fraction=1-pos/count)
  p.update(updated_at_hkt=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),status='FIXED_IC_PRODUCTION_DRAINED',dataset_version='fixed_ic_v1',fixed_IC_waves_stopped=True,running=0,pending=0,transition_cancelled_unstarted_slots=snapshot['cancelled_pending_slots'])
  write_json(ROOT/'results/dataset_progress.json',p)
  snapshot.update(drained_qualified={s:p['datasets'][s]['qualified'] for s in ['train','validation']},drained_at_hkt=p['updated_at_hkt'],drained_running=0,drained_pending=0,new_worker_receipts_admitted=admitted)
  write_json(ROOT/'results/fixed_ic_transition_snapshot.json',snapshot)
  (ROOT/'reports/fixed_ic_transition_snapshot.md').write_text('# Fixed-IC transition snapshot\n\n```json\n'+json.dumps(snapshot,indent=2)+'\n```\n\nExisting data and splits retained. Running workers completed and were admitted using the original validator/admission logic. User-cancelled unstarted slots are not numerical failures. No additional fixed-IC waves will run.\n')
  print(json.dumps({'admitted':admitted,'qualified':snapshot['drained_qualified']}))
if __name__=='__main__':main()
