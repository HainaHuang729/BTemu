"""Use existing training implementations; compare on identical exact-positive validation."""
import sys,subprocess,time,os,traceback
from pathlib import Path
import numpy as np
import torch
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'maintenance/v2'))
from bt_history.data_control import read_json,write_json
from bt_history.contracts import file_hash
from bt_history.transforms import Normalizer
from bt_history.resmlp import ReionizationHistoryEmulator
from bt_history.metrics import fidelity
import baseline
from loader import load
from bt_history.training import train
from models import PCAMLP,Classifier
RUN=Path(sys.argv[1])
def main():
 start=time.time();plan=read_json(RUN/'plan.json');write_json(RUN/'status.json',{'status':'DEVELOPMENT_TRAINING_RUNNING','job_id':os.environ.get('SLURM_JOB_ID'),'counts':{'train':plan['N'],'validation':plan['validation_n']},'sealed_access':False})
 assert file_hash(RUN/'snapshot.json')==plan['snapshot_sha256']
 for p,h in [('configs/training.json',plan['training_config_sha256']),('maintenance/v2/models.py',plan['model_implementation_sha256']),('maintenance/v2/baseline.py',plan['baseline_implementation_sha256'])]:assert file_hash(ROOT/p)==h
 c,rows,post=load(RUN/'snapshot.json');cfg=read_json(ROOT/'configs/training.json')
 train(c,rows,{r['sample_id']:r['split'] for r in rows},cfg,RUN/'direct_resmlp',post)
 baseline.load=load
 oldargv=sys.argv;sys.argv=['baseline.py','--snapshot',str(RUN/'snapshot.json'),'--out',str(RUN/'nnero_style'),'--train']
 try:baseline.main()
 finally:sys.argv=oldargv
 val=[r for r in rows if r['split']=='validation'];positive=np.array([r['exact_xHI_at_observation_redshifts']['5.9']<.31 for r in val]);pv=[r for r,b in zip(val,positive) if b]
 cfg=read_json(ROOT/'configs/training.json');torch.set_num_threads(1);x=np.array([[r['physical_parameters'][k] for k in c['parameter_order']] for r in val]);direct=RUN/'direct_resmlp';nn=RUN/'nnero_style';dn=Normalizer(**read_json(direct/'normalizer.json'));nnorm=Normalizer(**read_json(nn/'normalizer.json'));dx=torch.tensor(dn.transform(x),dtype=torch.float32);nx=torch.tensor(nnorm.transform(x),dtype=torch.float32)
 dp=[];npred=[];probs=[]
 for seed in cfg['seeds']:
  model=ReionizationHistoryEmulator(10,32,**cfg['architecture']);model.load_state_dict(torch.load(direct/('seed_%d.pt'%seed),map_location='cpu'));model.eval()
  with torch.no_grad():dp.append(model(dx).numpy())
  classifier=Classifier();classifier.load_state_dict(torch.load(nn/('classifier_seed_%d.pt'%seed),map_location='cpu'));classifier.eval()
  with torch.no_grad():probs.append(torch.sigmoid(classifier(nx)).numpy())
  rp=nn/('regressor_seed_%d.json'%seed)
  if rp.exists():
   report=read_json(rp);basis=np.load(nn/('PCA_'+report['transform']+'_basis.npz'));model=PCAMLP(basis['mean'],basis['basis'][:report['K']],transform=report['transform']);model.load_state_dict(torch.load(nn/('regressor_seed_%d.pt'%seed),map_location='cpu'));model.eval()
   with torch.no_grad():npred.append(model(nx[positive]).numpy())
 dmean=np.mean(dp,axis=0,dtype=np.float64);pmean=np.mean(probs,axis=0);pred=pmean>=.5
 output={'validation_count':len(val),'exact_positive_validation_count':len(pv),'same_positive_validation_IDs':True,'direct_training_scope':'all qualified train','nnero_regressor_training_scope':'exact classifier-positive train only','classifier_not_used_as_prior_or_prediction_gate':True,'classifier_ensemble':{'false_negative':int((positive&~pred).sum()),'false_positive':int((~positive&pred).sum()),'false_negative_rate':float((positive&~pred).sum()/positive.sum()),'accuracy':float((pred==positive).mean())},'direct_ensemble_all_validation':fidelity(c,val,dmean,post),'direct_ensemble_positive_validation':fidelity(c,pv,dmean[positive],post),'deployment_accepted':False,'sealed_access':False}
 if len(npred)==len(cfg['seeds']):
  mean=np.mean(npred,axis=0,dtype=np.float64)
  if np.isfinite(mean).all() and np.all((mean>=0)&(mean<=1)):output['nnero_ensemble_positive_validation']=fidelity(c,pv,mean,post)
  else:output['nnero_ensemble_positive_validation']={'status':'INVALID_PHYSICAL_HISTORY_NO_CLIPPING'}
 else:output['nnero_ensemble_positive_validation']={'status':'BLOCKED_BY_REPRESENTATION_AUDIT'}
 write_json(RUN/'comparison_metrics.json',output)
 write_json(RUN/'status.json',{'status':'DEVELOPMENT_COMPARISON_COMPLETED','job_id':os.environ.get('SLURM_JOB_ID'),'seconds':time.time()-start,'counts':{'train':plan['N'],'validation':plan['validation_n']},'five_seeds':cfg['seeds'],'production_accepted':False,'sealed_access':False})
if __name__=='__main__':
 try:main()
 except Exception as e:write_json(RUN/'status.json',{'status':'DEVELOPMENT_COMPARISON_FAILED','error':repr(e),'sealed_access':False});raise
