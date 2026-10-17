# Preparability: exact three-manuscript review collection

Author drafts; no independent acceptance claimed. Each manuscript below is copied verbatim from the immutable baseline. Earlier ledger acceptance does not cover these drafts.

---

Source: ResearchHistory/UQCF-GEM/research/physical-bridge/source_withdrawal_completion/PREPARABILITY_COMMON_PREDECESSOR.md
Git blob: 7f429b0499a50000b004cb9e5c30f63e676e6334

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

---

Source: ResearchHistory/UQCF-GEM/research/physical-bridge/constructions/preparability_branch_split/CONSTRUCTION.md
Git blob: 23bd3638ca637d814ac0ebb4d26083c4e42b3603

# Construction: preparability as native reachability by a pinned branch split (draft 1)

Author: proteinfolding-grokbot (UQCF Science Agent).
Date: 2026-10-17 America/New_York.
Mode: CONSTRUCTION MODE (STANDING_DIRECTIVE addendum (b)); Aaron's 2026-10-17 17:45 ET preparability directive (G as native reachability, not an external preparer).
Base: the frozen, Gemini-ACCEPTED [recoverable pruning ledger](../recoverable_pruning_ledger/FROZEN_ARGUMENT.md) (freeze `0fbea1c3`, review run 39070100916, native_bridge NOT_DERIVED). Notation (carrier tree, retraction \(r_j\), fibers \(F_j(t)\), shells \(A_l(t)\), readings \(R_{\min}<R_{\mathrm{inc}}^-<R_{\mathrm{full}}\)) is that document's.
Status: REVISED analytical draft; fresh independent review pending. Draft 1 received REVISE in run 39075699709. This revision narrows native-admissibility wording and additionally clarifies scalar-record, zero-grade and ordering scopes. No milestone, no CLOSED status, no preparation mechanism in code. No geometry, clock, dark-matter primitive or fitting. Time = pruning / ordered recoverability update.

---

## 0. Result first

The ledger's Witnesses A–D *wrote down* two source assignments. Here both histories are explicitly specified as tree extensions of one prefix \(P\). Their native admissibility and reachability are CONDITIONAL on the unproved semantic append premise N; Genesis hash-chain validation does not establish N. The receiver identity (its pinned ancestry path) and its initial accessible record are identical in both, because append-only extension leaves every entry of \(P\) unchanged. One common inherited operation \(\Omega\) (a fixed sequence of subtree retractions on addresses of \(P\)) then gives distinct receiver records. The exact criterion (Theorem 2.2) is that the two appended entries reach the receiver's fiber at different pruning steps.

Two witnesses come out of it:

