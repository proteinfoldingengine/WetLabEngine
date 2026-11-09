# Edge-provenance symmetry matching and the pure-completion obstruction

Date: 2026-09-05. Unnumbered theorem-first continuation.

## Result

**EDGE PROVENANCE CANONICALLY DEFINES SYMMETRY MATCHING; THIS DOES NOT DERIVE INVARIANT PURE-STATE GLUING.**

Unlike the preceding source-token and loop examples, the construction here starts directly from the existing bipartite density data Omega_ij and their given local-unitary covariance. No copy slots, loop operators, chosen metric, purification or cross-system Hilbert-space identification are added.

A canonical relation between local symmetry groups can be extracted. Its correlated part is described by isomorphic quotient groups. This supplies one mathematically legitimate answer to the matching-map question, at the level of symmetries rather than vectors.

However, the induced global symmetry generally acts on the space of compatible completions rather than fixing each completion. Requiring global invariance would be a new constraint. Exact averaging shows that it cannot shrink the full mixed-state marginal image; an exact GHZ example shows that it can eliminate every pure completion of otherwise valid data.

No native random ensemble was run. The group structure, averaging theorem and counterexample are exact. The claims are applications of established group and quantum-state mathematics, not new physical laws.

## 1. Start with the frozen primitive

For an edge state Omega on H_i tensor H_j, let G_i=PU(H_i) and G_j=PU(H_j), the local unitary groups modulo scalar phases. They act on density matrices by conjugation, which is independent of the representative chosen in each phase class.

Define the closed stabilizer subgroup

H_Omega = {(g,h) in G_i x G_j : (g tensor h) Omega (g tensor h)* = Omega}.

This subgroup is uniquely determined by the edge state and the frozen subsystem structure. Under a change of local basis, it transforms by the corresponding conjugation of the two ambient groups. Scalar phases have already been removed, so the central-phase obstruction to a deterministic map H_i->H_j does not apply to this construction.

This is a symmetry relation, not a selected transformation and not a transport map between state vectors.

## 2. The canonical shared quotient

Let P_i and P_j be the two projections of H_Omega. Define the independent stabilizer kernels

N_i={g in P_i : (g,e) in H_Omega},
N_j={h in P_j : (e,h) in H_Omega}.

They are normal subgroups of P_i and P_j. There is a canonical isomorphism

phi_Omega:P_i/N_i -> P_j/N_j,

specified by phi_Omega(g N_i)=h N_j whenever (g,h) belongs to H_Omega.

To check well-definedness, two partners of the same g differ by an element of N_j; changing g within its N_i coset does not change the resulting N_j coset. Closure under multiplication makes phi a homomorphism, and exchanging the factors gives its inverse. Normality follows by conjugating the pairs (n,e) or (e,n) inside H_Omega.

Consequently H_Omega consists exactly of those projected transformations whose quotient classes match through phi_Omega. This is Goursat's subgroup construction, applied to density-state stabilizers; see [Bauer, Sen and Zvengrowski, A Generalized Goursat Lemma](https://arxiv.org/abs/1109.0024), Theorem 2.1.

No chosen coset representative or basis is needed for the quotient isomorphism. Writing explicit matrices for it can require coordinates, but the relation itself does not.

## 3. What the matching object detects

### Product edge data

For Omega=rho_i tensor rho_j, partial trace implies that any preserving pair must separately preserve rho_i and rho_j. Thus H_Omega is the product of the two local stabilizers. P_i=N_i and P_j=N_j, so the shared quotient is trivial.

### Classically correlated qubits

For Omega=(|00><00|+|11><11|)/2=(I tensor I+Z tensor Z)/4, a preserving local pair must send its Z axes to either the same original signs or both reversed signs. Rotations about each axis remain independent. The correlated quotient is Z_2: the two axis-reversal parities must agree.

Thus nontrivial symmetry matching can arise from separable correlations. It is not an entanglement witness by itself. The coordinate-free object is the quotient relation; the displayed Z axes merely describe this example.

### Maximally entangled qubits

For Omega=|Phi+><Phi+|, a coordinate calculation gives V=e^(i alpha) conjugate(U) for a preserving pair (U,V). After quotienting scalar phases, the stabilizer is the graph of an isomorphism of the local projective unitary groups and the independent kernels are trivial.

This describes the symmetries of an already supplied entangled state. It does not derive entanglement by adding a new law. Nor does the coordinate formula provide a fully local-unitary-covariant linear Hilbert-space map extracted from an arbitrary bipartite density.

No claim is made that a nontrivial quotient exists for every edge or generically in the native generator ensemble.

## 4. Global assembly without invented loop data

For a complete declared edge tuple y={Omega_ij}, define

Gamma_y = {(g_i) in product_i G_i : (g_i,g_j) in H_(Omega_ij) for every edge ij}.

This is a compact subgroup. It is exactly the stabilizer of the complete visible edge tuple under the frozen product-local action. Intersecting the same edge conditions in any order gives the same subgroup, so its assembly is associative as a constraint construction.

Compatible restrictions on a subgraph are obtained by projecting global tuples; they satisfy every retained edge condition. The projected global group need not equal the full stabilizer reconstructed from the smaller subgraph, since removing constraints can create additional symmetries. Surjective reduction is not claimed.

The edge quotient groups are an alternative description of these matching conditions. They do not supply cross-system state-vector transitions, a cocycle source charge, or a positive additive multiplicity law.

## 5. Action on a realization fiber is not fixation of its points

Let F(y)={X>=0 : Tr X=1, M_E(X)=y}. If X belongs to F(y) and g belongs to Gamma_y, then

g X g* belongs to F(y).

