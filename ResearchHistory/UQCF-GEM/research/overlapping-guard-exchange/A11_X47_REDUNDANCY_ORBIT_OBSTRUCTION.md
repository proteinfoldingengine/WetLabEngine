# A11.X47 — redundancy/orbit orthogonality and the sharp bad-window quotient

Exact analytical candidate. Scope `0ba8354bec6446552a3f522babd4757ef1f3652e`; accepted analytical parent `362844769130098871e2a38f154bcd28e808cf6c`.
No numerical execution, implementation, benchmark or numbered certification.

## 1. Native carrier and typed statements

Fix a finite ordered palette (P), labelled original roots and their SAME ORIGINAL positive floors (a_i). One primitive toggles ONE incidence in ONE root. Larger temporary supports remain native; no label or root is added, no floor is weakened, and no simultaneous move, compactness, geometry or fundamental time is imposed.

Use the restored mask setting of X45–X46: nonempty role groups partition (P), SAME nonempty actual masks (Q_isubseteq G), and every restored root is the union of the groups indexed by its mask. Let (mathcal H_4) be the family of all four-role covers. For a directed simple ownership cycle
[
C=(c_0,ldots,c_{ell-1})
]
write
[
W_t={c_t,c_{t+1},c_{t+2},c_{t+3}},
quad
B_i(C)={t:W_tcap Q_i=arnothing}.
]
Indices are cyclic. Define
[
B(C)=igcup_i B_i(C),qquad
eta(C)=|B(C)|,qquad
Gamma(C)=sum_i|B_i(C)|.
]

**X47B (duplicate-insensitive bad-window theorem).** (B(C)) is exactly the set of bad cyclic four-windows, so (eta(C)) is the exact number of bad starts and
[
eta(C)leqGamma(C).
]
If
[
eta(C)<lceilell/2ceil,
]
two cyclically consecutive windows cover every actual root, hence X45's representative criterion holds. This is the sharp universal threshold using (eta) alone: for every even (ellgeq8), equality (eta=ell/2) can have alternating good and bad starts and no adjacent good pair. The exact adjacency test is stronger; the strict scalar bound is sufficient, not necessary.

**X47O (redundancy/orbit orthogonality family).** For every even (mgeq8) and every integer (dgeq1), there is a saturated exact-four template on (m) singleton roles and a destination whose ownership graph is one directed (m)-cycle such that:

1. its only four-covers are the (m/2) even-start cyclic four-windows;
2. X45's exact SAME-representative intersection is empty for the prescribed and only ownership cycle;
3. (eta=m/2) and (Gamma=dm/2);
4. its actual minimum pair-witness redundancy is
   [
   ho=dleft[inom{m-2}{2}-2ight],
   ]
   which can be made arbitrarily large without changing the cover family, (eta), the ownership cycle or the X45 obstruction;
5. accepted X40L nevertheless supplies a complete lower-protected endpoint path, and accepted maximum-layer Theorem A converts that complete lower path to a ({3,4})-band path between the exact endpoints.

Thus exact-four consistency and arbitrarily large raw pair redundancy do not force X46's strict gap condition or X45 representative compatibility. This is not native disconnection, not failure of every direct upper construction, and not failure of a band path.

## 2. The exact quotient behind X46

A start (t) is bad precisely when some actual mask misses (W_t), precisely when
[
tinigcup_i B_i(C).
]
Therefore (eta) is exact and the inequality (etaleqGamma) is only the union bound. Duplicating a labelled root repeats one set (B_i): it can multiply (Gamma) while leaving the union and (eta) unchanged.

If (eta<lceilell/2ceil), the number of good starts is at least
[
ell-lceilell/2ceil+1=lfloorell/2floor+1.
]
A subset of a cyclic (ell)-set with no adjacent positions has size at most (lfloorell/2floor). Hence two good starts (t,t+1) exist. For the forward cycle rotation (pi(c_s)=c_{s+1}),
[
pi(W_t)=W_{t+1}.
]
Both windows lie in (mathcal H_4), so
[
W_tinmathcal H_4cappi^{-1}(mathcal H_4).
]
X45's declared representative lift applies.

No converse follows. A bad-set arrangement smaller than the strict threshold is universally safe; at equality the alternating arrangement is possible. Above the threshold, adjacent good starts may still exist. Thus (eta<lceilell/2ceil) is the sharp count-only guarantee, not an iff criterion.

