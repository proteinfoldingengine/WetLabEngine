# Matched-input response: exact graph null and higher-correlation witness

**Baseline:** `72a3e4bec8c0ad906a6a01819543602529e106d4`.
**Status:** bounded continuation after the pruning-consistency correction.
**Arithmetic:** rational throughout; no fits, floating tolerances, or time evolution.

## Result and scope

Two deliberately separate experiments were executed. The corrected scalar
lineage response has **no endpoint response dependence on pruning order** in
four unchanged fixtures. Independently, an archived higher-correlation example
has **different source-response ratios despite identical proper marginals**.
The latter is a reproduced quantum-state/commuting-probability result, not a
new gravitational signal and not a derivation of a repair-history source law.

The observables are held fixed *within each matched experiment*. The quantum
susceptibility is not asserted to be the same object as the lineage scalar
potential. There is no fitted conversion or hidden connection between them.

## 1. Graph arm: changing order is not itself an extra response law

Use the four existing `pruning_consistency_audit.CASES`, the same initial and
final carriers, and the same extensive source pushforward. For each pair,
construct two different lawful sequences by removing available discarded
leaves in ascending versus descending address order. These ordering rules
are controls only; neither is promoted to a physical pruning rule.

Center the source once at the fine level and transport that actual forcing:

`J_c = P C_f J`.

The observable remains potential restricted to retained vertices, modulo a
constant. No fiber averages or freshly uniform coarse source background are
substituted. At the **all-source operator level**, compare direct and staged
source pushforwards, direct and staged restrictions, and final responses.

| Frozen case | Different lawful orders | Source composition residual | Restriction composition residual | Final response difference |
|---|---|---:|---:|---:|
| 1 | Yes | 0 | 0 | 0 |
| 2 | Yes | 0 | 0 | 0 |
| 3 | Yes | 0 | 0 | 0 |
| 4 | Yes | 0 | 0 | 0 |

The explanation is the existing exact identity `C_c S G_f = G_c P C_f`
together with composition of ancestral retractions and restrictions. A
history record can distinguish the paths without changing this endpoint
observable. This is not a test of every possible repair dynamics; it is the
null required before claiming an extra history-sensitive response.

## 2. Higher-correlation arm: the archived v13.13 witness

The source is not invented here. The earlier report explicitly supplies the
normalized exponential source family

`rho_s = exp(log(rho) + s P) / Tr exp(log(rho) + s P)`.

For commuting states and observables, direct differentiation gives

`d_s E[O] at s=0 = E[OP] - E[O]E[P]`.

Here `s` is a source-deformation parameter, not physical time. The test fixes
`epsilon = 1/5` from the archived witness and uses

`rho_+/- = 2^(-N) (I +/- epsilon Z_1 ... Z_N)`, with `N=k+1`.

The states are faithful: all their diagonal eigenvalues are
`(1 +/- epsilon)/2^N`, hence positive. Every proper marginal is exactly
maximally mixed. Tracing out even one site kills the parity term.

Choose **the same** source generator `P=Z_N` and **the same ordered pair**
of observables in both states:

`(O, P) = (Z_1 ... Z_k, Z_N)`.

Their first source-response vectors are

`v_+ = (epsilon, 1)` and `v_- = (-epsilon, 1)`.

In the three-site case, all one- and two-site marginal data agree, but the
pair-observable susceptibility is `+1/5` versus `-1/5`. The reference
susceptibility `d_s E[P]` is 1 for both states. Thus the difference cannot be
removed by a common source-amplitude convention:

`v_+[0]/v_+[1] = +1/5`, `v_-[0]/v_-[1] = -1/5`.

The exact determinant is `det(v_+,v_-)=2/5`, so the vectors are not collinear,
without selecting a geometric norm. This two-observable check is an added
amplitude-control diagnostic for the archived example, not a novelty claim.

For a predictor using only the common lower-marginal data and the same
source/observable, the first predicted coordinate must be a common value y.
Then `max(|y-epsilon|,|y+epsilon|) >= epsilon=1/5`. This is an exact
insufficiency witness, not an error measured on a trained predictor.

## 3. Exact execution and null controls

The executable constructs all rational probabilities and partial traces from
scratch; it does not read the historical `SUMMARY.json` as numerical truth.
This matters because the archived v13.13 `CHECKER.py` checks stored summary
fields rather than recomputing the state family.

The hierarchy was independently reproduced for `k=1..6` (`N=2..7`):

