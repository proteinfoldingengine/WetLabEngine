# Automatic retained upper-cover handoff scope

Date: 2026-10-06 (America/Phoenix).
Status: PROSPECTIVE ANALYTICAL SCOPE.

Parent phased-event closeout:
- PHASED_EVENT_INTERFACE_CLOSEOUT.md at e50ccd46bd3adae7ae9b9f359570a04a297a8ae5.

## Objective

Derive PREPARE -> HANDOFF -> FINISH event precedence automatically from retained source/target cover signatures rather than supplying the partition by hand.

This theorem handles the upper condition tau<=4. Require an independent fiber-uniform lower certificate guaranteeing tau>=3 for every endpoint-contained event state considered. Deriving lower witness handoff is outside this item.

## Endpoint event domain

For each original labelled root i retain the endpoint projection needed for two supplied physical covers:
- old cover H0, |H0|<=4, which hits every source root;
- replacement cover H1, |H1|<=4, which hits every target root.

Allowed native events are endpoint-only additions C_i minus E_i and deletions E_i minus C_i. Common incidences do not move.

Retained address data identify these endpoint-differing events on H0 union H1. Hidden invariant incidences outside the retained projection may vary but must not alter the independent lower certificate.

## Automatic gains

For root i:
- if E_i intersect C_i intersect H1 is nonempty, H1 has a permanent common hit and needs no preparation;
- otherwise choose deterministically one g_i in (C_i minus E_i) intersect H1.

Because H1 covers the target, such g_i exists whenever no common H1 hit exists.

Add edge
    Add(g_i) -> HANDOFF.

## Automatic old-cover holds

For root i:
- if E_i intersect C_i intersect H0 is nonempty, H0 has a permanent common hit and needs no hold edge;
- otherwise choose deterministically one l_i in (E_i minus C_i) intersect H0.

Because H0 covers the source, such l_i exists whenever no common H0 hit exists.

Add edge
    HANDOFF -> Delete(l_i).

This guarantees at least one old H0 incidence remains in every root until handoff.

## Floor-safe event order

For each root, impose every destination-only addition before every source-only deletion in that root. This is a sufficient floor rule because support never falls below min(|E_i|,|C_i|), assumed >= original floor.

Other endpoint events may occur whenever their graph predecessors permit.

## Required theorem

1. Before HANDOFF, H0 hits every root.
2. When HANDOFF becomes enabled, H1 hits every root.
3. After HANDOFF, H1 remains a cover.
4. Therefore tau<=4 throughout every topological event execution.
5. With the independent lower certificate, 3<=tau<=4 throughout.
6. The derived event graph is acyclic: all native precedence runs from additions toward deletions, with HANDOFF between required gains and held losses.
7. Every endpoint event executes once and exact labelled destination is reached.
8. Hidden-fiber legality/update must be uniform from retained endpoint signatures.

## Concrete embedding

Apply the rule to the closed macro-cycle carrier with
    H0={a,c},
    H1={a,b}.

Derive automatically:
- p requires Add b before HANDOFF and holds Delete c until after HANDOFF;
- q requires Add b before HANDOFF and holds Delete c until after HANDOFF;
- r has common b for H1 and holds Delete a until after HANDOFF;
- q's Delete f is not an H0-loss event and receives only floor/event-syntax constraints.

Show that this automatically generated graph contains the essential edges of the hand-supplied phased graph and admits a protected interleaving without manually prescribing the prepare/finish partition.

## Boundaries

This is an upper-cover theorem. It does not derive tau>=3. It does not claim all endpoint pairs possess suitable H0,H1 or an independent lower certificate.

Next frontier: automatic lower pair-witness handoff and then joint upper/lower event synthesis.
