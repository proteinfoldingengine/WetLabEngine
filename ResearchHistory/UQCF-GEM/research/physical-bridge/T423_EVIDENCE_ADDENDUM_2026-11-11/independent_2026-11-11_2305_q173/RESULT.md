# Q173 RESULT: PASS (the falsifier was found). A nonlinear reference that is P1-, I- and relabel-natural separates x±.
Run 2026-11-11 23:05 MST, python3 3.13.5 / sympy 1.14.0 (system python; the venv has no sympy), bytecode off. Script q173.py, output stdout.txt.
1. Stars (analytic): P1 + I + relabel naturality forces f_c = γ(x_c, M), f_o = φ(M) − Σ_c γ(x_c, M), with γ(0, M) = 0.
   Proof: prune every other leaf into the root, so f_c depends only on (x_c, M); the root follows from the one-vertex case plus P1. Conversely every such map is natural.
   Positive homogeneity gives γ = M ψ(x_c/M) and φ = βM. This is nonlinear in general, so mass-modulated linear references are a strict subclass.
2. Trees: the flux form f = M δ_root + div e, with e_c = Γ_d(m_c; ancestor subtree masses) and Γ(0; ·) = 0, is natural.
   Exact check on the 6-vertex depth-3 carrier, over all prefix subtrees × 5 seeded rational grades, plus leaf and chain I-extensions at every vertex:
   0 P1 residuals and 0 I residuals. Homogeneity residual 0.
   The control, which depends on a non-ancestor quantity, gives 70 P1 residuals (rejected as required).
3. Guard on the frozen pair with Γ_2 = m(1 + ε ψ(m/m_parent)), ε = 1/100:
   - ψ = 16r − 7: x+ gives f = (1/5, 101/500, 101/250, 97/500), FIXED. x− gives f = (1/5, 101/500, 97/500, 101/250), NOT fixed.
   - ψ = 8r − 3 (ψ(1/4) = −ψ(1/2); the in-script label "−4r+1" is a typo): x+ NOT fixed, x− FIXED.
   - Fixed(x+) ⇔ ψ(1/4) = −3ψ(1/2), and fixed(x−) ⇔ ψ(1/4) = −ψ(1/2). The linear case (ψ constant) gives both or neither, matching Prop 172.1.
Consequence: Prop 172.1 and its corollaries (blindness) depend on LINEARITY. Inside I-natural references, the separation direction is again set by an unsupplied function ψ,
so the Q157 obstruction relocates into the ratio dependence. The first supplied link becomes: linearity (or ratio-independence) of the reference, in addition to I-commutation.
Limits: relabel naturality is checked by construction, not numerically. Completeness of the flux form on trees (beyond stars) is not proved.
Not a physical result; native bridge NOT_DERIVED; scientific_breakthrough false.
