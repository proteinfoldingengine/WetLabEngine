# An existing role-transfer routine consumes the receiver shape signal

Author: ChatGPT research session with Aaron. Date: 2026-10-25 (America/Phoenix).
Status: author-checked analytical construction; not independently reviewed. Native bridge NOT_DERIVED.

## Positive result

The existing producer.replace_role routine can transfer the acquired T-122 distinction from index r into index a, whose entire starting view and bare command interface are identical in the two preparations. The same three calls, with the same source label r and destination label a, work for every admitted first-response case. No grade encoding, zero extension, decoder-guided edit, source-bit argument or new copying implementation is needed to calculate the transferred native incidence state.

This is a relay: r already carries the first-response signal, and the distinct downstream receiver is the existing palette index a. It is not an access proof for r and does not silently replace r by a vertex. The routine writes a source-sensitive incidence view for a within the supplied software invocation. Physical invocation, role association, completion and availability remain unproved.

## 1. Premises and source identities

1. Fixed rooted T, palette P={a,b,r}, nonempty nested supports, fixed root P, and one-incidence edits — INHERITED mathematical grammar [v16.53 NATIVE_ADMISSIBILITY.md, blob ebc315f7f2f6423fe9f6861cc3b8a0cfcf8420f2 at research 3ceb814258f43774b4af1352379ffcd0bd079599]. Only the bare grammar is used, not a hitting-profile budget or exact normalization target.
2. vertices(nodes,child) gives preorder traversal, and replace_role(current,nodes,child,x,y,path) rejects occupied destination incidences in that subtree, snapshots the source-used vertices, adds destination incidences in preorder, then deletes source incidences in reverse order — INHERITED SOFTWARE [producer.py lines 11 and 108–113, blob 0501a1b32c0a660646ff95ecbb8a37a8f2e04b80 at the same research SHA]. This is the existing helper, not a new implementation or claim that every caller is legal.
3. T-122's acquired states after its common source withdrawal and one proper r response — ACCEPTED-CONDITIONAL mathematics [RESULT at 43596de4fe9fd1083500987997ee04e15793f60c; ACCEPTANCE at 546511327ee6a224dcc583305e7864a456863c4f, review run 40235454564]. The carrier/preparations/acquisition phase retain their SUPPLIED status. Actual event occurrence is ACCEPTED INPUT; correspondence to this process is not derived.
4. Invoke the helper successively on the three root-child subtrees, in order u,v,w, always x=r and y=a, with b fixed — SUPPLIED common caller and completed transfer episode. No autonomous caller or actual-event binding is asserted. Choosing a as the downstream receiver and granting any physical access remain SUPPLIED.

## 2. Actual input and the same calls

T has edges o-u,o-v,o-w,u-x,u-y,u-z. Use the code's preorder (o,u,x,y,z,v,w), tree value (((),(),()),(),()), and palette order (a,b,r).

At the start of the relay, a occupies only o in every case. The first-response states are:

| Original source | b view | r view | Bit-mask columns (a,b,r) |
| --- | --- | --- | --- |
| 0 | {o,v} | T minus {v} | (1,33,95) |
| 1, first deletion x | {o,u,x,y,z} | T minus {x} | (1,31,123) |
| 1, first deletion y | {o,u,x,y,z} | T minus {y} | (1,31,119) |
| 1, first deletion z | {o,u,x,y,z} | T minus {z} | (1,31,111) |

These masks are analytic encodings, not program execution results. The code's child indices are 1,5,6. The literal common invocation is:

    path = [current[:]]
    replace_role(current, nodes, 1, 2, 0, path)
    replace_role(current, nodes, 5, 2, 0, path)
    replace_role(current, nodes, 6, 2, 0, path)

The bit is present in the source state supplied to the routine, not in a source-dependent choice of its arguments. The routine inspects the r column to select its used vertices. That is an existing system-side dependency; it is not a claim that a can inspect r or the full state. No full normalize invocation is asserted.

## 3. Legality and exact endpoint proof

Consider one called child subtree C. At that call, a is absent throughout C: initially it is absent below o, and earlier calls act on disjoint child subtrees. Thus the helper's vacancy check passes. Its used list is precisely C intersect Y_r at the start of that call.

Every destination addition is a proper legal +a(t). If t is the subtree root, its parent is o and already contains a. Otherwise prefix closure of Y_r puts t's parent in used, and preorder adds a there first. The existing r incidence at t keeps the support nonempty. Adding a cannot violate child nesting: every child already carrying a would have required a at t, which was absent before this addition. The helper adds only once at each previously vacant position.

