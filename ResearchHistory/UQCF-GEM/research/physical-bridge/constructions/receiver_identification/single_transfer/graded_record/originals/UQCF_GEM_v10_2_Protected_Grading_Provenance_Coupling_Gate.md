# UQCF–GEM v10.2 — Protected Grading Provenance-Coupling Gate

## Adjudication

\[
\boxed{
\texttt{WEIGHTED\_COMPOSITION\_PLUS\_BOUNDEDNESS\_FORCES\_AFFINITY}
}
\]

\[
\boxed{
\texttt{LOCAL\_COVARIANCE\_REDUCES\_ACCESS\_TO\_ONE\_SCALAR}
}
\]

\[
\boxed{
\texttt{PROTECTED\_GRADING\_FORCES\_N\_LINEARITY}
}
\]

\[
\boxed{
\texttt{P=GNT\_IS\_EXACTLY\_CLASSIFIED}
}
\]

\[
\boxed{
\texttt{GAIN\_REMAINS\_UNSELECTED}
}
\]

v10.1 established a consistent protected source grading \(N\), with protected integer amount
\(n\), while rejecting naive Hilbert-factor count.

v10.2 asks whether a second arbitrary source law is still required to couple this protected
amount to the intrinsic relational orientation \(t\).

The answer is stronger than expected.

Conditional on the explicit v10 grading architecture, the v9.218 weighted-composition law,
local covariance, and the all-count provenance bound, the response is forced to be

\[
\boxed{
F(n,t)=gnt
}
\]

for one real scalar

\[
\boxed{
|g|\le\frac12.
}
\]

No independent nonlinear function of \(n\) or \(t\) survives.

Thus the source-to-provenance **functional form closes**. Only one physical coupling scalar
remains.

This is a conditional structural theorem, not a gravity law.

## 1. Domain

Let

\[
V=
\operatorname{Herm}_0(C)\otimes\operatorname{Herm}_0(S)
\simeq
\mathbb R^3\otimes\mathbb R^3
\]

for the active qubit joint sector.

Let

\[
B_*=
\{t\in V:\|t\|_*\le1\}
\]

be the nuclear/projective carrier unit ball.

A source is described by

\[
(n,t),
\qquad
n\in\mathbb N,
\quad
t\in B_*.
\]

The weighted source composition retained from v9.218 is

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

for nonzero total \(n_1+n_2\).

Let

\[
F(n,t)\in V
\]

be the extensive provenance response.

Assume:

1. **independent-source additivity**
   \[
   F((n_1,t_1)\oplus(n_2,t_2))
   =
   F(n_1,t_1)+F(n_2,t_2);
   \]
2. **local covariance**
   \[
   F(n,R_CtR_S^T)
   =
   R_CF(n,t)R_S^T;
   \]
3. **all-count admissibility**
   \[
   \|F(n,t)\|_*\le\frac n2.
   \]

No linearity assumption is inserted.

## 2. Protected grading forces \(n\)-linearity

Take two identical source shapes:

\[
t_1=t_2=t.
\]

Then weighted composition leaves the normalized shape unchanged:

\[
(n_1,t)\oplus(n_2,t)
=
(n_1+n_2,t).
\]

Additivity therefore gives

\[
F(n_1+n_2,t)
=
F(n_1,t)+F(n_2,t).
\]

Since \(n\in\mathbb N\),

\[
\boxed{
F(n,t)=nF(1,t).
}
\]

Thus no nonlinear protected-count law

\[
h(n)t
\]

survives exact source additivity.

For any such law,

\[
h(n+m)=h(n)+h(m)
\]

forces

\[
h(n)=nh(1).
\]

## 3. Weighted composition forces midpoint affinity in \(t\)

Define

\[
f(t)=F(1,t).
\]

Compose two unit-token sources:

\[
(1,t_1)\oplus(1,t_2)
=
\left(
2,
\frac{t_1+t_2}{2}
\right).
\]

Using the \(n\)-linearity above,

\[
2f\left(\frac{t_1+t_2}{2}\right)
=
f(t_1)+f(t_2).
\]

Hence

\[
\boxed{
f\left(\frac{t_1+t_2}{2}\right)
=
\frac{f(t_1)+f(t_2)}{2}.
}
\]

So \(f\) obeys the midpoint Jensen equation on the full convex nuclear unit ball.

## 4. All-count boundedness eliminates pathological Jensen solutions

The provenance bound at \(n=1\) gives

\[
\boxed{
\|f(t)\|_*\le\frac12
}
\]

for every

\[
\|t\|_*\le1.
\]

A midpoint-affine function bounded on a convex set with nonempty interior is continuous and
affine.

Therefore

\[
f(t)=L(t)+c
\]

for a real linear map \(L\) and constant tensor \(c\).

No regularity assumption beyond the already-derived physical boundedness is needed.

This is the key step: **global admissibility supplies the regularity that kills pathological
Cauchy/Jensen solutions.**

## 5. Covariance removes the affine offset

At

\[
t=0,
\]

local covariance requires

\[
f(0)=R_Cf(0)R_S^T
\]

for every independent pair

\[
R_C,R_S\in SO(3).
\]

The joint representation

\[
(3,3)
\]

contains no invariant vector.

Therefore

\[
\boxed{
f(0)=0.
}
\]

The affine map is actually linear:

\[
f(t)=L(t).
\]

## 6. Schur classification gives one scalar

