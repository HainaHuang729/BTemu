"""Pre-register nested parameter IDs; no label or sealed-payload access."""
import json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[2]
d=json.loads((root/'contracts/dataset_design_v2_100k.json').read_text())
rows=[json.loads(s) for s in (root/'manifests/train_full_design.jsonl').read_text().splitlines()]
for sh in d['stages']['train']:
 for line in (root/sh['manifest']).read_text().splitlines():
  r=json.loads(line)
  if r['stratum']!='reserve_broad':rows.append(r)
assert len(rows)==100000
out=root/'manifests/v2_100k/learning_curves';out.mkdir(exist_ok=True)
for n in [1024,2048,4096,8192,16384,32768,65536,100000]:
 selected=rows[:n];families={r['family_id'] for r in selected}
 assert all(r['family_id'] not in families for r in rows[n:]),'Family straddles subset boundary'
 payload={'role':'development','design_version':d['design_version'],'requested_n':n,'sample_ids':[r['sample_id'] for r in selected],'split':'train','frozen_parameter_subset_only':True,'missing_or_failed_labels_must_be_reported':True,'no_validation_or_sealed_labels_read':True,'PCA_fitted_only_on_qualified_classifier_positive_train':True,'reserves_not_implicitly_substituted':True}
 f=out/('train_%06d.json'%n);text=json.dumps(payload,indent=2)+'\n'
 if f.exists():assert f.read_text()==text
 else:f.write_text(text)
print('Frozen 8 nested parameter-ID subsets; no labels read.')
