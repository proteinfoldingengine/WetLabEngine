"""Read-only audit of the accepted marked-branch archive; no new runs of its producer."""
from collections import Counter
import hashlib, importlib.util, json, sys
from pathlib import Path
archive, ref = list(map(Path, sys.argv[1:3]))
demos = ref/'ResearchHistory/UQCF-GEM/demos'
def pinned(name, path, blob):
    data = path.read_bytes()
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == blob
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
atom = pinned('atom', demos/'v16.26-consistency-increment-law/engine.py', 'c10ac57f988a439144e21898bd2b33ece0838a9b')
proof = pinned('proof', demos/'v16.26-consistency-increment-law/verify.py', '91cd1e507e955683e744fbdbb0745cac19d66cb3')
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
assert digest == '319c43442aee53b9da4e94bc2005841bcaba39629318d285b2b4f9d11838f515'
counts = Counter()
first, depths = Counter(), Counter()
def views(state, n):
    return tuple(tuple(i for i in range(n) if (m>>i)&1) for m in state)
def reject(par, y, actor, leaf):
    try: atom.atomic(par,y,actor,leaf)
    except ValueError as e: assert str(e)=='same union'
    else: raise AssertionError('illegal sole-holder withdrawal admitted')
for row in json.loads(archive.read_text()):
    names = row['order']
    par = tuple((-1 if v=='Pin' else names.index('Pin' if v in ('P','Q') else 'P' if v.startswith('X') or v=='A' else 'B' if v.startswith('b') else 'Q')) for v in names)
    R = row['receiver']; C = 1-R
    path = row['path']
    if len(path)==1: counts['idle']+=1; continue
    counts['nonconstant'] += 1
    copies = 0
    for i, ((old,pre),(new,mid)) in enumerate(zip(path,path[1:])):
        diff = old[R]^new[R]
        if not diff or diff&(diff-1) or not diff&new[R]: continue
        l = diff.bit_length()-1
        if names[l][0] not in 'XY': continue
        copies += 1
        only_c, both, only_r = [views(s,len(names)) for s in (old,new,path[i+2][0])]
        assert l in only_c[C] and l not in only_c[R] and l in both[C] and l in both[R]
        d = atom.atomic(par,both,C,l)
        assert tuple(map(tuple,d['after']))==only_r
        proof.verify_atomic(d)
        reject(par, only_c, C, l)
        reject(par, only_r, R, l)
        assert mid == path[i+2][1]
        counts['copies_and_immediate_verified_release'] += 1
        counts['receiver_records_unchanged_by_release'] += 1
        depths[(d['tau_before'],d['tau_after'],d['trigger'])]+=1
        if copies==1:
            assert all(mask[R] & diff for mask,_ in path[i+1:])
            assert not any(mask[C] & diff for mask,_ in path[i+2:])
            assert dict(mid[0])[l] in (1,8) and dict(mid[1])[l] == 9-dict(mid[0])[l]
            first[(i+1,names[l][0],d["tau_before"],d["tau_after"],d["trigger"])]+=1
            counts['first_copied_leaf_retained_exclusively_after_release'] += 1
    assert copies > 0
print(json.dumps({'sha256': digest, 'counts': dict(counts),
                  'first_release_preceding_copy': sorted(first.items()),
                  'local_cover_before_after_and_trigger': sorted(depths.items())}, sort_keys=True))
