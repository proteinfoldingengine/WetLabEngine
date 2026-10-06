# A12.1 — signed admissibility response in the protected relational state graph

Date: 2026-10-06 UTC.
Status: analytical physics-bridge candidate for fresh independent whole-argument review.
Scope freeze: 8a9b9747a3e95118af46b5d16c2bffa5938d7d6e.
Dependencies: only the native root/incidence state space, original floors, and target-four protected band used by accepted A11 mathematics. Pending X62-X64 are NOT used.

No geometry, metric, spacetime, energy, probability, force magnitude, autonomous dynamics, numerical execution, implementation, benchmark or physical-law claim.

## 1. Native admissibility response

Let E=(E_i) be any finite labelled root state with original floors f_i and

    3 <= tau(E) <= 4.

A typed incidence move is:
- Add(i,x) if x is absent from E_i;
- Del(i,x) if x is present in E_i.

Its legal indicator L_E(m) is1 exactly when:
1. the toggle is syntactically available;
2. for deletion, the resulting root still has size at least f_i;
3. the resulting state remains in 3<=tau<=4.

Otherwise L_E(m)=0.

Take a legal move e and a DISTINCT incidence move f whose incidence status is not directly toggled by e. Define

    R_E(e->f)=L_(eE)(f)-L_E(f) in {-1,0,+1}.

R=+1 means e enables f; R=-1 means e suppresses f; R=0 means its legality is unchanged.

This is a one-update response of the admissible continuation structure. It is not a force.

## 2. Transversal monotonicity

