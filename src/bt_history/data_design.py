"""Independent LHS batches, frozen families, old 448 preserved in train only."""
from collections import Counter
import copy
import json
from pathlib import Path
import numpy as np
from scipy.stats import qmc
from scipy.spatial import cKDTree
from .contracts import digest,file_hash,parameters
from .data_control import read_json,write_json

VERSION='shared10d_data_v1'
SEEDS={'train':2026092801,'validation':2026092802,'sealed_test':2026092803,'challenge_development':2026092804,'preflight':2026092805}

def generate(project):
    root=Path(project)
    frozen=root/'contracts/dataset_design.json'
    if frozen.exists():
        existing=read_json(frozen)
        if existing.get('development_amendment'):
            for path,sha in existing['manifest_sha256'].items():
                if file_hash(root/path)!=sha:raise ValueError('Frozen amended manifest changed')
            return existing
    c=read_json(root/'contracts/science_contract.json');order=c['parameter_order']
    views={k:read_json(root/'contracts'/k/'science_contract.json') for k in ['fixed','continuous_ms']}
    prior=np.array([c['prior_support'][k] for k in order]); astro=c['astro_parameter_order']
    batches=[]; rows={k:[] for k in SEEDS}
    def tags(p):
        out=[]
        for name,v in views.items():
            if all(p[k]==x for k,x in v['fixed_parameters'].items()) and all(v['prior_support'][k][0]<=p[k]<=v['prior_support'][k][1] for k in v['active_parameters']):out.append(name)
        return out
    def make(p,split,stratum,seed,*,sample_id=None,family=None,origin=None,engine='adapter'):
        p={k:float(p[k]) for k in order};parameters(c,p)
        sampler={'ETA_STAR':p['F_STAR10']-np.log10(p['t_STAR']),**{k:p[k] for k in astro if k!='F_STAR10'}}
        if 'continuous_ms' in tags(p):sampler['MS']=p['MS']
        return {'sample_id':sample_id or f'{split}_{len(rows[split]):06d}','family_id':family or 'theta_'+digest(p),'split':split,'stratum':stratum,'inference_view_tags':tags(p),'design_version':VERSION,'design_seed':seed,'canonical_parameters':p,'physical_parameters':p,'original_sampler_coordinates_if_applicable':sampler if tags(p) else None,'fixed_parameters':c['fixed_parameters'],'requested_ic_seed':c['ic_target']['seed'],'simulation_ic_seed':c['ic_target']['seed'],'effective_ic_seed':None,'model_initialization_seed':None,'science_contract_hash':digest(c),'engine':engine,'origin':origin or 'new_LHS'}
    def lhs(split,stratum,n,offset,fixed=None):
        seed=SEEDS[split]+offset
        v=qmc.scale(qmc.LatinHypercube(len(order),seed=seed).random(n),prior[:,0],prior[:,1])
        for point in v:
            p=dict(zip(order,point))
            if stratum in views:
                view=views[stratum];p.update(view['fixed_parameters'])
                for k in view['active_parameters']:
                    j=order.index(k);lo,hi=view['prior_support'][k];p[k]=lo+(point[j]-prior[j,0])/(prior[j,1]-prior[j,0])*(hi-lo)
            if fixed:p.update(fixed)
            rows[split].append(make(p,split,stratum,seed))
        batches.append({'split':split,'stratum':stratum,'count':n,'seed':seed,'method':'independent_LHS_batch_on_stored_coordinates'})
    old=read_json(root/'configs/proposed_448_point_design.json')
    for r in old:
        label=r['design_stratum'];stratum='broad' if label=='broad_rectangle' else 'fixed' if label=='fixed_view' else 'continuous_ms' if label=='continuous_ms_view' else 'anchors_edges'
        oldseed=20260928 if stratum=='broad' else 20260929 if stratum=='fixed' else 20260930 if stratum=='continuous_ms' else 20261001+int(label.rsplit('_',1)[1])
        rows['train'].append(make(r['physical_parameters'],'train',stratum,oldseed,sample_id=r['sample_id'],origin='immutable_448_design'))
    initial=copy.deepcopy(rows['train'])
    lhs('train','broad',2816,10);lhs('train','fixed',320,20);lhs('train','continuous_ms',320,30)
    # 32 PL families x 3 KP values = 96 points, plus 96 new edges, plus 64 old edges.
    points=qmc.scale(qmc.LatinHypercube(8,seed=SEEDS['train']+40).random(32),prior[:8,0],prior[:8,1])
    for i,v in enumerate(points):
        fam=f'train_PL_family_{i:03d}'
        for kp in [1.,10.,30.]:
            rows['train'].append(make({**dict(zip(astro,v)),'KP_h_Mpc':kp,'MS':.968},'train','anchors_edges',SEEDS['train']+40,family=fam,origin='PL_KP_family'))
    for i,fixed in enumerate([{'KP_h_Mpc':1.},{'KP_h_Mpc':30.},{'MS':.5},{'MS':4.}]):lhs('train','anchors_edges',24,50+i,fixed)
    for split,counts in [('validation',[256,128,128]),('sealed_test',[512,256,256])]:
        for i,(s,n) in enumerate(zip(['broad','fixed','continuous_ms'],counts)):lhs(split,s,n,10*(i+1))
    base=c['original_plan']['baseline_astro'];basep={**base,'KP_h_Mpc':10.,'MS':2.5}
    pf=[('normal_original',basep,'original'),('normal_adapter',basep,'adapter'),('PL1_original',{**base,'KP_h_Mpc':1.,'MS':.968},'original'),('PL1_adapter',{**base,'KP_h_Mpc':1.,'MS':.968},'adapter'),('PL10_adapter',{**base,'KP_h_Mpc':10.,'MS':.968},'adapter'),('PL30_adapter',{**base,'KP_h_Mpc':30.,'MS':.968},'adapter'),('continuous_original',{**base,'KP_h_Mpc':1.,'MS':1.5},'original'),('continuous_adapter',{**base,'KP_h_Mpc':1.,'MS':1.5},'adapter'),('strong_original',{**base,'KP_h_Mpc':1.,'MS':4.},'original'),('strong_adapter',{**base,'KP_h_Mpc':1.,'MS':4.},'adapter'),('normal_original_repeat',basep,'original'),('normal_adapter_repeat',basep,'adapter')]
    for name,p,e in pf: rows['preflight'].append(make(p,'preflight',name,SEEDS['preflight'],sample_id='preflight_'+name,family='preflight_PL' if name.startswith('PL') else 'theta_'+digest(p),origin='prespecified_parity',engine=e))
    # Challenge is independent of final test and carries its own separate budget.
    for i in range(12):
        p={k:float(sum(c['prior_support'][k])/2) for k in order}
        k=order[i%len(order)];p[k]=c['prior_support'][k][i//len(order)]
        rows['challenge_development'].append(make(p,'challenge_development','boundary_endpoint_risk',SEEDS['challenge_development'],origin='predefined_boundary'))
    lhs('challenge_development','numerical_and_transition_search',12,10)
    counts={s:dict(Counter(r['stratum'] for r in rr)) for s,rr in rows.items()}
    assert [len(rows[s]) for s in ['train','validation','sealed_test','preflight','challenge_development']]==[4096,512,1024,12,24]
    # Collision and family checks are validation, never post-hoc nearest-neighbor exclusions.
    exact={};rounded={};families={};repeated=[]
    for split,rr in rows.items():
        for r in rr:
            p=r['canonical_parameters'];key=digest(p);roundedkey=tuple(np.round((np.array(list(p.values()))-prior[:,0])/(prior[:,1]-prior[:,0]),12))
            if key in exact:
                prev=exact[key]
                if split!=prev['split'] or split not in ['preflight']:raise ValueError('Unexpected exact duplicate '+r['sample_id'])
                repeated.append([prev['sample_id'],r['sample_id']])
            if roundedkey in rounded and rounded[roundedkey]['split']!=split:raise ValueError('Rounding duplicate across splits')
            if r['family_id'] in families and families[r['family_id']]!=split:raise ValueError('Family leakage')
            exact[key]=r;rounded[roundedkey]=r;families[r['family_id']]=split
    prior_used=[]
    for name in ['fixed','continuous_ms']:
        for line in (root/'results'/f'{name}_quarantined_development.jsonl').read_text().splitlines():
            r=json.loads(line)
            if r.get('physical_parameters'):
                p={**r['physical_parameters'],**views[name]['fixed_parameters']};prior_used.append(digest(p))
    overlap=[r['sample_id'] for s,rr in rows.items() for r in rr if digest(r['canonical_parameters']) in prior_used]
    if any(r['sample_id'] in overlap for r in rows['sealed_test']):raise ValueError('Sealed design overlaps old used development records')
    files={'preflight':rows['preflight'],'train_initial_448':initial,'train_full_design':rows['train'],'validation_design':rows['validation'],'sealed_test_design':rows['sealed_test'],'challenge_development':rows['challenge_development']}
    manifests=root/'manifests';manifests.mkdir(exist_ok=True)
    hashes={}
    for name,rr in files.items():
        path=manifests/(name+'.jsonl');data=''.join(json.dumps(r,sort_keys=True,allow_nan=False)+'\n' for r in rr)
        if path.exists() and path.read_text()!=data:raise FileExistsError('Frozen manifest differs; new design version required')
        if not path.exists():path.write_text(data)
        hashes[str(path.relative_to(root))]=file_hash(path)
    train=np.array([[r['canonical_parameters'][k] for k in order] for r in rows['train']]);train=(train-prior[:,0])/(prior[:,1]-prior[:,0]);tree=cKDTree(train)
    nn={}
    for split in ['validation','sealed_test']:
        x=np.array([[r['canonical_parameters'][k] for k in order] for r in rows[split]]);x=(x-prior[:,0])/(prior[:,1]-prior[:,0]);dist,_=tree.query(x)
        nn[split]={'normalized_L2_to_train':dict(zip(['min','q50','q95','max'],np.quantile(dist,[0,.5,.95,1]).tolist())),'uses_parameters_only':True}
    d={'design_version':VERSION,'status':'PARAMETERS_FROZEN_LABELS_NOT_AUTHORIZED','science_contract_hash':digest(c),'counts':counts,'manifest_sha256':hashes,'independent_design_seeds':SEEDS,'batches':batches,'old_448_sha256':file_hash(root/'configs/proposed_448_point_design.json'),'old_448_allocation':'train_only; exact original IDs and coordinates preserved','method':'independent LHS batches plus declared anchors; concatenation is NOT one global LHS','sampling_distribution':'uniform in stored coordinates per LHS batch; original view priors preserved, oversampled mix not prior-unbiased','prespecified_PL_limit':.968,'duplicate_audit':{'cross_split_exact':0,'cross_split_rounded_12_normalized_decimals':0,'cross_split_families':0,'intentional_preflight_repeats':repeated,'old_development_parameter_overlaps':overlap},'geometry':nn,'seed_target':'fixed_ic; not a grouping key','no_labels_generated':True}
    path=root/'contracts/dataset_design.json'
    if path.exists() and read_json(path)!=d:raise FileExistsError('Frozen design contract differs')
    write_json(path,d)
    return d
