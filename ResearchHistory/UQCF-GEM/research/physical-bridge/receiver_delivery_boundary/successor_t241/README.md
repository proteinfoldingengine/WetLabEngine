# Successor verification of CORRECTION_T241 + CORRECTION_T242 (code only; no result claimed here)

Author: Grok (proteinfolding-grokbot), 2026-11-01 ~11:30 MST. The prospective plan (V1-V5, C1-C6 in CORRECTION_T241 §4 at
8157f7b4; V6, V6b, V7, C7, C8 in CORRECTION_T242 §4 at e16a7b79) was committed before any of these files existed.
RESULT.md, CORRECTION_T241.md, CORRECTION_T242.md, the T-240 scripts and the run 41313483346 evidence are unchanged.

- `produce_s.py`: sympy producer (exact radicals).
- `verify_s.py`: stdlib-only checker with its own Q(√2) arithmetic, sparse tensor indexing, 2×2 trace norm and rank routine;
  it rebuilds every operator from the definitions and hardcodes the frozen predictions.
- `test_controls_s.py`: C1-C8 plus producer-hash and dropped-section integrity controls; each must make the checker RED.
- Workflow `.github/workflows/uqcf-receiver-delivery-successor.yml`: FCV stack, produce, verify+controls, fresh reproduction.
  No Gemini job yet; the fresh whole-argument review, the publication audit and the readback are separate later steps.

Disclosed choices the frozen plan left open (made before any run; no local execution of these scripts, only `py_compile`):
- V5(i) "three fixed exact non-basis realizations from the V2 family": the V2 rational set has only two non-basis points
  (cos θ = 3/5, 4/5). The third is T-240's W_N (e_0 = (3/5)|00⟩ + (4/5)|11⟩, e_u = |01⟩), which is outside the θ family.
- V5(ii) "two named realizations": F_p = diag(1,0,0,0) on K vanishes on every V2-family and W_N realization (none has
  e_u overlapping |00⟩). The named pair is W_E (contrast 0) and W_X: e_0 = |11⟩, e_u = |00⟩ (contrast 1/5).
- "Pair contrast" of a fixed F means |Tr F (Wρ_+W† − Wρ_−W†)|; Δ of an interface is the optimized contrast over its effects.
- V6 "initial contrast" is Tr F (Δρ ⊗ |00⟩⟨00|), which equals Tr P_ψ Δρ = 0 because every diagonal block of F is scalar.
- V7 uses F = (1/3)·1 + (1/2)·P_ψ ⊗ 1_R for the compression check (f = (1/3, 7/12, ·, 11/24)).

Scope unchanged: the original diagonal pair, finite blank K, the unrestricted class 𝒲(C,K). Supporting mathematics only.
Native bridge NOT_DERIVED; scientific_breakthrough: false; no claimStatus change.
