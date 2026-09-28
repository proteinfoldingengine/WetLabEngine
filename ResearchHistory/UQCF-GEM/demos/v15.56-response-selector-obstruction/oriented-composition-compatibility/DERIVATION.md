# Oriented completion and support compatibility

Let A and B be real rank-two partial isometries in oriented three-dimensional endpoint spaces. Define F(X)=V_X+cof(V_X) for a rank-two matrix X, where V_X is its support polar factor. F(X) is the unique proper completion of V_X. A maps the intermediate node to the destination; B maps the origin to the intermediate node.

Set P_A=A^T A and Q_B=B B^T. Define

c^2=tr[(I-P_A)(I-Q_B)], 0<=c<=1.

These are the initial plane of A and final plane of B at their common node. The singular values of AB are (1,c,0). For c>0 the product stays rank two and

||F(AB)-F(A)F(B)||_F^2=4(1-c).

Consequently F(AB)=F(A)F(B) if and only if P_A=Q_B. At c=0 the product has rank one and no unique proper completion is prescribed.

Proof: A=R_A P_A and B=R_B P_B with R_A=F(A), R_B=F(B). Then

AB=R_A R_B (R_B^T P_A R_B) P_B.

Left multiplication by R_A R_B factors out of the completion. The remaining two plane projectors have one shared axis; their other principal-angle cosine is c, the absolute normal overlap. Choose oriented coordinates so their product has polar completion a proper rotation through that acute principal angle. Its trace is 1+2c and its squared Frobenius distance from I is 6-2(1+2c)=4(1-c). Equality requires c=1, equivalently equal planes. This coordinate reduction proves a frame-invariant identity; no alignment is performed on the measured data.

The exact certificate uses U=rotation_y(theta), c=(1-t^2)/(1+t^2), s=2t/(1+t^2), 0<t<1, P=diag(1,1,0), Q=U P U^T. Then QP=U diag(c,1,0), support V=UP, and F(QP)=U. Both projector factors individually complete to I, exhibiting the obstruction. At t=0 the supports match; at t=1 the product has rank one. Orthogonal normals represent the boundary, not a failure of linear composition.

Compatible rank-two partial isometries form a composition-closed class when the intermediate initial/final planes match. Their products remain partial isometries, and proper completion respects the resulting paths, including compatible triples. Ordinary matrix composition remains associative even when compatibility fails. A failure of F to preserve composition is not a failure of matrix associativity.

The planar links from v15.93 supply compatible paths. The native v15.83 spatial loop L supplies an incompatible pair (L,L), with no new support choice. This is composition of retained maps at a fixed ordered slice, not sequential physical source updates. The theorem assumes partial-isometry factors; arbitrary correlation factors can introduce stretch-dependent polar-composition effects. No erased quantum information is recovered by the completion.
