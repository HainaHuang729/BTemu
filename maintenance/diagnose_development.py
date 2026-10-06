"""Trajectory diagnostics on frozen development labels, without new simulations."""
import sys,json,os
from pathlib import Path
import numpy as np
root=Path(sys.argv[1]);run=Path(sys.argv[2]);sys.path.insert(0,str(root/'src'))
from bt_history.data_control import read_json,write_json
from bt_history.contracts import file_hash,read_contract,parameters
from bt_history.runtime_qualification import inspect_runtime
from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter
from bt_history.history_dataset import load_development
from bt_history.transforms import Normalizer
from bt_history.resmlp import ReionizationHistoryEmulator
import torch
try:
 assert os.environ.get('SLURM_JOB_ID') and os.uname().nodename.split('.')[0] in ['chpc-cn%03d'%n for n in range(57,65)]
 assert inspect_runtime(root)['qualified_for_full_simulation']
 torch.set_num_threads(1);c=read_contract(root/'contracts/science_contract.json');rows,_=load_development(run/'manifest.json',c,OriginalPostprocessingAdapter(c));tr=[r for r in rows if r['split']=='train'];va=[r for r in rows if r['split']=='validation'];out=run/'diagnostics';out.mkdir(exist_ok=True)
 trained=run/'direct_resmlp';cfg=read_json(trained/'training_config.json');manifest=read_json(trained/'model_manifest.json');nm=read_json(trained/'normalizer.json');norm=Normalizer(nm['mean'],nm['scale'])
 tx=norm.transform(np.array([parameters(c,r['physical_parameters']) for r in tr]));vx=norm.transform(np.array([parameters(c,r['physical_parameters']) for r in va]));tensor=torch.tensor(vx,dtype=torch.float32);pred=[]
 for member in manifest['members']:
  path=trained/member['checkpoint'];assert file_hash(path)==member['sha256'];model=ReionizationHistoryEmulator(10,32,**cfg['architecture']);model.load_state_dict(torch.load(path,map_location='cpu',weights_only=True));model.eval()
  with torch.no_grad():pred.append(model(tensor).numpy())
 predictions=np.mean(pred,axis=0,dtype=np.float64);exact=np.asarray([r['global_xHI'] for r in va]);error=predictions-exact;rmse=np.sqrt((error**2).mean(1));near=np.sqrt(((vx[:,None,:]-tx[None,:,:])**2).sum(2));nearest=near.min(1)
 # Confirm regenerated predictions reproduce saved validation metrics.
 saved=read_json(trained/'ensemble_metrics.json');assert np.allclose(rmse,saved['trajectory_RMSE'],atol=1e-12,rtol=0)
 details=[]
 for i in np.argsort(-rmse):
  row=va[i];d=saved['derived_errors'][i];details.append({'sample_id':row['sample_id'],'physical_parameters':row['physical_parameters'],'stratum':row['stratum'],'inference_view_tags':row.get('inference_view_tags',[]),'trajectory_RMSE':float(rmse[i]),'trajectory_max_abs_error':float(abs(error[i]).max()),'nearest_train_distance_train_standardized':float(nearest[i]),'nearest_train_sample_id':tr[int(near[i].argmin())]['sample_id'],'delta_tau':d['tau'],'delta_xHI_obs':d['xHI_obs'],'delta_logL_tau':d['logL_tau'],'delta_logL_xHI':d['logL_xHI'],'xHI_z5_exact':float(exact[i,0]),'xHI_z35_exact':float(exact[i,-1]),'LF_reference_valid':not row.get('original_end_to_end_success') is False})
 curves=[]
 for member in manifest['members']:
  seed=member['seed'];cs=read_json(trained/f'seed_{seed}_curves.json');selected=cs[member['selected_epoch']];last=cs[-1];curves.append({'seed':seed,'epochs_executed':len(cs),'selected_epoch':member['selected_epoch'],'selected_train_MSE':selected['train_history_mse'],'selected_validation_MSE':selected['validation_history_mse'],'last_train_MSE':last['train_history_mse'],'last_validation_MSE':last['validation_history_mse'],'last_LR':last['lr'],'all_seeds_retained':True})
 write_json(out/'trajectory_diagnostics.json',{'n_train':len(tr),'n_validation':len(va),'validation_is_development_only':True,'sorted_trajectory_errors':details,'training_curves_summary':curves,'correlation_RMSE_vs_nearest_train_distance':float(np.corrcoef(rmse,nearest)[0,1]),'interpretation':'Training loss decreases while validation error often worsens; generalization gap observed. No cause assigned from correlation alone.','labels_or_architecture_changed':False,'sealed_access':False,'new_exact_evaluations':0})
 np.savez(out/'validation_predictions.npz',redshifts=np.asarray(c['redshift_grid']),exact=exact,ensemble=predictions,member_predictions=np.stack(pred),sample_ids=np.asarray([r['sample_id'] for r in va]))
 import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
 fig,axs=plt.subplots(2,4,figsize=(14,6),sharex=True,sharey=True)
 for ax,i in zip(axs.flat,np.argsort(-rmse)[:8]):
  ax.plot(c['redshift_grid'],exact[i],label='Exact BT',linewidth=1.8);ax.plot(c['redshift_grid'],predictions[i],label='Direct ensemble',linewidth=1.5);ax.set_title(va[i]['sample_id']+'\nRMSE %.3f'%rmse[i],fontsize=9);ax.set_ylim(-.02,1.02);ax.set_xlabel('Redshift');ax.set_ylabel('Volume mean xHI')
 axs.flat[0].legend(fontsize=8);fig.suptitle('Eight largest history errors: frozen development validation; no label edits');fig.tight_layout();fig.savefig(out/'worst_history_trajectories.png',dpi=160);plt.close(fig)
 write_json(out/'status.json',{'status':'DIAGNOSTICS_COMPLETED','job_id':os.environ['SLURM_JOB_ID'],'n_validation':len(va),'sealed_access':False});print('Diagnostics completed',flush=True)
except Exception as error:
 write_json(run/'diagnostic_failure.json',{'error':repr(error),'job_id':os.environ.get('SLURM_JOB_ID')});raise
