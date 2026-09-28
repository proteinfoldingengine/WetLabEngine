# v15.91 — fully separable outputs can retain rotational response

Parent: 5e4c27c47dbfbc922fdfcf903f0f9dd95d139fdd. Return to the native three-qubit polar-skew response after the conditional qubit-channel audits. The question is whether a nonzero retained rotational response witnesses surviving output entanglement.

## Covariant attenuation and exact polar invariance

Define the single-qubit CPTP depolarizing map D_a(z)=a z+(1-a)Tr(z)I/2, with 0<=a<=1, and its three-site product D_a^tensor3. This channel commutes with every independent local unitary; choosing Pauli coordinates to implement it does not introduce a preferred physical frame.

For any normalized three-qubit state, one-body moments scale by a and two-body moments by a^2. Consequently connected correlations satisfy

    C_e(D_a^tensor3 rho)=a^2 C_e(rho).

For any trace-zero tangent y, the full connected-correlation derivative obeys delta C'_e=a^2 delta C_e, including derivatives of both one-body factors. For a>0 on the regular polar domain, C=OP gives

    O'=O, P'=a^2 P, Q'=a^2 Q, W'=W.

The last statement follows from the invertible skew Sylvester equation PW+WP=Q. Thus the edge rotational tangent map E, its rank, and the polar factors are unchanged. Raw correlations and the polar-skew numerator are suppressed; this is not an assertion of unchanged experimental sensitivity. At a=0, C=0 and polar geometry is undefined, not a zero rotational response assigned by convention.

## Fully separable measure-and-prepare certificate

Let Pi_(k,s)=(I+s sigma_k)/2 for k=X,Y,Z and s=+1,-1. Use six POVM effects E_(k,s)=Pi_(k,s)/3 and prepared states tau_(k,s)=(I+3a s sigma_k)/2. For 0<=a<=1/3 these are normalized positive states, and

    D_a(z)=sum_(k,s) Tr(E_(k,s) z) tau_(k,s).

Tensoring the six-outcome representation yields 216 product preparations. Their weights are nonnegative and sum to one for every input density matrix. Every three-qubit output is therefore fully separable among the three sites. The map is also entanglement breaking between the total output and any external reference. Neither claim is inferred merely from PPT tests.

Postcompose the frozen CPTP source S_(lambda,u) of v15.81 with this channel:

    Psi_(lambda,u,a)=D_a^tensor3 composed with S_(lambda,u).

For a<=1/3, Psi is entanglement breaking and all its outputs are fully separable, for arbitrary inputs. The effective POVM is S^dagger applied to the product effects; its positivity follows from the source channel. The source may still involve nonlocal access. This construction does not show that every intermediate source operation or the original global consistency law is classical.

For the inherited 27 hidden directions h, evaluate the finite-input tangent S(h), then D_a^tensor3 S(h), at the corresponding finite centers. The geometry identities above prove invariance of this hidden-to-rotation response for a>0. At a=1 the original v15.81 finite response is recovered. The incoherent source arm lambda=0 is the matched rotational-null control.

Psi_(lambda,0,a)=D_a^tensor3, so for a<1 this family is not an identity-anchored source flow, and it is not asserted to satisfy a source-strength semigroup law. This is a valid composite CPTP update and a postprocessing obstruction to interpreting E as an output-entanglement witness. It does not replace the prior source-vector-field classification theorem.

## Scope

The v15.81 primary signal was rank 6 on edges (1,2) and (2,0), with source edge (0,1) null. That signal is conditional on the specified source-component interference law. The new test does not select that law from global consistency, derive gravity, or claim geometry is primitive. It asks whether surviving output entanglement is necessary for the already defined polar observable.

Entanglement-breaking qubit channels and measure-and-prepare structure are established theory; see Ruskai, Qubit Entanglement Breaking Channels (2003), https://arxiv.org/abs/quant-ph/0302032. The explicit six-outcome construction and polar scaling supply the certificate used here. No priority claim is made.

Genesis Pin and all historical verdicts remain intact. Source strength u is an ordered update parameter, not fundamental time. No fit, external alignment mechanism, or dark-matter primitive is introduced. Nonzero rotational geometry alone need not identify quantum entanglement or a gravity mechanism.
