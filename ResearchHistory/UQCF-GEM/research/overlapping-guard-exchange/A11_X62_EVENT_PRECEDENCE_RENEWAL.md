# A11.X62 — event-level precedence certificate for lower witnesses and moving covers

Date: 2026-10-05 UTC.

Status: exact analytical candidate for fresh independent whole-argument review. Analytical only.

Frozen scope: db79b27a5eeb4555f3d13287584c64b77ed5f12a, A11_X62_SCOPE.md.

Accepted analytical parent: A11.X61 candidate f8b96d1fabb4cd15b87cb943a8d87f0f470a9463.

No numerical execution, implementation, benchmark, integration merge, numbered certification, or physical claim.

## 1. Native endpoint events

Fix arbitrary ORIGINAL labelled exact-four source and destination tuples

    E=(E_1,...,E_r),   C=(C_1,...,C_r)

on one finite palette P. Root i has the SAME original positive floor

    f_i <= min(|E_i|,|C_i|).

A native primitive toggles ONE incidence in ONE original root.

For every endpoint-differing incidence define one native event:
- A(i,x) for x in C_i minus E_i;
- D(i,x) for x in E_i minus C_i.

Let W be the finite set of all such events. A path using each event once and no other incidence has length

    d(E,C)=sum_i |E_i symmetric-difference C_i|,

the unavoidable endpoint Hamming lower bound.

For every root impose the floor edges

    A(i,x) -> D(i,y)

for ALL destination-only x and ALL source-only y in that root.

Any topological order respecting these edges adds every destination-only incidence before deleting any source-only incidence in the same root. During additions the root contains E_i; during deletions it contains C_i. It therefore never falls below min(|E_i|,|C_i|)>=f_i, and every intermediate support is contained in E_i union C_i.

## 2. Exact event-level lower witness transfer

For a physical pair K subset P, |K|=2, define actual endpoint witness sets

    O_K={i:E_i intersect K=empty},
    T_K={i:C_i intersect K=empty}.

Exact-four endpoints make both nonempty.

If O_K intersect T_K is nonempty, choose any common root w. Since both E_w and C_w avoid K, their union avoids K, so w remains an actual witness through every endpoint-contained intermediate support. No lower precedence edge is needed.

Otherwise choose one ACTUAL old witness u_K in O_K and one ACTUAL new witness v_K in T_K. They are distinct.

Because u_K is not in T_K, C_u intersects K while E_u avoids K. Hence the nonempty set

    Lose_K(u)={A(u,x): x in K intersect C_u}

contains exactly the endpoint additions whose occurrence can destroy u's old witness status.

Because v_K is not in O_K, E_v intersects K while C_v avoids K. Hence the nonempty set

    Gain_K(v)={D(v,x): x in K intersect E_v}

contains exactly all K incidences that must be deleted before v becomes a new witness.

Add precedence edges

    d -> a

for EVERY d in Gain_K(v_K) and EVERY a in Lose_K(u_K).

Then until all Gain_K(v) events have occurred, no Lose_K(u) event can occur, so old u still avoids K. After all Gain events have occurred, v contains no K label and remains a witness forever because C_v avoids K and no destination addition in v belongs to K.

Thus this edge family transfers actual lower protection at event resolution; it does NOT require the whole destination root v to finish before the whole source root u starts.

Choose such actual u_K,v_K independently for each noncommon pair only as NAMES of roots; all resulting edges live in ONE shared graph. If the combined graph cycles, the certificate fails rather than allocating fictitious independent capacity.

## 3. Event-level upper cover intervals

Supply a finite ordered list of physical sets

    H_0,H_1,...,H_q,    |H_j|<=4,

with H_0 hitting every source root and H_q hitting every destination root.

For any H define actual source/destination exception sets

    U_H={i:E_i intersect H=empty},
    V_H={i:C_i intersect H=empty}.

Require

    U_H intersect V_H = empty

for every supplied H. If a root misses H at both endpoints, its endpoint union misses H, so no endpoint-only minimum path can make H hit that root; excluding such a cover is necessary for this certificate.

