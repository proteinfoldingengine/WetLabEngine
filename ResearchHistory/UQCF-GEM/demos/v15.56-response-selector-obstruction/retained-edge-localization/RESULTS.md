# v16.05 final report: retained-edge localization

**Completed 2026-09-28. Verdict: EXACT_RETAINED_EDGE_LOCALIZATION_CONFIRMED. All validity controls passed.**

D's cubic null is localized before the readout Hessian: its connected direction is exactly zero on the five selected edges, while its sixth-edge direction is nonzero. The earlier nonzero six-edge norm does not demonstrate a nonzero input to the five-edge Hessian.

## Scope and execution

The preregistration was committed at `c10168fd844f68a891fa63bbd041dcd9105d3b81` before measurement. Scientific execution head: `24315bf18eed287f174f9b8e1e033fad55ea48f0`. [Successful run 36482986412](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36482986412): all 12 candidate jobs and controls succeeded. The controls ran 6 new, 11 v16.04 and 9 v16.03 tests. Six additional publication-validator tests pass locally; these do not alter the measurement code or execution head. The expected absent-implementation RED is preserved in run 36482428976 and its full log.

Candidates: 13,16,22,25,27,29,37,39,46,50,66,77. Both preparations, 81 hidden probes, native/transformed frames, 50/80 digits, and archived binary attenuation values 1,1/3,1/6 were retained. This gives 72 configurations per precision, two frames, or 288 frame configurations overall. No source, state, edge, threshold or geometry was fitted after measurement.

## Results

| Check | Result |
|---|---|
| Exact state/preparation cases | 24/24 first-five direction matrices identically zero as polynomials in a |
| Sixth-edge polynomial | nonzero in all 24 cases |
| Conditional support basis | all 112 words certified, exact transfer reconstruction passed |
| EB numerical cases, 80-digit native | 48/48 RETAINED_EDGE_NULL |
| Identity-middle cases | 24/24 RETAINED_EDGE_NULL; exact directions vanish at a=1 |
| Native first-five EB norm | exactly stored as zero in all 48 cases |
| Omitted-edge EB norm range | 0.0001756937539093722 to 0.001308319510858797 |
| D response rank | zero at all three frozen thresholds, both precisions and frames |

The full transformed-frame directions, residuals, spectra, matrices and domain diagnostics are retained in the raw files. Numerical covariance residuals are bounded by the frozen 1e-35 gate; the maximum cross-precision discrepancy is 7.439e-50, below 1e-30. Agreement with the parent response and complete direction norm passed in every case.

## First-principles explanation

The ideal historical state is a mixture of a three-site state on 012 with an identity at 3 and one on 013 with an identity at 2. In its 112-word support class, the D commutator on pair (2,3) has no one-body output, and its only possible two-body output lies on (2,3). The diagonal local preparations preserve that support. The one-body product terms in the connected differential therefore vanish. Projecting onto edges (0,1),(1,2),(2,0),(1,3),(3,0) removes the D direction before any smooth Hessian on those edges is applied.

The archived binary states are **not exactly in the ideal support span**. Their nonzero excluded-sector coefficients were preserved as exact rationals, not rounded away. Their entire excluded-sector commutator is exactly zero in every case, so the sufficient argument extends to these actual states. Direct exact six-edge polynomial calculations independently confirm the conclusion.

| Candidate | Nonzero excluded coefficients | Excluded-sector commutator |
|---|---:|---|
| 13 | 9 | zero |
| 16 | 12 | zero |
| 22 | 9 | zero |
| 25 | 6 | zero |
| 27 | 10 | zero |
| 29 | 12 | zero |
| 37 | 10 | zero |
| 39 | 6 | zero |
| 46 | 8 | zero |
| 50 | 6 | zero |
| 66 | 10 | zero |
| 77 | 12 | zero |

This resolves the v16.04 ambiguity between edge projection and readout annihilation. It does not establish a universal D-null theorem for arbitrary states, loops or preparations. The model still uses time as pruning / ordered recoverability update. It derives neither a universal source law nor gravity, and introduces no dark-matter primitive or external alignment.

