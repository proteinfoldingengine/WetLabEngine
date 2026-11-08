# Contrast-specific support construction: what must be fixed, and what need not be

Author: GPT Work. Date: 2026-11-07 America/Phoenix.
Research parent: 70dd277e0b014b2804992550fbfc5edaf5bcb609.
Status: unreviewed working calculation and bounded original-archive inspection.
Native owner-held action: NOT_DERIVED. No numbered stage or physical promotion.

## 1. Response to Dot and the positive target

Dot's PR111 comment 6716989021 correctly removes a unique pair representative or total pair map as a universal requirement. I inspected its numbered steps 1–3: subtracting two proposed linear weights gives its annihilator criterion; pulling back the outgoing support row gives its increment coefficient; the singleton and full-fiber examples give e_u and zero, respectively. These statements hold with their stated supplied weight/support meanings.

There is a further distinction relevant to Aaron's requested unavoidable consequence. A unique numerical action increment is sufficient but is not necessary for a fixed owner-owned observable to change in every allowed realization. Different permitted implementations can produce different nonzero contrasts. A positive uniform lower bound would be stronger still. None of these claims may change the identity of the owner or observable after choosing the implementation.

Accordingly, do not make full cochain descent, a unique q, identical action values, or equality of the two procedures in INCIDENCE_UPDATE_CHECK.md mandatory for every possible native bridge. Those are scoped checks for particular proposals. The immediate constructive target is the least support information that forces the specified contrast, provided the action/observable is independently bound to the retained owner.

## 2. Exact restricted calculation

Use the already established finite P1 pushforward P along r:X -> Y. For this calculation only, let lambda range over a NONEMPTY set L of proposed event-compatible matches for one fixed pair-class observable. The membership of L must ultimately come from the native event relation; it is SUPPLIED here. All matches must refer to the same fixed claimed output.

For match lambda, supply unsigned source-address incidence rows c_X^lambda and c_Y^lambda and the meaning

    w_X^lambda(z) = c_X^lambda z,
    w_Y^lambda(Pz) = c_Y^lambda Pz.

This is the support-grade proposal of ASSESSMENT.md, not a recovered historical weight law. Source-node/address identification, unsigned support extraction, pair-class matching and weight-as-grade remain SUPPLIED.

For the weight-only action slice, let k_X^lambda,k_Y^lambda be nonnegative squared residual costs, independent of z on the compared preparations. This is a restriction of the working model, not a property inferred from V1696.6. Define

    J_lambda(z) = k_Y^lambda c_Y^lambda Pz
                   - k_X^lambda c_X^lambda z.

Subtracting at z_plus and z_minus gives the full claim:

    J_lambda(z_plus)-J_lambda(z_minus)
      = (k_Y^lambda c_Y^lambda P-k_X^lambda c_X^lambda) Delta z.       (1)

Consequently, for the FIXED proposed observable and preparation contrast:

- exact realization independence requires all values in (1) to be equal;
- an unavoidable change requires every value in (1) to be nonzero;
- a uniform separation epsilon>0 requires their absolute values to be at least epsilon.

For infinite L, pointwise nonzero values do not imply a positive uniform lower bound. These are different claims. This elementary distinction does not add a mechanism.

### One varying extensive source coordinate

For formal extensive grades with Delta z = delta e_u, delta>0, (1) reduces to

    delta [k_Y^lambda c_Y^lambda(r(u))-k_X^lambda c_X^lambda(u)].      (2)

Thus one does not need the entire incidence matrix to settle this restricted contrast.

If the inherited event were to supply, for EVERY allowed match,

    c_Y^lambda(r(u))=1, c_X^lambda(u)=0,
    k_Y^lambda >= k_min > 0,                                      (3)

then (2) would be at least delta k_min. k_X can vary and the rest of both support rows can vary. This would yield a robust source-side action contrast without a unique pair representative. Condition (3) is a proposed sufficient construction target, NOT a native finding, NOT necessary in the general model, and NOT an independently justified receiver effect.

For the still narrower equal-cost slice k_X^lambda=k_Y^lambda=k>0, the exact four possibilities are:

| Outgoing membership at r(u) | Incoming membership at u | Action contrast |
| --- | --- | --- |
| 0 | 0 | 0 |
| 0 | 1 | -k delta |
| 1 | 0 | +k delta |
| 1 | 1 | 0 |

