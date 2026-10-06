import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from bt_history.data_status import collect
p=argparse.ArgumentParser();p.add_argument('--project',default=str(Path(__file__).resolve().parents[1]));a=p.parse_args();print(json.dumps(collect(a.project),ensure_ascii=False,indent=2))
