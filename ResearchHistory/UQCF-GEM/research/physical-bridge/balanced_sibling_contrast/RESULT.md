# Balanced sibling contrast under inherited P1 pruning

Date: 2026-10-21 (America/Phoenix).
Source baseline: def537e928c9839fe956aeddb6ad81ed5e6380ba.
Status: analytical candidate; independent review pending. Native bridge NOT_DERIVED.

## 1. Scientific question and relation to prior work

Can one fixed preparation pair be initially blind at a parent for every positive natural holding law, while a fixed P1 event produces a nonzero parent contrast, without requiring adjacent-depth equality?

Yes, conditionally on a positive leaf self-holding. A balanced difference between two sibling leaves cancels the parent's initial descendant contribution without choosing the pair using unknown coefficients. Removing only one of those leaves exposes a contrast. Removing both erases it.

The inherited positive-holdings classification and its one-location transfer formula are credited to positive_retained_holdings/RESULT.md Theorems 1–2. Receiver identification §17.6 and §27.4 already give coefficient-dependent correlated preparations that avoid universal own-coordinate identification. This note does not claim the first correlated-pair escape. Its target is a coefficient-independent balanced pair, the exact common blindness subspace, and the partial-versus-complete pruning control.

This changes the preparation class. It does not refute the adjacent-depth condition for the earlier one-location or inside/outside pair.

## 2. Typed setting and supplied interfaces

Let X be a finite rooted tree. Let p have depth k and distinct leaf children u,v. Grades are nonnegative real vectors. Use the established family

    H_X(x)_w = a_j x_w + (a_j-a_(j+1)) D_w(x),
    D_w(x) = sum of grades at strict descendants of w,
    j = depth(w),   1 = a_0 >= a_1 >= ... >= 0.             (1)

The all-tree classification assumes linearity, rooted-isomorphism invariance, positivity and pruning naturality (PN). Here (1) is the candidate family, not a law of physical access. We do not derive its all-carrier applicability or normalization.

For each preparation the proposed complete scalar receiver state is H_X(x)_p, including all functions of that scalar. Identifying this with the receiver's entire actually available record remains supplied. This is weaker than global I*: holdings need not equal own grades. If the receiver also has available child-resolved information, scalar blindness is insufficient.

P_S removes a fixed subset S of immediate leaf children of p and adds their grades into p. Other grades and retained depths are unchanged. It is a composite of inherited P1 leaf contractions, independent of pruning order. The same S is used on both preparations; no selection based on occupied leaves, hidden source labels or desired outputs is allowed. Mathematical admissibility of P_S is not physical event typing or preparability.

## 3. Exact coefficient-independent blindness subspace

For a fixed difference Delta=x_plus-x_minus, let

    q = Delta_p,       d = sum_(w strictly below p) Delta_w.
    
The parent contrast before the event is

    B_a(Delta) = a_k q + (a_k-a_(k+1)) d.                  (2)

**Theorem 1.** B_a(Delta)=0 for every normalized nonincreasing nonnegative sequence a if and only if q=d=0.

Proof. Sufficiency follows from (2). For necessity choose the admissible all-ones sequence: (2) gives q=0. Choose a_j=1 for j<=k and a_j=0 for j>=k+1: (2) then gives q+d=0, hence d=0. These are witnesses used to characterize a family, not fitted physical coefficients. The argument includes k=0. QED.

This subspace fixes the parent's own grade and its total strict-descendant grade between preparations. It permits redistribution inside the cone. In particular Delta=g(e_u-e_v), g>0, belongs to it without any knowledge of a.

**Theorem 2.** Put s=sum_(l in S) Delta_l. For the same parent after P_S,

    B'_a(Delta) = B_a(Delta) + a_(k+1) s.                 (3)

Thus on the common blindness subspace, the post-event contrast is exactly a_(k+1)s.

Proof. The parent's new own-grade difference is q+s. Its surviving strict-descendant difference is d-s. Substitution in (1) gives
a_k(q+s)+(a_k-a_(k+1))(d-s)=B_a(Delta)+a_(k+1)s.
All surviving depths are unchanged. QED.

The consequence is positive for a positive s precisely when a_(k+1)>0. Adjacent equality a_k=a_(k+1) is unnecessary. No coefficient-independent positive lower bound follows: allowed a_(k+1) can approach zero or equal zero.

## 4. Explicit fixed-preparation witness

Take X={o,p,u,v}, with p a child of o and u,v children of p. Let

    x_plus = g e_u,        x_minus = g e_v,     g>0.
    S={u},                k=1.                              (4)

