# A11.X62 scope — event-level witness/cover handover beyond batch ordering

Date: 2026-10-05 UTC.

Status: prospective analytical scope freeze. Analytical only; no numerical campaign, implementation, benchmark, integration merge, or numbered certification.

Accepted analytical parent: A11.X61 candidate f8b96d1fabb4cd15b87cb943a8d87f0f470a9463, independently accepted in INDEPENDENT_A11_X61_WHOLE_REVIEW.md.

## Objective

Generalize X61 from ordered ROOT BATCHES to a sufficient certificate on the actual endpoint-differing INCIDENCE EVENTS themselves.

The target case is a cyclic root-level obligation: lower protection may require one root to become a destination witness before another root changes, while upper-cover reachability may require the opposite root-level order. A valid native path can still exist if the required additions and deletions interleave inside those roots.

Prove a direct native {3,4} endpoint-Hamming-minimum theorem whenever a finite event-precedence graph, derived from actual old/new pair witnesses and a finite chain of physical upper covers, is acyclic.

## Fixed native objects

Start with arbitrary ORIGINAL labelled exact-four source/destination tuples E=(E_i), C=(C_i) on one finite palette. Root i has the SAME original positive floor f_i<=min(|E_i|,|C_i|). A native primitive toggles one incidence in one original root. No extra labels, roots, floor weakening, simultaneous primitives, relabeling, compactness or imposed geometry.

For each root i define endpoint-differing events:
- Add(i,x), x in C_i minus E_i;
- Del(i,x), x in E_i minus C_i.

A minimum-incidence path may use each such event once and no other incidence event.

## Already-known analytical leads disclosed before proof freeze

1. Floor-safe endpoint containment can be enforced by putting every Add(i,*) before every Del(i,*). Then the active root contains its source throughout additions and its destination throughout deletions.

2. For a physical pair K:
   - a common witness i with E_i and C_i both avoiding K remains a witness throughout any endpoint-contained edit of i;
   - a source-only witness u stops being guaranteed precisely when a K-labelled destination addition occurs;
   - a destination-only witness v becomes guaranteed once all K-labelled source-only deletions in v have occurred.
   Thus choosing actual v,u and requiring EVERY K-deletion of v before EVERY K-addition of u should transfer lower protection without requiring v's whole root to finish before u's whole root starts.

3. For a physical upper set H of at most four labels:
   - a source-exception root can become H-hit when one endpoint-required H-addition occurs;
   - a destination-exception root remains H-hit until its last old-only H label is deleted.
   Designating an actual gain event g(i,H) for every source exception and a last-loss event l(i,H) for every destination exception suggests an event-level cover interval.

4. For a cover chain H_0,...,H_q with H_0 covering the source and H_q covering the destination, requiring every gain for H_(j+1) before every last-loss for H_j should make adjacent cover-valid intervals overlap. This is the event-level analogue of X51/X61 and permits a switch inside an active root at its enlarged endpoint union.

5. The resulting precedence graph should include:
   - all Add-before-Del floor edges within each root;
   - edges making each designated l(i,H) the last H-deletion in that root;
   - adjacent-cover gain-before-loss edges;
   - lower-witness all-required-deletions-before-any-witness-destroying-addition edges.
   If this graph is acyclic, a deterministic topological order should supply the native path.

These are unreviewed deductions to prove or refute. No finite computation is authorized or offered as evidence.

## Required theorem obligations

1. Define source/destination/common witness sets for EVERY physical pair and prove the exact event at which a chosen old witness can be lost and a chosen new witness becomes valid.
2. Define upper-cover source/destination exceptions and prove an exact interval criterion for H under endpoint-only events.
3. Handle multiple H labels in one root correctly: a destination exception loses H only after its LAST old H incidence is deleted; a source exception needs only ONE persistent destination H addition.
4. State all designated event choices explicitly. Acyclicity must be checked on ONE shared graph; do not allocate the same event independently to incompatible obligations.
5. Prove any topological order preserves tau>=3 and tau<=4 after EVERY individual event.
6. Prove original-floor legality, literal event availability, finite termination, exact labelled destination restoration and global endpoint Hamming minimum.
7. Show X61 batch certificates embed as a special event-level case.
8. Supply a structural control where a natural/root-level lower-versus-upper precedence cycle blocks the corresponding batch certificate but an acyclic event-level certificate succeeds. Scope any separation to the declared certificate; do not infer native disconnection from a failed batch order.
9. If no clean separation family is derived, retain the general event theorem but state that strict extension beyond X61 is not yet demonstrated.

## Competing outcomes

- Strong positive: event-level acyclicity theorem plus a strict family beyond X61 batch ordering.
- Interface positive: correct event theorem, no proved strict separation family yet.
- Partial positive: lower or upper event interval works but joint graph needs additional compatibility.
- Refutation: identify the first false lead and preserve X61 as the current frontier.

## Boundaries

This is a sufficient certificate, not a claim every exact-four endpoint pair admits one. Failure or a graph cycle is a method limitation unless native disconnection is independently proved.

No higher-target, unrestricted directed/nested universality, physical force law, fundamental time, numerical certification or efficiency claim.

Completed v16.54/v16.55 and all frozen evidence remain unchanged. Separate efficiency implementation remains unstarted.
