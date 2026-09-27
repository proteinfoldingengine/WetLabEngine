# v15.86 — CPTP completion of a retained plane

Parent: c0adc88d4ef2b955a07d567b4cf2c3ab3d1fa24d. This bounded gate changes only the previously fixed action on the missing Bloch direction. It does not rescue the full zero-extended map in v15.85.

Let L be a real rank-two partial isometry with singular values (1,1,0), and P=L^T L. Seek a qubit Hermiticity-preserving trace-preserving affine map r -> T r + t with T P=L. Translation is initially unrestricted. This is agreement of linear response on the retained plane; CPTP will also force agreement on the states in that plane.

Choose any orthonormal v1,v2 in ran P; set u1=L v1,u2=L v2, v3=v1 cross v2, u3=u1 cross u2. These frames are proper, hence correspond to unitary changes of qubit coordinates, not external alignment. In these frames T has columns e1,e2,(a,b,c).

Positivity on the two pure inputs +/-v1 requires |t+u1|^2<=1 and |t-u1|^2<=1. Their sum is 2+2|t|^2, so t=0. This statement uses the unit length inherited from L; it is not a claim for arbitrary contracted planes.

The input-first unnormalized Choi matrix for the resulting canonical map is

    [(1+c)/2, (a-i b)/2, 0, 1]
    [(a+i b)/2, (1-c)/2, 0, 0]
    [0, 0, (1-c)/2, -(a-i b)/2]
    [1, 0, -(a+i b)/2, (1+c)/2].

Positive diagonal entries require c<=1. Its expectation in (|00>-|11>)/sqrt(2) is (c-1)/2, hence positivity requires c>=1. Therefore c=1. At c=1, the principal minor on rows 0,1 equals -(a^2+b^2)/4, requiring a=b=0. This is an exact certificate for uniqueness over all three missing-column coefficients and all translations; no parameter grid proves uniqueness.

Consequently the sole CPTP completion is the proper orthogonal map

    R = L + cof(L),

where cof denotes the cofactor matrix, not its transpose. For rank-two partial isometries cof(L)=u3 v3^T. It acts only on the missing direction, has Frobenius norm 1, and is independent of the chosen orthonormal basis of the retained plane. R is a unitary qubit channel with a unitary inverse. This restores the discarded direction's distinguishability instead of implementing pruning of that direction. The missing direction is algebraically constrained because two independent Pauli observables generate the whole qubit matrix algebra.

One preserved axis does not suffice: identity and complete dephasing about that axis are distinct CPTP maps agreeing there. Nor does positivity suffice: diag(1,1,0) is positive on the Bloch ball but not completely positive. The improper orthogonal completion has the same retained-plane action and is positive, but is not CP.

This is a conditional channel-completion statement, not selection of the original source law, extraction functor, or physical requirement that a retained link be a CPTP map. No full polar continuation across v15.82's boundary is established. Completion may agree with one limiting orthogonal map and disagree with the other; this gate does not test those limits. No gravity derivation, fundamental time, dark-matter primitive, heuristic fitting, or external alignment is introduced. Genesis Pin and all historical verdicts remain unchanged.
