# Sharp tolerance of retained-reference leakage in the fixed receiver effect

Date: 2026-11-13 UTC. Author: proteinfolding-gpt / dot.
Integrated parent: `2ab565c3f5bf10305a96ddeef30901de49959ba5`.
Status at freeze: AUTHOR CONDITIONAL ARGUMENT; independent review pending.
Native bridge **NOT_DERIVED**. No numerical execution or numbered-stage certification.

## 1. The bounded follow-up and premise ledger

Following the user's “Next,” relax only exact quiet-reference behavior in the accepted conditional PR145 argument. Keep the original proper qubit receiver R, its initial blank |0>, fixed effect F_R=|1><1|, exact source channel and fixed diagonal source pair. No effect is optimized or rotated, and E tensor R never replaces R. This is robustness only to reference leakage, not to channel error, mixed initial R, uncertain spectrum or an unearned physical interface.

**SUPPLIED:** S has basis (o,p,u,v), Q=I-|u><u|,

    C(rho)=Q rho Q+rho_uu |p><p|,
    rho_+=diag(1,1,2,1)/5,  rho_-=diag(1,1,1,2)/5.

The initial state is rho tensor tau_E tensor |0_R><0_R|, with fixed E dimension d>=1 and qubit R. A fixed, preparation-independent unitary U on S,E,R implements C for every system input after tracing E,R. The physical typing, factorization, preparation and availability of F_R remain supplied. **ACCEPTED INPUT:** the event occurs; no physical time is introduced.

**NEW resource premise:** tau is full rank, with known eigenvalues lambda_1>=...>=lambda_d>0, sum lambda_i=1. This is the full-rank case of the previously supplied bath benchmark, not a native deduction.

For basis inputs define

    q_0 = Pr(F_R | p),   q_u = Pr(F_R | u).

Exact C makes q_0 identical for every retained basis input. **NEW QR_epsilon:** q_0<=epsilon, with a fixed 0<=epsilon<=1. This is a reference-output constraint, not an imposed outcome on u. The old QR is epsilon=0. Neither condition has a derived native producing operation.

For the same diagonal pair, the signed contrast is

    Delta = Tr[F_R(omega_R(rho_+)-omega_R(rho_-))]
          = (q_u-q_0)/5.

All findings below were analytically known before this freeze. This is a general proof review, not a prospective numerical discovery or an empirical noise estimate. The exact QR theorem and its scope correction are pinned to PR145 head `fe4a49b9093cc1e24c619d84ec646d9f6d075de0`, which is reviewed but not merged into the integrated parent. Its explicit lack of a robustness theorem is the immediate scope being extended here; no archive-wide or literature novelty is claimed.

## 2. Sharp minimum and exact signal threshold

Let L_j be the sum of the j smallest bath eigenvalues and H_j the sum of its j largest, with L_0=H_0=0 and L_d=H_d=1. For epsilon in [L_j,L_{j+1}], 0<=j<d, define

    T(epsilon)=H_j+(lambda_{j+1}/lambda_{d-j})(epsilon-L_j).

Adjacent definitions agree at endpoints; T(1)=1. Then the exact minimum over every implementing U satisfying QR_epsilon is

    min Delta = [1-epsilon-T(epsilon)]/5.                      (1)

The minimum is attained by a full-channel unitary with q_0=epsilon. Define

    epsilon_* = L_n                             if d=2n,
    epsilon_* = L_n + lambda_{n+1}/2             if d=2n+1.

Every admitted implementation has strictly positive Delta if and only if epsilon<epsilon_*. At equality an admitted implementation is blind to the fixed effect. For larger epsilon that same blind implementation remains admitted, so no nonzero fixed-effect contrast is guaranteed, even though the minimum *signed* contrast is negative. More precisely,

    min |Delta| = max(0, [1-epsilon-T(epsilon)]/5).             (2)

Equation (2) concerns this one effect. Equal probabilities do not in general mean equal complete receiver states.

## 3. Proof for every exact implementation

### 3.1 Full-rank frames exhaust the complement

Diagonalize tau in the occupied E basis e_i. Purity of each basis-state system output and positivity of every lambda_i force

    U|s,e_i,0>=|s>|a_i>   for s=o,p,v,
    U|u,e_i,0>=|p>|b_i>.

The common a_i across all retained s follows by retaining their coherences: sum_i lambda_i <a_{t,i}|a_{s,i}>=1, and a positive average of normalized overlaps can equal one only if each overlap is one. Unitarity on |p,e_i,0> and |u,e_j,0> gives cross-index orthogonality, so the a and b frames are separately orthonormal and mutually orthogonal for all i,j.

There are 2d frame vectors and dim(E tensor R)=2d. Thus together they form a complete orthonormal basis. This saturation uses both full rank and the unchanged *qubit* receiver; it is not asserted for a larger receiver or rank-deficient bath.

### 3.2 Opposite spectral allocations bound leakage

Let P=I_E tensor F_R, a rank-d projection. Put

    alpha_i=<a_i|P|a_i>,
    gamma_i=1-<b_i|P|b_i>.

All entries lie in [0,1]. Completeness of the two frames and Tr P=d give

    sum_i alpha_i=sum_i gamma_i=:t,
    q_0=sum_i lambda_i alpha_i,
    q_u=1-sum_i lambda_i gamma_i.

