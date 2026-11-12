# UQCF–GEM v9.179 — Connected Native-Incidence Interaction Gate

## Adjudication

**CONNECTED_PAIR_DENSITY_IMPRINT_ACTIVATES_HIDDEN_PAIR_MODE__COUPLING_POSTULATED**

The gate constructs a new, explicitly hypothesized interaction from the already
specified compatible pair density and the marked native A–B incidences. In the
same-source two-specimen example, this interaction converts a selected hidden
completion correlation into an original-pair measurement difference. All terms
are two-body on the six original five-level factors. No extra coherent qutrit
reference, selected outcome, or fitted response coefficient is introduced.

The activation is proved by an exact invariant-subspace reduction, a nonzero
fourth-order response coefficient, and a rigorous small-angle remainder bound.
Original-space matrix calculations corroborate the result and quantify a much
smaller signal than the background state change.

This is a conditional operational mechanism, not a native source law or a gravity
breakthrough. The density-to-interaction assignment, specimen preparation relation,
copy registration, signs, strengths and unitary family remain physical hypotheses.
The pair density is a fixed operator-valued input. It is not updated from the
instantaneous evolving state, and no nonlinear feedback law is derived.

## Version and evidence

v9.178 explicitly proposed this gate as v9.179. v9.172 remains reserved for the
separate saturation-boundary audit; B1 remains an unnumbered precursor. The
supplied v9.178 report was read in full. Its unchanged v9.173 parent constructor
is retained in reference/ and rerun for both arrangements.

The local gate specification follows analytic planning, including exploratory
8-dimensional calculations, and precedes the recorded final checker. It is NOT
external preregistration. The main hypothesis uses all marked native A–B edges
and the complete supplied compatible pair density, not a subset selected by
maximizing the hidden signal. Ablations diagnose the resulting mechanism.

## 1. New H179: fixed pair-density imprint on native incidences

One specimen is S=A B1 B2, with each factor five-dimensional. A registered second
specimen is S'=A' B1' B2'. Native edges in each specimen are A–B1 and A–B2. Let
sigma be the common, compatible pair marginal of the retained parent optimum T0.
This sigma is NOT the original incompatible target rho and NOT the optimal dual
witness W. The two arrangements have their own sigma, fixed before the probe.

Let F_x exchange the corresponding registered factor x,x', identity elsewhere.
Postulate the Hermitian generator

\[
 K=g_AF_A+g_1F_{B_1}+g_2F_{B_2}
   +\lambda_1(\sigma_{AB_1}+\sigma_{A'B'_1})
   +\lambda_2(\sigma_{AB_2}+\sigma_{A'B'_2}).                 \tag{1}
\]

Every embedded sigma acts on its two original factors only. Added spectators
remain outside the marked supports. Equation (1) can equivalently be specified
by its expectation on all joint densities: add the marked exchange expectations
and the overlaps of each native pair marginal with the supplied sigma. Such an
expectation clause fixes the operator by linearity; it does not establish the
physical truth or uniqueness of the clause.

Motivation: test whether interaction at the existing relational incidences can
connect the three otherwise independent role channels of v9.178. The whole
local pair description is used without an eigenvector or hidden-coherence
selection. Interpreting a density operator as an interaction coefficient is a
NEW constitutive hypothesis, not a theorem of compatibility. It is not a choice
of the optimizer as a state evolution, and it is not a claim that an unknown
state can program this gate from one copy without resources.

The primary convention is g_A=g_1=g_2=lambda_1=lambda_2=1. Partner exchange
requires equal B coefficients, not equality with g_A or with lambda. Strength,
relative strength and sign are not derived. Set U(theta)=exp(-i theta K).
Theta is a dimensionless probe angle, not emergent or external physical time.
The law is a reversible candidate interaction relation, not pruning.

## 2. Valid inputs, spectators and covariance

Retain t=21/41,z=16 and

\[
 e=|0,4,4\rangle,\quad f=|2,1,1\rangle,\quad Z=|e\rangle\langle f|,
 \quad b=9/820,\quad h=9/1640.
\]

T0 has isolated diagonal entries b on e,f. The same-source joint input is

\[
 \Omega(m)=T_0\otimes T_0+m(Z\otimes Z^\dagger+Z^\dagger\otimes Z),
 \qquad m=\kappa h^2,\quad 0\le\kappa\le1.                 \tag{2}
\]

