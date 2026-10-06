import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from bt_history.contracts import read_contract,digest
from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter
from bt_history.history_dataset import load_development,split_groups,nested_ids
from bt_history.training import train,save_json
from bt_history.metrics import representation_audit

p=argparse.ArgumentParser();p.add_argument('action',choices=['validate','train','representation']);p.add_argument('--contract',required=True);p.add_argument('--manifest',required=True);p.add_argument('--output',required=True);p.add_argument('--config',default=str(Path(__file__).resolve().parents[1]/'configs/training.json'));a=p.parse_args()
c=read_contract(a.contract);post=OriginalPostprocessingAdapter(c);rows,failures=load_development(a.manifest,c,post)
split=split_groups(rows)
if a.action=='validate':
    save_json(a.output,{'valid':len(rows),'failures':failures,'split':split,'nested_train_ids':nested_ids(rows,split,[1000,2000,4000,8000]),'full_prior_coverage':False})
elif a.action=='train':
    cfg=json.loads(Path(a.config).read_text());train(c,rows,split,cfg,a.output,post)
else:
    tr=[r for r in rows if split[r['sample_id']]=='train'];va=[r for r in rows if split[r['sample_id']]=='validation']
    report=representation_audit(c,tr,va,post,range(1,min(len(tr),len(c['redshift_grid']))+1))
    report['gate_passed']=False;report['reason']='Thresholds pending scientific confirmation; finite tiny pilot is not prior coverage';save_json(a.output,report)
