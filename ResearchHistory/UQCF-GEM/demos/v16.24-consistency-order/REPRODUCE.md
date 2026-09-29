# Reproduce v16.24

Use the publication branch `research/v16.24-consistency-order` or the immutable published commit recorded by its GitHub PR. Original scientific execution: `19c7069bad79ff361d612f742ad5e79dbfef1dc6`. The later documentation/publication commit is not that execution.

Python 3.11; `sympy==1.13.3 mpmath==1.3.0`. From the repository root:

```bash
cd ResearchHistory/UQCF-GEM/demos/v16.24-consistency-order
sha256sum -c PUBLICATION_SHA256SUMS
python test_gate.py
python test_validation.py
(cd ../v16.23-overlap-descent && python test_gate.py && python test_schema.py)
(cd ../v16.22-response-selection-closure && python -m unittest discover -v)
(cd ../../foundational-closure-verification && python tests/test_fcv.py)
(cd ../v15.56-response-selector-obstruction && python -m unittest -v test_pruning_consistency_audit)
cp evidence/certificates.json.xz /tmp/v1624-original-certificates.json.xz
cp evidence/VERIFICATION.json /tmp/v1624-original-verification.json
python engine.py
python verify.py
cmp evidence/certificates.json.xz /tmp/v1624-original-certificates.json.xz
cmp evidence/VERIFICATION.json /tmp/v1624-original-verification.json
```

The independent verifier does not import the producer. Its declared size/view/sample bounds are checked against input metadata rather than trusted from producer flags. `test_gate.py` also checks valid and deliberately malformed certificates. Test execution regenerates diagnostic receipts; verify the publication manifest before regeneration.

A negative scientific witness is valid evidence. Malformed input, missing coverage, changed hashes or a corrupted dual certificate cause nonzero exit. The general proofs H0–H6 must also be reviewed; a passing finite enumeration is not a proof of all finite/rational cases.

Read RUN_REGISTRY.json for all original RED/GREEN metadata and PUBLICATION_EVIDENCE.json for the distinct fresh-publication execution. Original ZIPs are durably preserved under evidence/archives.
