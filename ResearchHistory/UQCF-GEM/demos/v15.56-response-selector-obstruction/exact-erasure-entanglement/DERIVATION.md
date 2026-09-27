# v15.88 — exact qubit erasure implies entanglement breaking

Parent: 38c675b1af1c9df6b926adc5d243d0a889d00f93. This is a reproducible application of an established qubit-channel result, not a claim of a new quantum-information theorem or a new physical source law.

## Existing theorem and explicit certificate

Write a qubit CPTP map as r -> T r+t, with real 3x3 T and real t. Suppose Tn=0 for a unit vector n: an input Bloch direction is exactly erased, and rank(T)<=2. The translation is unrestricted except by complete positivity. This includes image planes, lines, and points.

In proper input coordinates with n=e_z, the third column of T vanishes. Transposition on the input qubit has Bloch matrix F=diag(1,-1,1). Conjugation by Pauli X has A=diag(1,-1,-1). Since the third column vanishes, TF=TA, so Phi composed with transpose equals Phi composed with the unitary X channel. Their unnormalized Choi matrices obey

    J^(Gamma_input) = (X tensor I) J (X tensor I).

This is INPUT PARTIAL transpose, distinct from v15.85's FULL transpose identity. It follows that J and its input partial transpose have identical spectra; if Phi is CP, both are positive. For a 2x2 bipartite Choi state, positivity of the partial transpose is equivalent to separability. A separable Choi state is equivalent to an entanglement-breaking channel. Therefore every qubit CPTP map erasing any nonzero Bloch direction is entanglement breaking, including nonunital maps.

For direct evaluation in the inherited coordinates, define the kernel reflection H=I-2nn^T and A=HF. H has determinant -1, A is a proper orthogonal matrix, TH=T and TA=TF. Every proper Bloch rotation is a unitary qubit channel. Thus J(TF,t)=J(TA,t) again proves positivity and spectral equivalence without fitting or external alignment. The choice of transpose basis is a representation choice, not a preferred physical frame.

The exact certificate checks the canonical identity on all ten independent affine coefficients: the constant, six free entries in the two retained columns, and three translation components. Numerical native controls verify partial-transpose indexing, the proper-rotation relation and isospectrality. The universal statement comes from the algebra and established separability/channel equivalences, not from finite sampling.

## Exact erasure is essential

Let L be the inherited rank-two partial isometry and N=cof(L). Its proper completion is L+N. The frozen nearby family

    T_epsilon = L/2 + epsilon N,  t=0,  0<=epsilon<=1/2

keeps the retained-plane action fixed while restoring a small missing-direction action. In proper input/output coordinates it is diag(1/2,1/2,epsilon). Its Choi spectrum is

    {epsilon/2, (1-epsilon)/2, (1-epsilon)/2, 1+epsilon/2},

and its input-partial-transpose spectrum is

    {-epsilon/2, (1+epsilon)/2, (1+epsilon)/2, 1-epsilon/2}.

It is CPTP throughout this interval, but is NOT entanglement breaking for every epsilon>0. The normalized Choi negativity is epsilon/4, and the missing-axis antipodal trace distance is epsilon. Thus arbitrarily small nonzero singular values cannot be treated as exact erasure for this theorem. There is no uniform positive approximate-erasure threshold that implies entanglement breaking near this boundary. This does not exclude robust entanglement-breaking neighborhoods elsewhere.

Full-rank entanglement-breaking channels also exist; the converse implication is false. The frozen depolarizing channel T=I/4 is a control for that boundary. An identity channel and amplitude damping with gamma=1/2 supply full-rank non-EB controls.

## Scientific scope and sources

Entanglement breaking means all output-reference entanglement is destroyed for every input and every external reference, not that all classical distinguishability disappears. The result concerns one qubit input and one qubit output. Neither this PPT implication nor the singular-map conclusion is asserted for arbitrary dimensions. It is conditional on interpreting the retained map as a physical qubit channel; it does not derive that interpretation, a source law, gravity, or an alteration of admissible worlds. No fundamental time, heuristic fitting, external alignment, or dark-matter primitive is introduced. Genesis Pin and all historical verdicts remain intact.

Established sources inspected before preregistration:

1. M. Horodecki, P. Shor and M. B. Ruskai, Entanglement Breaking Channels (2003), https://arxiv.org/abs/quant-ph/0302031, full text https://arxiv.org/html/quant-ph/0302031v2. The introduction explicitly states the qubit plane/line-image result; Theorem 4 identifies separability of the normalized Choi state with entanglement breaking.
2. M. Horodecki, P. Horodecki and R. Horodecki, Separability of Mixed States: Necessary and Sufficient Conditions (1996), https://arxiv.org/abs/quant-ph/9605038. PPT is necessary and sufficient in 2x2 and 2x3, not generally in higher dimensions.

The contribution of this gate is a pinned certificate and boundary controls connected to the retained-loop research chain. No priority or novelty claim is made for the general theorem.
