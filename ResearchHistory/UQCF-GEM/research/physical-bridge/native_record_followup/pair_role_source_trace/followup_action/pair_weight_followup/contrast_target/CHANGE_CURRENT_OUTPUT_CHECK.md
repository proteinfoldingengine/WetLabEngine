# A polar change-current can distinguish erased inputs

Author: GPT Work. Date: 2026-11-08 America/Phoenix.
Research parent: 8d827f647916c7335272aadc38f7415f11d89c55.
Status: unreviewed application of the existing conditional polar-lift result; no new native premise or physical promotion.

## Purpose

PR140 constructs a covector from a supplied weight change. Its accepted mathematical scope is preserved. This note checks a separate question: does a contrast in that change-current establish a contrast in the retained output?

It need not. The following normalized, fixed-ledger example obeys the polar-lift assumptions and has distinct nonzero change-currents while the final weights, action, and final action covectors are identical. It is an explicit application of the already known distinction between change and retained record, not a new general obstruction.

## Exact construction

Let U=R^2, B=R, h(s,t)=st, V=Bil(U x U,R). Fix the two test pairs (e_p,e_p),(e_u,e_u), with evaluation E(K)=(K_pp,K_uu). Let the fixed actual residual be delta(x,y)=x_p y_p, so E(delta)=(1,0).

For weights w=(w_p,w_u)>=0, the declared quadratic action is

    I_w(K)=w_p K_pp^2+w_u K_uu^2,
    I_w(delta)=w_p,
    (R_w delta)(K)=w_p K_pp.

Choose normalized input weights

    w_plus =(3/4,1/4),
    w_minus=(1/4,3/4).

Compare both to the same final weights w_out=(1,0) on this FIXED ledger. This is a supplied weight-only comparison, not a new rule for physical pair weights or a pair-birth/death claim. The second pair stays on the declared ledger with zero final weight.

The arithmetic w_out=(w_p+w_u,0) is the zero-extended sum map associated with merging u into p. P1 already fixes that sum for correctly typed native grades. Here using it on product-pair weights is explicitly SUPPLIED; no source-grade/pair-weight identification is earned by the example.

The weight directions are

    mu_plus =(1/4,-1/4),
    mu_minus=(3/4,-3/4).

The line segments w_s+t mu_s, 0<=t<=1, are nonnegative. Connection, residual, ledger, arguments and branch form stay fixed. Thus this is within the reviewed weight-only slice.

By the reviewed formula J_s=E*D_mu_s G E delta,

    J_plus(K) =(1/4)K_pp,
    J_minus(K)=(3/4)K_pp.

Both currents are nonzero, and their difference is the nonzero covector

    (J_plus-J_minus)(K)=-(1/2)K_pp.

It acts on the fixed test variation K=delta with value -1/2. There is no adaptive choice of test vector or output here.

Nevertheless, at the output,

    I_out(delta)=1 for BOTH preparations,
    (R_out delta)(K)=K_pp for BOTH preparations,
    w_out is identical for BOTH preparations.

Every function of that final weight record agrees between the preparations. The source-dependent change-current is not a function of that final record alone: it still uses the differing input weights through mu.

The baseline forms for both preparations are positive on both declared evaluations. Their null space consists of maps with K_pp=K_uu=0, which J_s annihilates. Therefore this example does NOT exploit the zero-baseline-weight quotient failure from PR140. The final zero weight is permitted. The obstruction here is the distinction between a comparison current and an output, not failure to define the covector.

No claim is made that these two input weights are initially indistinguishable to an owner. Indeed their initial action values are 3/4 and 1/4. That is exactly why nonzero contrast in the CHANGE cannot be promoted to acquisition. A separate archive of J_s could retain a distinction, but its production, retention and access would be an additional operation.

## Positive implication with the correct premise

Write a_X^s for the actual initial response of the claimed observable and a_Y^s for its actual final response, for a fixed owner/effect identification and source preparation s. Set j^s=a_Y^s-a_X^s. Then, purely algebraically,

    a_Y^+ - a_Y^- = (a_X^+ - a_X^-) + (j^+ - j^-).                 (1)

Consequently, if the INITIAL response is equal, a nonzero contrast in its change is precisely a nonzero FINAL response contrast. With lambda indexing all actually allowed realizations, equality initially plus a common lower bound j_lambda^+-j_lambda^->=epsilon>0 gives the same final lower bound for every lambda.

Equality of one initial response is enough for that one response claim. Acquisition by an initially uninformed receiver requires equality on its entire actual initial interface, not just one scalar. The claimed action must also genuinely be a response available to that owner; an action functional or covector does not become an observable merely by being computable.

Equation (1) already underlies CONTRAST_TARGET.md's four-endpoint calculation. This addendum makes its application to the newly reviewed polar current explicit. It changes no formula or acceptance. In the example, initial contrast +1/2 and change contrast -1/2 cancel, leaving final contrast zero.

For the earlier positive membership slice, c_X(u)=0 can give initial equality for the formal extensive contrast delta e_u when all other inputs and costs are fixed. For normalized delta(e_u-e_v), the v term must also be checked. A new proof must establish the initial/output correspondence and actual allowed event relation, rather than borrowing a nonzero action-change coefficient as a receiver result.

## Inspected sources and consequences for work

- Complete PR140 DERIVATION.md sections 3–7 and REVIEW_DISPOSITION.md at 159ca4afd3d4a06f00aab83cfdb52e10ad0abc9c: fixed-ledger setup, canonical polarization, quotient criterion and explicit non-physical scope. This note does not rerun that independent review or adopt the rejected raw native-status field.
- CONTRAST_TARGET.md at the research parent: equations (1)–(4), supplied incidence/action semantics and normalized compensation.
- pruning_current_bridge/RESULT.md sections 5–7 at the research parent: prior exact distinction between preserved amount, lost source-location information, comparison current and actual retained access. Credit remains with that earlier result.
- V1691.1 and V1694.4 originals at the research parent: the relevant action and retained-pair dual definitions. No historical code lineage is inferred.

The practical consequence is specific. In the P1 -> incidence -> action proposal, producing nonzero mu or J is not yet the final scientific target. The producing operation must also identify an actual retained effect or retained current record, with a source contrast there. This is the existing frontier applied to the new lift, not an added requirement for a unique microscopic map, a particular action, or a sharp measurement.

Do not extend the polar-lift branch with more response formulas merely because the lift is available. It is supporting mathematics ready for use once an inherited event supplies its inputs and a retained interpretation. The next constructive source demand remains the native event-to-support/weight operation and owner-held output. Other direct owner-effect routes remain eligible without any action current.

Premise status: historical action formula and reviewed lift are conditional mathematical infrastructure; weights, pair-grade matching, endpoint comparison and residual in this example are SUPPLIED. Actual occurrence is ACCEPTED INPUT, not a producer of those data.
Native premise removed: none.
W_R/W_E/Bell: NOT SCORED for this untyped operational example.
Scientific importance: a concrete scope check preventing change-current contrast from being mistaken for retained acquisition; not a breakthrough.
No historical simulation, new numerical campaign, Gemini rerun, PR merge or held-PR change.
