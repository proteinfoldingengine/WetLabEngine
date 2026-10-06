# A11.X64 scope — exact cycle-breaking slack law for unit handovers

Date: 2026-10-06 UTC.

Status: prospective analytical scope freeze. Analytical only; no numerical campaign, implementation, benchmark, integration merge, or numbered certification.

Accepted analytical parent: A11.X61 candidate f8b96d1fabb4cd15b87cb943a8d87f0f470a9463.
Pending candidates X62/X63 remain pending and are not assumed accepted.

## Objective

Isolate the smallest exact obstruction behind event-level repair cycles without depending on X62/X63.

Study arbitrary ORIGINAL labelled exact-four endpoints with a fixed physical upper cover H that hits every endpoint UNION, and a declared unit-exchange subproblem in which each participating root has exactly one destination-only addition a_i and exactly one source-only deletion d_i.

For every physical pair lacking a common endpoint-union witness, declare an ACTUAL destination witness v and ACTUAL source witness u. In the unit model its protection handoff requires d_v before a_u. Let T be the directed root dependency graph v->u.

A root is saturated when |E_i|=f_i, so its addition must precede its deletion. A root with at least one unit of initial slack may delete first.

Target theorem: the declared minimum-event handover certificate is feasible IF AND ONLY IF the subgraph of T induced by saturated roots is acyclic. Equivalently, every directed dependency cycle must contain at least one root with available slack.

## Required obligations

1. Prove fixed H supplies tau<=4 through every endpoint-only event order because H intersects every E_i union C_i.
2. Prove each declared lower transfer edge v->u is exactly the event precedence d_v -> a_u needed to overlap the chosen old/new witnesses.
3. Prove saturation forces a_i -> d_i, while one unit of initial slack removes that precedence for a unit-exchange root without violating its floor.
4. Prove every event-graph directed cycle alternates transfer and saturated-floor edges and therefore projects to a directed cycle of T entirely inside saturated roots.
5. Prove every saturated directed cycle in T lifts to an event cycle. Hence acyclicity is equivalent.
6. A topological order must give literal one-incidence edits, all floors, actual pair witnesses, finite termination, exact labelled destination and endpoint Hamming minimum.
7. Scope necessity to THIS declared witness-transfer certificate. A cycle does not imply native disconnection; alternative witnesses or nonminimum temporary incidences may work.
8. Derive the feedback-vertex corollary: if one is free to choose which roots receive one unit of initial slack while keeping the declared T fixed, the minimum number of slack roots needed is the directed feedback-vertex number of T. This is a combinatorial resource statement, not physical energy.
9. Compare to X36: X36 shows saturated cycles can also be resolved by a different mechanism using incoming additions before outgoing deletions and transient unfinished-root protection. Therefore X64's cycle law characterizes the simpler endpoint-witness unit certificate, not all repair mechanisms.

## Competing outcomes

- Exact theorem and feedback-vertex corollary.
- Partial theorem if multiple pair obligations on one event invalidate the projection.
- Refutation by an event cycle not corresponding to a saturated root cycle.

## Boundaries

No claim of universal exact-four repair, arbitrary witness-choice optimization, higher target, directed/nested universality, physical force/energy/action, numerical certification or efficiency.

v16.54/v16.55 and evidence remain unchanged. Separate efficiency implementation remains unstarted.
