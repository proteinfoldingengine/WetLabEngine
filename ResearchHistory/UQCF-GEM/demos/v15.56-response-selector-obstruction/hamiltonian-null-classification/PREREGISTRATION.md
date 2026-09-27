# v15.74 — Fixed Hamiltonian null classification

Parent certified documentation head: 71c4ece38c4d973884f15cebe104f895f0893671.
Branch: research/v15.74-hamiltonian-null-classification.
No v15.74 numerical measurement precedes the missing-implementation RED.

## Question and frozen source space
Can coherent combinations of interacting Hamiltonian terms cancel all hidden-probe retained rotation? v15.73 ranks were computed in the hidden/source product space. Here coefficients of a SINGLE Hamiltonian are shared across every hidden probe and every state. This is a distinct linear inverse problem.

Use all 63 nonidentity raw three-qubit Pauli P in lexicographic order, H_P=P/2, real coefficients. Probe all 27 full-support h=P/sqrt(8), also lexicographic. Use the exact historical 12 states [13,16,22,25,27,29,37,39,46,50,66,77], inherited selector unchanged. No new seeds or ensemble selection. Identity is excluded because it commutes with everything; it can be restored as an additional trivial null coefficient.

For Y_P,h=-i[H_P,h], stack all one-body and raw pair moments into a state-independent retained map B, shape (27*36,63). For each rho compute dC=d<pair>-d<a_i>a_j^T-a_i d<a_j>^T, then Q=O^T dC-dC^T O and PW+WP=Q. Use skew coordinates (q01-q10,q02-q20,q12-q21)/sqrt(2). For each source coefficient column, flatten hidden-major then edge-major then skew coordinate. A_Q and A_E have shape (243,63); stack the 12 states in historical order to give (2916,63). Archive the full maps, spectra and null-projectors. Source weight 1 has nine columns, weight 2 has 27, weight 3 has 27; interacting subspace has 54 columns.

## Rank gates and verdict
Use relative thresholds [1e-9,1e-10,1e-11]. For each map use the largest singular value of its complete 63-column map as reference for every restricted-column map. Use the complete stacked map's scale for stacked subspaces. Null projectors use the middle threshold 1e-10. Record all three ranks; agreement is required by scientific gates rather than silently choosing a favorable cutoff.

Scientific confirmation requires: each state's weight-two Q and E maps have rank 27 at all thresholds; stacked interacting Q and E have rank 54; stacked full Q and E have rank 54; each stacked full null-projector agrees with the coordinate projector onto the nine local columns within Frobenius norm 1e-8. Report per-state full/interacting ranks without requiring any chosen outcome. For any interacting stack kernel at the middle threshold, archive its basis and B/Q/E residual norms; these are diagnostics, not a tuned new gate.

Valid and all scientific conditions true -> HAMILTONIAN_NULL_KERNEL_LOCAL_ONLY_CONFIRMED.
Valid but any scientific condition false -> HAMILTONIAN_INTERACTION_NULL_NOT_EXCLUDED.
Failed numerical validity/controls, nonfinite data, state identity or coverage mismatch -> INVALID.
Tests must accept either valid scientific verdict. Unexpected programming errors fail CI and require an implementation correction, not a scientific interpretation.

## Frozen controls and numerical validity
- All 12 states and both control fixtures below must be positive normalized Hermitian: minimum eigenvalue >=-1e-12; trace and Hermiticity errors <=1e-12; each connected correlation positive-polar and smallest singular value >=.015.
- Independently evaluate B by adjoint trace i Tr(h[H,O]); maximum complex disagreement with direct commutator moments <=1e-12; maximum imaginary retained moment <=1e-12. Y trace and Hermiticity error <=1e-12.
- Exact algebraic positive control: B has full rank 54, weight-two pair map rank 27, weight-three one-body map rank 27. Local B is zero within norm 1e-12. Rank thresholds use the corresponding full B scale.
- Local-column Q/E relative Frobenius norm <=1e-12 in all states and control, referenced to full map norms. Sylvester residual <=1e-10 for every source/probe/edge.
- Source centered derivative for every 63*27 source/probe pair: with U_s=cos(s/2)I-i sin(s/2)P, s=1e-3, derivative equals sinc(s)Y within absolute norm 1e-10; unitary residual <=1e-12.
- Linear assembly control: fixed coefficients c_j=(-1)^j/sqrt(63), j=0..62; recompute with H=sum c_j P_j/2, compare direct Q/E to map multiplication for every state/probe, maximum absolute discrepancy <=1e-10. This checks coherent combinations without fitting.
- Exceptional control rho0=(I+.04 sum_{edges,a} sigma_i^a sigma_j^a)/8. It has zero one-body moments and C_e=.04I. Its weight-three sources must have Q/E zero relative to the full control-map norm <=1e-12, despite the full-rank one-body leakage map. Full control Q/E rank must be 27, and full null-projector must equal local-plus-weight-three coordinate projector within 1e-8. The positive quantum state is a control fixture, not geometry inserted into a source law.

- Connected-subtraction positive control: add .02 X on qubit 1 to the numerator of rho0 (zero-based labels), keeping connected correlations .04 I. With H=XXX/2 and h=YXX/sqrt(8), Y=ZII/sqrt(8); edge (0,1) must have Q Frobenius norm .08 and E norm 1, with other edges zero, absolute tolerance 1e-12. This catches missing or misordered Bloch-subtraction terms.

There is no new finite polar difference gate or source-amplitude sweep. Use analytic Sylvester derivatives to avoid the previously adjudicated cancellation problem. Freeze numpy==2.3.5 and Python 3.11 in the targeted workflow. No thresholds, source coefficients, ensemble, or interpretation changes after seeing results.

## Boundaries
DERIVATION.md proves an open-state statement for fixed state-independent Hermitian generators and all hidden probes. The finite ensemble gate tests whether these particular states already witness that classification. It does not prove a finite-precision universal theorem by itself. This does not classify general CPTP channels, dissipative generators, state-dependent sources, or source changes to admissible worlds. Hamiltonians parameterize ordered source updates, not fundamental time. No geometry-dependent interaction, source-law selection, gravity, new matter primitive or change to Genesis Pin is claimed. Historical verdicts remain unchanged.
