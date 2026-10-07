# Post-A12: X2 handover information model and analytical scope

Date: 2026-10-06 (America/Phoenix).
Status: ANALYTICAL SCOPE; NO EXECUTED VERIFICATION OR NEW ACCEPTANCE.
Integrated parent: 963ad536d9f110e7fe51b443e90c1f8afc461096.
Authority: user approval of the proposed six-move A11.X2 information-sufficiency investigation.
Branch: research/uqcf-overlapping-guard-exchange.

This is one theorem-first work item, not A12.6. Analytical design observations preceded this record; it freezes the information model and obligations before formal result publication, not a preregistration of unseen analytical outcomes. No computational search, test, workflow, benchmark or outside-AI request is authorized here.

## 1. Immutable sources and selected class

- A11.X2 proof: ResearchHistory/UQCF-GEM/research/overlapping-guard-exchange/A11_RENEWABLE_SINGLETON_ANCHORS.md at 1cd572d2e90ba3880dc5598d260c14e8a92acc5c; blob f4c295a21a545be746def65acb4fe38c781e3f14. The complete proof was read; Sections 3-5 supply the prepared invariant and six primitive moves.
- A11.X2 historical closeout: A11_RENEWABLE_ANCHOR_CLOSEOUT.md in that directory at the integrated parent; blob 3520650e6d0bd3f7b37b35d55e6e1ae6b00ea3cd. Its original acceptance is history, not an independent verdict on this work.
- A12 R1 proof: A12_CONSOLIDATED_PROOF_AND_AUDIT.md at b2085eb1fdca0bbe754743e6bd74ef6fda6bdbef; blob f670e9a6687aec49b18429655285f937404e1a36.
- Closed A12 record: A12_1_5_CLOSEOUT.md at bbc6e6f68beaf7d2d1641e711b46b55ae0bf62db.
- Approved proposal: POST_A12_THEOREM_FIRST_SYNTHESIS.md at the integrated parent; blob 29f61b20b72665e3972abdae49b5020eb5547c17.

Select target four and a PREPARED carrier only: finite palette P of size k>=4; four distinct labelled slots alpha,beta,i,j; original anchor floors f_alpha=f_beta=1; positive guard floors f_i,f_j<=k-2. All other labelled roots form a fixed residual family R of nonempty supports satisfying their positive original floors.

For an ordered pair (u,v) of distinct labels, E_R(u,v) has anchors {u},{v}, both guards equal P minus {u,v}, and residual family R unchanged. The initial and target prepared states must lie in 3<=tau<=4. They need not be exact four, but any exact-four examples will state that explicitly. The target prescribes the ordered anchor pair and hence the two final guard supports; every residual labelled support is to remain exactly as it started.

This is a subclass/stage of X2, NOT its full arbitrary-endpoint repair. Preparation, changing residual supports, destination-guard installation, reverse normalization and maximum-layer removal are not assumed to factor through the proposed record. The original X2 proof guarantees only the lower bound along its six-move schedule before applying its separate upper conversion to a complete path.

## 2. Proposed retained input

For each H subset P with |H|<=4, let B_R(H)=1 exactly when H meets EVERY residual root. This is the A12 upper-cover predicate applied to R, not an additional physical primitive.

The proposed stored residual signature is the Boolean table

    F_R(U)=1 iff there exists H subset P, |H|<=4,
                       B_R(H)=1, U subset H, and H minus U nonempty,

indexed by every UNORDERED two-label set U. This definition does not assume a sufficiency theorem. The table may require a global read of R to initialize; no internal observer/readout or efficient initialization claim is made.

The policy's allowed input is: P and its supplied order; the four distinguished slot identities and immutable original floors; the current ordered anchor pair; F_R; the prescribed target ordered anchor pair; and finite phase memory. For a handover, memory identifies the changing anchor, its old and new labels, the retained guard order (i,j), and phase 0,...,6. Intermediate supports in the four controlled slots are the ones prescribed by X2's table. Individual residual supports, their incidence syntax table, and unrecorded full-state history are NOT available to the policy after initialization. Validity and immutability of residual floors/supports are domain promises, not data secretly queried by the policy.

F_R is unchanged while R is unchanged. Its state-dependent residual part has at most binomial(k,2) bits; this is not a claim of constant space as the palette grows or a universally shorter encoding than every full state. Immutable carrier/floor metadata is separate. The map must be shown non-injective on a stated carrier before calling it information reduction.

## 3. Prescribed moves and obligations

Use exactly X2's six moves when replacing anchor label p by t outside the current anchor pair, keeping the other anchor label w fixed. With G=P minus {p,w}, G'=P minus {t,w}:

1. Add p at guard j.
2. Delete t at guard j.
3. Add t at the changing anchor.
4. Delete p at the changing anchor.
5. Add p at guard i.
6. Delete t at guard i.

All moves change one native incidence; no new slot or palette label is supplied.

Required proof obligations:

1. Check syntax and original floors at every phase and prove the lower bound directly.
2. Derive EXACT upper-cover conditions throughout the handover. Do not replace direct band legality by X2's later conversion or assume safe start implies safe finish.
3. Determine whether F_R and phase memory decide the prescribed next-move legality and update their own record without consulting R. Do not claim reconstruction of full W/C fields unless separately proved.
4. Determine whether repeatable handovers reach the exact prepared target under a checkable condition on the retained input; give a terminating selection rule or a matched-input/policy-class obstruction. An induced finite graph may describe handover choices, but is not a physical geometry or a new primitive.
5. Distinguish any universally connected sufficient subclass from a conditional reachability statement. Failure of this prescribed macro policy is not failure of arbitrary native repair or of X2.
6. Supply exact symbolic positive, upper-failure, information-loss and domain-boundary checks. Counterexamples to a larger claim must satisfy the actual domain and show impossibility for the precise allowed policy, not merely different successful schedules.
7. Audit all conclusions separately from historical acceptance, and publish limitations and next unresolved obligation.

No blanket certificate-only theorem for every A11 class, every legal move, changing residual families or arbitrary endpoints is in scope. In particular F_R is a derived summary of the FIXED residual family; it is not asserted recoverable from the current global W/C fields alone.

## 4. Completion record and limits

Publish a complete mathematical argument or precise obstruction with an author-side whole-argument audit and immutable readback. If an unresolved finite question actually requires computation, stop short of a computational verdict and publish a separate prospective execution scope before running it. This item does not require a numerical campaign solely to produce a passing-case count.

The initial ledger is: source selection/read complete; input model frozen here; proofs/refutations pending formal publication; no executed evidence; source/reporting audit pending. Later result/status files record actual progress without rewriting this prospective checkpoint.

The closed A12.1-A12.5 result, issue #104, certified v16.54/v16.55 and accepted A11 sources remain unchanged. No physical force, geometry, energy, GR/ADM, dark-matter replacement, physical nonlocality, continuum, observer field or fundamental time is inferred. No outside-AI polling or dispatch, and no efficiency campaign.
