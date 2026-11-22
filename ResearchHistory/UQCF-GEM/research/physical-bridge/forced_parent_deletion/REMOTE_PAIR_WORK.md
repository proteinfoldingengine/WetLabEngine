# A source deletion can be identified from the first work change between two other views

Use the archived v16.43 star writer, with root and leaves 1, 2, 3. Give each leaf a common positive ambient grade and put $w_v=g_v^2$. The original v15.40 pairing on the P1 star coordinates of views $i,j$ gives
$W_{ij}=\sum_{v\in Y_i\triangle Y_j}w_v$.
Indeed P1 retains the original leaf grade if the leaf is present and sends its grade to the root otherwise. A retained leaf edge has that grade as subtree flux and potential drop for the unit-star inverse. Coordinates for absent leaf edges are zero. The work is the dot product of the two differences in these coordinates. This is a pair comparison even if two distinct views coincide. No square-geometry admission, transport field, or clock is required to compute it.

## Which receiver and donor the running writer uses

Take exactly two indispensable occupied views on a star, one blank B, and one shared leaf u. Each occupied view has at least one private leaf and together they cover the star. The unique minimum cover consists of the two occupied views. Duplicate cleanup therefore deletes u from the later occupied view A and leaves it in the earlier occupied view R. Grant only that this original invocation runs with its given leaf priority. The actual editor is determined once the view order is supplied.

If B is in either of the first two palette positions, the last index is A. In the original palette alignment the only excess index is A and the only missing index is B. It follows that the source of the pruning is the donor, B is the receiver, and R remains fixed throughout this copy. If B is last there is no such transfer. For the three-leaf examples m>q and later recoloring only targets indices 0,1, so the last blank stays blank. A permutation of the same three starting views can implement either behavior. Pair geometry at preparation, transported with the roles, cannot select between them.

On an active transfer, write S and T for the disjoint nonempty private leaf sets of A and R. After cleanup A has S, R has T union {u} and B is blank. Each copied private leaf increases work between B and R by its squared grade. Restoring just the cleared bit in A before the snapshot causes the inherited transfer to copy S union {u}. The extra copied u *decreases* that same work by $w_u$ at its own insertion. At completion of the addition loop the original work exceeds the control work by precisely $w_u$, regardless of the grades, enumeration order of the leaves and the two possible active positions of B. These are evaluations at program-defined boundaries. A listener with only the two views may be unable to identify that boundary.

## A sign witness that needs no program phase or palette order

Fix the named memberships A={2,3}, R={1,2}, B=empty, omitting the compulsory root. Compare every permutation of these views under the original leaf ordering. For each of the six orders, execute the unchanged writer and the control that restores its *actual* first editor's cleared leaf 2. If that editor is R, this control restores R. Read the sign of the first nonzero change in W between B and R from their initial value. Repeated readings are discarded, including an arbitrarily long run of unchanged values. The test uses no elapsed time, source snapshot after preparation, phase label or copy-completion marker.

| Ordered roles | Original first change in B or R | Under restoration |
| --- | --- | --- |
| B,R,A or R,B,A | B adds 3, absent from R. Work increases by $w_3$. | B adds 2, present in R. Work decreases by $w_2$. |
| R,A,B | R drops 2 while B is blank. | Same. |
| B,A,R or A,B,R | R drops 2 while B is blank. | B gains 1, present in R. |
| A,R,B | R drops 2 while B is blank. | R drops 1 while B is blank. |

Thus a first **increase** identifies an actual deletion at A followed by a B write within this declared comparison family. It occurs in the two active A-deletion originals. A third original A deletion leaves B silent and gives the same B,R history under restoration. All three competing original R deletions and all six controls give a decrease. Exact magnitudes depend on the supplied grades, but the directions hold for every positive grade choice. The counts are enumerated orders and control arms, with no probability interpretation. The historical leaf priority 1,2,3 matters for the first-change test. The sign implication is scoped to these inputs and interventions.

## A transfer can also be completely hidden from the two other views

In original row 232, take A to be the holder of {1,2}, R the holder of {2,3}, and B the blank. In numerical order the masks are (13,1,7) for R,B,A. A drops leaf 2 and the original transfer makes B acquire leaf 1. In the restoration control the transfer additionally copies leaf 2 to B. After all remaining instructions, the ordered pairs of B and R masks change through exactly the same sequence in both executions:
$$
(1,13), (3,13), (7,13), (7,9), (7,11), (5,11).
$$
The original acquires 2 at B during later recoloring. The control already copied it there. A full sequence of B and R's changes therefore fails to distinguish these source alternatives for every deterministic function of that sequence, including pair work at every local update and arbitrary fixed grades. Counting unobserved global edits or reading a marker for the transfer boundary grants additional information. Both global paths pass the same exact profile and canonical endpoint test. The original is the archived trajectory and the restored trajectory is a generated control. This alternate assignment of the marked source and reference uses the same family of masks as the six-order sign test.

**Scope.** The software actually copies the donor's surviving addresses. No extra launch is inserted between pruning and copying. The historical palette still selects occurrence, and its leaf order affects which first writes are distinguishable. The two-view reading is a mathematical relation reconstructed from those views. No inherited reader located at B has been shown to receive R's state or to produce this number there. The physical occurrence of the program, accessibility of the record, and any connection to gravity remain open.
