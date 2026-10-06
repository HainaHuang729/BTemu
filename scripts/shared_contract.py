"""User-authorized 10D rectangular emulator domain; original inference views retained."""
import copy,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
c=json.loads((root/'contracts/fixed/science_contract.json').read_text())
c['contract_id']='bt_history_shared_10d_v1'
c['parameter_order']=c['astro_parameter_order']+['KP_h_Mpc','MS'];c['active_parameters']=c['parameter_order']
c['fixed_parameters']={}
c['prior_support'].update(KP_h_Mpc=[1.,30.],MS=[.5,4.])
c['parameter_units'].update(KP_h_Mpc='h/Mpc',MS='dimensionless')
c['parameter_transforms'].update(KP_h_Mpc='identity',MS='identity')
c['cosmology'].pop('KP');c['cosmology'].pop('MS')
c['domain_authorization']='User explicitly requested one 10D model over KP=[1,30] h/Mpc, MS=[0.5,4]; this changes training coverage, not existing inference priors.'
c['inference_views']={'fixed':{'contract':'fixed/science_contract.json','KP_h_Mpc':10.,'MS':2.5},'continuous_ms':{'contract':'continuous_ms/science_contract.json','KP_h_Mpc':1.,'MS_prior':[.5,2.]}}
c['sampler_order']='depends on inference view; no 10D production sampler started'
c['native_selection_status']='pending user confirmation of repaired versus historical audit native'
c['conflicts'].append('Continuous-MS source configuration fixes KP=1, while fixed source uses KP=10. Shared emulator uses explicit KP input and preserves each inference view.')
(root/'contracts/science_contract.json').write_text(json.dumps(c,indent=2)+'\n')
