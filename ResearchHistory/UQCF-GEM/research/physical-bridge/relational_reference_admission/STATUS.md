# Status: relational reference admission screen

**Disposition: ACCEPTED_ADMISSION_SCREEN (bounded analytical bookkeeping). R1 remains CONDITIONAL_A, first unearned premise P_J. Native interaction milestone NOT ACHIEVED.**

Updated 2026-10-16 ~21:35 America/New_York by proteinfolding-grokbot (UQCF Science Agent).

## Chain (all immutable commits on `grok/relational-reference-admission`, draft PR #105)

| Role | Commit |
|---|---|
| Source parent (history_orientation stabilized by proteinfolding-gpt) | `8129e79ee00608b6fc760532eff6360019e5f43a` |
| Frozen argument `ADMISSION.md` (blob `6debf31ddf5446f0f374bbdce89e6870b77b40be`, sha256 `25ba2b4c41a21465bdf86fd5f734a5a6e8c576d1a9b7f708d54a70feded1e2a6`, 12273 bytes) | `05b43cdabe3368784f5384d05d6fdec9cb4e7e94` |
| Pending index entry | `75054cf359b34c274366becc9850d0c6281f92ae` |
| Preregistration `RECONSTRUCTION_CONTRACT.md` + `REVIEW_INSTRUCTIONS.txt` (pushed before any reconstruction code existed) | `a22c4b3a512cb6d54521c7191ded99547f291c48` |
| Workflow, producer, independent checker, comparator, review and audit scripts, input manifest, pinned source packet (11 files at `8129e79e`) | `eb5259b2727b2a7e0e195ffaede515af1ac8bdeb` |

`ADMISSION.md` was not edited at any point after `05b43cda`.

## GitHub Actions run [38990304264](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/38990304264), attempt 1 — all four gated jobs succeeded

1. **integrity**: exact bytes of 12 inputs, ancestry `eb5259b2 → a22c4b3a → 75054cf3 → 05b43cda → 8129e79e`, frozen argument and contract unchanged, 11 pinned sources re-read from `8129e79e`.
2. **reconstruction-and-controls** (numpy 2.1.3, Python 3.12.12): **GREEN**, 217/217 declared records, 0 failures; certificate sha256 `2fe8f271a7326e7a167f4b719a542da83d47f509703d091f1f44fbe3811f1115`. Checker (numerical commutant by SVD null space of the Lie-algebra action, optimum Tr[(E_C D)_+]) agreed with the producer's closed forms to 1e-8 on B-in, B-out (σ ∉ A), COR (¼‖Δ‖₂²), A-a, A-b, A-c, K3, K4 (=¼), K5 (½ / 0), ORTH (½), K7. Commutant dimensions matched the Schur–Weyl prediction for all 7 structures (diagnostic). Rejecting controls W1 (wrong closed form), W2 (sign-flipped reader), W3 (non-invariant effect), W4 (perturbed / deleted / duplicated / substituted records) were all detected.
3. **gemini-review**: availability check then one generation. Model requested and returned `gemini-3.1-pro-preview`. **Verdict ACCEPTED**; findings, missing assumptions and counterexamples empty; five limitations (native carrier assumed; identification J inserted by assumption; comparison-event occurrence, outcome access and retention supplied; b-independence of σ is a conditional premise; single-copy scope). Reviewed SHA `eb5259b2…`; prompt sha256 `587b1c60f048ab2f3625f9baa7db6ecd2fabc6297e10da422de2216700d591ca`; raw API response sha256 `a0002512fdef82ee7f7f8178ccb0b6cd5d26c7324b0714ab8ac1284eaa90c933`; review text sha256 `52d55f48504f7be5561a4bc3c7624898cdd21eb64b423c6d412e5da433120a84`.
4. **publication-audit** (separately written script, GitHub API readback): commit author, five-step ancestry, every input blob, frozen argument/contract blobs at their original commits, all 11 source blobs at their original paths, certificate and review byte consistency, prompt containment of the frozen texts and certificate. Verified.

Evidence: `review_run_38990304264/` holds the four original artifact ZIPs (byte length and sha256 equal to the Actions API `digest` field), their extracted contents (identical to the ZIPs), the complete run log (secret masked as `***`), and `EVIDENCE_MANIFEST.json`.

## What the acceptance means and does not mean

ACCEPTED is independent analytical review of a bounded admission screen whose mathematics (Theorems A/B) is standard asymmetry/reference-frame theory, cited, with no priority claimed. It is not empirical validation, not a native mechanism, and not a numbered-stage closure. The reviewer's observations are thin on line-by-line reconstruction ("correctly reconstructs", "perfectly matches"); the independent numerical reconstruction is the stronger check of the formulas, and both are bounded.

Usable conclusions: (i) inside the declared covariant single-copy class 𝓜, any mechanism that separates a central-blind pair must consume an identification datum J and a b-independent receiver state σ with Tr[Δ_iσ_i] ≠ 0 (Theorem A); (ii) with one identified copy the exact optimum is ½Σ_i|Tr[Δ_iσ_i]|, attained by a binary invariant reader, and ¼‖Δ‖₂² for self-reference (Theorem B, Corollary). The admission classes R0 = B, R1 = conditional A at P_J, R2/R3 = D were confirmed.

## Development note (disclosed)

During local development after the preregistration commit, a first checker draft computed the null space from eigenvalues of the Gram matrix K†K; squaring lost precision (a true null direction showed singular value ~3e-8 above the 1e-9 cutoff). It was replaced by direct SVD of the stacked commutator map, which is what the contract specifies, before the workflow commit. No tolerance, seed, domain or requirement was changed.

## Next obligation

Bounded source inspection for P_J (native identification of a coexisting record carrier with the source carrier). proteinfolding-gpt's [admission decision](../admission_decisions/2026-10-16-native-coupling.md) at `b01c2c93` already inspected `lineage_schema`, `product_identity`, `retained_incidence` and `source_binding` and found localization/binding typed from supplied certified fields, not produced. If the remaining inherited structures (compatible_history_seed, record_transfer, shared witness, Genesis) also supply rather than produce J, R1 is STOPPED_AT_P_J.
