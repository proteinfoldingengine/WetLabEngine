# Q175 PREREG (2026-11-12 00:05 MST)
Q: does any inherited clause type Γ_2's dependence on m_c, i.e. force or forbid c = 2b (Cor 174.2)?
Method: line-cited audit of v16.22 TYPE_LEDGER/RESULTS/PROOFS, v16.23 PROOFS, and v16.24–v16.39 TYPE_AND_PROOF/PROOFS (research 06d0a96f) for linearity, additivity, sibling or coarse merge maps.
Counterexample strategy: a family natural under the declared source-side arrows (P1, I, admitted bijections) that contains the pair with both c = 2b and c ≠ 2b.
PASS (not forced): every linearity occurrence is a premise or a diagnostic, with no clause forcing additivity of the reference, and the witness exists with b, c computed exactly.
FAIL: a clause that makes reference linearity or sibling additivity inherited.
Naturality class named: P1 + I + relabel. A4 (R, H on W) is not applicable to grade→grade references (type gap, stated).
