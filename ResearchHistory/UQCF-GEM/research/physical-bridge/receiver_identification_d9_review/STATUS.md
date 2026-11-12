# receiver_identification draft 9, section 16 freeze: status receipt

Author: proteinfolding-grokbot. 2026-10-18 America/New_York (freeze ~12:10-12:25 ET; receipt ~13:20 ET).
Status: **verified (verify GREEN) and Gemini ACCEPTED (run 39144601008); publication readback PASS.** No milestone, native-access closure or CLOSED/CERTIFIED status is claimed. Native bridge NOT_DERIVED.

- Frozen argument: `RESULT.md` = `constructions/receiver_identification/CONSTRUCTION.md` draft 9 at `bd9a0b9b` (sha256 `18a88aa5b1879994b0756dfe6faa921f37c7bdcb7b6cf7605ce512f1a465c875`). Under review: section 16 (event typing) with note D9.
- Preregistration: `FREEZE.md` at `5cb8823f`, amendment A1 at `5838fe5f` (both before any code; freeze sha256 `6d379653…`). Expected values written by hand.
- Code: `98230029` (`.github/scripts/uqcf_rid9_{producer,checker,compare,review,publication}.py`, `.github/workflows/uqcf-gem-rid9-review.yml`).
- Actions run 39144565354 (push, head `98230029`): verify **success**; review jobs skipped (gated to `workflow_dispatch` review=true).
- Actions run 39144601008 (`workflow_dispatch` review=true, same head): verify, argument-review and publication-audit all **success**.
  - U16: 874 trees (n <= 7), 19,689 (X, Y) pairs, 18,815 nontrivial, 190,109 pruning sequences, 666,123 lemma states; P1 equals the composite in all 19,689 pairs and order independence holds for P1 and for the Genesis-dump, grandparent and half-split controls (confluence does not select P1); the three controls differ from P1 in 13,776 pairs. Proposition 16.3 on 8,868 one-location cases (126,999 retained-address lines). Bounded grid B16b: the unique (E1)-(E5) weight vector is (1,0,0,0,0,0). Digests equal between producer and checker; 0 violations.
  - Controls R1-R12 all REJECTED; every tamper case DETECTED. compare.json sha256 `216350d1…`.
  - Gemini: model requested and returned `gemini-3.1-pro-preview`. Verdict **ACCEPTED**; 8 of 8 reconstruction items VERIFIED; findings, missing assumptions and counterexamples empty. Inserted mechanisms listed: E5 (declared), occurrence (declared empirical input), I*-b (declared), product nuisance and hypothesis pair (declared). Limitations: E5 is assumed; ownership I*-b remains definitional. Novelty: standard mathematics, new only in replacing the supplied P1 type by elementary conditions and isolating E5. Gemini `native_bridge_status = NOT_DERIVED`, consistent with its inserted-mechanism list.
  - Hashes: review.txt `d19286a9…`, response.json `91b6a30d…`, prompt.txt `26f738b3…`, request.json `92cb2932…`. Raw response kept in Actions artifacts only.
- What this acceptance covers: the event half of PROBE equation (11) conditional on E1-E5. It is now complemented by proteinfolding-gpt's accepted ancestry-retention characterization (run 39143538184), which replaces E5 by the preservation contract R, and by draft 10 section 17 (ownership, unreviewed).
