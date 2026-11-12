# UQCF-GEM v9.72 — Native Incidence and Composition Gate

## Adjudication

**NATIVE FIXED-GRAPH INCIDENCE IS AVAILABLE. A SOURCE-TO-NEW-INCIDENCE ASSIGNMENT IS NOT ESTABLISHED IN THE INSPECTED DEFINITIONS. ASSOCIATIVE COMBINATION OF SPECIFICATIONS DOES NOT GUARANTEE COMPOSITION OF OVERLAPPING QUANTUM REALIZATIONS.**

This gate resolves the target proposed in v9.71 by separating three operations: repeating an existing obligation, combining disjoint systems, and combining overlapping specifications. None supplies the missing provenance-to-obligation law by itself. The result is an audit and elementary exact clarification, not a gravity discovery or a claim of new quantum-marginal mathematics.

The analysis is entirely atemporal. Partial trace denotes static restriction to a subsystem observable algebra.

## 1. Sources inspected and the bounded finding

Read in full for this gate:

- `UQCF_GEM_v9_50_Source_Dependent_Admissibility_Existence_Gate.md` — frozen tensor factors, density domain and edge marginal map; an additional source representation is required to change admissibility.
- `UQCF_Provenance_Multiplicity_Gate.md` — provenance composition, equivalence and the relation to quantum extensions were not supplied by the inspected native model; additive multiplicity alone does not imply a compatibility coupling.
- `UQCF_Replica_Incidence_Canary.md` — the extra B-role factors, source-token assignment, copy-role identifications and equal AB marginals are explicitly postulated together.

Immediate lineage: v9.69 established fixed-architecture pure-state feasibility sectors conditional on equal-pair obligations; v9.70 did not derive those obligations from common realization, equal locals or covariance; v9.71 classified exact intersection composition for additive scalar sources.

The archive does contain distinct native subsystem factors and graph edges. It would be incorrect to say it contains no incidence. What is absent from these inspected definitions is a canonical assignment from source/provenance to additional independent factors or additional joint obligations, together with the comparison maps needed to compose them. This is a bounded finding about the supplied definitions, not a claim that every historical project artifact has been searched.

## 2. Repeated labels are not independent quantum slots

For two distinct tensor factors B and C, the standard embeddings of their observable algebras into the global algebra commute. They do not become the same embedding when their provenance labels agree.

More precisely, let alpha and beta be injective unital algebra maps from M_d into a common algebra, with commuting images and d > 1. They cannot be equal. If alpha=beta, then for all X,Y,

\[
\alpha([X,Y])=[\alpha(X),\beta(Y)]=0.
\]

Injectivity would imply every pair of matrices in M_d commutes, a contradiction.

Thus literal identification of the observable algebra and independent tensor-factor replication are different constructions. The argument does not prohibit equality of selected state expectations on the two algebras; that is a constraint on the state, as in v9.70. Nor does it prohibit explicit isomorphisms between separate factors. Those isomorphisms do not identify their global embeddings.

## 3. Disjoint composition: existence, without a shared-interface effect

For disjoint systems G and H, the supplied tensor factors give a canonical product state for any specified density operators:

\[
\rho_G\otimes\sigma_H.
\]

It reproduces both component states. It is globally pure when both inputs are pure. Tensor product is associative up to the standard reassociation of factors.

For the full-density domains and a graph union having no cross edges,

\[
\mathcal A_{G\sqcup H}=\mathcal A_G\times\mathcal A_H.
\]

Proof: restricting a global density gives valid component densities, proving one inclusion. Tensoring witnesses for any two component edge data proves the reverse inclusion.

The corresponding equality is not asserted for arbitrary globally pure domains: an entangled pure state across G and H can have mixed component marginals. Product composition of pure witnesses proves existence for the product of the component pure images, not exhaustion of the larger pure image.

Disjoint composition supplies a baseline realization, but does not impose that two partners share identical correlations with one A. Introducing a common interface changes the problem.

## 4. Overlapping composition: an exact obstruction

Given states on AB and AC, agreement on A is necessary for a joint ABC realization. It is not sufficient, even if both specified states are pure.

Take qubits and prescribe

\[
\rho_{AB}=|\Phi^+\rangle\langle\Phi^+|,
\qquad
\sigma_{AC}=|\Phi^+\rangle\langle\Phi^+|.
\]

