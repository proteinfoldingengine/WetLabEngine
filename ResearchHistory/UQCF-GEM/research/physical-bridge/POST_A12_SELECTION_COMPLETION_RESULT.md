# Post-A12 selection/completion: exact labelled-address theorem

Date: 2026-10-06 (America/Phoenix).
Status: ANALYTICAL RESULT CANDIDATE WITH COMPLETE ARGUMENT.
Scope freeze: POST_A12_SELECTION_COMPLETION_SCOPE.md at eff1e50769c4e73bd325fe8b1ff06a72ea06d2ee.
Evidence: written mathematics only. No numerical campaign, implementation, independent review, benchmark or physical validation.

## 1. Selected class

Use P={a,b,c,d}. Fixed controlled roots:
    alpha={c}, beta={d}, i={a,b}, j={a,b}.
All anchor/residual floors are1; guard floors are positive and at most2.

There are n>=1 labelled residual roots r_1,...,r_n, each support either {a} or {b}. The exact labelled target has every residual root equal {a}.

Let
    Q={r:S_r={b}}
be the labelled mismatch set and m=|Q|.

The only selected endpoint-directed macro on r in Q is
    {b} -> {a,b} -> {a}
by Add(r,a), then Del(r,b).

## 2. Exact protected-band values

Anchors force c,d in every state. The guards require at least one of a,b.

At a prepared boundary:
- if both an {a} residual and a {b} residual exist, those singleton roots force both a and b, so tau=4;
- if residuals use only one of {a},{b}, that label together with c,d hits every root, so tau=3.
No prepared boundary has tau outside {3,4}.

During a macro, the active residual becomes {a,b}. All other residuals remain singleton.

If the remaining singleton residuals include both labels, tau=4.
If they include only a, only b, or none, c,d plus one suitable label from {a,b} hit every root, so tau=3.
The lower bound is at least3 because c,d are forced and neither hits the guards.

Thus every primitive of every selected macro stays in 3<=tau<=4.

Floor legality is immediate: Add grows a singleton; Del from {a,b} returns to size1, meeting the active floor. Controlled roots never change.

## 3. Aggregate miss counts forget labelled ownership

Let n_a=n-m and n_b=m.

For every nonempty H subset P, |H|<=4,

    M_R(H)
      = n_a * 1_{a notin H}
        + n_b * 1_{b notin H}.

Therefore M_R depends only on the COUNTS (n_a,n_b), not on which labelled residual roots carry which singleton.

Any permutation of residual root identities preserving the multiset of supports leaves the complete M_R field unchanged.

## 4. Exact M-only selection no-go

Take n=2,m=1.

State A:
    r1={a}, r2={b}.

State B:
    r1={b}, r2={a}.

They have identical palette, controlled roots, root identities/count, floors, exact target, and M_R field by Section3. Both sources have tau=4 because a,b,c,d are forced by the two residual singleton labels and two anchors.

The target has both residual roots {a} and tau=3.

In the selected endpoint-directed policy:
- A has exactly one available first macro, on r2;
- B has exactly one available first macro, on r1.

A deterministic controller receiving only M_R and the identical immutable metadata must choose the same action in both states. If it stops, it fails both exact targets. If it names r1, the macro is syntactically unavailable in A because r1 is already {a}; if it names r2, it is unavailable in B.

Therefore M_R is sufficient for legality AFTER a root/support is named, as proved by the parent theorem, but is insufficient to select the labelled mismatched root needed for exact completion.

This is a selection-information obstruction, not a native-connectivity obstruction.

## 5. Q gives a terminating exact controller

Retain Q explicitly.

Controller:
1. If Q is empty, stop.
2. Choose the least root r in Q under the supplied bookkeeping order.
3. Add a to r.
4. Delete b from r.
5. Remove r from Q.
6. Repeat.

Section2 proves both primitives are band-safe and floor-safe. Syntax is known from Q: r in Q means its prepared support is exactly {b}; after the addition the controller's phase memory knows it is {a,b}; after deletion it is {a}.

Each macro decreases rank |Q| by exactly one. Hence after exactly m macros and 2m primitive edits, Q is empty.

