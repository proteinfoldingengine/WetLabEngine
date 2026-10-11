import pathlib,re,subprocess,json
p=pathlib.Path(__file__).resolve().parent;out=p/'inherited';out.mkdir(exist_ok=True)
suites=['source_escape','cover_static','nonuniform_reserve','weak_trace','fingerprint_lock','private_cover','moving_cover','saturated_handover','slack_handover','handover_graph','anchored_release','local_progress','capacity_gap','saturated_transfer','label_release','footprint','fixed_family'];rows=[]
for suite in suites:
 folder=p.parent/suite;tests=[x for x in folder.glob('test_*.py') if x.name!='test_original_audit.py'];assert len(tests)==1,(suite,tests)
 r=subprocess.run(['python3','-m','unittest','discover','-s',str(folder),'-p',tests[0].name,'-v'],capture_output=True,text=True);log=r.stdout+r.stderr;(out/(suite+'.log')).write_text(log);match=re.findall(r'Ran (\d+) tests',log);rows.append(dict(suite=suite,exit_code=r.returncode,tests=int(match[-1]) if match else None));(out/'results.json').write_text(json.dumps(rows,indent=2)+'\n');print(rows[-1],flush=True)
 if r.returncode:raise SystemExit(r.returncode)
assert sum(x['tests'] for x in rows)==455
