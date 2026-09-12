# UQCF-GEM Gate Changelog

Append-only research ledger. Detailed evidence and executable controls live in each gate directory.

## 2026-09-12

### v13.14 — Symmetry-Reduced Sufficient State / Schur-Weyl ETL Closure

- Re-tested the v12.47 Schur-Weyl compression against the actual ETL/PGRL source-response problem rather than exchange dynamics alone.
- Exchange/permutation commutant remains an exact ETL-invariant sector when both state and source lie inside it, but the state dimension remains Catalan and exponential.
- Adding collective frame sources enlarges the exact invariant algebra to total-spin `J` blocks with exact dimension `D_N = binom(2N,N)(3N-1)/(2N-1)` and asymptotic scaling `(3/(2 sqrt(pi))) 4^N/sqrt(N)`.
- Two positive `N=3` states with identical total-J block projection have different projected ETL response under the same site-local source (`0.0533333334` gap), so block data are not sufficient for generic local QMAR.
- A single site-local Pauli couples adjacent total-J sectors and reduces the remaining center commutant to scalars for every tested `N=2..8`; by double-commutant/Burnside reasoning the generated unital *-algebra is the full operator algebra.
- Therefore exact Schur-Weyl compression survives only in symmetry-compatible restricted source sectors; it collapses for the site-resolved geometry/source class used by QMAR.
- Next: v13.15 Relational Locality / Sparse Source Closure.

### v13.13 — Hidden-Completion Response State / Minimal Markov Closure

- Proved the v13.10 chiral three-body scalar is not a sufficient hidden response coordinate: identical one/two-body data plus identical chiral scalar can still yield different QMAR source-response jets.
- At a generic faithful three-qubit point, the complete 27-dimensional weight-three Pauli hidden sector maps into the all-local-source QMAR response with rank **27/27** while every one/two-body marginal remains unchanged.
- Therefore fixed `N=3` exact response closure requires the full three-body moment sector, which is equivalent to complete state tomography.
- Proved an exact **ETL/PGRL finite-moment hierarchy no-go**: for every finite `k`, positive commuting states identical on all moments through weight `k` can have different source derivatives of a retained `k`-body observable because of hidden `(k+1)`-body parity.
- Product/factorization closure fails exactly under generic two-body ETL source deformation.
- RCCL remains the correct missing architecture: retain the required higher-incidence state or derive a canonical exact lifting/closure.
- Next: v13.14 Symmetry-Reduced Sufficient State / Schur-Weyl ETL Closure.

### v13.12 — Shear Nonmetricity / Curvature Response Coupling

- Defined the gauge-covariant traceless shear observable `Sigma_ij = dev(log G_ij)` after removing the exact trace/Weyl sector.
- Closed a two-way structural independence result: one exact control has zero shear response with nonzero holonomy response; a complementary PGRL control has nonzero shear response with zero holonomy response.
- Therefore shear nonmetricity does not determine curvature/holonomy response, curvature does not determine shear, and no universal zero-intercept norm bound connects them in the current kinematics.
- A constant-linear shear-to-holonomy candidate failed generic holdout (`R^2=-0.0488`); this was used only as a falsification test, not as a fitted field equation.
- Preserved the claim boundary that the older shear-dominated `Q~g -> R~g^2` Retained Bridge result belongs to a different connection and cannot be imported without a typed bridge.
- Next: v13.13 Hidden-Completion Response State / Minimal Markov Closure.

### v13.11 — Metric-Affine Source Response / Nonmetricity-Torsion Dynamics

- Derived a conditional first-order **Quantum Metric-Affine Response operator (QMAR)** from PGRL/ETL through BKM metric and polar transport differentials.
- Verified source linearity and independent local-frame covariance of the response stack.
- Proved the **BKM Trace-Exactness Theorem**: `tr log G_ij = log det K_i - log det K_j`, hence closed-cycle trace/Weyl nonmetricity circulation vanishes exactly and under source response.
- Random generic 24-channel response audit found rank 23/24; the sole constant-linear null aligned exactly with the trace-cycle identity.
- Demonstrated torsion-like response is not canonical without a source-to-solder/coframe lift.
- Proved geometric source-response non-autonomy: identical instantaneous visible geometry can have different connection/holonomy response jets because of hidden completion.
- No autonomous metric-affine field equation, action, stress-energy law, or Einstein equation is derived.

### v13.10 — Hidden-Completion Source Rigidity / Holonomy-Phase Preservation

