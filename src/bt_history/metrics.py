import numpy as np

def quantiles(x):
    return dict(zip(['q50','q90','q95'], map(float,np.quantile(x,[.5,.9,.95]))))

def fidelity(c, rows, predictions, post, *, stratify=True):
    exact=np.asarray([r['global_xHI'] for r in rows],float)
    pred=np.asarray(predictions,float)
    if pred.shape!=exact.shape or not np.isfinite(pred).all(): raise ValueError('Prediction shape/nonfinite')
    error=pred-exact
    result={'n_trajectories':len(rows),'quantile_unit':'whole physical-parameter trajectory',
      'per_redshift_MAE':np.abs(error).mean(0).tolist(),'per_redshift_RMSE':np.sqrt(np.square(error).mean(0)).tolist(),
      'trajectory_RMSE':np.sqrt(np.square(error).mean(1)).tolist(),'trajectory_max_abs':np.abs(error).max(1).tolist(),
      'trajectory_RMSE_quantiles':quantiles(np.sqrt(np.square(error).mean(1))),
      'trajectory_max_abs_quantiles':quantiles(np.abs(error).max(1)),'regions':{}}
    for name,mask in [('low',exact<=.1),('high',exact>=.9),('transition',(exact>.1)&(exact<.9)),('exact_zero',exact==0),('exact_one',exact==1)]:
        n=mask.sum(1); keep=n>0
        vals=np.divide(np.where(mask,error**2,0).sum(1),n,out=np.zeros(len(n)),where=keep)
        result['regions'][name]={'n_trajectories':int(keep.sum()),'RMSE_quantiles':quantiles(np.sqrt(vals[keep])) if keep.any() else None}
    derived=[]; penalized=0
    for r,p in zip(rows,pred):
        a=post.evaluate(r['physical_parameters'],c['redshift_grid'],r['global_xHI'])
        b=post.evaluate(r['physical_parameters'],c['redshift_grid'],p)
        penalized+=a['logL_xHI']<0
        derived.append({k:b[k]-a[k] for k in a})
    result['derived_errors']=derived
    result['derived_absolute_quantiles']={k:quantiles(np.abs([d[k] for d in derived])) for k in derived[0]}
    result['tau_mean_bias']=float(np.mean([d['tau'] for d in derived]))
    result['penalized_xHI_trajectories']=int(penalized)
    result['LF']='unchanged by construction; end-to-end parity separately required'
    if stratify and 'KP_h_Mpc' in c['active_parameters']:
        groups={
            'fixed_view': [i for i,r in enumerate(rows) if r['physical_parameters']['KP_h_Mpc']==10 and r['physical_parameters']['MS']==2.5],
            'continuous_ms_view': [i for i,r in enumerate(rows) if r['physical_parameters']['KP_h_Mpc']==1 and .5<=r['physical_parameters']['MS']<=2],
            'BT_boundary': [i for i,r in enumerate(rows) if r['physical_parameters']['KP_h_Mpc'] in [1,30] or r['physical_parameters']['MS'] in [.5,4]]}
        result['target_regions']={name:fidelity(c,[rows[i] for i in ix],pred[ix],post,stratify=False) if ix else {'status':'missing_validation_coverage'} for name,ix in groups.items()}
    return result

def representation_audit(c, train, validation, post, ks, epsilon=1e-5, train_baseline=None, val_baseline=None):
    from scipy.special import expit
    from .transforms import logit, fit_pca
    x=np.asarray([r['global_xHI'] for r in train]); v=np.asarray([r['global_xHI'] for r in validation])
    u=logit(x,epsilon); uv=logit(v,epsilon)
    base=np.zeros_like(u) if train_baseline is None else logit(train_baseline,epsilon)
    bv=np.zeros_like(uv) if val_baseline is None else logit(val_baseline,epsilon)
    output={'epsilon':epsilon,'clipping_only':fidelity(c,validation,expit(uv),post),'by_K':{}}
    for k in ks:
        mean,basis=fit_pca(u-base,k,split='train')
        reconstructed=expit(bv+mean+(uv-bv-mean)@basis.T@basis)
        output['by_K'][str(k)]=fidelity(c,validation,reconstructed,post)
    return output

