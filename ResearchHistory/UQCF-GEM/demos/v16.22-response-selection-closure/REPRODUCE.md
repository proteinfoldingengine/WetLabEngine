# Reproduce v16.22

Use branch `research/v16.22-response-selection-closure` or the exact published commit. The final scientific executable source is `1167e88ee38c332de27ed2d96795c036f7f521e8`. Later report/publication files do not replace that execution identity.

Python 3.11, `sympy==1.13.3`, `mpmath==1.3.0` match GitHub. The mathematics uses exact rational operations, not floating thresholds.

```bash
python -m pip install sympy==1.13.3 mpmath==1.3.0
cd ResearchHistory/UQCF-GEM/demos/v16.22-response-selection-closure
sha256sum -c PUBLICATION_SHA256SUMS
python -m unittest discover -v
python engine.py
python verify.py
```

The producer writes the COMPLETE finite certificate to `evidence/certificates.json.xz`, and PRODUCTION.json records its raw hash. The independent verifier reconstructs the finite category, solution space and reference inverse; it writes VERIFICATION.json and rejections.json. An invalid input/certificate causes a nonzero process exit and an INVALID.json diagnostic. Passing valid data is not enough: all deliberate corruption checks must also be rejected.

The inherited suites are separate and their scope is not expanded into unrelated protein work:

```bash
(cd ../v15.56-response-selector-obstruction && python -m unittest -v test_pruning_consistency_audit)
(cd ../../foundational-closure-verification && python tests/test_fcv.py)
```

Proofs establish general statements under their stated assumptions. This finite enumeration is not their substitute. To reproduce the smaller checker-control universes, import engine.produce(N), N=1..5, and pass the returned object to verify.verify. The public command-line campaign uses the frozen bound 5.

`evidence/archives/` preserves all four original Actions archives byte-for-byte. `evidence/history/` preserves run/job metadata and original job logs. `RUN_REGISTRY.json` pins each expected SHA and archive digest. `PUBLICATION_EVIDENCE.json` distinguishes original scientific execution from later fresh reproduction and the durable publication. Review is self-review, not independent human/agent review.
