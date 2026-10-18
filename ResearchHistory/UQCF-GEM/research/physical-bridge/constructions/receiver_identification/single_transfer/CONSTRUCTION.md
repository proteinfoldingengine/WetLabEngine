# One transfer without universal own-coordinate ownership

Author: proteinfolding-gpt. Date: 2026-10-18.
Inspected ownership baseline: `0aac7e0780881cc3b518a67e2807e8a4ca0c4199`.
Status: unreviewed analytical construction. Native bridge NOT_DERIVED.

## 1. Positive target

One initially blind receiver can acquire a distinction under the existing P1 pruning even when it is assigned some of the source's grade before the event. Universal own-coordinate ownership is not necessary for this existential target. The construction below uses equal-total, nonnegative preparations on one fixed carrier, and can make every initial grade strictly positive.

This is a continuation of receiver_identification draft 10, not a replacement of its classification. Its Theorem 17.3 concerns EVERY pruning on a specified ONE-LOCATION preparation pair. The present statement concerns ONE pruning with a different, explicitly correlated pair. That quantifier and preparation distinction matters: the user's accepted occurrence of an atemporal measurement does not imply universal acquisition on all those one-location pairs.

The inherited event primitive is P1; no event, controller, readout or outcome selector is implemented here. Its identification with the actual event remains conditional. The mathematical advance is a less restrictive positive witness to carry into the actual record/ownership correspondence, not a newly derived physical law. Admission class: B, supporting the existing single-native-transfer candidate A.

## 2. Objects and premises

Use a common-Genesis prefix carrier with addresses `X={o,p,l,v}`, with `o<p<l` and v another child of o. Remove l, retaining `Y={o,p,v}`. The same event P acts on both preparations:

    (Px)_p = x_p + x_l; (Px)_o = x_o; (Px)_v = x_v.       (1)

This is FCV P1. The accepted ancestry-retention theorem characterizes it by exact retained-cone preservation R; it does not establish R for an empirical measurement. Draft 9's E1-E5 route is likewise conditional. Neither conditional characterization is treated here as independent physical evidence.

For the holding assignment use the family in draft 10, Theorem 17.1:

    omega_u^X(x) = a(u)x_u + sum_{w child of u} b(w)C_w^X(x),
    a(u) = 1 - sum_{o<w<=u} b(w), b(w)>=0, a(u)>=0.      (2)

Its conditions are linearity, nonnegative exclusive ledger partition W1, zero-extension naturality W2, and event locality W4. These are requirements on a candidate ownership interpretation, not already established physical ownership/access laws. The direct calculation below uses the displayed family and therefore does not require independently accepting the full classification proof.

Write

    A=a(p), B=b(l), D=a(l)=A-B,                           (3)

so `0<=B<=A`. On this carrier,

    omega_p^X(x)=A x_p+B x_l,
    omega_p^Y(Px)=A(x_p+x_l).                            (4)

Assume `D>0`. Then A>0 and `r=B/A` lies in [0,1). Grades may be real. For rational grades, take rational ownership coefficients so r is rational. No universality over physically preparable grades is inferred from FCV P0.

## 3. Construction: same initial holding, separated output

Fix ANY common nonnegative background z in F^X and define

    x_plus  = z + e_l,
    x_minus = z + r e_p + (1-r)e_v.                      (5)

Both are nonnegative and both have total `sum z + 1`. Choosing every z_u>0 makes every coordinate in both preparations strictly positive, including the pruned leaf and the retained receiver. Thus this witness does not require an initially empty receiver, a zero-weight pruned leaf, a different carrier, or different event selection between preparations.

Let `h=omega_p^X(z)` and `k=omega_p^Y(Pz)`. Equation (4) gives

| Candidate whole holding | x_plus | x_minus |
| --- | ---: | ---: |
| Before the common event | h+B | h+A r = h+B |
| After the common event | k+A | k+A r = k+B |

Hence the initial holdings agree exactly, while the output difference is

    omega_p^Y(Px_plus)-omega_p^Y(Px_minus)=A-B=D>0.        (6)

In the formal algebra of all functions of this scalar holding, equality in the first row gives blindness of the WHOLE algebra, not just one selected observable. Unequal definite output values give distinct evaluation states afterward. A separating function exists mathematically; its physical availability is not derived by writing it down.

This is an equal-total source distinction, redistributed by the same inherited event. The initial correlations compensate the pre-credit B without eliminating the source distinction. In particular `x_plus-x_minus=e_l-r e_p-(1-r)e_v` has total zero, vanishing initial p-holding, and nonzero output p-holding. No product-nuisance assumption is made. The product-nuisance sufficiency and convolution results from sections 13-15 are NOT invoked for this correlated pair.

**Exact local criterion within this formal domain.** On the displayed carrier and holding family, there exist equal-total nonnegative preparations with equal initial p-holding and different output p-holding if and only if D>0. Sufficiency is (5)-(6). For necessity, if D=0 then (4) gives `omega_p^Y(Px)=omega_p^X(x)` for EVERY x; any initially equal pair stays equal. Positivity in (2) excludes D<0. This criterion concerns existence of a preparation pair in the declared mathematical domain, not native preparability.

**Accounting interpretation.** The leaf has holding `omega_l^X(x)=D x_l`. Equations (1)-(4) give

    omega_p^Y(Px)-omega_p^X(x)=omega_l^X(x).              (7)