At that point every labelled residual root has support {a}; controlled roots were unchanged. The exact labelled target is reached.

No residual support is queried after initialization.

## 6. Information lower bound for no-read endpoint-directed completion

Fix n and mismatch cardinality m with 0<=m<=n. There are

    binomial(n,m)

possible labelled mismatch sets Q.

For all of them M_R is identical by Section3.

Consider any deterministic controller in the selected no-read policy model. Its initial supplemental retained record Z may depend on Q. Thereafter it observes only:
- its own previous choices/phase;
- the aggregate M updates;
- its deterministic updates of Z.
It cannot query a hidden residual support.

Claim: if two distinct mismatch sets Q,Q' of the same cardinality share the same initial Z, the controller cannot succeed on both.

Proof. Their initial M fields and Z are identical, so the controller chooses the same first action.

A legal macro root must lie in Q intersect Q'. If it chooses outside the intersection, one execution is syntactically invalid. If it chooses r in the intersection, both executions perform the same {b}->{a} macro. Their new aggregate M fields remain identical because both mismatch counts drop from m to m-1. Their deterministic Z updates are also identical because their prior Z, action and observed aggregate update were identical.

Repeat this argument. The controller can remove only roots in the current intersection while remaining valid in both worlds. Since Q and Q' are distinct but have equal cardinality, after all common roots are removed, each world still has at least one mismatch and the remaining mismatch sets are disjoint. The controller then has no root on which the next endpoint-directed macro is syntactically valid in both. Stopping misses both targets.

Contradiction. Therefore every two distinct size-m mismatch sets require distinct initial supplemental records.

Hence the record has at least binomial(n,m) distinguishable values and any fixed-length binary encoding needs at least

    ceil(log2 binomial(n,m))

bits.

This lower bound is conditional on the declared deterministic, no-read, endpoint-directed policy and the fixed m ensemble. It is not a universal information lower bound for arbitrary native repair.

## 7. Q is sufficient but not encoding-optimal

The literal set Q can be stored as n membership bits and completely determines the residual incidence state in THIS binary-singleton class. Therefore M_R is redundant once Q is known here.

This is not a defect in the theorem. It identifies the exact role separation:
- M_R is an aggregate certificate state that forgets labelled ownership;
- exact labelled completion requires ownership/address information;
- in the smallest binary class, retaining enough address information happens to reconstruct the whole residual state.

For fixed m, an enumerative encoding of Q can approach the lower bound ceil(log2 binomial(n,m)) rather than n bits. No claim is made that Q is a minimal representation.

In richer support classes, a root-address record need not automatically determine every incidence; that is the next place to test whether legality certificates and address information can remain genuinely separated.

## 8. What advanced

The previous dynamic-residual theorem closed:
    named root + known support -> legality + exact retained-record update.

The present theorem closes, for this selected class:
    retained labelled mismatch address -> root selection -> legal finite sequence -> exact labelled destination.

It also proves why aggregate miss counts alone cannot perform that selection.

The result therefore separates two information functions that were previously conflated:

    CERTIFICATE INFORMATION:
        is a proposed relational change protected?

    ADDRESS INFORMATION:
        which labelled component still differs from the exact destination?

Exact labelled completion can require both roles even when the global protected-band certificate is perfectly updateable.

## 9. Remaining frontier

The binary-singleton class is intentionally small, and Q reconstructs its residual state. The next scientifically useful question is whether a richer class admits a NONTRIVIAL factorization:

    aggregate certificate field
    +
    substantially smaller labelled address/difference record
    -> terminating exact completion,

without the address record becoming a disguised copy of all residual incidences.

A suitable next class should permit multiple support patterns per root while giving the controller a declared finite family of endpoint-directed macros. The theorem should compare the number of possible hidden incidence states with the number of required address states and preserve exact floors/band legality.

Alternative policies with temporary probing edits, randomized observations, external root reads, or non-endpoint-directed moves are outside the present lower bound and may reduce the retained address requirement.

Closed A12.1-A12.5, certified v16.54/v16.55 and accepted A11 sources remain unchanged. No A12.6, force, geometry, energy, GR/ADM, dark-matter replacement, continuum, physical nonlocality, observer field or fundamental time is inferred.
