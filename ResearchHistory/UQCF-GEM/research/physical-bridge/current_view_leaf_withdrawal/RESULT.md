# Current-view retention under interleaving and minimal leaf withdrawal

Date: 2026-10-22 UTC. Author: ChatGPT research session with Aaron, through proteinfolding-gpt; distinct from dot.
Source baseline: b8adfb56e6cbc41ff1ab444b74f696e570101e03.
Status: analytical candidate frozen for independent review. Native event/receiver association NOT_DERIVED.

## 1. Question and contribution

For the existing two-cone preparation, can the CURRENT receiver view carry a correct persistent source distinction throughout source/receiver interleaving, without a separately retained first-response log? Which source deletions are actually needed?

Within the explicitly supplied deletion-only history class, the answer is yes on histories that execute the full specified source list. We prove an exact prefix-completion criterion and show that withdrawing the source index at every cone leaf is sufficient. Among initially legal common source lists, every leaf is necessary for this all-history, both-source guarantee; internal source deletions are unnecessary. The six-vertex example needs three source deletions instead of four.

This is a conditional reduction of a particular construction. It does not identify an actual native observation, implement a completion filter, or derive receiver access. Full source execution is a premise about the history; no completion flag is a decoder input.

Credit: first_pruning_own_view_review/RESULT.md §§2–8 provides the preparation, common source withdrawal, post-source current-view decoder and retention, and early-response/restoration controls. receiver_move_interface/RESULT.md §§1–3 provides bare move legality and initial interface equivalence. Grok's corrected T-050 Theorem O, with dot's history-universe correction in PR #111 comment 6348161148, gives first-response correctness under interleaving. T-051 and T-052 of this research session state the arguments consolidated here. We claim neither a new basic pruning operation nor archive-wide mathematical priority.

## 2. Premise ledger and exact episode

All repository-relative sources below are under ResearchHistory/UQCF-GEM unless stated otherwise. Source excerpts and full-file identities are bound by SOURCE_PACKET.json.

P1 — INHERITED mathematical category: a fixed finite rooted tree T with root o, fixed finite palette P, S_o=P, nonempty supports S_z subset P, and S_child subset S_parent. The operation toggles one index incidence at one nonroot vertex while preserving these conditions. Y_i={z:i in S_z} is the transposed view. Producing operation: single-incidence addition/deletion; demos/v16.53-four-child-boundary/NATIVE_ADMISSIBILITY.md, “Carrier and extension,” and receiver_move_interface/RESULT.md §§1–2 at b8adfb56e6cbc41ff1ab444b74f696e570101e03. We use the bare grammar; no hitting-profile budget or physical interpretation is imported.

P2 — SUPPLIED preparation and role assignment: T={o,w} disjoint-union U disjoint-union V. The root has precisely children u,v,w; U and V are the finite nonempty descendant cones of u and v, and w is a leaf. P={a,b,r}. S_o=P and S_w={r}. Put (A_0,B_0)=(U,V) and (A_1,B_1)=(V,U). In preparation s, S_z={a,r} on A_s and S_z={a,b,r} on B_s. Source: first_pruning_own_view_review/RESULT.md §2 at the baseline. Physical preparation and role identification are not derived.

P3 — SUPPLIED episode: choose Q subset D=U union V and a fixed common ordered list sigma_Q deleting a once at every member of Q. The list is legal from the unmodified initial preparations. A finite legal history has outside-r projection exactly a prefix of sigma_Q, in order; every other operation is an r-deletion. All operations are executed incidence changes, not requests or NOOPs. There are no additions, b-changes, other source operations, carrier changes, or root changes. After the list is complete, only further r-deletions are permitted. This exact alphabet applies throughout every history discussed below.

P4 — SUPPLIED completion condition, used only where stated: the entire chosen list sigma_Q has successfully executed by the end of the finite history. Legal prefixes without this condition are also considered in the completion tests. Neither universal completion nor a physical postselection rule is inferred.

P5 — SUPPLIED observational interpretation: the receiver can access its current Y_r and a common source-independent carrier/reference. For arbitrary cones the reference includes their association with the source labels U,V. In the six-vertex specialization below, the source answer is distinguished structurally by depth, without an arbitrary branch-name test. The mathematical decoder reads no a-view, b-view, command log, occurrence count, first-response memory, or completion flag. Mathematical availability of a function does not establish physical availability of its input.

P6 — ACCEPTED INPUT: actual atemporal measurement/pruning occurrence. It does not identify that occurrence with this list, select actor r, imply P2–P5, or assign probabilities. Time remains ordered pruning/recoverability update, not a fundamental clock.

Definitions: L=L(U) union L(V) consists of the global leaves in D and excludes w. For a reachable state S write M(S)=T minus Y_r(S). On the common reference define d(T)=UNKNOWN; d(Y)=0 if the nonempty missing set is contained in V; d(Y)=1 if it is contained in U; d(Y)=INVALID otherwise. Since U,V are disjoint these cases are unambiguous. INVALID is a mathematical convention, not a claimed native rejection signal. An incorrect single-cone missing set may decode to the wrong bit without being INVALID.

