# Reproducing v16.23

Check out `research/v16.23-overlap-descent`, or the immutable publication commit linked from its draft PR. Do not merge to main to reproduce.

Python 3.11, SymPy 1.13.3, mpmath 1.3.0 were pinned in GitHub. The exact scientific inputs and raw certificate hashes are in RESULTS.md and PUBLICATION_EVIDENCE.json.

From `ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent`:

```sh
python -m pip install sympy==1.13.3 mpmath==1.3.0
sha256sum -c PUBLICATION_SHA256SUMS
python test_gate.py
python test_schema.py
(cd ../v16.22-response-selection-closure && python -m unittest discover -v)
(cd ../../foundational-closure-verification && python tests/test_fcv.py)
(cd ../v15.56-response-selector-obstruction && python -m unittest -v test_pruning_consistency_audit)
python engine.py
python verify.py
```

The first checksum command should precede regeneration: tests and verification write local receipts. For byte comparison, first copy evidence/certificates.json.xz and evidence/VERIFICATION.json elsewhere, regenerate, then use `cmp`. The published full certificate and corrected verifier outputs are deterministic at the pinned environment. `xz -dc evidence/certificates.json.xz` exposes every input, map, compatibility certificate, local-positive count and triple key. No source data are fetched from an external service during scientific reproduction; the parent certificate is already in the checkout and is hash-bound.

`publish.py` is a publication utility for the dedicated GitHub workflow, not required for mathematical reproduction. It reads only pinned artifact/run/job endpoints in this repository, treats all metadata as data, checks original ZIP and member hashes, runs fixed commands, and never executes an artifact-provided command or sends credentials to an external attestation service. The workflow commits only the new research package and numbered report after verification; it uses no force push.

General arguments: PROOFS.md O1–O7. Provenance: TYPE_LEDGER.md and PARENT_BINDING.json. Claim-to-check mapping: CLAIM_MAP.json. Review limitations: REVIEW.md and RESULTS.md.
