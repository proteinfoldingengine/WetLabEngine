# Peer review round 2 — review of `AUTHOR_RESPONSE.md`

**Scope.** This review reads the author response against the first referee report and checks it against the executable artifact and public claim files.

## Overall

**Accept the letter. Do not accept the artifact as revised.**

The response is a real author reply: it is scoped to the six-qubit artifact, it does not raise claims, and it accepts the referee report on every load-bearing point. The authors correctly promote the homogeneity obstruction, demote the dashboard, and write a go/no-go rule for RGCL. That is what a competent reply looks like.

However, the executable package and its front page have not yet been brought into line with the letter. The public README still leads with “Full-Stack Gravity Progress Simulation” and “metric-affine/ADM-like structure.” The response should therefore be treated as binding and the not-yet-updated README as stale.

## What the response gets right

The author response accepts all seven major comments without hedging.

The displayed homogeneity lemma is the correct central result: the graph, incidence matrix `B`, cycle basis, and state-point geometry have weight zero; the source tangents and selected current have weight one; therefore the construction selects only the projective class `[Sigma]`.

It also correctly states that the `~10^-16` projective-drift number is an implementation check rather than evidence for the theorem.

Other clean concessions in the response:

- `D=-4.5` and `D=2` are algebraic identities / implementation controls;
- there is no map from the vertex-local `q_i` to a spatial three-metric;
- there is no discrete diffeomorphism action;
- there is no lapse, shift, Hamiltonian constraint, momentum/diffeomorphism constraint, or ADM constraint algebra in the demo;
- the selected graph current `J` is not `T_{mu nu}`;
- the “spatial-stress” distance is generated from two hand-declared 3x3 matrices and is not a derived stress-tensor completion;
- `max theta_C = pi` remains unadjudicated;
- the frequency with which the closest unconstrained orthogonal factor would have determinant `-1` is not reported;
- product-state, classical-mixture, chain, and beta-limit controls have not yet been run;
- there is no third-party physical observable that currently falsifies the pipeline as a gravity model;
- a free dimensionful multiplier is operationally equivalent to inserting a coupling such as `G`;
- the proposed public abstract is appropriately conservative.

The Q20–Q21 commitments are particularly important. If the next gate only inserts a scale, the authors say they will classify it as an added calibration rather than a derivation and will not invent another missing-law name. That is the correct stop condition.

## Remaining scientific nits

These do not reopen the gravity claim. They make the obstruction lemma precise.

### 1. Weight-zero geometry is a fixed-state statement

The homogeneity lemma freezes `K`, `O`, and `M` while rescaling the already-computed tangent data `(s,y)`. That is the correct statement.

If instead one rescales the generator `P` at fixed `lambda`, or changes `lambda`, the state changes and so generally do `K`, `O`, and `M`.

The revision should retain an explicit sentence that the obstruction is homogeneity of the **selection rules at a fixed state / tangent point**, not invariance of the full `rho_lambda` dashboard under arbitrary source rescaling.

### 2. The failure criterion is too conjunctive

The response currently treats failure as requiring both a no-go and that every repair reduces to a free scale. Either is already sufficient to defeat a **target-blind derivation**.

Prefer the disjunctive criterion:

> The target-blind source-to-geometry derivation fails if either (a) a no-go theorem rules out the required pairing in the frozen ontology, or (b) every successful repair introduces only an externally free coupling scale.

The current conjunction leaves room for a vaguely specified new pairing to linger indefinitely.

### 3. `Z` is overloaded

In the homogeneity lemma, `Z` denotes the cycle basis. Elsewhere `Z` denotes the Pauli operator. This is harmless in code but should be cleaned up in a paper.

### 4. BKM motivation is acceptable, but downstream objects are metric-dependent

The response correctly does not claim uniqueness of BKM. That distinction should remain explicit:

- `K`, `M`, and represented `q` depend on the chosen Petz/BKM metric;
- the projective homogeneity obstruction does not depend on that particular metric choice.

### 5. Q14 remains the live research question

The authors correctly admit that they have not exhaustively ruled out nonlinear functionals of `{K_i,O_ij}`.

Therefore v13.28 should not be framed as “derive RGCL.” It should be framed as:

> Search a named class of target-blind source-to-geometry pairings and adjudicate each as derived, obstructed, or requiring a new axiom.

That is a materially stronger research protocol.

## What is not yet done

The author response is stronger than the public artifact framing. The README still contains phrases such as:

- “Full-Stack Gravity Progress Simulation”;
- “quantum -> ... -> metric-affine/ADM-like structure”;
- language that RGCL “must fix” the coupling, which can read as a scheduled derivation rather than the name of an unresolved object.

The response explicitly says no fingerprint or scientific output changed. Therefore the revision checklist is still a promise rather than an executed patch.

For the response letter to count as an implemented revision, the minimum patch is:

1. Rename the public README title to the methods / obstruction title already proposed by the authors.
2. Remove “ADM-like sector” from the README, figure/panel labels, and `X_UPDATE.md`.
3. Put the homogeneity lemma before the fingerprint / numerical table.
4. Relabel the stress-completion calculation as a **toy block-underdetermination control** in machine-readable and ledger text.
5. Add audits for the raw unconstrained polar determinant and for the pre-clip holonomy trace/angle argument.

The following can remain revision-requested rather than reject-level:

- a deliberately nonhomogeneous counter-control showing how an added rule would break the scale symmetry;
- product-state / classical-mixture / simple-chain controls;
- a beta sweep and broader source-support sweep.

Those controls would make the obstruction read more clearly as a theorem embedded in a methods note rather than as an algebraic remark illustrated by one dashboard.

## Referee disposition

| Item | Disposition |
|---|---|
| Homogeneity lemma | **Accept as the result** |
| Relabeling of DeWitt / current / holonomy / graph | **Accept in the response** |
| RGCL go/no-go and “free scale = inserted coupling” | **Accept** |
| Public abstract | **Accept** |
| Claim upgrade | **None attempted — good** |
| Artifact as currently published | **Still needs promised rescope** |
| Gravity / Einstein closure | **Remains open** |

**Decision on the reply:** satisfactory.  
**Decision on the demo:** not yet ready for a journal-facing methods note until the README and labels match the letter.

If the label changes and the two inexpensive audits (raw `det O` and pre-clip holonomy) are shipped, the remaining controls can be treated as ordinary revision requests rather than rejection-level issues.

The science of this artifact is the obstruction lemma now written down. Everything else is methods context and packaging.
