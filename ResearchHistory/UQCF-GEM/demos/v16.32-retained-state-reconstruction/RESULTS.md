# v16.32 — Retained-state reconstruction / information-loss closure

## Adjudicated result: NONINJECTIVE

The complete value-level closure data earned through v16.31 do **not** reconstruct the underlying indexed retained cover state.

The smallest exact witness found uses only three vertices and two indexed views. Let the tree be a root 0 with children 1 and 2.

State L:
- view 0 = {0}
- view 1 = {0,1,2}

State R:
- view 0 = {0,1}
- view 1 = {0,1,2}

Both are legal states in the same endpoint interval, with the same union. They are distinct retained covers. But in both states view 1 alone covers both root children, so

    tau = (1,0,0)
    h = 1

and the declared v16.31 value-level component signature is identical:

    component_values = ((0,1),)

The independent verifier reconstructs both states, their legality, common interval, tau, h and signature from the raw parent array and views. It rejects fabricated or cross-interval collisions.

## General argument

The collision is not accidental. Minimum-cover cardinalities forget redundant incidence identity. If another view already supplies every minimum cover affected by a labeled incidence, adding or removing that redundant incidence can leave every tau_v unchanged. Since h is a function of tau and the normalized component values reconstruct those same local values, the complete frozen value-level signature remains unchanged.

Therefore no inverse from this signature to the indexed retained cover can exist on the full admitted category.

## Bounded audit

All same-union endpoint intervals on rooted unordered trees through four vertices, with up to four distinct initial views and at most five removed events under the implementation limits, were searched.

- endpoint intervals: **4,397**
- legal state occurrences: **36,178**
- excess state occurrences inside tau-signature collision classes: **28,937**
- excess state occurrences inside the complete frozen value-level signature classes: **28,937**
- verdict: **NONINJECTIVE**
- canonical digest: `39b5e537a5e59e26cc4c77f65a93228c87ef03d52e5409d57f0631aa119afade`

These counts are implementation evidence; the universal noninjectivity claim needs only the explicit admissible counterexample above.

## What information is missing?

The witness differs only in whether the labeled incidence (view 0,node 1) is retained. That incidence is redundant for all minimum-cover values.

The full labeled view-node incidence relation would reconstruct the state, but supplying it is equivalent to supplying the object being reconstructed. Doing so would make injectivity tautological and is therefore **not** adopted as a new closure invariant.

The exact missing information is:

**redundant labeled retained-incidence identity not represented by minimum-cover/component values.**

This is a mathematical information boundary. It does not establish physical information destruction, quantum loss, geometry, or time.

## Evidence

- Preregistered wiring RED: run **36649682306**.
- Provisional search/GREEN: run **36651291089**, execution SHA `fbe644e31ab92713b5449e788a435c97936a8241`; current tests, exact witness verification, and inherited v16.31–v16.29 regressions passed.
- The producer searched 4,397 intervals / 36,178 states and returned the collision counts above.
- The verifier does not accept state/deletion masks as signature fields and reconstructs the published collision directly.

Review is self-review. No independent authorship or proof-assistant formalization is claimed.

**Time is pruning / ordered recoverability update.**
