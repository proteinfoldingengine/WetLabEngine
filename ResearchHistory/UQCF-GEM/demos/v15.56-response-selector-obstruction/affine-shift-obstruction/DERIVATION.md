# v15.85 — Affine shifts cannot rescue a non-CP qubit linear part

Parent b35525fd01bea949cacd6b2f65939c57a2911682 certifies v15.84. Keep its
loop matrices and candidate qubit interpretation; relax only unitality.
For real T and real shift t define
Phi_(T,t)(z)=Phi_(T,0)(z)+Tr(z)(t.sigma)/2.
This is the general Hermiticity-preserving, trace-preserving qubit map with
fixed linear Bloch action T. Complete positivity is still to be tested.

## An all-shifts obstruction, not a finite search

The input-first Choi matrix is
J(T,t)=J(T,0)+I tensor (t.sigma)/2.
Let S=sigma_y tensor sigma_y. Exact Pauli identities give
J(T,-t)=S J(T,t)^T S^dagger,
where T on the right-hand J denotes full matrix transpose, not partial
transpose. Full transpose preserves positivity, and S is unitary. Thus if
J(T,t) is positive for any t, J(T,-t) is positive too. Their average is
J(T,0). Therefore

there exists a CPTP affine shift with linear part T
if and only if its unital extension J(T,0) is positive.

The reverse implication uses t=0. This exact qubit theorem removes the
unitality loophole without fitting or optimizing translations. It does not
make every shift of a CP linear part admissible. Verify the identity on the
constant, nine linear-T, and three shift coefficient matrices exactly.

For each inherited non-CP loop power, the negative unital Choi eigenvector
is maximally entangled. Its rank-one witness has output marginal I/2, hence
zero expectation against all three shift coefficient matrices. Its negative
expectation is consequently independent of t. Numerical witnesses corroborate
the exact theorem; a merely small floating coefficient is not a proof over
unbounded shifts. The all-shifts conclusion rests on the symbolic identity
and positivity/convexity argument, not a finite grid.

## Nonunital positive controls at the fourth power

For rank-two T=U diag(s1,s2,0) V^T, choose the null left singular direction
u3 and t=tau*u3. Proper input/output rotations give Choi eigenvalues
[1±sqrt(tau^2+(s1+s2)^2)]/2 and
[1±sqrt(tau^2+(s1-s2)^2)]/2.
The exact admissible interval on this line is
|tau|<=sqrt(1-(s1+s2)^2).
This is an analytic line section, not a classification of the full
three-dimensional shift region. The axis is extracted from the unchanged
operator, not an external realignment. Its sign has no effect on the
symmetric control ladder.

## Recovery obstruction survives every admissible shift

For two input states, the common affine offset cancels in their output
difference. Thus the antipodal right-singular-axis pairs still have output
trace distances s1,s2,0, for every t for which the map is CPTP. The same
trace-distance contraction proof rules out exact CPTP recovery when s_a<1.
For each separate equally likely pair, optimal mean pure-target overlap
remains (1+s_a)/2, attained by the binary measurement-and-preparation
recovery. A common offset can affect individual outcome probabilities but
not this equal-prior average. Fidelity means Tr(rho_target rho_recovered),
without a square root; no arbitrary-ensemble optimum is asserted.

## Scope

This extends v15.84 beyond unitality while preserving its linear Bloch
interpretation. It does not derive that interpretation from recoverability,
identify it with the original three-qubit source channel, or select a source
law. A physical fourth-power block does not make non-CP elementary powers
physical. Traversals remain spatial paths at one ordered slice, never
fundamental time. Earlier verdicts, Genesis Pin and the distinction between
acting on states and changing admissible worlds are unchanged. No heuristic
fit, external alignment, dark-matter primitive or gravity derivation.