## Evidence and reproduction

[summary.json](summary.json) contains every 80-digit native configuration and aggregate checks. [EVIDENCE.json](EVIDENCE.json) binds each raw shard to its job, artifact ZIP digest and gzip digest. All twelve `result-N.json.gz` files are committed permanently beside this report, with exact polynomials, six-edge directions, all T_D matrices and controls. `SHA256SUMS-N`, measurement logs, full job logs, preregistration, source manifest, derivation, implementation, tests and independent review are included. Files are small enough for ordinary GitHub publication; no size workaround is needed.

Reproduce the publication check using `python summarize.py . --output summary.json` and `python -m unittest test_summary -v`, with sympy 1.13.3. The workflow pins the complete measurement dependencies. The independent reporter checks ensemble completeness, execution head, frozen limits, exact zero predicates, certificate integrity, numerical matrix norms and reported ranks/classes; it does not rerun the scientific measurement.

## Maximum control residuals

| Precision:control | Maximum absolute residual |
|---|---:|
| 50:coefficient_identity | 0 |
| 50:state_reconstruction | 0 |
| 50:transfer_identity | 9.2587285491135673356250412619791992776743056482136E-51 |
| 50:commutator | 1.5382617079350829340879362177400864626242557596152E-53 |
| 50:exact_direction | 3.6912696309029068682388464642284214096320763613805E-54 |
| 50:global_covariance | 7.2520763046978978122591248283827001709123116075339E-50 |
| 50:retained_covariance | 3.0573868562204387232610671863070346882730972080355E-52 |
| 50:response_covariance | 1.7384212656919069837286872644202036694233158098015E-51 |
| 50:precision | 0 |
| 50:hidden_null | 4.7197035989773172041119239052020839692548829914164E-51 |
| 50:hidden_pair_equality | 2.8583638537594135042114426875656232987798801537005E-51 |
| 50:hessian_identity | 5.3187697693512056341591811307847915443687138244911E-50 |
| 50:parent_response | 1.5491906041638377535883940786101911914440337460704E-101 |
| 50:parent_complete_norm | 4.4372070382389966781629999942944523378767916954869E-53 |
| 50:identity_middle_null | 0 |
| 80:coefficient_identity | 0 |
| 80:state_reconstruction | 0 |
| 80:transfer_identity | 8.4337583545844185794788592410160152061679691058948060400622104200865154327758077E-81 |
| 80:commutator | 1.2889662014113733112677196597307588680227896092727154170090114512986964266969702E-83 |
| 80:exact_direction | 2.9118983024488972445969485538272209889195925231370779870282485504872905801147998E-84 |
| 80:global_covariance | 6.5307020724403473718310432676691920773230106530407108053911893116077538690605656E-80 |
| 80:retained_covariance | 1.3326931175148123243669637515819949176788433654516299376842389405719825034963712E-82 |
| 80:response_covariance | 1.32743561487330717237138989190055316451588287461095038648632836760894777704241E-81 |
| 80:precision | 7.4389324918198641709153210087471113673114716939630956245310111544259353212828964E-50 |
| 80:hidden_null | 3.6869215488227932510905287061138323419525292079371069494839220117149746461591791E-81 |
| 80:hidden_pair_equality | 2.1290529148183476842211932328660340622160199633587855494674200657500265578173889E-81 |
| 80:hessian_identity | 5.2926712105961545167992937417608743164098538484992023594671644329052690406032971E-80 |
| 80:parent_response | 1.3101396616511729251330435671303259079943504672870141979423543315327120325670334E-161 |
| 80:parent_complete_norm | 3.0885345536808173508833713040830133811650277487407736963118446362621516477450468E-83 |
| 80:identity_middle_null | 0 |

## Next scientific question

Determine whether an independently motivated, admissible readout that includes (2,3) can observe the omitted direction. First audit its polar domain and loop requirements analytically. A nonzero connected direction alone does not guarantee a defined or nonzero geometric response. Any extension needs a new preregistration; the sixth edge was not inserted into this experiment after observing its result.
