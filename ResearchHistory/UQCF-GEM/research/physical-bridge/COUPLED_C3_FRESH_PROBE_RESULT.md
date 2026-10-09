# C3 uniformly safe fresh-label readout with exact restoration
Status: analytical candidate; independent review and publication audit pending.
Scope commit: 4457d8e6abeb4ca96a8a7de03f293ab19348988d.
Inherited event inverse and fixed-core obstruction are pinned at a959ab61dcfd4d65375b41d3a2be4737b4d24123.

## 1. Declared native interface
Let E=(S_1,...,S_N) be a finite labelled family of nonempty supports over a declared finite palette P. Positive immutable floors f_i satisfy |S_i|>=f_i and 3<=tau(E)<=4. A label w in P is globally absent. This is a reserved-label promise across every initially consistent world, not knowledge of any complete support.

Choose a named root r. The controller can issue +w(r) or -w(r). Each request resolves exactly once either to the indicated valid toggle or to NOOP; there are no delayed duplicates, other writers, additional toggles, root/partition/palette changes or changes between resolved slices. Legal requests need not commit. The controller knows the issued address and retains its phase and observed transcript.

For the FULL fixed root family, let M(H)=#{i:S_i intersect H is empty}. The only count coordinates used are
M({w}) and M({w,y}) for y in P minus {w}.
Their exact changes across each resolved request are accessible. This is a restriction of the previously defined field, not a derivation of its accessibility. The controller retains the decoded response after restoration; the incidence state, not observer-plus-carrier memory, is what returns to its initial state.

Alternatively, if N is known and the exact current singleton is available, M({w})=N certifies global absence: every one of the N nonnegative absence indicators must be one. This does not guarantee that the palette has a free label, derive N, or justify using a residual-only count to certify absence from uncounted roots.

## 2. Fresh-label invariance lemma
For any nonempty selected support S_r and a label w absent from EVERY source support, let E+ add w only to S_r. Then
tau(E+)=tau(E).

Proof. Adding an incidence cannot invalidate an old hitting set, so tau(E+)<=tau(E).
Conversely take a hitting set H of E+. If w is absent from H, H also hits S_r before the edit and all other roots are unchanged, so H hits E. If w is in H, choose any s in the nonempty old S_r and set H'=(H minus {w}) union {s}. Every other root was already hit by H minus {w}, because none contains w. The old selected root is hit by s. Thus H' hits E and |H'|<=|H|. Taking a minimum H gives tau(E)<=tau(E+). QED.

The existence of s proves safety; the controller need not identify s. The addition improves the selected floor and leaves the others unchanged. Therefore it is uniformly safe across all nonempty admissible supports satisfying the freshness promise, BEFORE any count response is read. No hypothetical legality query or hidden full-state guard computation is needed to certify this particular action.

Removing w afterwards, with no other edit intervening, restores E exactly and hence restores every original floor and the same hitting number. This is a structural proof about the declared two edits, not a general derivation of an enforcement mechanism for arbitrary requests.

## 3. Star response reads the unknown support
For an actual +w(r) let Delta=M_after-M_before on the star. Since w was globally absent,
Delta({w})=-1,
Delta({w,y})=-1 if y is absent from S_r, and 0 if y is present.

Only root r contributes a changing miss indicator. If y is present, the pair already hits r; if y is absent, adding w changes its pair miss from1 to0. Therefore
S_r = {y in P minus {w}: Delta({w,y})=0}.
A NOOP gives the all-zero response and is distinguished by Delta({w})=0.

The analogous removal has singleton +1 and pair +1 exactly for y absent from the original support. The changed label and address are already those of the unique issued command. Unlike general event inversion, this protocol needs only the fixed marker star, not all pairs.

## 4. Complete phase policy with arbitrary NOOPs
Start in ADD with marker globally absent. Request +w(r).
- If its singleton difference is zero, the outcome is NOOP under the closed atomic interface. Remain in ADD.
- If it is -1, retain the decoded original support and enter REMOVE.

In REMOVE, request -w(r).
- If its singleton difference is zero, remain in REMOVE.
- If it is +1, declare this probe complete.

Any response incompatible with the interface is an error, not permission to infer support or completion. The theorem concerns exact interface-consistent executions, not fault tolerance.

