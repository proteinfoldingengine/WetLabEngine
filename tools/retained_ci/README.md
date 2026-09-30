# Retained execution reference pipeline

This approved infrastructure campaign validates a faster execution layer against the closed v16.39 program. It is not a new scientific stage. Historical scientific files and test bodies stay unchanged.

Commands (scientific execution belongs on GitHub):

- `python tools/retained_ci/run.py preflight out/preflight`: infrastructure controls, frozen-parent anchors, current scientific rejecting controls and durable-publication verification.
- `python tools/retained_ci/run.py phase out/science --benchmark`: paired same-runner v16.36 fixture benchmark, then full scientific reconstruction and inherited stack in two isolated processes.
- `python tools/retained_ci/run.py phase out/reproduction`: fresh full replay with new process-local fixtures and uncached verifier calls.
- `python tools/retained_ci/publish.py receipt RUN_ID out/receipt PR_NUMBER`: verify downloaded actual-merge artifact, exact PR/merge/workflow identity and durable bytes; assemble a hash-bound receipt. The workflow runs this automatically after successful post-merge verification and commits the receipt on a separate branch.

The source uses explicit parent, stage and inherited-count bindings. A future scientific stage must update those bindings under its own prospective registration; do not silently point this campaign at a different universe. Reuse the fixture-isolation, parallel-process and integrity helpers, not a prior stage's successful verdict or computed science. Only producer test inputs are reused inside the v16.36 test process. Verifier calls and all three scientific executions remain fresh.

Performance reports distinguish baseline and concurrent timings and record the source, runner, test identities, fixture bytes, producer generations and verifier calls. Timing comparisons are single-run observations. Fewer repeated fixture generations is deterministic; a universal wall-clock speedup is not claimed.