The modified block on |e,f>,|f,e> has diagonal b^2 and off-diagonal m;
its eigenvalues are b^2 +/- m, strictly positive at the selected m=h^2.
Normalization and all one-specimen marginals are unchanged. All initial original
pair marginals coincide for every m. The complete initial specimen spectra
need not coincide; m is genuine hidden joint correlation, not a coordinate label.
The preparation is supplied, as in v9.175–176, not produced by cloning or a source
operation. H176 need not be true for this two-specimen calculation: any retained
preparation with the same kappa has the same Omega_2.

For any spectator E and any correlated state Xi on the active system plus E,

\[
 \operatorname{Tr}_E[(U\otimes I_E)\Xi(U^\dagger\otimes I_E)]
   =U\operatorname{Tr}_E(\Xi)U^\dagger.                     \tag{3}
\]

Hence spectators with unchanged active marginal are exactly neutral in every
dimension. Absorbing a spectator into an active role and redefining sigma or
F_x is a different interaction specification, not the same neutrality comparison.

Under local coordinate changes, transform sigma and the role registrations
along with all states and effects; K transforms by conjugation and probabilities
are unchanged. In the displayed parent coordinates each sigma commutes with
D tensor conjugate(D), so K also commutes with the parent common phase torus
on the six factors. No Hilbert-amplitude map is extracted from edge provenance.
With equal edge coefficients, K and the input are symmetric under partner
exchange, ensuring equal AB1 and AB2 outputs. Outputs need not stay optimal for
the original static compatibility problem.

## 3. An exact 8-dimensional invariant support inside dimension 15,625

Write u=(0,4,4), v=(2,1,1). For a placement bit string x=(x_A,x_1,x_2), put u_x
in the first specimen and v_x in the second when x=0 on that role, and reverse
them when x=1. The eight resulting coordinate kets span H_*.

These are positions of original labels across specimens, NOT new physical
qubits, pooled states, spatial positions or the 315/311 completion dimensions.
The full input difference in (2) lies on H_* and has normalized form

\[
 C=|000\rangle\langle111|+|111\rangle\langle000|,
 \qquad\Omega(m)-\Omega(0)=m C.                            \tag{4}
\]

Vertical role swaps preserve H_* and act as placement Pauli X_x.
For every ket in H_*, the A labels belong to {0,2}, while B labels belong to
{4,1}. They are disjoint. The parent sigma has only diagonal entries on these
A-not-equal-B coordinates; its non-diagonal entries connect only |ii> and |jj>.
Consequently all native pair-density terms preserve H_* too.

Define four actual pair populations

\[
 s_{04}=\langle04|\sigma|04\rangle,\quad
 s_{01},\ s_{24},\ s_{21},\qquad
 J_0=\tfrac12(s_{04}+s_{21}-s_{01}-s_{24}).                 \tag{5}
\]

For the parent class s_ab=(1-t)V_ab/50 when a!=b. Then, up to an irrelevant
identity term, the exact restriction of (1) is

\[
 \boxed{K_*=g_AX_A+g_1X_1+g_2X_2+J_1Z_AZ_1+J_2Z_AZ_2,\quad
 J_j=\lambda_j J_0.}                                     \tag{6}
\]

This is a three-placement-spin transverse-field Ising matrix. That label names
a standard matrix form; no Ising source or emergent spatial geometry is inferred.
For the two retained pair states,

\[
 J_0^A=1/41,\qquad J_0^B=4/205.                            \tag{7}
\]

Their scalar identity offsets at the primary strengths are 22/205 and 24/205.
The differences between arrangements are explained by already different LOCAL
pair populations. They are not attributed to different hidden-fiber dimensions.

The checker verifies all eight full-space support columns with exact radicals,
not just a projected Hamiltonian assumed to be closed. It separately constructs
the full 15,625-dimensional sparse generator and checks closure numerically.

## 4. Exact hidden-to-pair activation

Use the block population contrasts on original factors

\[
 D_A=|0\rangle\langle0|-|2\rangle\langle2|,\quad
 D_B=|4\rangle\langle4|-|1\rangle\langle1|,
 \quad E_{AB_1}=(I+D_A\otimes D_B)/2.                     \tag{8}
\]

E is a valid effect and invariant under the parent phase group. It is a stated
readout of the known hidden block; it was not used to choose K's native support
or its full pair-density coefficients. We also use the input effect sigma itself
and the complete pair trace norm. The original Bell projector is a negative
readout control.

