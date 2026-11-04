"""Post-review arithmetic audit. Run only after the three reports are frozen."""
from pathlib import Path
import json,re,hashlib
import numpy as np
B=Path(__file__).resolve().parent;P=B/'packet'
expected=['fd71d9757c5e64bf857233cde6be734eac3712d5ed57a4b5bcf082cab935b4ee','ede12bd330296e9d9235f01d5bdb13ba4edabe7e5b19078939f840532dbd9b7d','92d7cf61cc2de8ea32ff09798ef6095c332ca8d2aa7abc144036ee2c0bc8e03a']
for i,sha in enumerate(expected,1):assert hashlib.sha256((B/f'reviewer_{i}.md').read_bytes()).hexdigest()==sha
manifest=json.loads((B/'packet_manifest.json').read_text())
for name,sha in manifest.items():assert hashlib.sha256((P/name).read_bytes()).hexdigest()==sha
findings=[]
def add(id,status,location,claim,evidence,check,result,impact,resolution,overlap):
 findings.append(dict(audit_id=id,status=status,location=location,claim_pointer=claim,evidence_pointer=evidence,check=check,result=result,impact=impact,resolution_test=resolution,reviewer_overlap=overlap))
with np.load(P/'validation_predictions.npz',allow_pickle=False) as a:
 truth=a['truth'];avg=a['ensemble'];seeds=a['seeds'];ids=a['sample_ids']
 assert truth.shape==avg.shape==(512,32) and seeds.shape==(5,512,32) and len(set(ids))==512
 assert np.allclose(avg,seeds.mean(axis=0),atol=1e-14,rtol=0)
 stats={}
 for label,pred in [('average',avg),('seed11',seeds[0])]:
  e=np.sqrt(np.mean((pred-truth)**2,axis=1));stats[label]={'median':float(np.median(e)),'q95':float(np.quantile(e,.95))}
add('AUD-01','passed','Methods reported-history-accuracy and new-model-validation','Older validation metrics distinguish average and seed 11','validation_predictions.npz; methods_body.tex tab:accuracy','Recompute trajectory RMSE from all 512 histories and verify the arithmetic physical-output average',stats,'The older prediction-level results are reproducible; source old-model column mixing is already corrected in the manuscript','Retain separate predictor definitions','R1-M3; R2-M4 mention the distinction without asserting the old metrics fail')
m=json.loads((P/'metrics_100k.json').read_text())
add('AUD-02','aggregation_ambiguity','Methods new-model-validation; HTML validation table','The new q90 and RMSE values characterize the current predictor','metrics_100k.json; methods_body.tex tab:100k-validation','Inspect fields and supplied evaluation artifacts',{'training_n':m['N'],'split_n':m['validation_n'],'training_seeds':[s['seed'] for s in m['seeds']],'prediction_arrays_in_packet':False,'missing':['evaluated membership','prediction aggregation','signed/absolute q90 definitions']},'No matched improvement factor or current-predictor inference qualification can be reproduced','Supply the generating evaluation code and prediction/label pairs','R1-M3; R2-M4')
rows=[]
for key in ['kp10 / ms2.5','**kp1 / ms1.5**','kp5 / ms1.5']:
 line=next(l for l in (P/'results_20261104.md').read_text().splitlines() if l.startswith('| '+key+' |'))
 values=[float(v.replace('*','').strip().replace('−','-').split('±')[0]) for v in line.split('|')[2:7]];rows.append(values)
