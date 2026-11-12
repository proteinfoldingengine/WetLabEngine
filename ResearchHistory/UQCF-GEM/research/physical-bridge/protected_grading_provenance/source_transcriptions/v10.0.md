# UQCF–GEM v10.0 — Minimal Protected Source Primitive Consistency Gate

## Adjudication

\[
\boxed{
\texttt{MINIMAL\_PROTECTED\_SOURCE\_PRIMITIVE\_IS\_FREE\_ONE\_GENERATOR\_POSITIVE\_MONOID}
}
\]

\[
\boxed{
\texttt{UNIT\_FIXING\_UNIQUELY\_GIVES\_W\_EQUALS\_COUNT}
}
\]

\[
\boxed{
\texttt{WEIGHTED\_PROVENANCE\_STACK\_IS\_CONSISTENT}
}
\]

\[
\boxed{
\texttt{PHYSICAL\_TOKEN\_IDENTITY\_REMAINS\_NEW\_AXIOM}
}
\]

v9.222 reached an irreducible-law stop boundary: the frozen architecture contained no
canonically selected nonzero protected total source amount.

v10.0 therefore does not claim another derivation from the frozen theory.

It introduces the **smallest explicit protected-sector extension** capable of supporting a
nonzero additive amount that is unique after one unit choice.

The new primitive is a protected source token \(s\), with source sectors forming the free
commutative monoid on that one generator:

\[
\boxed{
\mathcal Q_{\rm src}
=
\langle s\rangle_+
\simeq
\mathbb N.
}
\]

Source-blind local quantum operations may alter the ordinary state/provenance-shape data but
cannot create, destroy, or change the protected token count.

This is an explicit new axiom, not a hidden consequence of v9.

## 1. Minimality theorem

### Zero protected generators

With no protected generator, the only sector is the monoidal vacuum.

Every nonnegative additive amount is therefore zero.

### One free generator

Let the protected sector be

\[
\mathbb N s.
\]

Any additive amount obeys

\[
f((n+m)s)=f(ns)+f(ms).
\]

Therefore

\[
\boxed{
f(ns)=\kappa n.
}
\]

Fixing one primitive token to one amount unit,

\[
f(s)=1,
\]

gives

\[
\boxed{
w_{\rm total}(n)=n.
}
\]

The amount is then unique.

### One generator with a nontrivial relation

Suppose instead the generator obeys

\[
rs=qs,
\qquad r\ne q.
\]

Additivity gives

\[
rf(s)=qf(s),
\]

hence

\[
\boxed{f(s)=0}.
\]

So a nonzero additive real amount requires the generator to remain free of such collapsing
relations.

### Two or more free generators

For two protected generators,

\[
\mathcal Q=\mathbb N^2,
\]

unit fixing on the first still leaves the relative amount of the second arbitrary.

Thus the free one-generator positive commutative monoid is the smallest sector architecture
with:

- nonzero total amount;
- additivity;
- one-dimensional amount cone;
- unique amount after one unit normalization.

## 2. Protected processing rule

A source datum is now

\[
\boxed{
x=(n,\rho,t,\ldots),
}
\]

where

\[
n\in\mathbb N
\]

is protected.

Allowed source-blind local processing acts on the ordinary quantum data but satisfies

\[
\boxed{
n\longmapsto n.
}
\]

Therefore

\[
w_{\rm total}=n
\]

survives arbitrary state replacement inside a fixed token sector.

The executable checks explicitly vary density-state purity while keeping \(n\) fixed.

## 3. Integration with the weighted carrier

v9.218 introduced the weighted carrier

\[
(w,t),
\qquad
\|t\|_*\le1,
\]

with barycentric composition.

The new primitive fixes

\[
\boxed{w=n.}
\]

Thus the carrier becomes

\[
\boxed{
(n,t),
\qquad
n\in\mathbb N.
}
\]

Independent composition is

