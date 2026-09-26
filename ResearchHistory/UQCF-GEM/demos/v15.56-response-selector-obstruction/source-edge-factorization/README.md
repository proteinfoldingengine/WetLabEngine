# Source-to-edge factorization: measured 243 -> 9 -> 3

Date: 2026-09-26. This is the bounded follow-up to the origin adjudication at ec33024e0343193f6a5d0c7ed62d8512701dd541. Historical source code, source prescription, fixtures, original verdict and original result files are unchanged.

## Status and exact evidence

Implementation: `9b78f689449a2bfe9dc332cad3542700e059f2ab`, `gate.py` git blob `b3a5d74cc6dfdbc4cce927305c1e40625280d249`, SHA-256 `eb6fa780cd6ab39399ccae4d77e357ea669531e0a3670bc599079a9b3e2a11eb`. The published blob was checked against the locally executed file.

Preregistration: `2a4d59d835d3bde70aa6c80958083d06b2cce198`, before implementation and the full measurement. No tolerance, state, source coefficient, or acceptance rule was tuned after the run.

RED: GitHub run [36271172393](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36271172393), exact head `90de106742e3515ae6e9147cbc94f239a9eed19f`. All 20 new tests failed for the expected absent implementation, without import-error masking. RED evidence artifact 10915019989 has ZIP SHA-256 `53a0899289cda4338f0a740daa6192bc2e9f77e5d4f463b40c2cdde717c04489`. Source snapshot artifact 10916055592 has ZIP SHA-256 `1f840233af536719e0fa26193d2ce64a71045947eac75a11a18a113ae5a1968c`. Both digests were verified locally after download.

Local GREEN: 20/20 new tests passed, and the complete pre-existing v15.56 demo unittest discovery passed 301/301. This is the UQCF demo suite, not a claim about the unrelated protein-engine repository-wide tests. All 11 x 243 source columns were measured; all saved artifacts were reread and validated successfully. The verdict was `FACTORIZATION_VERIFIED_243_9_3`.

Separate GitHub reproduction: [run 36271450389](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36271450389) on the exact implementation head above. Its live status must be read from Actions; local success is not a substitute for observing that run's completion. The workflow preserves the exact source snapshot, logs, full JSON report and all raw NPZ files as artifacts. Artifact availability is subject to GitHub retention; source code and this result summary are committed.

The adjacent `LOCAL_RESULT_SUMMARY.json` explicitly labels its measurement origin and preserves every fixture's loop-visible fraction. Full per-fixture spectra and arrays belong to the raw evidence bundle, not this condensed summary.

## What the raw data now establish

All eleven frozen states gave these effective ranks:

| Map | Shape | Rank |
| --- | --- | --- |
| E, source to edge coordinates | 9 x 243 | 9 |
| L, edge coordinates to loop coordinates | 3 x 9 | 3 |
| Full loop response K | 9 x 243 | 3 |
| Pi E, loop-visible edge response | 9 x 243 | 3 |
| (I-Pi) E, loop-invisible edge response | 9 x 243 | 6 |

Here Pi=L.T L/3. The three skew generators are Hilbert-Schmidt orthonormal; the edge coordinates are those of M_e O_e.T. The raw K is assembled by the unmodified historical `R.K_for`, independently of E and L, but shares its analytic derivative ingredients. The numerical factorization test reconstructs the full matrix response from L E, not merely its rank.

Local maximum factorization relative error: **1.0912481999644802e-15**. All main ranks were stable over the frozen relative cuts 1e-9, 1e-10 and 1e-11 with the floating-point floor retained.

The minimum sigma_9(E)/sigma_1(E) was **0.5292203972728348**. The largest sigma_4(K)/sigma_1(K) was **4.087100105630707e-16**. Thus the measured nine-dimensional edge image is not a collection of barely-resolved spectral directions on this ensemble. Minimum state eigenvalue was 0.03267949192431124; minimum edge singular value was 0.02000000000000003; the largest polar Sylvester condition number was 6.324555320336748. This does not establish behavior on singular strata or arbitrary states.

## The non-skew rank-eight ambiguity is resolved on actual measured data

The fresh run reproduces the original-style self-relative non-skew rank **8** at every edge. But the same actual residual arrays have effective rank **0** at every edge when compared to their unprojected parent response, under the preregistered policy. Their maximum Frobenius norm relative to the parent was **2.9170300317686414e-16**. This is no longer just a synthetic roundoff demonstration: the raw O and M arrays are saved, so the residuals can be recomputed.

The original rank-eight record is not erased or edited. Both the self-scaled diagnostic and the parent-scaled rank are retained in the new report. The correction changes how a theoretically vanishing residual is interpreted, not the source law or K. The hidden first-edge derivatives were zero on all measured basis columns. The maximum identity-source null response was 1.2051237634830628e-13.

