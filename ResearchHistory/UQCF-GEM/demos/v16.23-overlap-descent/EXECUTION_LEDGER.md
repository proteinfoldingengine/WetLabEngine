# v16.23 execution ledger

- Parent verified: a02202bc218adb4080489c54dd37a1f9e5ec77d1. New branch research/v16.23-overlap-descent. No main or historical changes.
- Definitions/proofs/preregistration/plan committed first: d091319bd837d5c6dccd66fcdb6b8ee139e79045.
- Wiring RED: d75bb1d9c043634a6f60c66d1a0153f39c7192c8, run36568025339, job109404706116. 22 expected missing-module failures, setup valid, archive preserved.
- Implementation: 939293191fd5bdd13a086b1d86ac15af595a1b6d. Initial run36569139253/job109408436653 passed 22 new and 57 inherited tests, complete producer and independent verifier.
- Self-review ruling: verify declared coordinate changes, not shape equality and variant labels alone. Added test_schema.py without altering producer inputs.
- Substantive RED: 54a3a1c57be3d749e86c88969b1556452235d513, run36569553274/job109409840157. Old22 passed; 2 rejection regressions failed, positive transformed case passed.
- Corrected scientific GREEN: 1a1a38db702b1da47a829f08ce2740e2d578ea27, run36570394253/job109412645015. 25 new +57 inherited tests passed. All7 commands exit0. Full producer bytes unchanged; verifier includes actual label/storage guards.
- Final original archive downloaded and ZIP SHA, CRC, all member hashes and source bytes checked. Full raw certificate SHA a9b4d6c28dcb5ffbfcd5a997e2cb12668de37f4360846a45a6b8125985e8ff8a; corrected verifier SHA76316091867ac1f6daf3cb8c9b5e8df3f67b23ded780afe79b853aa8568085bf.
- Supplemental local full verification had missing-file staging errors then reached a180-second tool timeout. No completed second-environment reproduction is claimed. Local unit/schema tests did complete. An unsupported streaming session request made no changes. These tooling events were not scientific GREEN failures and changed no source/criteria.
- Publication utility archive checks accepted all four original ZIPs and rejected tampered bytes locally. A local utility import from a shallow staging path failed before it was placed in the intended repository directory; no scientific code changed.
- Review is self-review. Algorithmic verifier independence is not separate reviewer authorship. No external attestation or artifact-provided executable instructions are used by publication.
- Final durable publication records its own SHA/run/job/attempt and fresh reproduction in PUBLICATION_EVIDENCE.json. The original scientific SHA is not relabeled as the publication head.
