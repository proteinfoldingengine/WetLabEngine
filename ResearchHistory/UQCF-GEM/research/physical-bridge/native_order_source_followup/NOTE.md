# Retained-order source follow-up: the scalar control is nonassociative

Author: proteinfolding-gpt, research session with Aaron. Date: 2026-10-28 America/Phoenix.
Inspected shared research head: `c5cefae1b1dd8d877d1a919c27f4196eb150e353`.
Status: exploratory source finding and elementary analytical correction; UNREVIEWED. Native bridge NOT_DERIVED. This is a brief Class C source assessment, not a new A mechanism, numbered stage, or claim of mathematical priority.

## 1. The concrete operation recovered

The retained-order investigation first checked the existing receiver-process and observation-effect arguments. They already cover propagation by later P1 contractions and supplied later motions; those results are not new progress here. A bounded search for the older V957/V960 generation code and V970 fitting code did not recover those implementations. It did return a separate, actual implementation, `v1735_native_algebraic_law_hardening.py`, and its explicitly imported dependency, `v1730_native_nonmetric_law_audit.py`. Both complete source texts were read. This is new input to this pass, not a claim that these files were unknown throughout the project.

The strongest useful positive fact is that this route has an explicit update to inspect, rather than only a fitted response table. V1730 defines, for six-component real vectors, a default coupling `G=0.17` and cyclic shift `roll`:

    star(a,b,g,assoc=False) = a + g*(roll(a)*b - a*roll(b)).

The products on the right are componentwise. V1735 consumes the resulting associator bank and a separately constructed shear tensor. This identifies the implementation being tested. The inspected files do not derive this update or the coupling from P1, a lineage retraction, or an occurring measurement. V1730's order-neighbor sample is explicitly `q2=roll(q)`; it is supplied in the dataset generator. V1735 itself declines a universal retained-order transport/balance law.

## 2. Exact correction to the declared associative control

The same `star` function's `assoc=True` branch is

\[
a\star_g b=(1+g\mu(b))a,\qquad
\mu(b)=\frac1n\sum_{i=1}^n b_i.
\]

V1730 comments that this is an "associative/linear-ish control" and labels it "associative control" in execution. V1735 describes "associative collapse" and uses the same branch. Its scalar linear-update interpretation is valid. Its associativity interpretation, for the binary operation that the code actually tests, is not.

For the source's associator convention,

\[
\begin{aligned}
(a\star_g b)\star_g c
  &=(1+g\mu(b))(1+g\mu(c))a,\\
a\star_g(b\star_g c)
  &=[1+g(1+g\mu(c))\mu(b)]a.
\end{aligned}
\]

Subtracting gives the exact identity

\[
\boxed{A_g(a,b,c)=g\mu(c)a.}
\]

Thus for every nonzero g the branch fails associativity on its declared vector domain. Take n=6, a=c=(1,1,1,1,1,1), b=0 and g=17/100. The left parenthesization is (117/100)a, the right is a, and the associator is (17/100)a. The special g=0 branch returns a and is associative. Composition of the scalar update operators as functions is also associative; that is a different expression from the binary associator implemented here.

## 3. Why a vanishing shear control does not fix this

For `assoc=True`, the implementation gives

\[
J(q)=[1+g\mu(q)]I,
\qquad M(q)=m(q)I,
\]

where m includes the source's scalar eigenvalue-floor adjustment. Its coded derivative and connection arrays are

\[
(dG)_{aij}=(g/n)\delta_{ij},\qquad
\Gamma_{mai}=(g/n)\delta_{mi}.
\]

Direct substitution into its `Q_tensor` formula therefore gives

\[
Q_{aij}=(g/n)(1-2m(q))\delta_{ij}.
\]

Every a-slice is proportional to I, so the implemented Euclidean trace subtraction `shear_part` removes it identically. Consequently the coded Q_shear and K_Q vanish in this branch even though the binary associator above need not vanish. This is an identity of the implementation's formulas; it does not assert that its coded derivatives equal derivatives of the clipped metric everywhere. At q=0 the floor is inactive, so that qualification does not affect the example.

For example, the bank includes A(e_i,0,e_j)=(g/n)e_i, which is nonzero for g nonzero, while Q_shear(0)=0. The control's shear collapse is therefore compatible with nonassociativity. It cannot serve as a contrast between an associative operation and the other operation, or isolate nonassociativity as the source of shear. This does not refute every possible A-to-Q map: a map can send nonzero associator features to zero. Nor does it invalidate all reported fits or diagnose their numerical accuracy.

## 4. Consequence for the unresolved bridge

The recovered route supplies a vector update, coupling, order-neighbor map, metric construction and diagnostic. The two inspected files contain no derivation identifying these with an actual pruning event and an existing receiver-owned record. A prediction score for the supplied diagnostic would not establish that missing association. The operation is a conditional model to study, not an inherited physical interaction earned by calling it native.

The new finding is the explicit control correction, not a physical no-go. P1, the accepted receiver-process mathematics, and PR #123 are untouched. No replacement operation, fitted coupling, receiver, or physical axiom is adopted. No old numerical campaign was replayed and no new scientific enumeration was run. A small rational-arithmetic substitution checked the displayed witness after the analytical result was known; it is not a prospective experiment or independent verification campaign.

Both complete returned source texts and their source identifiers are preserved alongside this note. Their readback byte lengths match the reported file lengths. The manifest hashes the returned UTF-8 texts; original binary downloads and historical execution results were not independently verified. No archive-wide absence claim follows from the unsuccessful V957/V960/V970 code search.

Before this correction becomes accepted research evidence, independent review must check the two parenthesizations, the Q_shear substitution, the exact meaning of the source's control label, and the limited physical conclusion. No Gemini acceptance, merge, milestone, or schedule change is claimed here.
