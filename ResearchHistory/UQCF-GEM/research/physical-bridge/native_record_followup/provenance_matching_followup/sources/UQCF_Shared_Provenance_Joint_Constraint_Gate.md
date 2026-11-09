# Shared provenance to joint constraints: conditional entanglement bound

Date: 2026-09-05. Unnumbered continuation of the non-replica twist gate.

## Adjudication

**COMMON ANCESTRY DOES NOT SELECT COLLECTIVE GLUING. A SPECIFIED TRANSFORMATION DIAGRAM DOES SELECT A COMPATIBLE ACTION GROUP, BUT STATE INVARIANCE IS AN ADDITIONAL PREMISE.**

Under the previous explicitly postulated collective Pauli-invariance model, a rigorous consequence can nevertheless be derived: each component split into odd numbers of active qubits forces one bit of entanglement across the split. Contributions from disjoint components add, and the resulting lower bound is sharp.

The statement is conditional quantum mathematics. No native provenance-to-action extraction has been supplied, no geometry is selected, and no scientific novelty or gravity breakthrough is claimed. This report develops the existing toy hypothesis rather than inventing another ensemble.

## 1. The actual provenance question

“These sectors share an origin” and “these sectors must transform together” are different assertions. A rooted graph or common record identifier establishes a relationship between records, but does not by itself specify how transformations of those records must agree.

To express the latter, suppose two sectors carry transformation groups G_1,G_2 and a common interface carries G_0, with homomorphisms

r_1:G_1->G_0, r_2:G_2->G_0.

The compatible transformation group is the fiber product

L={(g_1,g_2) in G_1 x G_2 : r_1(g_1)=r_2(g_2)}.

This is a subgroup: equality is preserved under multiplication and inversion because the r_i are homomorphisms. Its projections to G_i have equal composites into G_0. Any pair of group maps with that agreement factors uniquely through L by taking their ordered pair. This is the elementary universal property selecting L once the maps are specified.

For more interfaces the analogous group consists of tuples satisfying all restriction equalities. Rebracketing the same complete collection of equalities does not change the group. This gives a conditional associative assembly rule at the level of transformation data, not an automatic gluing of quantum states.

### Exact underdetermination counterexample

Keep the SAME groups G_0=G_1=G_2=Z_2 x Z_2 and the SAME fork-shaped diagram.

- If r_1=r_2=id, L is the diagonal group {(g,g)} of order four.
- If both r_i are trivial homomorphisms, L is the full product group, of order sixteen.

The common ancestry graph is identical; the permissible joint transformations differ. Therefore diagram shape alone cannot derive the desired coupling. Requiring faithful or otherwise specified restriction maps would be additional information, not a consequence of shared ancestry.

This is a formal counterexample about insufficient premises, not a claim that actual UQCF restriction maps are trivial. If native provenance already contains such maps, those exact maps should be recovered and tested rather than replaced by the example.

## 2. Covariance still does not imply invariant states

Even after L is determined and represented on a Hilbert space, its action only specifies how states transform. The full density-state domain is closed under every unitary action. It does not follow that every physical state must be fixed by that action.

Both of the following sets are covariant under the supplied group:

1. all density matrices;
2. the density matrices fixed by every represented group element.

They generally differ. Choosing the second as admissibility is the invariant-state axiom used in the preceding twist candidate. It requires a further justification, such as a specifically derived parallel-section condition. Even interpreting a symmetry as a gauge redundancy does not by itself prove that density representatives must be pointwise invariant: gauge-equivalent states may instead be identified as orbits, and a constrained-vector formulation would need its own derivation.

Thus there are TWO missing bridges:

- provenance -> transformation groups and compatible restriction maps;
- compatible action -> the particular physical gluing/admissibility constraint.

Neither is established by discovering an entangled invariant state after supplying both.

## 3. Conditional model retained for the theorem

Partition a fixed finite set of active qubits into disjoint components C_1,...,C_m. A component represents sectors assigned the same collective pair of loop actions. Different components have independent loop variables.

For each component C define

U_C = tensor-product_(i in C) X_i,
V_C = tensor-product_(i in C) Z_i,

