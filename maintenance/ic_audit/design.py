"""Frozen development-only family selection and independent IC schedule."""
import sys,json,sqlite3,random,hashlib,math
import numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from bt_history.contracts import file_hash,digest
from bt_history.data_control import write_json
RUN=ROOT/'data_runs/ic_audit_v1'

def build():
 RUN.mkdir(parents=True,exist_ok=True)
 if (ROOT/'contracts/ic_audit_v1.json').exists():raise RuntimeError('Audit already frozen; do not redesign')
 c=json.loads((ROOT/'contracts/science_contract.json').read_text());n=c['likelihood']['neutral_fraction'];cut=n['threshold']+5*n['sigma_above_threshold']
 source=Path(c['original_project_root'])/'workflows/MCMC/fixed_btps_posterior/inference/non21_likelihood.py'
 cc={'status':'DERIVED_FROM_FROZEN_ORIGINAL_LIKELIHOOD','quantity':'volume_mean_global_xHI','redshift':n['redshift'],'observational_bound':n['threshold'],'sigma_above_bound':n['sigma_above_threshold'],'n_sigma':5,'cut':cut,'allowed_comparison':'xHI_5p9 < cut','boundary_equality':'negative at exact cut','delta_logL_at_cut':-12.5,'kernel':'one-sided penalty -0.5*((xHI-bound)/sigma)^2 above bound; zero below','model_error':0.0,'original_likelihood_source':str(source),'original_likelihood_source_sha256':file_hash(source),'classifier_probability_gate':None,'hard_gate_enabled':False,'reject_semantics':'No production reject implementation until independently validated; the exact likelihood remains finite at the cut.'}
 write_json(ROOT/'contracts/classifier_cut.json',cc,exclusive=True)
 (ROOT/'docs/classifier_cut_derivation.md').write_text('# 5-sigma classifier boundary\n\nThe frozen original neutral-fraction likelihood has zero penalty below xHI=0.06 and `-0.5*((xHI-0.06)/0.05)**2` above it, with model_error=0. Thus the 5-sigma observational exclusion boundary is **0.06 + 5*0.05 = 0.31**, giving delta logL=-12.5 at equality. Quantity: simulator-defined volume-average global_xHI, evaluated with the original interpolant at z=5.9.\n\nAll exact histories remain stored. Allowed/positive is xHI<0.31; equality is negative. This label is not a new prior and does not authorize replacing a finite likelihood by minus infinity. Classifier probability threshold, false-negative policy, and hard-gate semantics remain to be validated. NNERO Xe and this volume-mean xHI are distinct quantities.\n\nSource SHA256: `'+file_hash(source)+'`.\n')
 db=sqlite3.connect('file:'+str(ROOT/'data_runs/dataset_v2_100k/dataset_manifest.sqlite')+'?mode=ro',uri=True)
 # Scalar selection features only. No sealed registry or labels are accessed.
 candidates=[]
 for sid,split,xhi,metadata,item in db.execute('select id,split,xhi,metadata,item from labels'):
  m=json.loads(metadata);p=m['physical_parameters'];v=[(p[k]-c['prior_support'][k][0])/(c['prior_support'][k][1]-c['prior_support'][k][0]) for k in c['parameter_order']]
  candidates.append({'id':sid,'split':split,'xhi':xhi,'params':p,'v':v,'lf_valid':m['lf_valid'],'xhi_z10':m['global_xHI'][c['redshift_grid'].index(10.0)],'item':json.loads(item)})
 rng=random.Random(202610071);rng.shuffle(candidates);selected=[];used=set()
 vectors=np.array([v['v'] for v in candidates]);distances=np.full(len(candidates),np.inf)
 for j,v in enumerate(candidates):v['candidate_index']=j
 def choose(tag,predicate,count,key=None):
  pool=[v for v in candidates if v['id'] not in used and predicate(v)]
  if len(pool)<count:raise RuntimeError('Insufficient development candidates: '+tag)
  for _ in range(count):
   if key is not None:v=min(pool,key=key)
   elif not selected:v=pool[0]
   else:v=max(pool,key=lambda a:distances[a['candidate_index']])
   v=dict(v);v['selection_tag']=tag;selected.append(v);used.add(v['id']);distances[:]=np.minimum(distances,np.sum((vectors-vectors[v['candidate_index']])**2,axis=1));pool=[x for x in pool if x['id']!=v['id']]
 for ik,(kl,ku) in enumerate([(1,5),(5,15),(15,30.000001)]):
  for im,(ml,mu) in enumerate([(.5,.968),(.968,1.5),(1.5,4.000001)]):
   choose('KP_MS_cell_%d_%d'%(ik,im),lambda v,kl=kl,ku=ku,ml=ml,mu=mu:kl<=v['params']['KP_h_Mpc']<ku and ml<=v['params']['MS']<mu,4)
 for i,k in enumerate(c['parameter_order']):
  for side in [0,1]:choose('boundary_'+k+'_'+str(side),lambda v:True,1,key=lambda v,i=i,side=side:abs(v['v'][i]-side))
 choose('early',lambda v:v['xhi_z10']<.5,12)
 choose('intermediate',lambda v:.1<v['xhi']<.8,12)
 choose('late',lambda v:v['xhi']>.8,12)
 choose('near_cut_below',lambda v:v['xhi']<cut,12,key=lambda v:abs(v['xhi']-cut))
 choose('near_cut_above',lambda v:v['xhi']>=cut,12,key=lambda v:abs(v['xhi']-cut))
 choose('lf_valid',lambda v:v['lf_valid'],6)
 choose('lf_invalid_history_valid',lambda v:not v['lf_valid'],6)
 assert len(selected)==128
 ic_rng=random.Random(202610072);seeds=set();rows=[];families=[]
 for i,v in enumerate(selected):
  family='ic_audit_%03d'%i;original=json.loads((ROOT/v['item']['path']).read_text());assert file_hash(ROOT/v['item']['path'])==v['item']['sha256']
  assert original['effective_ic_seed']==c['ic_target']['seed'] and original['native_sha256']==c['native_sha256']
  families.append({'family_id':family,'canonical_parameters':v['params'],'source_sample_id':v['id'],'source_split':v['split'],'selection_tag':v['selection_tag'],'fixed_reference':v['item'],'lf_valid':v['lf_valid'],'fixed_xHI_5p9':v['xhi']})
  for s in range(8):
   seed=c['ic_target']['seed'] if s==0 else ic_rng.randrange(1,2**31)
   while s and (seed in seeds or seed==c['ic_target']['seed']):seed=ic_rng.randrange(1,2**31)
   if s:seeds.add(seed)
   rows.append({'sample_id':family+'_ic%d'%s,'family_id':family,'split':'challenge_development','stratum':v['selection_tag'],'design_version':'IC_AUDIT_V1','design_seed':202610071,'ic_design_seed':202610072,'realization_index':s,'canonical_parameters':v['params'],'requested_ic_seed':seed,'reuse_fixed_reference':s==0,'source_split':v['split'],'source_sample_id':v['id'],'fixed_reference':v['item'],'lf_valid':v['lf_valid']})
 manifest=ROOT/'manifests/ic_audit_v1.jsonl';manifest.write_text(''.join(json.dumps(v,sort_keys=True)+'\n' for v in rows))
 write_json(RUN/'families.json',families,exclusive=True)
 contract={'version':'IC_AUDIT_V1','status':'FROZEN_AUDIT_ONLY','base_science_contract_sha256':file_hash(ROOT/'contracts/science_contract.json'),'base_science_contract_hash':digest(c),'native_sha256':c['native_sha256'],'manifest':str(manifest.relative_to(ROOT)),'manifest_sha256':file_hash(manifest),'families_sha256':file_hash(RUN/'families.json'),'theta_count':128,'ICs_per_theta':8,'existing_fixed_IC_realizations':128,'new_complete_evaluations':896,'theta_design_seed':202610071,'ic_design_seed':202610072,'random_seed_generator':'Python random.Random MT19937 with frozen explicit schedule; integers uniform in [1, 2**31-1], unique across fresh audit realizations','native_seed_policy':'Requested integer passed unchanged via existing API; effective coeval seed must equal requested. No modulo or rounding. Fixed seed remains 725213656658. Native GSL MT19937 uses master seed; thread count frozen at 16.','network_input_seed':False,'family_split_policy':'All ICs stay in one development audit family; no audit family is a sealed final test.','single_IC_production_authorized_before_pass':False,'statistical_target_caveat':'Mean history and mean likelihood need not commute; verify both. Arithmetic mean in physical xHI. Eight ICs estimate finite-box scatter, not guarantee cosmological ensemble convergence.','classifier_cut_sha256':file_hash(ROOT/'contracts/classifier_cut.json'),'sealed_access':False}
 write_json(ROOT/'contracts/ic_audit_v1.json',contract,exclusive=True)
 print(json.dumps({'families':128,'manifest_rows':1024,'fixed_reused':128,'new_evaluations':896,'positive_selected':sum(v['xhi']<cut for v in selected),'LF_invalid_selected':sum(not v['lf_valid'] for v in selected)}))
if __name__=='__main__':build()