The tolerance policy is an explicit numerical resolution rule, not a rigorous bound for every source of matrix-evaluation error. NumPy distinguishes these issues in its [rank documentation](https://numpy.org/doc/2.3/reference/generated/numpy.linalg.matrix_rank.html).

## Independent derivative probes

Three predetermined dense hidden/source combinations were checked on every fixture: **33 probes**, each evaluated at two four-corner steps, 2e-4 and 1e-4, and combined by the fixed Richardson formula. The maximum scaled discrepancy against the analytic derivative was **8.617460967362495e-8**, below the preregistered 1e-5 limit. The scale is max(1,||K_analytic||_F); analytic norms in this local run ranged from 4.90 to 18.90.

These are independent finite-difference evaluations of the state update and polar geometry. They are not an independent proof of the chosen source law and not a finite-difference check of all 2673 separate basis columns. Both step outputs, coefficients and analytic probe matrices are preserved.

## New state-dependent information beyond the compulsory rank cap

The squared-norm fraction ||Pi E||_F^2 / ||E||_F^2 varied from **0.291093568885343** to **0.3477852479702825**. The remainder is in the loop-invisible edge response. These are response-norm diagnostics, not probabilities, physical energies or counts of physical states.

The geometrical map L alone does not set this fraction. For example, under the additional isotropy assumption E E.T=c I_9 it would be tr(Pi)/9=1/3. No such isotropy assumption was imposed here. The measured variation belongs to the state/source-to-edge map E, not to an unexplained 243 -> 3 collapse. Its physical significance remains unestablished.

## Fail-closed behavior and verification scope

The new gate rejects false control flags, missing or duplicate fixtures, wrong or duplicated column labels, wrong matrix shapes, nonfinite values, source/provenance changes, corrupt raw artifacts, altered summary metrics and inconsistent verdicts. Invalidity returns a nonzero exit code even with Python -O. Explicit bash makes pipefail apply to workflow logging pipelines. Desired ranks are not required for validity: a controlled different rank structure is reported as a valid alternative; threshold-sensitive rank is unresolved.

The persisted verifier checks file hashes and recomputes all algebraic diagnostics and summaries from NPZ files. It does not remeasure the source derivative for every column. The execution artifact and frozen source provenance are therefore part of the evidence, not dispensable decorations.

A separate self-review tested five falsifications of the actual complete result: changed rank summary, false row control, wrong hash, missing actual fixture, and wrong verdict. All were rejected. Review was self-review; no separate independent code reviewer participated.

A minor helper limitation is deferred: `rank_info` permits an explicitly supplied zero parent scale with a nonzero residual rather than issuing a special diagnostic. This input is outside the measured path: every relevant parent response here is nonzero, and residual validity is also checked separately. It does not affect the reported results.

Execution rulings: use an additive child branch to preserve the historical record and avoid redundant historical workflows. Direct container cloning was unavailable, so the exact GitHub source-snapshot artifact was used and hash-checked rather than reconstructing dependencies from memory. These decisions do not change the scientific inputs.

## Reproduction

Check out the implementation commit (or a descendant containing unchanged gate and preregistration), then:

```bash
python -m pip install numpy==2.3.5
cd ResearchHistory/UQCF-GEM/demos/v15.56-response-selector-obstruction/source-edge-factorization
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m unittest -v test_gate
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python gate.py --output fresh_output
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python gate.py --verify fresh_output
```

Use a new output directory; the CLI refuses to overwrite an existing run directory. The existing demo regression command, run from the parent directory, is `python -m unittest discover -v`. Each raw NPZ has an explicit schema, fixture and column labels; `report.json` records its digest, metrics, software versions, historical source hashes and, in Actions, the exact execution head and run ID.

## Next scientific discriminator: source-law specificity

This is a proposed next task, not an executed comparison. Let pi(rho) collect the retained marginals and let geometry be g(pi(rho)). If a source update has an autonomous retained description, pi(T_s(rho))=Phi_s(pi(rho)), then any hidden h in ker(pi) gives

    g(pi(T_s(rho+eta h))) = g(Phi_s(pi(rho))),

independent of eta, and therefore mixed hidden/source response K=0 on a regular differentiable stratum. This is a conditional algebraic null theorem. A nonzero K under the chosen exponential tilt cannot establish a retained-marginally closed source update under those hypotheses.

The next useful comparison is the same exponential tilt versus an explicitly marginally closed local-unitary control, followed separately by a conditioning-selected, symmetry-breaking state ensemble. Freeze each control before measuring it. No alternative source law or non-axial ensemble was run in the present task. Nothing here derives gravity, selects the physical source law, or establishes a spatial dimension.
