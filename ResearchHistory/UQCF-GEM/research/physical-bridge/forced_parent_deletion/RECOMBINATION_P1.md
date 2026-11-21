# Can a native P1 prune produce the archived response change?

The two V1687.16 bracketings gave a difference of 207 at one fixed port. We tested the literal binding in which the program’s twelve coordinates carry the same ancestral grades before and after an event. A single P1 pruning operation cannot produce the full archived change. This remains true if the changed grade first passes through either original fixed grouping with its gates held fixed. The archived response difference has rank 10. The corresponding upper bounds for one native prune are 2 for direct input to the outer operation and 6 after the two inner operations.

The comparison also isolates what survives coarse-graining. For each of the two settings of the right operand, the original full output fails to descend to the same cyclic rule after every single removal tested. The full contrast does descend for two mergers. Their individual errors are identical and cancel in the subtraction. The nominated read at site 3 can survive many more mergers.

## Operations and scope

The frozen [matched-port result](SAME_PORT_RESPONSE.md) uses the original V1687.16 operation with fine cyclic successor \(S e_j=e_{j+1}\), indices modulo \(n\), and \(\gamma=3\) in the outer call. Call its two internally computed right operands \(q^{(3)}\) and \(q^{(4)}\). Fix the two groupings, their original gates and the matching identity of the left-input and output coordinates. The fine operator is
\[
R_n(x,q)=x+q+\gamma B_\sigma(x,q),\qquad
B_\sigma(x,q)=(Sx)\odot q-x\odot(S^{-1}q).
\]
Here \(\sigma(j)=j+1\bmod n\). P1 and P2 are the inherited extensive pushforward and literal retained inclusion in the [foundational proofs](../../../foundational-closure-verification/PROOFS.md). P1 sends all addresses in each ancestral fiber to the sum of their grades. For testing one removal \(u\to p\), \(P e_j=e_{r(j)}\) with \(r(u)=p\) and \(r(j)=j\) otherwise. Literal inclusion \(I\) fills the deleted slot with zero. This is a candidate alignment to the existing array routine. The archived array program itself supplies no such address map. All 132 ordered pairs test every possible pair in this slot alignment. They include connections that a particular fixed tree might exclude.

## Bound on the operator change from one event

The left-input Jacobian is
\[
J(q)=I_n+\gamma (S-I_n)\operatorname{diag}(S^{-1}q).
\]
An off-diagonal entry \(J_{\sigma j,j}\) equals \(\gamma q_{\sigma j}\). At fixed nonzero \(\gamma\), the right-operand change is therefore identifiable from the full change of this Jacobian. A column of the difference for \(s=\Delta q\) is \( \gamma s_{\sigma j}(e_{\sigma j}-e_j)\). Any proper subset of the columns of the directed cycle incidence matrix is independent. Each resulting path has an endpoint of degree one, so leaf elimination forces every coefficient of a zero combination to vanish. Hence
\[
\operatorname{rank}(\Delta J)=\min(n-1,|\operatorname{supp}(\Delta q)|).
\]
The archived difference \(q^{(3)}-q^{(4)}\) has ten nonzero coordinates and rank 10. For one direct P1 edit with initial fine grade \(q\), the change with literal inclusion is \(q_u(e_p-e_u)\). The rank is at most 2, regardless of the event amplitude.

The rank bound continues to constrain a real nested call. Freeze the grouping, gates and other fields and apply a single P1 edit to one of the three inner leaf inputs. With the other operand fixed, a change at one coordinate spreads only to that coordinate and its immediate neighbor. A change in the left input can move one index forward. A change in the right input can move one index backward. Two such operations spread each of the two affected input coordinates to at most three consecutive cyclic slots, even when their orientations differ. The resulting right-operand change has support at most six. Its outer Jacobian difference therefore has rank at most six. The argument relies on the same grouping on both sides and alteration of only one inner argument. It also rejects the already published rank-eight matched-inner-gate comparison as the result of such a single edit.

There is a stronger direct test for monotone ancestral contraction alone, allowing arbitrarily many deletions under one fixed address alignment. A removed coordinate must be zero in the final zero-extended state. Every removed nonzero entry can change only its own slot and its final retraction target after composition. No nonzero entry of \(q^{(3)}\) is zero in \(q^{(4)}\), and only index 2 of \(q^{(4)}\) is nonzero and then zero in \(q^{(3)}\). A direct sequence in either direction could therefore differ in at most zero or two slots, respectively. The actual difference uses ten. Intermediate recombination or a changing identification of operands would require a separately sourced equation. For a fixed initial grade and fixed final retained carrier, functoriality also gives the same final grade for every monotone deletion order.

The exact replay finds zero direct matches over 264 initial-arm/merger choices and zero matches over 792 fixed-grouping/inner-input/merger choices. It uses the original signed fields and gates. None of those finite default-input trials even matches the one-site 207 difference in either direction. This last finding is bounded to the original supplied fields. It is not an amplitude-independent one-site obstruction. For example a free leaf transfer of 23 in the B3 inner input \(J_3\) for \(0\to2\) gives the same one-site coefficient \(9\cdot 23=207\) while the full operator change is still of rank at most six. In the replay this is the linear extension of the tested unit direction, not the native grade at slot 0 of the archived \(J_3\).

## Descent of the full output