For real m, the hidden pair difference is diagonal on (04,01,24,21). The
placement complement X_A X_1 X_2 commutes with K_* and C, so complementary
placement probabilities coincide. The trace of C is zero. These facts force

\[
 \Delta\sigma_{AB_1}(\theta)=\frac{mR_1(\theta)}2 D_A\otimes D_B,
 \quad
 R_1(\theta)=\frac12\operatorname{Tr}
 [Z_AZ_1e^{-i\theta K_*}Ce^{i\theta K_*}].                \tag{9}
\]

The second pair has the analogous R2. Hence

\[
 \Delta p_{AB_1}=mR_1,\qquad
 D(\sigma_m(\theta),\sigma_0(\theta))=|mR_1|.              \tag{10}
\]

All original single-factor hidden differences vanish for this real m,
but a pair correlation can now be nonzero. This is a change from v9.178.
The pair effect sigma already supplied as input has gap

\[
 \operatorname{Tr}(\sigma\Delta\sigma_{AB_1})=mJ_0R_1.     \tag{11}
\]

Thus the existence of the effect is not confined to a custom block diagnostic.
The Bell projector is insensitive to the same difference because it is supported
on |ii>, disjoint from (04,01,24,21).

### First nonzero coefficient and a rigorous finite interval

Repeated commutation in the exact eight-state matrix gives

\[
 \boxed{R_1(\theta)=-\tfrac83 J_2g_Ag_1g_2\theta^4+O(\theta^6),}
\]
\[
 \boxed{R_2(\theta)=-\tfrac83 J_1g_Ag_1g_2\theta^4+O(\theta^6).} \tag{12}
\]

All coefficients of orders zero through three vanish. Odd orders vanish for
these real symmetric input, generator and readout matrices. The exact sixth
coefficient for R1 is

\[
 \frac4{45}J_2g_Ag_1g_2
 (11J_1^2+6J_2^2+20g_1^2+6g_2^2+6g_A^2).
\]

The trace formula (9) is exact at every angle; (12) is explicitly a local
expansion, not a fitted full-angle formula. For the primary positive unit
strengths, ||K_*||<=3+2J0<4. The trace norm of C is 2 and ||E||<=1, so Taylor's
remainder after order five is bounded by

\[
 |R_1+(8/3)J_0\theta^4|\le\frac{2\,8^6}{6!}|\theta|^6.    \tag{13}
\]

For BOTH parent arrangements and 0<|theta|<=1/200, the right side is less than
(4/3)J0 theta^4. Therefore

\[
 \boxed{\Delta p_{AB_1}\le-(4/3)mJ_0\theta^4<0\quad(m>0).} \tag{14}
\]

This conservative interval proves actual nonzero activation, rather than only a
formal Taylor coefficient. The population sign is tied to declared readout and
coupling signs. It is not gravitational attraction.

### Balanced all-angle spectral reduction

When g_A=g_1=g_2=g and J1=J2=J, partner symmetry and placement complement reduce
the part accessed by C to two three-dimensional blocks:

\[
 K_+=\begin{pmatrix}2J&g&\sqrt2g\\g&-2J&\sqrt2g\\
 \sqrt2g&\sqrt2g&g\end{pmatrix},\quad
 K_-=\begin{pmatrix}2J&-g&\sqrt2g\\-g&-2J&\sqrt2g\\
 \sqrt2g&\sqrt2g&-g\end{pmatrix}.                          \tag{15}
\]

With Q=diag(1,-1,0) and v=(1,0,0), the exact function in (9) is one half of
<v|exp(i theta K+) Q exp(-i theta K+)|v> minus the analogous K- expression.
There is no numerical diagonalization threshold defining these sectors.

## 5. Mechanism controls: graph connectivity is necessary, not sufficient

1. **No native horizontal terms:** J1=J2=0 gives the v9.178 null exactly.
2. **Only A–B1 coupling:** J2=0 leaves AB1 blind to this hidden mode, at every
   angle. The B2 placement channel is still disconnected from that readout.
   Interchanging the indices gives the corresponding AB2 null.
3. **Bell-only connected graph:** replacing each horizontal source-density term
   by the parent Bell projector connects the same graph but annihilates every ket
   in H_*. The hidden trajectory is exactly the role-only trajectory. Bare graph
   connectivity alone does not imply operator-level access.
4. **Diagonal off-diagonal-coordinate part of sigma:** on H_* it has exactly the
   same action as full sigma. The hidden response is caused by the local
   population contrast (5) acting jointly with the exchanges, NOT by the Bell
   coherence part of sigma.