For t=j+x, integer 0<=j<d and 0<=x<=1, elementary exchange of diagonal weight gives

    sum_i lambda_i alpha_i >= L_j+x lambda_{d-j}=:L(t),
    sum_i lambda_i gamma_i <= H_j+x lambda_{j+1}=:H(t).

The first minimum fills the smallest weights first; the second maximum fills the largest weights first, with each slot bounded by one. At t=d both functions equal one. Positivity of the spectrum makes L strictly increasing, so L(t)<=q_0<=epsilon implies t<=L^{-1}(epsilon). H is increasing as well, hence

    sum_i lambda_i gamma_i <= H(L^{-1}(epsilon))=T(epsilon).

Therefore 5 Delta=1-q_0-sum_i lambda_i gamma_i >=1-epsilon-T(epsilon), proving the lower bound. No assumption that arbitrary diagonals are realizable is used in this step; explicit attainment supplies that part next.

### 3.3 Sharpness and full-channel extension

For epsilon in [L_j,L_{j+1}], set

    x_i=1                                      for i<=j,
    x_{j+1}=(epsilon-L_j)/lambda_{d-j},
    x_i=0                                      for i>j+1.

For each i let h=d+1-i and define

    a_h=sqrt(1-x_i)|e_h,0>+sqrt(x_i)|e_i,1>,
    b_i=-sqrt(x_i)|e_h,0>+sqrt(1-x_i)|e_i,1>.

These are independent rotations of disjoint two-dimensional coordinate planes. They form two mutually orthogonal orthonormal frames, with

    q_0=sum_i lambda_{d+1-i} x_i=epsilon,
    q_u=1-sum_i lambda_i x_i=1-T(epsilon).

Use these frames in Section 3.1's prescription. Its 4d input images are orthonormal in the full 8d-dimensional S,E,R space and therefore extend to a unitary. All retained source matrix units are preserved; the u population resets to p; u-to-retained source coherences vanish after tracing E,R because the frames are orthogonal. Thus the exact all-input source channel is C. This proves attainment of (1), including epsilon=0 and 1.

The noisy-reference theorem does **not** claim that every receiver probability for a coherent source input is the population-only affine formula q_0(1-rho_uu)+q_u rho_uu. Without exact QR, cross terms involving <a_i|P|b_i> can survive in the receiver. The fixed pair here is diagonal, so its contrast uses only q_0,q_u. Channel equality on coherent inputs is nevertheless required and verified as above.

### 3.4 Threshold and absolute contrast

The continuous function epsilon+T(epsilon) is strictly increasing from zero to two. For d=2n, L_n+H_n=1, so its unique crossing of one is L_n. For d=2n+1, the central segment has slope lambda_{n+1}/lambda_{n+1}=1; the crossing is L_n+lambda_{n+1}/2. This proves the stated epsilon_*.

Below epsilon_*, (1) is positive and attained, so it also minimizes absolute contrast. At epsilon_* the construction has Delta=0. Because the admitted condition is q_0<=epsilon, this zero-contrast construction is admitted at every larger epsilon. This proves (2) without confusing a negative signed minimum with an absence of information in every implementation.

## 4. Exact analytical checks and controls

- Epsilon=0 recovers the full-rank exact-QR contrast 1/5.
- For 0<=epsilon<=lambda_d, T(epsilon)=(lambda_1/lambda_d)epsilon, so the condition-number bound `[1-(1+lambda_1/lambda_d)epsilon]/5` is exactly sharp. Beyond that first segment it is generally only a weaker lower bound, not the sharp formula.
- For a uniform bath, T(epsilon)=epsilon for any d. Thus min Delta=(1-2epsilon)/5 and epsilon_*=1/2. In particular d=1 has no external E storage; at the threshold a,b may be |+>,|->. The fixed effect is blind although the full receiver states differ. This rejects interpreting (2) as complete-receiver blindness.
- For d=2, lambda=(a,b), a>=b>0, a+b=1,

      min Delta=(b-epsilon)/(5b)      for 0<=epsilon<=b,
      min Delta=(b-epsilon)/(5a)      for b<=epsilon<=1.

  The threshold is b. At q_0=b the displayed construction can make the entire receiver output constant diag(a,b); this is a special stronger control, not a general inference from zero fixed-effect contrast. With (a,b)=(9/10,1/10), epsilon=1/20 gives minimum contrast 1/10, while epsilon=1/10 already admits zero contrast. These are exact substitutions, not simulation results.
- At epsilon=1, the minimum is -1/5. The blind threshold implementation is still admitted, so the minimum absolute contrast is zero.

## 5. Physical boundary

This quantifies the amount of new reference-output control required for a guaranteed response in the *same* receiver effect, conditional on a known full-rank bath and exact source channel. It does not show that the actual native event enforces any QR_epsilon, determine a real bath spectrum, identify the owner, or make the effect accessible. In particular, an empirical-looking tolerance parameter is not a derived physical mechanism.

No added numerical campaign, new source family, alternative receiver, optimally chosen detector, source recovery demand, multi-event claim, gravity fit, fundamental time, merger or numbered-stage closure is introduced. The next native question remains why the actual interaction constrains the nominated reference response and exposes the same effect. Conditional acceptance of this tradeoff cannot answer that question by itself.
