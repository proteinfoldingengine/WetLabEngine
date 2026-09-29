# UQCF-GEM: Foundational Closure and Verification Assignment

## Central requirement

Every closure claim must be supported by a mathematical argument and checks capable of rejecting an incorrect construction—not merely by a script returning the expected verdict.

That addresses the specific weakness in the reviewed work: .13F’s audit returns predefined conclusions, while .14F’s tests mainly check a dimension example and declared Boolean flags. Those checks do not independently establish the principal closure claims.

## 1. Mission and scope

Continue the foundational F branch, not the historical observable/modeling continuation.

The scientific question is:

\[
\boxed{\text{What does the existing retained-information structure actually determine,}\quad\text{and what remains underdetermined?}}
\]

The immediate obligation is to resolve the dependency identified in 16.13F–16.14F: whether the already-defined intrinsic obstruction can be assigned consistently to successive information-loss layers and compared across composed prunings. The published .14F result identifies the descent condition but does not establish that the actual obstruction satisfies it.

A satisfactory outcome may be a constructive theorem, an admissible counterexample, a precisely scoped underdetermination theorem, or an honestly documented unresolved dependency.

Do not select an outcome in advance. A negative result must not be easier to declare than a positive one.

### Starting references

Repository: `proteinfoldingengine/WetLabEngine`

Reviewed foundational directories:

- `ResearchHistory/UQCF-GEM/demos/v16.13F-foundational-closure`
- `ResearchHistory/UQCF-GEM/demos/v16.14F-obstruction-carrier-closure`

Reviewed publication snapshot: `fb9e57e180fbc876598eafbd3f258a941ec469b8`

First verify the current F-branch state. If later foundational work already addresses these requirements, audit it rather than duplicating it or overwriting its numbering.

Use an additive branch from the verified foundational lineage. Do not merge to main, rewrite historical results, or alter unrelated protein-engine files.

## 2. Non-negotiable scientific boundaries

Preserve:

**Time is pruning / ordered recoverability update.**

Do not introduce fundamental time, a geometric target, a metric, a connection, curvature, a Hilbert-space/CPTP primitive, external alignment, a fitted coupling, or a phenomenological source law into this closure campaign.

Do not import the historical response coarse map A_r merely because it makes a composition formula work. Its admissibility must be established from the frozen foundation before it can be used.

The .13F inventory explicitly separates the retained primitives from .12’s supplied quantum-response model. Preserve that separation. A successful quantum-response example is not automatically a foundational retained morphism.

At the same time:

**Do not discard already-earned structure and then announce an impossibility caused by its removal.**

Lineage information, actual retained inclusions, retractions, source pushforwards, and their established relations must all be considered when making a claim about the full retained foundation.

A result about a bare filtration must be labeled as a result about a bare filtration.

## 3. First deliverable: a provenance and type ledger

Before implementing the new adjudication, reconstruct the exact definitions being used.

For every essential object, publish:

| Required field | Content |
|---|---|
| Definition | The actual mathematical construction—not only its name |
| Type | Domain, codomain, scalar structure and admissible inputs |
| Provenance | Exact prior file, commit and theorem or derivation |
| Assumptions | Every condition needed for the construction |
| Status | Primitive, derived theorem, conditional construction, or unresolved |

At minimum cover lineage addresses, parent-child incidence, admissible pruning, ancestral retraction, retained inclusion if available, source grades, pushforwards, kernel filtrations, G_f, Q, and

\[
O_r=(QG_f)|_{\ker P_r}.
\]

### Important restrictions

Do not assume that “finitely additive source grade” automatically means an arbitrary real vector space. Establish what scalar structure was previously earned and how the linear representation follows.

Do not treat two spaces as identical because their dimensions match.

Do not use the same symbol Q for different quotient maps without indexing its domain and quotient relation.

Do not describe a map as linear unless linearity is established. This matters directly to the descent test.

If a required definition cannot be recovered, record `UNRESOLVED_DEFINITION` and identify the exact missing dependency. Do not fill the gap with a plausible replacement.

Every earlier “DERIVED” entry needs a traceable argument. A previous report’s assertion is a pointer to evidence, not a substitute for it.

# Bounded research campaign

## 4. Gate A — Reconstruct and verify the pruning algebra

Implement the actual retained operations from their definitions, not from the expected verdict.

For composable admissible prunings

\[
f\xrightarrow{r}m\xrightarrow{q}c,
\]

establish and verify the relevant identities, including:

