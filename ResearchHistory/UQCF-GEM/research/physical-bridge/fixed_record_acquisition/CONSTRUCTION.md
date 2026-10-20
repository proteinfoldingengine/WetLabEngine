# One fixed receiver record across nonunique event actions

Author: proteinfolding-gpt. Date: 2026-10-20 (America/Phoenix).
Inspected research parent: `aa5aa96c002c181fb2e833f12fcabb15d94c5d6f`.
Status: **unreviewed analytical support for the existing native-record candidate**. Native bridge **NOT_DERIVED**. This is elementary finite-dimensional duality, not a claim of new mathematics, a native mechanism, or a numerical campaign.

## 1. Positive construction and purpose

An event need not determine a receiver effect's entire response function to force an accessible distinction. It is enough that one **already available, fixed effect** has a strictly positive response difference, on the same initially blind preparation pair, for every justified admissible action. The difference may vary across actions.

This note gives an exact constructive criterion for that weaker target. It keeps the input preparations, their native state assignments, the complete initial receiver information, the available output effect, and the admissible action class fixed. None is optimized to obtain the desired answer. Only the preparation mixture is constructed, and that step is expressly conditional on legitimate mixture preparation.

The application is the open native-state/record interface after Draft 28. Draft 28 characterizes formal transfer under PN by climb blindness and Side_D. It does not supply the receiver's actual record. Earlier fixed-effect work allows one imperfect record, but its principal example has one response fixed by every coherent extension. The criterion here permits different response vectors across actions while certifying a common observable consequence. It does not replace or re-prove the accepted leaf-transfer theorem.

During this work, the concurrent `single_event_receiver_gain` manuscript was published at `86ea348c5886005431413eefd2207a293438f8fc`. Its exact text was inspected. It gives a local PN gain identity and the field-effect pullback, explicitly retaining complete initial blindness and availability as separate obligations. Its frozen proof and review process are untouched. The present note complements its one-action calculation with an action-family criterion; neither manuscript establishes the missing native record. This addition is not included in that manuscript's independent review.

## 2. Fixed objects and their provenance obligations

Let there be n specified admissible preparations x_1,...,x_n, with an independently justified state assignment when a state representation is used. There is no newly chosen encoder. Let M be a nonempty specified class of event actions on these preparations. Every member must represent the same event under the declared native premises and share a justified output-record identity. A convenient mathematical family of channels is not automatically this native class.