### Source-exception gains

For each i in U_H, C_i must meet H because i is not in V_H. Choose one actual event

    g(i,H)=A(i,x),  x in H intersect C_i.

It exists because E_i misses H, so every destination H incidence is destination-only. Once g occurs, that H label persists to C_i and root i is H-hit thereafter.

### Destination-exception last losses

For each i in V_H, E_i meets H and C_i misses H. Every H incidence of E_i is therefore old-only. Choose one event

    l(i,H)=D(i,y),  y in H intersect E_i,

and add edges

    D(i,z) -> l(i,H)

for every other z in H intersect E_i.

Consequently l(i,H) is the LAST H-labelled deletion in root i. Root i remains H-hit until l occurs; afterward it may cease to be H-hit.

Roots outside U_H union V_H are H-hit at both endpoints. If they share an endpoint-common H incidence it never moves. Otherwise at least one destination H addition occurs before every source deletion by the floor edges, so such a root remains H-hit throughout.

## 4. Zero-cost cover-switch markers

Introduce proof-only markers

    sigma_0,...,sigma_(q-1).

They are NOT native primitives, do not alter any incidence, do not contribute to path length, and disappear when the final native event sequence is read out. They only specify which supplied H_j certifies the upper bound between native events.

Add marker-order edges

    sigma_j -> sigma_(j+1).

For each transition H_j -> H_(j+1), require the next cover to be installed before the switch:

    g(i,H_(j+1)) -> sigma_j

for every i in U_(H_(j+1)).

Require the current cover not to lose any destination-exception root before the switch:

    sigma_j -> l(i,H_j)

for every i in V_(H_j).

For an intermediate cover H_j, 1<=j<=q-1, these two adjacent conditions say:
- all its source-exception gains occur before sigma_(j-1);
- all its destination-exception last losses occur after sigma_j.

Therefore H_j hits EVERY root throughout the entire interval after sigma_(j-1) and through sigma_j.

H_0 is a source cover, so U_(H_0)=empty and it is valid from the initial state until sigma_0. H_q is a destination cover, so V_(H_q)=empty and after all its gains occur before sigma_(q-1), it remains valid to the destination.

For q=0, H_0 covers both endpoints. U=V=empty; endpoint containment and Add-before-Del make it a cover throughout, and no marker is needed.

## 5. The shared event graph and theorem

Construct ONE finite directed graph G_event whose vertices are:
- every native endpoint-differing incidence event in W;
- the proof-only cover-switch markers sigma_j.

Its edges are exactly:
1. every within-root Add-before-Del floor edge from Section1;
2. every lower witness transfer edge from Section2;
3. every last-H-deletion edge from Section3;
4. every cover gain/switch/loss and marker-order edge from Section4.

**X62E — event-precedence repair theorem.**
If there exist actual lower-witness choices, a supplied cover chain H_0,...,H_q, designated gain/loss events, and the resulting G_event is ACYCLIC, then E connects to C by a finite native path satisfying

    3 <= tau <= 4

after every incidence primitive. The path preserves every original floor, restores the FULL exact labelled destination, and has exactly d(E,C) primitives, hence globally minimum incidence count.

### Proof

Take the lexicographically least topological order of G_event. Delete the sigma markers from the executed sequence; they change no state.

Floor safety and literal event legality follow from Section1. Every native event is endpoint-differing, appears once, and its incidence has not previously been toggled. Finite event count gives termination at C.

For tau>=3, fix any physical pair K. A common union witness remains actual throughout. Otherwise Section2's edges ensure old u_K persists until all K labels have been deleted from v_K; then v_K persists. Hence every pair misses an actual root after every native event. Since the exact-four endpoints require at least four palette labels, any hitting set of size zero or one could extend to a two-label hitting set. Therefore tau>=3.

