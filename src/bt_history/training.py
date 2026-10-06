"""Finite preregistered five-seed training on accepted development labels."""
import copy, json, time
from pathlib import Path
import numpy as np
import torch
from .contracts import digest, parameters, file_hash
from .transforms import Normalizer
from .resmlp import ReionizationHistoryEmulator
from .metrics import fidelity

def save_json(path,value):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')

def train(c,rows,split,cfg,out,post):
    out=Path(out); out.mkdir(parents=True,exist_ok=False)
    tr=[r for r in rows if split[r['sample_id']]=='train']; va=[r for r in rows if split[r['sample_id']]=='validation']
    if len(tr)<cfg['minimum_train_groups'] or len(va)<cfg['minimum_validation_groups']:
        raise ValueError('Insufficient independent development groups; no scientific training')
    if len({digest(r['physical_parameters']) for r in tr}) != len(tr):
        raise ValueError('Fixed-IC training requires deduplicated physical groups')
    x=np.array([parameters(c,r['physical_parameters']) for r in tr]); vx=np.array([parameters(c,r['physical_parameters']) for r in va])
    norm=Normalizer.fit(x,split='train')
    tx=torch.tensor(norm.transform(x),dtype=torch.float32); vy=torch.tensor([r['global_xHI'] for r in va],dtype=torch.float32)
    ty=torch.tensor([r['global_xHI'] for r in tr],dtype=torch.float32); tv=torch.tensor(norm.transform(vx),dtype=torch.float32)
    save_json(out/'normalizer.json',norm.as_dict()); save_json(out/'split.json',split); save_json(out/'training_config.json',cfg)
    torch.set_num_threads(cfg['threads']); torch.use_deterministic_algorithms(True)
    predictions=[]; records=[]; start=time.perf_counter()
    for seed in cfg['seeds']:
        torch.manual_seed(seed); np.random.seed(seed)
        model=ReionizationHistoryEmulator(tx.shape[1],ty.shape[1],**cfg['architecture'])
        optimizer=torch.optim.AdamW(model.parameters(),lr=cfg['learning_rate'],weight_decay=cfg['weight_decay'])
        scheduler=torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer,mode='min',factor=.5,patience=cfg['scheduler_patience'])
        best=float('inf'); stale=0; curves=[]; best_state=None
        generator=torch.Generator().manual_seed(seed)
        for epoch in range(cfg['epochs']):
            model.train(); total=0.
            for ix in torch.randperm(len(tx),generator=generator).split(cfg['batch_size']):
                optimizer.zero_grad(set_to_none=True)
                loss=((model(tx[ix])-ty[ix])**2).mean()
                if not torch.isfinite(loss): raise FloatingPointError('Nonfinite history loss; seed must not be dropped')
                loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),cfg['gradient_clip']); optimizer.step()
                total+=float(loss.detach())*len(ix)
            model.eval()
            with torch.no_grad(): vl=float(((model(tv)-vy)**2).mean())
            if not np.isfinite(vl): raise FloatingPointError('Nonfinite validation')
            scheduler.step(vl); curves.append({'epoch':epoch,'train_history_mse':total/len(tx),'validation_history_mse':vl,'lr':optimizer.param_groups[0]['lr']})
            if vl<best:
                best=vl; best_state=copy.deepcopy(model.state_dict()); best_epoch=epoch; stale=0
            else: stale+=1
            if stale>=cfg['early_stopping_patience']: break
        model.load_state_dict(best_state); model.eval()
        with torch.no_grad(): pred=model(tv).numpy()
        predictions.append(pred)
        path=out/f'seed_{seed}.pt'; torch.save(best_state,path)
        metrics=fidelity(c,va,pred,post)
        save_json(out/f'seed_{seed}_curves.json',curves); save_json(out/f'seed_{seed}_metrics.json',metrics)
        records.append({'seed':seed,'checkpoint':path.name,'sha256':file_hash(path),'selected_epoch':best_epoch,'selection':'minimum development history MSE'})
    ensemble=np.mean(predictions,axis=0,dtype=np.float64)
    save_json(out/'ensemble_metrics.json',fidelity(c,va,ensemble,post))
    manifest={'model_version':out.name,'science_contract_hash':digest(c),'normalizer_sha256':file_hash(out/'normalizer.json'),'training_config_sha256':file_hash(out/'training_config.json'),'split_sha256':file_hash(out/'split.json'),'data_digest':digest(rows),'members':records,'decoder':'direct','production_accepted':False,'posterior_passed':False,'seconds':time.perf_counter()-start}
    save_json(out/'model_manifest.json',manifest)
    return manifest
