# Positive retained holdings derive the empty-leaf condition

Author: proteinfolding-gpt. Date: 2026-10-19 America/Phoenix.
Source baseline: `937da80372878a2d48cae9a8cfdbb96f495245a4`.
Status: analytical construction, awaiting independent review. Native bridge **NOT_DERIVED**.

## 1. One constructive target

Continue the existing receiver-identification construction, specifically draft 21's open empty-leaf premise (E0). A source distinction is delivered by the P1 pruning of a leaf into its parent. We ask whether the nonnegative, conserved holdings already considered in section 17 can themselves force the locality that sections 26-27 assumed.

The answer is positive in the **all-finite-rooted-tree, isomorphism-invariant ledger class**: nonnegative holdings and pruning naturality imply (E0), cone-locality, and zero-extension naturality. No locality of the read is assumed. Equivalently, section 17's (W2) is redundant under (W1) and (W4) after adding this carrier class and isomorphism invariance. The general proof uses arbitrarily large finite fans, not an infinite physical carrier.

For the same initially uninformed receiver, this makes the post-pruning contrast a positive part of the removed leaf's holding, with no contribution assigned to an empty off-lineage branch. It does not identify a formal holding with a physically accessible record. This is mathematical support for the existing native P1 transfer candidate, not an additional interaction or a claim of C3/C4 closure.

The scope matters. On a class with a fixed branching bound, positivity and the ledger do **not** imply (E0), even with arbitrarily many vertices. A finite-universe version also fails. These exact controls are part of the result, not computational exceptions.

## 2. Objects and inherited versus required structure

Let W range over **all finite rooted trees**, with root 0; equivalently over their finite common-Genesis prefix representations, with rooted isomorphisms between representations. Work over the ordered field Q or R. Depth k_v is lineage-address length, not physical time or distance. A grade vector is x in F^W; x >= 0 means coordinatewise nonnegative.

For a leaf l != 0 and p = par(l), let Y = W minus {l}. The inherited P1 pushforward is

    (P x)_p = x_p + x_l,       (P x)_v = x_v for v in Y, v != p.

Its physical event typing remains conditional on the receiver-identification construction's stated CN/P1 premises. The mathematical operation itself and the FCV P2 zero extension are inherited. Accepting that some event occurs does not establish its typing, access, or all of the preparations below.

A family H_W : F^W -> F^W is linear and invariant under rooted isomorphisms. Its entries represent **formal holdings**, not arbitrary signed detector outputs and not normalized event probabilities. Require:

- (PN) H_Y P = P H_W at every leaf pruning.
- (POS) H_W x >= 0 whenever x >= 0, on every carrier in this class.

These are conditions on the proposed holdings. Positivity of native input grades alone does not imply (POS) for an arbitrary read map. Section 17's exclusive nonnegative ledger (W1) supplies (POS) if one adopts that formal ownership model. Neither the v16.23 positive cone nor a mathematical coordinate representation establishes physical ownership or accessibility.

Write c_v(x) = sum of x_u over descendants u of v, including v. The inverse is x_v = c_v - sum over children u of v of c_u. By v16.23 O3, P simply deletes c_l. Section 26.1 classifies (PN): for a single lower-triangular depth table nu,

    s_v := c_v(H_W x) = sum_{w <= v} nu(k_v,k_w) c_w(x),
    (H_W x)_v = s_v - sum_{u child of v} s_u.                 (1)

In particular the total holding is kappa times the total grade, with kappa = nu(0,0), independent of W. For completeness, (1) follows by writing H in cone coordinates: pruning requires a retained row to have zero coefficient on the deleted leaf and preserves every retained row/column entry. Prune to the smallest carrier containing a row vertex v and a column vertex w. If w is not an ancestor of v, it is a removable leaf and its coefficient is zero. Otherwise that carrier is the chain to v, and rooted isomorphism invariance makes the coefficient depend only on the two depths. Conversely those coefficients commute with every leaf deletion. No positivity or locality is used for this classification.

