# Numerical question

v15.99's eight strict-threshold disagreements appeared only in transformed planar K, while invariant J ranks agreed. The matrix covariance residuals passed their separate bound. This does not waive the failed rank test.

For a prescribed local frame, retained tensors transform as C_ij'=G_i C_ij G_j^T and dC_ij'=G_i dC_ij G_j^T. Exact oriented polar extraction gives R_ij'=G_i R_ij G_j^T. The unique skew solution of P W+W P=R^T dC-dC^T R consequently transforms covariantly. Loop K transforms by blockdiag(G0,G0), while the three trace derivatives J are invariant.

The observed computation has two rounding stages: formation/transport of the retained input tensors and evaluation of their polar/skew/loop readout. Evaluating the very same binary inputs in greater precision isolates dependence on the latter stage. Independently transporting native retained tensors using the prescribed exact rational frames supplies a control for the former. The control does not replace the frozen-input measurement or independently recompute a global quantum source.

Rounded rank-two tensors may actually have a tiny third singular value. The inherited readout selects the two leading singular vectors, completes V to R=V+cof(V), and solves using sym(R^T C), without discarding the signed third eigenvalue there. This audit preserves that extension. It records input support/PSD defects separately from arithmetic identities and never projects the response to a desired rank.

The skew sector has three basis matrices B_i with axial coordinates (W21,W02,W10). The Sylvester map becomes L_ji=coords_j(P B_i+B_i P); solving L w=coords(Q) gives an independent evaluator. At P=diag(2,1,0), its denominators are positive; variations dC=B_i P recover all three B_i. At rank-one P the skew map is singular, supplying an invalid-domain control.

Even if the audit recovers all expected ranks, v15.99 remains historically INVALID. A negative numerical result likewise establishes no physical obstruction. This is a precision and identity audit, with no new primitive geometry or fundamental time.
