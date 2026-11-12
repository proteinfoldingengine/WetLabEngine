# Q166 PREREG (2026-11-11 20:01 MST)
Claim: natural (pruning P + child relabeling) linear families are exactly span{T_0} ⊕ span{ E_{d,j} : 1≤d≤D, 0≤j≤d },
E_{d,j}(x) = Σ_{edges (q,c), |c|=d} m_{anc_j(c)}(x) (δ_c − δ_q), m_a = subtree mass. (E_{d,d} sums give T_d − T_{d−1}; E_{d,0} = D_d.)
Predicted dims: D=1:3, D=2:6, D=3:10. PASS: all candidates natural (exact integer residual 0), candidate rank = nullity, at D=2 (binary, full)
and D=1 (arity 3); D=3 binary checked by float nullity on a size-bounded universe (weaker; boundary artifacts possible).
FAIL otherwise. Consequence to test: global positivity (unbounded arity) kills all E_{d,j}, j<d ⇒ positive natural refs ⊂ span{T_k}, guard blind.
