"""Frozen exact-data snapshot, train-only PCA audit and finite NNERO-style fit."""
import argparse,json,copy,sys,time
from pathlib import Path
import numpy as np
import torch
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'src'));sys.path.insert(0,str(Path(__file__).parent))
from bt_history.data_control import read_json,write_json,assert_development_path
from bt_history.contracts import file_hash
from bt_history.transforms import Normalizer
from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter
from bt_history.label_quality import validate_label
from bt_history.data_control import verify_design
from models import Classifier,PCAMLP

def load(snapshot):
 c=read_json(root/'contracts/science_contract.json');sel=read_json(root/'contracts/selected_native_contract.json');post=OriginalPostprocessingAdapter(c);protocol=read_json(root/'contracts/data_quality_protocol.json')
 m=read_json(snapshot);rows=[];designs={};seen=set()
 if m['role']!='development':raise PermissionError('Only explicit development snapshots')
 for it in m['files']:
  if it['split'] not in ['train','validation']:raise PermissionError('No sealed or mixed split')
  path=root/it['path'];assert_development_path(path,it['split'])
  if it['sample_id'] in seen or file_hash(path)!=it['sha256']:raise ValueError('Duplicate or changed label')
  seen.add(it['sample_id']);r=read_json(path);rp=read_json(root/it['receipt'])
  if not rp.get('qualified') or rp['label_sha256']!=it['sha256']:raise ValueError('Unqualified receipt')
  manifest=Path(r['provenance'].get('design',''))
  if not manifest.is_absolute():manifest=root/manifest
  if not manifest.is_file():
   # Initial recovery provenance preserves original label coordinates, not a new design.
   manifest=root/'manifests/train_full_design.jsonl' if it['split']=='train' else root/'manifests/validation_design.jsonl'
  if str(manifest) not in designs:designs[str(manifest)]={v['sample_id']:v for v in verify_design(root,manifest)}
  design=designs[str(manifest)][r['sample_id']]
  if design['split']!=it['split']:raise ValueError('Frozen split mismatch')
  validate_label(c,r,design,sel,protocol,post);rows.append({k:r[k] for k in ['sample_id','split','family_id','physical_parameters','redshifts','global_xHI','exact_tau','exact_xHI_at_observation_redshifts','quality_flags']} | {k:r[k] for k in ['original_end_to_end_success','LF_reference_status','stratum','inference_view_tags','fixed_parameters','ic_seed','science_contract_hash','source_native_config_hashes','provenance'] if k in r})
 return c,rows,post

def audit(c,train,val,post,transform,epsilon):
 exact=np.array([r['global_xHI'] for r in train]);v=np.array([r['global_xHI'] for r in val]);raw=exact.copy();vr=v.copy()
 if transform=='logit':
  exact=np.log(np.clip(exact,epsilon,1-epsilon)/(1-np.clip(exact,epsilon,1-epsilon)))
  v=np.log(np.clip(v,epsilon,1-epsilon)/(1-np.clip(v,epsilon,1-epsilon)))
 mean=exact.mean(0);_,_,basis=np.linalg.svd(exact-mean,full_matrices=False);records=[]
 for k in [4,8,12,16,20,24,28,32]:
  if k>len(basis):continue
  r=mean+((v-mean)@basis[:k].T)@basis[:k]
  if transform=='logit':r=1/(1+np.exp(-r))
  invalid=np.any((r<0)|(r>1)|~np.isfinite(r),axis=1);tau=[];obs=[];lt=[];lx=[]
  for row,x,bad in zip(val,r,invalid):
   if bad:continue
   ex=post.evaluate(row['physical_parameters'],row['redshifts'],row['global_xHI']);pr=post.evaluate(row['physical_parameters'],row['redshifts'],x)
   tau.append(abs(pr['tau']-ex['tau']));obs.append(abs(pr['xHI_obs']-ex['xHI_obs']));lt.append(abs(pr['logL_tau']-ex['logL_tau']));lx.append(abs(pr['logL_xHI']-ex['logL_xHI']))
  rmse=np.sqrt(np.mean((r-vr)**2,axis=1))
  records.append({'K':k,'trajectory_RMSE_q95':float(np.quantile(rmse,.95)),'invalid_reconstructed_histories':int(invalid.sum()),'absolute_delta_tau_q95':float(np.quantile(tau,.95)) if tau else None,'absolute_delta_xHI_5p9_q95':float(np.quantile(obs,.95)) if obs else None,'absolute_delta_logL_tau_q95':float(np.quantile(lt,.95)) if lt else None,'absolute_delta_logL_xHI_q95':float(np.quantile(lx,.95)) if lx else None,'numerical_representation_screen_pass':bool(not invalid.any() and np.quantile(rmse,.95)<.001 and tau and np.quantile(tau,.95)<.0001 and np.quantile(obs,.95)<.001 and np.quantile(lt,.95)<.01 and np.quantile(lx,.95)<.01)})
 return mean,basis,{'fit_split':'train_classifier_positive_only','evaluation_split':'validation_exact_classifier_positive','transform':transform,'epsilon':epsilon if transform=='logit' else None,'epsilon_bias_max_on_train_raw':float(np.max(abs(np.clip(raw,epsilon,1-epsilon)-raw))) if transform=='logit' else 0,'records':records,'screen_thresholds_status':'preregistered_development_representation_screen_NOT_scientific_acceptance','deployment_accepted':False}

