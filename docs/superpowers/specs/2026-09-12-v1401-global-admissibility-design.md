# UQCF-GEM v14.01 — Canonical Source-Dependent Global Admissibility Design

## Goal

Test whether the frozen pre-pruning/global-consistency architecture canonically produces a nontrivial source-dependent admissibility deformation

\[
\mathcal A_G \longrightarrow \mathcal A_G(s)
\]

or equivalently a source-to-global-defect/higher-incidence map \(\eta\), without importing time/entropy, Einstein/ADM targets, a fitted coupling, or a new source law by hand.

## Why this is a new series

v13.28 closed the downstream source→geometry absolute-coupling branch relative to the frozen ontology. v14.01 therefore moves upstream and asks whether the missing universality can originate in global relational consistency itself.

This gate is not allowed to reopen the v13.28 branch by renaming the missing coupling.

## Frozen ontology used by the gate

The audit treats the following as already available:

1. a fixed relational graph / incidence structure;
2. visible quantum-relational data and hidden-completion freedom;
3. a source/current sector with balanced node source \(s\);
4. global compatibility/positivity as a source-independent admissibility rule unless a source→constraint map is independently derived;
5. covariance/naturality under allowed relabelings/frame changes;
6. the exact distinction between source action on a state and source deformation of the admissibility law.

The gate does not assume spacetime, physical time, stress-energy, Newtonian gravity, or Einstein equations.

## Core distinction

Changing the state or visible boundary data while keeping the observation/compatibility map and positivity cone fixed is **source action inside a fixed admissibility architecture**. It is not by itself a derivation of a new law \(\mathcal A_G(s)\).

A nontrivial law-level deformation requires the source to enter the defining constraint/higher-incidence structure through a map of the schematic form

\[
\eta:S\to P,
\]

where \(S\) is the retained source representation and \(P\) is a global defect / higher-incidence representation.

## Gate outcomes

Exactly one of:

- `DERIVED`: the frozen ontology selects a nonzero canonical deformation, including its functional form up to only already-certified gauge equivalence.
- `NONUNIQUE`: nonzero lawful deformations exist, but the frozen ontology admits two or more inequivalent choices and does not select among them.
- `NO_NATIVE_DEFORMATION`: the frozen operations generate no nonzero deformation at all.

If the outcome is `NONUNIQUE` or `NO_NATIVE_DEFORMATION`, this audited branch stops. A later restart requires an explicit new source→higher-incidence axiom or independently calibrated cross-domain observable.

## Candidate audit

### A. Source action under fixed admissibility rule

Audit the current global-compatibility architecture schematically as

\[
\mathcal A_G(b)=\{X_{\rm aff}(b)+H:\;H\in\ker O_G,\;X_{\rm aff}(b)+H\succeq0\}.
\]

A source may change the state or visible argument \(b\), but if \(O_G\), \(\ker O_G\), and the positivity rule remain fixed, it has not supplied a new source-dependent law. Record this as `STATE_ACTION_NOT_LAW_DEFORMATION`.

### B. Incidence-only source→cycle defect

For an oriented graph incidence matrix \(B\), balanced node source \(s\), and cycle-space projector

\[
P_{\rm cyc}=I-B^T(BB^T)^+B,
\]

test the canonical incidence map

\[
\eta_0(s)=P_{\rm cyc}B^Ts.
\]

Because \(\operatorname{im}B^T\) is orthogonal to \(\ker B\), this must vanish:

\[
P_{\rm cyc}B^T=0.
\]

This is the incidence-only no-go.

### C. State/relational-weighted incidence maps

Permit a frozen edge scalar invariant \(\chi_e\) and positive diagonal edge weights obtained by covariant scalar functional calculus:

\[
W_f=\operatorname{diag}(f(\chi_e)).
\]

Then

\[
\eta_f(s)=P_{\rm cyc}W_fB^Ts
\]

can be nonzero because \(W_f\) need not preserve the cut/cycle orthogonal split.

Test three positive functions:

\[
f_1(x)=1+x,\qquad f_2(x)=e^x,\qquad f_3(x)=1+x^2.
\]

Required tests:

- nonzero defect for generic balanced sources;
- linear source scaling;
- covariance under vertex relabeling plus signed edge-orientation permutations;
- inequivalence of at least two normalized defect directions or operators.

If multiple such maps satisfy the same structural rules, covariance/naturality has not selected a unique \(\eta\).

### D. Global-positivity selector audit

Positivity must not be silently treated as a selector.

**Faithful interior.** For a positive-definite center \(X_0\succ0\), the PSD cone is open relative to the Hermitian space: every finite family of bounded Hermitian perturbations \(\Delta_a\) remains feasible for one sufficiently small common \(\epsilon>0\). Therefore interior positivity can certify multiple candidate directions simultaneously and cannot select one.

Use a fixed injective control embedding of the seven edge-defect coordinates into `Sym(4)` only to test this geometric fact; it is not a physical stress tensor or coframe map. Require a common positive \(\epsilon\) for all candidate/trial perturbations and a strictly positive minimum eigenvalue margin.

**Boundary.** For the simple PSD boundary point

\[
X_b=\operatorname{diag}(0,1,1,1),
\]

with kernel vector \(e_0\), first-order PSD feasibility requires

\[
e_0^T\Delta e_0\ge0.
\]

`Sym(4)` has dimension 10 and the equality lineality subspace \(e_0^T\Delta e_0=0\) has dimension 9. Thus the boundary supplies an inequality/normal cone, not a unique source→defect direction. Record this as `INEQUALITY_FILTER_NOT_CANONICAL_SOURCE_MAP`.

This closes the loophole that global positivity by itself might secretly pick one deformation at a compatibility boundary.

### E. Scale family

For any lawful nonzero \(\eta\), positive scalar multiples \(c\eta\) preserve linearity and covariance. Unless a normalization already exists upstream, this remains an additional nonuniqueness.

This is logically separate from the v13.28 downstream coupling scale, but mathematically analogous: structural covariance alone does not select a nonzero coefficient.

### F. Positive control

Supply an explicit new law by declaring both the weighting functional \(f_*\) and normalization \(c_*\). Verify that the deformation then becomes unique by construction. This demonstrates gate sensitivity and must be labeled `ADDED_LAW_POSITIVE_CONTROL`, not a derivation.

## Computational control

Use a deterministic 5-node / 7-edge connected graph (cycle dimension 3) and 256 balanced random source trials with fixed seed `1401`.

Use source scales

`[0.2, 0.5, 2.0, 5.0, 11.0]`.

Record:

- incidence-only cycle leakage norm;
- minimum weighted operator norm;
- max source-linearity error;
- max covariance error under signed edge / vertex permutations;
- maximum normalized direction separation between candidate weighted maps;
- rank of the span of candidate defect operators;
- faithful-interior common positivity radius and minimum margin;
- boundary tangent-cone lineality dimension;
- positive-control reconstruction error.

## Claim boundary

A `NONUNIQUE` result means only that the current frozen ontology does not select a canonical source-dependent admissibility deformation from the audited incidence/state-weighted/PSD-positivity construction class. It does not prove that no deeper nonlinear/global law can do so.

A `NO_NATIVE_DEFORMATION` result is even narrower: it means the audited frozen operations fail to generate a nonzero law-level deformation.

Neither outcome is a claim about gravity in nature.