For tau<=4, before sigma_0 use H_0. Between sigma_(j-1) and sigma_j use H_j. After sigma_(q-1) use H_q. Section3 proves roots with neither exception remain hit throughout. The marker edges ensure every source exception has gained a persistent H_j label before H_j becomes active and every destination exception retains its designated last H_j label until after H_j is retired. Thus the active H_j hits every root after every native event in its interval. Since |H_j|<=4, tau<=4.

Every event in W executes once and no other incidence changes. Therefore the length is exactly d(E,C), which every native path must meet or exceed.

No random execution, simultaneous incidence move, fictitious owner edit, or temporary off-endpoint incidence is used.

## 6. X61 embeds as a special event certificate

Take any accepted X61 batch certificate B_1,...,B_q with hybrid-boundary covers H_0,...,H_q and actual lower witness choices where each difficult pair's destination witness lies in an earlier batch than its source witness.

Use the literal X61 schedule: within each batch perform all destination additions, then the boundary cover switch, then all source-only deletions.

Place sigma_j at X61's proof switch after additions of batch B_(j+1) and before its deletions.

For cover H_(j+1), every source-exception root must lie in one of the already processed batches through B_(j+1); otherwise the next hybrid boundary would not be covered. Its chosen H gain therefore occurs before sigma_j. For H_j, every destination-exception root lies in B_(j+1) or a later batch; choose its last H deletion in its actual batch, after sigma_j.

For a difficult pair, all events making the earlier destination witness avoid K occur in its earlier batch before any event that can destroy the later source witness. Hence all Section2 lower edges respect the X61 schedule.

Choose each designated last-H deletion to be the last such deletion in that root under the X61 fixed palette order. Every graph edge then points forward in the displayed X61 event/marker sequence. Thus G_event is acyclic.

Therefore X61B is contained in X62E. X62 changes the resolution of the certificate; it does not invalidate or rewrite X61.

## 7. Why event resolution can remove a root-level precedence cycle

The following is a certificate-level schematic, NOT yet claimed as a new exact-four structural family.

Suppose a source cover H0 and destination cover H1 have:
- a root u that is a source exception to H1, so an H1 gain addition in u must occur before the cover switch;
- a root v that is a destination exception to H0, so an H0 last-loss deletion in v must occur after the switch;
- a difficult lower pair K for which u is the chosen old witness and v the chosen new witness.

A whole-root abstraction can demand u before v for the upper handover while demanding v before u for the lower handover.

At event resolution these requirements need not conflict if the relevant labels are distinct. One legal precedence pattern is

    H1-gain addition in u
       -> sigma
       -> K-removing deletion in v
       -> K-destroying addition in u,

with the H0 last-loss deletion in v placed after sigma and all root Add-before-Del constraints also respected. The roots can be simultaneously unfinished.

This demonstrates the mechanism X62E is designed to certify, but it is NOT a strict separation theorem from every possible X61 batch certificate. Deriving an actual exact-four endpoint family whose available X61 certificates all fail while X62E succeeds remains open.

## 8. Limits and next obligation

X62E is a sufficient actual-event certificate. It does NOT prove every exact-four endpoint pair admits suitable witness choices, cover chain, gain/loss designations, or an acyclic graph.

A directed cycle rejects the chosen event certificate only. It is not native disconnection and does not exclude different witnesses, covers, temporary nonminimum incidences, or another repair mechanism.

The new theorem is strictly finer in descriptive resolution than X61, and X61 embeds, but a proved endpoint family outside ALL X61 batch certificates is not yet supplied. Therefore no strict connectivity or applicability separation is claimed.

The next analytical target is one of:
1. derive acyclicity or a valid event certificate from weaker endpoint invariants;
2. derive an exact-four structural family where a declared root-level certificate cycles but X62 event interleaving succeeds, with the separation scoped exactly to that certificate;
3. identify a minimal event-cycle obstruction and determine whether another witness/cover choice resolves it.

No arbitrary accessibility, higher-target/directed/nested universality, physical force law, fundamental time, numerical execution, implementation certification, or efficiency result.

Completed v16.54/v16.55, frozen inherited analytical sources and original evidence remain unchanged. Separate efficiency implementation remains unstarted.
