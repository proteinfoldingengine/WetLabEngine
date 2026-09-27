# v15.78 results — fixed-law covariance removes all hidden leakage

Verdict: **SOURCE_FREE_COVARIANCE_FORCES_RETAINED_CLOSURE**.
Separate channel gate: **COVARIANTIZATION_ERASES_POSITIVE_AND_NULL_LEAKAGE**.
All validity controls passed. No preregistered criterion changed; no
implementation repair was required. Three tests passed in the certified run.

## What was learned

For one fixed linear source map with no transforming source data, independent
local-frame covariance is too restrictive to select a leaking geometry source.
Already the six local X/Z conjugations distinguish all 64 Pauli tensors.
Every one of the 972 hidden-to-retained coefficients is forbidden: the exact
constraint rank is 972 and nullity is zero, with positive integer Gram entries
from 4 to 24. Independent local rotations leave eight support sectors with
sizes 1,3,3,3,9,9,9,27. The full local-rotation commutant is scalar on these
sectors. These are linear algebra dimensions, not geometric dimensions or
an assertion that every choice of sector scalar is CP.

The finite local Clifford average and the independent support-sector
projection agreed to 2.635e-15 or better. Generic local-rotation commutators
were zero at reported precision. This average constructs a different channel;
it does not reinterpret the original source or invalidate its historical result.

All 12 frozen reference states and all 27 hidden probes were covered: 72 rows
across three channels and two projection stages. The derivative measured is
DX[h]=Phi(h)-h for X=Phi-id, evaluated at the original regular reference.
It is not a finite-output polar derivative. Thus the singular correlations of
the depolarizing reset are not used as a polar base point.

| Channel | Before: retained norm | Before: retained rank | Before: Q/E rank | After: retained norm | After: Q/E rank |
|---|---:|---:|---:|---:|---:|
| Active symmetric null | 0.0173205081 | 1 | 0 / 0 | 8.33e-17 | 0 / 0 |
| Entangling XXI unitary | 2.4494897428 | 12 | 6 / 6 | 2.09e-17 | 0 / 0 |
| Identity | 0 | 0 | 0 / 0 | 0 | 0 / 0 |

All ranks were stable across the three frozen relative thresholds. After
projection, Q and E norms were exactly zero at reported precision for both
nontrivial controls. Before projection the active symmetric E norm was at
most 7.583e-17, whereas the unitary E norm ranged from 29.8881 to 49.0873.
The projected active symmetric channel agreed with complete depolarization
to 3.331e-16. Tiny post-projection retained residuals are roundoff, within
the frozen gate, not residual scientific leakage.

The minimum reported Choi eigenvalue was -1.412e-15 (rank-deficient controls;
within the frozen -1e-12 tolerance); maximum TP residual was 1.773e-15.
All original/projected CP checks and prepared-state checks passed. Matrix-unit
PTM reconstruction error was at most 4.603e-16; complex components were
preserved. Maximum Sylvester residual was 4.211e-15. Minimum reference
state eigenvalue was 0.0383382 and minimum edge singular value 0.0208610.

## Exact evidence

- Certified parent: `fdc9c239491d952672457e1ff994fbca7d4b4ed8`.
- Preregistration/tests, with gate.py absent: `c17d808c1e9954349e4e0e061b8de69f41276f44`.
- Scientific implementation tested: `e1dace9f60eabef5523d4b8550deec9aa7c0962d`.
- RED [run 36327099158](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36327099158), job `108641842831`, artifact `10934132126`.
- RED artifact SHA-256: `4412f08466bf94a95ee92c51bae35907af36c268bae53fc68bbbcf18041e5cef`.
- GREEN [run 36327292273](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36327292273), job `108642389532`, artifact `10933999459`.
- GREEN artifact SHA-256: `94c4730ba7cd35083210d3a19f52352c91e3cc717cf622b12db1f4b77db2e02a`.
- Full result JSON SHA-256: `67bd6a06bac15d48833332f102ee979404cc24985adb37e7da15ec02305e0343`.
- Lossless `RESULT.json.gz` SHA-256: `9ec1caff47d332f595f724fb5e91fb9c1a128b0f3d0a14e7e1e0c37aca2501ee`.
- Compressed result Git blob: `0d52a6f04e7a04c25e374eafa18a6b26d22293e9` (14,630 bytes).

Exact job logs were inspected. RED setup succeeded and stopped specifically
with `v15.78 scientific implementation absent: expected RED`; it ran zero
tests. Both artifacts were downloaded and their SHA-256 values checked.
Execution heads, frozen source bytes and the GREEN SHA256SUMS were checked.
GREEN passed all three tests; its JSON, not merely CI status, contains the
verdicts above. The complete JSON is archived losslessly to keep it available
beyond Actions artifact retention. `SUMMARY.json` is a derived convenience,
not a replacement for the full result. `TEST_LOG.txt` is from the artifact.

## Reproduce

From the tested commit, install Python 3.11 and numpy==2.3.5. In this folder:

```sh
OPENBLAS_NUM_THREADS=1 python -m unittest -v test_gate
OPENBLAS_NUM_THREADS=1 python gate.py > result.json
gzip -dc RESULT.json.gz > certified-result.json
sha256sum certified-result.json
```

The final documentation commit is additive; the tested scientific SHA above
is the certification boundary. No merge to main is performed.

## Boundaries and next bottleneck

This result is a structural obstruction under an extra hypothesis, not a
physical source-law selection. Fixed-channel invariance without source data
must be distinguished from covariance of a source-indexed family. In the
previous work the reference, generator, hidden tangent, and lift can transform
as source data. Those constructions remain covariant in that sense, and their
verdicts remain unchanged. Reference-free is not equivalent to source-data-free.

The tested extra axiom closes the entire hidden-to-retained channel before
polar geometry: it cannot distinguish symmetric from skew leakage. The next
meaningful question is which transforming source representations permit
hidden-to-retained transfer and whether additional naturality constraints can
select the observable skew sector while retaining a positive control.
No claim is made about all covariant source families, marginal descent,
changing admissible worlds, or deriving gravity. Genesis Pin and the ordered
recoverability framing are unchanged; no fundamental time or primitive
geometry is introduced.
