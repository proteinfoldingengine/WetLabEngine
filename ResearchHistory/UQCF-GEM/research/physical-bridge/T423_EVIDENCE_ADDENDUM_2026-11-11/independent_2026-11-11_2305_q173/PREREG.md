# Q173 PREREG (2026-11-11 23:05 MST; analytic sketch done before code, disclosed)
Q: do nonlinear, positively homogeneous references that commute with P1 (fiber sum into the nearest retained ancestor), with I (zero extension) and with
rooted relabeling exist beyond the mass-modulated linear span, and can one separate the frozen pair x+=(1,1,2,1)/5, x−=(1,1,1,2)/5 on fiber {p,u}?
Analytic sketch: (a) stars: P1+I+relabel naturality forces f_c = γ(x_c, M), f_o = φ(M) − Σγ(x_c, M), with γ(0, M) = 0. (b) Trees: the flux form
f = βM·δ_root + div(e), with e_c = Γ_{d(c)}(m_c; m_{anc_0(c)}, …, m_{anc_{d−1}(c)}) and Γ(0; ·) = 0, is P1-, I- and relabel-natural, because retained subtree and ancestor
masses are P1-invariant and the removed fluxes telescope. Candidate: Γ_1 = m, Γ_2 = m(1 + εψ(m/m_parent)), ψ(r) = 16r − 7 (ψ(1/2) = 1, ψ(1/4) = −3), ε = 1/100.
Predicted: x+ fixed, x− not. The reverse choice (ψ(1/4) = −ψ(1/2)) fixes x− instead.
PASS: exact check of P1-naturality over ALL prefix subtrees of a depth-3 carrier at 5 seeded random rational grades; I-naturality for leaf and chain extensions;
relabeling; positive homogeneity; guard outcome as predicted; reverse ψ reverses it. FAIL: any naturality residual ≠ 0, or the guard outcome differs.
Rejecting control: Γ_2 = m(1 + εψ(m/M_total − x_o)) (depends on a non-ancestor quantity) must FAIL P1-naturality.