Let \(q\) be fixed and known and consider first whether *any* map of \(Px\) can give \(P R_n(x,q)\) for all rational \(x\). The latter is affine in \(x\). It factors exactly when its linear part annihilates the direction \(d=e_u-e_p\), which spans \(\ker P\). This is weaker than the specific identity
\[
P R_n(x,q)=R_{n-1}(Px,Pq),
\]
where the coarse successor skips the deleted slot. The constant offsets agree automatically. To compare the linear parts, the fine correction in column \(j\) is \(q_{\sigma j}(e_{r(\sigma j)}-e_{r(j)})\). In the coarse rule it is \((Pq)_{\sigma'(r(j))}(e_{\sigma'(r(j))}-e_{r(j)})\).

Write \(a=\sigma^{-1}u\) and \(b=\sigma u\). For \(n\ge3\) and \(\gamma\ne0\), these two column tests give the following exact conditions.

| Parent | Any factor through \(Px\) | Same cyclic rule |
|---|---|---|
| \(p=a\) | \(q_b=0\) | \(q_b=q_u=0\) |
| \(p=b\) | \(q_{\sigma p}=0\) | \(q_{\sigma p}=q_p=0\) |
| Otherwise | \(q_b=q_{\sigma p}=0\) | \(q_b=q_{\sigma p}=q_u=0\) |

For \(p=a\) the internal fine edge from \(p\) to \(u\) vanishes after projection, requiring the competing outgoing coefficient from \(u\) to vanish. The edge entering \(p\) then tests whether folding \(q_u\) changes its coefficient. For \(p=b\) the internal edge is reversed and the predecessor \(a\) now sees the folded grade at \(p\), giving the second row. When the parent is neither neighbor, the two outgoing projected columns from \(u,p\) point in distinct directions. Both coefficients must vanish. The fine and induced coarse successors of \(a\) also differ, requiring \(q_u=0\). The additional discrepancy at the incoming edge to \(p\) then also vanishes. These tests exhaust the changed columns.

Write \(s=q^{(3)}-q^{(4)}\). The contrast is \(s+\gamma B_\sigma(x,s)=R_n(x,s)-x\), so the same conditions apply to its entire affine output. The literal fine vectors have zero sets \(\{2,11\}\) for \(q^{(3)}\), \(\{11\}\) for \(q^{(4)}\), and \(\{10,11\}\) for \(s\).

| Archived operand or contrast | Full output factors by some map | Full output by the same coarse rule | Site 3 by some map | Site 3 by the same coarse rule |
|---|---:|---:|---:|---:|
| \(q^{(3)}\) | 6 | 0 | 90 | 73 |
| \(q^{(4)}\) | 2 | 0 | 90 | 73 |
| \(s\) | 4 | 2 | 90 | 74 |

The full-output columns span all 132 maps. The read columns use the 121 maps retaining site 3. If the original probe sites 2 and 10 must both remain as well, the same-law row works for the same 65 maps in all three cases. This is a check of the entire row on all left-input vectors, beyond retaining just the previously measured coefficient. The full-response obstruction therefore cannot be used as a general null for the selected read.

The two full same-law contrast mergers are \(9\to10\) and \(10\to9\). Both individual arms have the identical nonzero difference between their fine-projected and coarse Jacobians,
\[
-12(e_p-e_8)e_8^\top,
\]
because both have \(q_{10}=4\). The exact coarse contrast retains rank 10 and the 207 probe difference, with the compensating probe pushed by P1 when site 10 is removed. A conservative response in ten or fewer retained sites has contrast rank at most nine. It could not preserve all ten independent response directions from these two particular comparisons. The survival result compares two supplied right operands. It gives no event that chooses them.

## Why both freely varying inputs require more data

The monomial check is decisive for the stronger proposed interpretation with both grades free. For a proper quotient of a finite simple directed cycle with at least two distinct retained fibers, choose a nonsingleton fiber and a crossing edge entering it. Such an edge exists because the cycle is connected and the fiber is proper. Let its fine tail be \(j\) and its head be \(k\), and let \(k'\ne k\) be another member of the head fiber. Use the same \(x=e_j\) and compare \(q=e_k\) with \(q=e_{k'}\). The P1 totals of both arguments coincide. The bilinear correction projects to a nonzero coarse edge for \(k\) and to zero for \(k'\), since \(j\) has just one successor. Thus there is no function of the two P1 marginals that returns the entire projected original output for all inputs. This does not require guessing the coarse operator.

For one merger the two missing fine directions in the inputs are \((d,0)\) and \((0,d)\), where \(d=e_u-e_p\). A linear summary sufficient on all inputs cannot identify two inputs separated by any nonzero pair \((\alpha d,\beta d)\). Varying the right argument over all backgrounds detects the first component on an outgoing crossing of the merged fiber. Varying the left argument detects the second on an incoming crossing. Invariance for all backgrounds thus forces \(\alpha=\beta=0\). At least two extra linear scalars are required and restoring one original fine value per argument suffices. In the fixed-right-operand setting the earlier column test decides between zero and one extra scalar. This is an information requirement of this candidate software interface.

## Evidence and next causal step

The [protocol](RECOMBINATION_P1_PROTOCOL.md) records the known analytical boundaries before running the finite replay. The [checker](check_bracket_pruning.py) reconstructs the historical input/gates, checks 1,584 original P1 basis pushes, evaluates actual operations as rational arithmetic, and compares against independent column conditions. It also checks 264 positive two-input controls for the two lost directions. Download [the complete result](evidence/recombination_p1/pruning_interface.json.gz) or read the [summary and checksum](evidence/recombination_p1/summary.json).

The viable interface would have to change a grouping, gate, or effective right input through a named inherited event operation. The literal one-event grade insertion at a fixed grouping cannot account for the archived matrix. A narrower existing-site observable could still be viable if a native operation produces it and a receiver reads it. No externally declared measurement, underlying spatial identification, or new conversion from these units to gravity is used here.
