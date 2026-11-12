# RD-8 counterexample and corrected receiver-owned effect criterion

Date: 2026-11-01 America/Phoenix. Status: frozen author argument for independent review. Native bridge NOT_DERIVED. No priority or physical-realization claim.

## Scope, admission and assumptions

This is the bounded correction requested for full-stack completion after the source-level challenge at 60520667. It does not open another channel-classification program. The admission question is whether T-243 RD-8(iii)'s stated two-zero condition really suffices for full complementary ownership; the falsifier below answers no. Its correction is supporting mathematics, not the next native discovery.

INHERITED: native P1 pushes extensive grade at u to its retained ancestor p. SUPPLIED representation: normalized quantum diagonal inputs Pi(z) on H_S=span{o,p,u,v}, output atom images f(o)=o,f(p)=p,f(u)=p,f(v)=v, finite-dimensional isometric dilation W:H_S -> H_S tensor K, and a fixed factorization K=E tensor R when R is considered. These assumptions are the enlarged atom-compatible class used by RD-8, not the previously accepted exact coherent channel C. SUPPLIED physical identification: an actual receiver and access to all effects of its designated R factor. We do not derive that identification. Actual occurrence is accepted input and plays no role in this conditional linear-algebra calculation.

Pure source outputs imply W|j>=|f(j)>|e_j> with unit e_j. Isometry forces <e_u|e_p>=0 because f(u)=f(p). It imposes no other complement overlap zero between distinct source-output labels. Write tau_j^R=Tr_E |e_j><e_j|; N_R(Pi(z))=sum_j z_j tau_j^R. For the complete complement use tau_j^K=|e_j><e_j|.

The target here is the strong full-domain equation Tr[M N_R(Pi(z))]=z_p+z_u for every probability vector z, with one fixed effect 0<=M<=I_R. This is stronger than nonzero contrast for the original pair. Calibration atoms are mathematical inputs in the stipulated simplex; no physical preparability is asserted.

## 1. Explicit counterexample to the stated sufficiency

Choose K=C^2, e_p=|0>, e_u=e_v=e_o=|1>. Thus

 Wp=p tensor 0, Wu=p tensor 1, Wv=v tensor 1, Wo=o tensor 1.

The four columns are orthonormal. The channel Tr_K W(.)W* has the four required atom images. Both kappa_pv=<e_v|e_p>=0 and kappa_po=<e_o|e_p>=0. Yet N_K(pi_u)=N_K(pi_v)=|1><1|, although their owner indicator values are 1 and 0. No fixed effect or source-independent K-only decoder can represent the full owner value.

For z+=(1,1,2,1)/5 and z-=(1,1,1,2)/5, in o,p,u,v order, both K outputs are diag(1/5,4/5). The formal owner values are 3/5 and 2/5. Thus the two-zero condition does not force even complete-complement contrast for this pair.

RD-8's favorable example proves existential attainability, not sufficiency for every fixed dilation satisfying those two conditions. This counterexample does not invalidate its trace-distance bound or the accepted exact-C owner exclusion; it uses RD-8's explicitly enlarged class.

## 2. Correct criterion for the designated R

Define A_R=span(supp tau_p^R union supp tau_u^R) and B_R=span(supp tau_o^R union supp tau_v^R). There exists a fixed R effect representing z_p+z_u on the whole simplex if and only if A_R is orthogonal to B_R.

Proof, necessity. The four atom calibrations require Tr(M tau_p)=Tr(M tau_u)=1 and Tr(M tau_o)=Tr(M tau_v)=0. For any density operator tau, positivity implies Tr(M tau)=0 only if M annihilates supp tau: Tr(tau^(1/2) M tau^(1/2))=||M^(1/2)tau^(1/2)||_HS^2=0. Apply the same reasoning to I-M when the expectation is 1. Therefore M equals identity on A_R and zero on B_R. Since M is self-adjoint, these eigenspaces are orthogonal.

Proof, sufficiency. If A_R is orthogonal to B_R, the orthogonal projector onto A_R is a fixed effect with the four required atom expectations. Linearity supplies the equation for every diagonal mixture. Unused directions in R do not affect the result; finite dimension and rank deficiency cause no exception.

For the complete complement K the condition reduces exactly to span{e_p,e_u} orthogonal to span{e_o,e_v}. All FOUR cross-block overlaps must vanish, not merely the two involving e_p. In the counterexample the two missing overlaps <e_o|e_u> and <e_v|e_u> are 1.

This is a necessary/sufficient mathematical criterion in an explicitly supplied representation class. It is not a derivation of the criterion from native structure, nor a minimal new physical postulate for weaker nonzero receiver contrast.

## 3. Standing informative/blind test after the correction

Fix E=R=C^3, each with basis 0,1,2, and use the same four-dimensional source. Two fixed-blank-compatible isometries are specified by complement vectors:

 informative: e_p=|0>_E|1>_R, e_u=|0>_E|2>_R, e_o=e_v=|0>_E|0>_R;
 blind:       e_p=|1>_E|0>_R, e_u=|2>_E|0>_R, e_o=e_v=|0>_E|0>_R.

Both are isometries. Their complete complement Gram matrices coincide, so their entire reduced source channels coincide, not just their atom images: each matrix unit maps to |f(j)><f(k)| <e_k|e_j>. Both satisfy all four complete-complement cross-block zeros. The receiver factor R and its dimension are fixed throughout; this is not an interface enlargement between comparisons. With a common blank input E,R, each isometry can be extended to a unitary on H_S tensor E tensor R by completing orthonormal bases, so that blank preparation supplies no obstruction. This is existence within the representation, not a native implementation.

For the informative member, A_R=span{1,2} is orthogonal to B_R=span{0}; M=|1><1|+|2><2| represents the owner value and has original-pair contrast 1/5. For the blind member every tau_j^R=|0><0|, so A_R=B_R=span{0} and every receiver contrast is zero. Initially both receivers may have the same fixed blank state.

These are new explicit calibration witnesses for the correction, not the old W_R/W_E of exact C. They are denoted informative/blind here to avoid changing the meaning of the accepted pair. The old pair remains valid in its own class. The corrected global condition still admits a blind designated R. The corrected R condition excludes it by demanding receiver ownership itself, but no inherited producer of that condition is established. No native constraint has newly changed the standing delivery verdict.

## 4. Disposition

DERIVED, conditional: counterexample to RD-8(iii); corrected support-span criterion and its pure-vector specialization; explicit common-source-channel informative/blind comparison. SUPPLIED: representation, dilation, output split, receiver identification/access, and any adoption of the support condition as a physical rule. Accessible effect contrast is 1/5 only for the supplied informative witness. No realization-independent nonzero contrast follows from the native premises inspected.

The inherited scientific infrastructure is unchanged. The unresolved discovery target remains an inherited joint-event or owner-retention operation that excludes the blind allocation while admitting an informative one. This review does not create such an operation, a laboratory prediction, or a physical signal.