\[
\boxed{
(n_1,t_1)\oplus(n_2,t_2)
=
\left(
n_1+n_2,
\frac{n_1t_1+n_2t_2}{n_1+n_2}
\right)
}
\]

for nonzero total count.

The nuclear unit ball remains closed by convexity.

The numerical closure error is at machine precision.

## 4. Replication

For one token sector with shape \(t\),

\[
(1,t)^{\oplus n}
=
(n,t).
\]

Therefore:

\[
\boxed{
\text{protected amount}=n,
}
\]

while the normalized relational shape remains unchanged.

This gives the clean separation:

\[
\text{count/amount}
\neq
\text{shape}.
\]

## 5. Provenance response compatibility

Retain the weighted provenance response

\[
\boxed{
P=gnt.
}
\]

The all-count nuclear bound requires

\[
\boxed{
|g|\le\frac12.
}
\]

For every

\[
n\ge0,
\qquad
\|t\|_*\le1,
\]

this gives

\[
\|P\|_*
\le
\frac n2.
\]

Independent source composition remains exactly additive:

\[
P_{12}=P_1+P_2.
\]

So the new protected token extension is fully compatible with the v9.218 weighted provenance
cone.

## 6. What this extension closes

Once the new primitive is accepted:

1. the protected total amount is no longer an arbitrary additive functional;
2. the amount unit is fixed by the primitive-token convention;
3. the v9.218 amount/gain rescaling degeneracy is removed;
4. product sources can have nonzero total amount;
5. local quantum processing does not erase that amount.

Mathematically,

\[
\boxed{
w_{\rm total}=n
}
\]

is then closed.

## 7. What remains open

The physical access gain still obeys only

\[
\boxed{
-\frac12\le g\le\frac12.
}
\]

Nothing in v10.0 selects one value.

More importantly, the architecture does not derive why:

- one elementary physical source corresponds to one protected token;
- a composite/bound source contains a definite integer token count;
- mere refactorization of one global source cannot change the token count;
- local processing must preserve token number.

Those are now the physical content of the extension.

Thus the one-token primitive is **minimal**, but not derived.

## 8. No force law follows

The protected token \(n\) carries an extensive scalar only.

By itself it provides no:

- relational orientation;
- propagation rule;
- range dependence;
- attraction/repulsion sign;
- spatial distance;
- metric;
- spacetime;
- gravity.

Therefore this gate is a source-sector consistency result, not a force derivation.

## 9. Status

**EXPLICIT ARCHITECTURE EXTENSION:** introduce one protected source token \(s\).

**THEOREM:** the free one-generator positive monoid is minimal for a nonzero additive amount
unique after one unit fixing.

**THEOREM:** unit fixing gives

\[
w_{\rm total}=n.
\]

**THEOREM:** the resulting integer-weighted carrier is associative, additive, replication
extensive, and compatible with the all-count provenance cone.

**THEOREM:** every universal gain

\[
|g|\le1/2
\]

remains globally admissible.

**SELECTION BOUNDARY:** \(g\) remains free.

**NEW AXIOM BOUNDARY:** the physical meaning and invariance of the protected token are not
derived from v9 kinematics.

**NO GRAVITY BREAKTHROUGH DECLARED.**

## 10. Next gate

**v10.1 — Protected Token Naturality / Splitting Gate.**

The next test is essential because naive count semantics are dangerous.

Require the protected token assignment to be invariant under **mere refactorization of the same
global source** while remaining additive under genuinely independent source composition.

Test:

1. subdivision of one source into tensor factors;
2. regrouping of factors;
3. formation of composite/bound sources;
4. indistinguishable-token symmetrization;
5. spectator addition;
6. source merger/splitting represented only by a change of factorization.

If token count depends on arbitrary Hilbert-factor bookkeeping, reject the primitive.

Only if a factorization-independent token law exists can \(n\) remain a viable protected total
source amount.
