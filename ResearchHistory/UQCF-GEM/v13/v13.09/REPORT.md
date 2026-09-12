# UQCF-GEM v13.09 — Symmetry-Origin / Einstein-Sector Source Selection Gate

**Date:** 2026-09-12

## Adjudication

The successful v13.08 symmetry has now been separated into what it genuinely protects and what it does not.

### Positive theorem

Common `U(1)` axial symmetry plus equal/cyclic local data protects **BKM metric compatibility** to all orders.

### New no-go

The same visible symmetry does **not** protect full Levi-Civita sector preservation.

Hidden global completion data, invisible to all initial one- and two-body observables, can change the source evolution of the polar connection, holonomy, and solder closure.

Therefore v13.08's exact source-preserving sector requires more than visible pair symmetry.

## 1. Why U(1) symmetry protects Q=0

For one common axis n, U(1)-invariant faithful qubit marginals have BKM metric

`K = k_perp P_perp + k_parallel P_parallel`.

A pair connected-correlation map commuting with the same U(1) has its polar factor in that U(1).

Therefore

`O^T K O = K`.

If all local marginals are cyclically equal, QTC follows exactly.

The executed visible and hidden-completion flows both satisfy:
- axial-K residual below numerical precision;
- U(1)-transport residual below numerical precision;
- QTC below numerical precision.

Thus the source may move the polar angle and still remain metric-compatible.

This is an all-orders stabilizer protection of the **Q=0 sector**, not yet the torsion-free/full-LC sector.

## 2. Hidden completion defeats full LC preservation

Start from the exact v13.08 state:
- faithful;
- cyclic;
- U(1)-invariant;
- equal local marginals;
- identical pair correlations;
- QTC exact;
- fixed-RESA closure exact;
- holonomy angle `0.81`.

Now add the cyclic three-body operator

`G_hidden = sum_cyclic (sigma_x^i sigma_y^j - sigma_y^i sigma_x^j) sigma_z^k`

with amplitude

`eta=0.003`.

It satisfies:
- `[G_hidden,J_z]=0` to `0.000e+00`;
- cyclic invariance error `0.000e+00`;
- global state minimum eigenvalue `0.07175`.

Crucially, every one- and two-body marginal is unchanged:

maximum initial visible-data difference

`0.000e+00`.

So the original state and hidden-completion state are indistinguishable by the entire initial local/pair dataset used to construct K and O.

They also begin with the same QTC and solder closure.

## 3. Same source, different future geometry

Apply the exact same radial source

`P_z=(1/sqrt(3)) sum_i sigma_z^i`.

For the original visible completion, the polar angles remain fixed and v13.08 preserves LC exactly.

For the hidden completion, QTC remains exact but the polar phase drifts.

At `s=0.8`:

- max QTC defect: `7.000e-16`;
- max polar-map shift: `0.0687315907882`;
- fixed-RESA solder closure defect: `0.102077895732`;
- holonomy-angle shift: `0.145816075014`.

Thus:

`same visible initial geometry + same source != same retained connection evolution`.

The missing datum lives in the hidden completion.

## 4. Strong preservation requires hidden-completion phase rigidity

The full source-preserving LC stack now requires:

1. common stabilizer -> shared axial BKM metrics;
2. polar transports remain in that stabilizer -> QTC;
3. **hidden-completion phase rigidity** or an independently derived source-solder lift -> torsion-like closure / holonomy preservation.

Define:

**HCPR — Hidden-Completion Phase Rigidity**

HCPR requires source evolution of globally admissible hidden completion data to preserve the polar-phase relations needed by the retained solder/holonomy geometry.

HCPR is not derived.

## 5. Why current ontology does not select it

Global positivity cannot do it.

The hidden completion above is explicitly positive.

Relational identity cannot do it.

The v10.14 polar theorem is defined on generic distinct-singular-value pair data as well as enhanced-degeneracy strata. It selects the transport *given C*; it does not require C to lie on an axial-degenerate stabilizer stratum.

