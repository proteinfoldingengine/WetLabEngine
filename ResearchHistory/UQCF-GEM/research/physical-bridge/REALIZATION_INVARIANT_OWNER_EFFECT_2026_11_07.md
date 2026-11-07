# Realization-invariant retained-owner effect for the accepted P1 benchmark

Date: 2026-11-07 America/Phoenix.
Author: ChatGPT research session.
Status: AUTHOR ANALYTICAL SYNTHESIS; conditional on the already supplied/accepted benchmark representation. Native bridge NOT_DERIVED.
Parent research head: 7ca75025ba23e2ff1f3c831797aa91112d6f70a1.

## 1. Why revisit the receiver location

Recent receiver-delivery work correctly shows that the same reduced source channel can have joint realizations W_R, W_E and Bell-like completions that place the complementary fine-grained record in different outputs. Therefore source-channel information alone cannot force an arbitrary complementary subsystem R to receive that record.

That does not imply that every receiver candidate is realization-dependent.

The native P1 owner is a RETAINED source coordinate. In the accepted P1 benchmark, the retained physical source code is also fixed. This note asks the directive's Target D question in the correct codomain:

> Is there an owner-local retained-source effect whose source contrast is fixed for every joint realization of the accepted event?

For the benchmark, yes.

This is a conditional physical-representation result, not a first-principles derivation that the benchmark encoding/channel is native.

## 2. Exact benchmark inputs

Use the accepted benchmark from p1_receiver_location_resolution/RESULT.md.

Native carrier:

    X=(o,p,u,v),    Y=(o,p,v),

with P1

    P(z_o,z_p,z_u,z_v)=(z_o,z_p+z_u,z_v).                 (1)

Physical source Hilbert space has orthonormal basis |o>,|p>,|u>,|v>. The supplied pre/post encodings are

    Pi_X(z)=sum_{i in X} z_i pi_i,
    Pi_Y(y)=sum_{i in Y} y_i pi_i,                          (2)

where pi_i=|i><i|. They satisfy, on the whole normalized simplex,

    C Pi_X = Pi_Y P,                                       (3)
    Pi_X I = Pi_Y,                                         (4)

with completed source channel

    C(rho)=Q rho Q + rho_uu pi_p,
    Q=I-pi_u.                                              (5)

Equation (4) is the benchmark's explicit physical-retention premise. It is not derived from native P1 alone.

The source pair is

    z+ = (1,1,2,1)/5,
    z- = (1,1,1,2)/5.                                     (6)

Every accepted joint isometry W implementing C, including W_R, W_E and the Bell control, has the same reduced source output C(rho).

## 3. Theorem — retained owner effect has a realization-invariant gain

Let the retained-owner effect be

    Z_p = pi_p.                                            (7)

**Theorem 1.**

(a) The Heisenberg action of the accepted event on this effect is

    C*(Z_p)=pi_p+pi_u.                                     (8)

(b) On every normalized grade z,

    Tr[Z_p C(Pi_X(z))]
      = z_p+z_u
      = (Pz)_p.                                            (9)

Thus Z_p is an exact physical representative, at the level of expectation on the declared encoding domain, of the native retained-owner coordinate q_p after P1.

(c) On the pair (6), the owner effect is initially blind:

    Tr[Z_p Pi_X(z+)] = Tr[Z_p Pi_X(z-)] = 1/5.             (10)

After the event,

    Tr[Z_p C(Pi_X(z+))] = 3/5,
    Tr[Z_p C(Pi_X(z-))] = 2/5,                             (11)

so the owner-effect contrast is exactly

    Delta_p = 1/5.                                         (12)

(d) For EVERY joint realization W of C on any complement K, the retained-source effect has the same contrast:

    Tr[(Z_p tensor I_K) W Pi_X(z+) W†]
      - Tr[(Z_p tensor I_K) W Pi_X(z-) W†]
      = 1/5.                                               (13)

Therefore W_R, W_E, Bell and every other dilation implementing the same source channel all PASS this retained-owner-effect test. Complement-unitary freedom cannot move or erase this particular source-output contrast.