acting as identity outside C. Require the globally pure density rho=|psi><psi| to satisfy

U_C rho U_C*=rho, V_C rho V_C*=rho

for every component. This is exactly the previously postulated collective-invariance rule. It is not derived by the group-diagram construction alone.

Zero active sources impose no loop constraints and leave the full original pure-state domain. The component partition and the active-source set are additional source data on the fixed Hilbert space. Their existence or uniqueness in the native theory is not asserted.

## 4. Pure realizability criterion

For a component C,

U_C V_C=(-1)^|C| V_C U_C.

If |C| is odd, no common invariant ray exists. Since global invariance of a pure density requires an invariant ray for each unitary, one odd component makes the globally pure invariant set empty, even if the state could otherwise be entangled across components.

If every nonempty component has even size, pure invariant states do exist. Pair the qubits arbitrarily within each component and put each pair in a Bell state. Their product is a common eigenvector of every U_C,V_C, and its density is invariant.

Therefore, in this model:

PURE GLOBAL REALIZABILITY IFF EVERY ACTIVE COMPONENT HAS EVEN SIZE.

Empty components are omitted. This is not a general condition on arbitrary quantum provenance; it is specific to these projective Pauli actions and this imposed invariance rule.

## 5. Exact odd-cut entanglement theorem

Assume every component has even size and rho is any admissible globally pure state. Divide the qubits into arbitrary subsets A and B. This is a subsystem partition, not a spatial surface.

Define

q(A)=number of components C for which |A intersect C| is odd.

Then B intersects the same components oddly because each full component is even.

**Theorem.** The von Neumann entanglement entropy across A|B, using base-two logarithms, obeys

S(rho_A) >= q(A) bits.

More strongly, there is a unitary change of coordinates within H_A such that

rho_A is unitarily equivalent to (I_(2^q)/2^q) tensor tau

for a density matrix tau. Every nonzero eigenvalue of rho_A consequently has multiplicity divisible by 2^q, and its rank is at least 2^q.

### Proof

Partial trace of global U_C-invariance gives invariance of rho_A under U_(A intersect C); similarly for V. This follows because conjugation on the traced subsystem drops out of the partial trace.

For an odd intersection T=A intersect C, the restricted Pauli products U_T,V_T are Hermitian unitary involutions that anticommute. Their generated algebra is unitarily equivalent to M_2 tensor I on H_T: diagonalize V_T into its plus/minus eigenspaces; U_T swaps those spaces isometrically, identifying them as two copies of a common multiplicity space. In those coordinates V_T acts as Z tensor I and U_T as X tensor I.

Commuting with both operators therefore forces a density to act as identity on that two-dimensional representation factor. Odd intersections from distinct components are supported on disjoint qubit sets, so their generated matrix algebras tensor together as M_(2^q) tensor I.

Hence rho_A has the displayed normalized form. Its entropy is

S(rho_A)=q+S(tau)>=q.

No optimization, numerical threshold or chosen entanglement functional entered the constraint. Entropy is merely a familiar expression of the derived spectral degeneracy. Because rho is globally pure, this reduced-state entropy measures entanglement, not pruning-induced information loss. The total state's entropy remains zero.

### Sharpness

For any fixed cut, in every even component choose pairs entirely within A and entirely within B whenever possible. If the component intersects A oddly, exactly one pair must cross the cut; all remaining sites can be paired internally. Put every pair in a Bell state.

The resulting product of Bell pairs is admissible and has exactly q(A) crossing pairs, hence exactly q(A) bits of entanglement. The lower bound is therefore sharp for every declared cut. The saturating pairings may differ between cuts; this construction does not select one universal state that saturates every cut simultaneously.

## 6. What is additive, and what is not

The bound adds over disjoint constrained components. It is not proportional to total source count within one component. A single even component contributes either zero or one forced bit according to the parity of its intersection with A, regardless of its total size.

It is therefore a multiplicity of independent algebraic obstructions across a partition, not a mass law or a source-strength law. Grouping four active qubits into one component versus two components changes q(A); the grouping must not be chosen after seeing a desired entanglement pattern.