Induction over resolved attempts maintains:
- in ADD the incidence state is exactly the unknown source E, so the same fresh addition remains uniformly safe;
- in REMOVE the state is exactly E+, so removal restores E and is uniformly safe;
- completion has exactly the original labelled incidence state and a retained accurate description of S_r.

Every finite prefix respects every floor and the protected band. A completed probe has exactly two actual incidence toggles, irrespective of how many NOOP attempts occur. This is not an information-theoretic minimum-cost claim.

An execution may stay forever in ADD or REMOVE through NOOPs. In the latter case the marker remains present and the incidence state is not yet restored. Thus neither finite completion nor unconditional eventual restoration is claimed.

## 5. Reuse and completed scans
Only after a completed removal is the marker globally absent again. The same lemma and phase policy may then be applied to another named root.

For any finite prescribed list of roots, if each probe completes, all original supports are preserved exactly at every completed-probe boundary, while their decoded copies accumulate in the retained transcript. Probing all N roots therefore reconstructs the original/current labelled incidence family after 2N actual toggles, returning that family to its exact original state. No arbitrary physical clock or fairness is used.

This is a conditional controllable readout. The ability to retain the transcript and access counts remains a premise; the proof does not build an internal physical observer.

## 6. A genuine gain beyond the initial aggregate
Reuse the independently closed native swapped-root example:
fixed roots {a,b},{b,c},{a,c}, two residual supports {d,e,u},{d,e,v}, assigned to r0,r1 in World A and swapped in World B. All floors2 and tau3. Choose a globally unused w.

The complete initial aggregate miss fields agree in the two worlds, even if queries of every degree are allowed. Yet +w(r0) is uniformly safe in both by the lemma. Its pair response on {w,u} is zero in A and -1 in B, revealing the selected support. Removal returns each world to its own exact source. This is not merely reading information that the initial aggregate had already assigned to the labelled root.

The previous event inverse only decoded a supplied actual transition. The present composition supplies a structurally certified safe transition BEFORE that readout is available, and a restoration policy. It removes pre-probe support/prospective-legality access for this restricted protocol. It does not remove the assumed count-difference channel.

## 7. Rejecting native controls
Global freshness matters. For E=({a,b},{b,c},{a,c},{d,e}), tau=3 and all floors2. Label d is absent from r0 but present elsewhere. Adding d at r0 gives a two-cover {c,d}; the band is violated. Local absence is insufficient for the lemma.

Premature reuse matters. Add a fresh u at r0 of the same E; tau remains3. Before removing it, also add u at r3. Now {c,u} hits all four roots, so tau becomes2. Reuse requires certified completed removal, not merely knowing the marker was fresh at the start of a larger sequence.

The old fixed-core obstruction is preserved. Compare E(empty) and E({u}) in the four-root prepared carrier, and probe the fourth root with a fresh w, then restore. Core projections, all core-only miss counts, tau3 and floor-validity flags agree throughout both histories. The star pair {w,u} is outside that fixed-core channel and distinguishes the supports. The result therefore does not contradict the closed safe-probe impossibility theorem or derive its missing observable.

The native controls are mathematical assumption checks, not claims that unsafe commands are permitted by the protected controller.

## 8. Evidence scope and limits
The frozen algebraic test domain contains 399 ordered nonempty-support families on three base labels with one to three roots, 1134 selected-root contexts, and 4536 phase/outcome records. Floors are the original support sizes. Every source and successor is checked for exact tau invariance and floor preservation; this generic domain includes tau1 and tau2 and is not a protected-only census.

Production uses direct disjointness and hitting-subset enumeration. Independent verification uses Boolean incidence enumeration, occupancy/co-occupancy star fields, minimum unions of one representative per root, and candidate-support search for inversion. Complete identities/values, not just totals, must agree. Separate floor-two native controls and an eight-toggle four-root scan are included. The inherited event suite covers the swapped-root control.

Eleven local RED failures precede implementation. GitHub execution, independent mathematical review, publication audit and author reconciliation are required before scoped closeout. No full numbered-stage certification is claimed.

The remaining native-origin obligation is the accessibility and retention of the marker-star counts and resolved exclusive request interface, together with availability or certification of a free marker. No force, geometry, dark matter, fundamental time or GR derivation follows. Broader C3/C4-C6 remain OPEN; path A active.