Fix a binary effect E already available to the receiver **after** the event. Define its actual response vector for action m by

    q(m)_i = Pr(E's outcome | preparation x_i, action m),
    Q = {q(m) : m in M} subset [0,1]^n.                    (1)

In a quantum representation this is Tr[E Phi_m(sigma_i)]. In a classical representation it is the corresponding probability. Neither representation is required to be fundamental. Suppose Q is nonempty and compact; below we also give the consequence when compactness is absent. The effect E, its outcome label and its availability do not depend on m or on which preparation was selected.

Let B be a finite real matrix whose columns describe the preparations' **complete initially available receiver states**, together with a first row of ones. Additional already justified comparison constraints may be included as rows. Its defining contract is

    B mu_plus = B mu_minus

if and only if the two mixtures satisfy those initial-record and comparison equalities. In finite-dimensional quantum theory, a real coordinate basis for the full initial receiver state suffices. For a finite classical record alphabet, use its full probability distribution, not merely the mean of one coordinate. More generally, finitely many preparations make the span of their initial response vectors finite-dimensional, but the completeness of the supplied rows must still be proved from the actual access model.

An extra total-grade row enforces equality of **mean** grade, not identical grade distributions or a definite common charge. To compare a definite conserved sector, restrict the x_i to that sector. Alternatively include all required sector-indicator rows. There is no implicit equivalence between these requirements.

Finally assume the admissible preparation family includes all probability mixtures mu of these n preparations, with affine initial and final probabilities. Randomization is not a free native primitive: this is a preparation assumption to establish. Without it the exact constructive converse below need not hold. The chosen mixture is independent of the unknown action m.

All these are interface contracts, not newly derived native premises. The inspected source trace has **not** supplied this complete tuple for a native event.

## 3. Exact construction for one action-independent response

First suppose Q = {q}. Put L = ker B, with its ordinary Euclidean inner product, and let Pi_L be the orthogonal projection onto L. This is a proof device, not an observation or a physical geometry.

**Proposition 1.** There are probability mixtures mu_plus, mu_minus with identical initial records and comparison data but unequal E-response if and only if

    q not in row(B), equivalently v := Pi_L q != 0.        (2)

A concrete witness is obtained by writing v = v_+ - v_- componentwise and setting

    s = sum_i (v_+)_i = sum_i (v_-)_i > 0,
    mu_plus = v_+/s,  mu_minus = v_-/s.                   (3)

The outcome-probability difference is ||v||^2/s > 0.

*Proof.* The normalization row implies sum v_i = 0, so (3) gives probability vectors. Bv = 0 proves all initial and comparison equalities. Since q-v lies in row(B), q dot v = ||v||^2. Conversely, any admissible pair has d = mu_plus-mu_minus in ker B. If q lies in row(B), q dot d = 0. QED.

This constructs mixtures of fixed preparations; it does not create a source-to-state association or supply a measurement. For a fixed prescribed pair, the test is simply Bd = 0 and q dot d != 0; no ability to prepare every mixture is needed for that direct check.

## 4. A common observable contrast without a common microscopic response

Define the compact convex set

    K = conv{Pi_L q : q in Q} subset L.                  (4)

Taking this convex hull is an analytical operation. It does not assume physical randomization between event mechanisms.

**Theorem 2.** The following are equivalent:

1. There are two probability mixtures with B mu_plus = B mu_minus and a number delta > 0 such that

       q dot (mu_plus-mu_minus) >= delta for every q in Q. (5)

2. The origin is not in K.

If 0 is not in K, let v be the point of K nearest the origin. Formula (3) gives an explicit pair satisfying (5) with

    delta = ||v||^2/s > 0.                               (6)

This is a guaranteed lower bound for this constructed pair, not a claim that the pair maximizes the achievable contrast.

*Proof.* K is nonempty compact and convex in a finite-dimensional space, so a minimum-norm v exists. If 0 is not in K then v != 0. For any k in K, v+t(k-v) belongs to K for 0 <= t <= 1. Differentiating its squared norm at t=0 from the right gives

    v dot (k-v) >= 0, hence v dot k >= ||v||^2.

Because v is in L, q dot v = (Pi_L q) dot v >= ||v||^2 for every q in Q. The normalization row and Bv=0 again make (3) a valid initially blind pair, giving (6). Conversely, if (5) holds, d = mu_plus-mu_minus lies in L and d dot k >= delta for every k in K. This is impossible if 0 is in K. QED.

The same outcome label and the same sign work for every action. The binary output laws therefore have total-variation distance at least delta. This is a probability-law distinction; it neither identifies the source from every individual outcome nor grants repeated independent trials. Retention and availability of the actual binary outcome remain part of the record contract.

If Q is not compact, replace K by its **closed** convex hull. Since Q is bounded, that set is compact; the theorem still characterizes a uniform positive margin. Pointwise strict differences whose infimum is zero are weaker and do not satisfy (5).

## 5. Exact analytical examples and controls

These are hand calculations, not sampled event mechanisms, native preparation evidence, or a computational campaign.

### Positive example: response varies, discrimination survives

Take two preparations with identical complete initial receiver states and comparison data, so B has row space spanned by (1,1). Suppose the justified response set were

    Q = {(1,0), (3/4,1/4)}.

The projected vectors are (1/2,-1/2) and (1/4,-1/4). Their segment's nearest point is v=(1/4,-1/4), so s=1/4 and delta=1/2. Formula (3) selects the two original preparations. Their E-response differences are 1 and 1/2. No unique response function is needed. These probabilities illustrate the criterion; they are not selected as a native law.

### Control A: a common sign is stronger than nonzero contrast

With the same B and Q={(1,0),(0,1)}, the projected segment contains zero. There is no pair with the same strictly positive signed difference for both actions. Nevertheless the two pure preparations have absolute contrast one under each action. Thus failure of Theorem 2 is **not** a theorem that every allowed action is blind, nor that no action-dependent test can distinguish. If a half-and-half mixture of the two actions is independently admissible, that mixed action is blind, but its admissibility must not be inferred merely from forming (4).

### Control B: include the whole initial record

Let two preparations share one displayed scalar holding, but differ in another already available initial record bit. The correct B includes the row (0,1) as well as (1,1), so ker B={0}. The criterion certifies no acquisition between different mixtures of these two preparations. Omitting the extra bit would incorrectly call an already informed receiver blind. This is exactly the interface obligation left open by the formal holding results.

### Control C: preparability cannot be supplied by linear algebra

Consider three initial classical binary states with outcome probabilities 0, 1/2 and 1, and fixed final responses q=(0,0,1). Then

    B = [[1,1,1], [0,1/2,1]],  d=(1,-2,1),
    Bd=0,  q dot d=1.

The equal mixture of preparations 1 and 3 is initially identical to preparation 2 and has final response 1/2 instead of 0. If only the three individual preparations are admitted and their mixtures are forbidden, all initial states differ and no distinct initially blind pair exists. The converse requires the stated mixture closure.

### Control D: a nonconstant record need not acquire information

For the same B as Control C, q=(0,1/2,1) belongs to row(B). Its final response is already an initial receiver statistic. Every initially matched pair has zero final contrast, although the effect varies across individual preparations.

## 6. Application to the existing leaf-transfer candidate

The accepted mathematics gives, for an admitted one-location pair and the stated PN/blindness/Side_D premises,

    F_W e_l = kappa e_l,  F_Y P e_l = kappa e_p.

It remains essential not to replace B by a single row F_W(·)_p unless that row is proved to encode the receiver's complete initial state. Nor may q be assigned the value of F_Y(·)_p without an independently available effect and its response correspondence.

For the existing **conditional** same-total placement example, take the four-address carrier o<p<l with v another child of o, preparations e_l and e_v, and prune l into p. Both have total grade one and initial own-coordinate x_p=0. If the receiver's complete initial state is independently established to depend only on x_p and an already fixed output effect has responses b at grade one and a at grade zero, then B's columns coincide and q=(b,a). Proposition 1 gives contrast |b-a|, with the preparation labels interchanged when necessary. This reuses the earlier placement construction; it does not newly earn its access or preparability premises.

The useful extension is that exact values a,b need not be uniquely selected by the native event. A derived action class with q_1-q_2 >= delta > 0 suffices. More generally Theorem 2 constructs the pair when the actual response family satisfies its separation condition. The input association, output effect and admissible action class must come from sources **before** this test is applied.

Draft 28 is unchanged. This note supplies neither Bl_D nor Side_D, and does not identify formal holding transport with an available record. It makes the operational target less restrictive than requiring a fully event-determined effect on every input: only one fixed pair's signed response needs to be uniformly separated.

## 7. Native evidence still needed and stopping rule

The exact missing object is one source-backed tuple

    (admissible preparations and their state assignment,
     complete initial receiver record B,
     actual event-action class M,
     already available retained output effect E).

For that same tuple, prove the response constraints defining Q and the preparation permission used by the witness. This note supplies no native instance of that tuple. The existing grade-to-quantum source trace explicitly leaves the assignment missing; the V1172 writer trace identifies software telemetry but not native receiver access. These findings are preserved, not reclassified as new obstructions.

No numerical search over encodings, effects, partitions or channels is authorized by this certificate. There is no reason to optimize a hypothetical Q. The next decisive work is to obtain the actual tuple from the inherited event/record construction and apply this exact criterion, using a prescribed pair directly if mixture closure is unavailable. If a source only grants a formal coordinate, keep that boundary explicit.

This is category B analytical support, pending independent whole-argument review if incorporated into a material native candidate. It is not category D, an empirical prediction, or a completed physical bridge. No separate numerical or reviewer campaign is proposed merely to certify elementary separation algebra. The accepted prior reviews do not cover this note. Broad C3/C4-C6 and physical origin remain OPEN.
