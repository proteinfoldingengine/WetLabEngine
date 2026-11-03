# Corrected scope for the existing thermal-bath test

Date: 2026-11-02, America/Phoenix. Supporting mathematics, not native delivery. This note makes the already accepted C1/C2 corrections reviewable together. Original files and their original review remain unedited.

## Premises and retained conclusion
The source channel, Hilbert factorization, receiver interface, dimensions and arbitrary-unitary realization class are SUPPLIED. TB (full-rank E, pure blank R) is a NEW ASSUMPTION. Native P1/accounting does not derive these physical premises.

The single-collision condition rank(tau_E) <= d_E/2 remains the stated Theorem L scope. For sufficiency, choose an orthonormal eigenbasis of the supported bath subspace L and an isometric copy L' orthogonal to it. On initially supported inputs, fix every un-erased source basis vector and map |u,k> to |p,k'>. These images are orthonormal. Extend the resulting isometry to a full unitary, for example by swapping the paired basis vectors. “Identity elsewhere” in the original shorthand must not fix the already-used target columns of that unitary. This spells out its existing construction, not a new channel.

For finite-dimensional Gibbs states with finite Hamiltonian and finite positive temperature, the eigenvalues exp(-beta E_i)/Z are strictly positive. Full rank does not mean absence of pure-state decompositions.

## C2: a local collision condition is not a global existence threshold
For a collision of f orthogonal source states mapped to one pure source output, unitarity preserves the joint input rank f*r, where r=rank(tau_E). If R is untouched, the output support lies in that one source output tensor E, of dimension d_E. Thus f*r <= d_E is necessary for that collision. It does not establish simultaneous realization of the entire channel.

For the existing carrier A, take H_S with basis (o,p1,u1,p2,u2,v) and
Q=diag(1,1,0,1,0,1), L1=|p1><u1|, L2=|p2><u2|.
The composed erasure channel is C_A(rho)=Q rho Q + L1 rho L1^dagger + L2 rho L2^dagger.
The three vectorized Kraus matrices are nonzero and orthogonal, with Gram matrix diag(4,1,1). Hence rank J(C_A)=3.

A pure initial E of dimension two can provide at most two Kraus operators K_j=<j|U|0> for an R-untouched realization. Therefore it cannot implement C_A, even though each fan-in-two condition is 2*1<=2. This is the previously identified counterexample, not a new theorem of the native model.

The existing dimension-three control is explicit: swap |u1,0> with |p1,1>, and |u2,0> with |p2,2>, fixing all remaining basis vectors of S tensor E. These are disjoint transpositions, so the full matrix is unitary. On the initially supported E=0 inputs it produces Kraus operators Q,L1,L2 and realizes C_A for all inputs, including coherences. R remains an untouched spectator. This proves the known pure-bath capacity distinction; no mixed-bath global iff follows.

## Record location and the research disposition
In the original equal-qubit E/R benchmark, postcompose W_R tensor I_E with SWAP_ER. The reduced S channel stays C, while R is left in tau_E independent of the source and E contains the record. Thus the tested TB ingredient does not force a nonzero designated-R source contrast. The tested full-rank setup can consume R's purity without leaving the source distinction there.

The fresh review is to adjudicate the corrected C2 implication and its consistency with the preserved original packet, plus the code that verifies it. It must not rebind the old review or treat this as a new native receiver selection mechanism. No broader claim about arbitrary output dimensions or every possible initial-state constraint is asserted here. After this bounded verification/publication obligation, the thermal route stops.
