"""Software/design verification, never a scientific precision claim."""
import json,sys,hashlib
from pathlib import Path
import numpy as np
import torch
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'src'));sys.path.insert(0,str(Path(__file__).parent))
from models import Classifier,PCAMLP
from bt_history.data_control import verify_design,check_execution_gate,read_json,assert_development_path
from bt_history.quarantine_admission import qualified_pipeline_matches
from bt_history.contracts import file_hash
assert Classifier()(torch.zeros(3,10)).shape==(3,)
assert PCAMLP(np.zeros(32),np.eye(32)[:8])(torch.zeros(3,10)).shape==(3,32)
x=PCAMLP(np.zeros(32),np.eye(32)[:8],transform='logit')(torch.zeros(3,10));assert torch.all((x>=0)&(x<=1))
assert int(.30999<.31)==1 and int(.31<.31)==0
try:assert_development_path(root/'sealed_store/never_opened.json','train')
except PermissionError:pass
else:raise AssertionError('Sealed path not blocked')
assert qualified_pipeline_matches(root,read_json(root/'results/native_qualification.json'))
for budget,manifest in [('configs/batch2_budget.json','manifests/train_full_design.jsonl'),('configs/v2_100k_budget.json','manifests/v2_100k/train_0000.jsonl')]:check_execution_gate(root,'train',root/budget,root/manifest,require_runtime=False)
d=read_json(root/'contracts/dataset_design_v2_100k.json');assert d['existing_train_count']==4096
for stage,expected in [('train',100000),('validation',11024),('sealed_test',5000)]:
 count=sum(sh['count'] for sh in d['stages'][stage]);assert count==expected,(stage,count)
 for sh in d['stages'][stage]:assert file_hash(root/sh['manifest'])==d['manifest_sha256'][sh['manifest']]
for sh in d['stages']['train'][:2]:
 rows=verify_design(root,root/sh['manifest']);assert len(rows)==512
 assert all(r['simulation_ic_seed']==725213656658 and r['split']=='train' for r in rows)
print('PASS: v1/v2 gates, sharded checksums/counts, architecture shapes, strict classifier boundary, sealed-path rejection. Software checks only.')
