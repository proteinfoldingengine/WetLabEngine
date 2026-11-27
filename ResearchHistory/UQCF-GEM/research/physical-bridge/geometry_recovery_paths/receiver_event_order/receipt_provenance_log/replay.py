"""Trace the historical receipt object to the logged JSON and identify its reader."""
from copy import deepcopy
from hashlib import sha1, sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import json
import re
import subprocess
import sys

PIN = 'e61d5b0e827f7b412824ad46021e2ad6cc6f7875'
DEMO = Path('ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure')
ARCHIVE = DEMO / 'completion/evidence/historical-producer.log'


def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args]).decode().strip()


def blob(raw):
    return sha1(b'blob '+str(len(raw)).encode()+bytes(1)+raw).hexdigest()


def main(root):
    assert git(root,'rev-parse','HEAD') == PIN
    folder = root/DEMO
    engine_path = folder/'engine.py'
    log = (root/ARCHIVE).read_bytes()
    assert blob(engine_path.read_bytes()) == '48f132d141167d9cd85ff79ec41720b5dca4f8bb'
    assert blob((folder.parent/'v16.26-consistency-increment-law/engine.py').read_bytes()) == 'c10ac57f988a439144e21898bd2b33ece0838a9b'
    assert blob(log) == '84ac51dc629da88adf84549a3c3a139f612c3cc6'
    evidence = (root/ARCHIVE).parent
    manifest = {name:digest for digest,name in (row.split(maxsplit=1)
                for row in (evidence/'SHA256SUMS').read_text().splitlines())}
    assert manifest['historical-producer.log'] == sha256(log).hexdigest()
    execution = json.loads((evidence/'EXECUTION.json').read_bytes())
    assert execution['execution_status'] == 'COMPLETED'
    assert str(execution['run']) == '36626045181'
    for path in (engine_path,folder.parent/'v16.26-consistency-increment-law/engine.py',folder/'completion/run_campaign.py'):
        assert sha256(path.read_bytes()).hexdigest() == execution['source_sha256'][str(path.relative_to(root))]
    commands = json.loads((evidence/'COMMANDS.json').read_bytes())
    historical, = [r for r in commands if r['name']=='historical-producer']
    assert historical['cwd'] == str(DEMO) and historical['command'][1:] == ['engine.py']
    assert historical['exit_code'] == 0
    run = subprocess.check_output([sys.executable,'-B','engine.py'],cwd=folder)
    assert run==log

    spec = spec_from_file_location('historical_attribution',engine_path)
    engine = module_from_spec(spec)
    spec.loader.exec_module(engine)
    original = engine.v26.atomic
    issued = {}
    def observe(*args):
        d = original(*args)
        if tuple(d['parents']) == (-1,0,0) and d['index']==2:
            issued[id(d)] = d
        return d
    engine.v26.atomic = observe
    try:
        report = engine.produce(4)
    finally:
        engine.v26.atomic = original
    serialized = (json.dumps(report,sort_keys=True)+'\n').encode()
    assert serialized == log
    witness = report['first_witness']
    rows = witness['path_a'] + witness['path_b']
    def live(row):
        return issued.get(id(row)) is row
    assert len(rows)==len({id(d) for d in rows})==4 and all(map(live,rows))
    assert deepcopy(rows)==rows and not any(map(live,deepcopy(rows)))
    reconstructed = json.loads((evidence/'WITNESS.json').read_bytes())
    assert reconstructed == witness and not any(map(live,reconstructed['path_a']+reconstructed['path_b']))
    bad = deepcopy(report)
    bad['first_witness']['path_a'][0]['trigger'] = False
    assert (json.dumps(bad,sort_keys=True)+'\n').encode()!=log
    assert historical['cwd'] != str(DEMO/'completion')

    names = [s for s in git(root,'ls-tree','-r','--name-only','HEAD','--','ResearchHistory/UQCF-GEM').splitlines()
             if s.endswith('.py')]
    scan = {s:(root/s).read_text(errors='replace') for s in names}
    readers = sorted(s for s,txt in scan.items() if re.search(r'historical-producer\.log|ORIGINAL_LOGGED_RESULT\.json',txt))
    assert readers==[str(DEMO/'completion/run_campaign.py')]
    explicit = {s:[i for i,l in enumerate(t.splitlines(),1) if re.search(r'\.atomic\s*\(',l)]
                for s,t in scan.items() if re.search(r'\.atomic\s*\(',t)}
    old_calls = sorted(s for s in explicit if '/demos/' in s)
    assert old_calls==[str(DEMO.parent/'v16.26-consistency-increment-law/test_gate.py'),str(DEMO/'engine.py')]
    missing = set(names)-set(scan)
    assert not missing
    event_words = [[[d['index'],d['leaf'],d['delta_h']] for d in witness[k]] for k in ('path_a','path_b')]
    local_before = [[d['before'][d['index']] for d in witness[k] if d['leaf']==1][0] for k in ('path_a','path_b')]
    assert local_before[0]!=local_before[1]
    return dict(checked_out_sha=PIN,archive_git_blob=blob(log),archive_sha256=sha256(log).hexdigest(),
                bytes=len(log),historical_run=execution['run'],historical_run_sha=execution['sha'],
                bounded_endpoints=report['endpoints'],original_receipts_at_serialization=4,
                addressed_event_words=event_words,local_prior_for_chart2_leaf1=local_before,
                reconstructed_witness_equal=True,copy_identity_control='rejected',
                changed_field_bytes_control='rejected',wrong_command_directory_control='rejected',
                historical_python_files=len(names),literal_log_or_alias_mentions=readers,
                attribute_atomic_calls=explicit,original_demo_files_with_attribute_atomic_calls=old_calls)


if __name__=='__main__':
    print(json.dumps(main(Path(sys.argv[1]).resolve()),sort_keys=True,indent=2))
