# V1712 state-dependent patch update and geometric readout

This is a source-level result in the archived V1712 model. The physical event, ownership and gravitational correspondence remain open.

## Source boundary

- INHERITED in the archived model: [V1712](https://github.com/proteinfoldingengine/WetLabEngine/blob/e7e01bab68ba5171dacd91333f98d208d810dac3/Tmp/TOE/Einstein_13_V1720%20retained_bridge_core/v1712_rg.py) defines cyclic transport at lines 8–9, the metric and non-metricity tensor at lines 11–36, the patch writer at lines 41–48, and its caller at lines 50–60. Git blob: bc4504edbde3bc35815959f7f52288a57dced81a.
- INHERITED in the foundational P1 model: the extensive grade of a removed fiber sums into its nearest retained ancestor. The comparison below only tests identifying two V1712 patch vectors with grades of a single P1 fiber by literal coordinate addition.
- SUPPLIED in V1712: Gaussian starting patch states, a coupling constant and pairing by adjacent list index. SUPPLIED in this check: the controlled initial patches in §3. The original caller uses the written patch in its next scale's statistic.
- ACCEPTED INPUT: an actual atemporal occurrence. Its association with this computation and a physical receiver's access are open.

The [V1472.20 adapter](https://github.com/proteinfoldingengine/WetLabEngine/blob/e7e01bab68ba5171dacd91333f98d208d810dac3/Tmp/TOE/Einstein%207/v1472_20_uci_candidate_package/v1472_20_uci_incident_adapter.py#L107) constructs a disorder proxy from incident fields, sorts within a ticket by timestamp and modification count, and uses the preceding row's ID in the written record. V1712 takes patch arrays and performs its own adjacent pairing. No input or output binding between these two callers is evidenced in their source. The V1700.20 and V1700.21 archive members with a Python extension are report stubs. Their printed status and saved tables supply no executable producer for a binding.

## 1. What the writer retains

Let \(S\) denote the cyclic shift, \((Sv)_i=v_{i-1}\), and use zero-based indices modulo \(n\). Let \(a,b\) be the left and right input patches and let \(g\) be the real coupling used for both calls. Exactly in real arithmetic, substitution of native_T in rg_step gives

\[
 F(a,b)_i = a_i + g^2(a_i b_{i-1}-a_{i-1}b_i).
\]

Thus the right-patch contrast \(d\) writes \(\Delta F_i=g^2(a_i d_{i-1}-a_{i-1}d_i)\). The caller replaces its patch list with the returned list and evaluates Qtensor on the returned states at the next scale when there are at least two patches, limited to the first 40. The patch operation is scheduled by list positions. The state determines the value written.

For nonzero \(g\) and every \(a_i\ne0\), the kernel of the right-input map \(d\mapsto\Delta F\) is exactly \(\mathrm{span}(a)\). Indeed, dividing the zero equation by \(a_i a_{i-1}\) equates consecutive ratios \(d_i/a_i\) all around the cycle. The rank is \(n-1\). When \(\sum a_i\ne0\), distinct right inputs of equal total necessarily produce distinct patch states under these hypotheses. A contrast parallel to \(a\) is invisible to every subsequent read of the written patch. Such a contrast changes the literal P1 sum \(a+b\), so the two operations differ on this interface.

## 2. What the existing geometric read sees

Use the historical dimension \(n=6\). In a neighborhood where the eigenvalue floor is inactive, the metric is \(G(q)=(J(q)+J(q)^T)/2\), where \(J(q)=I+g[\operatorname{diag}(q)S-\operatorname{diag}(Sq)]\). Its derivative is constant in \(q\), and \(A_k=\partial_k J=g(e_ke_{k-1}^T-e_{k+1}e_{k+1}^T)\). The tensor in the original code is

\[
 Q_k(q)=\partial_k G(q)-A_k^T G(q)-G(q)A_k.
\]

This is affine in \(q\). In particular \(Q_{k,k+1,k+1}(q)=g-2g^2q_k\), so a changed patch has a changed full tensor in this regime if \(g\ne0\). In exact arithmetic the archived centered differences agree with these derivatives when their evaluations stay in the region. The caller reads the tensor's Frobenius norm and reports its median across patches.

At \(q=\mathbf 1\), cyclic shifts leave \(Q(q)\) invariant under simultaneous shifts of its three indices. The linear change \(L(d)=Q(\mathbf 1+d)-Q(\mathbf 1)\) is cyclic-equivariant. The linear functional \(d\mapsto \langle Q(\mathbf 1),L(d)\rangle_F\) is therefore a constant times \(\sum_i d_i\). For any zero-sum nonzero \(d\) with both neighborhoods in the no-floor region, the squared-norm difference is \(\|L(d)\|_F^2>0\). The fixed caller statistic can therefore respond even with no new measurement functional.

## 3. Fixed replay and controls

Use \(g=17/100\), \(a=\mathbf1\), and four input patches \((a,b,a,a)\) in their original list order. Hold the left patch and the second pair fixed. The baseline is \(b=4a\). The contrast arm is \(b=4a+3(e_0-e_1)\), with equal positive totals. The first coarse patch changes from \(a\) to \(a+3g^2(-e_0+2e_1-e_2)\). The second coarse patch is \(a\) in both arms. Both first coarse patches and their finite-difference neighbors have \(\|q\|_\infty<1.18\). The diagonal-dominance bound \(1-2g\|q\|_\infty>0.59\) keeps the floor inactive.

At block size 1 the median equals the read of \(a\) by three identical entries. At block size 2 it stays there for the baseline and increases for the contrast arm, by exactly half the increase in the first coarse patch's norm. The original loop skips the terminal singleton. The independent checker compares the unchanged original caller (feeding the four declared inputs instead of Gaussian draws) to a rational implementation of the write and tensor. It also runs these controls:

1. Shift the contrast cyclically by one slot. The written vector still changes, and the original medians agree with the unshifted contrast because the norm forgets orientation.
2. Set \(b=5a\). The extensive right-patch total changes, and the written vector and both medians agree with the baseline.
3. Set \(g=0\) and keep the baseline and positive contrast inputs. Both runs have zero tensor and identical written vectors.

The distinguished patch in this program is fixed by the original caller. Thus a comparison that reroutes its difference to another patch would change this software contract. The proof supplies no restriction on the physical realizations \(W_R,W_E\): both remain admissible under the established P1 source-only premises. The patch values have no established physical source units, and the caller's non-metricity statistic has no established correspondence to a physical gravity observable.

