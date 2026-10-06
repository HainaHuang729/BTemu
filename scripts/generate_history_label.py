"""Single canonical entry point; no expensive action can bypass budget/native gates."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
def main():
    p=argparse.ArgumentParser();p.add_argument('--project',default=str(Path(__file__).resolve().parents[1]));p.add_argument('--manifest',required=True);p.add_argument('--index',type=int,required=True);p.add_argument('--budget',required=True);p.add_argument('--stage',choices=['preflight','train','validation','challenge_development','sealed_test'],required=True);p.add_argument('--internal-worker',action='store_true');p.add_argument('--attempt-id');p.add_argument('--ledger-root');p.add_argument('--workspace');a=p.parse_args()
    if a.internal_worker:
        from bt_history.label_worker import evaluate
        return evaluate(a.project,a.manifest,a.index,a.budget,a.stage,a.attempt_id,a.ledger_root,a.workspace)
    from bt_history.data_runner import run
    result=run(a.project,a.manifest,a.index,a.budget,a.stage);print(json.dumps(result));return 0 if result.get('qualified') or result.get('mechanical_qualified') or result.get('status')=='already_qualified_skipped' else 1
if __name__=='__main__':sys.exit(main())