## 3. Initial blindness and legal source lists

By P2, Y_r=T in both preparations. Initially all leaves of D have outside-r coverage from a, while w has none. Thus the pair (Y_r,E_r), with E_r the externally covered nonroot global leaves, is the same in both cases. The inherited interface argument in receiver_move_interface §§2–3 gives identical bare r-command experiments while external labels are fixed. Briefly: an addition consults only r's own view and parent membership; a deletion requires an own-view tip, and nonemptiness is automatic at an internal tip by a nonempty child support. At a global leaf it consults external coverage. Identical (Y_r,E_r) therefore gives matching commands and preserves equality inductively. This is initial interface blindness under that named hypothetical interface, not a statement about rates, hidden extra reads or future external changes.

By P1–P3, an initially legal Q must be descendant-closed inside D: if a is deleted at z, it must already be absent at every descendant. Only source actions change a, so all those descendants belong to Q and precede z in the list. Conversely, every descendant-closed Q has a descendant-first legal order in either preparation, since r initially retains every vertex. The fixed order in P3 necessarily respects these dependencies. In particular Q=L is legal in any fixed order, and Q=D is legal in a child-before-parent order.

Every legal prefix preserves the b-view, determines the a-view from the executed source prefix, and makes M grow by inclusion. Root membership is fixed. Removing r at w is impossible because it is its only label. These are deductions from P1–P3, not additional restrictions.

## 4. Full withdrawal: exact prefix-completion criterion

Theorem 1. Take Q=D with the common child-before-parent list. At any reachable prefix S under P1–P3, the following are equivalent:

(i) S admits a legal continuation in the same episode completing the source list;
(ii) the remaining source suffix can execute immediately without further r-action;
(iii) A_s subset Y_r(S).

Proof. (i) implies (iii): if z in A_s lacks r at S, it can never regain r under P3 and never has b. Completion removes a at z if it has not already done so. Its final support would be empty, contradicting P1. (If a was already absent, S itself would have been invalid.)

(iii) implies (ii): r-moves do not affect any a-tip condition. The remaining a-deletions still occur descendant-first. Each deleted incidence in A_s retains r by (iii); each in B_s retains b by P2–P3. Thus every remaining step is legal. (ii) implies (i) by choosing that very suffix. QED.

At every prefix of a history satisfying P4, its actual remaining suffix provides (i). Hence A_s is retained at every prefix and M subset B_s, even before source completion. If a response occurs, M becomes nonempty and cannot shrink. Thus d reads s from the CURRENT view at every subsequent prefix. No separate stored first-response record or source-before-response order is needed in this conditional history class. The history may execute the entire source list and still have no r-response; then d remains UNKNOWN.

## 5. Leaf withdrawal: exact minimum for the declared guarantee

Define G(Q) as follows: in BOTH preparations, EVERY legal finite history in P3 satisfying P4 has M subset B_s at every prefix. Consequently every nonblank current view in such a history decodes correctly and remains nonblank thereafter.

Theorem 2. For any initially legal common list sigma_Q as in P3, G(Q) holds if and only if L subset Q. Therefore Q=L is the unique least sufficient source SET under inclusion, and the minimum number of distinct atomic source deletions is |L(U)|+|L(V)|. Several leaf orders can realize this same least set; uniqueness of an order is not claimed.

Proof of sufficiency. Suppose L subset Q. At the final state each leaf l in A_s has lost a, never had b, and must retain r by nonemptiness. Since r cannot be restored, it retained r at every earlier prefix. Every vertex of the finite cone A_s has a descendant global leaf. Nesting forces r at that vertex at each prefix. Root and w also retain r. Hence M subset B_s throughout. Receiver deletions only enlarge M, proving correctness and persistence after any response. No internal a-deletion is used in this proof.

Proof of necessity. If l in L is omitted from Q, choose the preparation with l in A_s. Initially -r(l) is legal: l is a global leaf with support {a,r}. Execute it first, then the full list sigma_Q, with no other receiver actions. Source a-tip tests are unchanged by the r-deletion. At each requested vertex r is still present, since the sole missing r-incidence is at l and l is not in Q. Thus every source deletion is legal and the full list executes. But M={l} throughout, so d returns 1-s, including at completion. This is a legal counterhistory to G(Q), for any omitted leaf and any fixed initially legal list. QED.

The theorem is only an iff for this preparation, alphabet, all-history quantifier and decoder. It does not classify all safe protocols, alternate decoders, empirical event laws, or special selected histories. Successful source completion is still supplied; this theorem does not provide a physical filter that excludes the counterhistories of incomplete execution.

