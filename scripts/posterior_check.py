import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from bt_history.metrics import posterior_reweight
p=argparse.ArgumentParser();p.add_argument('--independent-development-comparisons',required=True);p.add_argument('--output',required=True);a=p.parse_args()
m=json.loads(Path(a.independent_development_comparisons).read_text())
if m['role']!='independent_development_exact_comparisons':raise ValueError('Independent exact comparisons required')
r=posterior_reweight(m['exact_logL'],m['emulator_logL'],m['parameters'])
Path(a.output).write_text(json.dumps(r,indent=2)+'\n')
