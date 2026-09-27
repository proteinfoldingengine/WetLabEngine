# v15.72 Operational mixture-affinity gate

Frozen 2026-09-26 America/Los_Angeles, before implementation/measurement.
Parent: `068abcc33ea69b9f1f3d8beaff55194b969ff710`.
Branch: `research/v15.72-operational-mixture-affinity`.

## Question

Does the v15.71 memory-enriched null law define an affine update of the density matrix when no preparation/conditioning record is supplied? If not, does the resulting preparation-dependent discrepancy enter the retained polar-skew sector?

We test the unchanged X_h(rho)=Tr(h rho)Y(rho) and T_s=rho+s X_h(rho). A fixed unconditioned CPTP map is linear on operators, hence affine on density matrices. Failure of affinity excludes that interpretation. Passing affinity would NOT establish positivity, complete positivity or a physical law. This gate does not impose unconditioned CPTP dynamics on the whole UQCF-GEM program.

## Frozen ensemble

Unchanged v15.58 selector, seed20260928, indices [13,16,22,25,27,29,37,39,46,50,66,77]. One fixed source h=XXX/sqrt(8) throughout. All 27 HS-unit weight-two Pauli v, in v15.71 order. No new random frames or state selection.

eta=1e-4, delta=1e-4, s=1e-3, mixture weights p=[.25,.5,.75]. For each base and v:

    a = rho+eta h+delta v
    b = rho-eta h-delta v
    r = p a+(1-p)b
    J = p X_h(a)+(1-p)X_h(b)-X_h(r)
    finite_gap = p T_s(a)+(1-p)T_s(b)-T_s(r) = s J.

972 cases. Compute J directly from vector fields, not by dividing small differences of states. Independently verify the finite identity. Compare density matrices before applying the nonlinear geometry extractor.

## Frozen diagnostics and controls

- Same Python3.11/numpy2.3.5/OPENBLAS_NUM_THREADS=1 environment.
- Validate every input, pooled input, updated endpoint, pooled updated output and updated pooled input: trace/Hermiticity <=1e-12, density eigenvalue >=-1e-12, positive regular polar factors and minimum edge singular >=.015.
- All diagnostics finite, exact counts/identities. Baseline hidden memory <=1e-12. Memory affinity error <=1e-12, showing the supplied scalar itself averages linearly.
- Finite identity ||finite_gap-sJ|| <=1e-14; J trace/one-body moment residuals <=1e-12.
- Normalized field defect j=||J||/[4p(1-p)eta delta]. Frozen affinity threshold 1e-6. Absolute field and finite gaps also reported.
- At p=.5, verify J/(eta delta) against analytic DY_rho[v] from v15.71, with error ||difference||/max(1,||DY||)<=1e-4. This is a numerical identity/control, not fitting an exponent or response.
- Affine control: fixed local unitary U=(I-i X_0)/sqrt(2), channel rho->U rho U-dagger; mixture defect <=1e-12 and source activity >1e-6.
- Hidden-only control a0=rho+eta h,b0=rho-eta h (same retained data/Y): vector-field mixture defect <=1e-12.
- Visible-only control av=rho+delta v,bv=rho-delta v (zero hidden memory): vector-field mixture defect <=1e-12.
- Positive sensitivity control F(rho)=Tr(h rho)^2 v: defect is exactly 4p(1-p)eta^2 v. Relative error <=1e-8 and norm >1e-10.
- Individual branch null check: rotations before/after each endpoint's source update differ <=1e-10. A failure is reported as a scientific secondary-gate failure, not rescued by reinterpreting the source.

## Retained skew discrepancy

For each normalized tangent D=J/[4p(1-p)eta delta], compute the full connected-correlation derivative DC_e at the pooled input r, including derivatives of one-body subtraction terms. Then Q_e=O_e(r)^T DC_e-DC_e^T O_e(r). Represent each skew block in the HS-orthonormal three-component basis and stack three edges: a nine-component column.

For each original state and each p, assemble its 27 columns. Report all singular values and ranks at relative tolerances [1e-9,1e-10,1e-11], using no fitted threshold. The p=.5 map has a common pooled base rho. At other p the pooled base varies with v; those ranks are finite-probe matrix ranks, not the rank of one fixed-base differential. The secondary decision uses only p=.5.

## Verdicts

Primary, with all controls/validity satisfied:

- UNCONDITIONED_MIXTURE_AFFINITY_OBSTRUCTED if any normalized field defect exceeds 1e-6.
- MIXTURE_AFFINITY_NOT_OBSTRUCTED_ON_PROBES otherwise (no CPTP certification).
- INVALID for any validity/control failure, exception, missing case or nonfinite diagnostic.

Secondary PREPARATION_DEPENDENT_SKEW_CONFIRMED if all twelve p=.5 matrices have rank[9,9,9], the primary is obstructed, and every individual-branch rotation check passes. Otherwise PREPARATION_DEPENDENT_SKEW_NOT_CONFIRMED. INVALID primary implies INVALID secondary. Valid negative outcomes exit zero; INVALID exits2.

## TDD/publication and scope

Publish this file, derivation, tests and workflow with gate.py absent; inspect expected Actions RED before implementation. Then run GREEN, inspect exact scientific JSON/log, download/hash artifact and preserve full results and exact commit/run/job/artifact provenance. No merge to main, no old verdict changes, no threshold changes after observation.

Preparation dependence is not a gravity signal. A recorded selective operation or preparation-dependent controller has additional inputs and is not ruled out by this gate; neither is established here. The memory-enriched existence result remains valid in its earlier scope. No physical source-law selection or global admissible-world deformation is claimed.