Theorem 3 (reduced-list completion test). For Q=L at any legal prefix, statements (i), (ii), (iii) of Theorem 1 are again equivalent.

Proof. If a leaf in A_s lacks r, it still has a by validity. Its mandatory future a-deletion cannot execute without emptying its support, and r cannot return. Conversely, if every A_s leaf retains r, each pending source deletion retains r there or b in B_s, and its tip test is automatic because it is a global leaf. Thus the remaining list executes immediately. Every A_s leaf retains r if and only if A_s subset Y_r, by nesting and finite leaf coverage. This proves the three-way equivalence. QED.

## 6. Concrete six-vertex realization and rejecting controls

Let U={u,x,y} with children x,y of u, V={v}, and o have children u,v,w. The reduced common source list is (-a(x),-a(y),-a(v)); the old internal deletion -a(u) is unnecessary. All supports not explicitly changed are P2's supports.

After the source list with no receiver response, the first admitted r-deletion menus are {-r(v)} in source 0 and {-r(x),-r(y)} in source 1. Indeed A_s leaves are now exclusively r, B_s leaves retain b, w is exclusively r, and internal u still has r-children. The remaining a at u does not allow deleting its r-incidence while those children retain r.

For source 0, the interleaved history -r(v),-a(x),-a(y),-a(v) is legal and decodes 0 from the first step onward. For source 1, -r(x),-a(x),-a(y),-a(v) is legal and decodes 1 from the first step onward. The initially deleted leaf in either positive witness belongs to B_s and retains b at source withdrawal. These are lawful existence witnesses, not source-blind policies or positive-probability claims.

On this tree a structural decoder is UNKNOWN when M is empty, 1 when M contains any depth-two vertex, and 0 otherwise for nonempty reachable M. In source 0, M is a nonempty subset of {v}. In source 1 it lies in {u,x,y}, and absence of u forces absence of x,y by prefix closure; thus every nonempty M contains a depth-two vertex. Depth is ancestry length, not a metric or clock. The rule does not need to distinguish the two depth-one leaf children v,w by name, because w is never absent in the episode. The arbitrary-cone source association in P5 remains explicit outside this specialization.

Controls, all established analytically before the freeze:

1. Incomplete execution: source 1 admits -r(v),-a(x),-a(y), but the remaining required -a(v) is impossible at support {a}. Its current view wrongly decodes 0. A request resolving NOOP would not satisfy P4. No decoder input here detects failure to complete.
2. Missing required leaf: omit v from Q, and the preceding history IS complete and still wrong in source 1. Omitting x or y analogously permits that wrong early leaf deletion in source 0. These are Theorem 2's necessity witnesses.
3. Restoration: permit additions beyond P3. In source 1, -r(v),+r(v), then all three source deletions is legal and completes. The first current view is wrong and the second is blank. Thus completion without deletion-only persistence does not establish the all-prefix guarantee. This counterexample does not prove deletion-only is necessary among all alternative protocol classes.
4. No response: the source list alone completes legally in either preparation and leaves Y_r=T. Completion does not imply any nonblank output or actual receiver response.
5. Internal withdrawal only: initial legality forbids deleting a(u) while retaining a(x) or a(y). Arbitrary sets of internal deletions are not admitted as source lists. Conversely, leaving a(u) in place is harmless once the three leaf withdrawals execute; r at the A_s leaves protects their ancestors.
6. Changed outside alphabet: after source completion in source 1, +b(v) followed by -r(v) is legal in the larger grammar and gives the wrong current bit. P3 excludes that b-change explicitly. The source list's completion is not a substitute for external stability.

## 7. Scope and review contract

The mathematical gain is current-view correctness/persistence at all prefixes of successful interleaved histories and a minimal leaf-only source list in this construction. Three rather than four source commands in the example is a reduced supplied enactment burden, not a derived physical mechanism or fewer physical assumptions counted as a percentage.

No actual preparable pair, event-to-list association, receiver actor restriction, deletion-only law, common reference access or own-view access is established. Occurrence is accepted input; the issue is its correspondence to these operations and records. The proof conditions on successful full execution. Using that condition after the fact to discard failed histories would be postselection, not a derived online mechanism. A decoder without a completion input is not a receiver that knows completion will happen.

All general proofs, examples and controls were derived analytically before freezing. No simulator, enumeration, empirical fit or scientific numerical execution is proposed or performed. The whole argument, exact relevant source excerpts and immutable full-file identities must be sent through the standing Gemini Actions review, with prior review verdicts of this candidate absent. The reviewer must independently reconstruct all three theorems, find omitted premises or counterhistories, check the arbitrary-cone and structural-decoder distinction, and challenge any physical interpretation or excessive novelty claim. Preserve raw requests/responses, model availability and model identity, run/checkout/workflow identities and hashes. A separate publication audit must bind those exact bytes. No numbered-stage closure, inherited-stack replay, main merge, independent acceptance or native milestone is claimed by this document.
