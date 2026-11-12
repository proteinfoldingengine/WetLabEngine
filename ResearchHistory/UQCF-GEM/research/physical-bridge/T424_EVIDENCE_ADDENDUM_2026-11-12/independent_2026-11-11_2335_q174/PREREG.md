# Q174 PREREG (2026-11-11 23:35 MST; analytic sketch done before code, disclosed)
Q: is the flux form (f = φ(M)δ_root + div e, e_c = Γ_{d(c)}(m_c; ancestor subtree masses), Γ(0; ·) = 0) COMPLETE for references commuting with P1, I and relabeling?
Sketch: define e_c(x) := Σ_{v ∈ subtree(c)} f(x)_v. P1 pruning inside subtree(c) preserves that sum, and pruning outside the root–c chain leaves it unchanged.
So e_c equals its value on the chain carrier, whose grades are differences of the chain subtree masses. I-extension forces e(0; ·) = 0, and total output = φ(M).
Then reduce the frozen-pair guard to a = Γ_1(4/5; 1), b = Γ_2(1/5; 4/5, 1), c = Γ_2(2/5; 4/5, 1). Predicted: fixed(x+) ⇔ 2a = 2b + 3c, and fixed(x−) ⇔ a = 2b + c.
The verdicts coincide for every a iff c = 2b.
PASS: (i) exact flux reconstruction of the Q173 candidate and of 3 more seeded natural maps (all residuals 0);
(ii) rejecting control: a map whose flux depends on sibling mass gives P1 residuals ≠ 0; (iii) the a, b, c guard criteria match direct evaluation on 6 seeded (a, b, c).
FAIL: any mismatch.
