# v15.75 — Affine open-state null classification

Parent: 7d6f4cf42cc7165da7861aae4b0a4ee8184927a2.
Branch: research/v15.75-affine-open-null.
No new scientific measurement precedes the missing-implementation RED.

## Frozen classification
For a fixed affine state-space vector field X(rho)=L(rho)+b, the hidden derivative Y_h=L(h) does not depend on rho. Test whether the historical twelve states already distinguish every nonzero retained component of a fixed Y. Use unchanged selected candidate indices [13,16,22,25,27,29,37,39,46,50,66,77] and all 27 lexicographic weight-three h=P/sqrt(8). No new randomness or selection.

The 36 retained output basis matrices G are concat(M.ONE,M.PAIR)/sqrt(8), using v15.71 order: nine one-body coordinates then 27 pair coordinates, edges (0,1),(1,2),(2,0). Append the 27 hidden h to complete the 63-dimensional trace-zero Hermitian output basis. For each rho form F_Q,F_E of shape (9,36), with columns the analytic connected-correlation and polar derivatives of G. Stack states to (108,36); append 27 zero hidden-output columns to obtain (108,63). Archive maps, singular spectra and null-projectors. This classifies constant output tangents; the 27 independent hidden input columns are a tensor multiplicity, not a new geometric dimension.

Rank thresholds [1e-9,1e-10,1e-11] times the largest singular value of the corresponding full retained map, for both retained and appended full-output maps. Projectors use 1e-10. Primary confirmation requires both stacked retained maps rank 36, appended maps rank 36, and appended null-projectors within Frobenius norm 1e-8 of diag(0_36,I_27). All thresholds must agree. Per-state ranks are recorded; rank nine is an analytic positive control. If full retained rank is achieved, deduce unrestricted hidden-response operator rank 972 and nullity 729 by tensor multiplication. These are linear-space dimensions, not dimensions of the CPTP cone.

Primary verdict: AFFINE_OPEN_NULL_RETAINED_CLOSED_CONFIRMED if valid and all primary criteria hold; AFFINE_RETAINED_NULL_NOT_EXCLUDED for a valid negative; INVALID for failed validity. The analytic open-state theorem is separately frozen in DERIVATION.md.

## Frozen physical channels
All three channels are fixed linear maps Phi. Use the CPTP source family T_s=(1-s)id+s Phi with s=.1, hidden step eta=1e-4 and mixture weight p=.37. No negative source strengths are used. Channel generators are X=Phi-id.

1. Depolarizing reset: Phi(z)=Tr(z)I/8. Its hidden derivative is -h, with zero retained response.
2. Entangling rotation: Phi(z)=U z U-dagger, U=cos(theta/2)I-i sin(theta/2)XXI, theta=pi/4. Its retained hidden response is sin(theta) times v15.73's commutator response; Q/E hidden-probe rank is six at every frozen state.
3. Engineered pointwise-null channel: anchor is candidate 13. Compute Y_ref once using v15.71 global_lift(anchor), then freeze it for ALL inputs. A=XXX, kappa=.01. Phi(z)=Tr(z)I/8+kappa Tr(Az)Y_ref. This equals measurement M_±=(I±A)/2 followed by preparation tau_±=I/8±kappa Y_ref, hence is CPTP. This intentionally uses the anchor geometry as a counterexample control; it is not offered as a derived physical source law. Its retained derivative for h=XXX/sqrt(8) is kappa sqrt(8)Y_ref; all other hidden retained derivatives vanish.

Secondary scientific confirmation requires engineered retained coefficient norm >1e-6, anchor Q and E norms divided by that retained norm <=1e-10, and non-anchor stacked Q and E norms divided by retained norm >1e-6. Report every state's visibility without requiring each non-anchor state to be visible. Secondary verdict CPTP_POINTWISE_NULL_ONLY_CONFIRMED or CPTP_POINTWISE_NULL_ONLY_NOT_CONFIRMED; INVALID if numerical validity fails. A pointwise null refers to the infinitesimal source response, not finite-strength polar invariance.

## Numerical validity and controls
- Frozen base states: positive normalized Hermitian, density eigenvalue >=-1e-12; trace/Hermiticity errors <=1e-12; regular positive-polar correlations, smallest singular value >=.015.
- Basis Gram error <=1e-12; every per-state retained F_Q/F_E has rank nine at all thresholds; maximum analytic Sylvester residual <=1e-10. Compute actual hidden-output columns independently, with map norms <=1e-12, rather than assuming hidden closure solely by zero padding.
- Choi convention J=sum_ij |i><j| tensor Phi(|i><j|), input subsystem first, unnormalized trace eight. For each Phi and T_.1, Hermiticity error <=1e-12, minimum Choi eigenvalue >=-1e-12, partial trace over output differs from I by norm <=1e-12. Compare engineered Choi to I tensor I/8+kappa A^T tensor Y_ref within norm 1e-12. Compare measure-and-prepare formula to direct Phi on every matrix unit within norm 1e-12. Prepared tau_± must be positive, normalized and Hermitian at those same tolerances. Require Y_ref norm within 1e-12 of sqrt(3/8).
- For each channel, state and hidden probe (972 cases), inspect rho±eta h and their T_.1 images for positivity/normalization/Hermiticity at the tolerances above. Output polar regularity is not required because no finite-output polar observable is used.
- Mixture affinity residual at p=.37 <=1e-12. Recover Lh from [ (T_s(rho+eta h)-T_s(rho-eta h))/(2eta)-h ]/s and compare to Phi(h)-h within absolute norm 1e-9. All maps in this check are physical channels at positive strength.
- Independently compute channel Q/E from direct global Y_h and compare with F times its retained coefficient matrix; max entry discrepancy <=1e-10.
- Depolarizing retained norm <=1e-12, Q/E relative norms <=1e-12 using the corresponding entangling map Frobenius norm as reference. Entangling hidden-probe Q/E ranks must be six at every state, using its own positive largest singular value and the three frozen thresholds. Engineered construction visibility is the secondary scientific gate, not a numerical validity condition.
- Coverage mismatch, nonfinite data or failed validity -> INVALID. Unexpected programming errors fail CI. Tests accept both valid primary and secondary outcomes. Never retune after observing data.

Python 3.11, numpy==2.3.5, OPENBLAS_NUM_THREADS=1. Source labels are ordered updates, not fundamental time. No chosen channel is derived from Genesis Pin or recoverability; no gravity, physical source selection, or changed admissible-world law is claimed. Historical verdicts remain unchanged.
