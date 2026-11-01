# T-240 preregistration — receiver-delivery boundary for the accepted P1 blind/informative pair

Date: 2026-11-01 America/Phoenix (MST). Author: proteinfolding-grokbot (UQCF Science Agent).
Parent (verified with `git ls-remote` at 06:39 MST): research/uqcf-overlapping-guard-exchange = dbe016b6f15298280650a50025fe7f20f123b2da.
Governing direction: Aaron Spradlin's Receiver Delivery Frontier directive (2026-11-01): constrain the missing relation
"native event/source update -> receiver-owned retained output", using the accepted blind/informative pair as the standing adversarial test.
This file is committed BEFORE any script for this stage exists or is run. No code has been executed for this stage.
Already-known exploratory findings (hand derivations only, disclosed): the realization parameterization of
p1_receiver_location_resolution/RESULT.md §5, and the hand-computed predictions listed in §4 below.

## 1. Canonical challenge (INHERITED, exact source)

p1_receiver_location_resolution/RESULT.md (blob 4182ba34, scientific freeze 812daac0, accepted run 40933321991, integrated by PR #124 merge 71694b92):
H_S = span{o,p,u,v}; C(rho) = Q rho Q + rho_uu |p><p|, Q = I - |u><u| (L28-30); Pi_X, Pi_Y diagonal encodings (L36-37);
pair z+ = (1,1,2,1)/5, z- = (1,1,1,2)/5 in order (o,p,u,v) (L48); blank output K = E (x) R, |0_E 0_R> (L53);
W_R|j> = |j>|0>|0> (j=o,p,v), W_R|u> = |p>|0_E>|1_R> (L59-60); W_E|u> = |p>|1_E>|0_R> (L80); W_R = (I (x) SWAP_ER) W_E (L82).
Every isometry implementing C has W|j> = |j>|e_0>, W|u> = |p>|e_u>, <e_0|e_u> = 0 (L103-108). Status SUPPLIED benchmark premises
(carrier, encoding, C, E/R interface), accepted as the canonical challenge.

## 2. Frozen definitions

- W(C,K): isometries W: H_S -> H_S (x) K with Tr_K(W X W^dag) = C(X) for every matrix X.
- Product receiver interface: A = A_S (x) B(K_A) (x) 1_{K_B}, K = K_A (x) K_B, A_S a unital *-subalgebra of B(H_S).
- Contrast: Delta_A(W) = max{ |Tr F (W rho+ W^dag - W rho- W^dag)| : F in A, 0 <= F <= 1 }.
- Retained-output contrast: Delta_{A_S}(C) = max{ |Tr F (C(rho+) - C(rho-))| : F in A_S, 0 <= F <= 1 }.
- Initial blindness of A_S: max{ |Tr F (rho+ - rho-)| : F in A_S, 0<=F<=1 } = 0 (with K blank, K_A starts in the same state).
- U(K)-invariant predicate: k(W) = k((I (x) U)W) for every unitary U on K.

## 3. Frozen claims to be proved analytically in RESULT.md (no finite check is a proof of these)

Lemma RD-0 (orbit). W(C,K) is exactly one orbit of {I (x) U : U unitary on K} (dim K >= 2).
Corollary RD-0' (rigidity). Every U(K)-invariant predicate is constant on W(C,K); in particular it cannot hold for W_R and fail for W_E.
Lemma RD-1 (invariance of inherited constraints). Every inherited structure in the directive's list, as found in its producing source,
defines a predicate that depends on W only through Tr_K(W . W^dag) and native carrier/grade data, hence is U(K)-invariant.
Theorem RD-2 (guaranteed receiver contrast). For a product interface with dim K_B >= 2:
  min_{W in W(C,K)} Delta_A(W) = Delta_{A_S}(C), attained by a realization whose u-branch record lies entirely in K_B.
Theorem RD-3 (complete complement). If K_B is trivial, Delta_A(W) is the same for all W in W(C,K).
Corollary RD-4 (minimal premise). Within product interfaces, a nonzero receiver contrast holds for EVERY realization admitted by
U(K)-invariant constraints iff Delta_{A_S}(C) > 0, or K_B is trivial and the complete-complement contrast is nonzero.
Lemma RD-5 (removed summand). In W_R the receiver R records z_u (the summand P1 removes from the fiber r^{-1}(p)), not the owner y_p = z_p + z_u.

## 4. Frozen finite check (bounded evidence only) and predictions

Domain: realizations W_E, W_R, W_M, W_N with K = E (x) R, basis |e r> ordered 00,01,10,11:
  W_E: e_0=|00>, e_u=|10>.  W_R: e_0=|00>, e_u=|01>.
  W_M: e_0=|00>, e_u=(3|10>+4|01>)/5.  W_N: e_0=(3|00>+4|11>)/5, e_u=|01>.
Each written as (I (x) U)W_E with an explicit rational orthogonal U.
Receivers: all 15 set partitions of {o,p,u,v} (A_S = span of block projectors) x 4 interface types
  T0 = A_S (x) 1_K, TR = A_S (x) B(R) (x) 1_E, TE = A_S (x) B(E) (x) 1_R, TK = A_S (x) B(K).
Pairs: canonical z+/z- and removed-summand control z'+ = (1,2,1,1)/5, z'- = (1,1,2,1)/5.

Predictions (exact rationals):
 P1. All four W are isometries with Tr_K = C on all 16 matrix units; W_R = (I (x) SWAP)W_E; each W = (I (x) U)W_E.
 P2. T0 and TK contrasts are identical across the four W for every partition and both pairs.
 P3. For TR and TE, min over the four W equals the T0 value for every partition; attained by W_E (TR) and by W_R (TE).
 P4. Trivial partition, canonical pair: T0 = 0; TR: W_E 0, W_R 1/5, W_M 16/125, W_N 9/125; TE: W_E 1/5, W_R 0, W_M 9/125, W_N 16/125; TK = 1/5 for all.
 P5. Exactly three partitions are initially blind with T0 contrast > 0: {o}{p}{u,v}, {o,u,v}{p}, {o,p}{u,v}; each has T0 contrast 1/5.
     The retained cone-total partition {o}{p,u,v} is initially blind with T0 contrast 0 (T-225 control must fail to separate).
 P6. Removed-summand pair: T0 = 0 for every partition; trivial partition TR: W_E 0, W_R 1/5; TK trivial = 1/5.
 P7. Rejecting scientific control: a U(K)-invariant predicate (equality of the Choi matrix of Tr_K(W . W^dag) with C's) is TRUE on all four W;
     the factor-naming predicate k_R(W) = [Tr_E|e_u><e_u| != Tr_E|e_0><e_0|] is TRUE for W_R, W_M, W_N and FALSE for W_E.

Rejecting controls the verifier must reject: wrong contrast value; missing record; duplicated record; substituted pair;
non-implementing realization (W|o> = |o>|01>); non-isometric realization (e_u = e_0); false blindness flag; false producer hash;
dropped partition; non-orthogonal U.

Competing outcomes: any prediction failing is recorded as RED and preserved; a failure of P3 or P5 would refute RD-2/RD-4 as stated.
Resource rule: one producer run and one verifier run per Actions attempt; at most one Gemini request. Stopping rule: stop on first RED, report.
Producer: produce.py (sympy 1.13.3, matrices and partial traces). Verifier: verify.py (stdlib Fraction only, own partition enumerator and index arithmetic).
