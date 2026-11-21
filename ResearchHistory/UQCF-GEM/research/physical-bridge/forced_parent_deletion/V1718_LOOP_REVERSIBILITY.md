# Source-dependent loops and reversibility in V1718

This is an open Path-A source and calculation checkpoint. It follows the [earlier V1698 source-to-geometry trace](V1698_SOURCE_TO_GEOMETRY.md) and uses the same outstanding test of a source distinction reaching an actual geometric calculation. The exact target is the [historical V1718 implementation](https://github.com/proteinfoldingengine/WetLabEngine/blob/6909feacd82e72ea1c7d67096a5ab3093de8b4fc/Tmp/TOE/Einstein_13_V1720%20retained_bridge_core/v1718_complete.py), Git blob `638e68d00762642d6b58f692e7a1747816752232`. Thread T-301 through T-307 already checked generic invertibility of the same kernel at an earlier version. This checkpoint asks what V1718's **actual loop and reverse readers** establish and gives a fixed-total contrast alongside matched reversing controls.

The V1718 routines are INHERITED as historical simulation code. Their eight-dimensional carrier, cyclic shift, coupling and Gaussian source initializer are SUPPLIED mathematical inputs. Scripted source values below are controlled inputs to those routines. Actual atemporal occurrence is ACCEPTED INPUT and is unused in the calculations. The P1 pruning of the retained tree is a separate operation from the vocabulary used in the archive. The calculations below use ordered updates and no physical time parameter.

## 1. The source does update a carried vector and a loop

`native_T` (lines 5–6) maps the carried vector \(x\) through \(M(q)=I+gA(q)\), where

\[
 (A(q)x)_i=q_i x_{i-1}-q_{i-1}x_i
\]

with indices modulo the dimension. `loop_drift` (lines 36–42) draws a vector and one source state at each of three vertices, then replaces `x` by `transport(x, nodes[(k+1)%nloop])` on every step. The next edge consumes the changed vector. A loop with the saved states \((q_0,q_1,q_2)\) reads the norm of \(H x\) with \(H=M(q_0)M(q_2)M(q_1)\). The later `trajectories` caller also updates and reads the carried vector, drawing a new Gaussian `q` per step (lines 52–64).

Hold \(q_0=q_2=0\), set \(g=17/100\), and change just \(q_1\) from \(e_0+e_2\) to \(2e_0\), using zero-based coordinates. Both supplied source totals equal 2. For the first state the only altered diagonal entries of \(H\) are at 1 and 3, each \(1-g\). For the second only entry 1 changes, to \(1-2g\). In dimension 8, a matrix whose only possible entries are diagonal or in the cyclic predecessor column has only the identity and full-cycle determinant terms. In this case at least one predecessor entry vanishes, so only the diagonal term contributes. Hence

\[
\det H(e_0+e_2)=(1-g)^2=0.6889,
\qquad \det H(2e_0)=1-2g=0.66.
\]

For \(x=e_3\), the norm returned by the original loop routine is respectively \(0.83\) and \(1\). Both loop maps are invertible and their different determinants preclude similarity, including any simultaneous change of basis at the base vertex. These are exact predictions for a fixed-total source-dependent closed-path operator. Here the source numbers reach the loop through the transported state, where a direct read in V1698.75 reached only the signed boundary calculation. The V1718 contrast is on its supplied synthetic carrier.

## 2. What the reverse and loop controls measure

For fixed \(g\), \(\det M(q)\) is a polynomial in \(q\) with value 1 at zero. Its zero set has Lebesgue measure zero and each independent Gaussian draw therefore gives an invertible map almost surely in exact arithmetic. This can also be seen by expanding the determinant into the two terms above. Specially chosen non-Gaussian values can give singular maps, for example \(q=e_0/g\) for \(g\ne0\), which annihilates \(e_1\). The finite-action claim is about the sampled fixed-\(q\) operation and the intended continuous Gaussian law. It does not assert uniqueness of the prior vector when the realized source is unknown or an inverse is inaccessible.

`fwd_rev` (lines 20–26) returns the relative error after \(M(q_i)M(q_j)x\), with separately drawn endpoint values. Invertibility of the forward map says that \(M(q_j)^{-1}M(q_j)x=x\). The code does not compare to this inverse. Feed \(x=e_1\), \(q_i=q_j=e_0\) through the original routine. Its forward factor is \(0.83\) and its error is \(1-0.83^2=0.3111\). Solving against the same forward matrix gives zero reconstruction error in exact arithmetic. Thus a nonzero reported reverse error is possible under an ordinary invertible update, even with the two endpoint values held equal.

The unpruned control (lines 7–13) exponentiates the skew part of \(A(q)\). Norm 1 for this control follows from orthogonality. For the same loop slots, use \(q_0=q_2=0, q_1=e_0\). The skew generator has the single plane \((e_0,e_7)\) with off-diagonal entries \(\pm g/2\), hence gives a nonidentity rotation by magnitude \(0.085\) radians in that plane. The loop reader returns norm 1 on \(e_0\). Direct multiplication on that vector gives a change of \(2\sin(0.085/2)>0\) in Euclidean distance. Norm preservation here cannot test equality of the returned vector or identity of the vertex loop operator.

## 3. The independently sampled trajectory has a norm signal without a pruning event

In the simulated model let the coordinates of a fresh \(q\) have zero mean and identity covariance, independent of the current deterministic or conditioned vector \(x\). Then

\[
\begin{aligned}
E[M(q)x\mid x] &= x,\\
E[\|M(q)x\|^2\mid x] &= \|x\|^2+g^2\sum_i(x_{i-1}^2+x_i^2)
= (1+2g^2)\|x\|^2.
\end{aligned}
\]

The mixed terms vanish by the stipulated moments and distinct coordinates. Iterating for \(L\) independent draws gives \((1+2g^2)^L\) multiplying the initial squared norm. V1718's closed walk uses each of its independently drawn source values once, so the formula applies also to its three-edge loop conditional on the initial vector. The one-step factor at the archived coupling is \(1.0578\). The reported sample mean of the norm is a different statistic from the expected squared norm. The raw vector, conditional on a known deterministic input, also has mean equal to that input even when the source draw is hidden. This last statement concerns equality of distributions and gives no single-trajectory recovery rule or receiver readout.

## Frozen reconstruction and disposition

Pin the byte-identical original source and execute only its original `roll`, `native_T`, `Jgen`, `invertible_T`, `fwd_rev` and `loop_drift` definitions. The other runner code and original random campaign are outside the replay. Prescribe the draws strictly in caller order and reconstruct each matrix and determinant independently from the diagonal and predecessor entries. Compare the full matrices as well as the original scalar reads. Check repeated forward versus true inverse. Use a singular control and a dense full-cycle determinant control to discriminate a broken reverse test from actual rank loss. Check the orthogonal loop's nonidentity by its independently derived rotation. Verify the moment statements on the 16-point symmetric source sample \(\{\pm\sqrt 8 e_i\}\), which has the stipulated first two moments. No Gaussian sample-mean test is required or authorized by this checkpoint. Thresholds, specific vectors, analytic predictions and the source dataflow were known from inspection before freezing. Numerical execution and review follow the freeze.

The retained tree would have to determine an actual state or edge input in this writer, and a retained receiver would have to have justified access to its consequence. In V1718 `q` enters as an independent draw, the vector lives in a supplied fixed dimension, and the loop norm is computed by the host routine. The positive numerical source-to-loop route is established within this simulation. Its loop and reverse comparisons cannot justify the archive's pruning attribution. Native delivery and the identification of a pre-time gravity signal remain open.
