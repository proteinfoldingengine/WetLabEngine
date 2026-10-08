# C3 partial-seed Revised2: reporting clarification after mathematical acceptance

Date: 2026-10-08.
Status: MATHEMATICAL REVIEW ACCEPTED; separate publication audit and final publication/index closeout PENDING.

This companion makes the accepted model's target and disjointness assumptions literal. It does not modify or replace the frozen scope or second-corrected proof. The independent review classified these as reporting/formal-assumption clarity notes under the declared model, not material mathematical defects. This classification is preserved, not upgraded into an unconditional result.

## Immutable sources and exact review provenance

- Frozen scope: `COUPLED_C3_PARTIAL_SEED_SCOPE.md` at `542782cd198b65e9bfd79dd88193251666e74637`.
- Accepted proof: `COUPLED_C3_PARTIAL_SEED_REVISED2.md` at `d9f1e77fcbb9fdeb4bbcbe3237fb27e8ce2fc36a`.
- Completed mathematical review job: `01a11bd1-8688-731d-887d-3414d4b142ef`.
- Review thread: `01a11bd1-86b7-76fd-a0a7-45eea036d82b`; turn 1.
- Service/model: Firecrawl / `spark-2`; separate AI research-agent review, not human peer review or a machine-checked proof.
- Exact verdict: `ACCEPTED`. The returned `mathematical_defects` array is empty.
- Full structured response and archive metadata: [COUPLED_C3_PARTIAL_SEED_REVISED2_ACCEPTED_REVIEW.json](https://github.com/proteinfoldingengine/WetLabEngine/blob/a63e31a7dea1e266650c061f7c1a3d49415a8cb6/ResearchHistory/UQCF-GEM/research/physical-bridge/COUPLED_C3_PARTIAL_SEED_REVISED2_ACCEPTED_REVIEW.json).

The earlier job `01a119b9-ddfd-758e-95d4-494f373967b0` used invalid proof ref `19cba75e3f7cfb87c12322fd4b38e7b57b7b7317` and returned procedural REVISE. That is not acceptance, is not a mathematical rejection of the accessible Revised2 source, and is not the job archived above. Earlier mathematical revisions are not erased.

## Literal carrier and palette assumptions

The labels `a,b,c,d,e` are pairwise distinct. The finite spectator palette `T` satisfies

    T intersect {a,b,c,d,e} = empty.

The fresh buffer `w` is distinct from every core and spectator label:

    w not in ({a,b,c,d,e} union T).

The permitted repair incidence palette is `{a,b,c,d,e,w} union T`. Root slots `r1,r2,r3,r4` are labelled. The prepared starting carrier for the repair, after the observed ledger, is

    E(Z) = ({a,b}, {b,c}, {a,c}, {d,e} union Z),  Z subseteq T.

The EXACT labelled destination is

    F(Z) = ({b,d}, {b,c}, {c,d}, {a,e} union Z).

All spectator incidences must return to their original repair-start positions; `w` must be absent at the destination. There are exactly six endpoint-differing incidences. Each repair edit toggles one incidence while every root has size at least 2 and the hitting number satisfies `3 <= tau <= 4`.

Disjointness is a substantive hypothesis of this declared model. No assertion is made for palettes overlapping the core. This companion does not derive finite palette size, buffer availability, or root addressability from first principles.

## What the accepted result says

For the assumed complete valid ordered spectator sign ledger on `r4`, with known `N=|T|` and unknown initial seed, the feasible initial cardinalities form the exact interval in Revised2. Its shifted interval gives all possible current counts. Inconsistent ledgers are rejected, not assigned a zero-capacity bit.

For this carrier and exact target the shortest protected repair has six edits for nonempty `Z` and eight for empty `Z`. When the observation is compatible with both, there is no deterministic sign-ledger-only first edit that begins a shortest repair in every compatible world. The declared fresh-`w` eight-edit route is nevertheless legal and exact in every compatible world. An unused spectator can furnish another empty-case optimal buffer: no unique-buffer-label assertion is restored.

## Publication gate and proposed closeout boundary

This is NOT the final publication closeout. The next independent audit must check the immutable source refs, exact mathematical verdict/provenance, reporting clarifications, claim scope and publication/index consistency. It must distinguish a correctly scoped mathematical acceptance from completion of the repository publication workflow.

If the publication audit accepts the packet, the scoped closeout and canonical continuation index must record the accepted conditional partial-seed result, the separate audit verdict and immutable references; old candidate/revision entries must remain identifiable as historical. Final immutable readback is required after those writes. Until then the publication gate remains OPEN.

No numerical campaign was authorized or run for this theorem. No native or physical observer-access theorem, broader C3 closure, C4-C6 closure, force, geometry, energy, GR/ADM, continuum identification or fundamental time is asserted. Completeness, valid event directions, spectator typing, known finite capacity and labelled-root access remain assumptions. The next scientific obligation remains deriving which ordered-event distinctions are natively available; this publication step does not solve it.
