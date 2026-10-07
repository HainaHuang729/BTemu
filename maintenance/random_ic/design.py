"""Independent random-IC v2 designs; parameter-only sealed designs, no labels."""
import sys,json,random,sqlite3,struct,time
from pathlib import Path
import numpy as np
from scipy.stats import qmc
sys.path.insert(0,str(Path(__file__).parent))
from common import ROOT,RUN,read_json,write_json,file_hash,digest

def generate():
 dest=ROOT/'contracts/dataset_design_random_ic_v2.json'
 if dest.exists():
  d=read_json(dest)
  for f,h in d['manifest_sha256'].items():
   if file_hash(ROOT/f)!=h:raise ValueError('Frozen random design differs')
  if file_hash(RUN/'design.sqlite')!=d['index_sha256']:raise ValueError('Frozen random index differs')
  return d
 # Archive only this new version's incomplete design work, never labels or older designs.
 stamp=str(time.time_ns())
 for f in [RUN/'design.sqlite',RUN/'design.sqlite-journal']:
  if f.exists():f.rename(f.with_name(f.name+'.incomplete_'+stamp))
 prior=ROOT/'manifests/random_ic_v2'
 if prior.exists():prior.rename(prior.with_name('random_ic_v2_incomplete_'+stamp))
 c=read_json(ROOT/'contracts/science_contract.json');order=c['parameter_order'];bounds=np.array([c['prior_support'][k] for k in order]);db=sqlite3.connect(RUN/'design.sqlite');db.execute('CREATE TABLE seen(exact BLOB PRIMARY KEY, rounded BLOB UNIQUE)')
 # Parameter designs only; no existing sealed labels or derived statistics accessed.
 for oldname in ['dataset_design.json','dataset_design_v2_100k.json']:
  old=read_json(ROOT/'contracts'/oldname)
  for f in old['manifest_sha256']:
   for line in (ROOT/f).open():
    p=json.loads(line)['canonical_parameters'];key=tuple(p[k] for k in order);rk=tuple(np.round((np.array(key)-bounds[:,0])/(bounds[:,1]-bounds[:,0]),12));db.execute('INSERT OR IGNORE INTO seen VALUES(?,?)',(struct.pack('<10d',*key),struct.pack('<10d',*rk)))
 views={k:read_json(ROOT/'contracts'/k/'science_contract.json') for k in ['fixed','continuous_ms']}
 seedrng=random.Random(202610073);seeds={725213656658,725213656658&0xffffffff}
 for line in (ROOT/'manifests/ic_audit_v1.jsonl').read_text().splitlines():seeds.add(json.loads(line)['requested_ic_seed'])
 target=ROOT/'manifests/random_ic_v2';target.mkdir(exist_ok=True);hashes={};stages={};global_index=0
 db.execute('CREATE TABLE design(idx INTEGER PRIMARY KEY,split TEXT,primary_point INTEGER,payload TEXT)')
 for split,n,reserve,designseed in [('train',100000,4096,2026100701),('validation',10000,1024,2026100702),('sealed_test',5000,0,2026100703)]:
  m=int(np.ceil(np.log2(n+reserve)));x=qmc.scale(qmc.Sobol(10,scramble=True,seed=designseed).random_base2(m),bounds[:,0],bounds[:,1]);buf=[];chunks=[];counts={}
  for i,v in enumerate(x[:n+reserve]):
   p={k:float(a) for k,a in zip(order,v)};kind='broad' if i<n else 'reserve_broad'
   if split=='train' and i<n:
    residue=i%10
    if residue==8:
     kind='fixed' if (i//10)%2==0 else 'continuous_ms';view=views[kind];p.update(view['fixed_parameters'])
     for k in view['active_parameters']:
      j=order.index(k);lo,hi=view['prior_support'][k];p[k]=lo+(v[j]-bounds[j,0])/(bounds[j,1]-bounds[j,0])*(hi-lo)
    elif residue==9:kind='boundary';axis=(i//10)%10;p[order[axis]]=float(bounds[axis,((i//10)//10)%2])
   key=tuple(p[k] for k in order);rk=tuple(np.round((np.array(key)-bounds[:,0])/(bounds[:,1]-bounds[:,0]),12))
   try:db.execute('INSERT INTO seen VALUES(?,?)',(struct.pack('<10d',*key),struct.pack('<10d',*rk)))
   except sqlite3.IntegrityError:raise ValueError('Duplicate theta: refuse frozen design')
   seed=seedrng.randint(1,2**31-1)
   while seed in seeds:seed=seedrng.randint(1,2**31-1)
   seeds.add(seed)
   tags=[name for name,view in views.items() if all(p[k]==a for k,a in view['fixed_parameters'].items()) and all(view['prior_support'][k][0]<=p[k]<=view['prior_support'][k][1] for k in view['active_parameters'])]
   r=dict(sample_id=f'random_v2_{split}_{i:06d}',family_id='theta_'+digest(p),split=split,stratum=kind,inference_view_tags=tags,design_version='random_ic_v2',design_seed=designseed,ic_design_seed=202610073,requested_ic_seed=seed,effective_ic_seed=None,canonical_parameters=p,physical_parameters=p,fixed_parameters=c['fixed_parameters'],global_design_index=global_index,primary_point=i<n,base_science_contract_hash=digest(c),lf_valid=None)
   payload=json.dumps(r,sort_keys=True,allow_nan=False);db.execute('INSERT INTO design VALUES(?,?,?,?)',(global_index,split,int(i<n),payload));buf.append(payload+'\n');global_index+=1;counts[kind]=counts.get(kind,0)+1
   if len(buf)==512 or i==n+reserve-1:
    f=target/f'{split}_{len(chunks):04d}.jsonl'
    with f.open('x') as h:h.writelines(buf)
    rel=str(f.relative_to(ROOT));hashes[rel]=file_hash(f);chunks.append({'manifest':rel,'count':len(buf)});buf=[]
  stages[split]={'unique_primary':n,'finite_reserves':reserve,'design_seed':designseed,'base2_draw':2**m,'used_prefix':n+reserve,'counts':counts,'shards':chunks}
 db.execute("DROP TABLE seen");db.commit();db.close()
 d={'version':'random_ic_v2','status':'FROZEN_PARAMETERS_PENDING_IC_AUDIT','base_science_contract_sha256':file_hash(ROOT/'contracts/science_contract.json'),'native_sha256':c['native_sha256'],'parameter_order':order,'target_unique_theta':{'train':100000,'validation':10000,'sealed_test_design':5000},'random_IC_policy':'one unique seed per theta only if full audit supports it; seed passed unchanged, never network input','ic_design_seed':202610073,'method':'independent scrambled Sobol base2 draws, prefixes and explicit 80/10/10 train stratum mappings; not a globally balanced Sobol net','manifest_sha256':hashes,'index_sha256':file_hash(RUN/'design.sqlite'),'stages':stages,'deduplication':'exact and normalized rounded-12 digits across splits and all v1/fixed-v2 parameter designs; no sealed scientific labels accessed','fixed_IC_labels_counted_as_random':False,'sealed_generation_authorized':False,'finite_reserve_policy':'Primary points attempted first; only finite reserves to meet qualified targets; preserve every failed denominator, never hide conditional-success sampling'}
 write_json(dest,d,exclusive=True);write_json(ROOT/'contracts/learning_curve_random_ic_v2.json',{'nested_N':[1000,2000,4000,8000,16000,32000,64000,100000],'membership':'qualified Train in frozen design order, never use Validation/Sealed or fixed-IC labels','normalization_and_PCA':'train-only; positive subset for PCA','must_record_available_N':True,'design_sha256':file_hash(dest)},exclusive=True)
 return d
if __name__=='__main__':print(json.dumps(generate()['target_unique_theta']))
