# Preparability by native support histories: common predecessor and relational witness

Date: 2026-10-17 America/Phoenix.
Author: proteinfolding-gpt.
Source baseline: 370ee194cce581890ae7c7899934795d97989256.
Status: AUTHOR ANALYTICAL CONSTRUCTION / INDEPENDENT REVIEW PENDING.
No new mechanism code, numerical campaign, physical closure or numbered-stage certification.

## Purpose and scope

The user approved investigating whether the two initially receiver-blind source cases can be generated using existing primitives. This note constructs them in the inherited finite nested-support category, supporting the existing source-withdrawal candidate. It establishes relative admissible reachability, not physical occurrence of preparation. It does NOT establish preparability of arbitrary scalar grades or quantum states in the pruning-ledger/pinching construction.

The useful advance is an explicit common preparation prefix and two finite native continuations. The two endpoints differ relationally, even after simultaneous palette relabelling. Receiver support stays literally fixed throughout preparation.

## 1. Inherited objects

A fixed finite rooted tree T, root o, and finite palette P carry nonempty supports S_x with S_o=P and S_child subset S_parent. A primitive adds or deletes one label at one nonroot vertex while preserving these relations. No simultaneity, scheduler, probabilities, physical time or new label is added.

These are the bare admissibility primitives, not a physical actuator. A hitting-profile budget is an additional condition; where one is preserved below it is proved explicitly.

Source documents at the baseline:

- demos/v16.53-four-child-boundary/NATIVE_ADMISSIBILITY.md, blob ebc315f7f2f6423fe9f6861cc3b8a0cfcf8420f2.
- research/physical-bridge/receiver_move_interface/RESULT.md, blob 0371d4a8aa66ce02ffbda084ad5dde93f1ec1136: exact addition/deletion preconditions.
- research/physical-bridge/source_withdrawal_completion/WORKING_CONSTRUCTION.md, blob de34b95825345662fb9df1748e671acc7961ffaf: source-withdrawal completion and vertex-support interface.
- research/physical-bridge/STANDING_DIRECTIVE.md, blob 35ac66d715f9a60edc53fbdd72a192da39f7b76e: construction first, no supplied channel, actual access/occurrence distinguished from admissibility.

Paths above are relative to ResearchHistory/UQCF-GEM/.

## 2. General common-predecessor lemma

Let D be a descendant-closed set of nonroot vertices: if x belongs to D, all descendants of x do too. Fix a in P. Consider any target native state S satisfying

    S_x = {a} for every x in D.                                  (1)

Define a common state M_D independent of the target:

    (M_D)_o = P;
    (M_D)_x = {a} for x in D;
    (M_D)_x = P for other nonroot x.                             (2)

This is native: no edge leaves D toward its complement, and all remaining containments are immediate.

**Lemma.** Every target satisfying (1) is reachable from M_D by deletion-only native edits outside D, with D unchanged throughout. A path has exactly

    L(S) = sum over x outside D, x != o of (|P| - |S_x|)          (3)

edits, and this length is minimal among all one-incidence paths from M_D to S.

**Proof.** Process vertices outside D in child-before-parent order. At x delete each label in P minus S_x. Children outside D have already reached their target supports, contained in S_x; children inside D already have their target support {a}, also contained in S_x. Thus no child contains a deleted label. Every intermediate support at x contains the nonempty target S_x. Its parent either remains P or is the fixed root P; a parent in D is impossible by descendant closure. Each deletion is therefore native. Each unwanted incidence is removed once. Any one-incidence path must change every differing incidence at least once, giving the lower bound (3). QED.

Consequently any two target states satisfying (1) have a common native predecessor and preparation paths with the entire receiver cone D unchanged. This is an elementary reachability deduction, not a claim of mathematical priority or an inferred execution law.

The lemma does not preserve an arbitrary hitting-profile budget. The explicit pair below does preserve the all-one profile throughout preparation.

## 3. Small pair with a common preparation history

Use T with root children u,z, and u's child v:

    edges: (o,u), (o,z), (u,v);
    P = {a,b0,b1}.

Here u is the source, v the receiver, and z a common reference branch. The shapes distinguish u from z even without ordered sibling labels.

Begin at the common native seed B:

    S_o=P; S_u=S_v=S_z={a}.                                    (4)

Use this same preparation prefix in both cases:

    +b0(z), +b0(u), +b1(u).                                    (5)

After (5), call the state H:

    S_o=P; S_u=P; S_v={a}; S_z={a,b0}.                          (6)

Each addition is allowed because its parent is o with full palette P. v remains {a}; no change there is needed.

Now branch by one primitive:

    H -- -b1(u) --> F0: S_u={a,b0};
    H -- -b0(u) --> F1: S_u={a,b1}.                             (7)

The deletions are legal because the only child v contains neither b0 nor b1, and a remains at u. All other supports stay as in (6). Thus the two states used by the source-withdrawal construction have explicit native preparation histories from one common seed.

Throughout (4)-(7), v has exactly {a}. Any record consisting of this row and common fixed reference data is identical between the two histories, including its own support history. During the common prefix reference changes are also identical in both histories. No legality oracle, global-state access, event receipt or source-dependent timing record is granted to the receiver.

