# Source erasure with a retained converted record in nested support

Date: 2026-10-11. Source parent: 0427e18aeae1625b7bd685e511038f769eef0c01.
Status: analytical candidate pending independent review and prospective verification; NOT CLOSED.

## 1. Question and supplied structure

Can the temporary parent-membership record of COUPLED_C3_NESTED_RECORD_PROBE.md be converted so that its source incidence can be removed while a historical distinction remains? Work entirely in the inherited v16.53 nonempty nested-support grammar. A legal primitive toggles one incidence at one nonroot vertex, retaining nonemptiness, nesting and the fixed global root. No new primitive or physical enforcement law is supplied.

Fix the ordered tree o with children (u,B,C), and u with leaf children (r,w). Fix distinct labels a,b,c,d,x in an ordered finite palette P. Choose sets A,W,B0,C0 satisfying:

- {a,b} subset W subset A, and x not in A;
- c in B0, d in C0, with A union {x}, B0, C0 pairwise disjoint;
- every set is contained in P; unused root-only labels are allowed.

The source bit is sigma in {0,1}. Initially S_o=P, S_u=A union ({x} if sigma=1), S_r={a}, S_w=W, S_B=B0, S_C=C0. The initial record at r and every support other than u are identical across the two sources. The tree, ordered labels, common support preparation and request addresses remain supplied. No physical initialization is asserted.

Set internal targets q_o=3, q_u=1. These initial states are exact: the three top children are pairwise disjoint and nonempty; r and w share a.

## 2. Fixed five-request script

Use the same order in both sources:

    1. +x(r)
    2. -a(r)
    3. +b(r)
    4. -x(r)
    5. -x(u)

The mathematical protocol allows any command to be skipped. Executing it is permitted only if the named primitive is legal in the inherited grammar. Equivalently, a realized history is a legal ordered subsequence of these five commands, with each position used at most once. This is a class of histories for a conditional theorem, not a physical rule choosing a successor or ensuring an attempted command commits. No background edits, reordering, repeats or inserted commands are covered by the soundness claim.

Let m=1[a absent from S_r]. This is the proposed mathematical historical record. It is not an assumed observer readout, acknowledgement or probability law.

## 3. Complete positive construction

For sigma=1, all five commands can be executed. The changing supports are:

| Slice | S_r | S_u | (h_o,h_u) |
|---|---|---|---|
| Initial | {a} | A union {x} | (3,1) |
| +x(r) | {a,x} | A union {x} | (3,1) |
| -a(r) | {x} | A union {x} | (3,2) |
| +b(r) | {b,x} | A union {x} | (3,1) |
| -x(r) | {b} | A union {x} | (3,1) |
| -x(u) | {b} | A | (3,1) |

Each addition lies in the parent. Each deletion leaves its support nonempty. Deleting x at u is allowed only after its children omit x; w never contains x and step 4 has removed it from r. All other incidences stay fixed. The achieved cost is five actual edits; no optimality claim is made.

At the only inexact slice, {x} and W are disjoint, so h_u=2. At every other slice r intersects W in a or b. The top supports stay pairwise disjoint, so h_o=3 throughout. Therefore total excursion sum_v |h_v-q_v| is at most one. Both endpoints are exact.

For sigma=0, the legal subsequence consisting only of step 3 ends at S_u=A and S_r={a,b}. Thus two admitted histories begin with identical records and finish with identical source supports and different record supports. They use the same ordered script, but not the same committed subset. No deterministic realization of that difference is asserted.

## 4. Soundness under every permitted skipped-edit history

Claim: for every legal ordered subsequence, m=1 implies that the ORIGINAL source bit was sigma=1.

Proof. The only command deleting a from r is step 2. Before it, r can only be {a} or {a,x}, because step 1 is the only earlier possible edit. Deleting a from {a} is forbidden by nonemptiness. Hence a successful step 2 requires the earlier addition of x, and that addition requires x in u. No command has yet changed u; therefore x was present initially and sigma=1. No later command adds a, so once m=1 it remains 1 through the script. QED.

The converse is not promised: skipping steps can leave m=0 even when sigma=1. The result is a sound positive historical certificate relative to the protocol, not an exact guaranteed write of sigma.

Every legal ordered subsequence remains within the same unit-excursion bound. The possible nonempty record supports are subsets of {a,b,x}. Before step 2 they contain a; after step 3 any b present intersects W. The only possible support disjoint from W is {x}, which has h_u=2. No script command removes a or b from u, and u remains disjoint from B0,C0, giving h_o=3. Skipped commands add no native incidence edge.

If a permitted history ends with S_u=A and m=1, then S_r={b}. Indeed nesting excludes x at r, m excludes a, and nonemptiness requires b; there are no other record labels. Thus whenever source erasure and a positive record both occur, the temporary x incidence is absent from the record and the converted record is exact.

Within this fixed script that joint outcome requires all five positions. A positive record requires steps 1 and 2. Source erasure then requires step 5; nesting requires step 4 first; and after step 2, removing x from r requires step 3 to keep r nonempty. This is necessity within the declared protocol, not a shortest-path bound among arbitrary protocols.

## 5. Retention, downstream effect and provenance limitation

The preceding nested-record probe correctly showed that retaining x at a descendant pins x at its parent. This construction does not violate that observation: it removes x from the record after converting the distinction into absence of a, backed by b. The parent is then free to lose x. The record is a distinction about the declared history, not a certificate of current x membership.

At the two completed endpoints above, source u equals A in both. The same later request -b(r) has different native availability: it is forbidden at {b} by nonemptiness, and admitted at {a,b}, where it leaves {a}. Thus the retained difference can affect a further primitive after the original source incidence has disappeared. This is an operational distinction in the admitted graph. It is not a proof that a controller can query legality, detect rejection, or physically access m.

Protocol provenance is indispensable. Starting from sigma=0, the OUT-OF-PROTOCOL order +b(r), then -a(r) is a legal two-edit path to S_r={b} while S_u=A throughout; its internal targets remain exact. Therefore the final record alone is NOT a sound historical certificate over arbitrary native histories. It is sound only with the declared initial state and restricted edit order, excluding other writers. This explicit counterhistory must be preserved in verification and must not be rejected as natively illegal merely because it violates the protocol.

Nothing forces record persistence under arbitrary future operations. For example, +a(r) erases its distinguishing absence. No physical force, global information-destruction claim, permanent memory or intrinsic arrow of time follows. The five positions are an ordered script, not a fundamental clock.

## 6. Relation to the existing record and event results

The earlier internal-record attempt already demonstrated conditional incidence certificates and rejected a forced-commit completion. This candidate retains those limits. Its additional scoped content is the explicit conversion and source-erasure route, with exact restored source and endpoints, unit excursion, all-subsequence soundness and an explicit protocol-forgery control.

The existing event-init and command-provenance results require legitimate seeds and actual-event/exclusive-writer records. They do not supply physical provenance for this script. The phased/precedence theorems also begin with retained data and declared updates; they cannot be used circularly to initialize the present observer access. The record encoding and decoder here are a separately specified consumer, not satisfaction of the restored-marker gate or its swapped-root test.

This is a conditional mathematical mechanism inside the supplied native grammar. Initialization, execution/enforcement of the script, physical reference identities, accessible retained output and actual-successor selection remain separate unresolved obligations. Guaranteed progress is not required for the conditional claims, and no stochastic kernel is introduced.

The model does not inherit arbitrary C3 floor-two or universally protected hidden-completion guarantees: r is allowed to be a singleton, and the tree is nested rather than a depth-one C3 star. Broad C3/C4-C6 remain open. No physical source law or gravitational correspondence is claimed.
