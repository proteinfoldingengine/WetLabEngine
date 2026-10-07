# Post-A12 dynamic residual: retained miss-count scope

Date: 2026-10-06 (America/Phoenix).
Status: PROSPECTIVE ANALYTICAL SCOPE. No numerical campaign, implementation, benchmark, physical interpretation, or new numbered certification.

Parent closeout:
- POST_A12_HANDOVER_CLOSEOUT.md at ef317a97b72a869bd3c6ceb38a1bc8bb65375090.
Continuation index:
- POST_A12_THEOREM_FIRST_SYNTHESIS.md at 5ef7fa06cfcd2a7b36b643ad4450e0fad4859dab.

## Objective

Resolve the next explicit obligation left by the fixed-residual handover result:

    when one previously residual root is allowed to change,
    can the retained record be updated exactly without rereading all other residual supports?

First test whether the old Boolean F_R table is sufficient. If not, derive a broader retained summary with an exact local update law.

This item is about legality/updateability of declared native residual edits. It does NOT claim a universal route-selection theorem, arbitrary-endpoint completion, observer access, efficient compression, physical locality, geometry, force, energy, or fundamental time.

## Carrier

Use a finite palette P, |P|=k>=4. The controlled X2 prepared roots (two anchors and two guards) are explicitly retained. Residual roots are original labelled slots r with current nonempty supports S_r subset P and immutable positive original floors f_r.

A declared residual operation names one residual slot r, supplies its currently retained active support S_r and floor f_r, and proposes one native incidence toggle. During a multi-edit operation, the active support of that named root is tracked in phase memory. No other residual support may be queried.

This explicit active-root support is not a full-state read. How a future autonomous controller selects a hidden residual root or learns its support is OUTSIDE this item.

## Old retained record

F_R(U)=1 for an unordered pair U iff some H subset P, |H|<=4, hits every residual root, contains U, and has at least one label outside U.

Required negative test: determine whether F_R plus all declared carrier/floor/current-target metadata and the named active-root old/new support suffices to update F_R or decide residual-edit band legality.

A valid insufficiency counterexample must use the same palette, same number and identities of residual slots, same floors, same controlled prepared state, same F_R, same named active-root support and same declared edits, but require different correct outcomes.

## Proposed broader summary

For every nonempty H subset P with |H|<=4 retain

    M_R(H)=#{r in R : S_r intersect H = empty}.

This is an integer miss-count field. It is derived from the residual state, not a new physical primitive.

Required update law for a native edit S_r -> S'_r:

    M_R'(H)
      = M_R(H)
        - 1_{S_r intersect H = empty}
        + 1_{S'_r intersect H = empty}.

For one addition/deletion, derive the corresponding sparse coordinate update.

## Required theorem obligations

1. Prove the old F_R record is insufficient by an exact same-record/same-edit counterexample satisfying the domain above.
2. Prove M_R updates exactly from its old value plus only the named active root's old/new support; no other residual support is consulted.
3. Show F_R is derivable from the zero set of M_R:
       F_R(U)=1 iff some eligible H containing U has M_R(H)=0.
4. Prove exact target-four band reconstruction when controlled supports are explicitly retained:
   - global pair witness count for K equals M_R(K) plus the number of controlled roots missing K;
   - H of size<=4 is a global cover iff M_R(H)=0 and H hits every controlled root.
5. Therefore prove that M_R plus controlled supports, active-root floor/support and phase memory suffices to decide and update the legality of any DECLARED single-incidence edit to a residual or controlled root.
6. Include original-floor legality exactly.
7. Do not claim M_R is minimal, always smaller than the full state, non-injective, efficiently initialized, internally observable, or derivable from the old F_R table.
8. Distinguish exact updateability from route selection and guaranteed completion. This item may certify a supplied edit sequence step-by-step; it does not yet prove a terminating controller for arbitrary endpoints.
9. Supply exact symbolic edge cases: empty residual family, k=4, saturated active floor, addition, deletion, and the F_R insufficiency construction.
10. Publish an author-side whole-argument audit and precise next frontier. Any independent review, numerical execution, or certification is separate.

## Candidate insufficiency construction to prove or refute

Palette P={a,b,c,d,e}; three labelled residual slots r0,r1,r2; all residual floors1; same prepared controlled state with anchors {d},{e} and both guards {a,b,c}.

State A residuals:
    r0={a}, r1={a}, r2={b}.

State B residuals:
    r0={a}, r1={a}, r2={c}.

Both appear to have F_R(U)=1 for every unordered pair U.

Declare the SAME active-root replacement in both:
    r0: {a} -> {a,b} -> {b}
by Add(r0,b), then Del(r0,a).

The prospective claim is:
- both initial prepared states have tau=4;
- both intermediate addition states have tau=4;
- final A has tau=4;
- final B has tau=5;
- after the replacement F_A remains all-true, whereas F_B({d,e})=0.

These statements are analytical leads disclosed before the formal proof. They must be proved exactly or rejected; no computation is scientific evidence.

## Boundaries

Closed A12.1-A12.5, issue #104, certified v16.54/v16.55, and accepted A11 sources remain unchanged. This is post-A12 theorem-first work and not A12.6.

No physical force, geometry, energy, GR/ADM, dark-matter replacement, continuum, observer field, physical nonlocality or fundamental time is inferred.
