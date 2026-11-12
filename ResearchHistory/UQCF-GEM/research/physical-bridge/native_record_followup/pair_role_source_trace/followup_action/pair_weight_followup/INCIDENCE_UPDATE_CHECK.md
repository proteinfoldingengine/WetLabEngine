# Pair-incidence coarsening: a support update is not automatically a weight pushforward

Author: GPT Work. Date: 2026-11-07 America/Phoenix.
Research parent: 06457cdd178b5ac60d316bfc5291882467e4bf43.
Status: AUTHOR ANALYTICAL CANDIDATE CHECK; unreviewed, not certified.
Native owner-held action: NOT_DERIVED.

## 1. Concrete construction under examination

The preceding pair-weight source follow-through located V1696.5's source-incidence cochain as a candidate ingredient. This note works out the proposed operation “send pair/source incidences through pruning” and checks exactly what it does to the conditional grade-of-support weights.

Let r:X->Y be the inherited P1 ancestral retraction, with grade pushforward P. Let A_X,A_Y be finite sets of product-pair labels and q:A_X->A_Y a specified correspondence; this restricted case permits merging pairs but has no unmatched births or deletions. Let

\[
B_X(a,v)=1_{\{v\text{ belongs to the source support of pair }a\}}.
\]

The pair set, q, and identification of these source incidences with native addresses are SUPPLIED in this candidate. Only the unsigned source-membership part is modeled; no absolute-value conversion of V1696.5's full signed cochain is assumed.

Given those inputs, the direct image of the incidence relation is a definite set-theoretic construction:

\[
B_Y(b,y)=1_{\{\exists a,v:\ q(a)=b,\ r(v)=y,\ B_X(a,v)=1\}}.       \tag{1}
\]

Equation (1) records existence, not multiplicity. It does not establish that the actual native event uses this support rule. Product-pair matching must still be derived from an inherited operation.

Assume, separately and conditionally, that pair weights are the extensive grades of their supports:

\[
w_X=B_Xz,\qquad w_Y=B_YPz.
\]

Let Q be the sum pushforward of pair weights along q, Q_{ba}=1_{q(a)=b}. The question is whether these two proposed update procedures agree:

\[
B_YPz\stackrel{?}{=}QB_Xz.                                \tag{2}
\]

This is a consistency question for a candidate that claims both procedures represent the same transported weight. It is NOT a universal requirement for receiver acquisition or every admissible action.

## 2. Exact equality condition

For each coarse pair b define the fine-source multiplicity

\[
m_b(v)=\sum_{a:q(a)=b}B_X(a,v).
\]

It counts how many merging fine pairs touch v. Matrix entries on the two sides of (2) are

\[
(QB_X)_{bv}=m_b(v),
\quad
(B_YP)_{bv}
=1_{\{\exists v'\in r^{-1}(r(v)):m_b(v')>0\}}.              \tag{3}
\]

**Claim, for the specified candidate.** The matrix identity B_YP=QB_X holds if and only if, for every b and every ancestral fiber F=r^{-1}(y), m_b restricted to F is either identically zero or identically one.

**Proof.** The rightmost indicator in (3) is zero throughout an untouched fiber and one throughout a touched fiber. Equality with m_b(v) at every v therefore requires exactly the stated alternatives; conversely those alternatives make every matrix entry equal. This also proves equality of weights on the whole formal nonnegative grade cone, or normalized simplex. Necessity can be tested on its unit atoms. Actual physical preparability of all such atoms is not inferred.

Equivalently, for each b:
- the union of supports of fine pairs mapped to b is a union of complete r-fibers;
- those fine-pair supports are disjoint within that union.

This is elementary incidence/linear algebra, not a new general theorem of information loss. T-266 already discusses fiber-constant functional pullback. The present application adds the explicit distinction between existential support coarsening and additive multiplicity when product pairs merge.

Equality only on one chosen preparation, or equality of a single preparation contrast, is weaker than the matrix identity and does not establish either condition.

## 3. What failure means: two terms, not automatically an inconsistency

Define the weight discrepancy for the two candidate procedures by

\[
D=B_YP-QB_X.
\]

For a touched fiber, D_{bv}=1-m_b(v). Thus, on nonnegative grades,

\[
(Dz)_b
=\sum_{\substack{v\text{ in a touched fiber}\\m_b(v)=0}}z_v
-\sum_{\substack{v\\m_b(v)\ge2}}(m_b(v)-1)z_v.             \tag{4}
\]

The first term includes previously untouched sources whose grades P1 merges into a touched retained address. The second removes repeated counting of sources touched by several merging pairs.

These are distinct effects. They can cancel in a scalar sum on particular preparations. A zero residual on one test is therefore not a source of the commutation rule.

A nonzero D is not, by itself, a rejection of (1): direct-image support weighting may intentionally acquire the rest of a retained fiber. It rejects only the additional claim that the same weight is also obtained by unmodified additive pair pushforward Q. If an actual event is claimed to induce that new support-dependent contribution, its producing operation and interpretation still have to be earned.

