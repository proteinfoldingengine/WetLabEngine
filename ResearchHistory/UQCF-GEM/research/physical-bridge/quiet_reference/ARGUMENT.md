# Quiet retained reference and the sharp proper-receiver contrast bound

Date: 2026-11-12 UTC. Author: proteinfolding-gpt / dot.
Integrated parent inspected: `2ab565c3f5bf10305a96ddeef30901de49959ba5`.
Status at freeze: AUTHOR CONDITIONAL ARGUMENT; independent review pending.
Native bridge: **NOT_DERIVED**. No numbered-stage closure or certification.

## 1. Question, authorization, and fixed target

The user delegated a bounded investigation of explicitly labeled new physical assumptions, keeping the nominated proper receiver and its fixed effect unchanged. This note asks whether a condition on a retained reference input, together with the previously studied bath resource, forces source-dependent response in that same effect. It does not replace the receiver with the complete complement, change the effect after seeing an output, derive the new condition from native structure, or claim a general minimal physical premise.

The target is the existing qubit R, initially |0>, with the same effect F_R=|1><1|, and the source pair in `p1_receiver_location_resolution/RESULT.md`. E is outside this receiver's specified accessible interface. Neither E nor E tensor R is substituted for R. Allowing arbitrary finite d=dim(E) and rank k is the resource parameterization already used by T273-R. R remains a qubit throughout this note.

All results below were derived analytically before freezing this note. They are exploratory findings submitted for adversarial proof review, not prospectively discovered numerical results. No new scientific simulation or enumeration is proposed.

## 2. Premise ledger

- **ACCEPTED INPUT:** the relevant event occurs. Nothing here attempts to derive its occurrence or introduce physical time.
- **SUPPLIED benchmark:** H_S has ordered basis (o,p,u,v), Q=I_S-|u><u|, and the exact channel on every system input is

      C(rho)=Q rho Q+rho_uu |p><p|.

  Its physical correspondence to native P1 remains supplied.
- **SUPPLIED benchmark:** independently specified factors S,E,R; dim(E)=d>=1; dim(R)=2; initial product state rho tensor tau_E tensor |0_R><0_R|. A fixed unitary U, independent of the source preparation, implements C for every rho after tracing E,R. No source-dependent bath or additional uncounted purifying factor is allowed in this declared implementation class. An initially correlated extra factor would require a different analysis.
- **SUPPLIED resource parameter:** tau has rank 1<=k<=d and eigenvalues lambda_1>=...>=lambda_k>0, sum lambda_i=1. Eigenvalues are not chosen differently for the two sources.
- **NEW ASSUMPTION QR (quiet retained reference):** on input |p><p|, the final nominated receiver is exactly |0_R><0_R|. This restricts the interaction on one retained reference preparation; it does not directly prescribe its action on u.
- **NEW ASSUMPTION when invoked:** 2k>d, or the stronger full-rank condition k=d. Finite-temperature finite-dimensional Gibbs full rank is one supplied realization considered by T273-R, not a native result. The general theorem itself covers every k.
- **SUPPLIED source pair and available effect:**

      rho_+=diag(1,1,2,1)/5,
      rho_-=diag(1,1,1,2)/5,
      F_R=|1><1|=I_R-|0><0|.

  Their physical preparation and availability on the actual owner remain unearned.

Define omega_R(rho)=Tr_SE U(rho tensor tau tensor |0><0|)U^dagger and the signed contrast

    Delta_F=Tr[F_R(omega_R(rho_+)-omega_R(rho_-))].

The order of the sources and the effect are fixed. The theorem minimizes over all U meeting the premises; it does not select a favorable implementation.

## 3. The sharp conditional theorem

Set m=min(k,d-k). The admissible implementation class is nonempty for every d,k above, and

    min_U Delta_F = (1/5) sum_{i=m+1}^k lambda_i.                 (1)

In particular:

- If k=d, every admissible U has Delta_F=1/5 exactly.
- If 2k>d, every admissible U has a strictly positive fixed-effect contrast, bounded below by (1).
- If 2k<=d, a completely blank nominated receiver for every source input is attainable despite QR.

Thus 2k>d is necessary and sufficient for a positive uniform lower bound within this declared class and fixed spectrum. This is not a necessary condition for every particular signal-producing implementation.

### 3.1 Exact channel action fixes two orthogonal frames

Write tau=sum_i lambda_i |e_i><e_i| on its occupied support, and A=E tensor R. Because C sends any retained basis state s in {o,p,v} to the pure state |s><s|, positivity of the mixture and lambda_i>0 imply

    U|s,e_i,0>=|s>|a_{s,i}>.

Each a_{s,i} is normalized. For retained s,t, preservation of the off-diagonal operator |s><t| gives

    sum_i lambda_i <a_{t,i}|a_{s,i}>=1.

Every summand's real part is at most one. A strictly positive weighted average equals one only when every inner product is one. Hence a_{s,i}=a_i independently of s. Similarly C(|u><u|)=|p><p| implies

    U|u,e_i,0>=|p>|b_i>.

Unitarity on the occupied input vectors gives

    <a_i|a_j>=delta_ij,   <b_i|b_j>=delta_ij,
    <a_i|b_j>=0                                                   (2)

for all i,j. The last relation follows by comparing inputs |p,e_i,0> and |u,e_j,0>; it is stronger than orthogonality only at matching indices.

Conversely, any two mutually orthogonal orthonormal k-frames a,b define these images on the occupied input subspace. Their 4k system-environment images are orthonormal and can be completed to a unitary on the full 8d-dimensional S tensor E tensor R space. For each occupied i, the retained matrix units survive, u population resets to p, and every u-to-retained coherence vanishes by (2). Thus the resulting reduced map is exactly C on all system matrices.

