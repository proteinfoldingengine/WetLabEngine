# Post-A12 selection/completion: labelled mismatch-address scope

Date: 2026-10-06 (America/Phoenix).
Status: PROSPECTIVE ANALYTICAL SCOPE. No numerical campaign, implementation, benchmark, independent review, physical interpretation, or numbered certification.

Parent dynamic-residual closeout:
- POST_A12_DYNAMIC_RESIDUAL_CLOSEOUT.md at 46ccf73fafb974d8721bfd6736de7201d4cb95d7.
Continuation index:
- POST_A12_THEOREM_FIRST_SYNTHESIS.md at 5652b0bd2bfff3cec68064091ec409f719b0af68.

## Objective

Attack the remaining SELECTION/COMPLETION frontier.

First determine whether the aggregate update-closed miss-count field M_R can identify which LABELLED residual root should be edited toward an exact labelled destination without reading hidden residual supports.

Then, in the smallest nontrivial class, derive the extra root-address information sufficient for deterministic terminating exact completion and quantify why some such symmetry-breaking information is necessary.

This is not arbitrary X2 endpoint completion. It is a theorem-first bounded class designed to separate:
- global legality certificates;
- labelled root selection;
- exact destination termination.

## Binary-singleton selected class

Palette P={a,b,c,d}. Controlled prepared roots are fixed throughout:
- anchor alpha={c};
- anchor beta={d};
- guard i={a,b};
- guard j={a,b};
with original floors1 for anchors and floors<=2 for guards.

There are n>=1 labelled residual roots r_1,...,r_n, each floor1 and each support exactly one of {a} or {b} at a prepared boundary.

Exact target: every residual root must end at {a}; controlled roots remain unchanged.

Allowed endpoint-directed macro on a mismatched residual root r currently {b}:
    Add(r,a), then Del(r,b).
No other incidence edit is allowed in the selected policy. The intermediate support is {a,b}.

Define mismatch set
    Q={r:S_r={b}}.

The aggregate M_R field from the parent theorem is retained and updateable.

## Required negative theorem

Construct two sources with:
- same n and labelled root identities;
- same floors;
- same controlled state;
- same exact labelled target;
- same M_R field;
- different assignment of {a}/{b} to labelled residual roots;

such that no deterministic controller using only M_R plus immutable metadata can choose a syntactically valid endpoint-directed first macro for both.

Minimum control n=2:
State A: r1={a}, r2={b}.
State B: r1={b}, r2={a}.

Because M_R is invariant under swapping residual root identities, it is identical. The only mismatched root is r2 in A and r1 in B.

Prove both sources and target are in 3<=tau<=4 and each correct macro is band-safe.

## Required positive theorem

Retain Q in addition to M_R and immutable metadata.

Controller:
1. if Q empty, stop;
2. choose least labelled root r in Q under supplied bookkeeping order;
3. execute Add(r,a), then Del(r,b), checking legality from M_R/controlled roots as in the parent theorem;
4. update M_R locally and remove r from Q;
5. repeat.

Prove:
- every primitive is syntactically and floor legal;
- 3<=tau<=4 throughout;
- exact labelled target is reached;
- rank |Q| decreases after each macro;
- at most n macros=2n primitive edits;
- no hidden residual support is queried after initialization.

## Information lower bound inside the selected class

For fixed mismatch cardinality m, M_R depends only on m, not WHICH m labelled roots are mismatched.

Prove that any deterministic no-read endpoint-directed controller that must succeed for every source with |Q|=m needs an initial retained record that distinguishes all binomial(n,m) possible mismatch sets, because aggregate M updates caused by completing one {b}->{a} macro depend only on the count, not the root identity.

Hence the supplemental root-address record requires at least
    ceil(log2 binomial(n,m))
bits in the worst case for fixed m, under the declared deterministic/no-read policy model.

Do not overstate this as a universal lower bound for arbitrary native policies: temporary probing edits, external root reads, randomized protocols, different endpoint classes or richer observations are outside scope.

## Required obligations

1. Prove exact tau values for source, intermediate and target states.
2. Prove M_R identity under labelled-root permutation and dependence only on counts of {a}/{b} roots in this class.
3. Prove M_R-only selection no-go.
4. Prove Q+M_R controller legality, updateability, termination and exact labelled completion.
5. Prove the fixed-m information lower bound carefully, accounting for the fact that the controller observes its own M updates.
6. State whether Q actually makes M_R redundant for THIS tiny class. If yes, say so explicitly; do not manufacture necessity for both records. The purpose is separation of roles, not claiming optimal encoding.
7. No claim of observer accessibility or physical locality.
8. Publish author-side audit and next frontier.

## Boundaries

This class may be deliberately simple. Its value is to prove the first exact distinction between aggregate certificate state and labelled destination-address state.

Closed A12.1-A12.5, certified v16.54/v16.55 and accepted A11 remain unchanged. No A12.6, force, geometry, energy, GR/ADM, dark-matter replacement, continuum, physical nonlocality, observer field or fundamental time.
