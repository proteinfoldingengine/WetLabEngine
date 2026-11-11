# Q154 PREREG (2026-11-11T15:37:52-07:00) — Science, local, supporting math. NOT_DERIVED; Not claimed; scientific_breakthrough false.
Preflight: no lock; research 8c4f6594 (unchanged); thread 60c7e306 (T-417 posted 15:12 by parent under Engineering answer A — recorded here, was missing from ACTIVE); PR111 no comments after 6808310595.
Gate on original Q154 (are pinching-side receivers chain-intrinsic / does b_r play the (E1) role?): DROPPED as implied. The pinching chain has no removal/survivor choice, and Z(A_S) is characteristic (preserved by every automorphism of A_S); ledger §13 l.435 already says closure acts on the tree factor only.
Replacement Q154': label-free core of the PRODUCT frame (premise J, ledger §13, A_j = B_j ⊗ A_{S_j} on C^{X_0} ⊗ C^d).
Definitions: G_J = unitaries preserving every A_j (set-wise); survivor closure 𝒮_j ⊗ A_{S_j} (Thm 13.3 per l.435); Core^J_j = ∩_{g∈G_J} g(𝒮_j ⊗ A_{S_j}).
Claim P (to prove): every g ∈ G_J has form (π ⊗ I)·⊕_x U_x with π ∈ G (tree chain automorphisms), U_x normalizing each A_{S_j}, U_x^* U_{x'} ∈ A_{S_j}' for x ~_j x'; hence Core^J_j = Core_j ⊗ A_{S_j} (Core_j from Thm 152.1). Corollary: the pinching side adds no (E1)-type label dependence; witness l.445 (R_min suffices) is chain-intrinsic.
Premises/provenance: ledger §12–13 @8c4f6594 (v15.16 pinching, J, Thm 13.3); Thm 152.1 (local, independent_2026-11-11_1431); B_0 = full diagonal on X_0 (P1).
Novelty: not in ledger or Q144–Q153 (grep of RESULT headers: no product-frame core). Elementary.
Check (support only, not proof): n=4 witness parents (·,0,0,1), prune {2,3} then {1}; pinching on 2 qubits S_1={b1}, S_2={b1,b2}. PASS iff all sampled g verified in G_J and dim Core^J_2 = dim Core_2 · dim A_{S_2} = 2·4 = 8 and dim Core^J_1 = 4·8 = 32. FAIL otherwise.
Counterexample strategy: sample g with nontrivial per-atom phases U_x (the only possible non-product mixing) and bit-flip normalizers; seed 154.
