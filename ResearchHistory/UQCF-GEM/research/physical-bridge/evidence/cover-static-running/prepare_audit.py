"""Prepare closeout audit against this campaign; execution waits for originals."""
import ast,pathlib
p=pathlib.Path(__file__).parent;parent=p.parent/'nonuniform_reserve'
names=next(ast.literal_eval(n.value) for n in ast.parse((p/'review_runner.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='names' for t in n.targets))
s=(parent/'audit_originals.py').read_text()
s=s.replace('nonuniform_reserve','cover_static').replace('nonuniform-reserve','cover-static').replace('NONUNIFORM_RESERVE','COVER_STATIC').replace('test_nonuniform.py','test_cover_static.py')
a=s.index('DOCS=');b=s.index('\nassert set(docs)',a);s=s[:a]+'DOCS='+repr(set(names))+s[b:]
s=s.replace("'contracts.log':34","'contracts.log':35,'inherited_nonuniform_reserve.log':34")
a=s.index("classification={'static_spare'");b=s.index("\nif (P/'counts.json')",a)
s=s[:a]+"assert counts=={'sources':3072,'feasible_vectors':216299,'endpoint_occurrences':91214,'distinct_endpoints':53118,'hidden_checks':48769461}\nassert len(certificate['record_sha256'])==3072\n"+s[b:]
s=s.replace("['status']=='PASS'","['accepted'] is True",1)
s=s.replace("sum(test_counts.values())==378","sum(test_counts.values())==413").replace("-{'certificate.json'}",'')
s=s.replace('Nonuniform-reserve independent verdict:','Cover-static independent verdict:')
s=s.replace("'scope_freeze':'a072edf689f1aa3bb74b581bf2b32131bb9cb4a6'","'scope_freeze':'98bbefd62e95d0b9d89dd92b2267970a73f5a26e'")
s=s.replace("'finite_classification':classification,",'').replace("'tests_total':378","'tests_total':413").replace("'final_new_tests':34","'final_new_tests':35")
a=s.index("'limitations':[");b=s.index(']}',a)+2
s=s[:a]+"'limitations':['Arbitrary isolate-free finite pair-root carrier with source tau3or4 and all positive multiplicities; theorem analytical','Finite declared3072binary-profile sources only','Endpoint reserve only, no reachability or path assertion','First/last canonical anchor choices and one-hidden finite checks; universal anchor/hidden statements proof based','Repair, progress, native observation-access-origin-retainedoutput and broadC3/generalC4 OPEN']}"+s[b:]
s=s.replace('import hashlib,json,pathlib,re,zipfile','if not __debug__: raise RuntimeError("audit requires assertions enabled")\nimport hashlib,json,pathlib,re,zipfile')
(p/'audit_originals.py').write_text(s)
s=(parent/'test_original_audit.py').read_text().replace('378','413').replace('nonuniform-reserve','cover-static').replace("b'Ran 34 tests',b'Ran 35 tests'","b'Ran 35 tests',b'Ran 36 tests'")
(p/'test_original_audit.py').write_text(s)
(p/'reassemble_archives.py').write_text((parent/'reassemble_archives.py').read_text())
for f in ('audit_originals.py','test_original_audit.py','reassemble_archives.py'):ast.parse((p/f).read_text())
print('Prepared audit and nine rejection controls; not executed without original evidence')
