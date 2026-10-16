# A collective-covariance interaction candidate and its native premise gap

Date: 2026-10-15 America/Phoenix / 2026-10-16 UTC.
Immutable source parent: `0583236e036fc9bfad2481721be6cfc4dd9a4cf3`.

**Conditional analytical candidate assessment; native interaction milestone NOT ACHIEVED.** On two supplied qubit factors carrying the same identified representation, every unitary invariant under a simultaneous arbitrary basis rotation is a partial swap, up to a global phase. On the exact blank-memory source pair used in the preceding retained-reader report, every member except a scalar identity gives a positive memory probability contrast. The strength need not be chosen to obtain that qualitative consequence.

This supplies a precise conditional class in which a shared consequence survives nonuniqueness of the microscopic operation. It does not derive the class from the native retained ontology. Its two factors and their identification, invariance of the actual interaction under common rotations, occurrence of a nontrivial unitary, and the accessible retained reader are additional premises. They are examined here, not adopted as physical axioms. No source-semantics branch is reopened and no quantum carrier is inferred from a lineage tree.

The calculation uses standard partial-swap mathematics, not a new quantum mechanism or mathematical-priority claim. Its purpose is to assess whether common-frame symmetry could replace choosing a copying gate by hand, and to state exactly how far that replacement goes.

## 1. Candidate and actual source pair

The prior report already supplies the following comparison as an analytical control:

- Hilbert space H = C^2_S tensor C^2_M, with labelled source and memory factors.
- The same blank memory tau = |0><0|_M in both preparations.
- Source preparations sigma_0 = |0><0|_S and sigma_1 = |1><1|_S.
- Joint states rho_b = sigma_b tensor tau.
- Memory effect Q = I_S tensor |1><1|_M.

Thus Tr(Q rho_0) = Tr(Q rho_1) = 0. The memory initially lacks the preparation bit even though the source contains it. This is the inherited *quantum control pair*, not an earned representation of the native incidence-source pair or a new physical preparation.

A chosen identification of the two qubit representations makes the exchange operator well typed:

    F(|x>_S tensor |y>_M) = |y>_S tensor |x>_M,
    F = F^dagger,     F^2 = I.

The new candidate class is a common, state-independent unitary U satisfying

    [U, V tensor V] = 0                 for every V in SU(2).       (1)

This is **collective invariance of one fixed operation**. It is not the weaker fact that the matrix description of an arbitrary operation transforms covariantly when its generator and reference are transformed as data. Nor is it independent local invariance under V tensor W. Those distinct hypotheses must not be exchanged.

The collective representation is part of the input: equal dimensions alone do not identify the physical source and memory frames. Given that identification, the blank's orthogonal projector defines the above reader without choosing an additional coordinate axis. Simultaneously rotating the identification, states, blank and reader leaves the predictions unchanged. This coordinate independence does not supply a physical apparatus, access or record.

## 2. Derive the whole unitary class

Expand an arbitrary two-qubit operator in the Pauli basis:

    U = a I + sum_i b_i sigma_i tensor I
            + sum_i c_i I tensor sigma_i
            + sum_ij T_ij sigma_i tensor sigma_j,

with complex coefficients. Conjugation by V acts on the three Pauli components through the associated R in SO(3). Condition (1) therefore requires b and c to be fixed by every rotation, so both vanish, and requires

    R T R^T = T                        for every R in SO(3).

Rotations by pi around the coordinate axes force the off-diagonal entries of T to vanish; quarter-turns exchanging axes force its three diagonal entries to agree. This works for complex as well as real coefficients. Hence T is a scalar multiple of I_3.

Using F = (I + sum_i sigma_i tensor sigma_i)/2 gives

    U = alpha I + beta F.

The orthogonal symmetric and antisymmetric projections P_+ = (I+F)/2 and P_- = (I-F)/2 have nonzero ranges. Consequently U is unitary exactly when its eigenvalues alpha+beta and alpha-beta both have modulus one. Writing their phases as phi-theta and phi+theta yields the complete form

    U = exp(i phi) [cos(theta) I - i sin(theta) F].                 (2)

Conversely every (2) is unitary and satisfies (1). The scalar phase has no channel effect. The channel is identity exactly when sin(theta)=0; all other members are nontrivial. Full exchange is included at theta=pi/2.

No continuity, differential equation, Hamiltonian or physical clock is required. Theta is a dimensionless operation parameter; it is not identified with time or pruning depth. Equation (2) is a class characterization, not a law choosing theta or making an operation occur.

## 3. Pair-specific acquisition, before retention

Set c=cos(theta), s=sin(theta), and ignore the global phase. For the inherited pair,

    U|00> = exp(-i theta)|00>,
    U|10> = c|10> - i s|01>.

