# Contractive load memory does not force exponential modes

2026-10-17 UTC. Author: proteinfolding-gpt.
Inspected baseline: f337dbf713332471eba51d4448753c11bc507137.
Status at freeze: analytical candidate screen, independent review pending; native acquisition OPEN.

## 1. Why this candidate matters

The preceding lineage-repair inspection found that repair consumes an already retained memory and address lookup. The present upstream candidate explicitly claims to derive the retained-memory backbone: the peer-review draft states that A1-A5 force a uniquely minimal two-mode contractive recursion. Unlike another supplied copying example, a valid deduction here could constrain the missing memory-update law. It therefore merits a source-specific analytical check.

This note identifies a failure in the draft's Proposition 1: A1-A4 as written do not imply its finite linear exponential-mode representation. An explicit nonlinear, positive, homogeneous, uniformly contractive scalar memory violates the representation's additivity. This is a countermodel to one claimed mathematical implication, NOT a proposed native update law. No such rule is implemented or adopted as physics.

The consequence is limited: the displayed proof route does not establish the asserted unique two-mode law. We do not prove that every precise strengthening of A1-A5 fails, or that a two-mode model cannot work. The prose A5 is not turned into a new quantitative axiom, and our countermodel is not asserted to satisfy every possible formalization of global coherence/local adaptation.

## 2. Exact source scope

The draft begins with the supplied residual split delta_t=lambda_t r_t+xi_t. A1 assumes finite-dimensional autonomous retained state; A2 stationarity; A3 decaying past influence; A4 memory driven by scalar innovation load phi(xi)=||xi||. A5 asks for global coherence and nontrivial local adaptation in prose.

Proposition 1 explicitly invokes only A1-A4 and infers:

    R_t = sum_k w_k m_t^(k)
    m_(t+1)^(k) = (1-alpha_k)m_t^(k) + alpha_k u_t,
    u_t = ||xi_t||,  0<alpha_k<1.

No linear state update, superposition principle or fixed linear realization is included in A1-A4. Fixed coefficients and weights are the displayed modal representation being tested. Making weights depend on state/history would change that representation, not establish it.

The separately inspected MICROSCOPIC_LAW.md explicitly calls itself a blueprint, not a closed derivation. Its section 8 says derivation of A1-A5 is unproved; section 9 calls two-mode recursion a target. It assumes a causal lattice/set with geometry and matter, a superposition, propagation/pruning and a gravity-driven threshold. This document is not misrepresented as claiming to have completed the missing microscopic proof. No file chronology, executable import relation, or archive-wide completeness is inferred from these two texts.

## 3. Countermodel to the modal implication

Let the state m be a nonnegative real scalar and the input u=||xi|| be nonnegative. Use a discrete update index t, not a fundamental physical clock. Define only for this countermodel:

    m_(t+1) = F(m_t,u_t) = max(m_t/2,u_t),  m_0>=0.

Inputs may be arbitrary bounded nonnegative sequences. This map is one-dimensional, autonomous with its current input, and stationary. It uses only the declared innovation load. It is sign-invariant in xi and is positively homogeneous jointly in m and xi:

    F(c m,||c xi||) = c F(m,||xi||), c>=0.

