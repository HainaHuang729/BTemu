"""Freeze independent Sobol designs without altering v1 manifests or any labels."""
import sys,json,hashlib,copy,sqlite3
from pathlib import Path
import numpy as np
from scipy.stats import qmc
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'src'))
from bt_history.data_control import read_json,write_json
from bt_history.contracts import digest,file_hash
VERSION='dataset_design_v2_100k'

def generate():
 out=root/'contracts/dataset_design_v2_100k.json'
 if out.exists():
  d=read_json(out)
  for p,h in d['manifest_sha256'].items():
   if file_hash(root/p)!=h:raise ValueError('Frozen v2 changed')
  return d
 c=read_json(root/'contracts/science_contract.json');order=c['parameter_order'];bounds=np.array([c['prior_support'][k] for k in order]);views={k:read_json(root/'contracts'/k/'science_contract.json') for k in ['fixed','continuous_ms']}
 old=read_json(root/'contracts/dataset_design.json');used=set();rounded=set()
 for f in old['manifest_sha256']:
  for line in (root/f).read_text().splitlines():
   r=json.loads(line);p=r['canonical_parameters'];used.add(tuple(p[k] for k in order));rounded.add(tuple(np.round((np.array([p[k] for k in order])-bounds[:,0])/(bounds[:,1]-bounds[:,0]),12)))
 target=root/'manifests/v2_100k';target.mkdir(exist_ok=True);hashes={};stages={};batches=[]
 def tag(p):
  return [name for name,v in views.items() if all(p[k]==x for k,x in v['fixed_parameters'].items()) and all(v['prior_support'][k][0]<=p[k]<=v['prior_support'][k][1] for k in v['active_parameters'])]
 def sample(point,split,kind,seed,number):
  p={k:float(v) for k,v in zip(order,point)}
  if kind in views:
   view=views[kind];p.update(view['fixed_parameters'])
   for k in view['active_parameters']:
    j=order.index(k);lo,hi=view['prior_support'][k];p[k]=lo+(point[j]-bounds[j,0])/(bounds[j,1]-bounds[j,0])*(hi-lo)
  if kind=='boundary':
   axis=number%10;p[order[axis]]=float(bounds[axis,(number//10)%2])
  key=tuple(p[k] for k in order);rk=tuple(np.round((np.array(key)-bounds[:,0])/(bounds[:,1]-bounds[:,0]),12))
  if key in used or rk in rounded:raise ValueError('Duplicate design point; reject design version')
  used.add(key);rounded.add(rk)
  sid='v2_'+split+'_%06d'%number
  return {'sample_id':sid,'family_id':'theta_'+digest(p),'split':split,'stratum':kind,'inference_view_tags':tag(p),'design_version':VERSION,'design_seed':seed,'canonical_parameters':p,'physical_parameters':p,'original_sampler_coordinates_if_applicable':None,'fixed_parameters':c['fixed_parameters'],'requested_ic_seed':c['ic_target']['seed'],'simulation_ic_seed':c['ic_target']['seed'],'effective_ic_seed':None,'model_initialization_seed':None,'science_contract_hash':digest(c),'engine':'adapter','origin':'scrambled_Sobol_prespecified_stratum'}
 for split,n,extra,seed in [('train',95904,4096,2026100401),('validation',10000,1024,2026100402),('sealed_test',5000,0,2026100403)]:
  size=n+extra;m=int(np.ceil(np.log2(size)));engine=qmc.Sobol(10,scramble=True,seed=seed);x=qmc.scale(engine.random_base2(m),bounds[:,0],bounds[:,1])
  # Declare a prefix of a balanced base2 draw, never call the filtered/stratified output balanced Sobol.
  chunks=[];buf=[];counts={}
  for i,point in enumerate(x[:size]):
   if split=='train' and i<n:
    residue=i%10;kind='broad' if residue<8 else ('fixed' if (i//10)%2==0 else 'continuous_ms') if residue==8 else 'boundary'
   else:kind='broad' if i<n else 'reserve_broad'
   r=sample(point,split,kind,seed,i);counts[kind]=counts.get(kind,0)+1;buf.append(r)
   if len(buf)==512 or i==size-1:
    f=target/('%s_%04d.jsonl'%(split,len(chunks)));data=''.join(json.dumps(v,sort_keys=True,allow_nan=False)+'\n' for v in buf)
    if f.exists():
     if f.read_text()!=data:raise ValueError('Partial design differs; refusing overwrite')
    else:
     with f.open('x') as h:h.write(data)
    rel=str(f.relative_to(root));hashes[rel]=file_hash(f);chunks.append({'manifest':rel,'count':len(buf),'first_design_index':i-len(buf)+1,'reserve':i-len(buf)+1>=n});buf=[]
  stages[split]=chunks;batches.append({'split':split,'primary_new':n,'finite_reserves':extra,'counts':counts,'design_seed':seed,'base2_draw_count':2**m,'used_prefix_count':size,'method':'scrambled Sobol prefix plus declared train view/boundary mappings; NOT a balanced global Sobol net'})
 d={'design_version':VERSION,'science_contract_hash':digest(c),'preserved_v1_design_sha256':file_hash(root/'contracts/dataset_design.json'),'existing_train_design':'manifests/train_full_design.jsonl','existing_train_count':4096,'existing_train_labels_counted_only_if_qualified':True,'target_totals':{'train':100000,'validation':10000,'sealed_test_design':5000},'manifest_sha256':hashes,'stages':stages,'batches':batches,'classifier':{'threshold':.31,'positive_if':'original interpolated volume-mean xHI(5.9) < threshold','negative_histories_retained':True},'deduplication':{'exact_cross_split_collisions':0,'normalized_rounded_12_digit_collisions':0,'checked_against_all_v1_designs':True},'sealed_labels_generation_authorized':False,'reserves_policy':'Frozen finite independent candidates used only after primary attempts, original denominator/failures retained; stop when target qualified count reached; no infinite replacement.'}
 write_json(out,d,exclusive=True)
 write_json(root/'contracts/learning_curve_v2.json',{'design_sha256':file_hash(out),'sizes':[1024,2048,4096,8192,16384,32768,65536,100000],'nesting':'first existing v1 train design, then frozen v2 train order; preserve PL families together; unavailable labels explicitly flagged','validation_v1_benchmark_preserved':True,'validation_v2_independent':True,'PCA_train_only':True,'PCA_K_candidates':[4,8,12,16,20,24,28,32],'classifier_hidden':[30,30],'regressor_hidden':[80]*6,'threshold':.31,'threshold_is_not_prior':True},exclusive=True)
 return d
if __name__=='__main__':
 d=generate();print(json.dumps({'version':d['design_version'],'counts':d['target_totals'],'shards':len(d['manifest_sha256'])}))