deltas={'kp1_minus_kp5_eta':rows[1][0]-rows[2][0],'kp1_minus_kp5_alpha':rows[1][1]-rows[2][1],'kp1_minus_kp10_eta':rows[1][0]-rows[0][0],'kp1_minus_kp10_alpha':rows[1][1]-rows[0][1]}
assert np.allclose(list(deltas.values()),[-.629,.088,-.702,.180],rtol=0,atol=1e-14)
add('AUD-03','passed','Physics fixed-spectrum-100k; HTML fixed table','Reported parameter-centre changes are transcribed correctly','results_20261104.md; physics_body.tex tab:fixed-100k','Subtract the tabulated centres directly',deltas,'Correct descriptive arithmetic; significance and run parity remain separate questions','Retain fixed-MS and jointly changed-spectrum comparisons separately','R1-M1')
ledger=(P/'timing_ledger.md').read_text();assert '943,695' in ledger and '26 h of core time' in ledger
add('AUD-04','confirmed_internal_error','Source timing ledger section 4, phase60 row','The source equates 26 hours of core time with 943695 core-seconds','timing_ledger.md phase60 sealed test row','Divide core-seconds by 3600',{'source_hours':26,'core_seconds':943695,'recomputed_core_hours':943695/3600},'The source ledger has an arithmetic contradiction. The visible HTML already uses the correct 262.14 core-h; no manuscript number is changed by this finding','Correct the source hours or identify a different accounting quantity. Do not replace the corrected HTML by the 26 h prose','No reviewer-local concern ID for this arithmetic finding')
add('AUD-05','unresolved_input_needed','Source timing ledger section 2; metrics_100k.json seconds','New training time is reported under two totals','timing_ledger.md 13 h 30 m; metrics_100k.json seconds','Convert JSON seconds to hours and compare with the ledger',{'json_seconds':m['seconds'],'json_hours':m['seconds']/3600,'ledger_hours':13.5,'difference_seconds':13.5*3600-m['seconds']},'Different elapsed scopes or a transcription could explain the discrepancy. Current HTML distinguishes the two values','Supply job ID, start/end and the scope of the JSON timer','No reviewer-local concern ID for this elapsed discrepancy')
counts={'6D_last_half_rows':(5000-2500)*32,'8D_last_half_rows':(5568-2784)*32,'exact200_all_rows':200*32,'exact200_T6_rows':100*32,'T3_joint_ext2_rows':1000*32}
assert list(counts.values())==[80000,89088,6400,3200,32000]
add('AUD-06','passed','Physics app:current-chains and app:t3-selection; methods finite comparison','Displayed retained counts follow the stated distinct selections','physics_body.tex and methods_body.tex chain construction; visible_html_content.txt','Multiply stated retained steps by 32 walkers',counts,'No count conflict is found between these distinct archived selections; this does not diagnose convergence','Preserve selection labels and avoid assigning old plots to new 100k chains','R1-M1; R2-M2; R3-M1 distinguish sample construction from inference qualification')
add('AUD-07','provenance_gap','Physics spectrum-modification and both likelihood definitions','The physical interpretation depends on the actual native spectrum, normalization and inference convention','physics_body.tex spectrum-modification author note; methods_body.tex likelihood/postprocessing paragraphs','Read explicit implementation qualifications in supplied texts','Native no-break numerical equivalence, complete deployed identities and optical-depth parity are not established by this packet','A contract formula is not a verified native implementation or a primordial-spectrum mapping','Supply frozen run/native records or restrict framing to the verified phenomenological family','R1-M4; R2-M3; R3-M3')
T=json.loads((P/'T7_summary.json').read_text())
add('AUD-08','not_assessable','Methods T7 summary and eq:t7-target-difference','IC target-difference summaries describe finite-reference likelihoods','T7_summary.json; methods_body.tex initial-condition-scatter-and-limits-of-inference','Inventory raw family histories and deployed predictions in packet','Family-level likelihood arrays and deployed predictions are not supplied; signed and absolute statistics cannot be reconstructed from aggregate JSON','The IC audit cannot be turned into a new-model error bound or universal error floor','Provide family-level histories/likelihoods and same-point deployed predictions','R1-M2; R2-M4; R3-M2')
(B/'forensic_audit.json').write_text(json.dumps({'reviewer_hashes_before_audit':expected,'packet_hashes_verified':True,'findings':findings},indent=2)+'\n')
print(json.dumps({'old_validation':stats,'counts':counts,'ledger_phase60_core_h':943695/3600,'findings':len(findings)}))