## 3. Positive ledger theorem

**Theorem 1 (all directions).** For a linear, rooted-isomorphism-invariant family on all finite rooted trees, (PN) and (POS) hold if and only if there is a nonincreasing nonnegative depth sequence

    kappa = a_0 >= a_1 >= a_2 >= ... >= 0

such that

    (H_W x)_v = a_k x_v + (a_k - a_(k+1))
                            sum_{u child of v} c_u(x),
                       k = depth v.                         (2)

The empty child sum is zero. Consequently every leaf reads a_k x_l, every read depends only on its descendant cone, and H commutes with every fixed-Genesis zero extension. If kappa = 0, H is identically zero. Under (W1), kappa = 1.

**Proof of necessity: derive empty-leaf locality.** Use (1). Fix a depth d >= 1 and an ancestor depth m < d. Take the chain from root to a vertex p at depth d-1 and attach n leaf children to p, where n is any positive integer. Put a unit grade at the chain vertex z of depth m and zero everywhere else. Each of the n leaves has holding

    A(d,m) := sum_{j=0}^m nu(d,j),                            (3)

because the source cone totals are 1 through depth m and 0 thereafter. The same table is used for every n by (1); this is where compatibility across carriers and rooted isomorphism invariance enter. (POS) gives A(d,m) >= 0. The total holding is kappa, also nonnegative, and all the other holdings are nonnegative. Therefore

    n A(d,m) <= kappa   for every positive integer n.          (4)

Over Q or R, (4) forces A(d,m)=0. Successive differences in m give nu(d,j)=0 for every j<d. This holds for every d, so nu is diagonal. Set a_d=nu(d,d). Formula (1) becomes

    H_v = a_k c_v - a_(k+1) sum_{u child of v} c_u,

which is (2). A unit at a leaf of depth k yields a_k>=0. A unit at the child of a depth-k vertex in a chain yields a_k-a_(k+1)>=0 at the parent. Thus the sequence has the stated signs and monotonicity.

**Proof of sufficiency and zero extension.** In (2), all coefficients of x are nonnegative, so (POS) holds. The cone holding sums telescope to s_v=a_(k_v)c_v. P preserves every retained c_v and its depth, so the cone holding sums are also preserved; hence H_Y P=P H_W. Under zero extension from X to X', every new vertex has zero source cone, and the source cone total at every old vertex is unchanged. The same is true of s_v=a_(k_v)c_v. Taking the cone-to-vertex difference gives H_X' I=I H_X, including zero holding at all new vertices. QED.

The proof does not assume an empty leaf is unreadable and then rename that as positivity. It excludes positive allocation to that leaf by compatible replication and a finite conserved total. The signed, total-zero defects allowed by draft 21 Lemma 27.1 cannot satisfy these conditions on the entire carrier class.

**Corollary 1 (relation to the existing ownership ledger).** In this carrier class, assume linear isomorphism-invariant holdings and section 17's (W1) and (W4), but do not assume (W2). Then (W2) follows, and the holdings have (2) with a_0=1.

Proof. (W1) gives (POS) and total H_W x = total x. (W4) says every retained holding except the parent's is unchanged by pruning. Comparing conserved totals therefore gives H_Y(Px)_p=H_W(x)_p+H_W(x)_l, which is the remaining coordinate of (PN). Apply Theorem 1. Conversely, (2) with a_0=1 satisfies (W1), (W4), and (W2). QED.

The relation to section 17.1 is b(w)=a_(depth w-1)-a_(depth w). This is its depth-invariant subfamily. The corollary does not extend section 17's result to arbitrary address-dependent assignments on one fixed finite or bounded-branching ambient tree.

## 4. One source-to-receiver transfer

