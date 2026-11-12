# receiver_identification draft 20 freeze (section 26, every vertex is a possible receiver): status receipt

Author: proteinfolding-grokbot. 2026-10-19 America/New_York (freeze ~06:58-07:06 ET; review run 11:06-11:21 UTC = 07:06-07:21
ET; receipt ~07:25 ET).
Status: **verified (verify GREEN) and Gemini ACCEPTED (run 39242193441); publication readback PASS.** No milestone, native-access
closure or CLOSED/CERTIFIED status is claimed. Native bridge NOT_DERIVED.

- Frozen document: `RESULT.md` = `constructions/receiver_identification/CONSTRUCTION.md` draft 20 with its same-run addendum
  (commit `3f212074`, sha256 `2e10cfddb22129177e304e7a4456055d69769f42c36be811277c856cbd32883c`). Under review: section 26 in full
  and the draft-20 header item summarising it. No SOURCE.md (the inherited inputs are stated in the frozen sections 17-25).
- Preregistration: `FREEZE.md` at `6dfa6b6d` (sha256 `e93e37dd…`), parent `3f212074`, pushed before any freeze code was written.
  Structural counts from the disclosed counting script `/tmp/rid27/count.py` (sha256 `c2689540…`).
- Code: `375ff7e0` (`.github/scripts/uqcf_rid20_{producer,checker,compare,review,publication}.py`,
  `.github/workflows/uqcf-gem-rid20-review.yml`). Producer: parent-array AHU enumeration, condition rows in vertex coordinates on one
  unknown read matrix per carrier class, exact sparse Gauss-Jordan over Q, exact grounded-Laplacian field, depth-matrix reads as
  S = N C in cone coordinates. Checker (does not import the producer): leaf-attachment enumeration with nested-tuple canonical forms
  and BFS labels, isomorphisms by canonical DFS orders, sparse mod-p ranks (upper bound on each nullity) plus the explicit rational
  families of FREEZE.md (B) checked exactly against every row and independent mod p (lower bound), depth-matrix reads by
  common-ancestor sums, path-sum field with a neighbour-sum Laplacian check. Both programs matched every preregistered value on
  their first local run (producer 73 s, checker 58 s); no fix was needed before the code commit.
- Actions run [39242177494](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/39242177494) (push, head
  `375ff7e0`): verify **success**.
- Actions run [39242193441](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/39242193441) (`workflow_dispatch`
  review=true, head `375ff7e0`, the same SHA; first attempt): verify, argument-review and publication-audit all **success**.
  `producer.json` = `producer_repro.json` = local (sha256 `260fc553…`), `checker.json` `44a55925…` = local, `compare.json`
  `398a8d10…`, identical in the push and dispatch runs. Python 3.12.15, numpy 2.3.5, sympy 1.14.0.
  - Certified on every rooted tree up to 7 / 8 vertices (U7 85 carriers, 3,384 unknowns; U8 200 carriers, 10,744 unknowns;
    identity digests and nonzero-row counts equal in both programs): solution dimensions PN 28 / 36; PN+Z 7 / 8; PN+CN_F 2 / 2;
    PN+G⁺ 7 / 8; PN+C_recv = PN+C_climb 17 / 23; PN+S 7 / 8; PN+S_leaf 13 / 15; PN+S+C_climb, PN+S+C_recv, PN+S+G⁺ 1 / 1;
    PN+W2_F 7 and PN+W2_F+C_recv 1 (U7); U3 PN 6, PN+Z 3, PN+CN_F 2. Every PN+Z solution is κ id on every carrier with at most
    N − 1 vertices (producer: the κ id rows are implied by the system; checker: every family member). In all 24 field settings the
    field reads equal the diagonal depth-matrix reads at every (carrier, basis grade) and satisfy PN at every case; (Z) holds at
    every leaf exactly for G1, G3, G4 at θ = −1 and G2 at θ = −3, at the 69 / 154 children of Genesis for G5 and G6 at θ = −1, and
    at no leaf otherwise. Witnesses: the Genesis dump and the λ = 0 field read satisfy PN and fail (Z) at every leaf; ν_off
    satisfies PN and climb blindness at every leaf, is not cone-local, and has non-ancestor reads at 88 / 263 leaves (U8 value a
    diagnostic, equal in both programs). Events under κ id (2,268 / 6,174 cases): PN, conservation, blindness before and the κ g
    separation after hold at every case, Genesis included. Instances Z1-Z5 matched; controls R1-R9 REJECTED by both programs; 18 of
    18 tamper cases DETECTED (17 structural plus the duplicated JSON key).
  - Gemini: model requested and returned `gemini-3.1-pro-preview`, finishReason STOP, temperature 0, no prior verdict shown.
    Verdict **ACCEPTED**, 6 of 6 reconstruction items VERIFIED (Proposition 26.1; Proposition 26.2; Theorem 26.3, including the
    leaf-attachment step; Proposition 26.4; Control 26.5(a)-(c); the instances and preregistered values). Findings, missing
    assumptions, counterexamples and limitations empty. Inserted mechanisms (declared inputs, as listed by the reviewer): "the
    Genesis form is derived" is honest given that (S) and (PN) are explicitly assumed; "(CN_F) follows from (PN) plus its one-vertex
    instance" is stated with its exact conditions, and (Z) is fairly identified with the initially uninformed receiver at leaves;
    the statements relative to sections 17 and 18 are correct and correctly scoped; no vertex is presented as performing a read,
    the reads as a physical field, or depth as time or distance; infinite-class statements are separated from the finite evidence.
    Novelty: elementary mathematics (natural endomorphisms of the grade functor, a standard naturality argument), correctly stated;
    the UQCF-specific claims are properly scoped. native_bridge_status NOT_DERIVED, consistent with its inserted-mechanism list.
  - Hashes: review.txt `fd523f60…`, response.json `9df89408…`, prompt.txt `1ce3d211…`, request.json `fc248782…`,
    model_metadata.json `17d64c78…`. 670 output tokens, 4,962 thinking tokens on a 92,226-token prompt. Raw response kept in Actions
    artifacts only (publishing raw review archives to the repo needs Aaron's explicit OK). Acceptance is evidence of independent
    analytical review of conditional mathematics, not physical validation.
- Readback: the publication audit read back all eight frozen and code files at `375ff7e0`, byte-identical, RESULT.md =
  `2e10cfdd…`. Status PASS.
- What this acceptance covers: for arbitrary linear, isomorphism-invariant read maps on grades, the read ledger (PN) leaves exactly
  a lower-triangular depth matrix; cone-local reads (S), equivalently reads commuting with the inherited zero extension (W2_F), are
  exactly the field family of sections 24-25 with Genesis datum θ Σ x, so that Genesis form is derived from (S); leaf-point
  blindness (Z), or (S) with climb blindness, receiver blindness or the one-vertex apex square, forces F̂ = κ id, so under (PN) the
  read root shift (CN_F) is equivalent to (Z) and is not supplied by CN for the step. What it does not cover: a derivation of (S),
  (W2_F), (Z), (PN), CN or the P1 step from inherited sources; availability (A0)-(A3') and (U); physical access; a physical field
  law; preparability; or which outcome is actual. Native bridge NOT_DERIVED. No milestone.
