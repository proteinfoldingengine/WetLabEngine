# v16.30 — Pre-adjudication proof ledger

## P1 — parent locality of tau

Fix a retained union U. tau_v is defined solely from the family A_i(v)=Ch_U(v) intersect Y_i. Deleting a node c from a view changes A_i(v) only when parent(c)=v. Therefore deletions whose removed nodes have another parent leave every A_i(v), and hence tau_v, unchanged.

This proves C1 and C3 directly from the existing definition.

## P2 — exact profile factorization by parent

Partition deletion events by p(e)=parent(node(e)), writing E_v. For any reachable state S, the child-incidence family at v is determined by the initial cover and S intersect E_v alone. Thus there is a uniquely induced finite function f_v on reachable restrictions with

tau_v(S)=f_v(S intersect E_v).

Hence the vector profile factors coordinatewise by parent. This is stronger than pairwise-zero evidence and does not depend on enumeration.

It follows that G_tau has no edge across parents, proving C2. v16.29's MAX_ONLY effects are therefore properties of max aggregation, not cross-parent dependence in tau.

## P3 — what is not yet proved

Within a single parent, pairwise connected components are defined by witnessed nonzero second differences. Pairwise vanishing alone does not prove absence of higher-order dependence for an arbitrary finite function. The checker must demonstrate this using a pure three-way control.

Whether the special minimum-set-cover function tau_v forbids such higher-order cross-component dependence is the open C5 adjudication. No conclusion is preregistered.

## P4 — order constraints versus interaction

If two events are comparable in the deletion poset, they are never simultaneously enabled at a reachable state. Their ordering is inherited prefix legality, not evidence of a nonzero mixed difference. G_tau contains only incomparable, jointly enabled pairs.

No physical subsystem, coupling, geometry or time variable is inferred from these mathematical components.

## P5 — pairwise graph completeness on independently enabled cubes

Let f be any integer-valued function on a finite Boolean cube of independently executable events, and partition the events into connected components of the graph joining a pair whenever some second mixed difference is nonzero at some background. If e and f lie in different components, then by definition Δ_eΔ_f f(S)=0 for every background S enabling both.

Fix a component C. For any e in C, the first difference Δ_e f(S) is unchanged when any event outside C is toggled, because the corresponding second difference is zero. By successive toggles, Δ_e f depends only on S∩C. Choose a reference state and integrate these first differences within each component. This gives

f(S)=f(∅)+Σ_C g_C(S∩C).

Therefore every Möbius coefficient whose support crosses two graph components is zero. Conversely a nonzero cross-component Möbius coefficient would force some cross-component second difference at a suitable background. Thus the pairwise graph gives the exact additive factorization for independently executable events.

For retained pruning, apply this to each reachable Boolean subcube. Comparable predecessor-constrained events do not form such a cube and are not interaction edges; they remain order constraints. Combining P2 with this result gives a two-level decomposition: exact parent locality first, then exact pairwise-component factorization inside each independently executable parent-local cube.

This proves candidate C5 outcome **PAIRWISE_GRAPH_COMPLETE**. The executable Möbius search is a verifier of the implementation and includes a pure three-way checker control; universality rests on this finite-difference argument, not on bounded absence.
