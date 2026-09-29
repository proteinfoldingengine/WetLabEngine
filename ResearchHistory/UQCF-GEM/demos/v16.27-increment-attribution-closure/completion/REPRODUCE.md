# Reproducing the completed v16.27 evidence

Use the exact scientific execution SHA in PUBLICATION_EVIDENCE.json, or the final publication commit with unchanged scientific modules. Python 3.11; inherited tests use SymPy 1.13.3 and mpmath 1.3.0.

From repository root:

```bash
python -m pip install sympy==1.13.3 mpmath==1.3.0
python ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/completion/run_campaign.py
```

This runs both rejecting suites, generates all original and metamorphic path certificates, independently verifies complete coverage, and runs the stated inherited regressions. It records each command/exit code/test count, source checksums, actual environment and execution SHA. It does not run unrelated protein-engine campaigns.

To verify the durable raw certificate without calling the producer:

```bash
cd ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/completion
python verifier.py
```

Expected independently reconstructed original counts are 3,486 endpoints, 3,446 multipath endpoints, 1,091 dependent endpoints and 56,498 legal paths. The metamorphic copy has the same counts. The raw certificate SHA-256 is `1397e6d798c73126fc547afffb4bb7f681645bd83665af9b7ae6a66e472c866d`; these are reproduction targets, not hard-coded scientific acceptance.

The historical verifier's defect remains reproducible, without modifying it:

```bash
V27_VERIFIER=verify V27_EVIDENCE=/tmp/v1627-legacy-contract python test_contract.py
```

That command is EXPECTED TO FAIL seven of 11 checks. Run the unchanged strict contract against the corrected independent verifier with `V27_VERIFIER=verifier`; all 11 pass. Do not mislabel the preserved RED as a failed scientific counterexample.

For repository-file integrity use `sha256sum -c PUBLICATION_SHA256SUMS` in this directory. Regenerated metadata/logs need not be byte-identical to older runs; the publication receipt states which scientific files were compared byte-for-byte.
