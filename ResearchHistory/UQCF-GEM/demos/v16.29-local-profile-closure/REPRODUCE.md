# v16.29 reproduction

Use the publication branch/commit, Python 3.11 and the included pinned parent .28 archive. Primary producer and verifier require only Python's standard library. The inherited regression suites additionally use SymPy 1.13.3 and mpmath 1.3.0.

From repository root:

```bash
python -m pip install sympy==1.13.3 mpmath==1.3.0
python ResearchHistory/UQCF-GEM/demos/v16.29-local-profile-closure/run_campaign.py
```

Or run only the new stage:

```bash
cd ResearchHistory/UQCF-GEM/demos/v16.29-local-profile-closure
python test_gate.py
python producer.py
python verifier.py
```

The full runner requires 30 new tests plus 198 inherited tests and records every command/exit in evidence/COMMANDS.json. Scientific status, input validity, proof status and scope are separate fields in evidence/VERIFICATION.json.

Expected NEW primary extension: 17 tree shapes, 54,842 original two-event squares and a separately checked transported copy; local-transmitted 5,755, maximum-only 32, local-masked 19, zero 49,036. These are regression observations, not proof axioms. The general classification requires PROOFS.md.

The .28 audit has 45,488 original and 45,488 transported diamond occurrences; no inference of independent sampling is made between corpora. Six explicit controls are separate from exhaustive enumeration.

FULL_CERTIFICATES.json.xz contains every raw case. Decompress with Python lzma or xz. Uncompressed SHA-256 must be `19d291e2f51286051a1e1c2840ab2d5994b9f8fe52f88f574ad2460b7ba7e69b`. Preserve input parent .28 raw SHA `daedbb1ac332aa8c8058700b9f3a6b0eaa2a9d0a3341918b42a6b0495ba94df4`.

The publication workflow reruns the full campaign, compares FULL_CERTIFICATES.json.xz, PRODUCTION.json, VERIFICATION.json, EXAMPLES.json and TESTS.json byte-for-byte with the original GREEN, and writes exact run/commit metadata in PUBLICATION_EVIDENCE.json. Source/report commits after execution are distinguished from scientific execution.