The proof is substitution in (2). In this binary, equal-cost slice, an unavoidable nonzero contrast is equivalent to unequal memberships for every allowed match. A uniformly positive contrast is equivalent to the ordered membership pair (1,0) for every match. Allowing both off-diagonal cases preserves nonzero magnitude but not sign. Averaging such alternatives could cancel; this statement is about each allowed implementation, not an ensemble whose mixture is automatically included. If mixtures are admitted, they must also be tested in the actual admissible class.

This is a small support-level characterization inside supplied semantics, not a minimal physical-postulate theorem. k=0 produces no weight-only action contrast. If the residual depends on preparation, (1) does not apply; use the actual four endpoint action values.

### Normalized preparations

Delta z=delta e_u is a formal extensive-grade contrast, not a claim that normalized quantum preparations can vary only one population. For a normalized redistribution Delta z=delta(e_u-e_v), the correct coefficient is

    delta {k_Y^lambda[c_Y^lambda(r(u))-c_Y^lambda(r(v))]
           -k_X^lambda[c_X^lambda(u)-c_X^lambda(v)]}.               (4)

The compensating coordinate cannot be dropped. Condition (3) alone does not guarantee (4) is nonzero. Preparability, the fixed output identity and actual owner access require their own justification.

Nor is a pair-weight or action contrast automatically V_oplus* current, probability, or a bounded physical effect. No such identification is made here.

## 3. What the original V1696.6 archive can answer

I recovered the original Library ZIP, not a clean-room simulation:

    V1696_6_hardened_pair_class_signature_python_test_package.zip
    bytes: 32626
    SHA-256: 783d2482470e2a80cf699965561bf5c4eedfba8eb21d162651b3d8f10ec19d99

The archive has nine members: six CSVs, two JSONs and one Markdown report. No executable or notebook is among those nine members. This is a scoped archive fact, not a claim that no implementation exists elsewhere.

All CSV rows and all JSON/Markdown contents were inspected programmatically. The audit contains 210 rows with columns:

    seed, ladder_step, coarse_cell, role, JD_GD_len,
    support_nonzero, order_nonzero, compatible_family

It records support cardinalities 4,5,6,7 with frequencies 42,105,42,21. It does not record the source addresses in those supports. The 210 residual rows all report coarse_class_defined=True. There are 1,260 null rows; the support-shuffle comparison reports 179 wins and 31 losses out of 210. The archived run_manifest.json is byte-identical to SUMMARY.json, not a command/procedure manifest.

Those results are useful historical diagnostics. They do not recover the cochain entries, allowed match relation L, the action's source-grade pairing, or any of the membership pairs in (2). Nonzero-support counts and class distances cannot answer that address-specific construction question.

The full V1696.7 postmortem was also read and preserved as a transcription. It keeps the pair-class object and support/order components, but explicitly reports unresolved D1/D2 sensitivity and unrestored stationarity/action reduction. Its reported 0.0 action-reduction rate is not a statement that all proposed pair costs k vanish, and does not determine the derivative or event contrast in (1). No cause of its numerical outcome is inferred here.

The historical tests are not rerun. No coefficients or thresholds are fitted. V1696.2's rejection of vector transport remains in force; these working support matches do not resurrect it.

## 4. Concrete handoff

The next useful source answer can be much narrower than a full transport map:

1. Exhibit the inherited event operation defining which pair-class actions are allowed, including any undefined outcomes relevant to the claimed universal guarantee.
2. From that operation, determine the incoming membership of u and outgoing membership of r(u) for the fixed claimed action. For normalized contrasts, also determine the compensating-coordinate contribution.
3. Derive the grade/action pairing and the relevant nonzero cost or full endpoint response. Do not identify a signature-distance weight with an action weight.
4. Bind that very action to an effect available to the same retained owner. A successful source-side coefficient is not that access relation.

If the source defines only compatible classes, a class-level proof or robust bound may suffice. A unique microscopic representative is not demanded. But a representative chosen because it gives (1,0), or an assumed residual lower bound, does not answer this handoff.

Native premises: existing P1 structure within its accepted scope; occurrence is ACCEPTED INPUT.
Still supplied: every pair/grade/action/operational identification used in section 2.
New native premise removed: none.
W_R/W_E/Bell: NOT SCORED for this untyped operational proposal.
Accessible receiver consequence forced: not established.
Scientific status: focused construction target and historical evidence; not a breakthrough or Gemini-reviewed result.

This is working discussion, not a material native-bridge checkpoint. Preserve the established infrastructure and held PRs. Do not launch a signature-comparison campaign or another arbitrary-weight implementation from this note.