5. **Reverse the native-edge coefficient:** the leading sign reverses. The finite
   deterministic control uses lambda1=lambda2=-1 without any optimization.

For control 2, the omitted placement bit is dynamically separate. Tracing that
role removes its traceless tensor factor; equivalently, summing its diagonal
contribution in the placement reduction gives zero. The proof does not rely on
small-angle truncation.

Connected matrices and noncommuting couplings permit the access, but they are
standard quantum observability ingredients. The calculation supplies no claim
that this is a gravity-specific residue.

## 6. Numerically evaluated predictions at the fixed displayed point

At kappa=1, h=9/1640, unit strengths and theta=pi/4:

| Quantity | Arrangement A | Arrangement B |
|---|---:|---:|
| J0 | 1/41 | 4/205 |
| Pair probability difference | -3.6718640001e-7 | -2.9377271178e-7 |
| Pair trace distance | 3.6718640001e-7 | 2.9377271178e-7 |
| Source-effect sigma probability difference | -8.9557658538e-9 | -5.7321504738e-9 |

The larger pair differences are approximately -0.00003671864 and
-0.00002937727 **percentage points**, respectively. They are small. These decimal
values are evaluations of (9), corroborated in the full original space, not
claimed closed algebraic values at pi/4.

The original-space background and changed-input pure ancillary amplitudes give,
for the block diagnostic in arrangement A, approximately

- baseline probability: 0.5129317538309607;
- with hidden correlation: 0.5129313866445607.

The background state can change much more than this difference. Only the
subtracted, matched-input difference is the hidden activation signal. There are
no experimental observations or feasibility estimates for measuring it here.

## 7. What is and is not a new physical result

Relative to v9.178, the candidate now combines exact spectator neutrality,
connected original two-body support, common-phase covariance, and nonzero
same-source hidden-to-pair activation. No extra phase-sensitive detector or
reference qutrit was inserted. The second specimen's specified joint preparation
already carries the invariant relational resource.

The successful interaction does not follow merely from knowing that the original
pair states coexist. H179 declares that these pair matrices enter a Hamiltonian
linearly and are held fixed during the probe. Its strengths and their signs are
not selected by compatibility. This does NOT derive same-provenance identification,
relative registration, stress-energy, source magnitude, a universal force sign,
spatial dependence, gauge dynamics, spacetime, physical time, or pruning.

The exact small-angle response is fourth order for this selected input and
readout. It is not a Newtonian linear response or an inverse-square law.
The A/B response differences depend on local pair populations; do not attribute
them to the 315/311 extension-family dimension difference. No claim is made that
all hidden directions respond or that this mode is physically privileged.

The all-state fixed-image no-go is not contradicted: each unitary moves a state
inside the original finite-dimensional density-state domain. The admissibility
map is unchanged. Pair equality persists for the displayed exchange-symmetric
inputs but no preservation theorem for every nonsymmetric equal-marginal input
is asserted.

## 8. Computation and reproducibility

The final checker performs:

- the unchanged exact parent density/PSD/dual/equal-marginal checks for A and B;
- sixteen exact original-space invariant-support columns (eight per arrangement);
- symbolic nested commutators through order six for independent gA,g1,g2,J1,J2;
- exact balanced 3+3-sector matrices and the rational Taylor remainder bound;
- full entrywise integer-character covariance and specimen-exchange identities;
- 170 deterministic full-15,625-dimensional sparse exponential comparisons:
  two arrangements, five declared variants, seventeen angles;
- whole original-pair reductions from the propagated two-column hidden support,
  rather than only checking a scalar readout;
- full 15,625-by-625 positive background ancillary amplitudes propagated once per
  arrangement, then exact two-column block replacement to produce the propagated
  positive hidden-input amplitude and directly recompute its pair probability;
- a separate 64-dimensional complete-apparatus basis covariance check and a
  128-dimensional correlated-spectator test. These small tests are explicitly
  not presented as full five-level spectator simulations. The analytic proofs
  establish the general covariance and spectator statements.

The 8-dimensional model is an exactly embedded invariant support for the
**difference**. It is not a replacement for the full background state or a claim
that the whole quantum system has eight dimensions. The entire state is mixed on
the observed factors but represented by explicit pure ancillary amplitudes; no
physical mixing, discard or collapse is simulated.

