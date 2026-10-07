# Post-A12 richer factorization: hidden-spectator exact completion theorem

Date: 2026-10-06 (America/Phoenix).
Status: ANALYTICAL RESULT CANDIDATE WITH COMPLETE ARGUMENT.
Scope freeze: POST_A12_RICHER_FACTORIZATION_SCOPE.md at 1dde3e9887cc840a42e8bbe6bb750710094ecf81.
Evidence: written mathematics only. No numerical campaign, implementation, independent review, benchmark or physical validation.

## 1. Selected support class

Let
    P={a,b,c,d} union T,
where T={t_1,...,t_s}, s>=1.

Fixed controlled roots are
    alpha={c}, beta={d}, i={a,b}, j={a,b}.

Residual root r has
    S_r={q_r} union Z_r,
where q_r in {a,b} and Z_r subseteq T is arbitrary and immutable.

Its original positive floor satisfies
    f_r <= 1+|Z_r|.

The exact labelled destination is
    C_r={a} union Z_r.

Define the retained mismatch set
    Q={r:q_r=b}.

For r in Q the only selected macro is
    {b} union Z_r
      -> {a,b} union Z_r
      -> {a} union Z_r
by Add(r,a), then Del(r,b).

The controller is NOT supplied Z_r.

## 2. Structural protected-band theorem

**Theorem.** Every source boundary, every intermediate state of every selected macro, and every target state satisfies
    3<=tau<=4,
for every spectator assignment (Z_r)_r.

### Lower bound

The singleton controlled roots force c and d into every transversal.

The guards {a,b} require at least one additional label from {a,b}. Since a,b are distinct from c,d, every transversal has size at least3.

This argument is unaffected by residual supports and by the macro phase.

### Upper bound

Set
    H={a,b,c,d}.

H hits alpha through c, beta through d, and both guards through a or b.

Every residual root contains q_r in {a,b} at a prepared boundary. During the selected macro the active root contains both a and b after the addition and one of them after the deletion. Every other residual root still contains its core a or b.

Therefore H hits every root at every phase and tau<=4.

So 3<=tau<=4 throughout.

No aggregate M_R query is needed for this band proof.

## 3. Syntax and floors without spectator access

If r in Q, its retained core state is known to be b. Therefore a is absent and Add(r,a) is syntactically valid.

After that addition, phase memory records that both core incidences a,b are present, so Del(r,b) is syntactically valid.

The source size is
    1+|Z_r| >= f_r.
After addition the size is 2+|Z_r|. After deletion it returns to 1+|Z_r|.

Hence every original floor is preserved even though the controller does not know Z_r itself. The numerical floor may be retained as immutable metadata, but the proof needs only the domain promise f_r<=1+|Z_r|.

No spectator incidence is ever toggled.

## 4. Deterministic terminating controller

Use the supplied bookkeeping order on labelled residual roots.

Algorithm:
1. if Q is empty, stop;
2. choose the least r in Q;
3. Add(r,a);
4. Del(r,b);
5. replace Q by Q minus {r};
6. repeat.

Sections2-3 prove every primitive legal.

Each completed macro decreases integer rank |Q| by exactly one. Thus the process terminates after exactly
    |Q_initial|
macros and
    2|Q_initial|
native incidence edits.

At termination every root has core a. Since no Z_r incidence ever changed, its final support is exactly
    {a} union Z_r=C_r.

Thus the exact labelled destination is restored, including every hidden spectator incidence in its original labelled slot.

## 5. Genuine hidden-state multiplicity

Fix n,s and one mismatch set Q.

Each labelled residual root independently chooses any Z_r subseteq T. Therefore there are exactly
    (2^s)^n = 2^(ns)
different labelled spectator assignments.

All of them have:
- the same retained Q;
- the same core-edit controller transcript;
- the same sequence of selected labelled roots;
- the same 2|Q| primitive core edits.

Their full labelled incidence states generally differ, and their exact targets {a} union Z_r differ correspondingly.

Yet the controller never reads, reconstructs or stores any Z_r and still reaches each state's own exact residual-preserving target.

This is genuine retained-information reduction for the dynamic labelled incidence information relevant to the selected repair.