At u, the sole child is nonempty, so h_u=1. At o both child supports contain a throughout preparation, so h_o=1. Preparation therefore preserves the all-one profile exactly.

This construction uses the general native category, which permits unary vertices. It does not extend a separately restricted arity theorem.

## 4. The distinction is relational, not only a name swap

The added reference branch is common in both preparations and is itself constructed by the same primitive prefix. It carries no branch-specific input.

At the prepared endpoints,

    |S_u(F0) intersection S_z| = 2;
    |S_u(F1) intersection S_z| = 1.                            (8)

Intersection cardinality is invariant under every simultaneous palette permutation. The rooted-tree shape fixes u,z,v. Hence F0 and F1 are inequivalent even after allowing arbitrary global palette relabelling and rooted-tree automorphisms.

In the smaller chain without z, swapping b0 and b1 can exchange the two unlabelled states if all label references are forgotten. Equation (8) prevents that issue in this witness. If the framework fixes ordered palette labels already, no such enlargement of equivalence is necessary, but the stronger check is useful.

Equation (8) is a full-state invariant used to prove distinctness. It is NOT granted to the initially blind receiver, since it depends on S_u. Including only the common reference S_z in a proposed receiver interface does not include (8).

## 5. Join preparation to the existing completion consequence

From either F_s, the same specified source withdrawal is -a(u). A native completion is

    +b_s(v), -a(v), -a(u).                                    (9)

The first edit is legal because b_s belongs to S_u; the second preserves nonemptiness; the third is legal after the child no longer contains a. The reference branch is unchanged.

Every lawful immediate endpoint of that source withdrawal, when its source input is {a,b_s}, must satisfy

    empty != S_v subset {b_s}, hence S_v={b_s}.                 (10)

This is the existing completion theorem applied to the now explicitly reachable pair. It does not say that -a(u) is enabled at F_s: the child adjustment must precede the source commit.

A relational endpoint discriminator, if access to v's support and the common reference is justified, is

    q = 1[S_v intersection S_z is nonempty]:
    q(F0 after completion)=1;
    q(F1 after completion)=0.                                 (11)

Initially S_v={a}, so q=1 in both cases. To distinguish blank from a completed signal, retain the common blank reference {a}; a decoder returns blank when S_v={a}, and on the forced singleton endpoints uses (11). No claim is made that this decoder handles arbitrary other histories without a declared input contract.

The source-withdrawal theorem supplies the endpoint implication; it still does not supply a blind execution policy. The first receiver edit in (9) is branch-indexed and no common nontrivial receiver edit is initially legal. No choice rule or probability is inferred.

The marker version is in the bare category. After completion in branch 1, S_u={b1} and S_z={a,b0} are disjoint, so h_o=2. Thus the all-one-profile statement applies to PREPARATION, not to the complete interaction with this marker. This note does not claim fixed-profile interaction closure. The original marker-free all-one completion remains at its original labelled scope.

## 6. What this resolves and what remains

| Obligation | Result |
| --- | --- |
| Both support states are legal | Directly verified |
| Both reachable from one common native seed | Explicit four-edit preparation histories |
| Receiver support unchanged throughout preparation | Exactly {a} throughout |
| Difference survives palette relabelling | Intersection invariant 2 versus 1 |
| Preparation preserves all-one hitting profile | Yes |
| Same source-event identity in both cases | -a(u) |
| Committed event forces receiver endpoint | Existing completion implication, equation (10) |
| Common seed is physically realized | Not derived |
| Preparation branch occurs or has positive probability | Not derived |
| Source event commits | Not derived |
| Receiver owns/reads its row and reference | Not derived |
| Numerical grade or quantum-pair preparability | Not established by support reachability |
| Genesis certificate for these actual histories | No certificate-generation law derived |
| Independent acceptance | Pending |

The shared seed (4), fixed carrier and palette are still declared native input objects. Replacing two arbitrary starting cases by one common seed and explicit paths is a reduction of the preparability obligation; it is not creation from Genesis alone.

A preparation question has at least three levels: state admissibility; reachability under inherited moves from a specified common seed; actual generation under a justified event law. This note earns the second for this support witness. It must not be reported as having earned the third.

For the pruning ledger, a further typed map would have to carry these support histories into the required grade-functional or pinching-state histories while preserving common references, initial blindness, and the relevant update. No such map is assumed here. In particular, support cardinality must not silently become a physical scalar grade, and a support label must not silently become a quantum basis projector.

## 7. Next precise task and review questions

First seek a native realization of the common seed and the preparation edits, using the existing event/provenance binding at its actual type. A full arbitrary-state preparation theorem is unnecessary: this one pair suffices for the support candidate.

The first independent review should reconstruct (2)-(3), (4)-(8), and their composition with the existing completion theorem; test whether the initial receiver interface leaks the branch; challenge the gauge claim; and retain the explicit seed/enactment/access and grade-bridge limitations. The raw mathematical draft is now available for that review. No scientific execution or review verdict is claimed in this note.

No new mechanism was coded.
