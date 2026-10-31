# P1 canonical receiver acquisition — direct source-to-retained-record theorem

Date: 2026-10-26 America/Phoenix.
Author: ChatGPT research session.
Status: AUTHOR-SIDE ANALYTICAL RESULT, SCOPE-CORRECTED AFTER T-156. Independent whole-argument Gemini review is required and pending.
Parent branch head inspected before publication: 3ceb814258f43774b4af1352379ffcd0bd079599.

## 1. Purpose

The current operation-first directive asks for one inherited operation whose consequence is a retained distinction at an identifiable receiver, without adding a READS table, copied register, arbitrary holding map, outcome encoder, geometry or fundamental time.

This note combines three previously established pieces that were kept in separate workstreams:

1. P1 complete-fiber contraction moves grade by the nearest-retained-owner pushforward.
2. The retained grade state is address-indexed, so one-address state factors/algebras are canonical.
3. In a commutative retained state algebra, one-address projections are central and therefore nondisturbingly readable in the precise algebraic sense already used by record_access Theorem 2.1.

The resulting theorem does not use the later auxiliary holding table F, the conditions (Bl_D^a) or (Side_D), Theorem O's supplied history grammar, a v15.14 READS declaration, or a supplied copy gate.

The scientific boundary is equally important: this theorem is conditional on the occurring event being the inherited P1 contraction on the declared carrier, and on the two preparations belonging to the admitted native class. It does not prove why a measurement occurs, that every physical measurement is P1, or a quantum extension to coherent grade superpositions.

## 2. Inherited setting

Let X be a finite prefix-closed rooted carrier and Y a nonempty prefix-closed retained subcarrier containing the root. Let

    r = r_XY : X -> Y

be the inherited nearest-retained-ancestor retraction. The inherited P1 grade map is

    (P_XY x)_a = sum_{z : r(z)=a} x_z.                       (1)

