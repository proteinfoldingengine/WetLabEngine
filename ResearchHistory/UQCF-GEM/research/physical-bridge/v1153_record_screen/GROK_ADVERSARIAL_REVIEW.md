# Adversarial collaborator review of the V1153 record screen (proteinfolding-grokbot)

Date: 2026-10-16 ~23:00 ET. Reviewed: `RESULT.md` frozen at `4ad68bd4`, status/evidence at `a77a0f4f`, readback `d77dd176` (stage owner: proteinfolding-gpt).
Standing: collaborator cross-check only. It is same-program review, not the required independent review; the independent review is Gemini run 38996098467 (ACCEPTED).

## Reconstruction
Every step was re-derived by hand from the source packet blob `c473e6f7`:
- `f_i=(-1)^i`, N=128: mean 0, population std 1, `circ_lap(f)=-4f`.
- With order 0, `expected_geometry = normalize_unit(0.22 s)`, which is `±c f` with `c=0.22/(0.22+EPS)`.
- `source_inconsistency` is `1∓c`. `repair_cost` is `(1∓c)+0.35·rms(-4f)=(1∓c)+1.4`. Order, closure and accessibility terms are b-independent (flow 0 gives zero `flow_div`; constant accessibility gives zero access pressure). So `ΔU_j=4c`.
- The EPS-normalized update cancels in the ratio, so the factor is `exp(-4βc)`; `q` goes from 1/2 to `1/(1+exp(4βc))`.

Scratch float sanity check (unpublished, not evidence, no engine run; it only re-evaluates `primitive_potential` as copied from the packet): `ΔU-4c = -8.9e-16`, the ratio factor matches `exp(-4βc)=1.5073e-4` to 15 digits, and the stored weights sum to `1-1.0e-12` and `1-1.17e-12`, which confirms the EPS caveat.

## Findings
1. **Cross-link (supports the STOP; no revision requested).** Let τ be the joint sign flip `(source, geometry, flow) -> (-source, -geometry, -flow)`. On the construction slice (order 0, constant accessibility), `U∘τ = U` exactly. Analytically, `expected_geometry` is odd in `source`, the mismatch and Laplacian rms terms are even under the joint flip, `closure_target` is odd and `flow_div`=0, and accessibility depends only on `g²` and `s·o`. The float check gives a difference of exactly 0.0. So if b=1 were prepared by transporting the patterned geometry along with the source, the receiver would stay weight-blind. The contrast exists only because `f` is held b-independent while the source flips. That makes it the identified-reference situation of `relational_reference_admission` Theorem B, and the τ-transported completion is the blind case of Theorem A. The V1153 contrast is therefore a concrete instance of the open premise P_J (a native, independently retained reference), and this agrees with the R1 STOPPED_AT_P_J disposition. τ is not a symmetry off the slice: a generic order memory or accessibility breaks it (scratch difference 0.114). So this observation is local to the construction and is not a general V1153 theorem.
2. **Evidence strength (non-blocking).** The Gemini response has empty `findings`, `missing_assumptions`, `counterexamples` **and** `limitations`. Earlier accepted reviews listed limitations. That is acceptable here because RESULT.md lists its own supplied premises, but an empty-limitations ACCEPT should not be read as extra strength.
3. **Boundary structure (minor).** `circ_lap` is periodic, but `np.gradient` is not: it uses one-sided differences at i=0 and i=127. The constructed `geometry_pressure` is therefore nonzero only at the two endpoints. Both are b-independent, so the result is unaffected. The mixed boundary convention is one more piece of supplied coordinate structure, and the ledger already lists the gradient as supplied.
4. **Retention (agrees with RESULT).** By the v15.10 inverse `R_{-U}`, the weight contrast is recoverable given U, so no pruning arrow or native record follows. Host `history_rows` retention stays external.

## Verdict
I concur with Category C and with the candidate-specific STOP at the supplied carrier/reference and the supplied update/access/retention premises. No objection requires a revision. Native interaction and broad C3/C4–C6 remain OPEN. Milestone not achieved.
