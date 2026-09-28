# v16.03 — Finite-source continuation and the permitted cubic order contrast

Status: analytic conditional result; no new finite-strength measurement or CI certification is claimed.

Parent: v16.02 publication cb5aeb5791c187a8ec231f755bb1e298d0693f4d; tested scientific head ccc65c5569e904be3c98ec61e3d231f8e693eb92, run 36440529651. The v16.02 result is conditional on its frozen source/preparation laws.

## Question

Does the certified origin response imply a response in a finite physical protocol? Can an intermediate channel produce finite order sensitivity even when the two source channels commute?

The first question has a local conditional answer. The second has a new permitted leading coefficient, whose nonvanishing remains unmeasured.

## Objects and assumptions

Keep the four-qubit states, 81 weight-four hidden probes h, source generators L_A,L_B,L_D, five geometry edges and final preparations Q from v15.98–v16.02. The selected coherent source has L_X = Ad(U_X)-I, with U_X Hermitian and U_X squared equal to I. Write its finite CPTP map as E_X(s)=I+s L_X, 0<=s<1/2. This equals the inherited source-strength parametrization s=(1-exp(-2u))/2; u and s are protocol parameters, not fundamental time.

Fix a>0 and M_a=D_a tensor4. The forward and reverse protocols, with equal mixture parameters lambda, are

P_f(lambda)=E_Y(lambda) M_a E_X(lambda),
P_r(lambda)=E_X(lambda) M_a E_Y(lambda).

Let z_o(lambda)=Q P_o(lambda)(rho). Let C_o(lambda) be the list of its connected pair correlation matrices on the five declared edges. At zero both orders have the common baseline C_0. F(C) is the three-component invariant readout (tr H1,tr H2,tr(H1 H2)) constructed by the inherited polar links.

Work in a neighborhood in which every edge remains in its declared polar domain. For the isotropic arm this is the proper, invertible polar domain. For the planar arm, restrict to the fixed preparation support, with both supported singular values nonzero and the inherited oriented completion. On these domains F is smooth; in particular twice differentiable, and locally analytic. The relative spectral-domain inequalities must have positive margins at the origin.

The derivative with respect to hidden input is the 3x81 matrix J_o^phys(lambda), computed at rho for the actual finite protocol, without dividing by lambda squared.

## Exact reduction to a common hidden tangent

The inherited exact Pauli certificates state that h, M_a h, L_Y M_a h and M_a L_X h have no pair moments; the composed term has no one-body moments. Local unital preparations preserve these nulls. Expanding the two finite maps therefore gives

d_h C_o(lambda)=lambda^2 B_o,a,

where B_o,a is the prepared retained pair moment map of L_second M_a L_first h. The one-body hidden derivative is zero for the complete finite protocol, so the connected-correlation subtraction contributes no extra term. This equality holds at the finite protocol center, not only at the source origin.

The chain rule yields the central identity

J_o^phys(lambda)=lambda^2 DF(C_o(lambda))[B_o,a].              (1)

This identifies precisely what the previous finite correlation check did and did not certify: B is known, whereas DF must now be evaluated at the finite center.

## Local continuation

For lambda>0 define the normalized response Jhat_o(lambda)=J_o^phys(lambda)/lambda^2. Equation (1) extends continuously to lambda=0, with

Jhat_o(0)=DF(C_0)[B_o,a]=J_o^(16.02).

Hence every nonzero origin invariant response remains nonzero for sufficiently small positive lambda within the polar domain. More strongly, if the exact origin matrix has rank r, a nonzero r-by-r minor remains nonzero nearby, so finite response rank is at least r. This does not prove rank equality: previously null directions can activate.

Apply the same reasoning to the difference of the two invariant responses. A nonzero overlapping-source origin contrast persists for sufficiently small positive lambda. The full finite ensemble admits a common positive neighborhood by taking the minimum of its finitely many neighborhoods, conditional on the origin nonzero minors and strict domain margins.

This is an existence statement. It provides neither a numerical radius nor certification at u=0.1, and it does not turn thresholded numerical rank into an exact symbolic rank proof. Fixed absolute rank thresholds on unnormalized responses may eventually report zero as lambda approaches zero, even when the mathematical response is nonzero.

## Disjoint pair: quadratic cancellation, permitted cubic term

For X=A and Y=D, the inherited exact retained certificate gives B_f,a=B_r,a=B_a. Their global inserted protocols need not commute when a differs from 1. From (1),

Delta J^phys(lambda)
 = lambda^2 (DF(C_f(lambda))-DF(C_r(lambda)))[B_a].

Let V_f=C_f'(0), V_r=C_r'(0). Taylor expansion gives

Delta J^phys(lambda)
 = lambda^3 D^2F(C_0)[V_f-V_r,B_a] + O(lambda^4).            (2)

Thus the quadratic coefficient is exactly zero. A cubic coefficient is allowed; this proof does not show it is nonzero.

For explicit evaluation, write the connected-correlation map as C(z). Then

V_f-V_r
 = DC(Q M_a rho) [
     Q (L_D M_a + M_a L_A - L_A M_a - M_a L_D) rho
   ].                                                     (3)

DC includes the derivatives of the one-body-product subtraction. Omitting those derivatives would test a different coefficient.

At a=1 the disjoint source channels commute on the full operator space, so the two complete protocols, centers and invariant responses coincide at every admissible lambda. The entire order contrast is zero, including the cubic coefficient. At a=0 complete erasure leaves undefined polar geometry under these unital sources; it is excluded from the Hessian calculation and must never be assigned a zero polar response.

For overlapping sources, B_f,a and B_r,a can differ, giving

Delta J^phys(lambda)
 = lambda^2 Delta J^(16.02) + O(lambda^3).

The two orders may have different finite baseline invariant values; the quantity above is specifically their hidden-input derivative contrast. It is not the raw baseline invariant difference.

## Interpretation and limitations

The possible disjoint cubic signal would reflect insertion of M_a between sources and the nonlinear readout at different finite centers. It would not refute the commutation of E_A and E_D, imply nonassociative CPTP composition, or select a physical source law. The a=1 null distinguishes these claims.

The next measurement should evaluate the coefficient in (2) independently of finite-step differences, then test the predicted powers using fixed steps, full covariance and spectral-domain controls. Nonvanishing must remain a falsifiable outcome, not a success condition built into the implementation.

No source, preparation, threshold or alignment has been tuned. No fundamental time, dark-matter primitive, Einstein equation or gravity derivation is introduced. Geometry remains extracted from retained relations.

## Verification performed for this analytic step

The source definition and exact null/scaling certificates were read in composed-four-body-response/gate.py and intermediate-eb-retention/gate.py; the 16.02 global precision implementation and published results were inspected. Equation (1) follows by exact finite-channel expansion and the chain rule. Equation (2) follows by Taylor expansion on the stated smooth domain. A scalar symbolic check confirmed cancellation of the common quadratic term; it is bookkeeping only, not a numerical experiment, independent proof assistant certificate, or test of a nonzero cubic coefficient.
