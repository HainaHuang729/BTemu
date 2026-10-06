"""Freeze independent parameter manifests only; never opens any test labels."""
import argparse,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from bt_history.data_design import generate
p=argparse.ArgumentParser();p.add_argument('--project',default=str(Path(__file__).resolve().parents[1]));a=p.parse_args()
d=generate(a.project);print(d['design_version'],d['counts'])