If E_i subseteq E'_i for every root i, every hitting set of E also hits E'. Hence

    tau(E') <= tau(E).

Therefore:
- adding one incidence can only weakly DECREASE tau;
- deleting one incidence can only weakly INCREASE tau.

A single addition cannot violate the upper bound tau<=4 when starting in the band; it can fail only by producing tau<=2. A single deletion cannot violate the lower bound tau>=3; it can fail only by producing tau>=5, apart from its local floor legality.

These monotonicities are purely relational and require no embedding.

## 3. Signed response theorem

**A12.1S.** For every legal e and distinct candidate f:

    e Add, f Add:   R<=0
    e Del, f Del:   R<=0
    e Add, f Del:   R>=0
    e Del, f Add:   R>=0.

Thus same-direction incidence changes can only compete for admissibility, while opposite-direction changes can only facilitate it.

### Add -> Add

Floor legality is irrelevant. Suppose f is illegal before e. An addition can fail only because tau(fE)<=2. Since e is another addition,

    f(eE) is componentwise >= fE,

so tau(f(eE))<=tau(fE)<=2. Thus f cannot become legal. A legal f may become illegal, so R is0 or-1.

### Del -> Del

If f is floor-illegal before e, a distinct deletion cannot create slack in f's root; it either leaves that floor status unchanged or, in the same root, reduces slack further. If f is band-illegal, tau(fE)>=5. Since e is another deletion,

    f(eE) is componentwise <= fE,

so tau(f(eE))>=tau(fE)>=5. Thus f cannot become legal. A legal f may be suppressed by the upper bound or by same-root floor exhaustion. Hence R is0 or-1.

### Add -> Del

If f is legal before e, adding e cannot reduce its floor slack. Also

    f(eE) is componentwise >= fE,

so tau(f(eE))<=tau(fE)<=4. Because f is a deletion from legal state eE, tau(f(eE))>=tau(eE)>=3. Therefore f remains legal.

If f was illegal, e can enable it either by creating same-root floor slack or by lowering a would-be tau>=5 deletion result into the band. Hence R is0 or+1.

### Del -> Add

Addition f has no floor requirement. If f is legal before e,

    f(eE) is componentwise <= fE,

so tau(f(eE))>=tau(fE)>=3. Because f is an addition to legal state eE, tau(f(eE))<=tau(eE)<=4. Thus f remains legal.

If f was illegal because it produced tau<=2, deletion e can raise that result back into the band. Hence R is0 or+1.

This proves all four signs, including same-root distinct-incidence floor effects.

## 4. Cross-root response is globally mediated

If e and f act on DIFFERENT roots, e cannot change f's local floor slack or syntactic incidence status.

Therefore any nonzero cross-root R is caused solely by the global transversal constraint.

There are two channels.

### Lower-witness channel

Only additions can threaten tau>=3.

If an Add f is legal before a cross-root Add e but illegal after it, then after e+f some physical pair K hits every root. Because f alone was legal, K did not hit every root before f. The incidence added by f must participate in the newly completed pair cover; immediately before f, f's root is an actual missed-root witness for K. The prior addition e has removed the other obstruction needed to make that pair globally covering.

Conversely, if a cross-root Del e enables an Add f, the deletion restores enough missed-root structure that every pair again has an actual witness after f. In the sharp case where f was blocked by a specific pair K, e creates/restores a root missed by K.

Thus Add/Add suppression and Del/Add facilitation are lower-protection response.

### Upper-cover channel

Only deletions can threaten tau<=4.

If a Del f is legal before a cross-root Del e but illegal after it, the two deletions have jointly destroyed all hitting sets of size at most four although either allowed state remained protected. This is upper-cover competition.

If a cross-root Add e enables a Del f that previously produced tau>=5, e has supplied an incidence that restores some at-most-four hitting set after f. This is upper-cover facilitation.

Thus Del/Del suppression and Add/Del facilitation are upper-protection response.

No spatial locality is inferred. "Cross-root" means different original relational supports only.

## 5. Exact symbolic controls

All floors below are1 unless stated.

### Add suppresses Add

E has four roots

    {a}, {b}, {c}, {d}.

tau(E)=4.
Let e add a to root3 and f add b to root4.

After either addition alone tau=3. After both, pair {a,b} hits all four roots, so tau=2.

Hence R_E(e->f)=-1.

### Del enables Add

Use

    {a}, {b}, {a,c}, {d}.

tau=3.
Let e delete a from root3 and f add b to root4.

Before e, f creates pair cover {a,b} and is illegal at tau2. Deletion e restores four disjoint singleton roots, tau4; then f gives tau3.

Hence R=+1.

### Del suppresses Del

Use five roots

    {a}, {b}, {c}, {a,d}, {b,e}.

tau=3.
Let e delete a from root4 and f delete b from root5.

Either deletion alone gives tau4. Both give five disjoint singleton roots and tau5.

Hence R=-1.

### Add enables Del

Use

    {a}, {b}, {c}, {d}, {b,e}.

tau=4.
Let e add a to root4 and f delete b from root5.

Before e, f gives five disjoint singleton roots and tau5, so it is illegal. After e the state has tau3; applying f leaves tau4.

Hence R=+1.

These are exact analytical examples, not numerical evidence.

## 6. Relabeling covariance and invariant response scalars

Let sigma permute original root identities and pi permute palette labels, carrying floors with their roots. This bijection preserves incidence, root cardinality, transversal number and move type.

Let g=(sigma,pi). Then

    L_(gE)(gm)=L_E(m)

and therefore

    R_(gE)(ge->gf)=R_E(e->f).

So the directed response matrix is covariant: relabeling only permutes its rows/columns.

For fixed legal e define over all distinct typed incidence candidates f:

    S_E(e)=#{f:R=-1},
    F_E(e)=#{f:R=+1},
    Q_E(e)=F_E(e)-S_E(e),
    M_E(e)=F_E(e)+S_E(e).

Under g,

    S_(gE)(ge)=S_E(e),
    F_(gE)(ge)=F_E(e),
    Q_(gE)(ge)=Q_E(e),
    M_(gE)(ge)=M_E(e).

These are relabeling-invariant dimensionless response observables.

The response graph has directed edge e->f exactly when R is nonzero. Its cross-root subgraph removes purely local floor effects and retains only globally constraint-mediated response.

## 7. What this establishes and what it does not

The theorem establishes an intrinsic signed interaction structure on the protected relational state graph:

- a legal update can alter which other updates remain admissible;
- the sign of that alteration is fixed by whether the two changes move incidence in the same or opposite direction;
- nonzero cross-root response is mediated by the global hitting constraints, not by the receiving root's local floor;
- the response transforms covariantly under arbitrary relabeling, with invariant scalar summaries.

This is closer to a physics-facing response law than a repair schedule because it asks what one perturbation DOES to the available continuations of another.

It is still NOT a physical force law. Missing ingredients include:
1. an autonomous/model-derived rule selecting which legal update actually occurs;
2. an observer-accessible operational measurement of R or its coarse-graining;
3. composition and scaling across retained-order depth;
4. a derived notion of separation/locality if one exists;
5. dimensional calibration;
6. any continuum limit or relation to inertial/gravitational response.

No inverse-square, metric, curvature, energy, action, stress-energy, GR/ADM or dark-matter variable is inserted.

## 8. Next falsifiable bridge

The next question is whether the signed response survives coarse-graining in a nontrivial way.

A useful A12.2 target is a composition law for two disjoint interventions e1,e2 and a remote candidate f:

    Delta_12(f)=L_(e2 e1 E)(f)-L_E(f),

compared with the sum of one-step responses. Nonadditivity would measure genuinely collective constraint response; exact additivity under a structural separation condition would provide a native null/locality criterion.

That should be proved before attempting any force-distance interpretation.

v16.54/v16.55 and accepted A11 results remain unchanged. Pending X62-X64 are not promoted. Separate efficiency work remains unstarted.
