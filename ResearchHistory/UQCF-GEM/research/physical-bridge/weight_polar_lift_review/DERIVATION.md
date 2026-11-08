# Polar lift of the retained-pair weight variation

## 1. Question and scope

Can the weight-only part of the V1694.4 product action supply a well-typed retained-pair dual covector, rather than only a scalar change of action? This note derives one canonical mathematical lift of the complete quadratic weight-variation functional and gives its exact quotient-admissibility condition. It does not derive a native P1 event-to-pair-weight map or identify the historical support current with that lift.

This is a real, finite-dimensional, fixed-ledger result. The branch form is fixed and symmetric positive semidefinite. Connection A, test-pair arguments, retained ledger, product kernels, and orientation are held fixed in the weight-only variation. The direction mu is supplied independently of the desired response. Moving carriers, births/deaths, changes of product, and changes of branch metric require separate terms and are not represented by this theorem.

## 2. Original source evidence and provenance

All sources in SOURCE_PACKET.json are frozen at research commit 8d827f647916c7335272aadc38f7415f11d89c55, with byte counts, Git blob IDs and SHA-256 digests. The reviewer receives their full texts, not selected excerpts.

- V1691.1, `component_spaces.V_oplus`, defines the primal as bilinear residual maps K: V_B x V_B -> V_B, a retained-pair weighted form, and a retained-pair dual. Its branch form is positive semidefinite; `dual_admissibility.oplus_dual` disallows undeclared dense pairs. Degeneracy therefore cannot silently be treated as an invertible metric.
- V1694.4, `product_action`, gives I = sum_(e,a) w_(e,a) <delta_(e,a),delta_(e,a)>_B. Its `support_current.components.delta_w` gives sum_a (delta w_a)<delta_a,delta_a> and calls for an induced scalar-weighted pair-current covector. Its `support_current.lives_in` expressly requires mapping support variations back to retained-pair dual covectors. The source does not supply the complete identification of this polar lift with rho_support, including conventions and transport to a comparison endpoint.
- V1696.5 is supplied in full as the actual pair-class/support-weight proposal to which this action-side question is relevant. This note does not infer a native pair-support membership/update rule merely from its signatures or support-grade sums.
- FCV PROOFS.md is supplied in full to fix the inherited P1 setting. P1 grade pushforward is not being denied or rederived. Neither a toy nine-site construction nor an unproved V1696.3 -> V1696.5 implementation lineage is used.

Edge index e can be absorbed into the finite pair-ledger index a. This is bookkeeping, not an assertion that distinct local product spaces or endpoint transports are identical. The theorem applies to a declared single residual space, or a declared finite direct sum of local residual spaces. Any endpoint identification needed for a physical comparison remains additional data.

## 3. Typed finite-dimensional setup

Let U and B be finite-dimensional real vector spaces, with fixed symmetric positive-semidefinite bilinear form h on B. Let V be a declared real linear subspace of Bil(U x U,B). In the V1691.1 case U=B=V_B. Let a range over a fixed finite ledger of test pairs (x_a,y_a) in U x U, and define the linear evaluation map

    E : V -> B^m,    (E K)_a = K(x_a,y_a) = K_a.

Repeated or linearly dependent evaluations are permitted. Set G : B^m -> (B^m)* by (G b)(c)=sum_a h(b_a,c_a). For any real vector v of ledger coefficients define D_v as diagonal multiplication by v on the direct sum. In formulas E* D_v G E, D_v on the dual denotes the same coefficient scaling. No coordinates or inverse of h are required.

Let w_a >= 0 be the baseline weights and let delta in V be the actual residual. The fixed-ledger action is the quadratic functional

    I_w(K) = sum_a w_a h(K_a,K_a),    K in V.

Let mu be a supplied real coefficient direction. Algebraically the coefficient derivative in the ambient weight vector space is defined for any mu. If weights must stay nonnegative, a two-sided feasible direction at w_a=0 has mu_a=0; a one-sided direction t>=0 may instead have mu_a>=0 at such a coordinate. Distinguish these domains explicitly.

## 4. Derivation of the polar covector

For every K in V the exact coefficient variation is

    I_(w+t mu)(K) - I_w(K) = t F_mu(K),
    F_mu(K) = sum_a mu_a h(K_a,K_a).

This formula is exact, with no residual variation and no limit error. Polarize the complete quadratic functional:

    B_mu(K,L) = [F_mu(K+L)-F_mu(K-L)]/4
              = sum_a mu_a h(K_a,L_a).

Expansion and symmetry of h give the second equality. This is a symmetric bilinear form. It is the unique symmetric bilinear form whose diagonal is F_mu: if C is any such form, expanding C(K+L,K+L)-C(K-L,K-L) gives 4C(K,L), so C=B_mu. Uniqueness here concerns polarization of the complete quadratic functional, not every conceivable lift of a scalar or every historical convention for a current.

For the supplied actual residual delta, define

    J_(mu,delta) : V -> R,
    J_(mu,delta)(K) = B_mu(delta,K)
                   = sum_a mu_a h(delta_a,K_a).

This is a well-defined linear functional on V. In operator notation,

    J_(mu,delta) = E* D_mu G E delta.

It therefore respects all evaluation relations and uses only the declared retained ledger. In particular J(K)=0 if E K=0. No arbitrary dense-pair extension has been selected.

Two distinct identities fix the convention:

    J_(mu,delta)(delta) = F_mu(delta) = delta_w I(delta),
    D F_mu(delta)[K] = 2 J_(mu,delta)(K).