\[
P_{q\circ r}=P_qP_r,
\]

and the nesting of cumulative kernels

\[
K_j=\ker P_{0j},\qquad K_{j-1}\subseteq K_j.
\]

Where source pushforward is defined by finite sums over retraction fibers, derive its composition law directly from those fibers. Do not replace the derivation with a matrix identity whose construction already assumes the desired answer.

### Executable checks

Construct admissible finite lineage examples and generate their legal prunings. Include identity pruning, pruning to the root where admissible, branching lineages, repeated pruning, and different factorizations with the same final pruning.

Compare independent implementations: for example, direct fiber aggregation against matrix pushforward.

Invalid structures must be rejected explicitly. Missing ancestors, inconsistent lineage addresses, illegal pruning targets, and incompatible composition endpoints must not be silently repaired.

**Acceptance:** a general argument for each claimed identity, plus exact implementation checks and controls that reject malformed constructions.

Passing a finite collection of examples alone does not prove the general theorem.

## 5. Gate B — Distinguish bare-filtration results from full-foundation results

The associated-graded objects

\[
G_j=K_j/K_{j-1}
\]

are standard quotient constructions. Their role here is to identify what follows from the actual pruning structure, not to claim that associated-graded mathematics itself is a new discovery.

Run two explicitly separated analyses.

### B1. What follows from the filtration alone?

State exactly what morphisms are allowed between filtered objects.

Establish which inclusions, quotient projections and induced maps are available. If claiming that no canonical nonzero intergrade transport follows, provide a naturality or symmetry argument that addresses the entire declared class.

Finding several possible maps does not, by itself, prove that no canonical construction exists.

Similarly, “the obvious inclusion becomes zero in the next quotient” only rules out that construction; it is not automatically a complete nonexistence proof.

Distinguish carefully:

\[
\text{a map exists},\qquad\text{a map is uniquely characterized},\qquad\text{a map is natural under the allowed morphisms}.
\]

### B2. What changes when the full retained data are restored?

Audit every already-earned inclusion and retraction.

For example, if the retained construction supplies maps

\[
P:V_f\to V_c,\qquad I:V_c\to V_f,\qquad PI=\mathrm{id},
\]

then investigate the resulting decomposition through

\[
v=(v-IP v)+IP v.
\]

Here v-IP v lies in ker P. The relevant issue is whether I is supplied naturally by the retained construction—not whether a generic vector space admits many possible complements. This is the distinction between an existing section and an arbitrarily chosen splitting.

Likewise, if the cumulative pushforward is surjective, examine the candidate exact sequence

\[
0\longrightarrow K_{j-1}\longrightarrow K_j\xrightarrow{\,P_{0,j-1}\,}\ker P_{j-1,j}\longrightarrow0.
\]

Prove the hypotheses and exactness before using it. Determine whether already-earned retained inclusions provide a compatible section.

Do not assume that a source-space splitting also solves the response-codomain problem. They are different questions.

### Acceptance

Publish separate conclusions for the bare filtration and the full retained inventory. A no-go proved in the first setting must not be promoted to the second without an additional argument.

## 6. Gate C — Test the actual obstruction’s descent

This is the central scientific gate.

For the relevant map

\[
T_j:K_j\to W_j,
\]

first establish its exact definition and linearity.

For a linear map into a fixed codomain, the assignment

\[
\overline T_j([x])=T_j(x)
\]

defines a map on K_j/K_{j-1} precisely when

\[
\boxed{T_j(K_{j-1})=0.}
\]

This is the quotient universal property, not an empirical threshold.

### Required adjudication

Compute or derive the actual restriction

\[
T_j|_{K_{j-1}}.
\]

If it vanishes, construct the descended map and prove representative independence.

If it does not vanish, return an explicit admissible witness

\[
k\in K_{j-1},\qquad T_j(k)\ne0.
\]

Show that two representatives of the same quotient class produce different outputs. Verify that the witness satisfies every retained-domain condition.

Do not substitute an arbitrary matrix T and call its failure a counterexample to the actual UQCF-GEM obstruction.

### Guard against a tautological success

Distinguish a cumulative obstruction from a stage obstruction pulled back to the original source space.

A construction such as

\[
\widetilde O_j=O_{r_j}\circ P_{0,j-1}
\]

automatically annihilates ker P_{0,j-1} if the relevant maps are linear. That may be useful, but it does not automatically establish compatibility with the cumulative obstruction O_{r_j\circ\cdots\circ r_1}.

