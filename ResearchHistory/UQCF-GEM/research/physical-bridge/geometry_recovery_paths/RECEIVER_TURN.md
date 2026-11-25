# A matched source cut fixes the other chart's legal deletion and changes its own numerical record

In a two-chart retained tree, the same receiver with the same numerical prior can finish its next deletion with grade **4 or 6 at the same surviving address**. Both histories use one successful source deletion followed by one successful receiver deletion. The address to delete at the receiver is uniquely determined by the native union-preserving rule. The scalar readout takes only the resulting receiver state.

## The controlled histories

Both indexed charts start with the entire six-node tree. The root is 0. Its children are 1 and 2. Node 1 has leaf 4. Node 2 has child 3, which has leaf 5. The pre-event grade vector in either chart, in address order 0 through 5, is (3,4,1,4,2,2). Fix the measured address before the choice of source event. It is node 1, the parent of the shallower of the two leaves. Its initial receiver grade is 4. The two leaf grades are both 2.

| Event or measurement | Source drops shallow leaf 4 | Source drops deep leaf 5 |
|---|---:|---:|
| Receiver grade at node 1 immediately after the source event | 4 | 4 |
| Unique legal next leaf deletion in the receiver chart | 5 | 4 |
| Receiver grade at node 1 after that deletion | **4** | **6** |
| Receiver grade at node 3 after that deletion | 6 | 4 |
| Total receiver grade before and after | 16 | 16 |
| Source and receiver local/global cover orders throughout | 1 | 1 |
| Source or receiver cover-increment trigger | false | false |

Take the source cut of 4 first. The receiver still holds 4 and 5. It is now the last chart containing 4. Deleting 4 from it would change the union. Leaf 5 still occurs twice, so deleting 5 at the receiver is legal and transfers the receiver's own amount 2 to its node 3. Its node 1 stays at 4. After the opposite source cut, the receiver must preserve 5. Its unique legal deletion is 4, transferring 2 to node 1 and raising its grade to 6.

Both arms use the same receiver instruction, “take one legal deletion.” The test passes every vertex through the historical validator, then uses the sole successful result. Scanning in reverse order gives the same individual transition. There is no success-versus-exception encoding at the terminal readout. The grade and node measured are already in the receiver. The leaf identity is determined operationally at the level of the complete indexed family, since the legality check inspects which charts retain that leaf. The source's grade is never passed to the receiver's grade update. That update uses the receiver's old view, its actual new view and its own old numerical vector.

## General two-leaf argument

Let a finite rooted tree X have exactly two global leaves a,b and two indexed charts S,R initially equal to X. Choose a fixed extensive positive grade with the same nonzero amount t at both leaves. A legal v16.26 deletion removes a nonroot tip from a single chart while the union of all charts stays the same. The program can choose either source cut from its initial state.

After S removes a, R's view still equals X, so its only tip candidates are a and b. Deleting a fails the union condition. Deleting b retains a copy of b in S and preserves the complete union. Thus the set of legal receiver deletions is exactly {b}. Reversing the source cut gives exactly {a}. This proof uses neither a cover threshold nor a grade-based selector. It holds for any finite tree in the stated family. The execution protocol supplies one receiver turn after the source turn.

When the parents of the leaves differ, let p be the parent of a and keep that same address in both terminal measurements. The actual P1 map for the receiver's one-tip deletion adds t at the parent of its deleted tip. The two possible receiver grades at p are g(p) after S cuts a and g(p)+t after S cuts b. Every other surviving address outside the affected parent retains its numerical amount. This holds if one parent is an ancestor of the other. For sibling leaves the parent grade gains t in both arms, although the resulting labeled receiver leaf sets differ.

At the source step R covers X on its own. The local cover number of each nonleaf and the global consistency order remain 1. After the complementary receiver step with distinct parents, for every vertex one of the two charts still contains all of its immediate children. Hence those orders remain 1 again. For sibling leaves the common parent requires both charts after the receiver deletion, so the local order and the global maximum rise from 1 to 2 in both histories. In either case both arms have the same six v16.26 cover fields at each stage. The source leaf and its parent are addressed events and may differ between the arms.

## Two controls on what forces the result

* **Change the actor order.** After S removes a, S can also legally remove b. Reversing the two source deletions is legal as well. Both histories then leave R in exactly the same initial geometry and grade, including grade 4 at node 1 in the displayed example. Thus the native deletion law alone supplies no obligation for the other chart to be next. The experiment specifies an ordered opportunity for R to act; it supplies no physical clock or automatic alternation.
* **Add a third full chart.** After either source cut R can now legally delete either leaf, because both have outside copies. Making the same choice at R in both histories can produce the same stored record. This identifies loss of the last outside copy as the condition responsible for uniqueness in the two-chart case.

The experiment combines v16.26 `atomic` and its historical verifier with v16.23 `push`. The first returns a geometry certificate. The second transports the receiver's own grade to the selected new receiver view. The fixed iteration over candidates and the grant of one turn to the other chart are explicit in the harness. At the final measurement, the source and the family validator can both be withdrawn. A scalar lookup on the receiver suffices. The physical implementation of the global union constraint and an inherited reason for the receiver to act remain open.

## Preregistered enumeration and provenance

| Quantity | Result |
|---|---:|
| Topologically ordered parent arrays through six vertices with exactly two leaves | 42 |
| Matched comparisons, including both source/receiver role assignments | 84 |
| Histories with a successful receiver deletion | 168 / 168 |
| Candidate receiver vertices checked per complete forward scan across the histories | 920 |
| Legal receiver choices in those 920 trials | 168 |
| Distinct-parent comparisons with different fixed receiver-parent readings | 76 / 76 |
| Sibling comparisons with identical fixed parent readings | 8 / 8 |
| Comparisons matching all six cover fields at both source and receiver steps | 84 / 84 |

The producer calls the historical validator on every candidate and checks each successful result with its archived independent verifier. It transports grade with the historical operator. A second implementation enumerates the tree and chart identities independently, reconstructs all rejected and accepted vertices from tip multiplicities, and rebuilds every numerical record by atom addition. Nine deliberately altered artifacts test rejection. The two role assignments on a given parent array are labeled comparisons. Counts refer to this finite domain, while the proof above covers arbitrary finite two-tip trees under its premises.

| Status | Premise or conclusion |
|---|---|
| INHERITED | Common Genesis, prefix views, native duplicated-tip deletion with the union preserved, nearest-retained-ancestor P1 grade transport. The earlier receiver-interface argument identifies outside leaf coverage as a condition for deleting a tip. |
| SUPPLIED | The fixed initial two-chart state and fine positive grade, the source alternative, and one subsequent deletion at R. |
| DERIVED | The sole admissible receiver leaf, its actual P1 update, and a same-address numeric difference readable using the receiver alone. |
| OPEN | Derivation of the receiver turn and operational enforcement of the union rule from the physical model. |

[Prospective registration](RECEIVER_TURN_PLAN.md) · [Native producer](check_receiver_turn.py) · [Independent reconstruction](verify_receiver_turn.py) · [Complete certificate](receiver_turn_certificate.json) · [Raw labeled histories](receiver_turn_universe.json.xz) · [Preceding fixed-pair result](FIXED_PAIR_FIDELITY.md)
