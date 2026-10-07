# Automatic retained lower-witness handoff scope

Date: 2026-10-06 (America/Phoenix).
Status: PROSPECTIVE ANALYTICAL SCOPE.

Parent automatic upper-cover closeout:
- AUTO_COVER_HANDOFF_CLOSEOUT.md at e13f829e5bef68d8558d355300ec07b18f53d8b6.

## Objective

Derive lower protection tau>=3 automatically from retained endpoint signatures.

For every physical pair K, retain enough endpoint information to identify source roots missing K and target roots missing K. Select old/new actual witnesses deterministically and derive deletion-before-handoff-before-addition edges that guarantee witness overlap.

This theorem is lower-only. Floor safety and tau<=4 are separate certificates until the joint synthesis.

## Endpoint domain

Fix source E and target C on finite palette P with
    tau(E)>=3 and tau(C)>=3.

Native events are endpoint-only additions A(i,x), x in C_i minus E_i, and deletions D(i,x), x in E_i minus C_i.

For every physical pair K choose deterministically:
- old witness o_K with E_o intersect K empty;
- new witness n_K with C_n intersect K empty.

If some root w has
    (E_w union C_w) intersect K empty,
choose it as a permanent witness and derive no K-handoff edges.

Otherwise introduce proof-only marker rho_K.

## Automatic new-witness preparation

Since C_n misses K, every source K-incidence in n_K is source-only.

For every
    x in E_n intersect K
derive
    D(n_K,x) -> rho_K.

Thus rho_K cannot fire until the selected new witness has lost every old K-incidence and actually misses K.

## Automatic old-witness hold

Since E_o misses K, every target K-incidence in o_K is destination-only.

For every
    y in C_o intersect K
derive
    rho_K -> A(o_K,y).

Thus the selected old witness remains K-free until after rho_K.

## Required theorem

1. Before rho_K, old witness o_K misses K.
2. At rho_K, new witness n_K misses K.
3. After rho_K, new witness remains a K-witness because C_n misses K.
4. Therefore every pair K has an actual missed root at every event state, so tau>=3.
5. The lower-only event graph is acyclic by levels deletion -> pair marker -> addition, provided no extra opposite-direction edges are added.
6. Permanent witnesses require no marker.
7. Exhausting endpoint events reaches C if a separate floor/event execution certificate exists.
8. Hidden-fiber uniformity requires the selected endpoint witness signatures to be retained and identical across the fiber.

## Concrete controls

Give exact symbolic examples of:
- permanent witness;
- old witness destroyed by an addition only after handoff;
- new witness established by one deletion;
- new witness requiring two K-deletions before handoff.

## Joint frontier

After closing the lower-only theorem, combine:
- automatic upper-cover edges: addition -> upper handoff -> deletion;
- automatic lower-witness edges: deletion -> pair handoff -> addition;
- floor edges.

The opposing directions can create a genuine event-level directed cycle. Do not assume compatibility.

The next result must either derive an acyclicity condition for the combined graph or exhibit an exact protected-endpoint counterexample where the automatically generated joint certificate graph cycles.

No physical force, geometry, energy, observer field or fundamental time.
