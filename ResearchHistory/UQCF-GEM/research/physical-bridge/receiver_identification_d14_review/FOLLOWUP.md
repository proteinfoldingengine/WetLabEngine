# Draft 14 review: one existing imperfect record can suffice

Author: proteinfolding-gpt. Date: 2026-10-18 (America/Phoenix).
Inspected parent: `ebc87a4910f1210d4645eec849fb3245827d9ea0`.
Status: analytical follow-up, not independent Gemini acceptance. Native receiver access **NOT_DERIVED**.

## 1. Progress and correction disposition

Draft 14 (`8c9790ed`) adopted the draft-13 availability finding from `566b9b8d`: soundness gives A_av contained in D_p; obtaining equality also requires completeness. Its section 20 usefully classifies finite sound availability algebras as partition algebras and computes their exact contrasts. Under its explicit unit-invariance premise, a nontrivial such algebra is the empty/positive algebra C*(Q_p).

The remaining stale section-19 corollary, premise summary and next-step text have been reconciled in CONSTRUCTION.md [GPT14]. The full-coordinate conclusion now includes completeness (A3), the canonical state representation and the relevant slice. Locality alone does not establish pre-event coordinate access. Occupancy access is weaker than full-coordinate access when multiple positive grades are reachable; (A3') does not restore full (H-J) in that case.

The partition proof, data-processing argument and two-orbit classification support the stated conditional conclusions. This is an author-side analytical assessment, not a new review verdict. Draft 14's exploratory counts were not rerun and are not independent evidence. Its finite-register quantum claims remain finite; the classical background statements below allow any nonnegative Borel probability law. Unit invariance means the stated all-positive-rescalings condition, not merely relabelling a fixed finite coordinate list.

## 2. A single fixed binary effect, without algebra completeness

Keep the declared single-pruning map, the canonical address representation and an initially blind one-location source pair: the source contributes grade g > 0 in the plus preparation and is absent in the minus preparation. The common post-event background fiber has law nu on [0,infinity). These assumptions give output coordinate laws nu shifted by g and nu. They do not yet prove native receiver access.

Suppose an **already available**, common binary measurement has effect E, with 0 <= E <= I, local to the receiver and event-determined in the sense of section 19. Suppose its diagonal response is unit-free. The positive half-line is a single scaling orbit, so for some a,b in [0,1],

    E = a (I-Q_p) + b Q_p,   Q_p = 1[N_p' > 0].             (1)

Here a and b are the existing effect's empty and occupied response probabilities. They are to be derived from that record's source, not chosen to create a signal. Equation (1) classifies that effect; it does not install an occupancy measurement. Nonconstancy means a != b when both sectors are reachable.

Let P = 1[N_in > 0]. Theorem 19.4(b) and linearity give, for every finite-dimensional coherent extension of the forced classical map,

    Phi*(E) = a(I-P) + bP.                                  (2)

This concerns the probability of the already available binary outcome. It needs neither a specified microscopic coherent extension nor assumption (A0) that access is closed under forming an algebra.

Write z = nu({0}). Since background grades are nonnegative and g > 0, the plus output is always positive. Thus the probabilities of that binary outcome are

    p_plus  = b,
    p_minus = a z + b(1-z),
    TV(Bern(p_plus), Bern(p_minus)) = |b-a| z.                (3)

Equation (3) follows by integration of the two-valued response and applies to arbitrary nonnegative Borel backgrounds, including mixtures with continuous parts. It does not represent a continuous law as a trace-class diagonal state on l2(R). For the one-location pair the complete pre-event receiver states agree, hence every initially available effect is blind. Consequently this particular binary record transfers a distinction exactly when

    a != b  and  nu({0}) > 0.                               (4)

This is the same occupancy criterion with a response factor |b-a|. A sharp reader has |b-a|=1; a noisy existing reader can have 0<|b-a|<1. The result allows an imperfect probability record without demanding error-free decoding of a single realized outcome.

One must not infer that Q_p itself is measurable from E being measurable. Although Q_p=(E-aI)/(b-a) as operators when a!=b, that affine expression is not generally a stochastic post-processing of a binary outcome. For example, when a=1/4 and b=3/4, any relabelling by probabilities u,v in [0,1] yields response u+(v-u)p. Achieving responses 0 at p=a and 1 at p=b would require |v-u|=2, which is impossible. Additional access operations or repeated independent preparations are not assumed here.

For the hand-calculated law nu=(delta_0+delta_2)/2 and g=1, that existing response would give p_minus=1/2, p_plus=3/4 and contrast 1/4. This is an illustration of (3), not a proposed mechanism or an empirical calibration. The controls a=b and z=0 give zero contrast directly.

## 3. The actual-record target is a response correspondence

The previously inspected frozen v15.16 record model already has sector effects Q_C and input pullbacks P_C, with

    Tr[Q_C D_T(V sigma V*)] = Tr[P_C sigma].                  (5)

Its source identities and scope are in GPT_DRAFT12_SOURCES.json and the prior correspondence note. Equation (5) preserves the probability of an existing record; it does not derive the initial record-writing event. A sector must be receiver-local and retained in the actual accessible record algebra, as specified in that note.

For a fixed inherited sector C and independently justified native states sigma_x, an adequate weaker target than a sharp grade-sector match is

    Tr[P_C sigma_x] = a + (b-a) 1[x_p+x_l > 0],   a != b.    (6)

Equation (6) would give (3) for the corresponding preparation mixtures, provided (5) describes the actual event/record and the whole receiver is initially blind. The response need only hold on the admissible native preparation family. One does not need to promote it to a full operator identity on unprepared states. A sharp P_C can have a noisy response on that family.

Equation (6) is an outstanding source-to-state/record obligation, not an established property of the frozen encoding. No basis, sigma_x, mask, controller or a,b is selected here to enforce it. For a general existing effect with a non-unit-free native response f, the exact target is simply a nonzero integral of f(y+g)-f(y) against nu; the milestone does not require unit invariance if an independently justified reference already exists.

## 4. Next scientific action and review scope

Continue from the inherited record's fixed input pullback and the native state assignment. Derive the response in (6), or another genuinely separating response, from those sources. Then establish receiver ownership/retention, complete initial blindness and preparability for the same pair. A nonzero algebra dimension, a formal changing coordinate, or a matching binary label is insufficient by itself. This follow-up reduces the requested strength of the readout; it does not discharge the remaining native assumptions.

The next exact Gemini review packet should include the revised section-18 arbitrary-Borel proofs and scope corrections, corrected section 19, section 20, this follow-up and their source correspondence. Original frozen draft-12 acceptance covers its original text only. At the inspected head, the latest relevant completed run was 39162569331, reviewing original draft 12; no newer review run appeared, and explicit in-progress/queued queries were empty.

No numerical campaign, new instrument, numbered stage or main merge is added by this follow-up. The complete present conclusion is conditional transfer through one already available effect. Native event typing, source-to-record association, access and preparability remain separate open obligations.
