# V997 Protocol

## Objective

Demonstrate that visible-state equivalence underdetermines legitimate history.

## Procedure

1. Construct five histories.
2. Force all histories to converge to the same visible final state.
3. Certify once with visible-state-only acceptance.
4. Certify again with Genesis Pin acceptance.
5. Report which paths pass or fail and why.

## Histories

1. Legitimate history
2. Forked counterfeit
3. Self-defined counterfeit
4. Quorum-failed replay
5. Tampered append chain

## Pass Condition

The audit passes if:

- all histories are accepted without Genesis Pin,
- only the legitimate history is accepted with Genesis Pin,
- every rejected path has a specific rejection reason.
