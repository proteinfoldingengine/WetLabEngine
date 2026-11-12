# Q174 RESULT: PASS. The flux form is complete; the frozen-pair guard reduces to three scalars.
Run 2026-11-11 23:35 MST, python3 3.13.5 (Fractions, exact), bytecode off. Script q174.py, output stdout.txt.
Prop 174.1 (proof, all depths, under the supplied P1 + I + relabel naturality): e_c := Σ_{subtree(c)} f_v is invariant under P1 pruning inside subtree(c) and outside the root–c chain.
So e_c = Γ_{d(c)}(m_c; chain ancestor masses). I gives Γ(0; ·) = 0, and total output = φ(M). Hence every such reference has flux form.
Checks: 4 flux maps (the Q173 candidate plus 3 seeded) give 0 P1 residuals and 0 reconstruction mismatches. The sibling-dependent control gives 92 P1 residuals (rejected).
DISCLOSED: the reconstruction check only tests consistency on flux maps; completeness rests on the proof, not the code.
Cor 174.2: on the pair (fiber {p,u}), let a = Γ_1(4/5; 1), b = Γ_2(1/5; 4/5, 1) and c = Γ_2(2/5; 4/5, 1). Then fixed(x+) ⇔ 2a = 2b + 3c, and fixed(x−) ⇔ a = 2b + c.
Both were verified against direct evaluation on 18 seeded triples, with 0 mismatches. The two hyperplanes coincide iff c = 2b.
Therefore the whole natural class is blind on the pair iff Γ_2 is additive at the pair's sibling masses: Γ_2(2/5) = 2Γ_2(1/5) at (m_p, M) = (4/5, 1).
This is a two-point condition, strictly weaker than linearity. It sharpens T-423's "missing input is linearity" to an exact supplied scalar condition.
Limits: positivity is not imposed, and the result is about the formal pair only. Not physical; native bridge NOT_DERIVED; scientific_breakthrough false.
