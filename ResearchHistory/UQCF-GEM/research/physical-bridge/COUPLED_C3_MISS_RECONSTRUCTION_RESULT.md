# C3 sharp reconstruction threshold for retained miss counts
Status: analytical candidate; independent verification/review and separate publication audit pending.
Scope commit: 9c75d6ed5d7f5452c97032f64b50904171b69d28.
This is a finite combinatorial result about an existing conditional guard record. It does not derive observer access or physical record origin.

## 1. Objects and claim
Fix a finite palette P of k labels and N known residual slots. Their supports S_1,...,S_N are subsets of P, with repetitions allowed. Define
M(H)=sum_i 1[S_i intersect H is empty]
for every H subset P with |H|<=d, where d is a nonnegative integer and M(empty)=N.

The reconstruction target is the unordered multiset of supports, including multiplicities. Slot addresses and slot-specific floors are not part of this aggregate record.

**Theorem.** If N<2^d, the complete field M through degree d uniquely determines the support multiset. For palettes with at least d+1 free labels the threshold is sharp: two different multisets of N=2^d supports can have identical fields. In particular, the existing degree-four field determines every residual support multiset with N<=15. At N=16, nonuniqueness occurs even in an explicit floor-two protected native carrier.

This is a sufficient universal threshold, not a claim that every N>=16 record is ambiguous. For d>=k, the full Boolean transform is invertible at every N; sharpness requires enough labels.

## 2. Integer cancellation lemma
Let f:{0,1}^k -> integers be nonzero. Suppose
sum_x f(x) product_{j in H} x_j = 0
for every H with |H|<=d, including H empty. Let A(f)=sum_x max(f(x),0). Then
A(f)>=2^d.
The empty moment also makes total negative mass equal to A(f).

Proof by induction on d, simultaneously for all finite dimensions k.
For d=0, zero total and nonzero integer f require at least one positive integer coefficient, so A(f)>=1.

For d>=1, zero total implies that the support of f contains at least two distinct Boolean vectors. Choose a coordinate j on which two such vectors differ. Restrict f to the slices x_j=0 and x_j=1, obtaining nonzero arrays f_0,f_1 on k-1 coordinates.

For any monomial m of degree at most d-1 in the remaining coordinates,
sum f_1 m = sum f x_j m = 0.
Also
sum f_0 m = sum f m - sum f x_j m = 0.
Both arrays therefore satisfy the induction hypothesis of degree d-1. Their positive masses are each at least 2^(d-1). The slices are disjoint, so
A(f)=A(f_0)+A(f_1)>=2^d.
This proves the lemma. If the ambient dimension is too small to support such an f, the hypotheses are simply impossible; no nonexistent coordinate is assumed, since a varying coordinate is chosen only from two distinct supported vectors.

Integrality is essential to the stated numerical mass bound. This is not a theorem about arbitrary rescaled signed real weights.

## 3. Uniqueness and reconstruction
Represent a support S by its absence vector x(S), with x_j=1 exactly when j is absent from S. Then its contribution to M(H) is exactly product_{j in H} x_j.

Suppose two support multisets, each of size N, have the same field. Let f be the difference of their multiplicity arrays on absence vectors. All its moments through degree d vanish. After cancellation of common supports its positive mass is at most N. If the multisets differ, the lemma yields
2^d <= A(f) <= N,
contradicting N<2^d. Hence the multiplicity arrays agree.

An explicit finite reconstruction procedure is to enumerate all nonnegative integer multiplicity arrays on the 2^k subsets with total N, evaluate their miss fields, and retain the matching array. At least one matches when the supplied field is valid; the theorem gives exactly one when N<2^d. Invalid fields have no match. This is an exact terminating procedure, not an efficiency claim or an observer acquisition mechanism.

N must be known: a support equal to the full palette contributes zero to every nonempty miss query, so adding copies of that support is invisible if the empty query/slot count is omitted.

## 4. Sharpness
On d+1 free labels, take all even-cardinality subsets on one side and all odd-cardinality subsets on the other. Each side has 2^d supports and they are different.

For any H with |H|<=d, at least one free label remains outside H. Toggling that label pairs even and odd subsets that avoid H. Thus the numbers of supports disjoint from H agree. The empty query agrees as well. This proves sharpness in the algebraic class, including d=0.

## 5. Degree-four boundary inside the native protected class
Take core labels a,b,c,d,e and five spectator labels u,v,w,x,y, all distinct. There are three fixed roots {a,b},{b,c},{a,c} and sixteen labelled residual slots. In World E, residual supports are {d,e} union A for every even subset A of the five spectators. In World O use every odd subset. Assign these supports to the sixteen slots in any fixed declared order. Every original floor is two.

All residuals contain d,e, so all floors hold. The triangle needs two hits; residual supports are disjoint from its labels and need at least one further hit. A triangle two-cover together with d hits every root. Therefore both full worlds have tau=3, inside the inherited band [3,4].

The residual support multisets differ. For any query H of size at most four:
- if H meets {d,e}, both residual miss counts are zero;
- otherwise its core labels a,b,c are irrelevant to residual intersections;
- write J=H intersect {u,v,w,x,y}. At least one spectator remains outside J, and toggling it pairs even/odd subsets avoiding J.

Thus every retained full-palette degree-four residual count agrees. With five spectator labels in the query, World E has one residual miss (A empty), World O has zero. The ambiguity is exactly real, not a root-slot permutation.

The fixed triangle contributes the same counts in both worlds, so full-family degree-four counts also agree. This native fixture has 19 total roots and 16 residual roots; the threshold theorem is applied to the declared residual family, not misreported as 16 total roots.

## 6. Labelled reconstruction and C3 significance
The counts are invariant under permuting residual slot addresses. Even when the multiset is unique, an exchange of two distinct supports between labelled slots is not observable from this field alone. If a separately retained core projection uniquely identifies which slot each recovered support belongs to, that extra matching data can restore addresses; it is an additional available input, not part of M.

Consequently, in small-root carriers, describing the initialized full-palette field as a compressed hidden-state interface needs care: for N<=15 it retains the entire unordered support multiset. Core-only counts are different and are not covered by this reconstruction claim because their query palette omits spectator coordinates.

The result quantifies information already present in the conditional dynamic-residual guard. It does not justify obtaining that information from core observations, derive initialized counts, supply an actual outcome selector, or resolve guard enforcement. It sharpens the dependency ledger rather than closing native record origin.

## 7. Verification boundary
The frozen finite algebraic universe consists of all multisets of size 0 through 4 on three labels, evaluated at degrees 0 through 3. The 495 multisets produce 1980 degree-tagged records. This includes empty supports and is not described as a protected native campaign. The separate parity fixture checks the native floor-two, tau-three example and all 385 nonempty queries on its ten-label palette of size at most four.

Production uses direct disjointness on combinations with replacement. Independent checking enumerates occupancy compositions and computes a Boolean superset zeta transform; it reconstructs complete canonical identities and values without importing production. General uniqueness follows from the signed-integer proof, not this small enumeration.

Nine local contracts cover full identity equality and corruption/scope controls; the initial absent implementation yielded nine intended local RED failures. CI, independent mathematical review, separate publication audit and author reconciliation remain required. No numbered-stage full inherited certification is asserted.

No fundamental time, physical force, geometry, dark-matter variable or GR derivation is introduced. Broader C3 remains OPEN.
