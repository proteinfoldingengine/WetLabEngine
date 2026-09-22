# UQCF-GEM v15.43: Certified response geometry

## Finite result

The frozen v15.42 transport applied to the frozen response fields yields
`CANONICAL_RESPONSE_CURVATURE_NONZERO`: 740 cases, 148 canonical cases,
and 30,260 face records. The completed audit has no failed gate.
All five response families are nonflat on the common canonical carrier.
Nonzero curvature alone therefore does not establish canonical-family specificity.

The recovered full audit exited zero in 4,140 seconds. Its INPUTS and RESULTS
Git blobs match the previously reviewed artifacts byte-for-byte:
`f6435267950cde0985889056a67d5427f60f637f` and
`937024b3f90570c9b177bfb2eee7cdab25a13985`, respectively.

## Reproduction

From this directory, run `python -I response_geometry_gate.py --check docs/RESULTS.json`.
To regenerate, use `python -I response_geometry_gate.py --out docs/RESULTS.json`.
Official certification uses CPython 3.13.5, NumPy 2.3.5 and `PYTHONHASHSEED=0`
via `python ci_verify.py`; its exact-head success remains required.

## Interpretation boundary

Source correspondence is NOT_EVALUATED; physical claims and scientific breakthrough are false; Pillar 3 remains OPEN.

Source arrays are confined to inherited acquisition. The separate evaluator receives
only validated operational geometry and exact scalar responses, without source or
target data. Transport and inherited scientific artifacts remain unchanged.
The calculation depends on the inherited axioms and isotropic scalar lift.
No fundamental time or dark-matter primitive is introduced.
The prescribed next object is preregistered intrinsic-curvature interpretation
without source fitting. Novelty requires a separate prior-art assessment.
