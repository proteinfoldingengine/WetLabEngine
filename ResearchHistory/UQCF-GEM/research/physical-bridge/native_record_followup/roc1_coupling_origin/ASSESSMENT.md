# ROC-1: composition does not force a nonzero retained-action coupling

Date: 2026-11-09 America/Phoenix. Author: GPT Work.
Research parent: bd661947ebe97fd2ca356ec0b62e1103f63fd665.
Thread inspected through T-401 at e9dbba6059ed9b823b0a01672d8077327d657e0d.

**Status: source-specific analytical challenge, not independently reviewed. Native delivery NOT_DERIVED.** This is not a new physical postulate, scientific stage, numerical campaign, or revision of an accepted conditional model. Historical novelty is unassessed.

## The candidate and its strongest positive reading

The existing RSL-1 law writes a source-associated action increment into a declared retained edge/local state. ROC-1 then explicitly defines an action of that state on future edge conductance and capacity. Unlike a source diagnostic alone, the composed definitions contain an operator update:

    rho' = rho + P_G(ell)
    r = P_G(rho/c_ref)
    m = exp(-r)
    a_eff = m * a,  c_eff = m * c

Multiplication is componentwise. Here rho is retained action, not a quantum density operator. T-328-dot already checked a supplied one-edge example with different retained increments and a potential-probe response under this explicit exponential definition. That conditional calculation is preserved and is not a new finding here.

The bounded question in this pass is whether ROC-1's stated necessity argument forces any such nonzero operator response. It is upstream of interpreting an edge or probe as the current P1 owner. Success would require a genuinely forced update, not merely the definition of one that works.

## Original source and premise tags

The complete extracted source texts are preserved in transcripts/, with identities and read coverage in SOURCE_IDENTITIES.json. They are transcriptions, not certified original-byte downloads.

1. ROC1_specification.json, derived_coupling and composition: the displayed exponential update is an **INHERITED historical definition**, conditional on that architecture. Its physical enactment is not inherited by recovery of the text.
2. ROC1_specification.json, why_this_is_forced_minimally: the stated scalar argument uses additive burden, multiplicative composition, identity at zero and positivity. The report REPORT(274).md states the same implication. These are **INHERITED statements of the proposed argument**, not accepted proof of its conclusion.
3. RAG0_specification.json, types, primitive_observables_allowed and allowed_operations: edge capacities/conductances and an observer probe with a locked response map are allowed inputs. This is **INHERITED evidence about the declared grammar**. Their origin as this receiver's available interface remains **SUPPLIED**.
4. ARC1_REPORT.md: the repair rule is a constrained minimization over capacities. It is an **INHERITED historical definition**; the original empirical counts are not rechecked or recertified here.
5. Actual atemporal event occurrence is **ACCEPTED INPUT**. Event-to-RSL increment correspondence, P_G, physical edge/owner correspondence and owned probe access remain **SUPPLIED**.

## Exact counterexample to the forcing inference

For every nonnegative scalar burden r, set

    m_id(r) = 1.

Then, for all r,s >= 0,

    m_id(r+s) = 1 = m_id(r) m_id(s),
    m_id(0) = 1,
    m_id(r) > 0.

It is also continuous, nonincreasing and bounded by one. Thus granting those additional regularity and attenuation requirements does not remove it.

Applied pointwise, it gives a_eff = a and c_eff = c. Coefficients remain positive, their ratio is unchanged, and no future target, history identifier, coordinate primitive or force is inserted. The unchanged coefficients themselves are allowed RAG-0 primitive expressions. This observation is not an enumeration or completeness theorem for that grammar.

Different retained action states can therefore persist under RSL-1 while producing exactly the same future operator through m_id, when the graph, future source demand, base coefficients, constitutive law and probe are held fixed. This concerns dependence on retained action. It does not claim that current-source variations cannot affect flow by other routes, or that no information exists elsewhere.

