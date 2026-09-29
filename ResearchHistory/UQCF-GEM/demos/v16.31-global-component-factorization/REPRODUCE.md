# v16.31 reproduction

Use the published v16.31 branch/commit, not main. Executed environment: Python3.11.16. From repository root:

```bash
python -m pip install sympy==1.13.3 mpmath==1.3.0
python ResearchHistory/UQCF-GEM/demos/v16.31-global-component-factorization/run_campaign.py
```

This replays the historical verifier's three rejecting-contract failures (expected exit1, separately recorded) and then executes20 ordinary commands, all required to return0, with268 passing tests. It produces all exact certificates and independently verifies them. No prior verdict field is trusted.

For just the new mathematics:

```bash
cd ResearchHistory/UQCF-GEM/demos/v16.31-global-component-factorization
python test_contract.py
python test_gate.py
python test_review.py
python producer.py
python verifier.py
```

The producer creates evidence/FULL_CERTIFICATES.json.xz. Uncompressed SHA-256 must be `e95f9a46ca009c8f2ecf57148ae545b1c2b0f579ff7d236d253161b56bdc40f5`. Original totals:27399 endpoints,234116 state occurrences,376568 paths,295810 diamonds. Original and transported aggregate results agree, but copies are not independent samples.

Publication provenance is in PUBLICATION_EVIDENCE.json; original run ZIPs, metadata and logs live under evidence/history. A later invocation updates generated execution/log files in its checkout; it does not change the original archived attempts. The publication workflow checks source identity and compares deterministic scientific files to the final GREEN before committing durable evidence.

For the historical contract alone, V31_LEGACY=1 python test_contract.py is expected to FAIL exactly three tests. This demonstrates the inherited gap and must never be called a GREEN campaign.