## 3. Alternating-window template

Let (G=mathbb Z/mmathbb Z), with (mgeq8) even, in its cyclic order. Put
[
W_t={t,t+1,t+2,t+3}
]
and declare
[
mathcal H_{m alt}={W_t:t {m is even}}.
]
For every four-set (Jsubseteq G) with (J
otinmathcal H_{m alt}), declare (d) distinct labelled original roots, all having actual mask
[
Q_{J,s}=Gsetminus J,qquad 1leq sleq d.
]
There are no other roots. Every mask has width (m-4). Give each copy the saturated original floor
[
a_{J,s}=m-4.
]

### Exact four-cover family

For a four-set (Isubseteq G),
[
Icap Q_{J,s}=arnothing
iff Isubseteq J
iff I=J.
]
Consequently (I) hits every declared root exactly when its complementary mask was omitted, exactly when
[
Iinmathcal H_{m alt}.
]
Thus the family of all four-role covers is precisely (mathcal H_{m alt}).

Every three-set (T) has (m-3geq5) four-set extensions. A three-set belongs to at most two cyclic length-four windows: if its points are contained in such a window, the possible starts form at most the two extensions of a consecutive triple; all other arrangements have no more possibilities. Hence at most two extensions lie in (mathcal H_{m alt}). Choose an extension (J
otinmathcal H_{m alt}); then (Q_{J,s}) misses (T). Any smaller set extends to a three-set and is missed as well. Therefore the template transversal is exactly four.

The cover density is
[
rac{|mathcal H_{m alt}|}{inom m4}
=rac{m/2}{inom m4}
=rac{12}{(m-1)(m-2)(m-3)}<rac12
]
for every (mgeq8), and tends to zero.

## 4. Ownership cycle and exact upper obstruction

Give every role one actual label (x_t). The source groups are the singletons ({x_t}). At the destination send (x_t) to role (t+1). The incorrect-owner graph is exactly one directed simple (m)-cycle, with no alternative nontrivial simple cycle.

Let (pi(t)=t+1). It maps every even-start window to an odd-start window. Odd-start windows are not in (mathcal H_{m alt}), so
[
mathcal H_{m alt}cappi^{-1}(mathcal H_{m alt})=arnothing.
]
By X45C, no four SAME representatives from the declared one-per-role pool cover both restored endpoints for this prescribed cycle. Since the ownership graph has only this cycle, cycle choice cannot repair the failure.

This is exactly a limitation of X45's representative lift. It does not say that no other four-label strategy, no direct upper path or no native path exists.

The good starts are the even positions and the bad starts are the odd positions. Hence
[
eta=m/2.
]
A bad window (W_t) is missed by (Q_{J,s}) only if (W_tsubseteq J), hence only if (J=W_t). Exactly its (d) labelled complementary roots miss it. No root misses a good window. Therefore
[
Gamma=dm/2.
]
For (d=1), (Gamma=eta=m/2); the strict X46/X47 scalar bound fails at equality and no adjacent good starts exist. This proves sharpness. Increasing (d) leaves (eta) and the exact obstruction unchanged while making the union-bound budget arbitrarily loose.

## 5. Exact pair redundancy and X40 lower repair

A root (Q_{J,s}) avoids a role pair (K) exactly when (Ksubseteq J). There are (inom{m-2}{2}) four-sets containing (K). The only omitted such sets are members of (mathcal H_{m alt}) containing (K).

A pair lies in at most two even-start cyclic four-windows. Indeed, among all length-four windows containing a fixed pair, the possible starts form an interval of at most three consecutive cyclic positions, of which at most two have even parity. An adjacent pair in the appropriate parity position lies in two, so the maximum two is attained. Thus the minimum number of actual avoiding roots is exactly
[
ho=dleft[inom{m-2}{2}-2ight].
]

Already for (d=1),
[
inom{m-2}{2}-2-(m-2)
=rac{(m-1)(m-6)}2geq0.
]
Hence (hogeq m-2), and
[
inom{2ho}{ho}
geq inom{2m-4}{m-2}
geq inom{2m-4}{2}
>rac{m(m-3)}2
]
for (mgeq8); the last difference is ((3m^2-15m+20)/2>0). Accepted X40L therefore applies.

