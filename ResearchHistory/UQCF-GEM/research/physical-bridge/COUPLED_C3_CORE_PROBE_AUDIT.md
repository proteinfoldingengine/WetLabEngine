# C3 native core-probe theorem — author audit and reproducible hand checks

Date: 2026-10-08.
Disposition: AUTHOR CHECKS COMPLETED; INDEPENDENT MATHEMATICAL REVIEW NOT YET OBTAINED.
This document is not an independent review, publication-consistency acceptance, or scoped closeout.

## Exact provenance

- Integrated parent: 47358f41cd3bd0b1fc252afe07aaa28a6647a770.
- Frozen scope: COUPLED_C3_CORE_PROBE_SCOPE.md, commit 4e0cb8c68c807265fb48652b1f990a18d4a43a2c.
- Proof under audit: COUPLED_C3_CORE_PROBE_RESULT.md, commit e7dc592d0f98121c7c232f33018a0a199c30ba8e, blob d619932c44d051f2a0c698365709d6f42e02f078.
- Proof was fetched by immutable commit and read in full in two consecutive ranges, lines 1-100 and 101-end. Both returned the same blob SHA.
- The accepted predecessor observation-fiber closeout remains ce9e86013daeabdebc9c1118d8b08f1b39a437f1. Its independent acceptances do not transfer to this follow-on theorem.

## Whole-argument author checks

The proof's necessary floor inequality and constructive converse use the same fixed Z throughout each history. The converse supplies every hidden completion, not just a matching count: for every Z' of sufficient size, all attempted commands, committed core toggles, rejected outcomes, observed projections, miss counts and tau values are reproduced.

The hitting-number argument explicitly separates P4 nonempty from P4 empty. The latter requires |Z|>=2 and adds exactly one spectator to a transversal of the three purely core roots. Thus the proof does not use an empty-support transversal as though it were finite.

Rejected commands constrain neither the attempted successor nor the hidden capacity because rejection of legal commands is explicitly allowed. The exact online bound is updated from OBSERVED supports, not intended supports. Adaptivity is handled by induction on equal retained histories.

The positive certificate D>=1 depends only on the visible root-4 core count and the known support floor. Exact tau is used to establish band safety and complete observation equivalence; no separate measurement of tau is needed in the formula for D. This does not derive availability of the core projections themselves.

The preserved object is Z. D is a nondecreasing information bound, not a conserved quantity. Restoration is proved reachable by one further committed edit, not guaranteed after a finite number of attempts. The probe is not claimed to improve total repair cost: information acquisition and restoration themselves consume native edits.

The no-decision theorem explicitly uses the permitted all-rejection run. More generally, the exact fiber theorem says every feasible D=0 history remains ambiguous even when it contains committed common-admissible core edits. A stronger mandatory-success contract is identified as a different model, not imported as a premise.

## Local hand-case diagnostics actually executed

A standalone Python calculation enumerated candidate hitting sets for the explicitly listed supports below. It did not enumerate a preregistered state universe and is not evidence of universal coverage. Exit status was 0, with all assertions satisfied.

The first three roots in the primary hand cases are always {a,b},{b,c},{a,c}.

| Actual root 4 | History D | Actual spectator count | Exact tau | All floors >=2 |
|---|---:|---:|---:|---|
| {d,e} | 0 | 0 | 3 | yes |
| {d,e,z} | 0 | 1 | 3 | yes |
| {e,z}, after observed -d | 1 | 1 | 3 | yes |
| {d,e,z}, after observed restoration | 1 | 1 | 3 | yes |
| {e,u,v}, after observed -d | 1 | 2 | 3 | yes |
| {u,v}, after observed -d,-e | 2 | 2 | 3 | yes |
| {d,e}, after rejected -d at empty seed | 0 | 0 | 3 | yes |

Rejecting controls were also checked: the proposed {e} root at empty seed fails floor 2; a spectator shared by two roots can change tau from core 4 to full 3; removing an invariant spectator after restoration invalidates the old bound while leaving all native floors and tau valid.

## Reproduce the hand cases

Python standard library only. These are bounded hand-case diagnostics, not an inherited CI replay, independent implementation, or proof-assistant verification.

```python
from itertools import combinations


def tau(roots):
    palette = sorted(set().union(*roots))
    for k in range(len(palette) + 1):
        for h in combinations(palette, k):
            if all(set(h) & s for s in roots):
                return k
    return None


triangle = [set('ab'), set('bc'), set('ac')]
cases = [
    ('empty seed', set('de'), 0),
    ('one spectator', set('dez'), 0),
    ('successful -d', set('ez'), 1),
    ('restored +d', set('dez'), 1),
    ('two spectators, -d', set('euv'), 1),
    ('two spectators, -d,-e', set('uv'), 2),
    ('rejected -d from empty: unchanged', set('de'), 0),
]
for label, r4, d in cases:
    roots = triangle + [r4]
    t = tau(roots)
    floor = all(len(s) >= 2 for s in roots)
    assert t == 3 and floor
    q = len(r4 - set('abcde'))
    assert q >= d
    print(label, sorted(r4), 'tau=', t, 'floors=', floor,
          'history_D=', d, 'spectator_count=', q)

assert not all(len(s) >= 2 for s in triangle + [set('e')])
print('Rejected invalid deletion must not raise D.')

shared = [set('abz'), set('cdz'), set('ef'), set('gh')]
core = [s - {'z'} for s in shared]
assert tau(shared) == 3 and tau(core) == 4
print('Single-root spectator premise is necessary.')

r4_after = set('dez') - {'z'}
assert tau(triangle + [r4_after]) == 3 and len(r4_after) == 2
assert len(r4_after - set('abcde')) < 1
print('Hidden spectator removal invalidates old D=1.')
print('Local hand-case diagnostics completed.')
```

## Independent-review packet and uncompleted gates

A fresh independent mathematical review should examine exact sufficiency of the history fiber, the P4-empty boundary, treatment of rejected legal commands, adaptation, and whether the operational no-termination claim imports any unlisted assumption. It should also check the distinction between a visible core change and the inherited invisible spectator-command outcome, plus invariance and restoration caveats.

No fresh independent reviewer verdict has been obtained or represented here. No external review job was launched in this work unit. A separate publication-consistency audit and scoped closeout have NOT been performed. No CI/inherited-stack replay or main-branch merge is claimed.

A positive independent mathematical verdict, followed by a separate publication audit of the exact reviewed source and provenance, is required before changing this checkpoint to CLOSED/CERTIFIED. Correct and re-review any substantive issue rather than silently amending an accepted result. Broader C3 and C4-C6 remain OPEN.
