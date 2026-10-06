# A11.X63 - complete event certificate for minimum endpoint-only direct-band repair

Date: 2026-10-05 UTC.
Status: analytical candidate for fresh independent whole-argument review.
Scope: A11_X63_SCOPE.md, frozen at 2b4980c15661725f952ea6d03a3819e128e7e85f.
Accepted parent: A11.X61 candidate f8b96d1fabb4cd15b87cb943a8d87f0f470a9463.
X62 candidate f35c916abfaab7ebcf57ff328fb11693562f757b remains pending and is comparison-only.
No numerical execution, implementation, benchmark, integration merge, numbered certification or physical claim.

## 1. Native event class

Fix arbitrary ORIGINAL labelled exact-four source/destination tuples E=(E_i), C=(C_i) on finite palette P, with same original positive floor f_i<=min(|E_i|,|C_i|). Native primitives toggle one incidence.

Let W contain exactly A(i,x) for x in C_i minus E_i and D(i,x) for x in E_i minus C_i. An endpoint-only minimum path executes every W event once and nothing else, so its unavoidable length is

    d(E,C)=sum_i |E_i symmetric-difference C_i|.

Proof-only markers below change no support and are not native events.

## 2. Exact matched-floor resource

Put s_i=|E_i|-f_i. Choose at most s_i deletions in root i as FREE. Injectively match every other deletion to a distinct addition in the same root and add edge

    matched addition -> matched deletion.

At any prefix, completed deletions d are at most s_i plus completed matched additions a. Hence current size |E_i|+a-d>=f_i.

Conversely, scan ANY legal endpoint-only path. Spend a free token on a deletion while one remains; otherwise match the deletion to a distinct earlier unmatched addition. If neither exists, that deletion would make the root smaller than f_i. Thus every legal endpoint-only path induces such a forward matching.

This is exact floor accounting and is weaker than all-add-before-all-delete.

## 3. Exact transient pair-witness interval

Fix physical pair K and root i. If E_i intersect C_i intersect K is nonempty, a common K incidence never moves and i never avoids K.

Otherwise define Old_K(i)=E_i intersect K and New_K(i)=C_i intersect K. Root i avoids K exactly after ALL D(i,x), x in Old_K(i), have occurred and before ANY A(i,y), y in New_K(i), occurs.

Thus each root has one K-free interval: it may begin at source, end at destination, be genuinely transient with neither endpoint avoiding K, or be empty.

For each K supply a chain w_0,...,w_h of actual roots whose free intervals run from source to destination. Insert pair-switch markers rho_j. For handoff w_j -> w_(j+1), add

    D(w_(j+1),x) -> rho_j   for all x in Old_K(w_(j+1)),
    rho_j -> A(w_j,y)       for all y in New_K(w_j),

and order the rho markers. Then the arriving witness is already K-free before the departing witness can acquire a new K label. Shared roots/events for different pairs enter ONE graph.

## 4. Upper-cover intervals without all-add-before-delete

Supply covers H_0,...,H_q, each of size at most four, with H_0 covering E and H_q covering C. Insert ordered cover-switch markers sigma_j. H_j is active between its adjacent markers.

For root i and active H:
- if E_i intersect C_i intersect H is nonempty, that common incidence permanently hits i;
- otherwise Old_H=E_i intersect H and New_H=C_i intersect H consist only of moving incidences.

Certify H hits i throughout its active interval [alpha,beta] by one of:

OLD: choose x in Old_H and require beta -> D(i,x).
NEW: choose y in New_H and require A(i,y) -> alpha.
RELAY: choose x in Old_H,y in New_H and require
    alpha -> A(i,y) -> D(i,x) -> beta.

START/END are formal outer boundaries. OLD keeps an old hit through the interval; NEW installs a persistent new hit before it; RELAY installs the new hit before the selected old hit disappears.

Choose one valid mode for EVERY root under EVERY active cover.

## 5. Shared graph and forward theorem

