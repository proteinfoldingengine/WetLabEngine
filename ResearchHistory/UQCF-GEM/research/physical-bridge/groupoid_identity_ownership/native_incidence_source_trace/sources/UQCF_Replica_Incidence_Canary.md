# Replica-incidence canary: explicit coupling and exact falsification

Date: 2026-09-05. Unnumbered new-axiom candidate, following the provenance-multiplicity gate.

## Outcome

**CONDITIONAL MULTIPLICITY-SENSITIVE COMPATIBILITY FOUND; NATIVE PROVENANCE AND PURE-STATE TRANSFER NOT ESTABLISHED.**

One explicit source-to-gluing hypothesis produces a nonconstant compatibility hierarchy and a certified joint-composition obstruction without specifying a force, response amplitude or optimization objective. The consequence is ordinary quantum shareability/monogamy, not a newly discovered quantum law. The hypothesis does not follow from frozen provenance, and its mixed-state construction cannot silently be transferred to a fixed globally pure realization.

No random ensemble, fitted response or physical simulation was run. Small exact rational matrix identities were checked to validate the explicit witness. No v9 version number is assigned because later version artifacts have not been recovered.

## 1. What is postulated

**Replica-incidence hypothesis:** each additional elementary source token requires one additional interchangeable partner slot, and all source–partner pair marginals must agree as marginals of one positive normalized global state.

This is a candidate new law, not a provenance extraction theorem. The following ingredients are being supplied together and must remain visible:

- a distinguished bipartite interface A–B;
- a finite set of source tokens, modulo bijective relabeling;
- one extra B-role factor per token;
- specified identifications of those copies with the B role;
- equality of all A–B-role marginal states;
- global PSD normalization on the enlarged tensor product.

Counting tokens is intrinsic to this stipulated finite-set provenance model. It is not shown intrinsic to the frozen UQCF provenance. Replacing one token by two is not an equivalence in this candidate. If native presentation equivalence permits such a replacement, the candidate's count does not descend and the candidate fails that transfer gate.

The hypothesis changes global degrees of freedom as well as gluing constraints. It is therefore NOT a successful deformation of gluing alone with all original Hilbert factors held fixed. No Hilbert-space transition map is extracted from a density matrix. Copy-role identifications are explicit new data; their introduction is part of the cost of the candidate.

## 2. Source composition and neutral sector

Let source provenance be finite sets R up to bijection, with composition disjoint union. Define n=|R| and k=n+1, where the original partner B_1 is retained even for n=0.

Disjoint union gives n(R disjoint-union S)=n(R)+n(S), with the empty set neutral. Composition is associative and symmetric up to the ordinary relabeling isomorphisms. This is parallel multiplicity, not reversible operation composition, so the preceding positive-additive group obstruction does not apply.

For fixed H_A and H_B define

E_k = {rho_AB : there exists sigma on H_A tensor H_B^tensor-k, sigma >= 0, Tr sigma=1, and sigma_ABj=rho_AB for every j}.

All pair marginal equalities use the declared copy-role identifications. A permutation-invariant extension may be obtained by averaging over partner permutations without changing any pair marginal. This statement concerns mixed-state extensions; averaging is not a method for preserving a pure global state.

At n=0, k=1 and E_1=D(H_A tensor H_B). Thus the neutral sector exactly recovers the two-factor FULL-DENSITY baseline. It does not claim recovery of every frozen pure-state graph model.

For a larger original graph G, a possible explicit mixed-state generalization would require sigma restricted to G to equal X_G and impose equality between its original AB marginal and every extra AB_j marginal. At n=0 this again recovers the original full-density domain and its fixed marginal map. The pure-state obstruction to that generalization is proved below.

## 3. Covariance and reduction

If rho transforms by U_A tensor U_B, transform its extension by U_A tensor U_B^tensor-k. Membership in E_k is unchanged. Permuting replica labels is also immaterial. This is covariance of the declared abstract role construction.

If the replicas are represented as independently coordinatized physical subsystems with maps i_j:H_B->H_Bj, independent local basis transformations must transform i_j as well. Keeping the identifications fixed while rotating replicas independently would not preserve the equality constraints. Therefore unrestricted native local covariance is not certified by merely writing equal marginals; the added role-identification data must be included in the kinematic object.

Tracing out partner slots gives

E_(k+1) subseteq E_k.

All separable pair states pass every level: if rho_AB=sum_t p_t alpha_t tensor beta_t, then sigma=sum_t p_t alpha_t tensor beta_t^tensor-k is an extension. In particular, increasing count need not force any response at all for such states. This is an exact null family.