Tracing out S gives

    rho_M,0' = |0><0|,
    rho_M,1' = c^2 |0><0| + s^2 |1><1|.

Thus the conditional binary readout laws are

    Pr(1 | b=0) = 0,
    Pr(1 | b=1) = sin(theta)^2.                                    (3)

Their total-variation distance, and the memory-state trace distance, are both sin(theta)^2. With Delta = rho_1-rho_0, this tests exactly the preceding report's criterion:

    Tr(Q Delta) = 0,
    Tr[(U^dagger Q U - Q) Delta] = sin(theta)^2.                    (4)

This is not credit for merely changing an operator or flipping a blank independently of the source. It separates the specified preparations. Every nontrivial member of the classified unitary family passes this pair-specific conditional test. No particular nonzero theta was selected after seeing the signal.

A positive outcome is a sound partial record of b=1 within this ideal preparation/readout model. A zero outcome is generally ambiguous. There is no deterministic write unless sin(theta)^2=1, and no guaranteed positive outcome. Exact zero false-positive probability presumes the exact states and readout above; no experimental noise or error budget is inferred.

The same statement survives a common classical mixture of these unitaries. With a probability measure mu over theta, independent of the preparation label, replace sin(theta)^2 by

    lambda = integral sin(theta)^2 d mu(theta).

Then the output laws are (0,lambda), and lambda>0 exactly when mu assigns positive mass to nonidentity members. No mixture name needs to be made readable. The mixture model, if used, is another explicitly conditional interface, not a derived stochastic event law.

There is no uniform positive lower bound over all nontrivial members: theta can approach zero. Thus this class gives strict separation conditional on a nontrivial operation, not a uniform finite-resource discrimination guarantee. A concrete sampling/error contract would require further information.

## 4. What is retained, and what remains an access obligation

If a following nonselective expectation E_A retains Q, then

    Tr[Q E_A(U rho_b U^dagger)] = Tr[Q U rho_b U^dagger].

Any finite succession retaining that same reader also preserves (3), by the previous result. Pinching the memory basis is one supplied example. This is precisely where retention enters; the unitary precedes the reduction and does not fix Q when it transfers the distinction.

Actual availability of the local memory effect, the association of its outcome with this source/reference, event occurrence, and retention of an actual outcome remain separate. The formula for Q can be specified covariantly using the blank; that is not a derivation that an event measures it. No RCR selection is deduced.

A stronger restriction to **reference-free invariant joint effects** would give a different answer. Every effect commuting with all V tensor V lies in span{I,F} by the same proof. Such an effect commutes with every U in (2), so its statistics are unchanged. In particular P_- already has initial probabilities 0 and 1/2 on rho_0,rho_1 and retains them. It is not an initially blank acquired record. A symmetry-invariant joint detector cannot silently substitute for the local memory reader.

This separates collective symmetry of the operation from access to a localized, reference-associated record. There is no requirement that every physical reader be invariant; the point is to state which reader is actually being used.

## 5. Controls and relation to inherited results

**Identity is still admitted.** Equation (1) allows theta=0. Symmetry alone therefore forces no positive contrast. Requiring an actual nontrivial member is load-bearing. Calling a history event, a source active, or a pruning strict does not establish that its unitary on this carrier is nonidentity.

**Independent frame invariance removes this interaction.** If [U,V tensor W]=0 for every independent V,W, commuting first with all V tensor I gives U=I tensor B, and then commuting with all I tensor W makes B scalar. The channel is identity. The inherited v15.78 report treats a stronger independent-local symmetry for a different, three-qubit fixed-map interface; it is not contradicted. A common representation cannot be obtained merely by dropping that independence without native justification.

**Coordinate covariance does not impose (1).** The inherited v15.79 classification lets source tensors transform and admits multiple coupling tensors. It explicitly does not select a physical law. Any supplied copying operation can be described covariantly by transforming its defining data; that descriptive covariance does not make it commute with V tensor V. The present proof cannot be cited as a consequence of covariance in that weaker sense.

**Nonidentity covariant channels need not transfer.** Drop unitarity and take the CPTP map

    Phi(X_SM) = (I_S/2) tensor Tr_S(X_SM).

It is invariant under the collective rotations in the channel sense, is not identity, and changes both pure-source inputs, but leaves the memory blank in both. Thus (3) is not forced by symmetry plus generic channel activity. The reversible two-qubit scope is essential.

**The previous swap average is a different channel.** The inherited E_F(X)=(X+FXF)/2 has the same local-memory probabilities as theta=pi/4 on this pair. On |10><10| it is a mixture of |10><10| and |01><01|, whereas the unitary partial swap produces a pure superposition before further reduction. Equal local probabilities do not identify their global actions. The new calculation does not reclassify that expectation as a reversible native coupling.

