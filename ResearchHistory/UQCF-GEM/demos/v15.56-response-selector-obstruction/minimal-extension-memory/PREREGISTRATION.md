# v15.71 Minimal extension memory and rebased null integrability — preregistration

Date: 2026-09-26. Parent: 0d90d48da6c121ae2e808930a9c5d10198abe437.
Branch: research/v15.71-minimal-extension-memory.

## Question

v15.70 proved that marginal state data alone cannot carry a nonzero hidden-to-retained source response. What is the smallest explicit source/extension memory that restores descent for the historical 27-label hidden family, without restoring the full 63-dimensional global tangent? If that memory is carried through ordered source updates, does the symmetric-null assignment integrate consistently when the base point is recomputed?

This stage tests one canonical enriched object. It does not claim that Nature selects it.

## Frozen hidden fiber and memory

Use the 27 HS-orthonormal exact-weight-three Pauli strings

    h_a = sigma_i ⊗ sigma_j ⊗ sigma_k / sqrt(8),  i,j,k in {X,Y,Z}.

For a fixed global base rho and displacement z=sigma-rho, define the extension-memory vector

    m_a(z) = Tr(h_a z),   m(z) in R^27.

This is exactly the coordinate vector of the component invisible to every two-body marginal.

For an arbitrary linear source label

    s = sum_a s_a h_a,

the historical fixed-base operator is

    N_s z = Y(rho) <s,z> = Y(rho) s·m(z).

The enriched retained chart for edge e carries

    (R_e sigma, m(z))

together with the retained base R_e rho and source coefficients s.

## Local retained lift

Do not obtain the regional response by restricting the already-computed global Y.

Independently reconstruct it from the retained two-qubit state:

1. compute its connected 3x3 correlation matrix C_e;
2. take the proper polar factor O_e;
3. define D_e=O_e/sqrt(3);
4. construct

       Y_e = (1/4) sum_ab (D_e)_ab sigma_a ⊗ sigma_b.

This is the v15.70 analytic restriction formula and uses only retained state geometry.

The enriched regional update is

    T^e_q = q + strength (s·m) Y_e,

where q=R_e sigma.

## Frozen descent measurement

- Reuse the exact 12 asymmetric states [13,16,22,25,27,29,37,39,46,50,66,77].
- Hidden probe eta=1e-4.
- Source strength=1e-3.
- Test every one of 27 hidden input basis directions against every one of 27 source basis labels, both hidden signs, and all three edges.
- This gives 52,488 enriched descent witnesses.
- Compare the independently constructed regional output to the literal partial trace of the global historical update.

Validity thresholds:
- memory coordinate error <=1e-12;
- local Y_e versus restricted global Y relative residual <=1e-10;
- enriched output residual <=1e-12 absolute and <=1e-9 relative when the predicted update is nonzero;
- all finite states trace/Hermiticity <=1e-12 and minimum eigenvalue >=-1e-12;
- base lift residual <=1e-10.

## Linear-memory minimality

The primary minimality claim is limited to linear memory that must support the complete 27-dimensional linear source-label family.

Compute the 27x27 evaluation matrix E_ab=Tr(h_a h_b). Require rank 27 and all singular values within 1e-12 of one.

Positive compression obstruction: use L=[I_26 0]. Inputs differing only in the omitted 27th hidden coordinate have identical compressed memory, while the 27th source label produces a nonzero retained output. This must be detected.

Interpretation if valid: 27 real memory coordinates are sufficient and, among linear memories supporting all source labels, necessary. For one fixed source label, only its single pairing scalar would be necessary.

## Frozen rebased integrability test

Use the enriched memory as persistent source/extension data. The ordered source-strength parameter is not fundamental time.

For each base state define Y(rho) with the unchanged v15.64 minimum-norm construction. Freeze a unit memory/source pairing so the scalar source coefficient is one, and examine the rebased assignment

    rho -> rho + c Y(rho).

Freeze total strengths

    c in [-1e-2,-3e-3,-1e-3,1e-3,3e-3,1e-2].

At every rebased state rho_c, independently recompute Y(rho_c) and each local retained Y_e(rho_c).

Require:
- ||Y(rho_c)-Y(rho)||/||Y(rho)|| <=1e-10;
- hidden-memory drift max_a |Tr[h_a(rho_c-rho)]| <=1e-12;
- edge polar-rotation change <=1e-10;
- local retained lift agrees with restriction of Y(rho_c) <=1e-10 relative;
- polar-skew null residual <=1e-10 relative;
- density and positive-polar strata remain positive.

Rebased composition: freeze increments a=4e-3 and b=-1.5e-3. Sequentially recompute the lift after the first increment. Compare a-then-b, b-then-a, and the direct combined increment a+b. Require all Frobenius residuals <=1e-11 globally and on every retained edge.

## Verdicts

Primary:
- MINIMAL_EXTENSION_MEMORY_DESCENT_CONFIRMED
- MINIMAL_EXTENSION_MEMORY_DESCENT_NOT_CONFIRMED
- INVALID

Orthogonal rebasing report:
- REBASED_NULL_INTEGRABILITY_CONFIRMED
- REBASED_NULL_INTEGRABILITY_NOT_CONFIRMED
- INVALID

GREEN CI means the frozen computation completed; either valid scientific branch exits zero. INVALID exits 2.

## Interpretation limits

Confirmation would show that the v15.70 descent obstruction is repaired by carrying the exact hidden-fiber source memory, and that this specific symmetric-null assignment remains integrable over the frozen regular neighborhood.

It would not establish a unique physical source memory, global arbitrary-strength positivity, tensor-product composition, a preferred source selector, or gravity. It would instead sharpen the next question: what first-principles law, if any, selects or generates this extension memory rather than postulating it.