Partner deletion and local coordinate covariance are established. They are not a proof of every possible native graph-coarsening or subsystem-reduction axiom.

## 4. What associative composition does and does not guarantee

A specification with n tokens has k=n+1 partner slots. Combining n and m tokens keeps one common original B_1 and takes disjoint additional slots, giving k_total=n+m+1. Associativity holds at the incidence-specification level.

For specifications sharing A and B_1, however, separate quantum extensions need not possess a joint extension on the union of slots. Equal overlap marginals are necessary but not sufficient for quantum gluing.

Consequently,

E_(n+m+1) subseteq E_(n+1) intersection E_(m+1),

and the inclusion can be strict. The right side forgets joint realizability on the combined incidence object.

This does not violate associativity. It distinguishes associative combination of constraints from guaranteed existence of a state satisfying the combined constraints. If the intended source-composition axiom instead requires every pair of individually admissible source realizations to compose without obstruction, this candidate fails that stronger axiom.

Entirely disjoint A–B systems can be combined by tensor product of extensions. Their composition is not the shared-interface composition above. No “interaction” between disjoint sources is thereby derived.

## 5. Exact qubit obstruction, derived rather than fitted

Take H_A=H_B=C^2. Choose a singlet projector P_- as a witness on the pair, and let F=Tr(P_- rho_AB). Its choice is a diagnostic, not a preferred basis or singlet law inserted into the candidate. The whole witness family transforms under local unitaries; feasibility itself is basis invariant.

On A B_1 ... B_k define

Q_k = sum_(j=1)^k P_-^(A Bj).

If an equal-marginal extension sigma exists, then Tr(Q_k sigma)=k F.

Writing spin operators S_A=Pauli_A/2 and J_B=sum_j Pauli_Bj/2 gives the operator identity

Q_k = (k/4) I - S_A dot J_B.

For partner total spin j and joint spin j+1/2, the scalar product has eigenvalue j/2. For joint spin j-1/2, when j>=1/2, it has eigenvalue -(j+1)/2. Since j<=k/2, the greatest eigenvalue of Q_k is (k+1)/2, attained in the maximal partner-spin sector with the lower joint spin.

Therefore every k-extendible pair state obeys

F <= (k+1)/(2k).

This is a necessary witness inequality for general pair states; it is not asserted sufficient for arbitrary two-qubit densities. The normalized maximal-eigenspace projector is partner-permutation invariant and rotation invariant, so its pair marginals are equal Werner states saturating the bound. Thus the bound is sharp on that symmetric family.

| Extra tokens n | Partner count k | Maximum singlet overlap |
|---|---|---|
| 0 | 1 | 1 |
| 1 | 2 | 3/4 |
| 2 | 3 | 2/3 |

The decreasing upper bound is a compatibility limit, not a dynamical response or a choice of the state after adding a token.

## 6. Complete finite witness for failure of automatic gluing

Set

rho_* = (3/4) P_- + (1/12)(I-P_-).

It is PSD, normalized, and has F=3/4.

For k=2 write Q=Q_2 and define

sigma_2 = Q^2/3 - Q/6.

The exact identities checked are:

- Q(Q-I/2)(Q-3I/2)=0;
- sigma_2 is real symmetric;
- sigma_2^2=sigma_2/2;
- Tr sigma_2=1;
- Tr_B2 sigma_2=Tr_B1 sigma_2=rho_* under copy identifications.

Real symmetry and the quadratic identity put the eigenvalues of sigma_2 in {0,1/2}; trace one makes it a positive normalized rank-two state. This supplies an explicit extension, not merely a solver claim.

For k=3 the exact identity

Q_3(Q_3-I/2)(Q_3-3I/2)(Q_3-2I)=0

and real symmetry imply Q_3<=2I. Any equal-marginal three-partner extension of rho_* would have Tr(Q_3 sigma)=3*(3/4)=9/4>2, impossible.

Hence rho_* belongs to E_2 but not E_3. Two one-token specifications, each separately feasible for this pair state, have an infeasible two-token joint specification. The singlet-overlap exclusion margin is 1/12.

Verification used Python standard-library Fraction arithmetic and explicit 8x8 and 16x16 matrices, with no floating-point tolerances. It checked the displayed annihilating polynomials, marginal identities and projector normalization. A first optional SymPy attempt was unavailable; the successful verification required no external symbolic package. The proof does not depend on the computational check.

This is a known quantum marginal/shareability phenomenon. It is not a newly discovered source law.

## 7. Pure-state transfer obstruction

The explicit sigma_2 above is mixed, of rank two. Calling it a globally pure native realization would be incorrect.