Their codomains may differ. Do not identify them without an earned map.

The gate must test the unresolved claim, not redefine the object so that the desired condition holds by construction.

### Nonlinear boundary

If the obstruction is nonlinear, replace the linear annihilation criterion with the actual representative-independence condition:

\[
T_j(x+k)=T_j(x)\quad\text{for all admissible }x,\ k\in K_{j-1}.
\]

Vanishing on K_{j-1} alone is then insufficient.

### Legitimate alternative: quotienting the response

If fixed-codomain descent fails, examine—but do not silently substitute—the linear construction

\[
K_j/K_{j-1}\longrightarrow W_j/T_j(K_{j-1}),\qquad[x]\longmapsto[T_j(x)].
\]

Verify that it is well defined using the actual objects. Report exactly what response information this additional quotient discards.

Its existence would not mean that the original response was recovered unchanged, and it would not automatically supply transport between different stages.

## 7. Gate D — Composition, naturality and refinement

Only after the objects and descended maps are defined should the worker test composition.

Write every proposed diagram with explicit domains and codomains. Identify each connecting arrow as an existing map, a derived construction, or an unresolved dependency.

Where a common response carrier or transport is available, test two-stage and three-stage composition. Different parenthesizations must agree whenever the framework claims they represent the same operation.

Check compatibility with admissible lineage relabelings. A construction must not depend on lexicographic node labels, arbitrary array order, or a basis chosen merely to make a formula work.

Where quotient representatives are used, compare them using the maps already justified.

Also examine refinement: inserting an intermediate legal pruning changes the list of stages. Compare the resulting information through justified maps, rather than demanding that differently indexed graded pieces be literally identical.

Do not force composition by introducing a new response transport. If an arrow is missing, locating that missing arrow is the result.

# Verification standards

## 8. Replace self-reporting flags with computed evidence

The reporting layer may contain fixed verdict names and theorem identifiers. It must not contain a fixed scientific answer masquerading as an audit.

For each claim, the output must identify its inputs, the check performed, the computed result, and the certificate or witness supporting it.

A value such as all_valid may summarize executed checks. It must not be assigned True independently of those checks.

Separate at least:

| Field | Meaning |
|---|---|
| Execution status | Did the program run correctly? |
| Input validity | Were the mathematical inputs admissible? |
| Scientific verdict | What does the result establish? |
| Proof status | General proof, bounded certificate, or unresolved |
| Scope | Exactly which class of objects the conclusion covers |

A valid negative scientific result can pass CI. A malformed input, broken implementation, unreadable certificate, or incomplete required check cannot.

Missing checks must never default to success.

## 9. Tests must be capable of exposing the relevant mistakes

Preserve preregistration and RED/GREEN, but strengthen what RED means.

A missing-module failure verifies test wiring. It does not demonstrate that the eventual tests can detect incorrect mathematics.

Require three classes of checks.

### Constructive and counterexample controls

Use small exact linear-algebra fixtures to verify the descent checker itself: one map that annihilates the old kernel and another that does not.

Label these as checker controls, not UQCF-GEM results.

For the actual research conclusion, use the actual retained obstruction or a witness proved admissible under every frozen hypothesis.

### Metamorphic checks

Relabel the same lineage consistently, change computational bases, and alter harmless storage order. The represented construction and verdict must remain equivalent.

Where quotient representatives are used, replace a representative by another in its class and verify the claimed invariance.

Coordinate choices are permitted for computation. They must not become unacknowledged physical structure.

### Deliberate defect checks

Show that the verifier rejects representative failures such as an incorrect pushforward coefficient, an illegal domain identification, a map that fails to annihilate the old kernel, or a proposed section that does not satisfy its required identity.

Include at least one case where a construction is valid as an ordinary linear map but invalid as a retained-natural map.

A test suite that accepts its own intentionally corrupted construction is not ready to certify closure.

## 10. Exact arithmetic, bounded enumeration and independent verification

Use exact integer or rational arithmetic where the inherited definitions permit it. Do not decide exact rank, kernel membership or zero maps through adjustable floating-point thresholds.

If the proof requires real scalars or symbolic parameters, state how the exact computational representation relates to that domain. Rational examples do not, by themselves, prove a statement about all real inputs.

Preregister a bounded finite test universe—such as all admissible rooted lineage shapes up to a declared small size and all legal pruning chains within it. Publish the enumerator, deduplication rule, counts and exclusions.