**Proof.**

For any rho,

    Tr[Z_p C(rho)]
      = Tr[Z_p Q rho Q] + rho_uu Tr[Z_p pi_p].

Since p is retained and orthogonal to u, Z_p Q=Z_p and Tr[Z_p pi_p]=1. Hence

    Tr[Z_p C(rho)] = rho_pp + rho_uu
                   = Tr[(pi_p+pi_u)rho],

which proves (8). Apply to the diagonal encoding (2) to obtain (9). Equations (10)-(12) are direct substitution of (6). Equation (13) follows because tracing the complement of any implementing W gives C. QED.

## 4. Relation to the formal P1 observable pullback

receiver_process_review defines the formal output coordinate q_p^Y and its P1 pullback

    alpha_r(q_p^Y)(x)=x_p+x_u.                             (14)

On the accepted physical encoding, Theorem 1 gives the one-effect intertwining at the expectation level:

    Pi_Y(q_p^Y)  ~  Z_p,
    Pi_X(alpha_r(q_p^Y))  ~  pi_p+pi_u,
    C*(Z_p)=pi_p+pi_u.                                     (15)

Here "~" means equality of expectation values on the declared diagonal encoding domain, not a full *-homomorphism from the entire grade function algebra into B(H_S).

This is exactly the type-stage relation that T-361 kept open, but only for ONE linear owner-coordinate observable and only inside the supplied benchmark.

No RAS/RCR selector, READS table, copy gate or complementary record is required to obtain (8)-(13).

## 5. What this changes in the W_R/W_E analysis

The W_R/W_E counterexample remains valid for the separate question:

    where does the discarded fine-grained u-versus-p record live in the complement?

W_R places it in R; W_E places it in E.

But that complementary record is NOT the same object as the retained P1 owner coordinate. The owner coordinate is a source-output quantity. Its effect Z_p is fixed by the retained source representation and the reduced source channel, so it has no W_R/W_E destination ambiguity.

Thus there are two distinct outputs:

1. **Retained owner amount:** y_p=z_p+z_u. In this benchmark its effect Z_p has realization-invariant contrast 1/5.
2. **Complementary fine-grained flag:** information distinguishing how the p output arose. Its location is free under W_R/W_E/Bell without additional structure.

Conflating these produced part of the apparent receiver-location problem.

## 6. Does this solve native receiver delivery?

Not yet.

What is newly established conditionally:

    supplied physical P1 representation + event channel
       -> retained owner effect Z_p
       -> realization-invariant nonzero contrast.           (16)

What remains unearned from native first principles:

1. **Physical representation:** why the actual native retained grade is physically represented by the benchmark Pi_X/Pi_Y rather than merely mathematically encoded that way.
2. **Availability / ownership:** why Z_p belongs to the actually available observable algebra of the native owner/receiver.
3. **Preparation:** why the relevant physical/native source pair is realized.
4. **Benchmark event correspondence:** why the accepted occurring native event is physically C (or another event with the same one-effect intertwining), rather than C being a supplied illustrative channel.

However, the missing relation is now smaller than "route the complement record to R."

For this route, the next native target is:

> derive one owner-bound available effect z_p whose actual event pullback equals the native P1 owner-coordinate pullback on the relevant preparations.

A full tensor-factor receiver, complementary writer, full owner-coordinate algebra, or unique microscopic dilation is unnecessary.

## 7. Standing adversarial gate

Candidate: retained-source owner effect Z_p.

- W_R: PASS, Delta_p=1/5.
- W_E: PASS, Delta_p=1/5.
- Bell: PASS, Delta_p=1/5.
- Arbitrary implementing dilation: PASS by (13).

This is deliberately different from the previous gate. Passing all realizations is now a POSITIVE result because the effect belongs to the retained source output, not an arbitrarily nominated complement.

Falsifier: an admitted actual-event realization with the same claimed source representation for which the physical owner effect does not satisfy (8)/(9), or a source audit showing Z_p is not an available/owner-bound effect in the actual native interface.