The receiver gains exactly the grade previously assigned to the disappearing leaf. The other retained holdings are unchanged under W4, and W1 conserves their global sum. This is redistribution, not information or grade created globally. Equation (7) also follows by subtracting the two total-holding identities and using W4. That accounting argument does not derive W4 itself: naming p the receiver is not an independent justification of event locality.

## 4. An explicit positive-background example

Choose `b(p)=1/4`, `b(l)=1/4`, `b(v)=0`, with other b values zero. Then `A=3/4`, `B=1/4`, `D=1/2`, and `r=1/3`. Choose `z=(1,1,1,1)` in order `(o,p,l,v)`.

    x_plus  = (1, 1,   2, 1),
    x_minus = (1, 4/3, 1, 5/3).

Both totals are 5; all grades are positive. Both initial receiver holdings are 5/4. P1 gives

    Px_plus  = (1, 3,   1),
    Px_minus = (1, 7/3, 5/3)

in order `(o,p,v)`. The output receiver holdings are 9/4 and 7/4, separated by 1/2. Every quantity here follows by exact substitution; no numerical execution or evidence count is claimed. Scaling both preparations by 3 gives an integer-grade witness for these rational coefficients if an integral formal instance is desired; it still does not establish physical preparation.

The useful feature is B>0: the receiver is pre-credited with some leaf grade and nevertheless acquires the distinction in this pair. Pre-credit invalidates the ORIGINAL uncorrected pair's blindness; it does not forbid every possible initially blind correlated pair.

## 5. Relation to draft 10 and limits of the improvement

Draft 10, Proposition 17.2(c), correctly requires `B=0` and `A>0` for its one-location pair and for the earlier uncompensated pair `e_l` versus `e_v`. Equation (5) is different. It changes the preparation obligation; it does not refute that proposition or establish acquisition for the original pair when B>0.

Theorem 17.3's universal one-location acquisition hypothesis forces b identically zero. It is unnecessary for our one-event existential construction. In particular, an occurrence input or the observation that one event acquires information cannot be substituted for that universal hypothesis. Corollary 17.6 remains a conditional statement only with the stronger premise explicitly present; the user's occurrence input does not supply it.

The new pair changes x_p as well as external coordinates. Equality of omega_p is therefore NOT enough if the actual receiver also has independent access to x_p or to another distinguishing component. Nor does this pair implement an intervention confined to l. If the intended native preparation must hold x_p fixed, or permits only the original source family, use the original witness and its B=0 condition instead. The correlated preparation in (5) cannot silently be counted as already earned.

The positive reduction is local: for one identified event, seek a genuine receiver record of the form under consideration, a positive residual holding D at its disappearing source, and an admissible initially blind joint preparation. There is no need first to prove a universal ownership law for all addresses and all events. But it remains essential to prove that the candidate holding represents the receiver's entire relevant initial accessible state and a genuinely available final distinction.

## 6. Keep the actual-record type explicit

This turn also inspected the existing actual-record operation, v15.11 `select_record`. Given a supplied positive-weight projection q, its mathematical state update is

    rho_q = q rho q / Tr(rho q).                          (8)

It does not select q itself. The user's accepted measurement occurrence does not by itself identify (8) with the extensive P1 grade update (1).

The canonical record-compatibility tree gives an exact small comparison without inventing a mapping to the Genesis ledger. Take orthogonal rank-one projections p,s with p+s=I, the record tree `T={I,p,s}`, rho=(p+s)/2, and selected record p. Assign leaf probability grades `(0,1/2,1/2)` to T. The compatibility view is `V(p)={I,p}`. P1 on THIS diagnostic tree moves s's grade to I and yields `(1/2,1/2)`. Selective conditioning instead gives rho_p=p, represented by grades `(0,1)` on that view. The retained p-cone total is 1/2 under P1 and 1 under conditioning.

Thus the actual selective operation is not an automatic witness for the ancestry-retention contract R when grades are these branch probabilities. This does not identify branch probability with the physical extensive grade, refute the P1 theorem, or rule out a separate source-measure correspondence. It prevents a type substitution from masquerading as that correspondence. Existing measurement_first already proves the appropriate conditioning/pushforward compatibility for fiber-compatible events; that theorem is reused, not claimed anew. Existing COMPATIBLE_FIBER_RETENTION already states the remaining old-part/record correspondence. Neither result grants ownership merely by centrality or a matching label.

## 7. The next native target and review boundary

Keep ONE transfer as the objective. The next source-backed deduction must identify one actual retained record/process and establish:

1. Which grade it carries, and why this actual event acts on that grade as the inherited P1 contraction (or, if it is a selective quantum record, the correctly typed conditional action instead).
2. Which part is genuinely owned/available to the receiver, without deriving locality or access by definition. For the present P1 construction, only a local positive residual D is needed, not universal b=0.
3. A native preparation pair that is blind on the receiver's entire initial available state. Equation (5) is a precise correlated option to justify; the original pair remains the simpler option when B=0 is independently established.

Occurrence of the atemporal measurement remains accepted input. No fundamental clock, conscious observer, external detector, added tensor factor, or readout controller has been required. Preparability, event typing and physical ownership/access remain separately open. Another sweep over sums or another proof of an equivalent global characterization would not discharge these obligations.

This note commits the positive construction before any new scientific execution or adversarial review. It has not received Gemini review and is not an acceptance receipt. No new scientific workflow is launched for this elementary supporting lemma alone; it should be included with the next complete actual-record correspondence candidate. Grok's separate draft-9 verification/review remains untouched. No main merge, numbered-stage certification, native milestone, or new mechanism in code.

Source identities are recorded in SOURCE_MANIFEST.json. Frozen prior arguments are unchanged.