The linear map must intertwine the local product-group action:

\[
L(R_CtR_S^T)
=
R_CL(t)R_S^T.
\]

The joint representation

\[
V=(3,3)
\]

is irreducible over the product group.

Therefore

\[
\boxed{
\operatorname{End}_G(V)=\mathbb R I.
}
\]

The executable commutant calculation gives exact dimension

\[
\boxed{1}.
\]

Hence

\[
\boxed{
L(t)=gt
}
\]

for one real scalar \(g\).

Combining with the grading result:

\[
\boxed{
F(n,t)=gnt.
}
\]

This is not an ansatz. It is the complete classified form under the declared assumptions.

## 7. Nonlinear covariant controls

Covariance by itself is not enough.

Two explicit nonlinear maps transform in the same joint representation.

### Quadratic cofactor map

For a \(3\times3\) carrier,

\[
\boxed{
t\mapsto\operatorname{cof}(t)
}
\]

obeys

\[
\operatorname{cof}(R_CtR_S^T)
=
R_C\operatorname{cof}(t)R_S^T
\]

for

\[
R_C,R_S\in SO(3).
\]

The checker verifies covariance to error below

\[
2\times10^{-16}.
\]

But its median midpoint-additivity defect on random normalized carriers is about

\[
0.0874.
\]

### Cubic map

Likewise,

\[
\boxed{
t\mapsto tt^Tt
}
\]

is locally covariant.

Its covariance error is below

\[
7\times10^{-16},
\]

but its median midpoint defect is approximately

\[
0.0831.
\]

Therefore:

\[
\boxed{
\text{covariance permits nonlinear access laws;}
\quad
\text{weighted composition eliminates them.}
}
\]

## 8. Exact gain interval

The classified law is

\[
F(n,t)=gnt.
\]

For

\[
\|t\|_*\le1,
\]

all-count provenance admissibility requires

\[
|g|n\|t\|_*
\le
\frac n2.
\]

Therefore

\[
\boxed{
|g|\le\frac12.
}
\]

This is sharp by the rank-one carrier controls retained from v9.217.

Every

\[
g\in[-1/2,1/2]
\]

is already known to be compatible with the declared provenance cone.

So the exact response class is

\[
\boxed{
\left\{
F_g(n,t)=gnt:
-\frac12\le g\le\frac12
\right\}.
}
\]

## 9. What the grading does and does not solve

The protected grading now fixes two things that were previously free:

1. total source amount is \(n\);
2. dependence on source amount is exactly linear.

The weighted composition law then fixes the dependence on \(t\) to a linear intertwiner.

Local covariance fixes that intertwiner to the identity shape.

Thus there is **no second arbitrary source functional**.

However, the scalar \(g\) remains.

Because the token amount unit was fixed in v10.0/v10.1, this is no longer a source-unit
convention.

It is a genuine remaining physical coupling parameter.

## 10. Internal grading-sector state details

Once the source law is declared to depend on the protected amount \(n\) and the relational
carrier \(t\), arbitrary internal density-state details within the same grading sector do not
enter the classified response.

The executable controls vary internal-state purity while keeping

\[
(n,t)
\]

fixed and reproduce the same response exactly.

This is not a theorem that all possible future physics ignores internal sector data. It is the
closure statement for the specific minimal \(F(n,t)\) source architecture.

## 11. Scientific meaning

Conditional on the explicit v10 grading extension, the source-to-provenance law has now been
reduced from an arbitrary functional to a single scalar:

\[
\boxed{
(n,t)
\longmapsto
gnt.
}
\]

This is substantial structural closure.

The remaining physics is sharply localized:

\[
\boxed{
\textbf{what selects }g?
}
\]

No range law, attraction sign, spatial distance, metric, spacetime, or gravity follows from the
classification theorem.

The result is therefore a **conditional source-law form theorem**, not a gravity
identification.

## 12. Status

**THEOREM:** protected replication/additivity forces linearity in \(n\).

**THEOREM:** weighted composition gives midpoint Jensen affinity in \(t\).

**THEOREM:** the all-count provenance bound supplies enough regularity to force an affine map.

**THEOREM:** local covariance removes the affine offset.

**THEOREM:** the joint-sector equivariant endomorphism space is one-dimensional.

**CLASSIFICATION THEOREM:**

\[
\boxed{
F(n,t)=gnt,
\qquad
|g|\le\frac12.
}
\]

**COUNTEREXAMPLE:** nonlinear covariant maps exist but fail weighted composition.

**SELECTION BOUNDARY:** no current theorem fixes sign or magnitude of \(g\).

**ARCHITECTURE CONDITIONALITY:** the theorem depends on the explicit protected grading and
weighted-additive source composition introduced after the v9.222 stop boundary.

**NO GRAVITY BREAKTHROUGH DECLARED.**

## 13. Next gate

**v10.3 — Gain Selection / Processor Realizability Gate.**

The remaining scalar is now isolated.

Test whether every

\[
g\in[-1/2,1/2]
\]

can be implemented by a grading-preserving source-independent quantum processor.

Then audit:

1. complete positivity;
2. grading preservation;
3. local covariance;
4. sign reversal under intrinsic orientation reversal;
5. vacuum compatibility;
6. finite-angle fluctuation constraints retained from v9.199–200.

If the entire interval remains operationally realizable, record

\[
g
\]

as an irreducible new physical coupling primitive rather than choosing or fitting it.
