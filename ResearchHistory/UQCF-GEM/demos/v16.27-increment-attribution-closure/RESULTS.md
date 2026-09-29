# v16.27 — Increment-attribution closure

## Result: EVENT_ATTRIBUTION_PATH_DEPENDENT

The unit increments of v16.26 are not canonically attached to individual removed incidences. Only their endpoint sum is invariant.

Smallest explicit witness:

Tree: root 0 with children 1 and 2.

Before views:
- Y0={0,1}
- Y1={0,2}
- Y2={0,1,2}

After:
- Z0={0,1}
- Z1={0,2}
- Z2={0}

Path A removes event (view2, child1) first: h 1->2, delta=1; then child2: delta=0.
Path B removes child2 first: delta=1; then child1: delta=0.

Thus the same event (view2,child1) has delta 1 on one legal path and 0 on another; likewise for child2. Both paths preserve prefix closure and the common union at every step and reach exactly the same indexed endpoint. Both totals equal h(final)-h(initial)=1.

This refutes universal event-level attribution.

## Bounded audit

All same-union endpoint refinements on rooted trees through four vertices, at most four views, with 2–5 removed nodes were enumerated together with all legal atomic deletion orders:

- endpoints: **3,486**
- endpoints with multiple legal paths: **3,446**
- path-dependent endpoints: **1,091**
- legal atomic paths checked: **56,498**
- canonical search digest: `e8a972f4e1bdf9abe8b3f8599f1414e42e8e8d99b7267cbc092c49f2eb614763`

The remaining multi-path endpoints being path-independent in this bounded universe does not establish a universal theorem for that subclass.

## Interpretation

The v16.26 local minimum-cover trigger is a property of the **current retained state immediately before deletion**. Earlier deletions can change the minimum-cover family, so which later event carries the unit increment can change with legal pruning order.

The invariant content is:

**sum of atomic delta h = h(final)-h(initial).**

The decomposition of that total among individual pruning events is generally not invariant.

This strengthens the guardrail against treating atomic pruning order as a hidden fundamental time coordinate. Ordered pruning is operationally meaningful, but the attribution of an endpoint consistency increase to a particular elementary event can be path-dependent.

No response law or geometry is used.