- **W1 (inside vs outside).** One extra entry is appended either inside the receiver's future fiber or outside it. The two sources are distinct as pinned trees (no relabeling maps one to the other), the global total grade is equal, and the receiver separates them even under \(R_{\min}\). This works for **every** common operation that eventually retracts the inside branch into the receiver, including any content-covariant forced order.
- **W2 (Aaron's grade pair \((g,h)\) vs \((h,g)\)).** The extra entry is appended under sibling \(u\) or sibling \(v\). Both histories are exhibited, with equal total grade, the same receiver and the same initial record. They are separated under \(R_{\mathrm{inc}}^-\) by the common order "retract \(u\) then \(v\)", and not by any order derived covariantly from content (Proposition 3.2). This sharpens G against premise (2): **a fully forced, content-equivariant pruning order destroys the symmetric swap witness**. Forcing the *occurrence* of pruning, and the order of comparable (ancestor-related) retractions, does not.

What stays assumed is **N**, the Genesis-Pin legitimacy of append-only extensions that does not depend on where the append lands (§1). Access A/R\(_{\mathrm{inc}}^-\) is inherited open from the ledger. G is upgraded from *assumed preparation* to *exhibited reachability conditional on N*. It is not closed.

## 1. Native ingredients

Inherited and earned (cited, not re-proved):

- **E-pin.** Genesis Pin (V997 claim boundaries; V994 minimality): legitimacy is a property of the *history*. It requires a pinned registry and anchor root, quorum witness participation, append-only continuity and no circular bootstrap. After genesis, updates are governed recursively. v15.08: it certifies history legitimacy, not a reference state. v13.23 / site: it is "a ledger, not a selector".
- **E-addr.** Stable addresses \(r_{XY}(t)=t\). An entry's address is its pinned ancestry path. Append-only extension changes no existing address or grade.
- **E-ret.** Ledger P1/P2: closed ancestral retractions, fiber pushforward to the nearest retained ancestor, \(x=E_m x+\sum_l D_l x\), and Theorem 11.1 (owner record = pushforward onto block / shells / singletons). Theorem 11.5 (global nonincreasing, receiver nondecreasing) holds for any **fixed, source-independent** retraction sequence.
- **E-anc.** v15.10 intrinsic ancestry order. v15.13: incomparable events commute, and dependency arrows are declared. The only order constraint on retractions is ancestry (a descendant is removed no later than its ancestor). This is exactly the frozen ledger's class of closed pruning sequences.

Premise used here (not derived):

- **N (pinned append legitimacy, location-free).** (N1) Admissible histories are append-only extensions of a Genesis-pinned prefix satisfying the E-pin conditions. (N2) The E-pin conditions do not refer to the parent location of an appended entry: if appending an entry of type \(\tau\) (grade \(w>0\)) under \(\ell\in P\) is legitimate, so is appending the same type under any \(\ell'\in P\). (N3) At least one legitimate append beyond \(P\) exists. N1 is the inherited definition. N2 is an additional semantic-permission hypothesis, NOT a deduction from "ledger, not selector" or from absence of a location field in the V997 validator. N3 is witnessed in the V997 toy, where quorum and witnesses are supplied.

**Reachability vs emission.** G as reachability is the *modal* claim that both histories are admissible. It is not the *causal* claim that some native law emits one of them. The earlier append-only provenance screen (`73d78836`) found the causal version needs a native emission law \(P_{\mathrm{emit}}\), which is still missing. This construction needs only N, not \(P_{\mathrm{emit}}\).

## 2. Branch-split histories and the separation criterion

**Setup.** Take a pinned prefix tree \(P\) with root \(o\) (the pin anchor), nonnegative grades \(x\) on \(P\), and a receiver \(a\in P\setminus\{o\}\). For \(\ell\in P\), let \(T_\ell=P\cup\{e\}\) with \(e\) a new leaf under \(\ell\) of grade \(w>0\). Conditional on N, every \(T_\ell\) is admissible, anchored to the same pin; these are not yet certified native append histories.

**Lemma 2.1 (blind start, same identity).** For all \(\ell,\ell'\): \(a\)'s address, grade and fiber \(F_0(a)=\{a\}\) are identical in \(T_\ell\) and \(T_{\ell'}\). So the receiver's initial accessible record, under any reading, is the same.
*Proof.* E-addr: append-only extension changes no existing entry, and \(e\notin F_0(a)\). ∎

**Common operation.** \(\Omega=(p_1,\dots,p_m)\) with \(p_j\in P\), and \(a\) not in any subtree of a \(p_j\). Step \(j\) retracts the currently retained part of the subtree at \(p_j\) into its nearest retained proper ancestor. This is a closed ancestral retraction (E-ret, E-anc). It is written in addresses of \(P\) only, so it is the *same* operation on every \(T_\ell\), and it is source-independent as Theorem 11.5 requires. The appended leaf goes with its parent's subtree.

Define the **arrival step** \(s_a(\ell)=\min\{j:\ e\in F_j(a)\}\in\{1,\dots,m,\infty\}\).

**Theorem 2.2 (separation criterion).** Under \(\Omega\), with \(w=w'\) (same entry type):
1. (\(R_{\mathrm{inc}}^-\), raw) \(a\)'s records on \(T_\ell, T_{\ell'}\) differ iff \(s_a(\ell)\neq s_a(\ell')\).
2. (\(R_{\min}\), at step \(j\)) they differ iff exactly one of \(s_a(\ell), s_a(\ell')\) is \(\le j\).
3. (\(R_{\mathrm{inc}}^-\), projective, GPT's ratio contract) if both arrival steps are finite, the records differ projectively iff \(s_a(\ell)\neq s_a(\ell')\). If exactly one is finite and the base shell-sum vector has positive total M, they differ projectively unless that base vector is supported on the arrival shell alone. If M=0, the outside case is zero and has no positive projective ray; no two-ray comparison is asserted.

*Proof.* Theorem 11.1 with additivity of the pushforward: the shell-sum vector of \(a\) on \(T_\ell\) is \(\mathbf w_P+w\,\delta_{s_a(\ell)}\), where \(\mathbf w_P\) is the vector for \(P\) and \(\delta_\infty=0\). That \(e\)'s grade enters exactly one shell, at its arrival, follows from fiber pushforward: before \(e\) is removed its owner is \(e\); afterwards its owner is \(r_j(e)\), and fibers only merge. Parts (1) and (2) are immediate. For (3), two vectors with equal positive totals are proportional iff they are equal. With unequal totals \(M\) (for \(s=\infty\)) and \(M+w\) (finite \(s\)), proportionality means \(\mathbf w_P+w\delta_s=\lambda\mathbf w_P\) with \(\lambda=(M+w)/M\), i.e. \((\lambda-1)\mathbf w_P=w\delta_s\), so \(\mathbf w_P=M\delta_s\) is supported on shell \(s\) alone, which is the stated exception. ∎

**Ledger point (Theorem 11.5 applies).** The source variable \(S=\ell\) is fixed at the split, and \(\Omega\) is source-independent. So global distinguishability of \(S\) is nonincreasing along \(\Omega\), while, when the arrival steps differ, the raw retained-history record at \(a\) rises from 0 (Lemma 2.1) to 1 bit at their first finite arrival under a balanced prior. Equal arrival steps give no acquisition from this pair. **The receiver gains information by redistribution, and none is created globally.** The bit was in the ledger from the split, as the location of an append. Pruning relocates it into the receiver's fiber.

## 3. The two witnesses

Use unit (counting) grades for display. Theorem 2.2 needs only \(w>0\) and equal type. Take \(P=\{o,a,u,v\}\) with \(a\) under \(o\), \(u,v\) under \(a\), receiver \(a\).

**W1 (inside vs outside).** Sources \(T_u\) (append under \(u\)) and \(T_o\) (append under \(o\)). No pinned isomorphism fixing \(o,a\) maps one to the other: the appended entry sits at depth 3 vs depth 1. So the distinction is native and gauge-invariant. The global total grade is equal (5 = 5). With \(\Omega=(u,v)\), \(a\)'s cumulative history is \((1,3,4)\) vs \((1,2,3)\), so \(s_a(u)=1\) and \(s_a(o)=\infty\). It separates under \(R_{\min}\) at every step \(\ge1\), and under \(R_{\mathrm{inc}}^-\) raw and projectively.

**Proposition 3.1 (robustness).** For any common \(\Omega\) that eventually retracts \(u\)'s subtree with \(a\) retained, \(s_a(u)<\infty=s_a(o)\). This includes every content-covariant forced rule, provided it does this in both histories. So W1's separation does not depend on how the order arises.

**W2 (Aaron's grade pair).** Sources \(T_u\) and \(T_v\). By N2 they come from the same pinned prefix, are equally legitimate, and have the same receiver and the same initial record. With counting grades, the sibling-branch grades are \((g,h)=(2,1)\) vs \((h,g)=(1,2)\). Generally they are \((x_u+w,x_v)\) vs \((x_u,x_v+w)\), an exact swap iff \(x_u=x_v\). Both histories are explicitly specified, with admissible reachability still conditional on N. With common \(\Omega=(u,v)\): \((1,3,4)\) vs \((1,2,4)\). \(R_{\min}\) at the end is \(4=4\), not separated. \(R_{\mathrm{inc}}^-\) separates, with projective ratio \(q=2/3\) vs \(1/3\). With the simultaneous step \(\Omega=(\{u,v\})\), \(s_a(u)=s_a(v)\), so W2 is not separated (Theorem 2.2).

**Gauge.** The pinned automorphism \(\sigma\) (swap \(u\leftrightarrow v\), fix \(o,a\)) maps \(T_u\) to \(T_v\), so the two *sources alone* are gauge-equivalent. The *histories* \((T_u,\Omega)\) and \((T_v,\Omega)\) are not: \(\sigma(T_v,(u,v))=(T_u,(v,u))\neq(T_u,(u,v))\), and \(\sigma\) is the only nontrivial pinned automorphism. The gauge-invariant source distinction in W2 is therefore relational: *whether the append landed in the first-retracted or the second-retracted sibling branch*. The receiver acquires a fact about content relative to pruning order, that is, temporal-order information. This answers Aaron's symmetry condition. \(\sigma\) is admissible (N2, E-addr: sibling indices are chart, not provenance), and the two cases stay distinct modulo \(\sigma\) once the common operation is included.

**Proposition 3.2 (covariant-order collapse).** Suppose the retraction order is a function of content, \(\Omega=\Pi(T)\), equivariant under pinned automorphisms: \(\Pi(\sigma T)=\sigma\Pi(T)\). Then for every \(\sigma\) fixing \(o\) and \(a\), the receiver's record on \((T_{\sigma\ell},\Pi(T_{\sigma\ell}))\) equals that on \((T_\ell,\Pi(T_\ell))\) for scalar coarse-grade and shell-sum histories. A full address-bearing record is generally equivariant, not literally equal; equality for it is asserted only after passing to relabelling-invariant observables. In particular, W2 is never separated by such a rule.
*Proof.* \((T_{\sigma\ell},\Pi(T_{\sigma\ell}))=\sigma\,(T_\ell,\Pi(T_\ell))\). Records are indexed by step and by \(a\)'s address, both fixed by \(\sigma\). ∎
Example: "smaller branch first" gives \((1,2,4)\) on both, and "larger first" gives \((1,3,4)\) on both.

**Corollary 3.3 (G vs (2)).** For the specified symmetric swap pair under N, existence of both source/common-order combinations corresponds to admissibility of the two corresponding orders on one source. This is a statement about the declared abstract history class, not a general equivalence between native preparability and order contingency. Given N2-covariance, \((T_v,(u,v))\) is admissible iff \((T_u,(v,u))\) is. So the pair is reachable with a common operation iff both orders of the incomparable retractions are admissible for the same content. The abstract closed-retraction class permits these orders when ancestry allows them. This does not certify their occurrence or semantic permission in an actual pinned history. Selector nonuniqueness supplies neither such permission nor N. Constructive guidance for (2): derive that pruning **occurs**, for example from finite capacity, and the order of **comparable** retractions, but do **not** fix the order of pinned-symmetric incomparable retractions from content. Doing so would make this scalar-record W2 discriminator blind under that rule; it does not prove the source states themselves unpreparable. W1-type distinctions survive any forced order (Proposition 3.1).

## 4. Mission ledger after this draft

| Ingredient | Status |
| --- | --- |
| Native distinction | W1: location of a legitimate append (pinned-tree invariant). W2: append location relative to the common order. **EXHIBITED** as admissible histories, conditional on **N** |
| Preparability G | Upgraded from ASSUMED to **REACHED CONDITIONAL ON N** (modal). Causal emission \(P_{\mathrm{emit}}\) not needed and still open. **Not closed** |
| Update rule | Retraction: EARNED (ledger). Common \(\Omega\): admissible by E-anc, **SUPPLIED** as a choice. Occurrence SUPPLIED |
| Retained consequence | Shell arrival (Theorem 2.2): EARNED from ledger Theorem 11.1 |
| Receiver identity / access | Identity = pinned ancestry path, the same in both (Lemma 2.1). Reading the record: **A / R\(_{\mathrm{inc}}^-\) NOT DERIVED** (W1 needs only present-record access with a fixed unit; W2 needs the own history) |
| Separation | EARNED: Theorem 2.2, Propositions 3.1–3.2 |
| Ledger point | EARNED: Theorem 11.5, redistribution of the split bit |

## 5. Honest novelty

The mathematics is elementary: additive pushforward on a tree. Known analogues are alternative histories from a common past (decoherent/consistent histories), which treat preparation as the past branch rather than an external agent; the data processing inequality, which gives global nonincreasing under a fixed source-independent \(\Omega\); and which-path/ordering information. No claim is made against these. What is new for the program:
1. G is restated as **modal reachability** inside the pinned ledger, separated from causal emission. That removes the dependence on \(P_{\mathrm{emit}}\).
2. The exact separation criterion is **arrival-step inequality** (Theorem 2.2).
3. The **covariant-order collapse** (Proposition 3.2 / Corollary 3.3) shows the two open premises constrain each other. A content-equivariant order rule would make this symmetric witness's scalar receiver records coincide; that is a separation restriction, not a source-preparability theorem. So the arrow to derive is "occurrence plus comparable order", not "total order".
4. **W1** is a gauge-invariant preparable distinction whose transfer is robust to how the pruning order is eventually derived.

**Relation to proteinfolding-gpt's `86390b26`** ([PREPARABILITY_COMMON_PREDECESSOR.md](../../source_withdrawal_completion/PREPARABILITY_COMMON_PREDECESSOR.md), committed during this run and credited here). That note earns level 2 of its three-level hierarchy (admissibility, reachability from a common seed, actual generation) for the *nested-support* witness: support edits from a common seed, receiver support fixed, palette-invariant intersection \(2\) vs \(1\). It explicitly leaves open the pruning-ledger *grade* case and any typed map into it. The present draft is that complementary case, built natively in the ledger's own carrier with no support-to-grade map. Here the common predecessor is the pinned prefix \(P\) and the branch primitive is a legitimate append (N). This draft also reaches level 2 only, conditional on N, and does not claim level 3. The two gauge treatments match: in both, distinctness is proved by a relational invariant that is not granted to the blind receiver (there, intersection with the reference branch; here, append location relative to \(\Omega\)).

## 6. Exploratory check (not evidence)

Scratch script `/tmp/prep/chk7.py`, not committed, no preparation mechanism. Random trees with 3–8 atoms, random common \(\Omega\), all append-location pairs: 27868 pairs, 0 violations of Theorem 2.2(1). W1/W2 histories reproduced as above. Independent producer/checker verification follows the freeze, per construction mode.

## 7. Next

(a) Draft 2: replace the supplied common \(\Omega\) by a capacity-forced occurrence (finite retained capacity \(K\) forces removal once the append exceeds \(K\)). Test whether the forced set of removals, with contingent order among incomparables, still separates W1 and W2. This is premise (2) restricted to occurrence.
(b) Tie N2 to the V997/V994 pin conditions line by line, so N is cited rather than read in.
(c) Then freeze, preregister, run producer and checker, and send to Gemini via Actions.


## GPT extension: two locations and complete-fiber endpoint (2026-10-17)

[TWO_LOCATION_EXTENSION.md](TWO_LOCATION_EXTENSION.md) traces the original V997 validator and separates syntactic certificate continuity from semantic parent-location permission. W1 needs only two certified append locations, not universal N2. Complete contraction of the receiver's strict descendants gives order-independent present-state contrast using a common root reference, including when the outside entry is removed. This explicitly changes the proposed readout to a receiver/reference pair; its access, append semantics and actual contraction remain open. Author analytical extension; independent review pending. Original draft claims are preserved above, not recertified by this link.

---

Source: ResearchHistory/UQCF-GEM/research/physical-bridge/constructions/preparability_branch_split/TWO_LOCATION_EXTENSION.md
Git blob: fa21d2462659d793e55f407723a6bc3123d73d97

# Two-location preparation and order-independent present-record contrast

Date: 2026-10-17 America/Phoenix.
Author: proteinfolding-gpt.
Baseline: 2e2023aeef8ad63d286aa9fdc0f7a1156f4aa88a.
Status: AUTHOR ANALYTICAL EXTENSION / INDEPENDENT REVIEW PENDING.
Extends Grok's CONSTRUCTION.md draft 1 (blob 888e8b754da10641c42dc6c1592948e0c307975a). No mechanism implementation or scientific execution.

## Positive construction

Grok's inside-versus-outside witness can be strengthened in two ways:

1. It needs only two legitimate append locations, not location-free append legitimacy.
2. With complete collapse of the receiver's strict descendants and a common retained root reference, the resulting present-state ratio distinguishes the two cases independently of the pruning order. It does not require a history log or a chosen order between incomparable branches.

These are conditional deductions. The original Genesis audit earns certificate continuity for supplied events, not permission to append at either carrier location. That missing typed link is identified below using the original implementation rather than its prose description.

## 1. What the original Genesis implementation actually earns

Inspected at the baseline:
- Tmp/TOE/Einstein 4/v997_genesis_pin_publication_audit/v997_genesis_pin_publication_audit.py, blob 282b08b79b82be65391e1251a97891ad9c742b2f.
- Its v997_genesis_pin_outputs/CLAIM_BOUNDARIES.md, blob 8ce06f173a949fb36ca9219d902583238868996b.
- ResearchHistory/UQCF-GEM/demos/v15.56-response-selector-obstruction/source_binding.py, blob a1df8db6c1d1b3fd4491a5f502267841725f3f32.
- ResearchHistory/UQCF-GEM/foundational-closure-verification/PROOFS.md, blob a21acad73c80cb748f2e42c244f6db53146c2bf2.

V997 defines chained_transition(prev_root, registry, step, event, witnesses). The transition hashes those supplied fields. validate_append_only_chain reconstructs them successively from the pinned root. Registry equality, root equality, witness quorum and absence of modeled circular bootstrap are checked separately. build_path also checks a supplied/generated final visible-state condition.

**Certificate extension lemma.** Take a prefix with equally many events and witness sets, exactly one more root than events, and all its checks satisfied. Append a supplied event string E, a quorum-valid witness set W, and the root

    r_next = chained_transition(r_last, registry, n+1, E, W).   (1)

Then the extended hash chain passes validate_append_only_chain; all prior roots remain unchanged, registry/root checks are unchanged, and all witness-quorum checks pass. If the separate visible-state condition remains true, the conjunction used by build_path accepts it.

Proof: the first n validation iterations reproduce the old prefix; the final iteration is exactly (1). No hash collision assumption is needed for this validation identity. This lemma concerns syntactic consistency, not security or occurrence. Equal event/witness lengths are an explicit precondition; it does not generalize from zip truncation.

There is no carrier tree, parent-location parameter, grade, semantic append permission, or event-to-tree action in those functions. The hash predecessor is the previous chronological ledger commitment; it must not be identified with the parent of a new carrier vertex. An event string could encode a location, but such an encoding and its interpretation are not supplied by this validator.

Thus the implementation positively supplies a common-prefix certificate-extension procedure for supplied events and witnesses. It does NOT by itself prove that changing a tree parent preserves native legitimacy. Lack of a location check is not a semantic permission theorem.

The v15.56 binding supplies the distinct type

    source_event -> (genesis_id, full_lineage_address).

It explicitly earns no amplitude. It classifies the fields of an already certified binding; it does not construct the binding, certify an append operation, or show that the addressed vertex is the parent of a newly generated entry.

## 2. Replace universal N2 by a two-location obligation

Let P be the common finite prefix carrier and a its retained receiver. Let tau be an entry type with equal positive grade w in both preparations.

Write L(P,tau) for the set of parent locations for which an actual inherited semantic append certificate exists. This is notation for the unresolved domain, not a newly declared primitive or a computed set.

The needed obligation is only

    u belongs to L(P,tau), o belongs to L(P,tau),               (2)

where u is a strict descendant of a and o is the common root outside a's subtree. Fresh child addresses are required in both cases. Both append operations preserve old entries and grades, and have the same type/grade contract.

Universal location freedom is sufficient but unnecessary. A candidate proof of (2) should exhibit two certificates and their semantic validation rule. The certificate-extension lemma can then preserve their common pinned ancestry. No assertion that L contains either location is made from the current sources.

This is the precise separation:
- ledger chain continuation: derived at the syntactic model level;
- semantic permission and typed effect at the two locations: open;
- occurrence and accessible receiver output: open.

Grok's statement that lack of a selector supplies all alternate orders or placements must not replace (2). Nonuniqueness of a selector does not alone establish permission for a specified alternative.

## 3. Complete-fiber contraction removes the order choice

Take P={o,a,u,v}, with a below o and u,v below a. The base grades are c>0 at o, alpha>0 at a, beta>=0 at u and gamma>=0 at v. Put

    A = alpha + beta + gamma > 0.                              (3)

Preparation I appends an entry e of grade w>0 below u.
Preparation O appends an entry f of the same grade w below o.
This is Grok's W1, subject to the two-location obligation (2).
Total initial grade is c+A+w in both cases.

The proposed receiver record is the pair of present grades at a and o, modulo a common positive scale. This is an explicit extension from a single-owner scalar to a receiver/reference pair; access to both coordinates is an OPEN premise. It is not inferred from knowing the root's address.

Initially the pair is (alpha,c) in both preparations. The receiver is blind on this interface, even projectively.

Consider ANY finite sequence of inherited ancestral retractions satisfying:
- o and a remain retained throughout;
- at its terminal state all strict descendants of a are removed;
- in preparation O, f may either remain retained or be removed into o.

No sequence of intermediate removals, ordering between u and v, or history-storage architecture is prescribed.

By FCV P1 composition, the terminal pushforward equals the direct retraction to its terminal retained set. Therefore the final receiver/reference pairs are

    I: (A+w, c);
    O: (A, c) if f remains;
       (A, c+w) if f is removed.                              (4)

Every atom originally below a maps to a at this endpoint. An outside atom cannot map into a: its ancestry does not contain a. Removal of f instead maps it to o. These statements use actual prefix ancestry, not a proposed current or channel.

Consequently the present-state ratios obey

    q_I = (A+w)/c > A/c >= q_O.                                (5)

The separation holds for any positive w, without an external absolute scale. It survives all admissible intermediate orders and either fate of f. There is no history log in (4)-(5). For counting grades c=alpha=beta=gamma=w=1:

    initial q = 1 in both;
    final q_I = 4;
    final q_O = 3 or 3/2.                                     (6)

The common threshold A/c is part of the declared comparison contract. Pairwise separation itself does not assume the receiver was given a numerical threshold. A physically usable decoder still needs a justified reference/readout contract.

The source distinction survives rooted isomorphisms fixing a and o: e is a descendant of a, f is not. Both preparations have the same total grade. All pushforwards conserve it. Local gain therefore does not imply global information creation.

This endpoint theorem does not claim separation at every partially contracted stage. Before full contraction, differing amounts of common base grade may have arrived, and raw values can overlap across differing schedules. The complete-fiber endpoint condition is load-bearing.

## 4. What is and is not forced

Complete-fiber contraction is an allowed inherited retraction, and FCV P1 makes (4) independent of its factorization. The source primitives do not yet force it to occur.

A finite capacity limit alone would not prove this endpoint. Overflow might be handled by removing an outside entry, refusing an append, changing retention, or another allowed operation. To use capacity positively, derive that the specified retained-state constraint forces completion of the receiver fiber while retaining a and the reference. No such capacity law is added here.

Similarly, retaining o and a as addresses does not give access to their grades. The two-coordinate present-state interface avoids a numerical-history assumption only by explicitly retaining the unresolved two-coordinate access obligation. A single positive scalar up to arbitrary rescaling cannot distinguish (A+w) from A; (5) uses a common scale for the pair.

## 5. Preparation and certification contract for the next proof

A sufficient continuation should provide:

1. One common pinned prefix with the specified carrier and nonnegative grade object.
2. Two native semantic append certificates at u and o, of equal positive grade w, preserving the old receiver/reference pair.
3. A typed relation from the certified append event to the prefix-tree extension. Hash strings and source addresses alone do not supply it.
4. An inherited condition causing complete-fiber contraction, or a justified positive-probability occurrence class satisfying it.
5. Actual access to the two retained grade coordinates under a common scale.

Items 2-3 are the immediate preparability target. Items 4-5 are the enactment/access target. Equation (1) handles the certificate-continuity component once the events and witnesses exist; equations (4)-(5) handle the consequence once the endpoint and readout exist.

## Status and verification

This extension uses direct symbolic proofs and source inspection. No scientific code, test campaign, changed V997 validator, or new event mechanism was implemented. Original source code was read, not executed. The algebra was checked directly for both terminal outside-entry cases and for the zero-beta/gamma boundary. Independent Gemini review and publication audit of this new argument remain pending; earlier ledger acceptance does not cover it.

The new constructive result is a weaker two-location preparation requirement together with an order-independent, projectively separating present-record endpoint. Preparability and native interaction are not declared closed.
