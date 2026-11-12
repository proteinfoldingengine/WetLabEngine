# Q177 PREREG (2026-11-12 01:10 MST; analytic sketch before code, disclosed)
Q: (i) does any inherited clause supply continuity of the reference (e.g. the conditional R extension)? (ii) Under D_dc positivity alone, are BOTH separation directions realizable, so that the direction is free and not merely separable?
(i) Cited audit at 70aa8c08. Search terms: topolog, continu, dense, density, limit, real-scalar, F=R, over R.
(ii) S5 = the Q174b S4 design with h(1/4) = 6/5, h(1/2) = 4/5, h = 1/100 otherwise. Then a = 4/5, b = 6/25, c = 8/25: a = 2b + c (x− fixed), 2a ≠ 2b + 3c (x+ not fixed).
  D_dc positivity sketch: depth-1 f_q = m_q(1 − Σ r_c h(r_c)), with Σ r_c < 1 on D_dc. Worst cases: three children at 1/4 give 9/10, and one at 1/2 plus one at 1/4 gives 7/10, both < 1.
  Depth-2 f_v = h·x_v ≥ 0.
PASS: S5 has 0 P1, I and relabel residuals; 0 negative entries over ≥ 320 seeded D_dc points plus their P1/I images (atom-hitting points included); x− fixed and x+ not.
  The closed-cone control (1/5, 0, 1/5, 3/5)-type interior-zero point is rejected or negative as expected. FAIL otherwise.
