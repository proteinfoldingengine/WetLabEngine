# Post-A12 richer factorization: argument audit and scoped analytical closeout

Date: 2026-10-06 (America/Phoenix).
Disposition: ANALYTICALLY COMPLETE FOR THE HIDDEN-SPECTATOR FACTORIZATION CLASS.
Evidence: written mathematical proof with author-side audit and immutable readback. Not independent peer review, proof-assistant certification, numerical PASS, benchmark or physical validation.

## Immutable record

Scope:
- 1dde3e9887cc840a42e8bbe6bb750710094ecf81
- POST_A12_RICHER_FACTORIZATION_SCOPE.md

Result:
- eee9eba17ec2f272949051dcd7533e4424ab33f3
- POST_A12_RICHER_FACTORIZATION_RESULT.md

Parent selection/completion closeout:
- b5883356c2ec2eadf57fc1f9655998b687bd2129

## Audit findings

1. Anchors {c},{d} force c,d and guards {a,b} force a third distinct label, so tau>=3 throughout.
2. Every residual root contains a or b at every phase; therefore {a,b,c,d} is a permanent four-cover and tau<=4.
3. The selected macro Add a then Del b preserves every valid original residual floor because root size changes 1+|Z| -> 2+|Z| -> 1+|Z|.
4. No spectator incidence is read or toggled.
5. Q identifies exactly the roots whose mutable core is b. Each macro removes one Q element, so rank |Q| terminates at the exact core target in 2|Q| edits.
6. Since spectator incidences never move, exact final support is {a} union Z_r in the same labelled root even though Z_r is hidden.
7. For fixed Q there are exactly 2^(ns) spectator assignments. With all residual floors fixed to1, these assignments also share identical floor metadata, so the hidden information is not smuggled through floors.
8. Q has only n dynamic membership bits and does not determine the ns spectator bits. This is a genuine dynamic retained-state reduction.
9. The fixed-m address lower bound ceil(log2 binomial(n,m)) remains valid; spectators do not enlarge it because they are invariant and structurally irrelevant to legality.
10. M_R is unnecessary in this selected class because the protected band is structurally certified. The result therefore does NOT yet establish a nontrivial simultaneous certificate+address factorization.

No mathematical correction was required in this author-side audit.

## What advanced

The previous binary class showed that aggregate certificate information does not identify labelled mismatches, but its address set Q reconstructed the whole residual state.

The present class adds ns arbitrary hidden spectator incidence bits. The same Q-based controller reaches the exact labelled target while preserving those hidden incidences without reading or reconstructing them.

Thus exact labelled completion can depend only on a quotient of the full incidence state when the discarded distinctions are dynamically invariant for the task.

## Next frontier

The next theorem should make BOTH channels active.

Required target:
- some non-core incidences may change;
- legality of at least one permitted edit genuinely depends on an updateable aggregate certificate such as M_R;
- exact destination selection uses a labelled difference/address record;
- that address record plus the aggregate certificate still leaves multiple full incidence states indistinguishable;
- a deterministic terminating controller reaches exact labelled destinations without hidden full-state reads.

This would establish a genuinely nontrivial factorization rather than structural safety plus invariant hidden data.

No numerical campaign is authorized by this closeout.

Closed A12.1-A12.5, certified v16.54/v16.55 and accepted A11 remain unchanged. No A12.6 or physical force/geometry/energy/GR/ADM/dark-matter/continuum/fundamental-time claim.