This follows from covariance of the partial trace and the definition of Gamma_y. Global purity is preserved by the unitary conjugation as well. Therefore Gamma_y acts on both the full-density fiber and its pure subset.

The conclusion is not that g X g*=X. The group may move X to a different compatible completion carrying different hidden information.

Consequently, extracting a legitimate symmetry matching object solves only the symmetry-data problem. It does not justify replacing the fiber by its fixed points. That step would repeat the covariance-versus-invariance mistake identified in the preceding gate.

## 6. Exact no-exclusion theorem for full-density data

**Theorem.** Every nonempty full-density fiber F(y) contains a Gamma_y-invariant density matrix.

Proof: choose any X in F(y). Average its conjugates over normalized Haar measure on the compact group Gamma_y:

X_bar = integral_(Gamma_y) g X g* dmu(g).

Positivity and trace one are preserved. Every conjugate has the same edge data y, and the marginal map is linear, so M_E(X_bar)=y. Translation invariance of Haar measure makes X_bar fixed by Gamma_y.

The conjugation action is well-defined without selecting continuous representatives of projective unitaries; scalar phases cancel. This is an existence proof, not a proposal to perform a physical averaging operation or pruning process.

It follows that demanding the existence of a stabilizer-invariant mixed completion yields EXACTLY THE SAME visible admissible body as the frozen full-density theory. It adds no forbidden visible data. An additional nonconvex condition, especially rank one, is not preserved by this averaging argument and must be checked separately.

## 7. Complete pure-state counterexample

Take three qubits with all three pair marginals

Omega_ij=(|00><00|+|11><11|)/2.

Every state

|GHZ_theta>=(|000>+exp(i theta)|111>)/sqrt(2)

is a valid globally pure realization of the identical edge tuple y.

The full compatible density fiber can be computed exactly. Zero pair probability for mismatched bits, together with positivity, forces support into span{|000>,|111>}. The pair probabilities fix the two diagonal entries at 1/2. Thus every compatible global density has the two-dimensional block

X(c)=[[1/2,c],[conjugate(c),1/2]], with |c|<=1/2,

embedded in that support. Rank one holds exactly when |c|=1/2.

The single-site Z_1 belongs to Gamma_y because it preserves every pair marginal. It sends c to -c. Hence any Gamma_y-fixed completion must have c=0 and is mixed. No pure realization in this fiber is fixed by Gamma_y.

The unique fixed completion is the equal incoherent mixture of |000> and |111>. Its existence and full stabilizer invariance also follow from the averaging theorem and uniqueness under the necessary Z_1 constraint.

Therefore imposing invariant PURE completion would discard a manifestly valid pure-state edge tuple. Native marginal covariance does not entail this rule. Interpreting the phases as gauge would permit quotienting their orbit; it still would not require an invariant rank-one representative inside that orbit.

## 8. Exact verification

Python Fraction/integer arithmetic verified:

- GHZ+ and GHZ- have exactly identical complete pair marginals;
- conjugation by Z on the first qubit interchanges their distinct density matrices;
- their average preserves every pair marginal;
- the average has purity 1/2;
- the only computational-basis strings satisfying all pair equality-support conditions are 000 and 111.

The full-fiber support proof and the group/averaging statements are analytical. No stochastic samples, numerical ranks, fitted tolerances or purported physical dynamics were used.

## 9. Updated assessment

| Gate | Outcome |
|---|---|
| Extract matching data directly from Omega_ij | PASS as a canonical symmetry relation |
| Avoid forbidden deterministic Hilbert-fiber map | PASS; the output is a relation/isomorphism of group quotients |
| Assemble edge matching without chosen loop operators | PASS as the visible-data stabilizer Gamma_y |
| Derive a nontrivial matching quotient for every source | NOT ESTABLISHED; product-state quotient is trivial |
| Infer a source strength or multiplicity law | NOT ESTABLISHED |
| Infer that all compatible global states are invariant | FAIL by exact GHZ fiber |
| Change the full-density admissible image by requiring an invariant completion | FAIL by Haar averaging theorem |
| Preserve all valid pure-state data under invariant-completion requirement | FAIL by exact GHZ fiber |
| Authorize another native symmetry/commutant ensemble | STOP |

## 10. Research decision

Retain the positive mathematical result: the frozen edge state does supply canonical SYMMETRY matching data. It would now be too broad to say that no matching relation of any kind can be extracted from provenance. The frozen no-go for a deterministic covariant map between Hilbert fibers remains untouched.

Retain the negative result: this matching describes symmetries of information already supplied. It acts on the completion fiber and does not become a source-to-realizability law merely by requiring invariance.

This is an exact closure of the symmetry-to-invariant-gluing route, not a license to resume commutant or approximate-symmetry mining. A future source law must distinguish physical provenance restrictions from reparameterizations or symmetries of present data and justify any restriction on the completion fiber independently.

The current result is a useful clarification and canonical construction, not a gravitational breakthrough. The missing physical premise is narrower, but it has not disappeared.

## Continuity and sources

- The preceding visible-thread checkpoint UQCF_Shared_Provenance_Joint_Constraint_Gate.md distinguished common ancestry, restriction homomorphisms, covariance and invariance. This report supplies one particular native-state-derived matching object, without claiming it is the required physical coupling.
- The frozen local-unitary covariance and central-phase Hilbert-map obstruction remain controlling. All output groups use density conjugation, so no phase-sensitive vector map has been introduced.
- [A Generalized Goursat Lemma](https://arxiv.org/abs/1109.0024), Bauer, Sen and Zvengrowski, Theorem 2.1, supplies the established group-theoretic context. No novelty is claimed for the quotient construction or compact-group averaging.

The Library skill was used to retain this report. No historical artifact was overwritten, and no unrecovered v9 version was assigned.