G_63 has all W events, all rho markers and all sigma markers. Its edges are the matched-floor edges, lower witness-chain edges, upper mode edges, and marker-order edges.

**X63F.** If G_63 is acyclic, any topological order with markers removed from execution is a native path E->C preserving every original floor and 3<=tau<=4 after every event, restoring every exact labelled destination, and using exactly d(E,C) primitives.

Proof: Section2 gives floors and literal event legality. For each physical pair, its witness chain leaves an actual K-free root throughout, so no pair covers and tau>=3. One H_j is active at every stage and its per-root certificates make it hit all roots, so tau<=4. The finite order executes each endpoint-differing event once and no other event, hence reaches C at the global Hamming minimum.

## 6. Reverse theorem and exact characterization

**X63R.** Every existing endpoint-only minimum path preserving floors and 3<=tau<=4 induces an acyclic X63 certificate whose chronological event order, with markers inserted, is a topological order.

Floors: use the scan in Section2.

Lower witnesses: for fixed K, every state has an actual K-free root because tau>=3. Each root's K-free states form the single interval of Section3. These intervals cover the finite state line. Select a chain from a source interval to a destination interval, switching only at states where departing and arriving intervals overlap. Insert rho at each overlap. Then all arriving Old_K deletions are earlier and all departing New_K additions later, so every lower edge points forward.

Upper covers: let S_0,...,S_n be path states. At every state choose a hitting set of size<=4. Across an ADDITION, any cover of S_(j-1) still covers S_j, so switch after the addition if needed. Across a DELETION, any cover of S_j also covers S_(j-1), so switch before the deletion if needed. Therefore adjacent cover identities can always switch at a state hit by both.

For one root during one active cover interval, if no common H incidence exists, continuous H-hitting implies either an old H incidence survives to interval end (OLD), a new H incidence is already present at interval start (NEW), or some new H addition occurs before a still-present old H incidence is deleted (RELAY). Choose the corresponding events. Every upper edge points forward.

All certificate edges therefore point forward in one chronological event/marker order, so G_63 is acyclic.

Consequently, within the endpoint-only minimum class:

    minimum direct {3,4} path exists
    iff
    acyclic X63 certificate exists.

This is an exact static characterization of that path class. It does NOT assert every exact-four endpoint pair has such a path.

## 7. Relation to X61/X62 and X36

X61 batch paths are endpoint-only minimum paths, so X63R certifies them. X63F can also be read directly as a finer event interface.

Conditionally on X62 passing its own review, X62 is a special case: its stronger all-add-before-all-delete order supplies compatible floor matching; its old-to-new lower handoff is a two-witness X63 chain; its upper exceptions use OLD/NEW/RELAY modes.

Accepted X36 is a useful representation control. Its target-four cycle paths are endpoint-only minimum {3,4} paths, so X63R guarantees certificates for them. More concretely, X36's incoming-before-outgoing cycle additions provide the floor matches, and its actual missed-root invariant supplies the pair-witness interval cover. This shows X63 can represent a known multi-unfinished-root mechanism that does not rely on all-add-before-all-delete.

This is a REPRESENTATION statement, not a new proof of X36 connectivity and not a claim that X36 defeats every X61/X62 certificate.

## 8. Limits and next obligation

X63 turns minimum endpoint-only direct-band repair into finite certificate acyclicity, but it does not derive acyclicity from endpoint data. A directed cycle rejects the chosen witness/cover/matching choices, not native connectivity; another certificate or a nonminimum path may work.

The next mathematical target is therefore sharper: derive an acyclic X63 certificate from weaker endpoint invariants, or characterize a minimal unavoidable certificate cycle after optimizing witness chains, cover chains and floor matchings.

No temporary off-endpoint incidence, arbitrary certificate existence, higher-target/directed/nested universality, physical force law, fundamental time, numerical certification or efficiency claim.

Completed v16.54/v16.55 and all frozen evidence remain unchanged. Separate efficiency implementation remains unstarted.
