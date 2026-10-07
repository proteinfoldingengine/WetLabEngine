# Concrete three-payload precedence realization scope

Date: 2026-10-06 (America/Phoenix).
Status: PROSPECTIVE ANALYTICAL SCOPE.

Parent interface closeout:
- PRECEDENCE_INTERFACE_CLOSEOUT.md at e81c236b707d2ed1c5e07ebe806858bac83f1f25.

## Objective

Realize a nontrivial three-vertex retained precedence graph directly from native target-four certificate data.

## Carrier

Core labels a,b,c,d,e and spectator set T, |T|=s>=1.

Controlled roots:
    {d}, {e}, {a,b,c}.

Residual environment:
    h={b}, invariant.

Three labelled payloads p,q,r start with core a.
Allow arbitrary invariant spectator sets Z_p,Z_q subseteq T on p and q only:
    p={a} union Z_p,
    q={a} union Z_q,
    r={a}.
The second b-target payload r is deliberately spectator-free so the wrong-order obstruction is uniform over the hidden fiber.
All floors1.

Exact core targets:
    p->b,
    q->c,
    r->b.
Each target preserves its own Z exactly.

Payload macro a->x is Add x then Delete a.

Retain:
- labelled target address D;
- core-projected miss counts M_core(H) for nonempty core H of size<=4;
- completed/phase bookkeeping.

## Required derived graph

From retained data derive unfinished b-target payloads B and c-target payloads C.

In this selected carrier h={b}. Define one edge
    u -> v
for every unfinished u in B and unfinished v in C.

Initially:
    p -> q,
    r -> q.

Prove this graph is derived from retained environment certificate plus D, not hidden spectators.

## Required legality theorem

1. Any indegree-zero b-target payload may be repaired first; every primitive stays at tau4.
2. After one b-target completes, graph renews to the induced graph with the other b-target still preceding q.
3. If q is repaired while ANY b-target payload remains unfinished at core a, q's addition is safe at tau4 but its deletion gives tau5.
4. After both b-target payloads complete, q is safe and target tau4.
5. Exact completion occurs in three macros=six incidence edits for either topological order p,r,q or r,p,q.

Prove uniformly over all allowed hidden (Z_p,Z_q) assignments. Explain why allowing arbitrary spectators also on r would invalidate the uniform rejecting control.

## Hidden multiplicity

For fixed retained core/address data there are 2^(2s) spectator assignments (Z_p,Z_q) with the same retained graph and macro order choices. They remain hidden and are preserved exactly.

## Policy obstruction

The premature q macro is an exact rejecting control for violating a retained precedence edge. It is not a native-disconnection result.

A genuine directed-cycle realization remains a separate next question if this fork theorem succeeds.
