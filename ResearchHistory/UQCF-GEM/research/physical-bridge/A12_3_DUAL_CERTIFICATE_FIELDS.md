# A12.3 — exact dual certificate update law for the target-four protected band

Date: 2026-10-06 UTC.
Status: analytical physics-bridge candidate for fresh independent whole-argument review.
Scope freeze: 71f4b61f3201777a3654cc09aeb3725627d10c47.
Native derivation; A12.1/A12.2 are comparisons only and need not be accepted.

No geometry, force, energy, action, probability, continuum, numerical execution, implementation or numbered certification claim.

## 1. Two exact certificate fields

Let E=(E_i) be a finite root state on palette P.

For every two-label set K define the actual lower-witness multiplicity

    W_E(K)=#{i:E_i intersect K=empty}.

For every physical H subset P with |H|<=4 define

    C_E(H)=1  iff  H intersects E_i for every root i,

and0 otherwise.

Then exactly:

    tau(E)>=3  iff  W_E(K)>=1 for every |K|=2,

because tau<=2 precisely when some pair covers; a one- or zero-label cover can be extended to a pair when |P|>=2.

Also

    tau(E)<=4  iff  C_E(H)=1 for at least one |H|<=4.

Thus the protected band is exactly the simultaneous condition

    min_K W_E(K)>=1
    and
    sum_(|H|<=4) C_E(H)>=1.

Original root floors are a separate local constraint.

## 2. Exact addition update

Let e=Add(i,x), with x absent from E_i.

### Lower field

For pair K, roots other than i do not change. Root i stops being a K witness exactly when:
- x belongs to K; and
- E_i intersect K was empty before the addition.

Therefore

    W_(eE)(K)
      = W_E(K)-1_{x in K and E_i intersect K=empty}.

No W coordinate can increase under an addition.

The number of pair coordinates changed is exactly

    |P|-|E_i|-1,

because K must be {x,y} with y outside E_i and y!=x.

### Upper field

An existing cover remains a cover after a root grows, so C can never change1->0.

A noncover H becomes a cover exactly when:
- x in H;
- E_i intersect H=empty, so i was missed before;
- every other root already intersects H.

Equivalently i was the unique H-missed root and the new incidence x supplies its hit.

Thus additions consume lower witness multiplicity and may create upper certificates.

## 3. Exact deletion update

Let e=Del(i,x), with x present in E_i.

### Lower field

Root i becomes a new K witness exactly when:
- x in K; and
- E_i intersect K={x} before deletion.

Therefore

    W_(eE)(K)
      = W_E(K)+1_{x in K and E_i intersect K={x}}.

No W coordinate can decrease under a deletion.

The number of changed pair coordinates is exactly

    |P|-|E_i|,

one pair {x,y} for each y outside E_i.

### Upper field

A noncover cannot become a cover when a root shrinks, so C never changes0->1.

An existing cover H is destroyed exactly when:
- x in H;
- E_i intersect H={x};
- H hit every root before deletion.

After deleting x, root i is the newly missed root.

Thus deletions create lower witnesses and may destroy upper certificates.

## 4. Exact admissibility decomposition

Define

    mu_-(E)=min_(|K|=2) W_E(K),

and

    N_4(E)=sum_(H subset P, |H|<=4) C_E(H).

Within a protected state:
- an addition is band-legal exactly when mu_-(eE)>=1. The upper condition cannot fail because N_4 cannot decrease.
- a deletion is band-legal exactly when N_4(eE)>=1. The lower condition cannot fail because W cannot decrease.
- deletion additionally requires its same-root original floor.

Therefore target-four admissibility splits exactly into two dual certificate channels:

    ADDITION: do not exhaust the last lower witness.
    DELETION: do not destroy the last small upper cover.

This is not a conservation equation; W and C live on different index families and no invariant sum is asserted.

## 5. One-update bounds

Every W(K) coordinate changes by at most one.

An addition can lower mu_- by at most one; a deletion can raise mu_- by at most one.

N_4 is monotone nondecreasing under additions and nonincreasing under deletions, but one incidence may create or destroy many cover identities H. The exact affected H are those described in Sections2-3; no independent-cover approximation is made.

Thus the lower channel has an exact integer witness redundancy, while the upper channel is naturally a family of alternative certificates rather than one scalar resource.

## 6. Signed response follows from the dual law

For distinct moves e,f:
- Add e depletes only W and improves only C.
- Del e improves only W and depletes only C.

Candidate Add f is controlled by W; candidate Del f is controlled by C plus its local floor.

Hence:
- Add->Add cannot enable: prior W depletion cannot improve an addition's lower safety.
- Del->Del cannot enable: prior C depletion and possible floor depletion cannot improve deletion safety.
- Add->Del cannot suppress: C can only improve and floor slack can only improve in the same root.
- Del->Add cannot suppress: W can only improve.

This recovers the A12.1 sign quadrants directly from exact certificate dynamics.

For different roots, f's local floor is unchanged, so every nonzero response is mediated by W or C.

## 7. Collective response is witness-reservoir exhaustion

In the A12.2 n-family, for K={a,b},

    W_E(K)=n+1,

because C_0,...,C_n all miss {a,b}.

Each intervention e_j=Add(C_j,a) decreases this ONE coordinate by exactly1.

After any proper intervention subset, W(K)>=2, so candidate f=Add(C_0,a) leaves W(K)>=1 and remains legal.

After all n interventions,

    W(K)=1.

Then f consumes the last witness and makes W(K)=0, so pair {a,b} covers and f is illegal.

Thus the irreducible n-th-order response has a simple exact mechanism: distributed depletion of one global witness reservoir until the final legal margin is exhausted.

No individual intervention carries the collective effect.

## 8. Relabeling covariance

Let root permutation sigma and palette permutation pi act simultaneously on E. They biject physical pairs, candidate covers and roots.

Therefore

    W_(gE)(pi K)=W_E(K),
    C_(gE)(pi H)=C_E(H).

The full W and C fields transform by index permutation only. Consequently:
- the multiset of W values;
- mu_-;
- the number of covers N_4;
- the counts of covers by cardinality;
- all update laws above

are relabeling invariant/covariant.

No coordinate embedding is needed.

## 9. Physics-facing interpretation and limits

The mathematics now supplies an exact native response architecture:

    additions -> consume lower-witness protection / create upper-cover options
    deletions -> create lower-witness protection / consume upper-cover options.

A remote incidence change can alter another root's available move because both participate in the same global certificate field. That is a precise constraint-mediated interaction in the relational state graph.

This is NOT yet a physical force. W is a combinatorial witness multiplicity and C is a cover family. Neither is energy, charge, distance, curvature or stress-energy. No scalar combination is declared conserved.

The next bridge should ask whether an internal observer can access a coarse statistic of these fields and whether repeated ordered updates produce a stable response law under coarse-graining. A physically useful force-like description would require such an operational reduction plus a model-derived update-selection law and scale.

No fundamental time is introduced; only ordered relational updates are used.

v16.54/v16.55 and accepted A11 results remain unchanged. Pending X62-X64 and A12.1/A12.2 are not promoted. Separate efficiency work remains unstarted.