| k | Proper marginal pairs checked | Maximum difference | Absolute response determinant |
|---:|---:|---:|---:|
| 1 | 2 | 0 | 2/5 |
| 2 | 6 | 0 | 2/5 |
| 3 | 14 | 0 | 2/5 |
| 4 | 30 | 0 | 2/5 |
| 5 | 62 | 0 | 2/5 |
| 6 | 126 | 0 | 2/5 |

All **240 proper-marginal comparisons** are exact. Since the full states are
diagonal, their partial traces also have zero off-diagonal entries: this
checks the complete reduced density matrices, not merely selected Z moments.

Controls include source changes `P -> aP+bI` for three fixed positive a and
three fixed b, identity-source nulls, removal of hidden correlation, and site
permutations. Scaling rescales both response coordinates by a; b has no effect.
All reported control errors are exactly zero. Epsilon ablations at 1/10,
1/3, and 4/5 confirm that the response is computed from the input, not
hardcoded to 1/5. A nonsymmetric probability control tests covariance
centering and actual site-data permutation rather than only symmetric states.

Finite source deformations are checked at odds `u=1/4,1/2,1,2,4`, where
`u=exp(2s)`. Exact reweighting gives

`E_s[O] = +/- epsilon (u-1)/(u+1)`, `E_s[P]=(u-1)/(u+1)`.

These finite-tilt calculations independently verify the derivative formula
and normalization without finite-difference tolerances or matrix logarithms.

## 4. What was NOT earned

* The parity states are supplied completions; no repair/pruning process has
  been shown to generate them from the same initial state.
* The example is fully diagonal and also classical probability. It does not
  establish quantum-exclusive coherence, entanglement, or noncommutativity.
* The source law is the already supplied ETL/PGRL family. No Genesis-to-source
  selection, absolute observer calibration, or new source law was derived.
* No canonical map from these susceptibilities to the v15.56 lineage scalar
  Laplacian, its potential, physical curvature, or Einstein/ADM data is claimed.
* Matching all proper marginals does not match the full global state. The
  response difference is explained by that deliberately changed hidden state.

## 5. Verification and reproduction

Run in the demo directory:

```sh
python -m unittest -v test_pruning_consistency_audit test_matched_completion_response
python matched_completion_response.py
```

The new checker had a recorded local RED before implementation: one expected
availability assertion failure and 18 skipped tests. Its 19 initial tests
passed after implementation. Three additional review tests brought the new
suite to 22; together with the 15 exact baseline tests, **37 local tests pass**.
Three deliberate temporary mutations were caught: omitting covariance
centering, ignoring the hidden sign, and restoring the raw-source/background
mismatch. `MATCHED_COMPLETION_VALIDATION.json` records these receipts.

`MATCHED_COMPLETION_RESULTS.json` is recomputed and compared by the test suite.
GitHub CI additionally runs the complete historical v15.56 suite. Local
verification does not claim to have run unavailable historical modules.

## 6. Next scientific criterion

There is now a precise candidate beyond static graph/local-marginal data:
**hidden higher-order state information affects a supplied-source response**.
This is a result already present in v13.13, independently reconstructed and
separated from the corrected graph null here.

The next bridge must identify an existing, provenance-supported rule taking
this extra response information to an actual retained response observable.
The input/output spaces and source normalization must be stated before the
test. Changing the graph weights by hand or relabeling the quantum response
as curvature would not close that bridge.

## References and provenance

* Same repository, pinned baseline: `../../v13/v13.13/REPORT.md`, section 4,
  the commuting ETL/PGRL hierarchy witness; `../../v13/v13.13/CHECKER.py`,
  stored-summary validation scope.
* `../../v14/v14.03/REPORT.md`, sections 1-2: supplied support-source
  exponential family, tangent, and positive projective scaling. The report
  explicitly does not derive a Genesis-to-support-source selection map.
* `PRUNING_CONSISTENCY_AUDIT.md` and `pruning_consistency_audit.py`: unchanged
  exact graph baseline, blob `94d946dfc5fb5aa150834a807eb35c29b3133604`.
* F. Doerfler and F. Bullo, *Kron Reduction of Graphs with Applications to
  Electrical Networks*, IEEE TCAS-I 60(1), 150-163 (2013),
  DOI 10.1109/TCSI.2012.2215780, https://arxiv.org/abs/1102.2950 . Boundary
  elimination is established graph/network mathematics, not a novelty claim.
