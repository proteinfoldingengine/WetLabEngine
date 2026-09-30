# Retained CI optimization protocol

Approved bounded infrastructure work, not a new numbered scientific stage.
Verified starting parent: e789ce42bac28e084a4f0264180b738534d69923 (v16.39 actual-merge audit36768113676).

Keep the certified v16.39 scientific files, mathematical definitions, domain, outputs, independent verifier and every inherited test unchanged. No seven-vertex work. New code lives outside the certified scientific source tree.

Preflight must check the durable v16.39 source/publication manifests and run current rejecting controls before expensive work. Within each execution, run scientific reconstruction and the complete inherited stack in separate processes concurrently. All failures propagate; retain separate logs and command timing records.

Only v16.36 producer test-fixture generation may be reused, within one test process and keyed by bound. Deep-copy each returned fixture before mutation; cache no verifier result, accepted verdict, scientific output from another phase, or completed test. Instrument producer and verifier calls; emit exact test identities/outcomes and canonical fixture hashes. Baseline and optimized v16.36 executions run on the same GitHub runner with identical instrumentation. Compare every test identity/outcome and every fixture digest. Do not assert a speedup unless measured; report single-run timing limitations and full-phase concurrency overhead.

Each optimized phase independently runs all28 current scientific controls and261 inherited tests, plus new infrastructure controls, and freshly re-enumerates the entire v16.39 scientific domain. Require the three scientific files to equal the committed parent bytes. Preserve historical RED evidence. Baseline benchmarking is performed once in science; fresh publication and actual-merge replay repeat the optimized full checks without recycling fixtures across processes or phases.

Package full executed source/input files, logs, metrics, run/attempt/checkout/workflow metadata and checksums. Publication verifies API artifact digest/CRC, source identity, exact member sets and fresh scientific byte equality before committing durable evidence. Actual-merge replay verifies that publication and emits an artifact. Automate deterministic integrity checks and receipt creation; root independently inspects downloaded artifacts before declaring closure. Preserve failed runs, including initial infrastructure regression RED.

Acceptance: unchanged exact test outcomes/fixture bytes/scientific bytes; explicit non-cached independent verifier calls; preflight rejects corruption; parallel failures fail closed; all three phases pass; exact verified-head merge and actual-merge audit. Report measured performance without turning a noisy single-run comparison into a general guarantee.
