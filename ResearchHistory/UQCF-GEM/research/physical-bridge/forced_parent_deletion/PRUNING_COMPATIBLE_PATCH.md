# Which patch writes can commute with retained pruning?

This checkpoint continues the V1712 producer search at parent `3f111dc570de0c1c4009c0728794a68aeb103e9e`. It identifies an obstruction that survives changes of patch coordinates and classifies the matching alternating-bilinear laws on inherited tree grades. Native physical receiver delivery remains open.

## Inputs and scope

- INHERITED: the finite additive grade, nearest-retained-ancestor pushforward \(P_{XY}\), supplied zero-extension section \(I_{YX}\) as an available map, and [FCV P1–P2](../../../foundational-closure-verification/PROOFS.md). The [v16.23 proof, §O3](../../../demos/v16.23-overlap-descent/PROOFS.md) gives invertible subtree-sum coordinates. Section O4 gives the existing common-port comparison for the linear Green response.
- INHERITED in its archived model: V1712 `rg_step` and its next-scale caller. The earlier [frozen proof](V1712_PATCH_WRITE.md) showed that it uses a directed cyclic stencil on a six-component patch. V1713 repeats the stencil and initializes a separate patch list. Both modules import NumPy and construct their initial patch values with their own Gaussian draws.
- INHERITED in the historical software: the v16.42 normalizer reads membership, changes masks and returns a path. Its producer converts that path to graph state indices. Its verifier checks those indices, the cover budget and individual edits. The fixed \(q\) of this producer is a minimum-cover target, not an extensive source or patch field. The inspected caller and verifier do not pass a distinct intermediate mask into V1712 or V1713.
- SUPPLIED for the mathematical comparison: two signed real grades on one common rooted carrier, an alternating-bilinear correction \(B\), and commutation with the indicated pruning and section maps. This is a test of a candidate compatibility condition for the V1712 identification. It is not a proposal to fit coefficients or adopt a physical interaction. Actual atemporal occurrence is ACCEPTED INPUT and unused in the proof.

## 1. Exact form of a commuting correction

Let \(a,b\) be grades on a finite rooted tree \(X\). For a vertex \(v\), let \(c_v(a)\) be its subtree sum, with \(c_o(a)\) the total at the root. The inverse subtracts the sums of the immediate child subtrees. The coordinates are simply restricted along \(P_{XY}\), as every removed descendant of a retained vertex retracts to a retained ancestor still in that vertex's subtree. Along \(I_{YX}\), the coordinates in \(Y\) are unchanged and those outside \(Y\) are zero, since \(Y\) is prefix closed.

Suppose alternating-bilinear \(B_X(a,b)\) is a grade on the same carrier, and members of this family satisfy

\[
P_{XY} B_X(a,b)=B_Y(P_{XY}a,P_{XY}b).
\]

Projecting \(X\) to the root-to-\(v\) chain shows that the output coordinate \(c_v(B_X)\) depends only on the input subtree sums along that chain. Alternation then makes it a linear combination of the wedges of distinct chain coordinates. At the root the chain has one coordinate, so \(c_o(B_X)=0\) on every pair. This root constraint uses P1 alone.

If the family also satisfies \(B_X(I_{YX}a,I_{YX}b)=I_{YX}B_Y(a,b)\), apply it to a strict ancestor chain zero-extended to the chain ending at \(v\). The output at \(v\) must vanish when both input coordinates at \(v\) vanish. All ancestor-ancestor wedge coefficients are therefore zero. For each nonroot \(v\) the complete form is

\[
c_v(B_X(a,b)) =
\sum_{u\prec v} \lambda_{vu}
\big(c_v(a)c_u(b)-c_v(b)c_u(a)\big).
\]

