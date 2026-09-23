# UQCF-GEM v15.44: Intrinsic curvature interpretation preregistration

Status: written specification for review; no implementation or new measurements.
Parent: f121358c53ffdf88f9c0dcf351b850819ecb0298.
Parent certification: https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/35754551391
Branch: research/v15.44-intrinsic-curvature-interpretation.
Date: 2026-09-22.

## 1. Purpose and disclosure

Determine exactly what the certified response-to-curvature construction measures, characterize all responses it cannot distinguish from zero, and describe canonical-versus-control differences under fixed mathematical comparisons.

This advances the UQCF-GEM information-to-geometry program by turning a reproducible nonzero result into an interpretable mathematical operator. It does not assume fundamental time or pre-existing physical spacetime.

The v15.43 outcomes are already known: 740 cases, 148 canonical cases, 30,260 face records; all five families nonflat on a common canonical carrier. This is a prospective registration of additional analysis after those observations, not a blind prediction of nonzero curvature. L7 has already been inspected in v15.43 and is not fresh held-out evidence here.

Success is a complete exact characterization even if it shows generic response curvature, a large kernel, or no canonical distinction. No desired gravity outcome determines the procedure.

## 2. Selected approach and alternatives

Selected: derive an exact linear map from scalar fields to based curvature matrices, prove its equivalence to the frozen implementation, then compute its rational kernel and fixed family comparisons. This gives interpretable identities and finite completeness certificates.

A larger numerical sweep would add cases before explaining the map; defer it. A source-curvature fit would introduce a new scientific question and permit outcome-driven interpretation; exclude it. A literature review will assess novelty only after the mathematical object is stated precisely and cannot change this stage's analysis rules.

## 3. Frozen evidence and boundaries

All inherited tracked files remain byte-identical to the parent. PR #53 and PR #54 remain untouched, draft/open/unmerged. Work is additive on this descendant branch.

Pinned evidence:
- v15.43 docs/INPUTS.json: f6435267950cde0985889056a67d5427f60f637f.
- v15.43 docs/RESULTS.json: 937024b3f90570c9b177bfb2eee7cdab25a13985.
- v15.42 transport.py: df552284c16d43bc876340fbc13fe91eb9ee6a00.
- v15.42 holonomy.py: bad3f06b291bb448a903b4f48344a9e54a633f68.
- v15.43 application.py: 30348d71d366a751932ec2d58d18a9148d81ae83.
- v15.43 projection.py: f857f2cf1cd4c265c193121236af8e441b1f01dc.
- v15.43 carriers.py: 5cd286b014bb44025e16832ee91a6e6665291c8c.

Paths above are under ResearchHistory/UQCF-GEM/demos and their named version directories. The implementation plan must enumerate and pin the full executable closure from the exact parent before code execution; the named pins do not substitute for that closure.

The evaluator reads the committed validated projection and derived carrier objects. It receives no source arrays, targets, incidence-source support, external coordinates, historical source-correspondence verdicts, fitted parameters, or new response generators. Prior RESULTS enter a separate comparison process only after operator and kernel construction. Family labels select rows for reporting only; they never select operator coefficients, bases, carriers, or thresholds.

## 4. Domain and operator

Use exactly four existing carriers: L=5 and L=7, each at work scale 1 and 7/3. Preserve inherited label, edge, direction, frame, face, basepoint, and orientation conventions. Fields lie in Q^N, N=L^2. Include the full field space for kernel characterization although the archived response fields have zero sum.

For each oriented face f, let K_f(u) be the complete 2 by 2 matrix produced by the certified linearized holonomy. Define A_C: Q^N -> Q^(4F) by stacking its four entries row-major for every face in inherited order. Redundant zero/skew entries are retained. No arbitrary extraction of a signed scalar from a frame is needed.

Construct A_C column j by evaluating the frozen transport/holonomy on unit field e_j. These basis evaluations are a reference oracle, not the independent derivation.

Independently derive coefficients from the exact centered derivatives, endpoint averaging, identity-metric scalar term and skew term in the pinned transport. Expand the derivative of the four-factor ordered face product using a direct sum over the derivative slot. The derived coefficient implementation must not call construct_transport, linearized_holonomy, evaluate_field, or reuse the basis-built A_C.

Prove linearity from the formulas and demonstrate complete equality of derived and reference operators column-by-column. Trace which edge terms cancel around faces and which remain; do not predeclare a Laplacian, Hessian, physical curvature, or source law. Any compact stencil formula must be derived and verified against every coefficient, including periodic wraparound.

Any identification with a familiar operator must state exact domain, codomain, constants, orientation conventions and boundary conditions. An analogy or numerical resemblance is not an identity.

## 5. Exact kernel and image

For every carrier, compute rational RREF in fixed column order. Report rank, nullity, pivot columns, a deterministic nullspace basis, and an image basis. Normalize nullspace bases by the standard free-variable convention (one selected free variable equals one, other free variables zero).

Certificates must verify A_C Z=0, independence of Z, rank plus nullity equals N, and image-basis spanning/rank. Retain row-reduction certificates or an independently checked exact elimination result sufficient to verify the reported rank.

Check constants explicitly. Do not assume that constants exhaust the kernel; report every additional mode if present. On the zero-sum field subspace, separately report kernel dimension and a basis. State finite results for these four carriers only. No all-size or continuum theorem follows from two sizes; an analytic extension requires its own proof and a separately approved scope.

Compute the orthogonal projection onto the kernel under the fixed unweighted vertex inner product using exact rational linear algebra: P_Z=Z(Z^T Z)^(-1)Z^T, with zero projector when the basis is empty. Verify symmetry, idempotence, image, and A_C P_Z=0. This is an algebraic decomposition in the certified label space, not an added physical metric or tuned normalization.