Provenance covariance cannot do it.

A symmetry group may act on a compatible hidden realization fiber without fixing each completion point. Replacing an orbit by its fixed points would be an additional invariance condition.

Protected source grading cannot do it either: it controls source amount/extensivity, not the hidden phase response of the global completion.

Therefore:

**the symmetry/stabilizer responsible for v13.08 is not derived by the current ontology.**

## 6. Maximality at fixed nonzero holonomy

The v13.08 curved sector has nonidentity SO(3) holonomy.

For a fixed holonomy H, solve

`[A,H]=0`, `A in so(3)`.

Fresh centralizer result:

- curved holonomy angle: `0.81`;
- centralizer dimension: `1`;
- centralizer axis / holonomy-axis alignment: `1`.

Thus the connected pointwise stabilizer of a fixed nontrivial SO(3) rotation is one-dimensional.

The v13.08 source line lies exactly on that axis and therefore **saturates the continuous fixed-holonomy stabilizer bound**.

This is the correct maximality statement.

It does not forbid:
- a larger symmetry that moves the holonomy axis by conjugation;
- state-dependent source lifts;
- non-symmetry-based preservation mechanisms.

## 7. Why a larger non-Abelian algebra requires more symmetry

Set the retained connection flat and isotropic:

- local marginals maximally mixed;
- pair correlations `C_ij=c I`;
- `O_ij=I`;
- holonomy identity.

Then the centralizer dimension jumps from 1 to

`3`.

A fresh positive three-qubit isotropic state was tested with collective sources

`P_x, P_y, P_z`.

Across finite tilts:
- QTC stays below numerical precision;
- transports remain identity;
- solder closure remains zero.

The operator commutators close:

`i[P_x,P_y] = -1.15470053838 P_z`,
`i[P_y,P_z] = -1.15470053838 P_x`,
`i[P_z,P_x] = -1.15470053838 P_y`

with maximum residual

`3.846e-16`.

So a larger non-Abelian `su(2)`-type collective source algebra **can** coexist with LC preservation—but in this executed control the holonomy is flat.

Noncommuting ETL tilts still compose additively in log-density coordinates with error

`9.203e-16`.

## 8. Architectural interpretation

The current hierarchy is now:

`flat isotropic sector`
-> enlarged SO(3) stabilizer
-> 3D non-Abelian collective source algebra

versus

`curved axial sector`
-> fixed-holonomy U(1) stabilizer
-> 1D abelian source line.

This is an exact stabilizer result inside the retained architecture.

It should **not** be promoted to a claim that physical gravity breaks an SU(2) source symmetry.

The gravity connection remains open.

## Status

- visible U(1) symmetry -> Q=0 preservation: **CLOSED CONDITIONAL**
- visible U(1) symmetry -> full LCSP: **FALSE**
- hidden completion affects source-holonomy evolution: **EXACT COUNTEREXAMPLE**
- HCPR: **NOT DERIVED**
- v13.08 1D source line maximal for fixed curved holonomy stabilizer: **YES**
- larger non-Abelian source algebra: **YES IN FLAT ISOTROPIC CONTROL**
- symmetry origin from current ontology: **NOT DERIVED**
- generic metric-affine parent: **REMAINS**
- Pillar 3: **OPEN**

No broad scientific breakthrough is declared.

This is, however, a major architecture theorem: the missing GR-sector source law has moved one level deeper—from visible pair symmetry to the hidden global completion.

## Next — v13.10

### Hidden-Completion Source Rigidity / Holonomy-Phase Preservation Gate

The next exact question is whether retained higher-order history/provenance information already sees the difference between:

1. the source-flow-rigid v13.08 completion, and
2. the phase-drifting hidden completion constructed here,

despite their identical initial one- and two-body data.

Audit W2/W3 provenance, SGOD-F3 boundary observables, and global atlas/history data.

If those already distinguish and select the rigid completion, HCPR may be derived.

If they do not, freeze HCPR as a genuinely new source-to-hidden-geometry law.