The first checker invocation encountered an unevaluated symbolic zero in a strict
Python equality assertion. Simplifying that algebraic expression repaired the
implementation; the hypothesis, coefficients, cases and tolerances were unchanged.
The final logged run includes the added direct hidden-amplitude check. Results
are deterministic corroboration; no p-value, numerical universality, or external
preregistration is claimed.

## 9. Gate table

| Gate | Result |
|---|---|
| Explicit interaction premise independent of hidden signal optimization | New H179, stated |
| Native A–B support connected to marked cross-specimen roles | Yes |
| All interaction summands two-body on original six factors | Yes |
| Fixed-support spectator neutrality | Exact |
| Full-apparatus covariance / common phase invariance | Exact |
| Same-source selected hidden correlation becomes pair-visible | Yes, exact local theorem |
| Nonzero signal from Bell-only connectivity | No, exact dark-support control |
| An original one-factor readout detects this real hidden mode | No |
| Whole hidden fiber or physical source universality established | No |
| Native interaction rule or gravitational interpretation derived | No |

**Next proposed v9.180 — Full-Fiber Observability and Mechanism-Specificity Gate.**
Keep H179, its input-data rule and coefficients fixed. Determine which feasible
hidden directions in the actual completion fibers become pair-visible, which
remain protected, and what response distinctions are already explained by the
local operator algebra. Do not optimize a new interaction or equate an increase
in observable rank with gravity. A physical source law still needs independent
justification; this continuation audits the conditional mechanism, not its origin.

## 10. Primary context and originality boundary

The effect is an application of standard finite-dimensional quantum observability
and noncommuting interaction dynamics. There is no literature-priority claim.
The contribution is the new-hypothesis audit, exact placement-sector reduction,
fourth-order coefficient and finite-interval certificate inside this retained
UQCF–GEM completion model.

- D. D'Alessandro, *On Quantum State Observability and Measurement*,
  arXiv:quant-ph/0307127. https://arxiv.org/abs/quant-ph/0307127
- S. Lloyd, M. Mohseni, P. Rebentrost, *Quantum principal component analysis*,
  arXiv:1307.0401; Nature Physics 10, 631–633 (2014),
  DOI 10.1038/nphys3029. Density operators used as generators are an existing
  quantum-information construction; no algorithmic resources, implementation
  procedure or claimed speedup is imported here.
- Parent source: UQCF–GEM v9.178 Tensor-Factor Interaction-Support, read fully;
  v9.173 parent constructor retained unchanged, rebuilding v9.167–171 data.

See results/run_summary.json, response_scan.csv and execution.log for the final
recorded residuals. The attached notebook embeds the same implementation and
parent source; its fresh-kernel execution status is recorded in NOTEBOOK_EXECUTION.json.

## Recorded final results