The first follows by substitution. For the second, expand F_mu(delta+sK) as F_mu(delta)+2sB_mu(delta,K)+s^2F_mu(K). Thus J is the polar lift and 2J is the residual derivative of the weight-variation functional. They must not be silently identified. The source has not yet specified which, if either, is its rho_support weight component.

The scalar F_mu(delta) at one residual is insufficient to recover J. For example take U=R^2, B=R, h(s,t)=st, V=Bil(U x U,R), two pairs (e1,e1),(e2,e2), and choose delta with both evaluated values 1. The directions mu=(1,0) and mu=(0,1) each give F_mu(delta)=1, but their covectors return K(e1,e1) and K(e2,e2), respectively. The new construction uses the entire stated quadratic formula, not only its observed scalar.

## 5. Exact baseline-weighted quotient condition

Define the baseline bilinear form and its Riesz map

    B_w(K,L) = sum_a w_a h(K_a,L_a),
    R_w : V -> V*,    (R_w K)(L)=B_w(K,L),
    N_w = ker R_w.

Because w>=0 and h is positive semidefinite, N_w is precisely the null space of the baseline quadratic seminorm. Indeed B_w(K,K)=0 implies h(K_a,K_a)=0 for each w_a>0. Positive semidefiniteness implies h(K_a,L_a)=0 for all L_a at those coordinates (for example by the discriminant inequality for h(K_a+tL_a,K_a+tL_a)). Hence R_w K=0. The reverse implication is immediate.

A linear functional J descends to the quotient V/N_w if and only if

    J(n)=0 for every n in N_w.

Necessity follows because [n]=[0]; sufficiency follows because J(K+n)=J(K). In finite dimensions and for this symmetric R_w, the annihilator N_w^ann equals im R_w: symmetry gives the inclusion im R_w subset N_w^ann, and rank-nullity makes their dimensions equal. Consequently the exact condition for the polar covector is

    E* D_mu G E delta in im R_w.

When it holds, the R_w representer is unique modulo N_w. This is an algebraic quotient statement, not a choice of native physical identification.

A sufficient condition is supp(mu) subset {a : w_a>0}. For n in N_w the preceding PSD argument gives h(delta_a,n_a)=0 at every such coordinate, and therefore J(n)=0. This condition is sufficient, not necessary: evaluation relations, residual zeros, or cancellations can also make J annihilate N_w.

Automatic descent fails without an appropriate condition. Take U=B=R, h(s,t)=st, V={K_k : K_k(x,y)=kxy}, one test pair (1,1), delta=K_1, w=0 and mu=1. Then R_w=0 and N_w=V, but J(K_k)=k, so J does not descend to the zero baseline quotient. This is an admissible one-sided nonnegative path w(t)=t, t>=0. It is not an admissible two-sided direction at that boundary. Thus the example rebuts automatic descent for ambient or one-sided weight variations, not the strictly two-sided feasible case. For a two-sided feasible nonnegative-weight direction, mu vanishes at all zero-weight coordinates and the sufficient condition applies.

## 6. Evaluation relations and representers

Even where w>0 on the ledger, the formal evaluated values (mu_a/w_a)delta_a need not be evaluations of any member of V. For an exact example use U=B=R and V={K_k} as above but a ledger containing two copies of the same pair (1,1). Let w=(1,1), mu=(1,0), and delta=K_1. Then E(V)={(k,k)} whereas the formal componentwise reweighting is (1,0), outside E(V). Nevertheless J(K_k)=k is a valid covector, and its R_w representer is K_(1/2), since B_w(K_(1/2),K_k)=k. The covector formula E* D_mu G E delta avoids mistaking a pointwise reweighting for an admissible bilinear residual map. It also avoids using an inverse of a singular form.

## 7. What follows and what remains supplied

Earned here, under the stated real finite-dimensional fixed-ledger assumptions:

1. The complete historical quadratic weight term determines a unique symmetric polarization.
2. Evaluating one slot at delta yields an explicit retained-evaluation covector J, with a known factor of two between polarization and residual differentiation.
3. The exact condition for compatibility with the baseline weighted quotient is J(N_w)=0, and support containment is sufficient. The stated boundary counterexample prevents an unjustified universal quotient claim.
4. The construction respects evaluation relations without extending to undeclared pairs.

Supplied or still unproved:

- mu, the actual native pair-weight direction. In particular P1 grade pushforward and a support-grade sum do not by themselves settle native support membership before/after an event.
- the residual delta, fixed ledger and its arguments, h, orientations, and any allowed component spaces. The scalar equality is not a method for choosing these from a desired response.
- the identification and normalization of the historical support current with J or 2J, the other support-variation components, and any required endpoint transport or quotient-admissibility for the actual construction.
- source-event-receiver access, native bit readout, an independently prepared source intervention, or a physical interaction/law. No such result is implied by this action-side polar lift.

This construction is conditional mathematical support on the existing P1 -> V1696.5 incidence -> V1694 action route, not completion of the first native incidence arrow. It supplies a candidate definition of the missing weight-to-dual operation that is canonical once the complete quadratic functional is specified. It does not claim that historical operations already mandated this current, or that a scalar action identity identifies an owner-accessible response. Untyped receiver outputs remain NOT SCORED for W_R/W_E/Bell comparisons. PR130/131 holds remain unchanged. No physical, stage-closure, or merge claim is made.
