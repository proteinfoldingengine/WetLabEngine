# Automatic retained lower-witness handoff theorem

Date: 2026-10-06 (America/Phoenix).
Status: ANALYTICAL RESULT CANDIDATE WITH COMPLETE ARGUMENT.
Scope freeze: AUTO_LOWER_WITNESS_SCOPE.md at 5f9a109c68c9784b2a04c80e82a2ad3450a8c77a.
Evidence: written mathematics only.

## 1. Endpoint domain

Fix finite palette P and labelled source/target supports E=(E_i), C=(C_i) with
    tau(E)>=3,
    tau(C)>=3.

Native endpoint events are
    A(i,x), x in C_i minus E_i,
    D(i,x), x in E_i minus C_i.

Common incidences do not move.

For each physical pair K subset P, |K|=2, source protection gives at least one root missing K and target protection gives at least one root missing K.

Retained endpoint signatures choose deterministically:
    o_K: an old witness with E_o intersect K empty;
    n_K: a new witness with C_n intersect K empty.

If some root w satisfies
    (E_w union C_w) intersect K empty,
choose it as a permanent witness and no K marker is needed.

Otherwise introduce proof-only marker rho_K.

## 2. Automatically prepare the new witness

Because C_n intersect K is empty, every K-incidence present in E_n is absent from C_n and is therefore source-only.

For every
    x in E_n intersect K
derive
    D(n_K,x) -> rho_K.

When rho_K becomes eligible, all K-incidences that the selected new witness had at source have been deleted.

There can be no destination-only K addition in n_K because C_n misses K.

Therefore at rho_K:
    current n_K intersect K = empty.

The selected new witness is actual.

## 3. Automatically hold the old witness

Because E_o intersect K is empty, every K-incidence present in C_o is absent from E_o and is therefore destination-only.

For every
    y in C_o intersect K
derive
    rho_K -> A(o_K,y).

Before rho_K fires, none of those target K-incidences may have been added.

Since o_K began with no K-incidence, throughout every state before rho_K:
    current o_K intersect K = empty.

Thus the old actual witness persists until handoff.

## 4. New witness persists after handoff

After rho_K, n_K misses K.

Its target C_n also misses K. Therefore no endpoint addition belonging to K can ever enter n_K after handoff.

Further endpoint deletions can only preserve the property of missing K.

Hence n_K remains an actual K-witness through the exact destination.

## 5. Pair protection theorem

For every physical pair K:

- if a permanent witness was selected, that root misses K throughout;
- otherwise o_K misses K before rho_K;
- n_K misses K at and after rho_K.

Therefore after every native event state there exists at least one actual root missing K.

No two-label set can hit every root.

Consequently
    tau>=3
throughout every execution respecting the automatically derived lower-witness edges.

This is exact actual-root protection, not a numerical surrogate.

## 6. Lower-only graph is acyclic

Take the union of the derived edges over every physical pair K.

Vertices are:
- native deletion events;
- pair markers rho_K;
- native addition events.

Every edge has one of two forms:
    deletion -> rho_K,
    rho_K -> addition.

Assign levels
    deletions: 0,
    pair markers: 1,
    additions: 2.

Every edge strictly increases level.

Therefore the entire automatically derived LOWER-WITNESS graph is acyclic, even when the same native event participates in many pair obligations.

Permanent-witness pairs add no edges.

This acyclicity is lower-channel-only. Floor or upper-cover edges may point in the opposite direction and can create cycles when combined.

## 7. Endpoint completion and separate floor requirement

The lower theorem does not by itself certify that every deletion is floor-legal.

If a separate floor certificate supplies an execution of all endpoint events consistent with the lower graph, then each endpoint-differing incidence executes once and the exact target C is reached.

Every such execution preserves tau>=3 by Sections2-5.

Thus the theorem cleanly separates:
    lower witness protection
from
    root-capacity/floor scheduling.

## 8. Fiber-uniform retained interpretation

Suppose multiple hidden full states share the retained endpoint signatures used to select o_K,n_K and to identify their K-relevant endpoint events.

Then the derived lower graph is identical across that fiber.

The proof of witness persistence uses only those retained signatures:
- old selected root starts K-free;
- new selected root ends K-free;
- all relevant K deletions/additions are represented by graph edges.

Therefore lower legality is fiber-uniform over the declared retained quotient. Hidden invariant incidences outside K need not be reconstructed.

## 9. Symbolic controls

### Permanent witness

For K={a,b}, let one root have
    E_w=C_w={c}.

Then (E_w union C_w) intersect K is empty. No K marker or edge is needed.

### One-deletion handoff

Let
    o: {c}->{a,c},
    n: {a,d}->{d},
with K={a,b}.

o is an old witness and n a new witness.

The rule derives
    D(n,a) -> rho_K -> A(o,a).

Before rho_K, o misses K. After D(n,a), n misses K. Only then may o acquire a.

### Two-deletion preparation

Let
    n: {a,b,d}->{d},
again K={a,b}.

The rule derives
    D(n,a) -> rho_K,
    D(n,b) -> rho_K.

Both old K-incidences must disappear before n becomes an actual witness.

### Old witness with two destructive gains

Let
    o: {d}->{a,b,d}.

Then
    rho_K -> A(o,a),
    rho_K -> A(o,b).

Neither K addition may destroy the old witness before the new witness is established.

These controls show that the rule handles multiplicity rather than assuming one event per witness.

## 10. Duality with the automatic upper theorem

The closed upper-cover theorem derives

    addition -> upper handoff -> deletion

to install replacement H1 protection before consuming H0.

The present lower-witness theorem derives

    deletion -> pair handoff -> addition

to establish a replacement missed-root witness before destroying the old one.

The directions are exact duals:

    upper protection wants gains before losses;
    lower protection wants witness-creating losses before witness-destroying gains.

That opposition is mathematically important.

## 11. Next frontier: joint automatic event synthesis

Now combine in ONE graph:
- upper-cover gain/hold edges;
- lower pair-witness edges for every K;
- a floor certificate.

Neither channel alone cycles under the simple level proofs above. Their union can.

The next theorem must not assume compatibility. It should:
1. define the combined retained event graph;
2. prove acyclicity is sufficient for exact 3<=tau<=4 completion;
3. derive a useful structural acyclicity condition if possible;
4. otherwise exhibit a protected-endpoint instance whose selected automatic upper/lower/floor certificates create a directed event cycle;
5. distinguish failure of that selected certificate from native disconnection.

No physical force, geometry, energy, observer field or fundamental time is inferred.
