# v16.28 reproduction

Use the published branch `research/v16.28-diamond-attribution-closure`. Full final publication SHA and workflow/run metadata are given by the PR and PUBLICATION_EVIDENCE.json. Scientific execution SHA is `02954512b3e84e62a978dfe56f6007c501ef3b7f`; a later documentation/evidence commit is not retroactively called the scientific execution.

Python 3.11.16 was used by GitHub. The new primary programs require only the standard library; inherited tests additionally require SymPy1.13.3 and mpmath1.3.0.

From repository root:

```bash
python -m pip install sympy==1.13.3 mpmath==1.3.0
python ResearchHistory/UQCF-GEM/demos/v16.28-diamond-attribution-closure/run_campaign.py
```

This executes all 15 commands and checks exact expected test counts, totaling 198. It regenerates complete certificates, examples, verification, rejecting-test results, logs, source hashes and the actual execution receipt. Nonzero exit or missing expected tests is invalid execution, not a scientific negative.

For primary-only reproduction:

```bash
cd ResearchHistory/UQCF-GEM/demos/v16.28-diamond-attribution-closure
python test_gate.py
python producer.py
python verifier.py
```

To check the committed publication before rerunning anything:

```bash
cd ResearchHistory/UQCF-GEM/demos/v16.28-diamond-attribution-closure
sha256sum -c PUBLICATION_SHA256SUMS
```

After a full campaign, its newly generated evidence manifest can be checked with `(cd evidence && sha256sum -c SHA256SUMS)`. Execution receipts, timing-bearing logs and source archives legitimately change on reproduction; equality of these is not asserted.

The complete parent archive must remain available at `../v16.27-increment-attribution-closure/completion/evidence/FULL_CERTIFICATES.json.xz`, decompressed SHA-256 `1397e6d798c73126fc547afffb4bb7f681645bd83665af9b7ae6a66e472c866d`.

Expected v16.28 raw certificate SHA-256: `daedbb1ac332aa8c8058700b9f3a6b0eaa2a9d0a3341918b42a6b0495ba94df4`. These expected hashes identify the published experiment, not theorem assumptions inside the enumerators. The verifier separately reconstructs all admitted endpoints and paths.

Original counts: 3,486 endpoints,2,395 independent,1,091 dependent;34,562 states;45,488 diamonds;56,498 paths. The complete transported copy must agree, including each mapped state/diamond/coefficient. Diamond signs are 40,276 zero,3,344 negative,1,868 positive.

The publication workflow reruns the same full campaign and compares FULL_CERTIFICATES.json.xz,PRODUCTION.json,VERIFICATION.json,EXAMPLES.json,TESTS.json byte-for-byte with the original GREEN archive. Execution metadata and source archives legitimately differ by publication SHA; they are recorded separately, not asserted equal.
