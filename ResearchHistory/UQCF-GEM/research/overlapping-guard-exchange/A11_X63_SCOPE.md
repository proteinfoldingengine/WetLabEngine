# A11.X63 scope — matched-floor events and transient witness intervals

Date: 2026-10-05 UTC.

Status: prospective analytical scope freeze. Analytical only; no numerical campaign, implementation, benchmark, integration merge, or numbered certification.

Accepted analytical parent: A11.X61 candidate f8b96d1fabb4cd15b87cb943a8d87f0f470a9463.
Pending analytical dependency under review: A11.X62 event-precedence candidate f35c916abfaab7ebcf57ff328fb11693562f757b. X63 must not treat X62 as accepted until its independent review lands.

## Objective

Remove two remaining restrictions of the X62 candidate:

1. X62 floor safety forces EVERY destination-only addition in a root before EVERY source-only deletion in that root. Replace this with the exact weaker resource condition: a root may spend its initial slack, and every further deletion need only be preceded by a distinct addition that replenishes one unit of capacity.

2. X62 lower protection uses common endpoint-union witnesses or old-to-new endpoint witness transfer. Permit an actual root to protect a physical pair only during an INTERMEDIATE interval after its old pair incidences are deleted and before any new pair incidence is added.

The target is one shared finite event/marker precedence graph whose acyclicity gives a direct native {3,4}, exact-destination, endpoint-Hamming-minimum repair.

## Fixed native objects

Arbitrary ORIGINAL labelled exact-four source/destination tuples E=(E_i), C=(C_i) on one finite palette. Same original positive floor f_i<=min(|E_i|,|C_i|). Native primitive toggles one incidence in one original root.

Endpoint-differing events:
- A(i,x), x in C_i minus E_i;
- D(i,x), x in E_i minus C_i.

No temporary off-endpoint incidence is allowed in the proposed minimum theorem. Every event may execute at most once.

## Already-known analytical deductions disclosed before proof freeze

### Matched floor resource

Let initial slack s_i=|E_i|-f_i. For root i, choose at most s_i source-only deletions as FREE deletions. Every other source-only deletion must be injectively matched to a distinct destination-only addition in the same root, with edge

    matched addition -> matched deletion.

For any event prefix, the number of nonfree deletions cannot exceed the number of completed matched additions, while free deletions are at most s_i. Therefore

    |current root| >= |E_i| - s_i = f_i.

This is strictly weaker than all-add-before-all-delete when both event kinds exist.

### Exact pair-witness interval

Fix a physical pair K. A root containing a common incidence in E_i intersect C_i intersect K can NEVER avoid K on an endpoint-only path.

Otherwise put
    Old_K(i)=E_i intersect K,
    New_K(i)=C_i intersect K.

The root becomes K-free after ALL deletion events D(i,x), x in Old_K(i), have occurred, and remains K-free until the FIRST addition A(i,y), y in New_K(i), occurs. Empty Old means the interval begins at the source; empty New means it extends to the destination. Both nonempty gives a genuinely transient witness interval even though neither endpoint root avoids K.

A chain of such actual intervals can protect K if adjacent intervals overlap. Proof-only pair-switch markers can require:
- all old-K deletions of the next witness before the marker;
- marker before every new-K addition of the current witness.

### Upper covers

Retain X62's proof-only upper-cover switch idea, but do not assume all-add-before-all-delete. For physical H of size<=4, an H-hit interval for root i is determined by its common H incidences and the event order of old-H deletions/new-H additions. The candidate proof must formulate sufficient exact event constraints guaranteeing each supplied H hits EVERY root throughout its active cover interval.

### X36 comparison

Accepted X36 uses incoming-before-outgoing matched capacity, not all-add-before-all-delete. Its pair protection can be carried by actual unfinished supports. X63 should determine whether the accepted X36 cycle schedule admits the new floor matching and transient-witness interval certificate. Success would show the interface captures a known multi-unfinished-root mechanism; it would NOT by itself prove every X61/X62 certificate fails on X36 endpoints.

No numerical search or enumeration is authorized.

## Required proof obligations

1. Prove the matched-floor lemma for arbitrary unequal floors, including unused initial slack and zero-addition/zero-deletion roots.
2. Prove the exact K-free interval characterization for every root and physical pair under endpoint-only events.
3. Define lower witness chains with proof-only switch markers and prove actual pair protection after EVERY native event.
4. Generalize upper-cover validity without all-add-before-all-delete. Common H incidences, gain additions, and last surviving old H incidences must be treated exactly.
5. Put floor edges, lower witness-chain edges, upper cover-chain edges, and all markers in ONE graph. Acyclicity, not separate schedules, is the sufficient compatibility condition.
6. Prove any topological order yields literal legal events, all original floors, 3<=tau<=4, finite termination, exact labelled destination, and exactly sum_i|E_i symmetric-difference C_i| primitives.
7. Show X62 embeds when all additions are ordered before all deletions and lower chains use only endpoint witnesses. If X62 is still pending, state this as a conditional comparison.
8. Check the accepted X36 cycle construction against the new certificate analytically. Distinguish 'the known X36 schedule can be represented' from 'X63 derives X36 from endpoints without using its schedule.'
9. Do not claim strict applicability beyond all X61/X62 certificates unless an exact separation is proved.

## Competing outcomes

- Strong interface: matched-floor + transient-witness + moving-cover event theorem.
- Partial interface: floor and lower interval theorem works, but upper cover compatibility needs a stronger condition.
- Representation result: theorem works and encodes X36's accepted cycle schedule, without new endpoint connectivity.
- Refutation: identify the first false event-interval or capacity claim and preserve X61/X62 boundaries.

## Boundaries

Sufficient certificate only. A directed cycle rejects the chosen certificate, not native connectivity. No arbitrary certificate existence, higher-target/directed/nested universality, physical force law, fundamental time, numerical certification, or efficiency claim.

Completed v16.54/v16.55 and all frozen evidence remain unchanged. Separate efficiency implementation remains unstarted.
