# A11.X61 closeout - hybrid-boundary batch handover with competing covers

Date: 2026-10-05 UTC.
Status: accepted analytical checkpoint after fresh independent whole-argument review.
Analytical parent: d5f9cf86d32456b07d5c48a38557899c9bbfc8ee.
Scope freeze: 1a6dfe1f2937fcc7eb17504b3560ab2829c562c6.
Exact reviewed candidate: f8b96d1fabb4cd15b87cb943a8d87f0f470a9463.
Candidate tree: 3c4fb4f8fdc65099dd29853f15900ea36f6eab22.
Scope blob: d5606b1b919c0fa1f7ece7b07d2405684f57a612.
Proof blob: 3d980548c292748125cb9f93ad7e26ba63537d9c.
Review: INDEPENDENT_A11_X61_WHOLE_REVIEW.md.

## Exact new theorem

For arbitrary ORIGINAL labelled exact-four source/destination root tuples, choose an ordered partition of the roots into batches. Suppose:

1. every exact hybrid boundary, with earlier batches at destination and later batches at source, has a physical hitting set of at most four labels;
2. every physical pair has either an actual root avoiding it at both endpoints, or an actual destination witness in an earlier batch than an actual source witness.

Then processing each batch by all destination additions, a cover switch, and all source-only deletions gives a direct native path with tau in {3,4}. It preserves arbitrary same original positive individual floors, supplies every next edit, terminates at every exact labelled destination support and attains the GLOBAL endpoint incidence Hamming minimum.

The theorem uses actual original root identities. Shared roots may carry several pair obligations. It does not require the colored representation, a unique endpoint cover, a common static cover, equal floors, compactness or a cover hitting both endpoints of every active root before additions.

## Why the upper and lower certificates coexist

Before a batch changes, its previous boundary cover hits every source support in the batch. Additions preserve those intersections. Once every batch root contains its destination support, the next boundary cover becomes valid; deletions retain those destination intersections.

For a difficult pair, the later source witness remains untouched throughout installation of its earlier destination witness. Once the earlier batch completes, the destination witness persists. Common union witnesses remain disjoint from their pair throughout their own edits. These witnesses operate on the same batch order as the cover sequence.

This inside-batch switch weakens X51's strict block-stable requirement while retaining literal copy/root coexistence and all individual primitive checks.

## Competing-cover control outside X60

For every m>=9, use singleton roles with cyclic physical-label rotation and declare every complement-of-four type except
K0={0,1,2,3},
M={0,2,5,7}.

The source's exact four-cover family is {K0,M}; the destination's is {pi(K0),pi(M)}. No set of at most three labels covers either endpoint. In an X60 prepared endpoint the physical four-covers form a one-representative-per-anchor Cartesian product. A two-member such product differs in one representative, whereas K0 and M differ in two positions. Thus both endpoints have competing minimum covers outside X60's colored representation.

M contains no cyclic adjacent pair and cannot be a two-label old/new footprint. The sole noncommon pair is {x_0,x_2}. Actual type v with mask{1,3,4,6} is its destination witness; actual type u with mask{0,2,4,6} is its source witness.

Use:
- B1: all copies of types with masks {0,1,4,5}, {1,2,3,4}, {1,3,4,6};
- B2: all copies with masks {m-1,0,1,2}, {1,2,5,6};
- B3: all remaining roots, including u.

Boundary covers are K0, L={0,1,4,5}, K2=pi(K0), K2. Their source/destination exception calculations prove every boundary. Since v is in B1 and u in B3, the lower transfer is safe.

Every root changes. The complete endpoint-union tuple has transversal exactly two and has no permanent three-guard. Arbitrary positive copy multiplicities and unequal saturated floors are covered. The resulting path restores the full labelled destination at the exact endpoint Hamming minimum.

## Scope and next obligation

X61 proves a reusable sufficient certificate and an infinite family outside the colored class. It does not prove every exact-four endpoint pair admits the certificate, that the displayed three covers are necessary, or that failure implies disconnection.

The next analytical target is to derive a qualifying batch partition and boundary covers from weaker endpoint invariants. The harder alternative is partial-root interleaving when lower-witness precedence and upper hybrid-cover reachability create cycles.

No numerical execution, implementation, workflow, benchmark, integration merge, numbered certification or physical claim. Completed v16.54/v16.55, frozen inherited sources and original evidence remain unchanged. Separate efficiency implementation remains unstarted.