**Logical scope:** m_id satisfies the listed necessity conditions. It does NOT satisfy the additional defining equation m=exp(-r) for r>0. The challenge is to the claim that the former force the latter. It does not dispute calculations made after the exponential law is stipulated. If “coupling” is defined to require nonconstant dependence, that adds precisely the nontriviality assumption absent from the displayed functional-equation premises; the word alone is not its derivation.

## What composition does fix in a precise scalar class

For clarity, restrict to the explicitly stated class

    m : [0,infinity) -> (0,1],
    m(0)=1,
    m(r+s)=m(r)m(s).

This attenuation class is stronger than nonnegative positivity alone. It is an analytical scope restriction, not a newly derived native law.

Let g(r)=-log m(r). Then g is additive and nonnegative. For s>=r, g(s)=g(r)+g(s-r)>=g(r), so g is monotone. With lambda=g(1)>=0, additivity gives g(q)=lambda*q on nonnegative rationals. Rational lower and upper bounds on any real r, together with monotonicity, give g(r)=lambda*r. Hence

    m(r)=exp(-lambda*r),  lambda>=0.

No continuity hypothesis is needed within this strictly positive attenuation class. The zero-response member lambda=0 remains. A finite positive change of burden units can normalize lambda>0 to one; it cannot convert lambda=0 into a nonzero response.

Within this class, excluding m_id is equivalent to requiring m(r0)<1 at some r0>0, and then every pair of distinct scalar burdens has distinct multipliers. This is a statement about the conditional scalar family. It is NOT a proposed minimal physical postulate for receiver delivery: it neither creates the event-to-burden map nor earns an owner or a probe. Introducing nontriviality solely to obtain the desired response would supply that part of the mechanism.

## ARC-1 does not automatically remove this counterexample

ARC-1 starts from a baseline multiplier m0 and constrains m0_e <= m_e <= 1 while requiring some flow f with d f=b and |f_e|<=c_e m_e. Its objective minimizes added capacity sum_e c_e(m_e-m0_e).

For m0=m_id=1, the bounds force m_e=1 on every edge. Whenever the unmodified capacities admit the specified common future demand, the repair is feasible with zero cost and no retained-action-dependent change. If those capacities do not admit the demand, this instance is infeasible; it is not a counterexample on that domain. No replacement repair law is introduced.

This is a direct consequence of the stated bounds. It does not challenge the reported numerical results under their supplied exponential baseline, assert their uniqueness, or claim feasibility of a separate nonlinear constitutive solve from the capacity inequalities alone.

## Relation to the native ownership target

This inspection finds an explicit conditional update and a gap in its proposed necessity argument. It does not find a new inherited update that binds the current P1 event to an available effect of r(u).

There are distinct obligations:

- A nontrivial retained-action response must be justified rather than obtained by silently excluding the identity response.
- The actual event must generate the relevant difference in the retained burden.
- The affected edge/action and available response must belong to the independently identified retained owner.

ROC-1's componentwise definition names which model coefficient is changed once adopted. The scalar composition equation does not independently derive physical ownership or accessibility. The fixed probe map in RAG-0 is an allowed input, not a construction from P1 provenance.

No W_R/W_E/Bell score is assigned: no mapping from this edge-action architecture to those specified output interfaces has been earned. Agreement across realizations is not used to reject a possible retained-source effect. The existing 1/5 retained-source benchmark and its unresolved ownership/access boundary remain unchanged.

## Disposition

Preserve the conditional exponential model and T-328-dot's illustration. Do not promote ROC-1's displayed necessity argument into proof of native operator activity. This source-specific challenge requires a missing independent nontriviality premise or a corrected conditional statement; it does not call for another coupling, parameter, normalization or numerical sweep.

No historical scientific program was executed, no empirical result was replayed, no Gemini verdict was obtained, and no held PR or main branch is changed. Publication checks verify the source transcriptions and additive packet, not physical truth. This is a directly inspectable analytical challenge; no independent acceptance is claimed.
