# One receiver edit restores the original work geometry

A single pruning with positive squared subtree grade changes the work comparisons of one view. If the initial graph of minimum-work pairs had degree four, that deletion necessarily violates the original degree-four requirement. If one further positive deletion at a different view restores an admitted geometry, the two views must have been at least three edges apart in the original work graph. The proof uses degree and the original rule for opposite neighbor pairs.

I constructed a 25-view case on one ambient retained tree with a fixed positive grade. The source deletion disrupts the work graph. Among all 32,575 legal next deletions, just one restores the original geometry gate. View 12 must delete leaf 2. Its identity follows from the degree defects and its holdings. Reordering the action catalogue does not choose the outcome. A further deletion by the source is also legal under same-union pruning and fails geometric admission. [Proof and fixture](GEOMETRY_REPAIR.md) · [Exact replay](geometry_repair_evidence/geometry-repair-replay.zip)

| Quantity | Before the source deletion | After source deletion | After the unique recovery |
| --- | ---: | ---: | ---: |
| v15.43 geometry | Admitted | Degree-four test fails | Admitted |
| Receiver root grade | 242 | 242 | 244 |
| Invariant on the fixed square with the same field | 1/64 | Geometry unavailable | 0 |

The two admitted neighbor graphs exchange the source and receiver labels. The fixed square keeps all four labels. The field stays attached to the original source label, so the stencil at that square sees it before recovery and loses it afterward. With the field moved along with the graph, the relational comparison would move too. The result uses the fixed labeled field and proves a geometric change relative to it. The loop invariant is distinct from the grade delivered to the receiver's root.

**Scope.** I supplied the preparation, the evaluation field, and the condition that the geometry returns after exactly one more pruning. Given that condition, the existing geometry tests determine the action and P1 determines the receiver's record. Native enforcement of recovery and physical access to the retained grade or the loop read remain open. Graph distance here counts edges in the work graph.

## Verification

The exploratory carrier call failed because I passed integer work values to the rational-only interface. I corrected the exact type conversion before freezing the verification code. The independent checker enumerates the candidates from indexed memberships and verifies their counts against the support columns. The original v16.26 verifier checks the source and receiver deletions. The archived v15.40 work pairing, v15.43 carrier and field routines run at the accepted endpoints. A constant-field control returns zero on every face at both ends. [Verification contract](GEOMETRY_REPAIR_CHECK_PLAN.md)

Gemini 3.1 Pro Preview accepted the exact mathematical scope and left the physical bridge **open**. In the adjacency proof, the two maximal pairs are disjoint and cover all four neighbors. One maximal pair therefore includes B. The equality of the three pairs containing B then gives the contradiction. In the loop calculation, the repaired square's four corners have no incident edge to the marked source A. [Worked review](geometry_repair_evidence/review_verdict.json) · [Raw final review](geometry_repair_evidence/geometry-repair-review.zip)

Both GitHub replays and the separately extracted frozen checkout reproduced the same certificate SHA-256, `28b4892855331ac627986167f3882304e246b90d882df685e0917a3f6e404aa2`. The audit matched the originally returned review and the publication log. [Verification run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/45042380003) · [Exact readback receipt](geometry_repair_evidence/readback.json)
