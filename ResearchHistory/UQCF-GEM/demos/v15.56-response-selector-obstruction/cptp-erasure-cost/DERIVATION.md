# v15.87 — unavoidable CPTP cost of exact erasure

Certified parent: 3b1c4d29db91b2bfac7f6fe447de131671fd9206. v15.86 permits a unique unitary completion of a retained plane, but that completion does not erase the missing direction. This gate instead keeps exact erasure and permits arbitrary action on the retained plane.

Let L be the inherited real rank-two partial isometry, P=L^T L and K=I-P. Consider every real T and real translation t for which the affine qubit map r -> T r+t is CPTP and T K=0. No condition of proportionality to L, preserved output plane, or zero translation is initially imposed. The error objectives are the spectral/operator norm ||T-L||op and Frobenius norm ||T-L||F. They measure distortion of linear Bloch action; they are not diamond norms or a fitted physical source law.

## Universal bound over all allowed maps

Exact erasure implies rank(T)<=2. By v15.85's exact spin-flip argument, CPTP at any translation requires the unital part with that same T to be CP. Proper input/output rotations reduce any rank-at-most-two T to diag(s1,s2,0), with s1,s2>=0; the free null direction allows both coordinate frames to be proper without changing the two singular values. These are coordinate changes, not external alignment.

The unnormalized Choi eigenvalues are (1-s1-s2)/2, (1-s1+s2)/2, (1+s1-s2)/2, (1+s1+s2)/2. Therefore every admissible T obeys

    ||T||_* = s1+s2 <= 1.

Conversely, any such rank-two real T has a CPTP unital extension if s1+s2<=1. Not every translation is admissible.

Write <A,B>=Tr(A^T B). Since ||L||op=1, ||L||F=sqrt(2), ||L||_*=2, nuclear/operator duality gives <L,T><=||T||_*<=1. Thus

    <L,L-T> >= 1,
    ||T-L||op >= 1/2,
    ||T-L||F >= 1/sqrt(2).

The map T*=L/2 attains both bounds. It is unique for the Frobenius objective by equality in Cauchy-Schwarz. For operator-norm equality, choose orthonormal v1,v2 in ran P and ui=Lvi. Each ui dot (L-T)vi is at most 1/2, but their sum must be at least 1; equality forces (L-T)vi=ui/2 for both i. Together with TK=0 this forces T=L/2. Hence both objectives have the same unique linear minimizer, even when all retained-plane distortions and output directions are allowed.

## The optimal translation is also forced

In canonical coordinates T*=diag(1/2,1/2,0), the unital Choi J0 has normalized Bell-minus kernel vector w=(|00>-|11>)/sqrt(2). For arbitrary real t, Jt=J0+I tensor (t.sigma)/2 satisfies

    w^dagger Jt w = 0,
    ||Jt w||^2 = |t|^2/4.

If Jt is positive semidefinite, zero expectation forces Jt w=0. Therefore t=0. The unique optimal affine map is the unital map with T=L/2. This removes affine-shift ambiguity analytically, not by a finite search.

## Physical construction and operational meaning

For any orthonormal retained basis vi and ui=Lvi, let Mi measure the two projectors (I +/- vi.sigma)/2 and prepare (I +/- ui.sigma)/2 respectively. Then Phi*=1/2 M1+1/2 M2 has linear Bloch action L/2. It is CPTP and entanglement breaking by construction: even with an arbitrary ancilla, a measure-and-prepare channel produces a separable system-ancilla mixture. This is a property of this optimal map, not a claim about every allowed affine channel.

Every antipodal unit pair in the retained plane has trace distance 1 before the map and 1/2 after it. The kernel antipodal pair has output distance 0. For any pure retained-plane input, the trace distance between the output of Phi* and the formal target L is 1/4. This last number compares two outputs; it is different from antipodal-pair distinguishability. The target L is positive on individual qubit states but is not itself CP.

No optimizer or parameter tuning selects 1/2: it is the exact equality case of the frozen CP inequalities. This mathematical optimum does not select a physical source law. It retains the conditional interpretation of transport as a qubit channel, and does not show that geometry must use this interpretation. Composition counts remain ordered operations, never fundamental time. All earlier verdicts, Genesis Pin, and the distinction between acting on states and changing admissible worlds remain intact. No gravity derivation.
