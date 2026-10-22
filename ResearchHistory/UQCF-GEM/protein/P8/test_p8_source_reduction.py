import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def result():
    p=subprocess.run([sys.executable,str(ROOT/'p8_source_reduction.py')],capture_output=True,text=True,check=True)
    return json.loads(p.stdout)

def test_hashes_and_reopen_classification():
    r=result()
    assert r['globular_fold_qis']['hashes_match_freeze']
    assert r['stable_globular_qis_best']['hashes_match_freeze']
    assert r['classification']['p7_contact_only_reduction_applies_to_these_snapshots'] is False
    assert r['classification']['exact_named_patch_release_provenance'] is False

def test_compaction_persists_until_configured_lifetime():
    r=result()
    for name in ('globular_fold_qis','stable_globular_qis_best'):
        s=r[name]
        assert s['config_betti_threshold']==8
        assert s['config_dag_transition_lifetime']==100
        assert s['config_force_activation_lifetime']==50
        assert s['step0_transitioned'] is False and s['phase_after_step0']=='Compaction'
        assert s['step99_transitioned'] is False and s['phase_after_step99']=='Compaction'
        assert s['step100_transitioned'] is True and s['phase_after_step100']=='LockIn'

def test_lockin_adds_more_than_contacts():
    r=result()
    for name in ('globular_fold_qis','stable_globular_qis_best'):
        d=set(r[name]['phase1_minus_phase0'])
        assert 'contact_springs' in d
        assert 'screened_electrostatics' in d
    assert 'torsional_incoherence_penalty' in set(r['stable_globular_qis_best']['phase1_minus_phase0'])

def test_coordinate_paths_and_runner_order():
    r=result()
    for name in ('globular_fold_qis','stable_globular_qis_best'):
        s=r[name]
        assert s['fractal_loads_coords']
        assert s['electrostatics_loads_coords']
        assert s['history_before_dag'] and s['dag_before_force_loss'] and s['force_loss_before_backward']

def test_torsional_penalty_not_promoted_to_coordinate_force():
    r=result()
    assert r['stable_globular_qis_best']['torsional_phi_metric_rewrapped_as_tensor']