More generally, suppose the enlarged state sigma_GC is required to preserve the entire original pure state X_G=|psi><psi| as its marginal on G. Then

sigma_GC = |psi><psi| tensor tau_C.

Proof: the marginal has support on a one-dimensional subspace of H_G. Positivity forces sigma_GC to have support in that subspace tensor H_C, which gives the factorization. This holds even when the enlarged state is allowed to be mixed.

In particular, for an additional partner B_j outside G,

sigma_ABj = rho_A tensor tau_Bj.

It cannot equal a correlated original rho_AB. Thus preserving the full original pure realization while requiring a correlated pair relation to reappear with an added partner is impossible already at the first replica.

If the original system is just pure AB, only product pure pair states survive the first extra partner requirement; they survive all further ones by product extension. The graded mixed-state hierarchy does not survive that pure two-factor specialization.

One could instead preserve only selected marginal data, change the original global state, or allow an ancillary purification. Those are distinct enlarged specifications. This report does not silently adopt any of them or claim that they recover the native pure graph theory. Allowing a hidden ancilla solely to rescue a mixed witness would add another degree-of-freedom premise.

## 8. Native provenance and gravity discrimination

The multiplicity effect is not a harmless record label: under the explicit replica rule it removes baseline pair states at higher counts. However, the rule identifying source tokens with equal-marginal replica obligations is POSTULATED. It is not derived from an Omega_ij provenance state, a source observable, or the neutral theory.

The derived inequality is standard quantum monogamy once replica gluing is required. The coefficient and monotonicity in that inequality are not fitted, but the choice of replica gluing rather than another source law is new physical input.

No canonical state selection follows when a baseline state becomes excluded. There is no derived attraction, sign of mechanical response, exterior universal field, spatial range or pruning-to-geometry bridge. Increasing replica count is not a demonstrated native-resolution limit. Separable states remain compatible at every count.

Therefore the proper claim is a concrete example of how an explicit incidence axiom can produce multiplicity-sensitive feasibility—not provenance-derived gravity and not an axiom uniquely selected by covariance and composition.

## 9. Gate adjudication

| Requirement | Result |
|---|---|
| Explicit source object and equivalence | PASS for stipulated finite-token model; not native-derived |
| Additive, relabeling-invariant multiplicity | PASS within that model |
| Neutral recovery | PASS for full-density baseline; not a full native pure-state transfer |
| Covariance | PASS with declared copy-role structure; unqualified native covariance not established |
| Associative specification composition | PASS |
| Guaranteed gluing of individually valid overlapping realizations | FAIL by exact witness |
| Proper nonconstant feasibility hierarchy | PASS in the mixed-state construction |
| Non-inserted quantitative consequence | PASS conditionally: sharp quantum shareability bound |
| Preserve correlated original globally pure realization | FAIL already at first replica |
| Derived native provenance-to-incidence law | NOT ESTABLISHED |
| Distinguish consequence from standard quantum shareability | FAIL as a gravity-specific discriminator |
| Launch native ensemble simulation | STOP |

## 10. Research decision

Retain this construction as a mathematical control and explicit coupling example. Do not promote it to the next native canary ensemble and do not add a relaxation objective to manufacture a response.

The next admissible theoretical target must specify how actual provenance supplies higher incidence without copying an entire correlated relation across new partner factors, and how the zero-source and pure-state domains compare. It must also say whether source composition means associative constraints with potentially empty joint fibers or an everywhere-defined gluing of realized sectors. Those are different axioms; the example separates them exactly.

## Sources and novelty boundary

- Prior checkpoint: UQCF_Provenance_Multiplicity_Gate.md, source identifier libfile_7ada8bf4b3f88191845ed461fb6c04c2.
- Frozen architecture: UQCF_GEM_v9_50_Source_Dependent_Admissibility_Existence_Gate.md, source identifier libfile_dd4cb2b8d6d8819186eebb55fc4ee513; read in full in the preceding gate, setting reconfirmed here.
- Jakab, Solymos and Zimboras, [Extendibility of Werner States](https://arxiv.org/abs/2208.13743): established literature on one-/two-sided equal-marginal extension, its symmetry reductions and exact compatibility bounds. This report derives its small-qubit witness explicitly; it does not claim novelty for shareability or the spin-spectrum method.
- Chen, Ji, Kribs, Lutkenhaus and Zeng, [Symmetric Extension of Two-Qubit States](https://arxiv.org/abs/1310.3530): an independent established characterization of the two-qubit symmetric-extension problem. No new general two-qubit criterion is claimed here.

The Library skill was used to retain the prior gate and save this result. Existing research artifacts were not modified.
