# Independent whole-argument review — A11.X47

Reviewer: independent Codex review agent `/root/x47_whole_argument_review`  
Date: 2026-10-05 UTC  
Repository: `proteinfoldingengine/WetLabEngine`  
Exact reviewed candidate: `88f0c93d314d95c4b8a9a6ed6d75be05cfc109ea`  
Exact reviewed tree: `9c58efcb9be6f902fd54e222e2bc0ab26f173047`

Reviewed sources:

- `A11_X47_SCOPE.md`
- `A11_X47_REDUNDANCY_ORBIT_OBSTRUCTION.md`
- inherited `A11_X40_SPARSE_WITNESS_RENEWAL.md`
- inherited `A11_X45_ORBIT_COVER_TRANSPORT.md`
- inherited `A11_X46_CYCLE_GAP_TRANSPORT.md`
- the declared accepted maximum-layer Theorem A dependency

## Verdict

**ACCEPTED.** I found no mathematical correction required in the exact frozen candidate. The candidate proves the stated duplicate-insensitive bad-window criterion and the alternating-window obstruction family, while keeping the failed X45/X46 upper lift distinct from native connectivity and from the X40L-plus-Theorem-A band conclusion.

## 1. Exact bad-window quotient and sharp count-only boundary

For a fixed directed cycle, a start is bad exactly when at least one actual mask misses its four-window. Hence the bad starts are exactly

[
B(C)=igcup_i B_i(C),
qquad
eta(C)=|B(C)|,
]

and (etaleqGamma=sum_i|B_i|) is precisely the union bound. Repeating a labelled mask repeats one summand but not the union, so the claimed duplicate sensitivity of (Gamma) and duplicate insensitivity of (eta) are correct.

If (eta<lceilell/2ceil), the number of good cyclic starts is at least (lfloorell/2floor+1). A cyclic independent set has size at most (lfloorell/2floor), so consecutive good starts exist. With the declared forward orientation (pi(c_t)=c_{t+1}), one has (pi(W_t)=W_{t+1}), giving an element of (mathcal H_4cappi^{-1}(mathcal H_4)). This exactly matches X45C.

The even-cycle family realizes (eta=ell/2) with alternating good and bad starts and no adjacent good pair. It therefore proves that the strict threshold cannot be weakened as a universal scalar guarantee. The manuscript correctly does not claim necessity: configurations at or above the boundary may still have adjacent good starts.

## 2. Exact-four alternating-window template

Let (G=mathbb Z/mmathbb Z), with even (mgeq8), and omit exactly the even-start cyclic four-windows from the complementary-root list. For every declared root (Q_J=Gsetminus J) and every four-set (I),

[
Icap Q_J=arnothing
iff Isubseteq J
iff I=J.
]

Thus a four-set hits every declared root exactly when its complementary root was omitted, so the complete four-cover family is exactly the even-start windows.

Every three-set has (m-3geq5) four-set extensions. A three-set is contained in at most two cyclic four-windows, hence in at most two members of the omitted even-window family. Therefore some declared complementary root misses it. Extending smaller sets to three-sets handles all sizes below three. Since an omitted even window is a four-cover, the transversal is exactly four. The stated cover density follows algebraically and is below one half for the whole declared range.

## 3. Ownership orientation and exact representative obstruction

Sending (x_t) from role (t) to role (t+1) gives one directed full (m)-cycle and no alternative nontrivial simple ownership cycle. Its role permutation sends every even-start window to an odd-start window. Therefore

[
mathcal H_{m alt}cappi^{-1}(mathcal H_{m alt})=arnothing.
]

This is the exact failure of X45C for the declared one-representative-per-role pool and the only available ownership cycle. The candidate accurately limits the conclusion: it does not exclude other upper strategies or any native path.

The good starts are even and the bad starts odd, so (eta=m/2). A four-window can be missed by (Q_J) only when it equals (J); consequently each odd window is missed by exactly its (d) labelled complementary copies, no good window is missed, and (Gamma=dm/2). These values and the duplication claim are exact.

## 4. Exact pair redundancy and inherited lower repair

A declared root avoids a role pair (K) exactly when (Ksubseteq J). There are (inom{m-2}{2}) four-sets containing (K). A pair lies in at most two even-start length-four windows: all possible starts form at most three consecutive cyclic positions, of which at most two have even parity. An appropriately placed adjacent pair attains two. Thus the minimum number of actual avoiding roots is exactly

[
ho=dleft(inom{m-2}{2}-2ight).
]

For (d=1),

[
inom{m-2}{2}-2-(m-2)=rac{(m-1)(m-6)}2geq0.
]

Central-binomial monotonicity then gives

[
inom{2ho}{ho}
geq inom{2m-4}{m-2}
geq inom{2m-4}{2}
>rac{m(m-3)}2,
]

where the final difference is ((3m^2-15m+20)/2>0) for (mgeq8). The hypotheses of accepted X40L therefore hold, and labelled duplication only strengthens them.

The proof correctly separates conclusions. X40L supplies the complete endpoint-to-endpoint lower-protected path with actual pair witnesses, floors, renewal, progress and exact restoration. Only after that complete path exists may accepted Theorem A convert it to a ({3,4})-band path. The conversion does not preserve X40's schedule, event minimum or unfinished waypoints. X47 does not claim a direct representative upper lift.

## 5. Saturation, separations and controls

All masks and floors have size (m-4), so the endpoint is saturated. The stated sufficient-method separations check out:

- X38: the only nontrivial ownership cycle has length (mgeq8).
- X39: every mask has width (m-4<m-3).
- X40U: every role group is a singleton; only X40L is used.
- X41: distinct roles have distinct incidence profiles. Among the (inom{m-2}{3}) four-sets containing one prescribed role and not another, at most two are even-start windows, so a declared complementary root distinguishes the roles. Every actual root contains at least four distinct profiles and cannot be a singleton cell.
- X43: its size premise would require (4geq m-1), false here.
- X44: the exact cover density is below one half.
- X45: the exact prescribed representative intersection is empty.
- X46: (Gamma=dm/2
ot<lceil m/2ceil=m/2).

The auxiliary controls are also valid. Four pairwise disjoint floor-safe supports would require (4(m-4)>m) labels. For even (t), the source/destination footprints of (x_t,x_{t+2}) unite to the covering window (W_t), so that pair hits every whole endpoint-union root. Finally, no root is unchanged: invariance of (Q_J) under the full rotation would make its nonempty four-element complement invariant under a transitive (m)-cycle, which is impossible for (4<m).

## 6. Scope and scientific interpretation

The accepted conclusion is an orthogonality result: arbitrarily large actual lower pair-witness redundancy does not force organization of minimum four-covers along the ownership orbit. The sharper scalar for the X46 counting step is the duplicate-insensitive union size (eta), while the full adjacent-good-window pattern remains the exact X45 representative test.

This review does **not** accept a disconnection theorem, failure of all direct upper constructions, universality for arbitrary endpoint representations, unequal corresponding group sizes, below-X40 lower repair, mixed/directed/higher-target/nested connectivity, implementation, numerical certification, originality or physical interpretation. The next stated obligation—derive a genuinely joint condition coupling lower witnesses to upper-cover transitions rather than increasing raw redundancy alone—is correctly supported by the obstruction.

No numerical work was needed or performed for this analytical review. Certified v16.55/v16.54 and their evidence are outside the mutation scope of X47.
