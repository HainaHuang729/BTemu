import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from bt_history.label_quality import validate_development_file
p=argparse.ArgumentParser();p.add_argument('--project',default=str(Path(__file__).resolve().parents[1]));p.add_argument('--manifest',required=True);p.add_argument('--sample-id',required=True);p.add_argument('--label',required=True);p.add_argument('--sha256',required=True);a=p.parse_args()
print(json.dumps(validate_development_file(a.project,a.label,a.manifest,a.sample_id,a.sha256)))
