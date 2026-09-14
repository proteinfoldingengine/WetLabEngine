# v15.20 — Physical channel representation and readout cost

Continue the existing finite simulator. Preserve the v15.19 source and all nested dependencies byte-for-byte.

Question: can the 255-direction predictor Gamma-perp be represented by a CPTP map, and what changes in readout?

1. Test exact-direct-observable preservation versus CPTP recovery using the multiplicative domain. It is NOT enough to repeat that one orthogonal projection is nonpositive.
2. Derive a two-parameter Pauli-diagonal comparison family with visible multiplier lambda and parity multiplier t. Derive its Choi eigenvalues and Kraus weights before any grid search.
3. Test the candidate t=0, lambda=1/2: erases unused parity, remains CPTP, preserves predictions under an explicit gain-two ensemble readout. No smaller Hilbert-space carrier is claimed.
4. Prove the minimax direct Pauli-readout cost using Pauli twirling and a finite character sum, and test non-Pauli/nonunital comparison channels too. This is a theorem about a declared channel class/objective, not a physical collapse law.
5. Check commutation with the original finite motions and decoded original-target predictions, including mixtures of the two parity states. No physical time or entropy objective is introduced.
6. Produce a computed offline inspector, MP4, report, proof, and honest verification evidence. New maps are diagnostic comparison channels; no actual outcome, source, retention law, or replacement dynamics is adopted.

All float identity tests use 1e-10 unless the inherited v15.19 checks specify their existing 1e-9 limit. Do not tune to measured outcomes. Keep publication separate: earlier GitHub uploads were blocked; no alternate path is authorized to bypass them.
