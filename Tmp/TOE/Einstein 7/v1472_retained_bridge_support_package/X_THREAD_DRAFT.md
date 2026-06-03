# X Thread Draft — V1472 Retained Bridge Update

1/
Research update on the Retained Bridge:

The prior claim was simple:

Geometry cannot validate itself.

Since then, we tested that claim against real recovery traces.

2/
UCI 498 showed a strong pruning-order recoverability signal, but missed full holdout certification.

We kept it as a near-miss, not a win.

3/
BPI2014 initially looked like a pass, but the full null suite broke it.

Topology alone could be fooled by:

- entropy reversal
- repair before damage

That mattered.

4/
So we restored the missing admissibility rules:

- valid sequence
- valid provenance
- valid entropy arrow
- damage before repair
- closure downstream of retained history

5/
After that, BPI2014 passed the full adversarial suite:

real trace: M ≈ 0.875
8 adversarial nulls: all failed

6/
The lesson:

Static topology can fake shape.
It cannot fake valid history.

Geometry is not the proof.
Geometry is the exhaust.

7/
The bit comes first.
Then admissible history.
Then retained structure.
Then geometry.

8/
This is not a claim of GR, ADM, spacetime, or physical curvature.

It is narrower and cleaner:

order-dependent recoverability traces carry geometry-like closure signals that adversarial spatial counterfeits cannot reproduce.
