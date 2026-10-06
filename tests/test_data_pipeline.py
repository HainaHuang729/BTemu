import copy,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from bt_history.contracts import digest,file_hash,ContractError
from bt_history.data_control import read_json,read_design,verify_design,AttemptLedger,assert_development_path,check_execution_gate
from bt_history.history_dataset import split_groups,load_development
from bt_history.label_quality import validate_label,classify_failure,QualityError
ROOT=Path(__file__).resolve().parents[1]

class DataDesignTests(unittest.TestCase):
    def test_frozen_counts_and_hashes(self):
        for name,n in [('train_full_design',4096),('train_initial_448',448),('validation_design',512),('sealed_test_design',1024),('preflight',12),('challenge_development',24)]:
            self.assertEqual(len(verify_design(ROOT,ROOT/'manifests'/(name+'.jsonl'))),n)
    def test_448_exact_coordinates_and_ids_preserved(self):
        old=read_json(ROOT/'configs/proposed_448_point_design.json');new=read_design(ROOT/'manifests/train_initial_448.jsonl');full=read_design(ROOT/'manifests/train_full_design.jsonl')
        self.assertEqual(new,full[:448])
        for a,b in zip(old,new):self.assertEqual(a['sample_id'],b['sample_id']);self.assertEqual(a['physical_parameters'],b['canonical_parameters']);self.assertEqual(b['split'],'train')
    def test_families_and_duplicate_independence(self):
        seen={};fam={}
        for name in ['train_full_design','validation_design','sealed_test_design']:
            for row in read_design(ROOT/'manifests'/(name+'.jsonl')):
                key=digest(row['canonical_parameters']);self.assertNotIn(key,seen);seen[key]=name
                if row['family_id'] in fam:self.assertEqual(fam[row['family_id']],name)
                fam[row['family_id']]=name
    def test_PL_families_train_only(self):
        rows=[r for r in read_design(ROOT/'manifests/train_full_design.jsonl') if r['origin']=='PL_KP_family']
        self.assertEqual(len(rows),96)
        for family in {r['family_id'] for r in rows}:
            rr=[r for r in rows if r['family_id']==family];self.assertEqual({r['canonical_parameters']['KP_h_Mpc'] for r in rr},{1,10,30});self.assertEqual({r['canonical_parameters']['MS'] for r in rr},{.968})
    def test_frozen_split_never_randomized(self):
        rows=read_design(ROOT/'manifests/train_initial_448.jsonl')[:5]+read_design(ROOT/'manifests/validation_design.jsonl')[:5]
        self.assertEqual(split_groups(rows,seed=1),split_groups(rows,seed=999))
        self.assertEqual(sum(v=='validation' for v in split_groups(rows).values()),5)
        bad=copy.deepcopy(rows);bad[5]['family_id']=bad[0]['family_id']
        with self.assertRaises(ContractError):split_groups(bad)
    def test_sealed_rejected_as_training_split(self):
        with self.assertRaises(ContractError):split_groups(read_design(ROOT/'manifests/sealed_test_design.jsonl')[:5])
    def test_sealed_paths_and_symlinks_rejected_before_open(self):
        with tempfile.TemporaryDirectory() as d:
            sealed=Path(d)/'sealed_store';sealed.mkdir();target=sealed/'a.json';target.write_text('DO NOT READ');link=Path(d)/'alias.json';link.symlink_to(target)
            for p in [target,link,Path(d)/'x.gpg']:
                with self.assertRaises(PermissionError):assert_development_path(p,'development')
    def test_budget_zero_denies_before_native_import(self):
        with tempfile.TemporaryDirectory() as d:
            b=read_json(ROOT/'configs/data_stage_budgets.json');b.update(authorized=False,max_evaluations=0)
            path=Path(d)/'zero_budget.json';path.write_text(json.dumps(b))
            with self.assertRaises(PermissionError):check_execution_gate(ROOT,'preflight',path,ROOT/'manifests/preflight.jsonl',require_runtime=False)
    def test_no_legacy_records_transferred(self):
        s=read_json(ROOT/'results/dataset_status.json');self.assertEqual(s['legacy_transferred_to_train'],0);self.assertEqual(s['legacy_quarantined'],45)

