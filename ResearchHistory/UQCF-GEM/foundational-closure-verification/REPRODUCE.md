# Reproduce FCV-1

Use the `research/foundational-closure-verification` branch or an immutable publication commit. Original scientific execution is `b1858ca92c3eff57c25fd655f75fa9b91d6d4788`; later evidence/documentation commits do not change those scientific modules. No main merge is required.

From the repository root, with Python 3.11 and pinned dependencies:

```bash
python -m pip install sympy==1.13.3 mpmath==1.3.0
P=ResearchHistory/UQCF-GEM/foundational-closure-verification
(cd "$P" && python tests/test_fcv.py)
(cd ResearchHistory/UQCF-GEM/demos/v15.56-response-selector-obstruction && python -m unittest -v test_pruning_consistency_audit)
```

To verify the committed complete certificates without regenerating them:

```bash
(cd "$P" && sha256sum -c PUBLICATION_SHA256SUMS)
(cd "$P" && python verify_certificates.py)
```

The verifier reconstructs the complete universe and its operators independently. It checks the historical reproduction in `evidence/REPRODUCED_1615F.json` as a new reconstructed record, not a retroactive upgrade of the old run.

To reproduce scientific production as well, in a clean disposable checkout or after preserving original evidence:

```bash
(cd "$P" && python produce_certificates.py)
(cd "$P" && python verify_certificates.py)
```

`produce_certificates.py` writes `evidence/certificates.json.xz` and `PRODUCTION.json`. `verify_certificates.py` writes `VERIFICATION.json`; failures return nonzero and an `INVALID_VERIFICATION.json`. Compare raw SHA256 after decompression with `21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6`. A fresh execution need not reproduce diagnostic log durations. Do not modify original archived logs to make them look like a new run.

To reproduce the historical selected-chain calculation itself:

```bash
(cd ResearchHistory/UQCF-GEM/demos/v16.15F-graded-obstruction-descent && python -m unittest -v && python gate.py)
```

Its embedded execution head will be the new checkout; compare its scientific records, not that head, to the preserved original/reproduced record. The full FCV-1 workflow records all command exit codes, test counts, exact sources and dependencies. It must pass behavioral controls and inherited tests before producing the full enumeration.

Definitions and claim boundaries are in TYPE_LEDGER.md / type_ledger.json. General arguments are in PROOFS.md. CLAIM_MAP.json links each P0–P7 claim to assumptions, implementation, tests and certificate fields. REVIEW.md is explicitly self-review. Finite enumeration is implementation evidence, not a universal proof or a physical cutoff.