## 6. Full frozen response analysis

Use all five families, all response indices, both sizes, and both scales, with the exact v15.43 key ordering:
GLOBAL_BALANCE_COMPLETION; DIRECT_INHERITANCE; ONE_INCIDENCE_TRANSPORT; MATCHED_DIAGONAL_BALANCE; MATCHED_STEP2_BALANCE.

For every one of 740 fields u, report:
- N, F, exact squared field norm S=u^T u.
- Kernel component P_Z u and visible component (I-P_Z)u, with exact squared norms.
- All matrices K_f(u) from A_C u and their equality to archived v15.43 matrices.
- All face invariants I_f=-tr(K_f^2)/2, histogram, and total E=sum_f I_f.
- The amplitude-normalized response ratio E/S if S>0; otherwise null with reason ZERO_FIELD.
- The normalized invariant distribution I_f/E if E>0; otherwise null with reason ZERO_CURVATURE.
- The visible fraction ||(I-P_Z)u||^2/S if S>0; otherwise null with reason ZERO_FIELD.

The ratios characterize the fixed finite map. They carry no physical units or normalization claim. Keep signed matrices because squared invariants erase sign information.

For each size/scale/index, compare the canonical field against each of the four controls: exact matrix equality, exact normalized invariant-distribution equality, ratio differences, and visible-fraction differences. Also test whether their curvature matrices are proportional by one nonzero rational scalar across all faces; solve the scalar from the first nonzero reference entry in fixed order, then verify every entry. Handle zero/zero, zero/nonzero, and nonzero/nonzero separately with explicit categories. Do not silently equate proportionality with equality or with gauge equivalence.

Publish all 592 canonical-control pair receipts. Each control has 148 paired cases, including both scales. These are deterministic comparisons, not independent statistical samples. No p-values, significance thresholds, family winner, universal source specificity, or pass criterion based on the magnitude/order of ratios is permitted.

## 7. Controls and independent verification

Required exact controls:
1. Constant fields yield zero; every-root impulses match the inherited core.
2. For each carrier, verify the derived/reference map on a spanning basis. This and the linearity proof establish equality for all rational fields on that carrier.
3. Every reported nullspace basis vector yields zero via the frozen core, with rank completeness certified independently.
4. For fields u,v chosen as every pair of distinct unit basis fields, linearity follows from operator identities; explicitly check one fixed mixed field sum_j (j+1)e_j through the frozen core on each carrier as an integration test. No random field selection.
5. Verify archived scalar-amplitude scaling across every matched 1 and 7/3 response pair. Verify carrier alignment from inherited geometry before comparing operators; never assume a matrix equality across incompatible presentations.
6. Verify orientation reversal and cycle rotation/basepoint changes using inherited baseline transport. Verify all eight uniform D4 frame actions and each D4 action at every single vertex using the operator columns; also verify relabeling j -> N-1-j with carrier/field data moved together. Equality is after the corresponding codomain transformation, not raw-array equality.
7. Mutation tests must detect a swapped label/field ordering, wrong face orientation/basepoint handling, missing derivative-slot term, changed coefficient, dropped case, invalid nullspace vector, incorrect claimed rank, source/target payload injection, and corrupted parent blob.

Use exact integers/rationals for decisions. Reject floats, booleans in integer slots, duplicate keys, unknown fields, noncanonical fractions, shape errors, missing coverage and pin drift. Fail closed at the first actual failed stage; retain failure evidence and do not emit a successful characterization from partial cases.

## 8. Outcomes and claim discipline

Ordered stages: evidence -> projection/carriers -> operator derivation/equality -> kernel/image certificates -> controls -> all archived-field comparisons -> ledger.

Status INTRINSIC_CURVATURE_CHARACTERIZED requires every stage to pass. Any mathematical, evidence, schema, or coverage failure gives INTRINSIC_CURVATURE_INTERPRETATION_INVALID with the first failed stage and no completed scientific verdict.

Successful output reports descriptive categories per carrier and per control, including counts of exact equality, proportionality, and normalized-profile equality. There is no privileged expected category. A difference demonstrates only a difference for those frozen response cases; equality cannot establish equality of distinct response-generation laws outside the tested domain.

Keep separate:
- theorem: proved operator identities under explicitly stated assumptions;
- reproducible computation: exact finite ranks, kernels and complete comparisons;
- interpretation: what those identities suggest within the information-to-geometry program;
- open claims: source correspondence, physical curvature/gravity, spacetime, Einstein equations, continuum limit and literature novelty.

Source correspondence is NOT_EVALUATED. Physical claims, uniqueness from foundational axioms, and scientific breakthrough remain false in the stage ledger. Pillar 3 remains OPEN. The inherited-axiom and isotropic-scalar-lift dependencies remain explicit. Ordered computation and algebraic scale parameters are not declarations of fundamental time.

## 9. Deliverables and execution boundary

A later approved implementation plan will specify an additive v15.44 demo containing independent derivation, kernel analysis, controls, tests, a strict canonical result ledger, mathematical derivation document, README and narrow certification workflow. No changes to historical scientific artifacts or v15.43 source are permitted.

The ledger must contain parent/spec/dependency pins, exact operator and certificate hashes, all four carrier receipts, complete 740-case and 592-pair coverage, control counts, errors, theorem-versus-computation labels and claim boundaries. A replay must reproduce deterministic bytes. Dedicated CI runs once on the complete reviewed implementation; document receipts in PR metadata where possible to avoid documentation-only recomputation cycles.

This deliverable is only the preregistration specification. Written-spec review comes next, followed by an implementation plan for approval. No implementation, mathematical result, new audit run, merge, or source-fitting study is authorized by publication of this document.