### Floor metadata cannot explain the reduction

Restrict further to the valid subfamily with every residual floor f_r=1.

Then all 2^(ns) spectator assignments have IDENTICAL floor metadata as well as identical Q, carrier and controller transcript.

Thus the hidden multiplicity is not encoded in the floor vector.

## 6. Retained-state count versus hidden incidence count

The dynamic address record Q has 2^n possible values and can be stored literally in n membership bits.

For fixed Q, the hidden spectator component has ns independent incidence bits and 2^(ns) possibilities.

Across all core/spectator source states in the class there are
    2^n * 2^(ns)=2^(n(s+1))
possible residual incidence states,
while Q retains only the n core-owner bits.

The theorem therefore discards all ns spectator incidence bits from the dynamic controller state.

This statement is deliberately about dynamic labelled residual-incidence information. It does not include arbitrary encoding costs for immutable palette names, slot names, program text or externally supplied floors.

## 7. Address lower bound remains

Fix mismatch cardinality m.

There are binomial(n,m) possible labelled Q sets, and the structural band behavior is identical for all of them. A deterministic no-read endpoint-directed controller must nevertheless identify which labelled roots still carry b.

Suppose two distinct size-m sets Q,Q' share the same retained address state. The controller has the same immutable metadata and no spectator observation. It chooses the same first root.

To be syntactically valid in both worlds that root must lie in Q intersect Q'. Repairing a common root produces the same observable macro completion and removes that root from both hidden mismatch sets. Repeat.

After the common intersection is exhausted, the remaining mismatch sets are nonempty and disjoint because Q,Q' began distinct with equal size. No next selected macro can be syntactically valid in both worlds, while stopping misses both exact targets.

Therefore distinct size-m Q require distinct retained address states. At least
    binomial(n,m)
states, or
    ceil(log2 binomial(n,m))
fixed-length bits, are necessary under this deterministic no-read endpoint-directed policy.

The arbitrary spectator sets do not increase this lower bound because they are invariant and irrelevant to syntax/band legality in the selected class.

## 8. Why this is a genuine factorization

The previous binary-singleton theorem used Q, but Q reconstructed the entire residual state.

Here Q reconstructs only the mutable CORE incidence:
    whether each root carries a or b.

It contains no information about any of the ns spectator incidences.

Nevertheless exact completion factors as

    structural band certificate
    + labelled core mismatch address Q
    + invariant-hidden-spectator promise
    -> legal terminating exact labelled completion.

The structural certificate is constant for the class: {a,b,c,d} is always a four-cover and c,d plus the guards force tau>=3. Consequently M_R is unnecessary for legality here.

That is a feature and a limitation. It proves that exact labelled completion does not generally require retaining every incidence, but it does NOT yet show certificate field M_R and reduced address state both being actively necessary.

## 9. Rejecting boundaries

The proof fails outside its stated invariance.

1. If a spectator incidence may change, Q does not identify which spectator difference remains and cannot update its target.
2. If a residual root may lose both a and b, H={a,b,c,d} need not hit it.
3. If the destination prescribes Z_r' different from source Z_r, the controller lacks the address information for those changes.
4. If external semantics require the controller to output the hidden Z_r values rather than merely preserve them, this retained state is insufficient.
5. Q is supplied/initialized information. No observer-access theorem derives it internally.

None of these failures implies native disconnection.

## 10. Advancement and next frontier

This is the first class in the retained-information line where the terminating exact controller provably does NOT reconstruct the full residual incidence state.

The full hidden spectator state can grow as ns bits while the dynamic address record remains n core bits.

The next frontier should make both information channels nontrivial:

    updateable aggregate certificate
    +
    reduced labelled difference/address record
    -> exact terminating completion,

in a class where some non-core incidences themselves change.

That next class must prevent the address record from becoming a full incidence copy while making legality genuinely depend on aggregate certificate information. It should quantify the hidden-state multiplicity remaining after conditioning on the retained record.

Closed A12.1-A12.5, certified v16.54/v16.55 and accepted A11 remain unchanged. No A12.6, force, geometry, energy, GR/ADM, dark-matter replacement, continuum, physical nonlocality, observer field or fundamental time is inferred.