def posterior_reweight(exact_logl, emu_logl, theta):
    """Diagnostics only; caller must separately establish independent support overlap."""
    from scipy.special import logsumexp
    delta=np.asarray(exact_logl)-np.asarray(emu_logl)
    theta=np.asarray(theta,float)
    if delta.ndim!=1 or theta.ndim!=2 or len(delta)!=len(theta) or len(delta)<2 or not np.isfinite(delta).all() or not np.isfinite(theta).all(): raise ValueError('Invalid independent exact comparisons')
    w=np.exp(delta-logsumexp(delta)); mean=w@theta; centered=theta-mean
    cov=(centered*w[:,None]).T@centered
    widths=np.sqrt(np.diag(cov)); denom=np.outer(widths,widths)
    corr=np.divide(cov,denom,out=np.zeros_like(cov),where=denom>0)
    return {'ESS':float(1/np.sum(w*w)),'ESS_fraction':float(1/(len(w)*np.sum(w*w))),'max_weight':float(w.max()),'weighted_mean':mean.tolist(),'weighted_widths':widths.tolist(),'weighted_correlation':corr.tolist(),'unweighted_mean':theta.mean(0).tolist(),'unweighted_widths':theta.std(0).tolist(),'posterior_passed':False,'support_overlap':'requires independent evidence; cannot be established by reweighting alone'}

def trajectory_bootstrap(values, groups, *, resamples=2000, seed=20260930):
    """Cluster bootstrap: all IC of a physical parameter tuple move together."""
    values=np.asarray(values,float);groups=np.asarray(groups)
    unique=np.unique(groups)
    if len(unique)<2 or len(values)!=len(groups) or not np.isfinite(values).all():raise ValueError('Need >=2 independent finite groups')
    rng=np.random.default_rng(seed);statistics=[]
    for _ in range(resamples):
        sample=rng.choice(unique,len(unique),replace=True)
        v=np.concatenate([values[groups==g] for g in sample])
        statistics.append(np.quantile(v,.9))
    return {'statistic':'q90','resampling_unit':'physical-parameter group','resamples':resamples,'seed':seed,'CI95':np.quantile(statistics,[.025,.975]).tolist()}

def acceptance_gates(report, protocol, *, representation=False):
    """Proposed thresholds can never issue scientific acceptance."""
    t=protocol['thresholds'];f=protocol['representation_budget_fraction'] if representation else 1.
    q=report['derived_absolute_quantiles']
    checks={
      'history_RMSE':report['trajectory_RMSE_quantiles']['q95']<=f*t['trajectory_RMSE_q95_max'],
      'history_max':report['trajectory_max_abs_quantiles']['q95']<=f*t['trajectory_max_abs_q95_max'],
      'tau':q['tau']['q90']<=f*t['tau_abs_q90_max'],
      'tau_bias':abs(report['tau_mean_bias'])<=f*t['tau_abs_mean_bias_max'],
      'xHI_obs':q['xHI_obs']['q90']<=f*t['xHI_obs_abs_q90_max'],
      'tau_likelihood':q['logL_tau']['q90']<=f*t['delta_logL_tau_abs_q90_max'],
      'xHI_likelihood':q['logL_xHI']['q90']<=f*t['delta_logL_xHI_abs_q90_max'],
      'joint_likelihood':q['logL_joint_history']['q90']<=f*t['delta_logL_joint_abs_q90_max'],
      'penalized_xHI_present':report['penalized_xHI_trajectories']>=25}
    return {'checks':checks,'numerical_thresholds_met':all(checks.values()),'scientifically_accepted':protocol['status']=='CONFIRMED' and all(checks.values()),'posterior_accepted':False}