Both inputs have equal total grade g, the same parent own grade zero, and the same parent cone total g. The fixed event removes u in both cases, including the case with zero grade at u. No claimed native law ensures this event in both preparations.

The exact parent holdings are

| Record | plus | minus |
| --- | --- | --- |
| Before event | g(a_1-a_2) | g(a_1-a_2) |
| After removing u | g a_1 | g(a_1-a_2) |
| After subsequently removing v | g a_1 | g a_1 |

The intermediate contrast is g a_2. The parent is initially uninformed about this pair, but need not have zero holding. For example a_0=1,a_1=3/4,a_2=1/4 (extend with 1/4 at every deeper level) gives initial holdings g/2,g/2 and intermediate holdings 3g/4,g/2. It satisfies the strict inequality a_1>a_2, disproving any claim that adjacent equality is necessary for acquisition on every preparation class.

In the intermediate carrier the surviving leaf v has contrast -g a_2. Other retained vertices have zero contrast. The new parent distinction is balanced by the surviving sibling distinction. Total holdings remain equal, and no global information is created.

## 5. Retention, readout and rejecting controls

1. Complete-fiber erasure. Removing both u and v yields the same entire grade vector g e_p in both preparations. Every deterministic read of the final configuration is then identical, regardless of holding coefficients. No memory of the intermediate contrast has been constructed.
2. Wrong leaf. Add an empty sibling w and remove only w. Then s=0 and no parent contrast appears.
3. Zero self-holding. If a_(k+1)=0, partial pruning produces no parent gain despite initial blindness. The admissible Genesis-dump family is one example for a nonroot parent.
4. Broken balance. Delta=g e_u instead gives initial contrast g(a_k-a_(k+1)). The older one-location equality requirement is recovered exactly.
5. Extra receiver access. An available read of x_u, x_v, or their difference distinguishes (4) before the event. Our blindness statement covers the scalar holding and all its functions, not such an enlarged record.
6. Only occupancy available. If a_k>a_(k+1)>0 and g>0, both intermediate holdings are positive. The unit-free occupancy read 1[H_p>0] cannot distinguish them. Full scalar distinction must not be silently substituted for a justified available effect.
7. Unequal sibling weights. In receiver identification §17's more general address-dependent family, pre-event contrast is g(b(u)-b(v)); balance alone is blind only if b(u)=b(v). The coefficient-independent witness uses the depth-uniform family (1), whose provenance must remain explicit.
8. Symmetry and event choice. Rooted isomorphism invariance of H does not select u rather than v as an actual outcome. The event is a fixed addressed contraction supplied to the mathematical comparison. Its occurrence/type across preparations requires an independent association; no new selector is derived.

By PN, pruning a leaf into another retained parent leaves p's holding unchanged. More generally (3) quantifies any subsequent subset of p's leaf children. For (4), the contrast persists through operations not transferring the compensating v contribution into p, provided p remains the receiver and the holding model applies. Pruning v erases it even while p survives. Thus owner survival alone is not sufficient retention. There is no clock, duration or assumed opportunity to consume the intermediate result.

## 6. Scientific consequence and limits

The result replaces the adjacent-depth equality requirement for this balanced preparation class by the weaker nonzero self-holding a_(k+1)>0. It does not replace receiver identification, preparation or event typing. It derives no receiver-access change. The same scalar rule H is used before and after.

A conditional observational signature is an intermediate parent contrast g a_(k+1), followed by exact erasure when the compensating sibling is also absorbed. This is an event-ordered algebraic signature, not yet an executable physical prediction. An actual receiver would need an independently justified effect resolving the intermediate amounts and a retained record or use before erasure. No such consumer is inserted here.

The algebraic step beyond the cited prior results is modest: the common-kernel characterization in Theorem 1, a preparation fixed independently of the depth coefficients, and the selective-versus-complete contraction signature. The transfer increment itself is inherited PN bookkeeping. No archive-wide novelty claim is made.

## 7. Review contract

This is pure analytical work, not a numbered stage or scientific enumeration. All derivations and controls were known before freezing. No exploratory numerical result is recast as preregistered. Independent review must check both directions of Theorem 1, (3), the equal-total witness, every control, overlap with §§17 and 27, and the distinction between scalar blindness and physical access. The reviewer must challenge the compensating sibling, the fixed same event on an empty versus occupied leaf, retention and occupancy limitations.

No new native axiom, geometry, fundamental time, dark-matter variable, fitted detector or model coefficient is adopted. Native milestone and C3/C4–C6 remain open. No scientific execution or full foundational-stack replay is claimed; independent review, publication audit and immutable readback are required before calling this candidate accepted.