**Later interaction can undo the write.** U(-theta)U(theta)=I up to phase. The demonstrated persistence is through the specified reader-preserving reductions, not arbitrary future interactions. No irreversible force or universal memory stability follows.

**Not a cloning claim.** A partial swap redistributes state information and generally correlates the factors. Nothing claims to copy every unknown quantum state while preserving the source. The exact classical pair above is enough for the stated statistical consequence.

All controls are direct analytic calculations. No numerical source-response experiment or new test count is involved.

## 6. Native provenance audit

| Required object or premise | What is available | What this assessment does not derive |
| --- | --- | --- |
| Two labelled qubit factors and source pair | Explicit controls in the retained-reader report | A native source/receiver carrier, or a correspondence from the indexed-view source pair |
| Common identification of the two representations | Needed to type F and V tensor V | A relation identifying frames from equal dimensions, Genesis or lineage identities |
| Common-rotation invariance of the actual operation | The declared candidate condition (1) | A native law imposing this stronger fixed-operation symmetry |
| Reversible action on exactly these two factors | The declared unitary scope | Reversible implementation, exclusion of additional degrees of freedom, or actual occurrence |
| Nonidentity operation | Precisely sin(theta) != 0 | Exclusion of identity from native event premises; strength or probability of occurrence |
| Local blank and reader Q | Existing supplied control; reader specified relative to the blank | Physical preparation, measurement, delivery, error budget or source/reference association |
| Reader-preserving reductions | Inherited conditional retention theorem | The occurrence of those reductions or retention under arbitrary later interactions |

The v15.09 carrier-origin boundary remains intact. The compatible-record tree and compatible-history seed establish conditional representations; they do not supply these two tensor factors or a unitary on them. No tree projection, source grade or provenance label is identified with a qubit or Pauli operator here.

The candidate therefore advances from an individually chosen gate to a **whole explicitly restricted class** with a pair-specific shared consequence. That is a useful conditional mathematical specification, but its native premise gap remains substantial. In particular, imposing common representation, reversible nontrivial occurrence and local access solely because they yield (3) would still supply the mechanism by hand.

## 7. Disposition, next target and verification scope

**Disposition: CONDITIONAL_COLLECTIVE_UNITARY_CLASS_HAS_PAIR_SPECIFIC_TRANSFER; NATIVE_COMMON_REPRESENTATION_NONTRIVIAL_ACTION_AND_ACCESS_UNRESOLVED.**

No admitted native coupling has been found. The native milestone remains NOT ACHIEVED. This is not a general obstruction and does not make unitarity, common-frame symmetry, two qubits or a deterministic outcome compulsory for other candidates.

For this route, a useful next source investigation must produce an *independent* native relation binding the source and receiver representations and constraining their actual action/access. It must justify why its action falls in the collective class and is nonidentity, or derive another pair-sensitive operation directly. A symmetry condition written for a desired result, another partial-swap simulation, or another decoder does not meet that obligation. If no such relation is available, stop this candidate at its exposed premise gap rather than treating (3) as physical progress.

The eleven-source packet binds the governing AGENTS, milestone and continuation; the latest retained-reader assessment; both preceding record-representation reports; the finite-interaction assessment; the v15.09 carrier report; and the v15.78/v15.79 symmetry reports. Its scope is these exact sources, not an archive-wide absence or novelty claim. Historical numerical assertions in those documents are not freshly reproduced or recertified here.

Standard partial-swap context: M. Ziman et al., *Quantum homogenization*, arXiv:quant-ph/0110164, sections II and IV, https://arxiv.org/pdf/quant-ph/0110164 (consulted 2026-10-16 UTC). That work supplies prior context for partial-swap information transfer and uniqueness under its homogenization conditions. The distinct collective-invariance hypothesis and elementary Pauli-basis proof used here are stated in full; no thermal reservoir, duration or homogenization axiom is imported into UQCF-GEM.

All displayed findings were obtained by analytical reasoning before review. No scientific module, simulation, enumeration, historical replay or numerical campaign was run; no retrospective preregistration is claimed. Provenance hashing and document verification are publication checks, not scientific executions. Independent argument review and separate publication auditing must bind the exact final text. No main merge or numbered-stage CLOSED/CERTIFIED status is asserted.

Time remains pruning / ordered recoverability update. No inserted geometry, fundamental clock, dark-matter primitive, heuristic fitting, physical force or gravity derivation is introduced. Conditional RAS/RCR and earlier positive results remain preserved. Path A remains active, Path B stays closed, and broad C3/C4-C6 remain OPEN.