- Proved a **Frozen-Ledger HCPR Non-Factorization Theorem** for the executed rigid/drifting completion pair.
- The two positive completions have identical initial one/two-body data, BKM metrics, polar transport, Gamma_R, F2/F3, W1/W2/W3, J_R, and atlas schema projection.
- Their source-response jets differ immediately; the hidden completion generates polar, holonomy/F3, and solder-closure response while the rigid completion does not.
- W2/W3 are certificates rather than hidden-completion selectors; SGOD-F3 diagnoses post-source connection divergence but cannot select the rigid initial completion.
- **HCPR is frozen as IRREDUCIBLE RELATIVE TO THE CURRENT FROZEN LEDGER.**
- HCPR origin search: **STOP**. Next branch returns to the generic metric-affine parent.

### v13.09 — Symmetry-Origin / Einstein-Sector Source Selection

- Proved/verified that common visible axial `U(1)` stabilizer structure protects BKM metric compatibility (`Q=0`).
- Constructed a positive cyclic `U(1)`-invariant hidden three-body completion with exactly the same initial one/two-body data but different source-driven polar phase / holonomy evolution.
- Isolated **HCPR — Hidden-Completion Phase Rigidity** as the next missing law.
- Fixed nontrivial `SO(3)` holonomy centralizer is 1D; v13.08 source line saturates it.
- Flat isotropic control admits a 3D non-Abelian collective source algebra.

### v13.08 — LCSP Integrability / Source Superselection Algebra

- Generic connected LC family: fixed local-Pauli source tangent intersection is trivial in the tested class.
- Found a symmetry-selected exact finite LC-preserving source sector.
- Identified a 1D abelian radial PGRL/ETL source algebra preserving QTC, solder closure, and nonzero holonomy in that sector.
- Generic LCSP remains not derived.

### v13.07 — LCSP Origin / Source-Compatible Levi-Civita Morphism

- Closed exact first-order metric compatibility tangent equation.
- Closed independent torsion/solder tangent equation.
- Demonstrated PGRL source tangents are not generically LC tangent.
- Demonstrated PGRL does not select the solder lift.
- First-order tangency can fail at second order; isolated **SCLL**.

### v13.06 — Levi-Civita Sector Closure Under Retained Operations

- LC sector is not closed under the full retained operation set.
- Gauge/frame changes, strict disjoint composition, and compatible q-isometric/solder-compatible morphisms preserve it.
- Generic source insertion and unconstrained refinement leave the sector.
- Isolated **LCSP — Levi-Civita Sector Preservation Law**.

### v13.05 — Metric-Affine Pillar-3 / Einstein-Sector Minimality

- Reframed generic parent kinematics as metric-affine.
- Closed theorem: `Q=0` and `T=0` are jointly necessary/sufficient for `Gamma=Gamma_LC(q)`.
- Demonstrated the LC sector can retain nonzero curvature/holonomy.
- Distinguished sector restriction from observable-changing Levi-Civita projection.

### v13.04 — Score-Metric Refinement Regularity

- Existing PGRL, RESA, CRCL/AVT, and polar composition do not force BKM nonmetricity density convergence.
- Isolated **SMRRL**, **SMAVT**, and **QZL** roles.
- Metric-affine continuum closes only conditionally on added regularity; LC limit additionally needs Q-zero selection.

### v13.03 — Non-Metricity Continuum Fate / Projection No-Go

- Corrected continuum discriminator: raw `N_h -> 0` does not imply metric compatibility.
- Derived logarithmic edge-length-normalized BKM nonmetricity density.
- Exhibited smooth finite nonzero metric-affine continuum.
- Metric-compatible projection changes holonomy and is not a gauge transformation.

### v13.02 — QTC Origin / BKM-Holonomy Naturality

- QTC is not derived by polar correlation transport and is generically false.
- Exact qubit criterion isolated matching marginal spectrum + radial-axis transport condition.
- Derived a gauge-covariant discrete BKM nonmetricity defect.
- HLCB blocked generically before torsion.

### v13.01 — Metric-Origin Branch Stop / HLCB Dependency Reduction

- Froze MEA/BIFL as explicit conditional metric input.
- Local SMI closed conditional on MEA.
- Isolated QTC as independent metric-transport compatibility condition and TFHC as the subsequent torsion condition.
- Showed one universal overall metric scale does not affect the HLCB connection test.
