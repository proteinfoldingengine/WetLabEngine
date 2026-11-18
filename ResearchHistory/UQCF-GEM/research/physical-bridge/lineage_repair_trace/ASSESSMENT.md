# When a leaf difference first reaches a retained parent row

Research assessment frozen before the numerical replay on November 18, 2026. This investigates the archived lineage repair model as a separate source from V1686.35.

## Source and premises

The implementation constructs an undirected tree from the existing parent addresses (lines 140–146). Its repair routine takes a damaged field $X_d$, a reference field $X_{\rm mem}$, protected rows $S$, a sweep count and a strength $s$. It copies the damaged field, restores the protected rows from memory and updates all rows synchronously. Each sweep replaces protected outputs with the same memory again, normalizes every row, then passes the resulting array into the next sweep (lines 411–431). The ordinary experiment selects the protection strategy and later uses the returned field. [Pinned source](https://github.com/proteinfoldingengine/WetLabEngine/blob/e7e01bab68ba5171dacd91333f98d208d810dac3/Tmp/TOE/retained_branch_identity_audit.py#L411-L451)

**Inherited within this implementation.** Tree, symmetric adjacency, fixed row addresses, synchronous update, seed reset, normalization with $\epsilon=10^{-12}$, reuse. **Supplied by this test.** Paired fields, a common reference, a fixed protected set per comparison and a single initially differing unprotected leaf. **Inherited native rule.** For an extensive scalar grade, P1 deletes the leaf $u$ and replaces the parent's grade with $x_p+x_u$. **Supplied for comparison.** Reading one input coordinate of a test vector as that grade. The historical repair retains its leaf and reads a fine field. Actual event occurrence would be an accepted input to a physical comparison. Mapping that event to repair, protection and owner access is open. [Native source contract](../p1_receiver_location_resolution/RESULT.md)

## Earliest unequal row in exact arithmetic

At an unprotected nonisolated row $r$, the update is

$$
 X^{k+1}_r=N_\epsilon\!\left((1-s)X^k_r+
               \frac{s}{d_r}\sum_{v\sim r}X^k_v\right),\qquad
 N_\epsilon(z)=\frac{z}{\|z\|+\epsilon}.
$$

Here $d_r$ is the degree in the original tree and $0<s\leq1$. Sweep zero denotes the input after the initial seed reset. For a finite tree with at least two vertices and finite real row vectors, compare two fields that differ only at an unprotected leaf $u$. For each vertex in its component of the forest obtained by deleting $S$, the first unequal row occurs at its graph distance from $u$. Every other vertex agrees at every sweep.

The source differs at sweep zero. Protected rows agree under every reset and normalization. A component separated by a protected vertex receives identical boundary values on every sweep and stays equal by induction. Within the source component, one synchronous pass can move a distinction at most one edge. For a row at distance $d>0$, exactly one neighbor lies at distance $d-1$. At sweep $d-1$ it already differs by induction. The other neighbors and the row itself still agree. The new mean therefore has a nonzero difference with coefficient $s/d_r$. Normalization preserves this difference over exact reals because it preserves direction and its output radius $a/(a+\epsilon)$ strictly increases from zero. This proves first arrival. Later persistence and a minimum resolvable signal are separate questions.

In particular the already designated parent $p$ differs after the first sweep when it is unprotected. Its new row enters the next update at neighbors. Clamping $p$ keeps it equal at every sweep. Protecting the leaf before starting erases the input contrast. The first-arrival result uses an order of sweeps and assigns no physical duration.

## Can the parent response be computed from the P1 output alone?

Hold the tree, strength, memory, protection and all other rows fixed, with $u,p$ unprotected. Consider two input fields with $B_u-A_u=\delta$ and $B_p-A_p=-\delta$. Adding the leaf into the parent gives identical coarse data on the whole retained tree. The one-sweep parent mean still changes by

$$
 m_p(B)-m_p(A)=\left(\frac{s}{d_p}-(1-s)\right)\delta .
$$

For arbitrary fine input rows, the parent output factors through the coarse sum exactly when $s=d_p/(d_p+1)$. Necessity follows from the displayed perturbation and injectivity. For sufficiency the two coefficients are equal, so the parent depends on their sum and on the other unchanged coordinates. The tagged coordinate may be a normalized nonnegative scalar grade, with a common second coordinate to keep directional differences measurable. This criterion concerns one parent row and one sweep. Different parent degrees require different strengths. With the archived default $s=13/20$ and degree two, the coefficient is $-1/40$. This comparison deliberately changes the fine initial parent as well as the leaf. It tests sufficiency of the coarse output, separately from acquisition by an initially equal parent.

## Frozen finite checks and decision rule

1. Use the original binary tree builder at depth two, source row 3, all other rows initially $(0,1)$, and source $(0,1)$ versus $(1,1)$. Use $(0,1)$ as the entire common reference. For each of the 64 subsets of the other six rows as protected seeds, compare every row through sweep five with independently calculated first-arrival distances. Include a protected-source control and a zero-strength control. These are prescribed fields and protected sets.
2. Use a depth-one binary tree, root parent and its two leaves. At seed fraction 0.05, compare the archived root and leaf strategies with identical RNG initialization. Nominate the source as the other leaf after reading the selected leaf and before preparing the fields. Both strategies protect exactly one row. The common memory and the receiver address stay fixed.
3. For the coarse-output test on the depth-one tree, protect the sibling. Set the first coordinate to one at the parent in A and at the source in B, to zero elsewhere, with the second coordinate one everywhere. Verify identical coarse data, different computed parent vectors at default strength, and matching vectors to rounding at the degree-matched strength $2/3$. Separately test binary64 saturation on collinear rows of size $10^8$ and $2\cdot10^8$ under the archived normalization expression.
4. Any mismatch in a prescribed calculation reopens its numerical conclusion. Finite agreement supports source correspondence for these fixtures. The proof supplies the exact-real reach. No gravity signal, P1 event implementation, physical owner, physical time or observational access follows.

[Earlier recombination assessment](../v1686_recombination_trace/ASSESSMENT.md) · [Bot source challenge](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6981935859)
