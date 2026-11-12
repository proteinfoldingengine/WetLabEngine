# One source edit can enable a source-specific receiver record

Author: proteinfolding-gpt. Date: 2026-10-18 America/Phoenix.
Immutable source baseline: c21a1afb9915d801a282d382faa98d802eb229ec.
Status: analytical construction awaiting independent review. Native occurrence and physical access remain OPEN.

## 1. Constructive advance

The accepted first-pruning own-view construction needs source withdrawal to finish before receiver pruning: early receiver moves can otherwise produce a false answer. Here a different common preparation makes EVERY receiver move initially inadmissible. In an episode containing at most one source edit, any receiver response consequently certifies that the source has already delivered coverage at a leaf. Native nesting forces that leaf into the source-specific branch.

The source edit is NOT restricted in advance to an addition, a leaf, or a chosen branch. All its native atomic additions and deletions are admitted. No phase controller, completion notification, target-profile return, chosen transition probabilities or new reader is introduced. The declared one-source-edit episode is load-bearing; it is not derived as a physical law.

This is a positive continuation of the existing native enabling route, not another supplied quantum channel. It removes prescribed phase ordering within its explicit episode class and gives a sound partial record even through receiver restorations. It does not derive own-view availability or actual enactment.

## 2. Existing objects and blind preparations

Use the inherited nonempty nested-support grammar. The root support is P, every child support is contained in its parent's, and a primitive adds or deletes one label at one nonroot vertex while preserving these conditions.

Let P={b,r}. The same receiver is index r. Fix a rooted tree with root o, two internal children c_0,c_1, and respective disjoint leaf sets L_0,L_1. Each c_j has d_j>=2 children and no other descendants. Thus

    T={o,c_0,c_1} disjoint-union L_0 disjoint-union L_1.       (1)

For s in {0,1}, prepare

    Y_r=T,                 Y_b={o,c_s},                     (2)
    Y_i={v : i belongs to S_v}.

Equivalently, S_o={b,r}, S_c_s={b,r}, and every other nonroot support is {r}. These are valid nested nonempty states. The source distinction is which existing internal branch contains b; the entire r-view is identical.

Both preparations come from one valid seed Y_r=T, Y_b={o}, by the single legal preparation edit +b(c_s). During these alternative preparation paths the receiver view remains T and no external label covers any global leaf. This proves relative native reachability, not physical generation of the seed.

Common reference data are T, P and the receiver role r. The receiver is not supplied the b-view, hidden support rows, a legality oracle or source-dependent reference.

Initially the receiver's bare atomic command set is empty. Addition is impossible because Y_r=T. Deletion at an internal vertex violates nesting because it has an r-child. Deletion at a leaf violates nonemptiness because its support is {r}. Equivalently, both preparations have the same interface data (Y_r,E_r)=(T,empty), in the inherited receiver_move_interface classification. Thus even a hypothetical bare command-query interface is initially blind; query feedback is not used in this construction.

## 3. The episode class, without a prescribed phase order

Consider ANY finite legal native history starting at (2), subject only to:

- at most ONE b-incidence edit after preparation;
- any number of r-incidence edits, additions or deletions;
- fixed T, P and root support.

Both labels' edits use the original grammar. The source edit may occur anywhere permitted by that grammar, or never occur. Histories may stop at any prefix. There is no lower bound on the number of events, no fairness, prescribed ordering, leaf-only event family, selected location, probability law or requirement that a receiver response occur.

The one-source-edit limit is a restriction on the episode under study. A native primitive is a one-incidence edit, but bare legality does not prevent another source primitive. Applying this result to an actual process therefore requires that its episode has the stated source-event bound. We do not implement a counter or impose an event-stopping device.

## 4. Exhaustive source-action classification and forced response

Before the one possible source edit, no r edit can occur by section 2. From (2), the COMPLETE set of legal b edits is

    -b(c_s);
    +b(c_(1-s));
    +b(l), for l in L_s.                                    (3)

Proof. The only nonroot present b-incidence is c_s; its children have no b, and r retains c_s, so its deletion is legal. An absent b-incidence can be added exactly when its parent has b. This holds for the other child of o and for the leaves below c_s, and nowhere else. QED.

The first two cases in (3) still leave every global leaf exclusively r-covered. Therefore r remains unable to act. There is no receiver response in those episodes.

If the source edit is +b(l), l in L_s, then its only external leaf coverage is l. Since Y_r remains T, the ONLY legal r edit is

    -r(l).                                                   (4)

All additions are unavailable, all internal deletions violate nesting, and every other leaf is exclusively r-covered. After (4),

    Y_r=T minus {l},           Y_b={o,c_s,l}.                 (5)

The support at l is {b}, so nonemptiness is preserved; all nesting conditions hold.

**Forced-enabling theorem.** In every episode of section 3, if a proper receiver edit occurs, the source edit must already have occurred, must be +b(l) at some l in L_s, and the first receiver edit must be -r(l). The resulting own-view record identifies s through the branch containing its missing leaf.

The theorem derives the order AND the source/receiver edit directions within this episode class. It does not infer that a source edit or receiver response actually happens. A source event at an internal vertex is a legitimate nonresponding case, not a rejected physical outcome.

## 5. All-prefix readout, including receiver additions

After (5), the source-edit allowance is exhausted. The only absent r-incidence is l, so the only possible r-addition is +r(l). No r-deletion is legal: other leaves have only r, and each internal c_j still has an r-child. This last fact uses d_s>=2. The root is fixed.

Consequently every r-only continuation alternates, possibly with early stopping, between

    T     and     T minus {l}.                               (6)

