"""Input geometry is public; scientific summaries use qualified train/validation only."""
import argparse,json,sys
from collections import Counter
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from bt_history.data_control import read_json,write_json,verify_design
from bt_history.history_dataset import load_development
from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter
p=argparse.ArgumentParser();p.add_argument('--project',default=str(Path(__file__).resolve().parents[1]));p.add_argument('--include-qualified-labels',action='store_true');a=p.parse_args();root=Path(a.project);c=read_json(root/'contracts/science_contract.json')
r={'uses_sealed_labels':False,'inputs':{},'scientific_summaries':{'status':'no labels read'}}
for split,name in [('train','train_full_design'),('validation','validation_design'),('sealed_test','sealed_test_design')]:
    rows=verify_design(root,root/'manifests'/(name+'.jsonl'));v=np.array([[x['canonical_parameters'][k] for k in c['parameter_order']] for x in rows]);r['inputs'][split]={'count':len(rows),'strata':dict(Counter(x['stratum'] for x in rows)),'per_parameter_min':dict(zip(c['parameter_order'],v.min(0).tolist())),'per_parameter_max':dict(zip(c['parameter_order'],v.max(0).tolist())),'view_tag_counts':dict(Counter(t for x in rows for t in x['inference_view_tags']))}
if a.include_qualified_labels:
    rows,_=load_development(root/'manifests/qualified_development.json',c,OriginalPostprocessingAdapter(c));r['scientific_summaries']={}
    for split in ['train','validation']:
        rr=[x for x in rows if x['split']==split]
        if not rr:r['scientific_summaries'][split]={'status':'no qualified labels'};continue
        x=np.array([v['global_xHI'] for v in rr]);r['scientific_summaries'][split]={'n':len(rr),'all_zero_trajectories':int(np.all(x==0,axis=1).sum()),'all_one_trajectories':int(np.all(x==1,axis=1).sum()),'transition_trajectories':int(np.any((x>.1)&(x<.9),axis=1).sum()),'tau_range':[min(v['tau_exact_derived'] for v in rr),max(v['tau_exact_derived'] for v in rr)],'quality_flags':dict(Counter(t for v in rr for t in v['quality_flags']))}
write_json(root/'results/development_coverage.json',r);print('Parameter coverage written; sealed labels were not opened.')
