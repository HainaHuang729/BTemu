"""Audit uploaded materials without running simulations, training or sampling."""
from pathlib import Path
import csv,hashlib,json,subprocess
import h5py
import numpy as np

B=Path(__file__).resolve().parent
ROOT=B.parents[1]
SOURCE=ROOT/'paper/paper_materials'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def split_monitor(a):
    half=len(a)//2;x=np.concatenate([a[:half],a[-half:]],axis=1)
    W=np.var(x,axis=0,ddof=1).mean(0);V=half*np.var(x.mean(0),axis=0,ddof=1)
    return np.sqrt(((half-1)/half*W+V/half)/W)

def main():
    revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    changed=subprocess.check_output(['git','diff','--name-only','1b83d5f..27b03de'],cwd=ROOT,text=True).splitlines()
    result={'source_revision':revision,'new_paths':[{'path':s,'sha256':sha(ROOT/s),'bytes':(ROOT/s).stat().st_size} for s in changed],'chains':{},'selection':'finite log_prob rows; no added chronological discard or thinning','monitor_definition':'Ordinary split variance-ratio statistic over interacting walkers, ddof=1, using complete ensemble steps after the last initial nonfinite log_prob; descriptive, not independent-run rank/folded convergence acceptance'}
    table=[];file_rows=[]
    for p in sorted((SOURCE/'chains_20261104').glob('*.h5')):
        receipt={'file':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size}
        try:
            with h5py.File(p,'r') as f:
                a=f['chain'][:];lp=f['log_prob'][:];names=[x.decode() if isinstance(x,bytes) else str(x) for x in f['parameter_names'][:]]
                receipt['attributes']={k:v.item() if isinstance(v,np.generic) else v for k,v in f.attrs.items()}
            assert a.ndim==3 and a.shape[2]==len(names) and lp.shape==a.shape[:2]
            assert np.isfinite(a).all() and not np.isnan(lp).any() and not np.isposinf(lp).any()
            valid=np.isfinite(lp);flat=a.reshape(-1,a.shape[-1])[valid.ravel()];qs=np.quantile(flat,[.025,.16,.5,.84,.975],axis=0)
            bad_steps=np.where(~valid.all(1))[0];start=int(bad_steps[-1]+1) if len(bad_steps) else 0;monitor=split_monitor(a[start:])
            receipt.update(status='readable',shape=list(a.shape),stored_rows=int(lp.size),rows=len(flat),excluded_nonfinite_log_prob=int((~valid).sum()),all_coordinates_finite=True,monitor_start_step_zero_based=start,parameters=names,summary={})
            for i,name in enumerate(names):
                s={'mean':float(flat[:,i].mean()),'std_ddof0':float(flat[:,i].std()),'q025':float(qs[0,i]),'q16':float(qs[1,i]),'median':float(qs[2,i]),'q84':float(qs[3,i]),'q975':float(qs[4,i]),'ordinary_split_monitor':float(monitor[i])}
                receipt['summary'][name]=s;table.append(dict(chain=p.stem,steps=len(a),walkers=a.shape[1],stored_rows=int(lp.size),retained_rows=len(flat),excluded_nonfinite_log_prob=int((~valid).sum()),parameter=name,**s))
        except (OSError,KeyError,AssertionError,ValueError) as e:
            receipt.update(status='not_readable_as_supplied',read_error=str(e))
        result['chains'][p.name]=receipt
        file_rows.append(dict(file=p.name,status=receipt['status'],steps=receipt.get('shape',[''])[0],stored_rows=receipt.get('stored_rows',''),retained_rows=receipt.get('rows',''),excluded_nonfinite_log_prob=receipt.get('excluded_nonfinite_log_prob',''),sha256=receipt['sha256']))
    reported=json.loads((SOURCE/'kpms8_rhat_20261105.json').read_text())
    result['reported_joined8']=dict(reported,reported_max_rhat=max(reported['rhat'].values()),above_1p05=[k for k,v in reported['rhat'].items() if v>1.05],raw_16018_step_chain_present=False,definition_and_retention_exported=False)
    result['availability']={'kp20_raw_verified':True,'PL_and_kp1_kp5_kp10_and_freeMS7D_raw_verified':True,'joined8_raw_missing':True,'new_100k_validation_predictions_missing':True,'accuracy_figure_is_source_raster':True,'PS10D_report_is_progress_snapshot':True,'particle_profiles_destination':'separate nonlinear structure manuscript'}
    (B/'MATERIAL_AUDIT_20261105.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    for name,rows in [('CHAIN_SUMMARIES_20261105.csv',table),('CHAIN_FILES_20261105.csv',file_rows)]:
        with (B/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    print('Audited',len(changed),'new files;',sum(v['status']=='readable' for v in result['chains'].values()),'readable chain files')
    print('Reported joined8 maximum:',result['reported_joined8']['reported_max_rhat'])
    for c in result['chains'].values():
        if c['status']=='readable':assert sha(ROOT/c['file'])==c['sha256']

if __name__=='__main__':main()
