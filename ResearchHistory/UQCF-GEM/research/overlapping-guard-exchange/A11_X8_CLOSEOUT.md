# A11.X8 closeout — one-overlap incidence repair

Status: **COMPLETE / independently ACCEPTED analytical theorem within its stated class.**
Reviewer: independent Codex agent `/root/a11_x6_review`; no mathematical corrections requested.
No numerical campaign, execution job, implementation certification or new numbered version.

## Exact new statement

On a fixed finite ordered palette of k labels and r labelled roots with uniform original floor h, let exact-q endpoints be feasible, q>=3. Set N=floor(r*(k-h)/k). If r>=2N-1, every endpoint pair admits finite native one-incidence repair with transversal in {q-1,q}, restoring the original labelled destination and every noncompact incidence.

For a particular pair, exact uniform compaction with selected maximum incidence degrees d_A+d_C>=r-1 also suffices.

In particular, all seven-label, original-floor-three, exact-four endpoint pairs are connected at r=13,15,17. This is additional coverage beyond X7's disjoint incidence-guard criterion. It requires neither X5 qualification nor a cyclic endpoint description.

## Removed assumption and renewed progress

X7 required room for disjoint source and destination protecting families. X8 removes one required disjoint slot by composing X7G's actual incidence-derived guards with the already accepted O1 one-shared-slot handover. This known composition was disclosed before candidate development; no new universal multiple-overlap handover is claimed.

Accepted native exact-endpoint root permutation places the destination guard with at most one shared index. Uniform original floors justify that placement; mixed-floor permutations are not asserted. A small hitting set meeting all exclusive guards must miss both old and new shared supports, and thus their union. Every intermediate shared support lies in that union, retaining an actual witness against every forbidden small cover. At target four this covers every pair of palette labels.

Prepare destination-exclusive roots under the source guard; transfer the shared root under the comparison guard; complete remaining roots under the installed destination guard. Larger supports and temporary incidences are native. Each middle edit decreases total symmetric difference by one, and each unfinished phase supplies an eligible next primitive. The destination protection is reusable for the entire remaining repair; no return to exact q is required at each handover.

## Complete endpoint restoration and upper bound

The supplied preliminary middle path maintains transversal at least q-1; it can rise above q. Its support-floor upper bound is k-h+1, equal to five for the primary carrier. Accepted maximum-layer Theorem A converts that actual finite path to {q-1,q}. This conversion is explicitly distinguished from the preliminary path.

Exact source compaction, converted middle repair, reversed accepted endpoint permutation and reversed destination compaction concatenate at exact q. The result reaches the original labelled destination including all originally larger supports.

## Scope and remaining obligations

The universal theorem assumes uniform original floors, exact feasible endpoints, q>=3 and r>=2N-1. The pair-sensitive alternative assumes the stated compact maximum-degree sum. It does not characterize necessity.

At seven labels, floor three, target four, the remaining universal carrier obligations are confined to r=14,16,18 before accepted subclass and degree exclusions. Existing accepted O1 closes all r>=19; X7's r=12 closure remains valid. Failure of the incidence inequality is inconclusive and is not a no-path certificate. Multiple shared slots need further structural protection; independent missed-index sets need not intersect.

Original A11 destination-directed scheduling, remaining native carriers, and unrestricted nested universality remain OPEN. Earlier failed constructions and their correct method-limit classifications are preserved.

## Frozen and reviewed sources

Repository: proteinfoldingengine/WetLabEngine.
Analytical branch: research/uqcf-overlapping-guard-exchange.

- Parent publication: 7b475d5c904fb5bbba1888b9944be98ee1ad74b1.
- Scope commit: 8010f4e04b616d89cc2227cd53f7960a502d5af6.
- Exact reviewed candidate: 6c5b2159080486b83fd005d42e0bbd719561f9f2.
- Proof: A11_X8_ONE_OVERLAP_INCIDENCE_REPAIR.md; 12645 UTF-8 bytes; SHA-256 ee966487ab7b5de20574af2af127e3a7e1caf40040e8f0c4f732db3e8edb50ed; Git blob 5fd714a1e170c06490cbcc49f75a846bc8acf66f.
- Scope: 2624 UTF-8 bytes; SHA-256 c219cc9ff7fe39f7c05443768bea03ade35feaa61f122e61a4074a1d3080eaae; Git blob db4c8d154b3f7fb8e92dd87a3f5c68afe91386d5.
- Review: INDEPENDENT_A11_X8_REVIEW.md, attributable exact-source ACCEPT receipt.

Dependencies are X7G, frozen O1, baseline Lemma M and baseline Theorem A. Their hypothesis domains were checked; frozen sources were not rewritten or recertified. Certified integration remains 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.

## Publication completion gate

Publication must append the review and closeout, update STATUS.json, KNOWN_RESULTS.md, NEXT_OBLIGATION.md, A11_PROGRESS.md, README.md and PHASE_TRACKER.md, preserving the reviewed scope/proof blobs exactly. Completion is reported only after reading all ten packet files from the final immutable publication and checking exact content, the expected eight-file publication delta, absence of divergence, analytical head, and unchanged certified integration head. The immutable publication SHA is reported after that audit rather than embedded self-referentially here.
