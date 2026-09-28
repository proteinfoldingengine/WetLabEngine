# Full global operator precision audit

For four qubits, B_w=P_w/4 is Hilbert-Schmidt orthonormal. Writing rho=sum_w c_w B_w retains the complete256-dimensional operator, with c_w=Tr(B_w rho). A one- or two-body Pauli moment is4c_w. Applying a local channel to coefficient tensor indices is exactly its action on the global operator, provided its transfer matrix is formed using the local Pauli trace identity and its embedding is correct.

For a k-qubit local source AP, the generator transfer matrix is L_vw=Tr[P_v(AP P_w AP^dagger-P_w)]/2^k. Forming this matrix independently from the transformed local unitary AP' implements the transformed global source law. The input probe is also transformed, Gamma h, with its original column label. Neither operation requires transporting a retained target.

The isotropic intermediate channel multiplies a Pauli coefficient by a to the number of nonidentity factors. The planar preparation is the Pauli-unitary mixture with weights1/2,1/4,1/4 for I,X,Y; its Bloch action is diag(1/2,1/2,0). In another source frame, independently conjugating those local operators gives the same prescribed physical channel in that frame.

Exact covariance predicts global stage vectors Gamma Y, retained tensors G_i C_ij G_j^T and G_i dC_ij G_j^T, and the loop response blockdiag(G0,G0)K, with invariant J. These serve as comparisons only. The measured transformed pipeline is independently composed from its global input and local source/channel matrices.

v16.00 showed that high precision applied after retained tensors are rounded cannot remove the eight threshold crossings. This experiment moves high precision upstream to formation of the complete global operator and channels. The initial density and attenuation are the same binary inputs; algebraic unitaries are evaluated at the working precision. No source normalization, input projection, amplitude fit or external alignment is introduced.

The state has finite-precision trace error before this audit; it is not silently renormalized. Imaginary density entries contribute to real Pauli-Y coefficients and must survive exact complex decoding. Imaginary residuals of Hermitian operator coefficients are checked before any conversion to a real coefficient representation.
