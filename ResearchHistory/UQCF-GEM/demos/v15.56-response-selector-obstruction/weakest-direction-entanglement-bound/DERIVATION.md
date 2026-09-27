# v15.89 — a sharp weakest-direction bound on normalized Choi negativity

Parent: 8419150d3a8309a247d29ae9cfac337ca0f87b6a. v15.88 established exact erasure implies qubit entanglement breaking, while arbitrarily small transmission can preserve entanglement. This gate asks for a quantitative bound without imposing unitality or a special source law.

For a qubit CPTP map Phi with affine Bloch action r -> T r+t, use the input-first unnormalized Choi matrix J (trace 2). Let delta=s_min(T). Define normalized Choi negativity by

    N(J/2) = sum_i max(0,-lambda_i(J^Gamma_input))/2.

The claim is N(J/2)<=delta/2 for every qubit CPTP affine map, including arbitrary admissible translations. It is a Choi-state entanglement bound; it is not a quantum-capacity formula, diamond distance, or bound here claimed for every arbitrary channel input/reference state.

## Reflection comparison, without modifying the channel

Take any unit n, put w=Tn and F=diag(1,-1,1), the Bloch action of input transposition. Set H=I-2nn^T, A=HF. A is a proper orthogonal matrix, so it is a unitary qubit input channel. Therefore B=J(TA,t) is positive. The original partial transpose G=J^Gamma_input=J(TF,t) differs from B by

    D=G-B = ((Fn).sigma)^T tensor (w.sigma).

Indeed TF-TA=2(Tn)n^T F. Both Pauli factors are Hermitian, and the first is unitary because |Fn|=1. Hence D has operator norm |Tn|. It follows directly from B>=0 that

    lambda_min(G) >= -|Tn|.

A two-qubit state's partial transpose has at most one strictly negative eigenvalue. Thus N(J/2)<=|Tn|/2. Choosing a weakest right singular vector gives the stated delta/2 bound. All translations cancel from D; B is the original channel precomposed with a unitary, not a rank-truncated map assumed to be CP.

For completeness, the negative-eigenvalue fact follows because every two-dimensional subspace of C^2 tensor C^2 contains a product vector: represent its spanning vectors as 2x2 matrices and solve the homogeneous quadratic determinant equation over C. Two negative eigenvectors would span a strictly negative subspace containing a product vector, whereas a positive state's partial transpose has nonnegative expectation on every product vector. This contradicts positivity. The fact is established literature; see Rana (2013), which attributes the two-qubit result to Sanpera, Tarrach and Vidal (1998): https://arxiv.org/abs/1304.6775.

In coordinates n=e_Z, A=diag(1,-1,-1) is Pauli-X conjugation. The exact certificate is

    J^Gamma_input - (X tensor I) J (X tensor I)
        = Z tensor (T e_Z).sigma.

Verify this on all 13 affine coefficients, including all three components of translation. For arbitrary real w, D^2=|w|^2 I_4 supplies a further exact norm certificate. The direct n-dependent formula above is checked numerically for every frozen channel without changing its coordinates.

## Sharpness and nonunital examples

Let N0=cof(L) for the inherited rank-two partial isometry L. For 0<=epsilon<=1 define

    T_epsilon=((1+epsilon)/2)L+epsilon N0,  t=0.

In proper coordinates this is diag((1+epsilon)/2,(1+epsilon)/2,epsilon). Its Choi spectrum is {0,(1-epsilon)/2,(1-epsilon)/2,1+epsilon}; its partial-transpose spectrum is {-epsilon,(1+epsilon)/2,(1+epsilon)/2,1}. Hence it is CPTP, delta=epsilon, and N(J/2)=epsilon/2. The constant 1/2 is sharp over the whole allowed delta interval, including arbitrarily close to exact erasure. Eight Bell eigenvector equations certify these spectra exactly.

Amplitude damping supplies a nonunital equality family. With q=1-gamma, its canonical action is T=diag(sqrt(q),sqrt(q),q), t=(0,0,gamma). Its J spectrum is {0,0,gamma,2-gamma}, and its J^Gamma spectrum is {-q,q,1,1}. Thus delta=q and negativity=q/2. The frozen native evaluation uses proper frames extracted from L, not an externally aligned channel.

The bound is an upper bound, not an entanglement indicator by itself: a full-rank depolarizing channel can have zero negativity and positive delta. Nor must the bound be saturated. v15.88's fixed-retained-plane family has negativity epsilon/4, half the attainable ceiling for the same weakest singular value.

## Scope and provenance

This is a finite-dimensional channel inequality proved using standard Pauli, positivity and singular-value facts, with an explicit attained bound. A limited literature check verifies the negative-eigenvalue ingredient, not priority for this particular inequality. No novelty claim is made. The scientific contribution here is the reproducible bound and its use to quantify the retained-channel interpretation near a singular boundary.

No physical source law, channel interpretation of geometry, or gravity law is selected. The original retained-source question remains open. No fundamental time, external alignment, heuristic fitting, or dark-matter primitive is introduced; Genesis Pin and historical verdicts remain unchanged.
