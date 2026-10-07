# C2 author-side whole-argument audit and rejecting controls

Date: 2026-10-07.
Status: C2 AUTHOR-SIDE AUDIT PASSED / INDEPENDENT REVIEW PENDING.

Frozen scope: c00318259d31c92e2dd0bd7a3ce97755bf74ea02.
Proof candidate: 5d4e7548c03c7c13b04f25f5a39cb723a684ceb6.

## Checks

- Source and target each have forced singleton labels a,b,c and r4 intersects their three-cover, so tau=3.
- The exhibited eight-edit M1,M2,M4 schedule respects every original floor and every state has exact tau=3.
- M2-first fails immediately: {a,c} is a two-cover.
- M4-first is individually safe but its completion removes r4's {b,c}-miss witness. Then M1-first gives two-cover {b,c} and M2-first gives two-cover {a,c}.
- r4 is not passive padding: it changes source-to-target and directly changes which first moves are legal.
- The auxiliary w is unused; the result does NOT demonstrate necessity of a temporary buffer.
- The carrier does NOT establish an endpoint-event cycle or a unique global ordering. Partial M4 interleaving may change the policy picture.

## Rejecting false inferences

1. A passive fourth root with overlap is not automatically coupled: the C1 padded-swap example is explicitly rejected as C2 evidence.
2. An order-dependent failure of a chosen macro does not imply native disconnection: the complete eight-edit endpoint-only path is a counterexample.
3. An auxiliary-free path means this particular carrier cannot prove auxiliary necessity.
4. All lower-bound statements rely on actual missed roots/two-cover checks, not heuristics or assumed geometry.

## Disposition

C2 is a valid author-side bounded analytical candidate. It requires fresh independent mathematical review and publication reconciliation before acceptance. C3-C6 remain open.
