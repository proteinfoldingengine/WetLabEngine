# C3 shared-witness verification contract — prospective
Status: frozen verification domain; no computational acceptance or closeout.
Parent: edad36f7002f76bbc1d206a7d1ebd4f1c2a8ae9f.
Scope: 6b38dddb62b34ced1098c88f214b0190b2ebec7c.
Proof: 1c5d58a857a633854ab7485e9a0d0cf409f333c5.

Primary universe is exactly four occupancy states 00,01,10,11 and commands +1,-1,+2,-2. Include every rejection self-outcome, including malformed membership requests, plus each actual syntactically valid toggle whose successor obeys floors 2 and hitting band [3,4]. Analytically expected: 16 self-outcomes and 8 toggles, total 24. Locked x=1/root2-only restriction: two states and six outcomes. These expected counts and tau=4-xy are known deductions, not blinded predictions.

Producer will compute hitting numbers by exhaustive subsets of the nine-label carrier. Independent verifier will compute them by unions of one root representative per root, reconstructing state/command identities separately without importing producer. Compare entire canonical objects including identities, types, metadata, fibers, controls and claims; counts alone are insufficient.

Mandatory rejecting controls: missing, duplicated and substituted state/outcome rows; wrong hitting number (including bool/int confusion); duplicate JSON keys; false provenance; false guaranteed-progress or physical-access claims; premature decoder, silent anchor edit, invisible anchor cleanup, all-rejection path, one-root spectator, and tau-omitted observation. Published tests currently fail because verifier is absent; preserve red.log as initial tests-first evidence. That local shell pipeline printed failures, and its final tail exit code is not a successful test verdict.

Resources: standard-library Python, exact finite enumeration; each producer subprocess capped at 30 seconds; Actions job cap 15 minutes. Stop on any primary identity discrepancy or rejected control that is accepted. No exploratory domain expansion. Repeat only after substantive repair or bounded transient infrastructure retry.

Inherited core/A12 checks are compatibility diagnostics, not the full v16 certification stack. The four-state exhaustive result checks this frozen model only. The analytical arbitrary finite-cycle argument remains a mathematical proof obligation. Exact tau observation and the frozen anchor remain declared assumptions, with no physical observer derivation.

After passing verification: independent adversarial mathematical review of frozen proof and actual evidence, author's reconciliation, separate publication/provenance audit, durable original artifacts, final scoped closeout/index and immutable readback. No CLOSED claim before that sequence.
