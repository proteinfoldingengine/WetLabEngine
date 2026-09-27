# v15.82 — Polar continuation obstruction confirmed

Verdict: **POLAR_CONTINUATION_OBSTRUCTION_CONFIRMED**. All frozen validity
checks passed. This diagnostic explains the v15.81 domain exit; its
**FINITE_COMPONENT_INTERFERENCE_WINDOW_NOT_CONFIRMED** verdict is unchanged.

## What was learned

For the same candidate 46, lambda=-1 source and edge (0,1), the exact
connected-correlation determinant is a quartic in q=exp(-2u). Exact rational
isolation finds exactly one simple root in the preregistered q interval
[1/5,9/20]. Its ordered-strength location is approximately

u* = 0.75821740030905194884,
q* = 0.21949303007447578159.

No uniqueness outside that bracket is asserted. The label u is ordered
source strength, not fundamental time. The witness was selected because
v15.81 failed there; this is an explanatory diagnostic, not held-out evidence.

At the isolating-interval midpoint, the retained matrix singular values are
approximately (0.1526066643, 0.05223467545, 2.42e-63). The exact root has
rank two: a simple determinant zero cannot have rank at most one, since
then its adjugate and determinant derivative would vanish. The computed
determinant derivative with respect to q is 0.0004230830581.

The quantum matrix stays strictly positive. Its minimum eigenvalue at the
root approximation is 0.06664734093. More strongly, the exact convex mixture
of the original matrix and its unitary conjugate supplies a lower bound
of approximately 0.04338847702 throughout q in [0,1]. The original complex
binary64 matrix is retained without modification: its trace differs from
one by 8.3267e-17. Exact rational claims refer to that stored input, not an
unavailable exactly normalized preparation.

## Canonical polar geometry at the boundary

Before the root the canonical orthogonal polar factor has determinant +1;
after it, determinant -1. Thus it cannot extend continuously as a full
orthogonal link while agreeing with the unique polar factor on both sides.
Continuous local SU(2) frame changes cannot eliminate this determinant
change. This is a singularity of the specified geometric extraction along
a valid source path, not failure of quantum positivity or CPTP composition.

The frozen side-pair measurements were:

| Distance in ordered strength from root | Singular values of polar-factor difference |
| --- | --- |
| 1e-3 | (2, 5.5777050e-5, 5.5777050e-5) |
| 1e-5 | (2, 5.5844567e-7, 5.5844567e-7) |
| 1e-7 | (2, 5.5845243e-9, 5.5845243e-9) |

These agree with the rank-two crossing theorem: the limiting difference
has singular values (2,0,0). At the smallest frozen separation, both
factors have Frobenius distance one from the root partial-isometry
approximation to within 1.68e-15. The partial isometry is well-defined on
the retained support at the root; this does not supply a continuous full
orthogonal extension. Midpoint SVD values are approximations, not evaluations
at an exactly represented algebraic root.

All 27 hidden Pauli inputs have exactly zero source-edge marginal derivative
against all 15 nonidentity edge observables, coefficient by coefficient.
The baseline source path therefore crosses the geometric boundary on an
edge whose hidden-input restriction remains zero. These are different
derivatives. Root Q/E fields are **null because undefined**, not zero.
No reflection-corrected observable, omitted edge, shortened window or
threshold adjustment rescues v15.81.

## Verification and exact evidence

Parent documentation SHA: `8ef3c4388dffcd0b799578600246808e5aa14c2e`.
Preregistration/tests SHA: `c1aa2dcace27d4c1eb11dc68442935b6361eff5a`.
Scientific implementation SHA: `2a7fcdf5694561526901473f43c42af9e01c82ee`.
Branch: `research/v15.82-polar-boundary-obstruction`.

- [Expected RED run 36348949021](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36348949021), job `108703701101`.
  Setup succeeded; the explicit missing-implementation assertion failed.
  [Artifact 10941133419](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36348949021/artifacts/10941133419).
  ZIP SHA-256: `e3c456f9537d47d3594828f0c971c35c4356f099a7738d8083565a3e5767486a`.
- [GREEN run 36349171264](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36349171264), job `108704332891`.
  Three tests passed; scientific JSON independently reports the above verdict
  and `all_valid: true`.
  [Artifact 10940904024](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36349171264/artifacts/10940904024).
  ZIP SHA-256: `a5156ca25c784eb23f6708aeb49ac154adf8c1c583508a28f183367c225edb14`.
- Lossless [RESULT.json](RESULT.json) SHA-256:
  `a60feb6ab4506e8049d72c6a4e85627ae6f9137e3509aa9da44e14f6f151df56`.
  [SUMMARY.json](SUMMARY.json), [EVIDENCE.json](EVIDENCE.json),
  [TEST_LOG.txt](TEST_LOG.txt), and [SHA256SUMS](SHA256SUMS) are published.
  SHA256SUMS uses the artifact filename `result.json`; its bytes are preserved
  here as `RESULT.json`.

Both exact job logs and downloaded artifacts were inspected. ZIP hashes,
execution SHAs, frozen source bytes and every artifact checksum were checked.
The rational complex-input roundtrip error is zero. Across the five original
control strengths, state identity error is at most 1.39e-17 and connected
matrix error at most 5.56e-17. Maximum high-precision polar orthogonality
and reconstruction errors are 8.44e-81 and 1.59e-81 respectively.
The synthetic crossing and no-crossing controls passed. There were no
implementation repairs or changed scientific criteria after measurement.
Read-only mathematical, code and artifact interpretation reviews found
no critical or important issue.

Reproduce from the tested implementation SHA with Python 3.11 and:

```sh
python -m pip install numpy==2.3.5 sympy==1.13.3 mpmath==1.3.0
cd ResearchHistory/UQCF-GEM/demos/v15.56-response-selector-obstruction/polar-boundary-obstruction
OPENBLAS_NUM_THREADS=1 python -m unittest -v test_gate
OPENBLAS_NUM_THREADS=1 python gate.py > result.json
```

The final documentation commit is separate from the tested implementation
and uses `[skip ci]`. This branch remains unmerged.

## Interpretation boundary and next question

Physical source admissibility does not ensure that a full-rank canonical
polar atlas survives every ordered update. The newly identified boundary
requires an explicit treatment of changing retained support. The next
question is whether support-restricted transport and composition retain a
well-defined observable through this crossing, and what information is
necessarily lost. No such continuation is certified by this experiment.

This result does not obstruct every possible extraction of geometry, select
a unique physical source law, or modify admissible-world sets. Genesis Pin
and ordered recoverability remain foundational. No fundamental time,
external alignment, heuristic fit, dark-matter primitive or gravity derivation
is introduced.