X40L supplies a complete path between the labelled exact endpoints with actual pair witnesses, (	augeq3), literal add-before-delete primitives, same-slot floor legality, eligible continuation, renewal, strict finite progress and FULL exact labelled/noncompact restoration. This use of redundancy is substantive: X47 does not say redundancy is useless.

Because X45 compatibility fails, this argument does not produce X40's event-minimum direct upper lift. Instead, after the complete lower-protected path exists, accepted maximum-layer Theorem A converts that complete endpoint-to-endpoint path to the one-unit band (3leq	auleq4). The converted path need not preserve the preliminary schedule, its event minimum or an unfinished waypoint. These two conclusions must not be conflated.

## 6. Saturation and method controls

All root sizes and floors equal (m-4), so the endpoints are completely saturated and no root-floor reserve exists. Singleton source and destination groups have equal positive corresponding size.

**X38:** the unique nontrivial ownership cycle has length (mgeq8), outside its short-cycle premise.

**X39:** every actual mask has width (m-4<m-3), outside its dense-width premise.

**X40U:** all role groups are singletons, so no cover role contains two representatives. X40L applies only to the lower proof.

**X41:** all role incidence profiles are distinct. For (a
e b), among the (inom{m-2}{3}) four-sets containing (a) and not (b), at most two lie in (mathcal H_{m alt}); choose another (J). Then (Q_J) omits (a) and contains (b). A cell in any union-partition representation of the same endpoint must be profile-homogeneous, so roles cannot merge. Every actual mask contains (m-4geq4) distinct profiles, so no root is a singleton cell.

**X43:** for every actual mask, (p=m-4) and complement size (n=4). Its size premise (ngeq p+3) would require (4geq m-1), false.

**X44:** Section 3 gives cover density below one half.

**X45:** Section 4 proves the exact representative intersection empty for the prescribed only cycle.

**X46:** (Gamma=dm/2
ot<lceil m/2ceil=m/2). At (d=1) the threshold is met exactly and adjacency fails.

Four pairwise disjoint saturated supports would require (4(m-4)>m) incidences for (mgeq8), so no four private floor-safe roots fit.

The whole endpoint union is two-covered. Choose even (t) and labels (x_t,x_{t+2}). Their source/destination role footprints are ({t,t+1}) and ({t+2,t+3}); together they form (W_tinmathcal H_{m alt}). Hence the pair hits every root's source/destination union. Simultaneous whole-union preparation is unsafe.

Every root changes. If a mask (Q_J) were invariant under the full rotation, its four-set complement (J) would be invariant. A nonempty invariant subset of a transitive (m)-cycle is all of (G), impossible because (|J|=4<m).

These are controls on prior sufficient methods, not a no-path theorem. Certified L also supplies connectivity for these symmetry endpoints.

## 7. Scientific conclusion and next obligation

The lower and upper resources are orthogonal. Pair redundancy counts actual roots missing each forbidden pair and can force a complete reusable lower-protected repair. Orbit-compatible upper transport asks how the minimum four-covers are organized under the actual ownership permutation. Exact-four consistency does not couple these structures, and labelled duplication can amplify the former without changing the latter at all.

The sharper structural variable is the union of rootwise bad-window sets, not their multiplicity sum. Yet even exact (eta) gives only a sharp scalar guarantee; the full adjacency pattern of good windows remains the exact X45 condition for this representative lift.

A stronger theorem must therefore impose or derive a **joint/correlated condition** linking actual lower witnesses to transitions among actual four-covers—perhaps an overlap-corrected bad-window structure or a cycle-selection rule tied to cover adjacency. More raw witness count alone cannot close the gap.

No claim is made for arbitrary endpoints, unequal corresponding group sizes, below-X40 lower repair, every possible direct upper strategy, mixed/directed/higher-target/nested universality, literature originality or physical interpretation. No numerical execution, workflow, benchmark, integration merge or numbered certification is authorized. v16.55/v16.54, frozen sources and all original evidence remain unchanged. The separately promised efficiency implementation/fixtures/benchmarks remain unstarted.

Fresh independent whole review must check X47B/O together: exact bad-window union and sharpness; exact four-cover/no-three proof; ownership orientation and empty X45 intersection; exact (eta,Gamma,ho); duplication; X40 inequality and lower/A distinction; saturation, method/profile separations, private/whole-union controls; and every stated limit.
