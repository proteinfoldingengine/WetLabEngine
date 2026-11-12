# observation_effect draft 3: verification and review receipt

Author: proteinfolding-grokbot. Date: 2026-10-18 America/New_York (~01:30 ET).

**Run:** [Actions run 39099852840](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/39099852840), scientific and workflow SHA `f1792632ee79aa0971a201620c3127b8da93a342`. All three jobs succeeded.
**Frozen argument:** `RESULT.md` sha256 `97b031585f8cc947a69e240bde628258fd213c548d86903e157674ccc3855e87` (= `constructions/observation_effect/CONSTRUCTION.md` draft 3 at `02818522`). Preregistration `FREEZE.md` sha256 `fa4fd4f69d13fb31a82530c34c066b6f5947b1a7e06df219a5bbcae203b67eeb`, committed at `4efed1be` before any verification code existed.

## 1. Preregistered verification: GREEN

- Producer (sympy 1.14.0 exact) and checker (numpy 2.3.5 column-stacked superoperators plus exact Fraction atom maps, seed 20261018) reproduced all 27 preregistered exact keys with identical key sets. The producer bytes were freshly reproduced and byte-identical (`cmp`). Producer certificate sha256 is recorded in the verify artifact's `compare.json` (`a24341886bcd…` is the compare.json hash).
- Bounded evidence (NOT universal theorems), 0 violations in every family: Thm 1 300 cases (216 closed, 84 nonclosed), Thm 2(d) 300, Thm 3 300 (144 with nontrivial kernel), Thm 4(a) 200 (137 persistent, 63 not), Thm 12.3 100 spectra × 2000 Haar motions plus the saturation condition, Prop 12.4(a) 300, Thm 12.5(b) 1000 with λ certified by Choi bisection (largest ratio C/bound 0.125 on the Actions run).
- Rejecting controls R1–R8: all REJECTED as required (closed motion substituted; classical prefix with nonzero record; √D replaced by D; owner section with λ > 0; three-atom swap claimed preserving; C·I₂ claimed to admit a non-normalizer; Ky Fan rank-1 saturation for (¼, ¼, −¼, −¼); faithful 2-sector pinching claimed perfect). The certified qubit-pinching constant is λ = 1/2 = 1/M.
- Certificate tampering: missing key, duplicated key, substituted value, wrong value, false provenance, a flipped control and wrong RESULT bytes were each DETECTED.

## 2. Independent Gemini review: ACCEPTED

Model requested and returned: `gemini-3.1-pro-preview` (temperature 0, no fallback). No prior verdict on this document was shown. The review hash is `acf39a6a288b3f4738cd2fad2a87fea7fa70a6fe854cd3d08c170f72eae10798`. The raw prompt, request, response and review are kept only as Actions artifacts (`obs-effect-review-1`). Public archiving of the raw text awaits Aaron's OK.

- Findings, missing assumptions and counterexamples: all empty.
- Reconstruction: every listed claim was marked VERIFIED, along with all exact examples.
- Inserted mechanisms named by the reviewer are the declared inputs: the occurrence of E, receiver identification I* and the projections Q, the supplied motions and preparations (premise G).
- Limitations: the cause of observation is not modeled; receiver ownership is assumed; no native dynamics selects the nonclosed motions.
- Novelty: standard operator algebra and quantum information. What is new lies only in the UQCF application, namely the keep-or-reveal split and the receiver-relative hierarchy. The author's disclaimer of new mathematics was judged correct.

**One field is not adopted.** The reviewer set `native_bridge_status` to `DERIVED_FROM_SOURCES`. That conflicts with its own inserted-mechanism and limitation lists and with RESULT.md sections 9 and 11. I record it but do NOT adopt it. The native bridge (receiver identification I*, native motion) remains **NOT_DERIVED**. The acceptance certifies the mathematics given the declared inputs, nothing more.

A further limitation: the reviewer's reconstruction is summary-level ("VERIFIED" per claim) rather than a line-by-line re-proof. The independent producer/checker campaign is the computational cross-check.

## 3. Publication audit: PASS

An immutable GitHub contents readback at `f1792632` of all 8 frozen, code and workflow files matched the checked-out bytes. RESULT.md matched the frozen hash. The producer, checker, compare and review artifact digests were recomputed and matched their manifests.

## 4. Scope

This accepts observation_effect draft 3 (sections 0–12.5) as a mathematically forced, effect-level construction given the declared inputs. It is not a native milestone. It does not derive collapse, occurrence, native access or receiver ownership, and it carries no CLOSED/CERTIFIED status and no main merge. The 96-case table (section 6.3) remains exploratory.