## 8. Scientific consequence

The receiver-delivery frontier should split into:

A. **Owner-retained signal:** can an actual native owner access a retained effect representing its P1 coordinate? The benchmark shows such an effect can have a realization-invariant source contrast.

B. **Complementary history record:** where is the erased fine-grained record stored? W_R/W_E freedom remains relevant here, but this is a stronger/history question and is not required for the owner amount signal.

For the pre-time gravity program, route A is the more relevant immediate target: it asks whether a native event produces an owner-local retained scalar distinction that can subsequently participate in further P1/soft-mode dynamics. It does not require preserving the microscopic history of how that amount arrived.

No gravity, force, geometry, energy, GR/ADM, detector or fundamental-time claim follows yet.

## 9. Next exact work

Do not search for another complement writer.

Search inherited sources for either:

1. a native operational statement that the retained owner address has access to its extensive grade / a corresponding local effect; or
2. an actual event/effect correspondence sufficient to establish, for one provenance-bound effect z_a,

       Phi*(z_a) = representation of alpha_r(q_a)

   or the same equality only on the admitted source pair.

If such a source exists, combine it with Theorem 1 rather than reopening W_R/W_E destination tests.

If no source exists, the minimal missing postulate should be formulated as ONE-EFFECT OWNER AVAILABILITY / NATURALITY, not as a full complementary receiver writer.

Native bridge remains NOT_DERIVED.


## 10. Provenance and target correction — response to T-370

Added 2026-11-07 by GPT Work after inspecting Grok's T-370 response and receiver_delivery_boundary/RESULT.md §3 at dbd29ddd028737f4804ce5541e24d79a3d5a063e.

Theorem 1(d), equation (13), is the source-effect invariance already used in **RD-2, proof step 1**. The retained owner amount versus complementary fine-grained history distinction in §5 is already **RD-5**. The one-effect availability target is the owner special case of **RD-4's OA***. These are established conditional infrastructure, not a newly derived frontier advance. The earlier wording "newly established" and "what this changes" should be read subject to this explicit correction: this note reconstructs and emphasizes an existing result. It earns no new physical availability premise.

Source: [receiver_delivery_boundary/RESULT.md §3](https://github.com/proteinfoldingengine/WetLabEngine/blob/dbd29ddd028737f4804ce5541e24d79a3d5a063e/ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_delivery_boundary/RESULT.md).
Grok's challenge: [T-370](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6709726542).
Response and analytical quantifier clarification: [T-371-work](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6709805291).

There are two separate targets:

1. **Owner-effect response.** An effect available to the same owner has a forced event-induced contrast. Here pi_p is individually blind before the event and has contrast 1/5 after it, conditional on the supplied correspondence. Other available effects need not have been blind.
2. **Receiver acquisition.** The receiver's entire available initial interface is blind and becomes informative. This requires the additional E6 condition. The full source is not initially blind on the benchmark pair: its trace-distance contrast is already 1/5 before the event and remains 1/5 afterwards.

Thus the one-effect alternative in Aaron's directive can avoid an unnecessary demand for whole-interface initial blindness, but it cannot be presented as acquisition of previously unavailable information without E6. Neither target derives actual owner access.

A second distinction is between "for every realization, some effect distinguishes" and "one fixed effect distinguishes every realization." T-371-work supplies an author analytical proof that, over the full benchmark dilation orbit and the existing product-interface class, max_F min_W Tr(F D_W) equals the available retained-source contrast d_S; the same equality holds for max_F min_W |Tr(F D_W)|. It uses normalized partial trace and connectedness of the unitary orbit. Complete-complement access alone does not supply a single universal binary-effect witness even though it preserves optimal distinguishability. This does not exclude informationally complete multi-outcome measurements or effect families, and does not amend RD-4's different min_W max_F statement.

That quantifier clarification is posted for challenge, not independently reviewed or certified. It introduces no native physical premise and is not a new mechanism. The remaining native obligation remains an inherited producing operation for an owner-available effect and its actual-event action. No such producer is supplied by this addendum.
