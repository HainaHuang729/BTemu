"""Prepare a freeze record; sealed-label execution intentionally disabled this round."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from bt_history.contracts import file_hash,digest,read_contract
p=argparse.ArgumentParser();p.add_argument('--contract',required=True);p.add_argument('--artifact',required=True);p.add_argument('--protocol',required=True);p.add_argument('--output',required=True);p.add_argument('--open-sealed-test',action='store_true');a=p.parse_args()
if a.open_sealed_test:raise PermissionError('No sealed-test authorization has been granted for this deliverable. No labels opened.')
c=read_contract(a.contract);root=Path(a.artifact)
project=Path(__file__).resolve().parents[1]
analysis_files={str(x.relative_to(project)):file_hash(x) for folder in ['src','scripts','contracts','configs'] for x in sorted((project/folder).rglob('*')) if x.is_file()}
record={'analysis_and_configuration_files':analysis_files,'status':'prepared_not_scientifically_accepted','science_contract_hash':digest(c),'acceptance_protocol_sha256':file_hash(a.protocol),'artifact_files':{str(x.relative_to(root)):file_hash(x) for x in sorted(root.rglob('*')) if x.is_file()},'sealed_labels_opened':False,'production_mcmc_started':False,'required_next':['confirm scientific thresholds','pass independent history/derived/component likelihood gates including penalized xHI','independent exact posterior checks, ESS and support overlap','explicit sealed-test authorization before implementing final read']}
with open(a.output,'x') as f:json.dump(record,f,indent=2)
