# Q175 RESULT: PASS (not forced). c = 2b enters only through the supplied F-linearity premise (v16.22 A6).
Audit at research 06d0a96f:
- v16.22 TYPE_LEDGER A6: "Candidate family T_X ... F-linear ... New logical classification variable, not a supplied physical source". Linearity is a classification PREMISE.
- v16.22 A1: V_X = F^X is a "Conditional inherited linear diagnostic". This linearizes the SPACE, not maps on it.
- v16.22 A3: "No arbitrary coarse map A is introduced". There is no sibling-merge arrow, so additivity in m_c is not tied by any declared arrow.
- v16.22 RESULTS L32, v16.23 PROOFS L53, v16.31 PROOFS L20: finite additivity of physical grades is explicitly NOT used to infer more.
- v16.23 PROOFS L45 ("ANY v16.22 comparison-compatible linear family"): linearity is assumed there, not derived.
- v16.24–v16.39: no clause forcing linearity or additivity of a reference was found by grep (linear map/family/reference, additiv, sibling, merge, coarse).
  Hits concern attribution and Möbius structure (v16.28 D5, v16.30, v16.31), which is a different type.
Witness, naturality class P1 + I + relabel on the full positive domain (Q173/Q174 verified):
- ψ = 16r − 7 gives b = 97/500 and c = 101/250, so c ≠ 2b.
- The linear member gives b = 1/5 and c = 2/5, so c = 2b.
Both are in the class and contain the pair, so the inherited clauses do not decide c = 2b.
Self-check (Engineering 22:04 rule): this is an ABSENCE, not promoted into a requirement. Statement: "under supplied premise A6 (F-linearity) the guard is blind; without it, the direction is set by unsupplied Γ_2 values".
Limits: the audit is by text search plus reading of the named clauses, not proof-assistant level. A4 type gap noted. Not physical; NOT_DERIVED; scientific_breakthrough false.
