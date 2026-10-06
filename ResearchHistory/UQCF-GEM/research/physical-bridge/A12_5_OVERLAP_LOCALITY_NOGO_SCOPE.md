# A12.5 scope — no-go for naive incidence-overlap locality

Date: 2026-10-06 UTC.
Status: prospective analytical physics-bridge scope. Native exact control; no numerical campaign, geometry, force law or continuum claim.

## Objective

Test whether exact candidate admissibility can be determined from a bounded neighborhood in the obvious root-overlap graph.

Define the root-overlap graph G_E: original roots i,j are adjacent iff E_i intersect E_j is nonempty. For candidate move f on root i, its radius-r overlap data consists of the induced labelled incidence structure on roots within graph distance<=r from i, with their original floors and f's candidate incidence.

Target no-go: construct two protected exact states with the same palette size, root count, global tau, candidate root/floor/incidence, and identical radius-r candidate overlap data for EVERY finite r, but different legality for the same typed candidate addition.

A disconnected candidate component is permitted and, if sufficient, proves that even the full overlap connected component is not an exact response state.

## Proposed exact pair

Palette {a,b,c,d,e}, six roots, all floors1, candidate root R0={d}, candidate f=Add(R0,b).

State L:
 R0={d}
 R1={a,c}
 R2={c,e}
 R3={a}
 R4={a,c,e}
 R5={a,b}

State I:
 R0={d}
 R1={a,b,e}
 R2={a,b,e}
 R3={a,c,e}
 R4={b}
 R5={c}

In both states R0 is an isolated overlap component because d appears nowhere else. Verify both have tau=3.

After f:
- State L remains tau=3.
- State I has pair cover {b,c}, hence tau=2.

Thus candidate legality differs although the entire candidate overlap component is identical.

## Required obligations

1. Prove exact tau values before/after analytically, not by brute-force claim.
2. Prove candidate overlap components and all finite-radius data are identical.
3. State what extra global metadata is also matched: palette size5, root count6, floors, tau3, candidate syntax.
4. Conclude no function of the candidate overlap component plus those matched global scalars can determine exact legality uniformly.
5. Do NOT conclude physical nonlocality. Conclude only that raw incidence-overlap adjacency is insufficient as a derived locality notion for exact response.
6. Relate the difference to the candidate witness shadow: in I the candidate exhausts the last witness for {b,c}; in L it does not.
7. Next direction: derive locality from response dependence itself (e.g. a response/dependency graph), then test composition/coarse-graining there.

No fundamental time, geometry, metric, force, energy, numerical execution or efficiency claim.
