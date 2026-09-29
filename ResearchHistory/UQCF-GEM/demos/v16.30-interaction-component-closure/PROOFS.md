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