This also avoids a misleading “area law” interpretation. No distance, boundary area, spatial dimension or native refinement map is defined, and the partition function q(A) is a lower bound rather than the entropy function of a uniquely selected state.

## 7. Exact no-geometry-selection counterexample

Take four qubits in ONE collective component, so the constraints are invariance under X tensor X tensor X tensor X and Z tensor Z tensor Z tensor Z.

Both states below satisfy exactly the same constraints:

psi_1 = Bell_(12) tensor Bell_(34),
psi_2 = Bell_(13) tensor Bell_(24),

where Bell=(|00>+|11>)/sqrt(2). Every individual qubit has marginal I/2 in both states.

For the same cut A={1,2}, B={3,4}:

- psi_1 has entropy zero; its reduced rho_12 is a pure Bell projector;
- psi_2 has entropy two bits; its reduced rho_12=I_4/4.

Thus the same collective rule and the same single-site data permit different pairings and different entanglement across a cut. An entanglement-based geometry cannot be uniquely inferred from this rule alone. No pairwise distance prescription is adopted here.

The exact check used standard-library Fraction arithmetic on the two 16-dimensional vectors/densities. It verified collective X/Z invariance, all single-site marginals I/2, and cut purities 1 and 1/4, including the exact I_4/4 identity in the second case. Group enumeration also checked the order-four diagonal and order-sixteen independent fiber-product examples. These are finite algebra checks, not stochastic simulations.

## 8. Relation to established mathematics

The mechanism connecting projective symmetry actions, degeneracy of reduced-state spectra and a minimum entanglement is already present in quantum-information/condensed-matter research. For example, Pollmann, Berg, Turner and Oshikawa analyze symmetry-protected double degeneracy of the entanglement spectrum and the corresponding ln(2) lower bound in a one-dimensional Haldane-phase setting: [Entanglement spectrum of a topological phase in one dimension](https://arxiv.org/abs/0910.1811).

The present finite Pauli proof does not assume that chain, its Hamiltonian, a gapped phase, or spatial topology. It is an explicit conditional theorem for the stipulated collective-source model, not a novelty claim or evidence that UQCF realizes the Haldane mechanism.

## 9. Gate scorecard

| Question | Result |
|---|---|
| Does shared ancestry alone force collective transformation? | NO: same fork supports diagonal or independent actions |
| Do specified restriction homomorphisms determine compatible transformations? | YES: fiber product, conditionally |
| Does covariance force invariant-state admissibility? | NO |
| Is collective Pauli pure compatibility exactly characterizable? | YES: all active components even |
| Does the assumed rule impose a non-fitted entanglement minimum? | YES: S(A)>=q(A) bits, sharp |
| Is that a universal additive source-strength law? | NO: cut/component parity, not total count |
| Does the rule select a state or geometry? | NO: exact four-qubit counterexample |
| Is the missing provenance-to-gluing bridge recovered? | NOT ESTABLISHED |
| Should a native canary ensemble follow? | NO |

## 10. Research decision

The conditional math has moved from the existence of a Bell-state example to a general, sharp cut-entanglement theorem. Retain that result and its exact assumptions.

The native derivation remains blocked at a specific point: provenance must supply transformation restriction maps AND a physical reason for the chosen gluing constraint. No further Pauli-loop scan will derive those premises. Future work should recover or specify those maps and that constraint before proposing a geometry statistic.

Do not use “common origin” as a substitute for either bridge, do not equate covariance with invariance, and do not rename the entropy bound a force or area law. These boundaries preserve the mathematical result while exposing what remains unexplained.

## Source and continuity note

- UQCF_Nonreplica_Twist_Gate.md, previous visible-thread report; source identifier libfile_049da4affb0481919831ab3a2d6cc7ee. Its common-invariant-ray correction remains controlling.
- UQCF_Replica_Incidence_Canary.md, earlier visible-thread report; source identifier libfile_c8fa26f3868c8191bc5fbdd061b64a2c. No replica extension or copied marginal was used here.
- The literature source above was consulted to check the novelty boundary. The finite proofs in this report are given explicitly.

The Library skill was used to save this standalone research checkpoint. No prior report was overwritten and no unreviewed v9 version was assigned.
