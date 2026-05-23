# V997 Genesis Pin Publication Audit

## Executive Summary

This full-stack audit tests whether same observable state is sufficient to certify legitimate history in the V923 → V995 recoverability stack.

It is not sufficient.

All five histories converge to the same final observable state. Under visible-state-only certification, all five are accepted. Under Genesis Pin certification, only one is accepted.

```text
Histories tested: 5
Accepted without Genesis Pin: 5
Accepted with Genesis Pin: 1
```

## Core Result

Same observable state does not certify legitimate history in the tested recoverability stack.

Genesis Pin changes the certification object:

```text
from: final-state equivalence
to: recoverable-history legitimacy
```

## Genesis Pin Requirements

A path is accepted only if it satisfies:

1. same visible state,
2. pinned genesis registry,
3. pinned genesis anchor root,
4. witness quorum,
5. append-only chain continuity,
6. no circular bootstrap/self-defined origin.

## V923 / V994 / V995 Layer Stack

| layer   | name                           | role                                                         | audit_test                                                   | failure_without_pin                                                |
|:--------|:-------------------------------|:-------------------------------------------------------------|:-------------------------------------------------------------|:-------------------------------------------------------------------|
| V923    | Observable-state insufficiency | Visible equality is not legitimacy.                          | All histories converge to same final observable coordinate.  | All paths accepted under visible-state equivalence.                |
| V994    | Bootstrap/circularity boundary | Prevent self-defined legitimacy.                             | Reject self-defined registry/root.                           | Attacker can define its own registry and root.                     |
| V995    | Recoverable-history legitimacy | Legitimacy requires rooted continuity, not just final state. | Require pinned root, quorum, append-only chain.              | Forks, replays, and tampered chains can end at same visible state. |
| V997    | Genesis Pin publication audit  | Merge audit engine with publication package.                 | Five histories; 5 accepted without pin, 1 accepted with pin. | Visible-state-only certification is underdetermined.               |

## Certification Table

| history                  | same_visible_state   | genesis_registry_matches   | genesis_root_matches   | witness_quorum_all_steps   | append_only_chain_valid   | circular_bootstrap_detected   | accepted_without_genesis_pin   | accepted_with_genesis_pin   | reason                                                                |
|:-------------------------|:---------------------|:---------------------------|:-----------------------|:---------------------------|:--------------------------|:------------------------------|:-------------------------------|:----------------------------|:----------------------------------------------------------------------|
| Legitimate history       | True                 | True                       | True                   | True                       | True                      | False                         | True                           | True                        | accepted: visible state + pinned genesis + quorum + append-only chain |
| Forked counterfeit       | True                 | True                       | False                  | True                       | True                      | True                          | True                           | False                       | rejected: wrong genesis anchor root                                   |
| Self-defined counterfeit | True                 | False                      | False                  | False                      | True                      | True                          | True                           | False                       | rejected: self-defined registry and self-defined root                 |
| Quorum-failed replay     | True                 | True                       | True                   | False                      | True                      | False                         | True                           | False                       | rejected: witness quorum failed                                       |
| Tampered append chain    | True                 | True                       | True                   | True                       | False                     | False                         | True                           | False                       | rejected: append-only chain failed                                    |

## Interpretation

The audit demonstrates a modeled counterexample to visible-state-only legitimacy.

Five histories land on the same visible state. They are observationally equivalent at the final coordinate. But their generative histories are not equivalent.

The Genesis Pin separates legitimate continuity from:

- forked anchors,
- self-defined registries,
- quorum-failed replays,
- tampered append chains.

## Claim Boundary

This is a modeled full-stack audit demonstration.

It does not claim universal theorem status, production cryptographic security, physical spacetime, physical time, General Relativity, Einstein equations, or physical curvature.

## Correct Public Claim

Same observable state is insufficient for legitimacy in the tested recoverability stack; legitimacy requires recoverable history anchored to pinned genesis.