At T the only legal r edit remains -r(l), and at T minus {l} the only legal r edit is +r(l). This proves (6) for all finite continuations, without a pruning-only restriction.

On the union of all reachable receiver records, define

    d(T)=UNKNOWN;
    d(T minus {l})=s when l belongs to L_s.                   (7)

It is sound at EVERY prefix of EVERY episode, including before any source event. A restoration erases the answer to UNKNOWN; it never produces the opposite answer. No indefinite retention or irreversibility is claimed. A missing leaf is itself the mathematical response marker, so the decoder needs no separate source-completion acknowledgment or elapsed-time signal.

The receiver reads only its own current view and the same T if that interface is actually available. The construction of d is not a derivation of physical access. It does not require access to a changing global profile, source commands, event counts or other labels.

## 6. Relabelling-invariant witness and native budget

For a concrete common carrier, use d_0=2, d_1=3. It has eight vertices. The two internal branches are structurally distinguished by their arities, so s denotes the b-marked two-leaf versus three-leaf branch. The decoder can inspect the arity of the missing leaf's parent. This uses the inherited rooted structure, not a literal name, physical metric or new reference dictionary. It is invariant under simultaneous rooted-tree and palette relabellings with the receiver role carried along.

Both full initial receiver views have size eight. Every nonblank response has size seven; cardinality alone does NOT distinguish the sources. Source preparation is likewise structurally distinct although both b-views have size two.

There are explicit responding histories in both preparations: choose any l in the corresponding L_s and perform +b(l), -r(l). These are existence witnesses, not a source-blind selector or event law.

Let the reference hitting profile be q_o=q_c0=q_c1=1. Preparation and every permitted source edit preserve this profile because r is still in every child support. In state (5), the children of c_s include one support {b} and at least one support {r}, so h_c_s=2. The other branch has hitting number one and the two root children still share r, giving h_o=1. Hence

    sum_internal_v |h_v-q_v| = 0 at the blank,
                               1 at every nonblank record.  (8)

Thus the full episode class lies within the inherited total excursion <=1, including restorations. No profile constraint was used to force the response or its ordering, and no return to q is required. This is an analytical statement about these states, not a new numbered-stage certification.

## 7. Controls and scope

**The single-source bound matters.** From source 0, perform +b(c_1), then +b(l_1) for l_1 in L_1, then -r(l_1). All three edits are natively legal, but (7) would return 1. The second b edit lies outside section 3. Source 1 has the symmetric counterexample. Thus the decoder is not claimed for arbitrary interleavings with multiple source changes, even though the receiver still cannot act before leaf coverage arrives.

**Initial exclusive leaf coverage matters.** If b already covers a leaf at the beginning, r may delete there immediately. The initial inactivity argument and derived source-before-response order no longer follow. The common-seed preparations in section 2 deliberately preserve exclusive leaf coverage.

**Occurrence is not forced.** Zero edits, one internal source edit, and a leaf addition with no r-response are all admitted and leave d=UNKNOWN. No probability of response, unconditional contrast, transmission rate or universal progress is derived.

**Both directions remain native.** Later r-addition can erase the record. The soundness claim includes that erasure; it is not persistence of a known answer through all edits. Longer source histories and carrier changes require separate arguments.

**Availability is still open.** A named index and formal own-view function do not establish a receiver's actual observation algebra. Initial blindness has been proved for the complete declared own-view/bare-command interface, not for arbitrary additional physical observables or hidden-state-dependent rates.

## 8. Relation to the accepted construction and remaining target

The accepted first_pruning_own_view_review result uses source withdrawal and then a receiver phase. Its early-response control is an actual limitation: the receiver can make misleading deletions before withdrawal ends. The present construction changes the preparation and source operation class. The receiver is initially immobile; a response forces the preceding source action to be a leaf addition. We neither reinterpret the old source withdrawal nor silently extend its theorem.

The interface handoff explicitly asks for inherited coverage delivery without selecting a branch or stipulating a leaf-only event family. Equation (3) keeps ALL initial source atomic moves, including internal ones. Leaf delivery is a consequence of a response in the one-source-edit episode, not an input restriction on the source edit. The event-count restriction remains the precise tradeoff and must not be hidden.

Positive result: native compatibility can enforce an enabling order and a sound, source-specific partial record in the SAME initially blind receiver view, with no prescribed schedule, target-return guard, source completion flag or pruning-only receiver phase.

Outstanding: an actual source episode with the one-edit bound, occurrence of a receiver response, physical availability of its own view/reference, and physical seed/preparation. A positive application must establish those from the native event/record sources. This manuscript does not supply a measurement instrument, state encoder or actuator to make them true.

## 9. Review and evidence contract

This argument and its controls were developed analytically before any execution. They are disclosed findings, not prospective numerical predictions. No native simulator, finite search or archived scientific module was executed. Independent Gemini review must reconstruct (3), the initially empty receiver interface, the forced enabling order, the exact two-state continuation, the arity decoder, profile bound, and the multiple-source counterexample. It must distinguish a real removal of the prescribed phase premise from the still-explicit single-source-event bound and actual-access gap.

The packet contains exact native admissibility, receiver move classification, the accepted first-pruning argument and its interface handoff, plus the standing directive. Prior sources retain their historical status; this review is not wholesale recertification. Integrity and publication checks validate bytes and review provenance, not physical occurrence.

Time remains pruning / ordered recoverability update. No native milestone, broad C3/C4 closure, main merge, numbered-stage certification or empirical breakthrough is claimed.

