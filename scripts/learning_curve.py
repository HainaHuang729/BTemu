import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from bt_history.contracts import read_contract
from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter
from bt_history.history_dataset import load_development,split_groups,nested_ids
from bt_history.training import train,save_json
p=argparse.ArgumentParser();p.add_argument('--contract',required=True);p.add_argument('--manifest',required=True);p.add_argument('--config',required=True);p.add_argument('--output',required=True);a=p.parse_args()
c=read_contract(a.contract);cfg=json.loads(Path(a.config).read_text());post=OriginalPostprocessingAdapter(c);rows,failures=load_development(a.manifest,c,post);split=split_groups(rows)
nested=nested_ids(rows,split,[1000,2000,4000,8000]);root=Path(a.output);root.mkdir(parents=True,exist_ok=False)
save_json(root/'design.json',{'nested':nested,'validation_ids':[k for k,v in split.items() if v=='validation'],'failure_count':len(failures),'no_test_access':True})
for n,ids in nested.items():
    subset=[r for r in rows if r['sample_id'] in ids or split[r['sample_id']]=='validation']
    train(c,subset,{r['sample_id']:split[r['sample_id']] for r in subset},cfg,root/f'N{n}',post)
if not nested:save_json(root/'status.json',{'status':'insufficient_data_for_registered_learning_curve','curves_measured':False})