Keep the same P1 event l -> p, with l at depth d. On a common nonnegative background x, compare x and x+g e_l, g>0. Only the source leaf differs; the declared receiver is the same parent p. Equation (2) gives

    pre-event receiver contrast  = g(a_(d-1)-a_d),
    post-event receiver contrast = g a_(d-1),
    increment of p's holding on one input x = a_d x_l.        (5)

All other retained holdings are unchanged by (PN). Their unchanged values may contain information already present before the event; no claim is made that the entire network was initially blind. The total holding kappa sum x is conserved within each preparation; the two preparations need not have equal global totals.

**Theorem 2 (local acquisition, no universal climb).** On this pair the receiver's complete scalar holding is initially identical and becomes different exactly when

    a_(d-1) = a_d > 0.                                      (6)

Under (6), every depth-(d-1) vertex on every carrier has holding a_d x_v, regardless of the rest of the depth sequence. The transfer into p is exactly the leaf's prior holding a_d x_l. No full global own-coordinate identification and no climb at other depths is required.

Proof. Equality before and inequality after in (5) are exactly (6). Substitution of the adjacent equality in (2) removes every descendant-cone term at depth d-1. The leaf's prior holding is a_d x_l, and (PN) adds it into p. QED.

This is a positive redistribution construction. The native P1 map changes the receiver's formal scalar from a_d x_p to a_d(x_p+x_l). The receiver does not need to inspect a hidden source label in the formula. For example, the already known Genesis-tax sequence a_0=1, a_k=1/2 for k>=1 permits acquisition at every depth d>=2 while Genesis is pre-informed at depth 1. This example illustrates the theorem; it is not a new choice of physical ownership.

The advance over draft 21 is that (E0)/(S_L)/(W2_F) is **derived for positive natural holdings on this carrier class**, not separately required. The elementary transfer criterion itself was already present in section 17.2 and section 27.3 after locality was assumed. Equation (6), the preparation, P1 event typing, and identifying the scalar with an actual available record are not derived here. An occurrence of some event on some correlated pair does not establish (6).

## 5. Exact limits and controls

### 5.1 Finite universes and a fixed branching cap

Fix B>=1 and epsilon with 0<epsilon<=1/B. On every rooted tree whose root has at most B children, define

    H_0(x) = (1 - epsilon deg(0)) sum_W x,
    H_v(x) = epsilon sum_W x             if depth v=1,
    H_v(x) = 0                          if depth v>=2.        (7)

This is linear, rooted-isomorphism-invariant, nonnegative on nonnegative grades, and conserves the total. It satisfies (PN). If a depth>=2 leaf is pruned, root degree and total are unchanged and its holding is zero. If a depth-1 leaf is pruned, its epsilon times total is added to the root, exactly matching the decreased root degree. Other retained holdings stay unchanged. The singleton case has H_0=total.

Nevertheless, on a root with a single empty leaf and input e_0, that leaf holds epsilon>0. Thus (E0) fails. The same counterexample works when every vertex, rather than only the root, is subject to the branching cap, and the number of vertices is unbounded. For a universe with at most N>=2 vertices, choose B=N-1. It works on the entire finite universe, not only a chosen test subset.

In cone notation (7) is nu(0,0)=1, nu(1,0)=epsilon and all other entries zero. On unrestricted fans its root holding eventually becomes negative. This pinpoints the use of unbounded compatible fan sizes in Theorem 1. The theorem cannot be transferred to a fixed binary/ternary/four-child native domain without an additional source-backed enlargement argument. Finitely many passing tests would not establish it.

### 5.2 Dropping positivity

The accepted draft-21 table nu=I+E_20-E_21 satisfies (PN) and acquisition along every one-location chain climb, but on the chain 0->1->2 and input e_0 its holding is (1,-1,1). It violates (POS) and (E0). This is exactly the type of compensated empty-branch assignment the positive-fan proof excludes.

### 5.3 Dropping the pruning ledger

