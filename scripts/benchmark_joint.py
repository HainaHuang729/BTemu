"""Time trained history + unchanged LF/postprocessing on explicit development points."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from bt_history.contracts import read_contract
from bt_history.inference import load_development_provider,JointEvaluator
from bt_history.history_provider import BoundHistoryProvider
from bt_history.training import save_json
p=argparse.ArgumentParser();p.add_argument('--shared-contract',required=True);p.add_argument('--view-contract',required=True);p.add_argument('--artifact',required=True);p.add_argument('--development-points',required=True);p.add_argument('--output',required=True);a=p.parse_args()
m=json.loads(Path(a.development_points).read_text())
if m['role']!='independent_development':raise ValueError('Explicit independent development points required')
c=read_contract(a.shared_contract);view=read_contract(a.view_contract)
# This deliberately only permits the explicit benchmark points, not arbitrary prior deployment.
allowed=[{**r['physical_parameters'],**view['fixed_parameters']} for r in m['rows']]
provider=load_development_provider(c,a.artifact,lambda p:p in allowed)
evaluator=JointEvaluator(view,BoundHistoryProvider(provider,view));results=[]
for row in m['rows']:
    r=evaluator.evaluate(row['physical_parameters'])
    r['exact_reference_seconds']=row.get('exact_end_to_end_seconds')
    r['speedup']=row['exact_end_to_end_seconds']/r['timing']['end_to_end_seconds'] if row.get('exact_end_to_end_seconds') else None
    results.append(r)
save_json(a.output,{'rows':results,'posterior_validated':False,'cold_imports_excluded':True})
