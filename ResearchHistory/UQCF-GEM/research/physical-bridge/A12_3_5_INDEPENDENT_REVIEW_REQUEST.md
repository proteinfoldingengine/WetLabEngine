# A12.3-A12.5 independent whole-argument review request

Date: 2026-10-06 UTC.
Status: REVIEW REQUEST ONLY. This file does not review, accept, correct, publish, merge, certify, or extend any A12 claim.

## Review order

Review in dependency/concept order:

1. A12.3 — exact dual certificate update law
2. A12.4 — exact candidate-centered admissibility margins
3. A12.5 — no-go for naive incidence-overlap locality

Do not infer acceptance of a later item from an earlier one. Each receives its own attributable verdict.

## Immutable sources

### A12.3

Scope commit:
    71f4b61f3201777a3654cc09aeb3725627d10c47
Scope blob:
    e62cc948cdf36c925132a71d22401a3ff9e018e6
Scope file:
    ResearchHistory/UQCF-GEM/research/physical-bridge/A12_3_DUAL_CERTIFICATE_FIELDS_SCOPE.md

Proof candidate commit:
    cb8a6f1fc29b90e55a9cdf4f01b06eeaad8f855c
Proof blob:
    cded0e4481f656fd5bbcce9520f1b2843bcfe1d1
Proof file:
    ResearchHistory/UQCF-GEM/research/physical-bridge/A12_3_DUAL_CERTIFICATE_FIELDS.md

### A12.4

Scope commit:
    5be2e81ff224761a0f9622104354ac804dc15bae
Scope blob:
    7a7593740c65b87473cbe0bb36432064c278a428
Scope file:
    ResearchHistory/UQCF-GEM/research/physical-bridge/A12_4_CANDIDATE_RESPONSE_MARGINS_SCOPE.md

Proof candidate commit:
    c10c68922fbcbf520d28b1ca509faa38fcf3bcd5
Proof blob:
    a0d38aeacac80f036f9cb997f08f921f4e0f4b59
Proof file:
    ResearchHistory/UQCF-GEM/research/physical-bridge/A12_4_CANDIDATE_RESPONSE_MARGINS.md

### A12.5

Scope commit:
    fe6cf6207f5d9a007e52a75c088d0595d8c78a9d
Scope blob:
    001804a390c1ed9603e8bc15abac30cd255b981e
Scope file:
    ResearchHistory/UQCF-GEM/research/physical-bridge/A12_5_OVERLAP_LOCALITY_NOGO_SCOPE.md

Proof candidate commit:
    0f3a6790777ebe1ce1f6c2739c2ca99f0c2fa433
Proof blob:
    0da2ddad7ed177219f3fed50e7e152b2e1ffa679
Proof file:
    ResearchHistory/UQCF-GEM/research/physical-bridge/A12_5_OVERLAP_LOCALITY_NOGO.md

## Independence requirement

Use a fresh independent Codex/reviewer context. Do not reuse the proof-authoring chain as the reviewer. Read the complete immutable scope and proof files rather than relying on summaries in STATUS, chat, or this request.

The reviewer should attempt refutation before acceptance. A plausible argument or agreement with the intended physical direction is not sufficient.

## A12.3 review obligations

Check from first principles:

1. Exact equivalence tau>=3 iff every physical two-set K has W_E(K)>=1, including the palette-size assumptions needed to extend smaller covers.
2. Exact equivalence tau<=4 iff at least one physical H of size<=4 hits every root.
3. Addition update for W:
       W_(Add(i,x)E)(K)=W_E(K)-1
   exactly in the declared condition, and unchanged otherwise.
4. Claimed count |P|-|E_i|-1 of changed pair coordinates, including edge cases.
5. Deletion update for W and claimed changed-coordinate count |P|-|E_i|.
6. Addition monotonicity and exact 0->1 condition for upper cover indicators C_E(H).
7. Deletion monotonicity and exact 1->0 condition for C_E(H).
8. The legality decomposition: additions are controlled only by lower witness exhaustion; deletions only by surviving small covers plus local floor.
9. The one-update claims for mu_- and the non-scalar nature of the upper cover family.
10. The derivation of the signed response quadrants from W/C updates.
11. The A12.2 comparison is explanatory only; A12.3 must stand without A12.2 acceptance.
12. Relabeling covariance.
13. Claim boundaries: no conservation law, force, geometry, energy, or physical locality.

Actively search for counterexamples involving:
- palette size2 or3;
- roots containing all palette labels;
- covers of size0/1/2/3 rather than exactly4;
- same-root floor effects;
- several covers created/destroyed by one incidence.

## A12.4 review obligations

Check independently, even if A12.3 passes:

1. Exact addition shadow:
       Sh_-(i,x)={{x,y}:y notin E_i,y!=x}.
2. Iff criterion Add(i,x) legal iff A_E(i,x)>=2, including empty shadow and small-palette cases.
3. Exact deletion surviving-cover count D_E(i,x) and iff legality criterion with floor.
4. Threshold-crossing characterization of one-step response; do not accept sign claims by reference to A12.1 alone.
5. Relabeling covariance of A and D.
6. Exact addition counterexample showing same-state global mu_-/N4 cannot distinguish two candidates.
7. Exact deletion counterexample, including proof of tau before and after each deletion.
8. Scope of insufficiency: the displayed state-wide scalars are insufficient; information-theoretic minimality of A/D is NOT claimed.
9. Observer boundary: mathematical sufficient statistic is not an internally accessible observable.

Actively test:
- deletion candidates whose only surviving cover has size<4;
- additions whose shadow contains several count1 pairs;
- floor-saturated deletion;
- root containing all labels except x;
- candidate relabelings.

## A12.5 review obligations

This proof must stand natively without accepting A12.3/A12.4.

1. Verify both six-root states exactly as written.
2. Verify tau(L)=tau(I)=3.
3. Verify R0={d} is an isolated overlap component in BOTH states and that d occurs nowhere else.
4. Verify all matched metadata claimed by the no-go: palette size, root count, floors, tau, candidate root and candidate move.
5. Verify Add(R0,b) leaves L at tau3.
6. Verify Add(R0,b) makes I have a two-cover {b,c}; check whether tau could already have been<=2 before the move.
7. Verify the witness explanation, especially W_L({b,c}) and W_I({b,c}).
8. Check the logical conclusion: no function of the complete candidate overlap component plus the explicitly matched global scalars can decide exact legality uniformly.
9. Do NOT upgrade this to physical nonlocality or to failure of every possible emergent locality notion.

## Verdict format

Create separate files:

    INDEPENDENT_A12_3_WHOLE_REVIEW.md
    INDEPENDENT_A12_4_WHOLE_REVIEW.md
    INDEPENDENT_A12_5_WHOLE_REVIEW.md

Each must include:
- reviewer identity/context;
- date;
- exact scope/proof commit and blob;
- full verdict: ACCEPTED, ACCEPTED WITH REPORTING CORRECTION, REVISE, or REJECT;
- complete mathematical reasoning;
- any counterexample or correction;
- exact claim boundaries;
- whether the proof source itself must change.

If a proof needs mathematical correction, stop that result at REVISE and do not create a closeout. Freeze a corrected candidate and obtain a fresh review of the corrected proof.

If accepted, publication/reporting consistency review remains a separate gate before final closeout/accepted-status updates.

## Governance

No numerical campaign is requested. Do not reopen v16.54 or v16.55. Do not run the separately scoped efficiency benchmarks. Do not infer a force law, geometry, GR/ADM correspondence, dark-matter replacement, or fundamental time.

Further A12 theorem expansion is paused until these reviews are resolved.
