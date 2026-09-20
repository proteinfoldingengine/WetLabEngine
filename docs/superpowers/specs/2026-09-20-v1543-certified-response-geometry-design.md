# UQCF-GEM v15.43 — Certified transport applied to response geometry

**Date:** 2026-09-20

**Status:** written specification awaiting review; no implementation or response-curvature measurement performed

**Parent:** `0f426fa28d22871ce042e39bf9704695ede8b336` (v15.42, PR #53)

**Parent verdict:** `TRANSPORT_PROTOCOL_CERTIFIED`

**Pillar 3:** `OPEN`

## 1. Approved intent and the question

The next approved direction is `APPLY_CERTIFIED_TRANSPORT_TO_RESPONSE_GEOMETRY_WITHOUT_SOURCE_ADJUDICATION`.
This specification makes that direction concrete:

> Do the frozen global-balance response fields yield nonzero, presentation-covariant linearized holonomy when passed through the already certified transport rule on their canonical operational response geometry?

The intended outcome is a reproducible finite mathematical classification. Neither a nonzero result nor a null result may select a new connection, stencil, orientation, normalization, field lift, or response family. No source-correspondence verdict is permitted.

This is an atemporal calculation. The formal perturbation parameter is a derivative parameter; no physical time, entropy, pruning dynamics, pre-existing spacetime, or external embedding is introduced. Deriving emergent ordering or spacetime remains an open research objective.

## 2. Approach and alternatives

**Selected:** freeze the v15.42 core, build the canonical carrier from the inherited response-work geometry, and apply the inherited scalar response fields without fitting. Keep acquisition separate from mathematical construction. This isolates whether the certified protocol actually carries response curvature.

**Deferred:** construct a separate operational carrier for each control family. That would combine a carrier-identifiability comparison with this transport-application question. Here every control field is evaluated on the same canonical carrier, and that limitation must appear beside every control result.

**Rejected for this stage:** introduce a signed scalar contraction and compare it with a source target. Such a contraction requires its own identification argument. Nonzero matrix holonomy alone cannot select it or establish physical gravity.

L5 and L7 are the declared finite sizes. L7 is a held-out size for this application, evaluated with an unchanged rule after L5. L9/L11, continuum extrapolation, and general-size claims are outside this stage. No favorable result may widen the claim retrospectively.

## 3. Frozen authority

All paths below are relative to `ResearchHistory/UQCF-GEM/demos/` unless otherwise stated. The full parent commit pins the dependency closure; the implementation plan must enumerate every executable inherited dependency before execution.

| Artifact | Git blob |
| --- | --- |
| v15.42 `docs/RESULTS.json` | `f8f85ab8c8b4599e31bebf3d2fcb668e84ffb5df` |
| v15.42 `transport.py` | `df552284c16d43bc876340fbc13fe91eb9ee6a00` |
| v15.42 `holonomy.py` | `bad3f06b291bb448a903b4f48344a9e54a633f68` |
| v15.42 `protocol_types.py` | `e90a98d17baa6028f0d50a165f0b9d0046de13a2` |
| v15.42 `exact_algebra.py` | `c67ea42b61321469f7735ce589f2e729b241666a` |
| v15.42 `operational_complex.py` | `8163beba8e52bc2a3a6d0c8cf59dd1257222f65c` |
| v15.40 `response_generation.py` | `afd5a68ce74f7f80f49b6fd6307ebb0681182bf5` |
| v15.40 `response_geometry.py` | `9128c24b695c1b539ac60dc93aeaf0bd4795c57b` |
| v15.40 `docs/RESULTS.json` | `c56ca48110b3341e2d68289be717bf1e5308a20a` |

The versioned directories are `v15.42-duality-covariant-transport-repair` and `v15.40-global-balance-geometry-specificity`.
The v15.42 design remains blob `91f2c66bea982b3180a07c61ccc4bef76e9c031d`.
The original v15.41 design, erratum, and corrected ledger remain respectively `6d35aae0ccb6c2584d26d5a83d522b3cc7036728`, `d40d03d9d2498ce54839b15dad00c1505c1a586a`, and `46cae26d91c709fdde4c5cc39cd3cf3908980e97`.

Parent certification evidence is GitHub run `35519390489`, job `106100727467`: 48 v15.42 plus 43 inherited tests, both canonical replays, compilation, and additive scope passed at the exact parent head. A future execution must verify pinned bytes and its ancestor, not infer certification from a mutable branch name.

## 4. Input acquisition and honest separation

The existing v15.41 `response_inputs.py` is not the application interface: its records expose sources, and its module exposes a source-target helper. Do not import that wrapper or the v15.41 connection gate into the new evaluator.

Use two separate processes with an explicit serialized boundary:

1. **Frozen acquisition process.** Invoke only the pinned v15.40 response generator and response-geometry constructor, together with their reviewed dependency closure. Generate the five inherited response families. Construct work and neighbors only for `GLOBAL_BALANCE_COMPLETION`. Existing source arrays are allowed inside this process because the inherited response and work definitions require them. Their use is provenance, not a newly evaluated correspondence test. Do not invoke `generation_audit`, `geometry_specificity_gate`, `incidence_target`, v15.41 `source_target`, or any source/curvature comparison. Hash-only verification of historical ledgers does not authorize querying target results.
2. **Application process.** Read only a validated projection: carrier labels, canonical exact work matrix, canonical neighbor pairs, and exact response vectors. Source vectors, signed incidence support, source-target outputs, fitted coefficients, coordinates, and historical curvature outputs must not cross this boundary. Family names and response-index labels belong to the runner's metadata; the transport constructor receives only its original typed operational inputs and one scalar vector.

The acquisition output must contain a deterministic provenance manifest: parent SHA, dependency path/blob pairs, labels and ordering, family identifiers, sizes, scales, and hashes of each projected payload. It must reproduce byte for byte. Reject unknown fields, malformed dimensions, duplicate or missing labels, noncanonical rational strings, booleans, floats, and incomplete case coverage before construction. Do not deserialize executable objects.

The entire pipeline is **not source-free**: inherited acquisition uses source axioms and source arrays. The accurate claim is that the certified transport and curvature evaluator do not query source targets or source arrays. Report acquisition permissions and evaluator prohibitions separately; static checks are not runtime telemetry or a hostile-interpreter sandbox.

## 5. Carrier, scalar lift, and scales

At each size, acquire the canonical unit-scale work matrix and neighbors by the unchanged v15.40 definition. Construct the operational complex and its flat baseline with the unchanged v15.42 substrate. Never substitute the manufactured torus fixture if this construction fails. Require unique identification, tangent rank two, the certified D4 direction structure, and flat baseline; retain all structural audit facts and the first failure reason.

For each inherited response vector indexed by r, use exactly

```text
u(x) = response[r][position_of_x]
h(x) = u(x) g0(x)
```

Check its inherited zero sum exactly. Do not recenter, normalize, change sign, divide by a measured amplitude, smooth, or otherwise repair a field. Unit edge frames are the existing v15.42 convention. The scalar normalization of response work does not introduce a fitted length or an additional curvature normalization.

Scales are exactly `1` and `7/3`. Obtain both from the frozen acquisition functions, require `W_scaled = (7/3) W_unit`, unchanged canonical neighbors, and `u_scaled = (7/3) u_unit`. Reconstruct and validate the scaled operational carrier; relate presentations by the existing operational identification, never by fitting matrices to curvature. The required transport and curvature relations are linear, and the quadratic invariant scales by `49/9`.

## 6. Exhaustive declared cases

Sizes: `5`, `7`. Families, in frozen order:

1. `GLOBAL_BALANCE_COMPLETION`
2. `DIRECT_INHERITANCE`
3. `ONE_INCIDENCE_TRANSPORT`
4. `MATCHED_DIAGONAL_BALANCE`
5. `MATCHED_STEP2_BALANCE`

Evaluate every response index at each size and both scales: `5 * (25 + 49) * 2 = 740` base cases. Evaluate every operational face in every case. All families use the canonical global-balance carrier; no control field gets a different connection or its own work geometry in this stage. Control outcomes cannot choose the primary family, alter its pass condition, or establish specificity against alternative geometries.

Presentation checks cover the inherited bijection `pi(i) = (2*i+1) mod L^2`, transporting labels, vector components, response indices, work entries, and neighbor pairs together; all four base points and both orientations of every face; tangent/cotangent duality; and local D4 covariance. Use the v15.42 local structural identities plus all eight single-site D4 actions and a predetermined simultaneous mixed assignment (sorted-label position modulo eight in lexicographically sorted D4 actions). Do not claim enumeration of all simultaneous gauge assignments. The plan must assign these checks to cached immutable data without skipping a declared identity or selecting cases after output.

## 7. Frozen mathematics and recorded observables

Call the certified transport and holonomy implementations byte-identically, in an isolated module namespace. Do not rewrite their formulas or run the v15.41 closure ansatz. Reuse or vendor the dependency closure only with verified byte equality. Its original manufactured-control firewall stays unchanged; application access is outside that module boundary.

Record the full based endomorphism `K_C = delta H_C` for every canonical face presentation, its exact zero/nonzero predicate, and the already certified invariant `kappa_C^2 = -tr(K_C^2)/2`. Validate the expected metric-skew identity and nonnegative invariant exactly. Compute holonomy from edge products, not a shortcut Laplacian of the response. Cross-check the product derivative with the independent four-term expansion used by the certified tests.

Derived summaries are fixed: per-case face count, zero/nonzero counts, exact invariant histogram, and exact sum of invariants. Store full per-case matrices and invariants in deterministic rational JSON; no lossy compression or representative-only substitution for the 740 base cases. Presentation-equivalent outputs may be summarized by exact comparison receipts, with their counts and transformation rules retained.

No signed scalar contraction, source-shaped support statistic, source-target correlation, fitted slope, radial law, spectral comparison, physical unit conversion, or post-output threshold is allowed.

## 8. Gate order, controls, and failures

1. Verify parent ancestry, every pinned dependency and historical artifact, and the certified parent verdict.
2. Replay the unchanged v15.42 source-blind certification before acquiring response inputs. Failure stops acquisition.
3. Acquire and validate projected inputs and provenance in the separated processes.
4. Identify canonical unit and scaled operational carriers and flat baselines for L5, then L7; failure stops curvature evaluation for that size and makes the overall application invalid.
5. On each actual response-derived carrier, verify constant fields `0` and `7/3` give zero transport and curvature, and run every-root unit-impulse controls with the v15.42 frozen histograms. This checks that application carriers satisfy the protocol's operational prerequisites; manufactured fixtures cannot stand in for them.
6. Evaluate the 740 declared response cases and presentation checks; verify exact amplitude covariance, additive-constant invariance, and superposition using coefficients `2/3` and `-5/7` on response indices 0 and 1 for every family and size. Additional gauge-offset fields are controls, not replacements for primary inputs.
7. Emit a canonical ledger only after complete coverage. On failure emit a failure ledger with first failed gate, case, error category, completed counts, and all unfinished results null. No partial success verdict and no repair after observing curvature.

Every exact failure, malformed input, exception, unavailable dependency, or missing case is an application failure. A failure of application does not retroactively change the preserved v15.42 certification or the v15.41 erratum.

## 9. Mechanical outcome mapping

Classify each canonical-family response case as `FLAT` if every face matrix is exactly zero, otherwise `NONFLAT`. The global result uses all 148 canonical-family cases, including both scales:

| Condition | Status | Next required object |
| --- | --- | --- |
| Any required gate fails or coverage is incomplete | `RESPONSE_APPLICATION_INVALID` | `REPAIR_APPLICATION_WITHOUT_RETUNING_TRANSPORT` |
| All canonical cases are flat | `CANONICAL_RESPONSE_CURVATURE_NULL` | `CHARACTERIZE_CERTIFIED_TRANSPORT_KERNEL` |
| Every canonical case is nonflat | `CANONICAL_RESPONSE_CURVATURE_NONZERO` | `PREREGISTER_INTRINSIC_CURVATURE_INTERPRETATION_WITHOUT_SOURCE_FITTING` |
| Gates pass but canonical cases mix flat and nonflat | `CANONICAL_RESPONSE_CURVATURE_MIXED` | `CHARACTERIZE_FINITE_SIZE_OR_RESPONSE_DEPENDENCE` |

Control-family classifications and exact histograms are descriptive, never success prerequisites. Mixed outcomes are retained rather than resolved by discarding a size or response index. No numeric response-curvature values have been measured or preregistered as expected successes in this design.

## 10. Evidence and validation contract

The later implementation plan must specify behavior-first failure tests for pin drift, malformed projections, forbidden evaluator imports/I/O, missing cases, input-order mismatch, scalar relabeling, wrong scale, convention drift, and each first-failure gate. Test the acquisition/evaluator boundary, including rejection of injected source/target fields, and verify that changing inaccessible source metadata cannot change evaluator output with projected inputs held fixed.

Retain the 91 inherited tests and both byte-identical v15.41/v15.42 replays. Add a dedicated, manually dispatchable or narrowly path-filtered v15.43 workflow at the exact triggering SHA. Declare the runtime environment and dependency pins in the plan. Run one official certification after local verification, then a final exact-head run only if a committed receipt changes the head; keep later receipts in PR metadata to avoid a self-referential loop. Do not repeatedly run whole suites for documentation review.

The result ledger must contain input and code pins, manifest, complete case records, gate/control receipts and counts, per-family descriptive classifications, canonical outcome, and explicit claim fields. Canonical serialization uses sorted JSON keys, two-space indentation, canonical Fraction strings and a trailing newline; `--check` must fail on byte mismatch or invalid status.

## 11. Scientific boundary and delivery sequence

The strongest permitted successful statement is that inherited exact response fields produce nonzero operational linearized holonomy under one previously certified rule on the declared finite carriers. This remains conditional on inherited source/response axioms and the isotropic scalar lift. It does not derive those axioms from the foundational ontology.

In every outcome, source correspondence is `NOT_EVALUATED`; physical metric, physical curvature, stress-energy, Einstein equations, continuum limit, spacetime, physical gravity, and scientific breakthrough claims remain false. Pillar 3 remains `OPEN`; no pillar completion is inferred from this application. No fundamental time or dark-matter primitive is introduced.

This deliverable is one additive written specification on a branch based at the exact certified parent. Keep parent PR #53 unchanged and unmerged; publish this design in a separate draft PR targeting that branch. No implementation files, generated response-curvature artifacts, workflows, or historical documents change at this step.

After written-spec approval, write the implementation plan. After plan approval and execution-method selection, implement and certify the specified application. The proposed future directory is `ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/`; this specification does not create it.