### 3.2 Quietness on p propagates to the retained sector

Let B=E tensor span{|0_R>} and P_B=I_E tensor |0><0|. QR gives

    sum_i lambda_i <a_i|(I_A-P_B)|a_i>=0.

Every term is nonnegative, so each a_i lies in B. Therefore the entire retained Q sector has the same environment state sum_i lambda_i |a_i><a_i| and leaves R blank. This extension of QR to all retained inputs is derived from the exact channel; it is not a second calibration premise.

Let T=span{a_i}. Then T is a k-dimensional subspace of the d-dimensional B. By (2), each b_i lies in T-perpendicular. Its blank-R projection therefore lies in B intersect T-perpendicular, which has dimension d-k.

### 3.3 Spectral bound and signed contrast

Define leakage

    ell=sum_i lambda_i <b_i|(I_A-P_B)|b_i>.

The source difference is (|u><u|-|v><v|)/5, and QR makes v quiet. Hence Delta_F=ell/5. In fact Tr[F_R omega_R(rho)]=ell rho_uu for every input rho: retained terms vanish, and the cross terms vanish because I_E tensor F_R annihilates every a_i. This all-input statement follows within the supplied exact-channel benchmark; it is not imposed as an additional empirical calibration requirement for native success.

Let V map the ith coordinate to b_i and M=V^dagger P_B V. Then 0<=M<=I_k and rank(M)<=d-k. For Lambda=diag(lambda_i),

    Tr(Lambda M)<=sum_{i=1}^m lambda_i.                            (3)

A self-contained proof avoids any extra variational assumption: put h_i=M_ii. Positivity and M<=I imply 0<=h_i<=1; Tr M<=rank M<=m. For descending nonnegative lambda, the linear sum sum_i lambda_i h_i is maximized by allocating the available total weight m to its first m entries. Equivalently, moving weight from a later nonzero entry to an earlier unsaturated entry cannot decrease the sum, and unused weight can be filled since lambda_i>0. This proves (3), including m=0 and m=k.

Thus ell=1-Tr(Lambda M)>=sum_{i=m+1}^k lambda_i, proving the lower bound in (1).

### 3.4 Explicit attainment, without a hidden channel defect

Complete e_1,...,e_k to a basis of E and choose

    a_i=e_i tensor |0>,
    b_i=e_{k+i} tensor |0>     for 1<=i<=m,
    b_i=e_i tensor |1>         for m<i<=k.

All indices k+i used in the first case are <=d. These are mutually orthogonal orthonormal frames. Section 3.1 gives a unitary extension implementing the entire C, not merely the pair or the diagonal simplex. QR holds. The m largest eigenweights are blank and the remaining weights leak, so equality in (1) is attained.

At k=d no blank dimensions remain outside T=B, so every b_i lies in E tensor span{|1>}; ell=1 for every implementation. At 2k<=d, m=k and all a_i,b_i lie in B. Every source input then leaves R blank. This is an actual counterimplementation, not only a rank feasibility count.

## 4. Rejecting analytical controls

### Remove QR while keeping the same bath, receiver, effect, and channel

Let W_R on S tensor R swap |u,0> with |p,1> and fix the other basis vectors. It acts trivially on E and realizes C with R initially blank for any tau. Follow it by the qubit Hadamard H_R. The retained branch writes |+>_R, and the erased branch writes |->_R. Both have probability 1/2 for the unchanged effect F_R. Thus Delta_F=0 for every d,k, including full rank, while C is unchanged on every source input. This example is blind for the specified effect; it does not make the entire R state blind.

For the stronger complete-receiver blind control in the original qubit E,R setting, follow W_R by SWAP_ER. R is then tau independent of the source, including when tau is full rank; all receiver effects have zero source contrast. This violates QR. It is a countercontrol, not permission to rename E as the receiver.

### Keep QR but remove the bath-capacity threshold

The d=2,k=1 case of Section 3.4 is exactly the familiar W_E arrangement: the retained and erased branches occupy two orthogonal E states while R stays blank. It obeys QR and implements C on every source input. QR alone therefore does not stipulate the desired positive answer.

## 5. Relation to T273-R and to native ownership

T273-R (`constructive_candidates/t273_rank_refinement/ARGUMENT.md`) proved that for rho_*=(|p><p|+|u><u|)/2, output purity of R requires 2k<=d. Full rank therefore forces mixedness, but its SWAP control expressly prevented inferring a source record in R. The present note retains that boundary and adds QR explicitly. Orthogonality to the occupied *blank* subspace then forces a quantitative response in the already fixed effect. It does not infer delivery from mixedness alone, recover an unknown source, or solve the location ambiguity without an added premise.

The source channel, factorization, initial product state, resource constraint, quiet-reference behavior and actual receiver access are physical premises, not native deductions. In particular, no inspected native operation has been shown to enforce QR for the actual nominated owner. The next native obligation remains to justify the actual interaction/ownership/access relation. QR is one concrete conditional candidate to investigate, not a claimed universal weakest axiom or a replacement for that obligation.

The exact result is sensitive to support rank and exact quietness. Arbitrarily small positive eigenvalues still occupy support dimensions; no noise robustness or approximate-channel theorem is proved. The entropy/product-return restrictions of other possible models are not assumed or needed here. No external literature novelty, gravity law, physical energy or fundamental time claim follows.

Prior sources are read at the integrated parent named above; the separate review packet pins their exact blobs. Independent acceptance, if obtained, certifies only the stated conditional implications, not the supplied physical correspondence or a numbered-stage closure.