class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.ledger=AttemptLedger(self.tmp.name)
        self.row={'sample_id':'a','family_id':'family_a'}
        self.spec={'max_attempts':3,'cpus':16,'wall_seconds':60,'max_reserved_core_hours':1,'max_retries_per_sample':1,'max_retry_attempts':1,'max_concurrent':1,'global_max_attempts':3}
    def reserve(self,row=None,spec=None):return self.ledger.reserve(row or self.row,'train',spec or self.spec,budget_hash='budget',contract_hash='contract')
    def test_unsettled_attempt_cannot_duplicate(self):
        self.reserve()
        with self.assertRaises(RuntimeError):self.reserve()
    def test_resume_qualified_skips_without_budget(self):
        a=self.reserve();self.ledger.finish(a,{'simulation_status':'success','qualified':True});self.assertIsNone(self.reserve());self.assertEqual(len(self.ledger.entries()),1)
    def test_retry_consumes_budget_and_keeps_id(self):
        a=self.reserve();self.ledger.finish(a,{'simulation_status':'timeout','qualified':False});b=self.reserve();self.assertEqual(b['sample_id'],'a');self.assertEqual(b['ordinal_for_sample'],2);self.assertNotEqual(a['attempt_id'],b['attempt_id'])
        self.ledger.finish(b,{'simulation_status':'timeout','qualified':False})
        with self.assertRaises(PermissionError):self.reserve()
    def test_numerical_failure_not_retried(self):
        a=self.reserve();self.ledger.finish(a,{'simulation_status':'numerical_failure','qualified':False})
        with self.assertRaises(PermissionError):self.reserve()
    def test_concurrency_cap(self):
        self.reserve()
        with self.assertRaises(PermissionError):self.reserve({'sample_id':'b','family_id':'b'})
    def test_core_hours_cap(self):
        s={**self.spec,'max_reserved_core_hours':0.01}
        with self.assertRaises(PermissionError):self.reserve(spec=s)
    def test_global_cap_across_stages(self):
        a=self.reserve();self.ledger.finish(a,{'simulation_status':'success','qualified':True})
        s={**self.spec,'global_max_attempts':1}
        with self.assertRaises(PermissionError):self.ledger.reserve({'sample_id':'b','family_id':'b'},'validation',s,budget_hash='b',contract_hash='c')

class QualityTests(unittest.TestCase):
    def setUp(self):
        self.c=read_json(ROOT/'contracts/science_contract.json');self.design=read_design(ROOT/'manifests/train_initial_448.jsonl')[0];self.selected=read_json(ROOT/'contracts/selected_native_contract.json');self.protocol=read_json(ROOT/'contracts/data_quality_protocol.json')
        self.r={**self.design,'redshifts':self.c['redshift_grid'],'global_xHI':np.linspace(.2,.8,32).tolist(),'native_sha256':self.selected['native_sha256'],'source_fingerprint':self.selected['source_fingerprint'],'physics_table_fingerprint':self.selected['physics_table_fingerprint'],'config_hash':digest(self.c),'postprocessing_hash':self.selected['postprocessing_hash'],'requested_ic_seed':725213656658,'effective_ic_seed':725213656658,'simulation_status':'success','tau_exact_derived':.05,'xHI_at_observation_redshifts':{'5.9':.3}}
        class Post:
            def evaluate(self,*args):return {'tau':.05,'xHI_obs':.3}
        self.post=Post()
    def qa(self):return validate_label(self.c,self.r,self.design,self.selected,self.protocol,self.post)
    def test_endpoint_warnings_do_not_discard_valid_labels(self):
        q=self.qa();self.assertTrue(q['qualified']);self.assertEqual(len(q['quality_flags']),2)
    def test_seed_cannot_silently_wrap(self):
        self.r['effective_ic_seed']=self.r['requested_ic_seed']%(2**32)
        with self.assertRaises(QualityError):self.qa()
    def test_tiny_range_preserved_and_quarantined(self):
        self.r['global_xHI'][0]=-1e-8
        with self.assertRaisesRegex(QualityError,'tiny_range'):self.qa()
        self.assertEqual(self.r['global_xHI'][0],-1e-8)
    def test_derived_mismatch_fails(self):
        self.r['tau_exact_derived']=.06
        with self.assertRaises(QualityError):self.qa()
    def test_failure_categories(self):
        self.assertEqual(classify_failure(ImportError('GLIBC_2.29 missing')),'runtime_native_load_failure');self.assertEqual(classify_failure(MemoryError()),'out_of_memory');self.assertEqual(classify_failure(FloatingPointError('nan')),'numerical_failure')

if __name__=='__main__':unittest.main()
