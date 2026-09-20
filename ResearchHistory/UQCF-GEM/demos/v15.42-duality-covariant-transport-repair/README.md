# v15.42 duality-covariant transport repair

Mechanical status: **TRANSPORT_PROTOCOL_CERTIFIED**. **Pillar_3 remains OPEN**.

This certifies the exact manufactured transport protocol. All scientific claims
remain false: response geometry has not been applied, source correspondence has
not been evaluated, and no physical connection, curvature, stress-energy,
Einstein equations, continuum limit, spacetime, or breakthrough is derived.

The ordered gate checks evidence, canonical L=5/L=7 operational complexes and
flat baselines, typed manifest, unique centered derivative and endpoint average,
duality/metric and covariance controls, constant null, L=5 nonflat canary,
every L=5 root, held-out L=7, scale, and superposition. Any failed exact gate or
exception stops immediately with PROTOCOL_INVALID and the first failed gate.
Only nonunique selection yields PROTOCOL_NOT_IDENTIFIABLE.

The centered weights are (1/2, 0, -1/2), rank 3; endpoint weights are (1/2, 1/2),
rank 2. Tangent frame variation is -u/2 and cotangent variation +u/2; cotangent
transport is the mechanical transpose/pullback of one tangent connection.

| Unit impulse invariant | L=5 faces | L=7 faces |
|---|---:|---:|
| 0 | 13 | 37 |
| 1/64 | 8 | 8 |
| 1/16 | 4 | 4 |

Each carrier therefore has 12 nonzero faces. Every root is checked (25 and 49,
respectively). Constants 0 and 7/3 give zero transport/curvature; amplitude 7/3
scales curvature linearly and invariants quadratically (49/576 and 49/144).
Exact superposition and D4 frame, reversal, orientation, basepoint and relabeling
covariance pass. Frame checks use local structural generators, all single-site
D4 actions, and simultaneous mixed frames, not exponential enumeration.

Evidence checks verify the four frozen Git blobs, both byte-identical vendored
modules, and ancestry of certified parent
`b9c5f29d8687a7dbc2af0595430aa73fbc5b8553`. The parent ledger is read as bytes
only to hash it; none of its scientific content is queried. The production AST
firewall checks complete identifiers and imports, including fixtures and
vendored modules, permits only the reviewed local closure and explicit standard
library imports, and excludes scientific-module I/O and dynamic import/evaluation.
Tests reject forbidden imports, identifiers and dynamic access, and execute the
complete control family with file opens and process invocation denied. Ledger
zero-query fields express this reviewed construction boundary, not runtime query
telemetry or a general Python sandbox.

The gate constructs and verifies canonical manufactured substrates itself.
Underscored `_audit` callbacks and control executors exist for failure-injection
tests; public `audit()` accepts no external substrate. Evidence and gate verdicts
are checked afresh; only pure mathematical evaluations are cached.

Run from this directory:

```sh
python -m unittest -v test_evidence.py test_selection.py test_transport.py test_holonomy.py test_controls.py test_gate.py
python protocol_gate.py --out docs/RESULTS.json
python protocol_gate.py --check docs/RESULTS.json > /tmp/v1542-results.json
cmp docs/RESULTS.json /tmp/v1542-results.json
python -m compileall -q .
```

`--check` compares canonical bytes and exits nonzero on a mismatch; failed
certification also exits nonzero. JSON uses sorted keys, two-space indentation,
one trailing newline, and canonical Fraction strings (including integral
Fractions). `docs/RESULTS.json` contains the pinned evidence, typed manifest,
selection ranks/weights, all retained canary counts, and ordered control verdicts.

Next required object:
**APPLY_CERTIFIED_TRANSPORT_TO_RESPONSE_GEOMETRY_WITHOUT_SOURCE_ADJUDICATION**.