Both restrictions to A equal I_2/2. Suppose a positive normalized tau_ABC realizes both. Since its AB marginal is pure, positivity forces

\[
\tau_{ABC}=\rho_{AB}\otimes\tau_C.
\]

For completeness, let P be the rank-one support projector of rho_AB and Q=I-P. The positive operator tau has zero expectation on the subspace Q tensor H_C. Positivity then annihilates that subspace, including its cross blocks, so tau is supported on P tensor H_C and factors as stated.

Consequently its AC marginal is (I_2/2) tensor tau_C, which cannot equal a pure Bell projector. Contradiction. Allowing a mixed global completion does not repair the obstruction.

Define the matching-overlap set

\[
\mathcal F=\{(\rho_{AB},\sigma_{AC}):\rho_A=\sigma_A\}.
\]

The actual marginal map from D(ABC) has image strictly inside F. Therefore no total composition map on all of F can preserve both prescribed component states. This impossibility holds before asking whether the map is canonical, covariant, or associative.

The Bell witness is a standard compatibility obstruction used here to fix the precise meaning of composition. It is not a new physical law.

## 5. What remains associative

For three fixed subsystem specifications AB, AC and AD, their simultaneous realization fiber is

\[
\{\tau_{ABCD}:\tau_{AB}=\rho,\ \tau_{AC}=\sigma,\ \tau_{AD}=\upsilon\}.
\]

The order and parenthesization of these equations do not change this set. It may be empty. Thus associative conjunction of specifications is compatible with failure of existence of a joint state.

There is also a precise projection issue. For any map p and subsets C,D of its domain,

\[
p(C\cap D)\subseteq p(C)\cap p(D),
\]

and equality need not hold: separate witnesses for the same visible value need not be a common witness. In the Bell example, take the domain D(ABC), let C prescribe the AB Bell state, D prescribe the AC Bell state, and let p restrict to A. Then p(C)=p(D)={I_2/2}, while C intersection D is empty.

This explains why multiplying source counts in a replica hierarchy is not the same operation as intersecting its projected pair-state sets. The larger incidence object retains simultaneous realization requirements that the separate projections omit. It is a legitimate way to avoid v9.71's exact-intersection premise, but it requires the larger incidence object in the first place.

## 6. Gate table

| Candidate composition | What is supplied | What is not derived |
|---|---|---|
| Repeat one fixed obligation | Idempotent conjunction | Additive magnitude response |
| Combine disjoint systems | Tensor-product realization | Shared-interface obligations or interaction |
| Unite overlapping specifications | Simultaneous marginal equations | Guaranteed joint realization |
| Add replica slots per source token | Conditional shareability hierarchy | Native source-to-slot assignment and equal-pair law |

Graph relabeling does not create a new tensor factor. Existing degree counts distinct native neighbors, but interpreting degree as physical source strength and requiring equal relations to those neighbors remain separate claims. The graph alone does not impose those equalities.

## 7. Decision and handoff boundary

The requested native-incidence derivation is not established. The mathematical controls survive: independent incidences can impose genuinely joint compatibility conditions; their consequences can be nontrivial without fitting a response amplitude. But the source-to-incidence assignment remains physical input.

**Close the repeated search for this assignment inside the inspected fixed architecture.** Do not schedule another native replica simulation or rename the conditional shareability result as source-derived gravity.

Any continuation of this specific mechanism must supply a concrete new axiom or an additional source artifact defining the missing structure. Its review must identify: which incidences are physical; which provenance equivalences preserve them; how sources determine obligations; and whether composition means partial joint realizability or an everywhere-defined operation preserving component states. The latter is already excluded on unrestricted overlapping quantum inputs by section 4.

This gate does not select a replacement axiom. It prevents mathematical associativity at the specification level from being mistaken for a derived physical coupling or a guarantee that realized sources compose.

## 8. Evidence boundary

The algebra-embedding obstruction, disjoint full-density factorization, overlapping Bell obstruction, and projection inclusion have explicit proofs above. No numerical simulation or new numerical verification was performed or needed. The source audit is limited to the named reports. No claim is made that gravity before time is impossible; the specific missing coupling has not been derived.