After all additions in C, every vertex in used carries a. Deleting r at these positions in reverse preorder removes all r-descendants before their ancestors, so r nesting holds. Each deleted incidence retains a at its vertex, so nonemptiness holds. Other labels are unchanged. The global root is never edited.

The endpoint on C therefore has a exactly where r was, and r absent. If used is empty, the call makes no edits, which is the correct endpoint for that subtree. Across all three calls, with Z the original acquired r view,

    Y_a(final)=Z,    Y_r(final)={o},    Y_b(final)=Y_b(initial).

Each Z has six vertices, hence five nonroot r incidences. Each is added to a once and removed from r once: exactly ten primitive changes, with eleven snapshots when including the initial snapshot. These counts follow from the loops; they are not numerical test counts.

The final columns are respectively (95,33,1), (123,31,1), (119,31,1), and (111,31,1). The originally acquired distinction is now in a's own incidence view. The root label assignments preserve both index identities; no parent vertex becomes the receiver.

## 4. Initial blindness and separating consequence

At relay entry, Y_a={o} in every preparation. Moreover, r and b together cover every nonroot global leaf: a is absent there and the native supports are nonempty. Thus the external leaf-coverage set for a is the entire global leaf set in every case.

The inherited receiver_move_interface RESULT sections 2–3 (blob 0371d4a8aa66ce02ffbda084ad5dde93f1ec1136 at the research SHA) determines the bare a-command interface from its own view and that external coverage set. Therefore all finite a-only command experiments with r,b fixed have matching legality and own-view observations at this starting comparison. This is complete blindness within that specified hypothetical interface, not every conceivable physical observation or hidden-state-dependent probability law.

The relay itself is not such an a-only experiment: it also deletes r. Those source edits are exactly where the interface's fixed-exterior condition ceases to apply. There is no contradiction with the interface equivalence theorem.

At completion a's view is T minus v for source 0, or T minus one of x,y,z for source 1. Both have six vertices. Their maximum undirected degrees are four and three respectively, by the accepted T-122 calculation. Consequently the existing two-feature signal is now present in a. This does not require the helper to compute either feature. A decoder or physical observation is not supplied by proving that the endpoint differs.

Initially a's singleton view is common. The global path returned through the supplied path list is NOT an initially blind receiver record: its first snapshot already contains the source-bearing r and b columns. No acquisition is credited to that global history, and no permission for a to read it is assumed.

## 5. Scope, controls, and prior work

T-108 used the same helper on a different witness and needed a source-dependent destination b_s; vacancy alone did not ensure the parent's matching label. That objection is preserved. Here both operands are the same known labels r,a in all cases, and the required parent membership follows from root membership plus the proved preorder additions. This is a specific valid caller, not an autonomous label-selection theorem. The blank destination after T-122 withdrawal is essential; this routine would reject a subtree already containing a.

The routine transfers the r incidences; it does not leave r's original nonroot record intact. Before each source deletion the destination temporarily duplicates that incidence. Preservation beyond the completed endpoint is not claimed. Subsequent arbitrary incidence edits may erase or alter the a record.

Stopping before completion need not reveal the source: the first addition is +a(u) in every case, giving the same a view {o,u}. The ten-step completed call sequence is a supplied episode, not derived fairness, a physical clock or an outcome law. Nor does fixed argument selection derive why an actual event invokes the routine.

T-129's grade coalescence and T-130's P2 realization mismatch are unaffected. This relay uses existing label-incidence replacement rather than grade contraction or restoration. It derives a concrete software/native-grammar downstream state update once the common invocation is given. It does not produce a new physical interaction, access law, autonomous caller or readout mechanism.

## 6. Verification and review scope

The helper and traversal source were inspected directly; every loop edit and all four mask endpoints were reconstructed analytically. No scientific module, enumeration, simulator or native normalization campaign was executed. No claim is made about the all-one hitting profile, unit-excursion budget, all possible callers, or full normalize endpoint.

Independent review should reconstruct the full source-dependent state transformation with fixed arguments, verify every parent/child and vacancy condition, challenge initial-interface blindness and the changed actor class, check all four endpoints and the stopping control, and keep a distinct from the earlier receiver r. It must distinguish an inherited software consumer and a supplied caller from an actual receiver-owned process. All physical preparation, invocation, completion and access limitations remain explicit. Native bridge and broad C3/C4 remain OPEN. No main merge or numbered-stage certification is claimed.