Here \(u\prec v\) means strict ancestor. Every such family with the same coefficients on retained copies of the same lineage satisfies both identities. For \(v\) retained, all its ancestors and their coordinates survive. For \(v\) outside the zero extension, both its input coordinates vanish. Hence pruning alone permits \(\sum_v {d(v)+1\choose 2}\) independent coefficients on a fixed carrier and all its retained subsets. Pruning with the section permits \(\sum_v d(v)\). These counts concern labeled lineage coordinates with no additional symmetry conditions.

## 2. No additive coordinate identification of the V1712 write

Write the unscaled V1712 correction \(K(a,b)_i=a_i b_{i-1}-a_{i-1}b_i\), with indices modulo six. For each \(i\), \(K(e_i,e_{i-1})=e_i\). The correction therefore spans the whole patch space. For any invertible linear identification of the patch output with a six-coordinate extensive grade, the total defines a nonzero linear covector on that patch. The root constraint in §1 would make that covector annihilate the entire image of \(K\), a contradiction. This obstruction uses only the root projection of P1 and permits independent invertible input changes of coordinates.

There is a separate obstruction to treating the full update \(F(a,b)=a+g^2K(a,b)\) as a two-to-one extensive grade transfer. Even with arbitrary scalar functions \(m_\mathrm{out},m_L,m_R\), the identity \(m_\mathrm{out}(F(a,b))=m_L(a)+m_R(b)\) for all real patches makes \(m_R\) constant. Indeed, \(F(a,0)=F(a,a)=a\) for every \(a\). Comparing these two inputs forces \(m_R(a)=m_R(0)\). A right hand grade capable of distinguishing two right patches cannot satisfy that identity. The claim concerns a separately defined grade on each input and the full real patch domain. It leaves open models in which a separate event first writes a state, or models with additional input restrictions or event-dependent information.

## 3. Before the actual retained histories merge

Use the original v16.42 four-leaf fixture and the already recorded preparations \((A,B)=(21,11)\) and \((29,11)\). At entry to the common second-leaf operation `setleaf(leaves[1], B)`, the respective mask pairs are \((23,9)\) and \((27,13)\). Leaf 2 is absent and present, respectively, in B. The original routine tests that bit. Both histories later reach \((27,29)\).

At this common invocation the B carriers intersect in \(\{o,3\}\). They hold \(c_o\) and \(c_3\) of each input if both preparations are restrictions of the same two ambient grades. Under this stated matched-source condition, every correction in §1 gives the same result on the common carrier by P1. In particular, B's extra transient leaf cannot by itself change the shared root–3 edge in the existing Green read, which uses the shared subtree grade. This is a conditional common-port test using the inherited response and comparison. A transient bit can distinguish these software histories while that shared source-geometric read stays equal. Any claimed contrast on the common carrier needs a difference in its pruning-visible grade inputs or a producing operation outside this commuting grade class. Access by a physical receiver is a further open premise.

## Frozen replay

Re-execute the two exact historical paths and observe the bit-read call before it mutates the mask. Validate the original selected four-leaf family with the historical verifier. For the separate common-port control, fix the two ambient grades to \((2,3,5,7,11)\) and \((3,1,2,4,8)\) in vertex order. Project each into B and apply the published v16.22 grounded Laplacian as a diagnostic. The root–3 edge reads 7 and 4 respectively for these two grades, in each history.

Independently build rational coefficient constraints from the archived `Pruning.aggregate` on every prefix-closed subset of three fixed five-vertex trees. Use the rooted star, the tree with parents \((-1,0,1,1,3)\), and the rooted chain. The respective predictions are 16, 7 and 5 retained subsets, P1-only dimensions 4, 13 and 20, and P1-plus-section dimensions 4, 8 and 10. Distinct dimensions on the two deeper trees check the effect of the section requirement. Finally replay the six oriented basis pairs in the original V1712 write using exact rational arrays and verify full rank, the two right-insensitive inputs in §2 and preservation of their left patch. Pin all original source bytes. Any disagreement with these predictions is a failed check. These finite checks audit the proof within their stated mathematical and software scope.