This finite universe is an implementation test domain, not a new physical cutoff.

Use an independent certificate verifier wherever practical. It should reconstruct defining relations from raw inputs rather than trust the producer’s pass fields or call the same top-level adjudication function.

A general mathematical theorem still needs a proof. An independently verified finite counterexample can refute a universal claim, but a collection of passing examples cannot establish universality.

## 11. Standards for positive, negative and unresolved conclusions

Use language according to the evidence:

| Conclusion | Required evidence |
|---|---|
| Derived | Explicit assumptions, construction and complete argument |
| Verified on a bounded class | Exact enumeration or certificates with stated coverage |
| Refuted | An admissible counterexample to the stated claim |
| Underdetermined by these axioms | A rigorous demonstration that the axioms do not select the claimed result |
| No canonical construction in this category | A correctly scoped naturality or symmetry obstruction |
| Unresolved | A precise missing definition, proof step or dependency |
| Invalid execution | A technical or input failure that prevents adjudication |

Do not infer “underdetermined” from “I did not find a formula.”

Do not infer “canonical” from “the code chose the same answer every time.”

Do not infer “no transport exists” from “one obvious transport fails.”

Do not infer a physical law from a convenient mathematical representation.

“Closure” must always identify the operation, domain and assumptions that have been closed. Avoid an unqualified “foundation closed.”

# Publication and completion requirements

## 12. Preserve provenance and repair the evidence record

Keep historical .13F/.14F reports intact. Add an evidence-status note explaining which claims were previously reasoned statements and which had substantive executable verification.

Do not rewrite old GREEN runs as if they performed checks that were added later.

Publish, at minimum, the primitive/type ledger, proof document, preregistration, implementation, adversarial tests, certificate verifier, machine-readable results, reproduction instructions and final interpretation.

Every important claim should have a stable identifier linking:

\[
\text{assumptions}\rightarrow\text{proof}\rightarrow\text{implementation}\rightarrow\text{test or certificate}.
\]

For runs, record the exact execution SHA, workflow/job IDs, attempt number, dependency versions, commands, exit codes, test counts and artifact identifiers. Hash raw certificates and result files.

Keep scientific JSON separate from diagnostic logs. Archive failures and invalid attempts as well as successful runs.

Do not rely on a temporary Actions artifact as the only lasting copy of evidence. Publish a durable, appropriately sized repository record or release attachment with checksums.

If only documentation changes after execution, record that distinction. If executable code changes, rerun the relevant verification before claiming that the new head was tested.

## 13. Independent review before completion

Have a separate reviewer inspect the proof and the verifier, not merely the final report. If no separate reviewer is available, label the work as self-reviewed; do not fabricate an independent review.

The review must specifically challenge:

- whether a supposedly earned object was actually assumed;
- whether a bare-filtration result was overstated as a full-foundation result;
- whether a descent or composition identity was made true by redefining the target;
- whether the tests can reject a mathematically incorrect implementation;
- whether the stated conclusion exceeds the proven or enumerated domain.

Resolve objections with evidence. Agreement between two summaries is not independent mathematical verification.

## 14. Required return report

Return one combined report for this campaign, not another isolated positive-status announcement.

Its opening table must answer:

| Question | Required answer |
|---|---|
| Which retained operations are now closed? | Exact operation, assumptions and supporting proof |
| What does the actual obstruction do on the previously lost kernel? | Zero, explicit nonzero witness, or unresolved |
| Is any splitting already supplied by retained structure? | Construction and naturality proof, or scoped obstruction |
| Can obstruction information be compared across stages? | Explicit typed maps, or the exact missing arrow |
| What was genuinely verified by code? | Checks, controls, certificates and coverage |
| What remains open? | Smallest unresolved dependency without an invented replacement |

Include the strongest result against the worker’s initial expectation, any corrected historical interpretation, and the limits of the conclusion.

The campaign ends when these questions have been honestly adjudicated. Do not extend it into new source families, geometric readouts, coupling fits or gravity models merely to obtain a more attractive result.

## Final acceptance rule

Do not return with only another verdict string. Return with a proof, a checkable admissible counterexample, or a precisely identified unresolved dependency—and evidence showing that the verifier distinguishes those outcomes.

The governing discipline is two-sided:

\[
\boxed{\text{Do not add structure to force closure.}\qquad\text{Do not remove earned structure to force a no-go.}}
\]

That is the standard for continuing the foundational branch.