The scalar maximum is 1-Lipschitz in either scalar argument, so

    |F(m,u)-F(m',u)| <= |m-m'|/2,
    |F(m,u)-F(m,u')| <= |u-u'|.

Equal future inputs therefore suppress an initial-state difference by at least 2^(-t). A perturbation of u_j alone has influence at most 2^(-(t-1-j)) |u_j-u'_j| on m_t for t>j. Thus this is not merely bounded storage: it uniformly forgets individual past load perturbations. With 0<=u_t<=U, induction gives m_t<=max(m_0,U); with no further input it decays geometrically.

An exact expression, by induction, is

    m_t = max(2^(-t)m_0, max_(0<=j<t) 2^(-(t-1-j))u_j).

The empty-input case t=0 is just m_0. This is discounted maximum memory, rather than a linear convolution. It does store past unresolved load: histories u_0=1 and u_0=0 followed by the same zero next input yield different m_2. No zero-state/no-memory realization of this output can forget that distinction while reading only the same current input. No stronger global minimality theorem is claimed.

These checks satisfy the explicit structural content of A1-A4, including the scalar load choice and scale/sign requirements cited in A4. If 'minimality' or 'admissible' is intended to impose an additional unstated linearity or performance criterion, that criterion must be supplied as an extra premise; it is not inferred from these properties. Differentiability is not among A1-A4; the maximum's nondifferentiable switching boundary therefore is not a violation of the written axioms.

## 4. Exact rejecting control: additivity fails

Start every history at m_0=0. Consider two-step input histories a=(1,0), b=(0,1), and a+b=(1,1). Hand substitution gives:

| Input | m_1 | m_2 |
|---|---:|---:|
| (0,0) | 0 | 0 |
| a=(1,0) | 1 | 1/2 |
| b=(0,1) | 0 | 1 |
| a+b=(1,1) | 1 | 1 |

In particular m_2(a+b)=1 differs from m_2(a)+m_2(b)=3/2.

Every finite family of the displayed modes with fixed alpha_k, fixed w_k and common input-independent initial states has an affine input-output map. Its incremental response after subtracting the zero-input response is additive, regardless of the signs of w_k or equality/distinctness of poles. This follows directly by expanding each linear recurrence and summing; no spectral theorem is needed.

Therefore no such family represents this m_t on all nonnegative input histories. Allowing common nonzero initial modal states cannot repair the discrepancy: subtracting the zero-input response removes their contribution. A source/history-dependent initialization would insert the history into the representation and violate the common initialization comparison.

For contrast, the ordinary one-state law z'=z/2+u/2 with z_0=0 is in the displayed family (alpha=1/2,w=1). Its two-step values for a,b,a+b are 1/4,1/2,3/4 and do add. It has the same state-contraction factor 1/2. Contractivity itself therefore does not select between these additive and nonadditive memories.

These are exact calculations known before freeze, not a numerical campaign, sampled experiment or prospective prediction. We make no claim about approximation by modal filters, nonlinear readouts of modes, or a different encoding/decoder interface; those are distinct classes. The refuted claim is exact representation of the declared retained output by the displayed fixed linear sum.

## 5. What fails downstream, and what remains open

The draft's subsequent mode counting relies on Proposition 1 to restrict the whole admissible class. That reduction is not justified by A1-A4. In addition, A5 supplies no quantitative stability/adaptation criterion, admissible input class or success bounds from which the asserted lower bound of two independent horizons is proved. Our explicit countermodel defeats the prior implication; it does not adjudicate all conceivable interpretations of A5.

Accordingly, this draft does not establish unique minimality by its displayed argument. This is not a proof that two modes are unnecessary under a separately specified task, nor a denial of any empirical usefulness. One may impose a linear-filter model and investigate its minimal realization under precise performance constraints, but that would be a conditional model-class question. Such a restriction must not be passed off as derived from contractive forgetting alone.

The microscopic blueprint does not repair this gap: it openly leaves memory closure and the two-mode structure as derivation targets, and introduces its own physical assumptions. No numerical target matching or fixed-point sweep can supply the absent implication. We do not audit those numerical results here.

## 6. Native admission decision

Even a valid classification of memory laws would not by itself originate an event, a coexisting memory carrier, its address association or an accessible receiver. A1/A4 already assume a retained state driven by innovation; the draft does not derive an initially blind receiver's memory-write interface from earlier lineage/pruning primitives. The blueprint likewise does not supply a completed derivation of that interface.

Disposition: candidate-specific C stop, with a concrete analytical correction to the claimed modal reduction. No B program is admitted to optimize filters without an A mechanism. Re-entry needs an explicit inherited producer for retained memory and binding, together with a corrected exact premise-to-law derivation if this modal route is reused. No replacement recurrence, geometry, threshold, physical clock, measurement register or copying mechanism is adopted.

## 7. Verification scope

The complete two original documents are pinned in source_packet.json and source_lock.json at the inspected baseline. Original historical files remain unchanged. Independent review must challenge admissibility of the countermodel, contraction and influence bounds, additivity obstruction, the exact quantifier and initialization scope, and the distinction between refuting Proposition 1 and refuting every A1-A5 formulation. It must inspect the blueprint's explicit incomplete status.

All displayed reasoning was obtained before freeze. No archived module, scientific enumeration, simulation or historical numerical stack has been executed. Evidence-plumbing tests are not scientific trials. No mathematical novelty claim, universal native no-go, empirical validation, numbered CLOSED/CERTIFIED stage or main merge. Native interaction and broad C3/C4-C6 remain OPEN; time remains pruning/ordered recoverability update.
