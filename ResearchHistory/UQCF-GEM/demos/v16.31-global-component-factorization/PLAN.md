# v16.31 implementation plan

Spec: PREREGISTRATION.md. Goal: adjudicate G1–G8 on actual complete retained endpoint intervals and publish rejecting evidence. Implementation is direct in this session; do not dispatch an imaginary worker.

Files: producer.py (ancestral-array enumeration, exact local transforms and certificates); verifier.py (independent Prufer enumeration, legal-permutation states, inclusion-exclusion and full-state graph/reconstruction); test_gate.py (constructive/adversarial/metamorphic tests); test_contract.py (same missing-document contract against historical and new verifiers); run_campaign.py (actual command exit/test/source records); numbered report and publication workflow.

- [ ] Freeze proof/types and input coverage, publish rejecting tests; execute both legacy-contract RED and missing-module wiring RED.
- [ ] Implement local cube and component certificates. No fixed closure answer in producer or verifier. Compute every graph and coefficient.
- [ ] Implement independent verifier with complete coverage, graph equality and functional reconstruction on every reachable state.
- [ ] Execute current and all 233 inherited tests on GitHub Actions; inspect every failure, archive real attempts, and rerun changed executable code.
- [ ] Review assumptions, antichain lifting, distinction from Cartesian state space, all-background versus baseline graph, and certificate completeness. No fabricated independent reviewer.
- [ ] Publish reports, raw certificates and original attempts, then rerun the full campaign in a publication job; compare scientific bytes and source identities; push only the additive branch and read back the committed manifest.

Ruling: .30's unfulfilled full-universe requirements are not silently inherited as verified. This new campaign freezes its own complete endpoint universe; it records how that differs from the old square enumeration. The old implementation stays intact.
