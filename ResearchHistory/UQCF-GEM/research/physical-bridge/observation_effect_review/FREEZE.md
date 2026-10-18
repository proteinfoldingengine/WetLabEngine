# observation_effect draft 3: analytical freeze and prospective preregistration

Author: proteinfolding-grokbot (UQCF Science Agent). Date: 2026-10-18 America/New_York (~01:00 ET loop).
Baseline research head: `efae7e691f4045a58b805a8eb5fbf5d3e4334b9b`.
Frozen argument: `RESULT.md` is the byte-exact copy of `constructions/observation_effect/CONSTRUCTION.md` at commit `0281852258bede215d2df2dee48bb844a0ccd466` (git blob `754d2d0dff98a623696f4ced4b94f63e602394a7`, sha256 `97b031585f8cc947a69e240bde628258fd213c548d86903e157674ccc3855e87`). Sections 0–12.5 are the frozen argument; section 13 is a plan and makes no claim.

This file is committed BEFORE any producer, checker or control code for this freeze exists in the repository and before any of it is executed in Actions. The scratch checks `/tmp/obs/chk1–5.py` (RESULT.md section 10) were exploratory, were run before this freeze and are disclosed; their outcomes are known and are NOT relabelled as preregistered. The preregistered campaign below is executed by new code written after this commit.

## 1. What is frozen and what is reviewed

Reviewed claims (typed):
- **General proofs (analytic, for Gemini review):** Theorem 1 and Corollaries 1.1–1.4; Theorem 2(a)–(d); Theorem 3; Theorem 4(a)–(d) (4(e) is cited from GPT's separately reviewed extension and is not re-reviewed); Proposition 8.1; Proposition 12.1; Theorems 12.2, 12.3; Proposition 12.4; Theorem 12.5(a)–(d); Corollary 12.6.
- **Exact finite instances (producer + checker):** the named examples listed in section 2.
- **Bounded evidence (randomized, checker only, NOT universal):** section 3. No finite no-counterexample result is a theorem.
- **Not reviewed / exploratory:** the 96-case v15.17 table of section 6.3 (not independently reproduced here; stays exploratory), and literature priority statements.

Declared inputs and premises, unchanged and NOT claimed derived: occurrence of the observation (Aaron's empirical-input rule); which E; every motion U or Φ; the preparations and premise G except for the one-prefix occurrence pair; the receiver identification I* (Q is declared). No native access, receiver ownership, collapse cause, clock, geometry, dark-matter primitive or fitted parameter is claimed. No CLOSED/CERTIFIED status; no main merge.

Mentions in RESULT.md that OTHER documents were accepted are context only and are not evidence for this review; the reviewer is told to verify every cited ingredient that a frozen claim relies on.

## 2. Preregistered exact universe (producer: sympy exact rationals; checker: independent algorithm)

Each item has a declared exact expected value from RESULT.md. PASS requires producer = expected exactly and checker = expected (exact for rational classical items; |err| ≤ 1e-12 for floating quantum items), with identical key sets.

| Key | Object | Expected |
| --- | --- | --- |
| W.tv_obs, W.tv_unobs | 6.1 receiver trace distance observed / unobserved | 0, 1 |
| W.kappa, W.occ_tv | 12.2 κ and occurrence TV_R for prefix \|+⟩\|0⟩ | 1/2, 1/2 |
| W.kyfan | 12.3 F(2) for spectrum of Δ | 1/2 |
| P.tv_obs, P.tv_unobs | 6.2 | 3/10, 0 |
| P.global_obs | 6.2 observed global chain | 5/8, 1/2, 3/10 |
| P.kappa1, P.occ1, P.occ0 | 12.2 instances | 3/8, 3/10, 0 |
| H.central_equal, H.full_effect | Thm 2 strictness witness A = M2⊕M2, U = (1 2), ψ = (\|0⟩+\|2⟩)/√2 | true, 1 |
| Z.cadence | Cor 1.4 minimal cadence gap | 1/2 |
| S.swap_record | Thm 4(c) sector swap X on S, record (0,1,0,0) | (0,0,0,1) |
| L.owner, L.tracial, L.unobs | Cor 1.2 three-atom example | (1,0), (1/2,1/2), (1/2,1/2) |
| O.perfect | Prop 12.4(b) owner-section occurrence TV | 1 |
| Q.D, Q.C | Thm 12.5(c) qubit rotation, symbolic in θ | sin²(θ/2), ½\|sin θ\| = √(D(1−D)) |
| G4.D, G4.C | Thm 12.5(d) four-atom control | 0, 1 |
| G3.D, G3.C | three-atom swap | 1, 1 |
| N.kernel | Thm 3 nonfaithful kernel counterexample (E_m δ_u) | inclusion fails |
| M.witness | Thm 4(c) [D2] U = I⊗(I−π)+V⊗π on M2⊗I2 | in Z(A)′, not normalizing, keeps record |

## 3. Preregistered bounded evidence (checker, fixed seed 20261018, numpy pinned)

- Thm 1: E Φ E = E Φ ⟺ Φ*(A) ⊆ A on 300 random (A, E, Φ) with tracial, faithful nontracial and nonfaithful E, and normalizer, Kraus-in-A and Haar-random channels.
- Thm 2(d): ‖Nρ − Oρ‖₁ ≤ ‖ρ − Eρ‖₁ on 300 cases.
- Thm 3: support inclusion ker E(ρ) ⊆ ker ρ for 300 faithful cases.
- Thm 4(a): record persistence ⟺ [U, P_k] = 0 on 200 cases (commuting and generic U).
- Thm 12.3: for 100 random Δ and ranks, the closed form is attained by the constructed eigenvector-aligned motion and never exceeded by 2000 random unitaries each.
- Prop 12.4(a): κ ≤ 1 − 1/M for 300 random states and M-sector pinchings.
- Thm 12.5(b): C ≤ D + 2√(D/λ) with λ certified by bisection on the Choi matrix of E* − λ·id, 1000 cases incl. near-identity channels.

## 4. Preregistered rejecting controls (each must be REJECTED; any acceptance is RED)

R1 closed motion substituted in W (U = W_c only): claimed "unobserved 1 vs observed 0" must fail. R2 classical prefix claimed to carry a nonzero occurrence record. R3 the bound of 12.5(b) with √D replaced by D, tested on the qubit rotation at small θ. R4 the nonfaithful owner section claimed to have λ > 0. R5 the three-atom swap claimed preserving (D = 0). R6 the multiplicity-only algebra C·I_2 claimed to admit a non-normalizing unitary in Z(A)′. R7 Ky Fan saturation claimed at receiver rank q = 1 for spectrum (¼, ¼, −¼, −¼). R8 a faithful two-sector pinching claimed to give a perfect occurrence record. Certificate tampering: missing key, duplicated key, substituted value, wrong value and false provenance (wrong RESULT.md hash) must each make the comparator fail.

## 5. Resource and stopping rules

One Actions run per pushed head, ubuntu-24.04, Python 3.12, pinned `sympy==1.14.0`, `numpy==2.3.5`, `mpmath==1.3.0`. Job order: verify (producer, checker, comparator, controls) → Gemini argument review (`gemini-3.1-pro-preview`, temperature 0, no fallback model) → publication readback (immutable GitHub readback of the frozen bytes at the run's SHA). A RED verify result stops the run before review and is preserved. A REVISE or FAIL verdict is preserved and answered by a new freeze, never by editing this one. Raw reviewer output stays in Actions artifacts; only a summarized receipt is committed (public archive of raw output awaits Aaron's OK).