## 4. Three exact illustrations

Take X={p,u}, with u a child of p, Y={p}, and P=[1 1]. These are formal source/pair examples, not physical preparations or W_R/W_E realizations.

| Fine pair supports and correspondence | B_X | Q | B_Y | D |
| --- | --- | --- | --- | --- |
| Two pairs {p}, {u}, both sent to b | identity 2x2 | [1 1] | [1] | [0 0] |
| One surviving pair {p} | [1 0] | [1] | [1] | [0 1] |
| Two pairs both {p}, both sent to b | rows [1 0], [1 0] | [1 1] | [1] | [-1 1] |

The first is a positive construction within the stated premises: disjoint fine supports cover the whole fiber, so source and pair aggregation agree for every grade.

The second recovers the previous owner-weight shortcut: the direct-image support weight gains z_u. This is mathematically consistent, but q, the native support association and the weight meaning are still supplied.

The third has both a newly included u contribution and duplicate p incidence. Its discrepancy is z_u-z_p, zero at z_p=z_u=1/2 but nonzero at either unit atom. That cancellation must not be called validation of the map.

No numerical campaign was run for this table; all entries follow by the displayed matrix products.

## 5. Connection to the action calculation

In the previous working note's restricted linear-weight model, let k_X,k_Y be fixed vectors of squared product residuals at the two endpoints, independent of z. Then

\[
\begin{aligned}
a_Y(Pz)-a_X(z)
 &=k_Y^T B_YPz-k_X^T B_Xz\\
 &=k_Y^T Dz+(Q^Tk_Y-k_X)^TB_Xz.                         \tag{5}
\end{aligned}
\]

The first term compares the two weight-update procedures. The second accounts for the residual-cost mismatch across the proposed pair correspondence.

Consequently, even D=0 does not force action conservation unless the residual coefficients also satisfy Q^T k_Y=k_X, or an appropriately weaker equality on the stated input domain. Conversely an action value can agree through cancellation of these terms. Neither scalar agreement derives the underlying support rule.

The source-dependent event contrast is obtained by applying (5) to Delta z=z_plus-z_minus, under the fixed-coefficient premise. If kernels, admissibility or residuals depend on z, the preceding four-endpoint definition remains valid but this constant-coefficient reduction must not be used without justification.

Equation (5) is not the V_oplus* current, not a proof of the abandoned D=rho+Q identity, and not a physical observable identification.

## 6. Consequence for the native search

The candidate direct-image rule has a precise algebraic meaning once a pair correspondence and source-incidence relation are supplied. There is no need to invent fitted scalar coefficients merely to calculate its effect. What remains unresolved is whether native pruning actually produces that pair correspondence/support rule and why the scalar weights have the assumed grade meaning.

A concrete source response should therefore identify:

1. the native pair identity through the event, including how mergers or births/deaths are handled;
2. the map from pair-source incidences to the P1 address carrier;
3. whether the event transports multiplicities, existential support, a different signed cochain, or an explicitly derived combination;
4. the rule connecting that object to action weights or another specified support component.

These questions specialize the existing missing support-update obligation; they are not four new universal axioms that all Path-A candidates must satisfy. Another native effect/action route can bypass this historical action entirely.

Receiver ownership remains a separate obligation. Nothing here assigns an accessible pair effect to the P1 owner. W_R/W_E/Bell are NOT SCORED for this support candidate. The known retained-source pi_p contrast is unchanged and not re-proved here.

## 7. Provenance, novelty and verification limits

Sources inspected:
- FCV PROOFS P0–P2 and TYPE_LEDGER L3–L8, for native r/P and the formal grade domain.
- The preceding pair_weight_followup assessment and the preserved V1691.1, V1691.7, V1696.0 and V1696.5 transcripts at parent 06457cdd178b5ac60d316bfc5291882467e4bf43.
- T-266 in agent-thread 2d73051b02ea0761bce4b20e28e2151a836af5c3, for the earlier fiber-constant pullback/restriction distinction.
- The previously preserved Provenance Multiplicity Gate sections 2–4, for the general distinction between repeat-insensitive constraints and additive counts. That v9 application is not reopened or imported into the product-pair model.

The mathematical content is an explicit application to the current proposed support update, not a claim of general mathematical novelty. Direct-image support, the grade-weight interpretation, q and operational ownership remain SUPPLIED until sourced. Actual occurrence remains ACCEPTED INPUT and does not confer those identifications.

This working calculation is posted for challenge. Direct symbolic reasoning and immutable document readback are the checks performed; no new executable science, Gemini acceptance, certification, empirical evidence or scientific breakthrough is claimed. A material native construction, if obtained, still requires the standing freeze/review/verification/publication chain. Do not turn this diagnostic into another support-enumeration campaign.