def fit(model,x,y,vx,vy,cfg,kind,out):
 optimizer=torch.optim.AdamW(model.parameters(),lr=cfg['learning_rate'],weight_decay=cfg['weight_decay']);scheduler=torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer,mode='min',factor=.5,patience=cfg['scheduler_patience']);best=float('inf');state=None;curves=[];stale=0
 for epoch in range(cfg['epochs']):
  model.train();total=0
  for ix in torch.randperm(len(x)).split(cfg['batch_size']):
   optimizer.zero_grad();p=model(x[ix]);loss=torch.nn.functional.binary_cross_entropy_with_logits(p,y[ix]) if kind=='classifier' else ((p-y[ix])**2).mean()
   if not torch.isfinite(loss):raise FloatingPointError('Nonfinite loss')
   loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),cfg['gradient_clip']);optimizer.step();total+=float(loss)*len(ix)
  model.eval()
  with torch.no_grad():p=model(vx);loss=float(torch.nn.functional.binary_cross_entropy_with_logits(p,vy) if kind=='classifier' else ((p-vy)**2).mean())
  scheduler.step(loss)
  curves.append({'epoch':epoch,'train_loss':total/len(x),'validation_loss':loss})
  if loss<best:best=loss;state=copy.deepcopy(model.state_dict());stale=0;chosen=epoch
  else:stale+=1
  if stale>=cfg['early_stopping_patience']:break
 model.load_state_dict(state);torch.save(state,out);return {'selected_epoch':chosen,'minimum_validation_loss':best,'curves':curves}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--snapshot',required=True);ap.add_argument('--out',required=True);ap.add_argument('--train',action='store_true');a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
 c,rows,post=load(a.snapshot);tr=[r for r in rows if r['split']=='train'];va=[r for r in rows if r['split']=='validation'];cfg=read_json(root/'configs/training.json')
 x=np.array([[r['physical_parameters'][k] for k in c['parameter_order']] for r in tr]);vx=np.array([[r['physical_parameters'][k] for k in c['parameter_order']] for r in va]);norm=Normalizer.fit(x,split='train');tx=torch.tensor(norm.transform(x),dtype=torch.float32);tv=torch.tensor(norm.transform(vx),dtype=torch.float32)
 y=np.array([r['exact_xHI_at_observation_redshifts']['5.9']<.31 for r in tr]);vy=np.array([r['exact_xHI_at_observation_redshifts']['5.9']<.31 for r in va]);pt=[r for r,b in zip(tr,y) if b];pv=[r for r,b in zip(va,vy) if b]
 if len(pt)<32 or not pv:raise ValueError('Insufficient independent positive histories for PCA audit')
 candidates=[]
 for transform in ['physical','logit']:
  mean,basis,rep=audit(c,pt,pv,post,transform,1e-6);write_json(out/('PCA_'+transform+'_audit.json'),rep)
  passing=[r['K'] for r in rep['records'] if r['numerical_representation_screen_pass']]
  np.savez(out/('PCA_'+transform+'_basis.npz'),mean=mean,basis=basis)
  if passing:candidates.append((passing[0],transform,mean,basis))
 write_json(out/'normalizer.json',norm.as_dict());write_json(out/'plan.json',{'snapshot_sha256':file_hash(a.snapshot),'train_count':len(tr),'validation_count':len(va),'train_positive':len(pt),'validation_positive':len(pv),'classifier_threshold':.31,'classifier':[10,30,30,1],'regressor_hidden':[80]*6,'configuration':cfg,'negative_histories_retained':True,'PCA_selection':'minimum K passing all preregistered development representation screens; tie physical preferred','no_production_acceptance':True,'sealed_access':False})
 if not a.train:return
 torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
 for seed in cfg['seeds']:
  torch.manual_seed(seed);np.random.seed(seed);model=Classifier();rep=fit(model,tx,torch.tensor(y,dtype=torch.float32),tv,torch.tensor(vy,dtype=torch.float32),cfg,'classifier',out/('classifier_seed_%d.pt'%seed))
  with torch.no_grad():prob=torch.sigmoid(model(tv)).numpy()
  pred=prob>=.5;rep.update(seed=seed,false_negative_count=int((vy&~pred).sum()),false_positive_count=int((~vy&pred).sum()),accuracy=float(np.mean(pred==vy)),probability_threshold=.5)
  write_json(out/('classifier_seed_%d.json'%seed),rep)
  if candidates:
   k,transform,mean,basis=min(candidates,key=lambda t:(t[0],t[1]!='physical'));model=PCAMLP(mean,basis[:k],transform=transform);rep=fit(model,tx[y],torch.tensor([r['global_xHI'] for r in pt],dtype=torch.float32),tv[vy],torch.tensor([r['global_xHI'] for r in pv],dtype=torch.float32),cfg,'history',out/('regressor_seed_%d.pt'%seed));model.eval()
   with torch.no_grad():prediction=model(tv[vy]).numpy()
   invalid=np.any((prediction<0)|(prediction>1)|~np.isfinite(prediction),axis=1)
   rep.update(invalid_predicted_histories=int(invalid.sum()),physical_history_MAE_per_redshift=np.mean(abs(prediction-np.array([r['global_xHI'] for r in pv])),0).tolist())
   if not invalid.any():
    from bt_history.metrics import fidelity
    rep['fidelity']=fidelity(c,pv,prediction,post)
   else:rep['downstream_fidelity']='BLOCKED_INVALID_HISTORY; no clipping'
   write_json(out/('regressor_seed_%d.json'%seed),{'K':k,'transform':transform,**rep})
 write_json(out/'status.json',{'status':'DEVELOPMENT_TRAINING_COMPLETED' if candidates else 'CLASSIFIER_COMPLETED_REGRESSOR_BLOCKED_BY_PCA_AUDIT','scientific_deployment_accepted':False,'sealed_access':False})
if __name__=='__main__':main()
