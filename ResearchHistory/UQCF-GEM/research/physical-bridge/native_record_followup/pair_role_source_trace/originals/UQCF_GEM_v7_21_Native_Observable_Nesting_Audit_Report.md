# UQCF-GEM v7.21 — Native Observable-Nesting Audit

## 1. Commutative retained observables do nest canonically

Let a pruning/coarsening step be a quotient

\[
\pi:X_p\to X_q.
\]

Then retained observables at the coarse level are pulled back by

\[
\pi^*:C(X_q)\to C(X_p),
\qquad
(\pi^*f)(x)=f(\pi(x)).
\]

This map is automatically unital, injective, multiplicative, and
\(*\)-preserving.

Therefore

\[
\boxed{
C(X_q)\hookrightarrow C(X_p)
}
\]

is canonical for every genuine quotient, regardless of the sizes of the
pruning fibers.

This is precisely the v7.7 constant-on-fibers algebra and supplies the v7.20
forward state restriction.

## 2. The noncommutative pair-groupoid lift is different

Suppose the reversible atlas fiber on \(X\) is the pair groupoid. Its algebra is

\[
\mathbb C[\operatorname{Pair}(X)]
\cong M_{|X|}(\mathbb C).
\]

The object/ledger algebra is its diagonal subalgebra.

The quotient \(\pi:X_p\to X_q\) fixes the diagonal pullback:

\[
E_{yy}
\mapsto
\sum_{x\in\pi^{-1}(y)}E_{xx}.
\]

The right side has rank

\[
|\pi^{-1}(y)|.
\]

But all minimal diagonal projections \(E_{yy}\) of \(M_m\) are equivalent via
the matrix units \(E_{yz}\). Any \(*\)-homomorphism preserves that equivalence,
so their images must have equal rank.

Hence:

\[
\boxed{
\text{a diagonal-compatible unital }*
\text{-hom }M_m\to M_n
\text{ requires all pruning fibers to have equal size.}
}
\]

For unequal fibers the full matrix-algebra inclusion is impossible.

## 3. Equal fibers are still noncanonical

Even if every fiber has common size \(k\), an extension requires choosing
unitary identifications between the fiber spaces.

For the smallest nontrivial case, two coarse classes each containing two fine
objects,

\[
\Phi_U:
M_2(\mathbb C)\to M_4(\mathbb C)
\]

may be defined by

\[
\Phi_U
\begin{pmatrix}
a&b\\
c&d
\end{pmatrix}
=
\begin{pmatrix}
aI_2 & bU^\dagger\\
cU & dI_2
\end{pmatrix},
\qquad U\in U(2).
\]

Every \(\Phi_U\) is a unital \(*\)-homomorphism.

All choices agree exactly on the diagonal ledger algebra, yet differ on
off-diagonal observables.

Therefore:

\[
\boxed{
\text{ledger quotient data}
\not\Rightarrow
\text{canonical noncommutative lift}.
}
\]

## 4. Match to the frozen retained-pair protocol

V1696.2 explicitly defines retained pair identity as a quotient/equivalence-class
object, not a cross-scale vector transport. A coarse class exists only when the
fine classes form a compatible role-preserving family; otherwise it is undefined.

That is exactly enough to support the commutative quotient-observable branch.

But the frozen rule does not require:

- equal coarse-fiber multiplicity;
- unitary identification between fine members;
- an arrow map between reversible pair-groupoid transitions.

So it does not yet define the full noncommutative observable inclusion.

## Status

\[
\boxed{
\text{commutative observable nesting: CLOSED where the coarse quotient exists}
}
\]

while

\[
\boxed{
\text{noncommutative atlas/core nesting: OPEN}.
}
\]

The next minimal question is whether the already-frozen
role/orientation/provenance/order-preserving transformations of retained pair
classes satisfy the coherence laws of an arrow-level groupoid functor.

If they do, their linearization may supply the missing \(*\)-map. If they do
not, the exact missing coherence law should be isolated rather than inserting a
UCP map by hand.
