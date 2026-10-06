import argparse,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from bt_history.runtime_qualification import inspect_runtime
from bt_history.data_control import write_json
p=argparse.ArgumentParser();p.add_argument('--project',default=str(Path(__file__).resolve().parents[1]));p.add_argument('--output',required=True);a=p.parse_args()
r=inspect_runtime(a.project);write_json(a.output,r);print(r['status'],r.get('error',''))
if not r['import_passed']:sys.exit(2)