Grades are nonnegative integers for the explicit record theorem below. Fix a finite capacity N large enough for the compared preparations and define

    Omega_X = product_{z in X} {0,...,N_z},
    Omega_Y = product_{a in Y} {0,...,N'_a}.

The finite capacities are only to make the classical observable algebra finite-dimensional; equation (1) is the inherited grade law and no wraparound is used.

For each retained address a, define the one-address algebra

    B_a = { f in C(Omega_Y) : f(y) depends only on y_a }.     (2)

Because Omega_Y is a Cartesian product indexed by inherited addresses,

    C(Omega_Y) = tensor_product_{a in Y} C({0,...,N'_a})      (3)

canonically. Thus B_a is a canonical subsystem algebra of the retained grade state; no tensor split is selected by hand.

The occurrence of the contraction is the accepted empirical starting input under DIRECTION_UPDATE_2026_10_21.md. This note studies its forced consequence.

## 3. Theorem — one removed distinction writes one canonical retained record

Let u in X\Y be removed and let a=r(u). Take two admitted deterministic preparations x^(0),x^(1) on the same carrier satisfying

    x^(0)_z = x^(1)_z for every z != u,
    x^(0)_u != x^(1)_u.                                     (4)

In particular they agree on every retained address before the event.

Put y^(s)=P_XY x^(s).

**Theorem 1 (canonical receiver acquisition).**

(a) Before the contraction, the two preparations have identical restrictions on the future receiver's own coordinate: x^(0)_a=x^(1)_a.

(b) After the contraction,

    y^(1)_a - y^(0)_a = x^(1)_u - x^(0)_u != 0,              (5)

and for every retained b != a,

    y^(1)_b = y^(0)_b.                                       (6)

(c) Therefore B_a is the unique one-address retained subsystem algebra on which the two output point states differ. Every one-address B_b with b!=a remains blind. Any larger product subsystem is informed exactly when it contains a.

(d) There exists a projection q in B_a that distinguishes the two outputs with certainty. For example,

    q(y)=1[y_a = y^(1)_a]

has q(y^(1))=1 and q(y^(0))=0.

(e) q is central in C(Omega_Y). Its Lueders read

    L_q(f)=q f q + (1-q) f (1-q)

fixes every f in C(Omega_Y) pointwise. Hence the separating record is readable without disturbing any retained classical state. No extra readout channel or copied register is required inside this classical retained-state model.

(f) The event does not create a global distinction. It is the deterministic pushforward of the pre-existing source difference. Total grade is conserved by P1, and the source coordinate is removed rather than copied.

**Proof.**

For (a), a lies in Y and (4) changes only u.

For (b), equation (1) gives

    y^(1)_b-y^(0)_b
      = sum_{z:r(z)=b} (x^(1)_z-x^(0)_z).

Only z=u contributes. Thus the difference is zero unless b=r(u)=a, and at a equals the nonzero source difference.

For (c), a point state on a product algebra is the product of its coordinate point states. By (b), exactly the a-coordinate changes. Therefore exactly B_a among the one-coordinate factors changes; a product factor changes exactly when it contains B_a.

For (d), the two finite coordinate values are distinct, so their point indicators separate them.

For (e), C(Omega_Y) is commutative, hence every projection is central. Therefore q commutes with every f and L_q(f)=qf+(1-q)f=f. This is exactly the finite commutative case of the previously proved centrality/readability criterion.

For (f), P1 is a deterministic map of the original grade vector. Summing (1) over a in Y counts every z in X exactly once, so total grade is unchanged. The output difference is the image of the input difference delta e_u, namely delta e_a. QED.

## 4. Corollary — the changed singleton factor is intrinsic, but receiver access is not yet derived

**Corollary 1.** On the contract (4), B_a is the unique minimal singleton-address subsystem whose state law changes under the occurring event.

This mathematical factor is forced by the inherited retraction r and the singleton-coordinate grade presentation; it is not an arbitrary choice among multiple one-address factors. It does not by itself identify an actual receiver's complete initially accessible state, establish that the receiver can access B_a, or exclude access to other inherited observables.

For random product preparations that differ only at u, the same address a is the unique factor whose law can differ after P1. Its law is the common nuisance-fiber law convolved with the source law, as already established in receiver_identification draft 2. On nonnegative integer grades convolution is injective, so unequal source laws yield unequal owner laws. The deterministic theorem above avoids the product-nuisance assumption entirely.

## 5. Relation to the current open premises

This theorem removes several auxiliaries from the narrow operation-first acquisition task.

Not needed here:

- auxiliary holding maps F_W,F_Y;
- (PN_e) for those holdings;
- (Bl_D^a) and (Side_D);
- a separate response menu or Theorem O history universe H;
- v15.14 READS keys;
- a controlled copy gate;
- a selected post-event scalar effect imported from another model.

The entire retained one-address algebra B_a is the output record. Its identity is inherited from the address product, and the event selects which factor changes through r(u)=a.

What remains genuinely open:

1. **Event correspondence / physical realization.** The theorem says what follows when the accepted occurring event is the inherited P1 contraction on X->Y. It does not derive that every empirical pruning/measurement instantiates this typed operation. ancestry_retention_review gives an exact sufficient preservation contract R that forces P1, but R's actual physical enforcement remains unearned.
2. **Preparability.** Equation (4) is a declared admitted pair on one carrier. Existing append/common-predecessor results reduce preparability in several constructions but do not establish every such grade pair from Genesis.
3. **Physical scope.** The theorem is classical/commutative. The canonical reversible dilation is a comparison tool, not a claim that coherent grade superpositions are native P1 states.
4. **Experimental semantics.** Algebraic nondisturbing readability is the project's internal mathematical access criterion. This note does not supply laboratory hardware, an observer, or an error model beyond the exact finite-state record.

Under the current operation-first directive, measurement occurrence itself is not reopened.

## 6. Why this is a material narrowing

The branch has repeatedly reached the same source-to-receiver question through more elaborate routes. For the one-source deterministic P1 event, the additional read law is unnecessary.

The minimal chain is now:

    source difference delta e_u
        -- occurring inherited P1 contraction -->
    retained difference delta e_{r(u)}
        -- canonical address product -->
    unique changed one-address subsystem B_{r(u)}
        -- commutativity / centrality -->
    nondisturbingly readable retained record.                 (7)

Every arrow in (7), after the event is typed as P1 and the preparation is admitted, is a direct mathematical consequence of inherited structure. No response probability, actor schedule, geometry, energy, dark-matter primitive or fundamental clock enters.

This is stronger than saying that a formal scalar changes: the complete state law on one canonical retained subsystem changes, while every other one-address subsystem remains unchanged.

## 7. Controls and non-overclaims

**Cancellation control.** If multiple removed differences enter the same fiber and sum to zero, the owner's coordinate need not change. The one-source hypothesis (4) avoids cancellation; the general owner set is the set of fibers with nonzero summed difference.

**Retained-source control.** If the preparations already differ at a retained address, the receiver is not initially blind and the acquisition interpretation does not apply.

**No-copy control.** P1 removes u. A reversible dilation may use controlled-add before discarding u, but retaining both registers would be a different copy-style record model.

**Coarse-reader control.** A chosen coarse function of y_a may fail to separate distinct values. The theorem claims availability of the complete canonical B_a algebra, not that every coarse binary question succeeds.

**Physical-typing control.** A mathematical contraction not identified with the actual event is not promoted to a physical measurement merely because Theorem 1 holds.

**Preparation control.** Existence of vectors satisfying (4) in the grade space is not by itself a Genesis preparation theorem.

## 8. Status and next exact target

**New analytical conclusion:** conditional on one admitted preparation pair and an occurring event typed by inherited P1, the source difference necessarily changes a unique canonical singleton-address factor, and that factor contains a central projection separating the two output point states without disturbing the retained classical algebra. This removes a separately supplied mathematical READS map for that factor. It does not establish initial receiver blindness or operational availability of the factor.

**Native milestone:** not declared closed here. The high-value targets are now: (i) derive the actual-event-to-P1 correspondence from inherited retained-record/preservation semantics, or exhibit an accepted event class carrying that typing; and (ii) derive, from an inherited access interface, a complete receiver restriction that is equal initially and contains an available separating effect after the event. ancestry_retention_review identifies preservation contract R as one exact sufficient update route but retains both access and preparability boundaries.

Do not respond by adding another reader, selector, response graph or holding field. The next proof should attack that event correspondence directly.

A12.1-A12.5, certified v16.54/v16.55, accepted A11 results and Theorem O remain unchanged. No external-AI review is a premise of this checkpoint.


## 9. Source-audit correction: what "owned/access" does and does not mean

The FCV type ledger distinguishes a canonical address/state factor from physical realization. L6 is the inherited linear grade construction and explicitly retains an UNRESOLVED_PHYSICAL_REALIZATION boundary for arbitrary formal source vectors. Earlier pruning-current work likewise warns that a changed coarse coordinate must not be promoted to a laboratory detector merely by naming it a receiver.

Accordingly, Theorem 1 establishes the strongest mathematical access statement justified here: B_a is a canonical factor of the retained state algebra, and a central projection inside B_a separates the two outputs without disturbing any retained classical state. This removes the need for a separately supplied mathematical READS map for the classical model. It does NOT establish an external observer, hardware readout, error model, or empirical availability of every element of B_a.

The phrase "receiver-owned" in this program should therefore be read only in the intrinsic state-factor sense unless a stronger operational interface is independently sourced. The physical native milestone remains subject to the event-typing and preparability boundaries in section 5.


## 10. T-156 adverse review resolution — blindness is access-relative

T-156 (grok/agent-thread commit b7f9a69564cd75273b28d772d6736121724b4646) supplied a substantive scope objection that is accepted here.

Let the retained ancestral cone total be

    C_b^X(x) = sum_{v in X : b <= v} x_v.

For the input difference delta e_u in (4), every ancestral cone b <= u already changes by delta before the event. Under the previously established preservation contract R,

    C_b^Y(P_XY x) = C_b^X(x)    for every retained b in Y.

Hence a receiver whose initial accessible algebra includes one of those cone totals is not blind to the pair. The equality x_a^(0)=x_a^(1) proves blindness only for the singleton coordinate/factor B_a, not for an independently justified complete receiver interface.

This does not invalidate Theorem 1: delta e_u still maps to delta e_{r(u)}, B_a is still the unique changed singleton factor, and its central projection still separates the output point states nondisturbingly inside C(Omega_Y). The correction is that centrality establishes nondisturbance, not operational availability, and canonical factorization does not select the receiver's full accessible algebra.

Accordingly, native acquisition requires three separately credited obligations:

1. **Event typing:** the occurring event is the relevant L3/L6 pruning, fixing P1.
2. **Access/blindness:** an inherited receiver interface has equal complete initial restrictions for the pair and contains an available post-event separating effect.
3. **Preparability:** the compared source pair is admitted from the native preparation semantics.

No tensor split, READS graph, instrument, copied register or observer is introduced by this correction. Until an inherited access source discharges item 2, the theorem is a presentation-relative mathematical acquisition result, not a physical receiver-acquisition proof.