Let each nonroot input unit be held entirely by its parent, with the root retaining its own unit. This is nonnegative and total-preserving on every tree, but fails (PN). On 0->p->l with x=e_l it gives H_W(x)=(0,1,0). After pruning l, H_Y(Px)=(1,0), whereas P H_W(x)=(0,1). Positivity and conservation alone do not establish the proposed receiver transport.

### 5.4 Locality is not acquisition or access

The Genesis dump a_0=1, a_k=0 for k>=1 satisfies Theorem 1 but gives no new distinction to a blank nonroot receiver; Genesis is already informed. Zero holdings also satisfy (PN),(POS) if normalization is not imposed. Thus Theorem 1 does not force a nonzero acquisition.

Likewise, all equations above are consistent with giving every receiver only the constant observable as its actually available record. Formal holdings then exist and transform as stated, but no available output distinguishes the preparations. The positive-cone calculation supplies neither a detector nor the identification of an existing receiver-owned record. This is the same remaining access issue, not a new impossibility claim.

## 6. Premise accounting and scientific value

Earned here: the complete positive (PN) classification; empty-leaf and cone locality; zero-extension naturality; redundancy of (W2) under (W1),(W4) with the stated carrier symmetry and enlargement scope; the precise local acquisition consequence; the all-size bounded-branching control.

Inherited mathematical objects: same-Genesis rooted carriers, P1 fiber sums, P2 zero extension, cone coordinates and their pruning deletion rule, and draft 20's naturality classification. No root shift, tensor factorization, quantum state encoder, measurement channel, event probability, metric or physical clock is added to the proof.

Required on the candidate holdings: linearity; rooted-isomorphism invariance; compatibility on all finite rooted trees including arbitrarily large fans; (PN); (POS), or the existing formal (W1),(W4) package. Those are not automatically properties of actual physical reads. In particular v16.23 TYPE_LEDGER explicitly treats its positive cone as a mathematical subobject, not a declaration of all physically attainable grades.

Required for the transfer interpretation: the P1-typed event; the contrasted preparable pair and common background; initial blindness and positive post-event contrast in (6); and a justified identification between H_p and a record actually available to p. A finite compatible carrier family by itself supplies neither that identification nor the all-carrier extension. Occurrence remains the accepted existential input; no universal completion is inferred.

Scientific value: this removes a specific independent locality assumption from the **positive ownership version of the existing candidate**, and gives an exact reason why the signed dipole freedom is unsuitable for globally compatible nonnegative holdings. It also identifies the carrier-enlargement scope that a native application must actually justify. It is not a derivation of physical access, and the raw criterion for the native milestone remains unsatisfied.

Next native obligation for this candidate: identify a source-backed receiver record whose nonnegative holdings obey the pruning ledger and whose carrier-composition domain supports the needed fan comparisons (or establish its empty-leaf property directly on the actual domain). Then check the existing record on one preparable blind-to-distinguished event, without defining that record or its response to obtain the answer. Do not launch a numerical campaign to substitute for this interface obligation.

## 7. Review and execution contract

All statements and controls above were derived analytically before freezing; they are disclosed derivations, not prospective numerical predictions. No scientific simulation, finite enumeration, archived scientific module, fitted parameter search, or purported full-stack verification is performed for this analytical support note. General proofs, not finite no-counterexample counts, are the evidence for its quantified claims.

Freeze this exact manuscript and its full source packet. Independent Gemini review must reconstruct (1)-(7), challenge the all-carrier quantifier and physical reading, check the bounded-branching control at every pruning type, and distinguish the new implication from the earlier ownership classification and acquisition formula. Integrity and a separate publication job must bind the exact argument, sources, raw response, model and run identities. Preserve original artifact ZIPs and complete logs. Acceptance is analytical review of the declared scope, not physical validation.

No numbered stage, main merge, CLOSED/CERTIFIED label or native milestone is claimed. Broad C3/C4-C6 and physical access remain OPEN. Time remains pruning / ordered recoverability update.