```json
{
  "version": "v9.179",
  "classification": "CONNECTED_PAIR_DENSITY_IMPRINT_ACTIVATES_HIDDEN_PAIR_MODE__COUPLING_POSTULATED",
  "all_checker_assertions_passed": true,
  "native_interaction_derived": false,
  "all_angle_analytic_scope": "Exact invariant subspace; fourth-order coefficient and rigorous local sign interval",
  "exact": {
    "coefficients_per_unit_m": {
      "0": {
        "AB1": "0",
        "AB2": "0"
      },
      "1": {
        "AB1": "0",
        "AB2": "0"
      },
      "2": {
        "AB1": "0",
        "AB2": "0"
      },
      "3": {
        "AB1": "0",
        "AB2": "0"
      },
      "4": {
        "AB1": "-8*J_2*g_1*g_2*g_A/3",
        "AB2": "-8*J_1*g_1*g_2*g_A/3"
      },
      "5": {
        "AB1": "0",
        "AB2": "0"
      },
      "6": {
        "AB1": "4*J_2*g_1*g_2*g_A*(11*J_1**2 + 6*J_2**2 + 20*g_1**2 + 6*g_2**2 + 6*g_A**2)/45",
        "AB2": "4*J_1*g_1*g_2*g_A*(6*J_1**2 + 11*J_2**2 + 6*g_1**2 + 20*g_2**2 + 6*g_A**2)/45"
      }
    },
    "parity_reductions_exact": true,
    "small_angle_upper_bound": "1/200",
    "remainder_bound_per_m": "2*8^6*theta^6/6!",
    "negative_signal_bound_per_m": "-(4/3)*J*theta^4, nominal equal couplings",
    "bound_is_strict_for_both_arrangements": true
  },
  "parent": {
    "A": {
      "J": "1/41",
      "identity_offset": "22/205",
      "eight_support_columns_verified_exactly": 8,
      "original_dimension": 15625,
      "parent_positive_equal_pair_primal_dual_certificate": true,
      "Bell_only_edges_annihilate_hidden_orbit": true,
      "new_interaction_on_hidden_orbit": "sum g_x X_x + J1 Z_A Z_B1 + J2 Z_A Z_B2 + scalar I"
    },
    "B": {
      "J": "4/205",
      "identity_offset": "24/205",
      "eight_support_columns_verified_exactly": 8,
      "original_dimension": 15625,
      "parent_positive_equal_pair_primal_dual_certificate": true,
      "Bell_only_edges_annihilate_hidden_orbit": true,
      "new_interaction_on_hidden_orbit": "sum g_x X_x + J1 Z_A Z_B1 + J2 Z_A Z_B2 + scalar I"
    }
  },
  "numerical": {
    "full_original_dimension": 15625,
    "full_sparse_hidden_difference_comparisons": 170,
    "angles_per_case": 17,
    "background_amplitudes_propagated": 2,
    "errors": {
      "invariant_support": 0.0,
      "full_hidden_pair_vs_exact_reduction": 2.7614038177331916e-15,
      "unitary_column_norm": 4.551927089490217e-15,
      "pair_population_shape": 1.8864564666391135e-15,
      "single_site_hidden": 2.753012043523567e-15,
      "partner_hidden_equality": 0.0,
      "source_effect_identity": 1.1626538346646057e-16,
      "bell_hidden_null": 0.0,
      "absent_missing_edge_null": 2.752849043972395e-15,
      "full_character_covariance": 0.0,
      "specimen_exchange": 0.0,
      "Bell_ablation_support": 0.0,
      "background_normalization": 1.3322676295501878e-15,
      "background_pair_equality": 1.3183898417423734e-16,
      "background_imaginary": 6.154799841002114e-20,
      "hidden_amplitude_normalization": 1.3322676295501878e-15,
      "hidden_amplitude_pair_reconstruction": 7.93272824883254e-18,
      "absolute_probability_crosscheck": 5.749881992110845e-17
    },
    "small_system_controls": {
      "covariance_64_dimension_operator_error": 8.400361489980554e-16,
      "correlated_spectator_128_dimension_error": 1.1188630228279524e-16
    },
    "snapshots": {
      "A": {
        "arrangement": "A",
        "variant": "connected",
        "theta": 0.7853981633974483,
        "J": 0.024390243902439025,
        "probability_gap": -3.671864000056698e-07,
        "trace_distance": 3.671864000056698e-07,
        "source_effect_gap": -8.955765853796617e-09,
        "per_unit_m": -0.012192401746361103,
        "other_pair_per_unit_m": -0.012192401746361103,
        "hidden_block_probability_from_pure_amplitude": 0.5129313866445606,
        "background_block_probability": 0.5129317538309607,
        "hidden_block_probability": 0.5129313866445607,
        "background_source_effect_probability": 0.12433252860786653,
        "hidden_source_effect_probability": 0.12433251965210068,
        "background_amplitude_shape": [
          15625,
          625
        ]
      },
      "B": {
        "arrangement": "B",
        "variant": "connected",
        "theta": 0.7853981633974483,
        "J": 0.01951219512195122,
        "probability_gap": -2.9377271178094103e-07,
        "trace_distance": 2.9377271178094103e-07,
        "source_effect_gap": -5.732150473774497e-09,
        "per_unit_m": -0.009754704760568136,
        "other_pair_per_unit_m": -0.009754704760568136,
        "hidden_block_probability_from_pure_amplitude": 0.5103938711745213,
        "background_block_probability": 0.5103941649472331,
        "hidden_block_probability": 0.5103938711745213,
        "background_source_effect_probability": 0.12435903504577692,
        "hidden_source_effect_probability": 0.12435902931362644,
        "background_amplitude_shape": [
          15625,
          625
        ]
      }
    },
    "tolerance": 2e-11
  },
  "elapsed_seconds": 27.882774114608765
}
```

Fresh-kernel notebook status:

```json
{
  "status": "completed",
  "code_cells": 4,
  "errors": 0,
  "fresh_working_directory": "/tmp/v9179_notebook_tk2qocav",
  "elapsed_seconds": 34.94042682647705
}
```

The initial user-visible plot save failed on output-directory permissions; it was rerun successfully after correcting only those permissions. The displayed figure and archive contain the successful result. No mathematical data or graphical scaling was changed in that repair.
