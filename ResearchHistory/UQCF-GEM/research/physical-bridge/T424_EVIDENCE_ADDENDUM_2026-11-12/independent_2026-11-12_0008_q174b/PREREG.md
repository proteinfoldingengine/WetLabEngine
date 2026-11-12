# Q174b PREREG (2026-11-12 00:08 MST). Written before any q174b code ran. Analytic sketch done first (disclosed below).
Trigger: Engineering point 1 on T-424 (psi = 16r - 7 is negative for r < 7/16). Q: does the Q173/Q175 witness stay inside a positive reference class,
and if not, does a positive member of the P1 + I + relabel flux class (Prop 174.1) separate x+ = (1,1,2,1)/5 from x- = (1,1,1,2)/5?
Premises (all SUPPLIED, none promoted): reference commutes with P (FCV L7), I (FCV L8) and admitted relabelings (v16.22 TYPE_LEDGER L19);
flux form from Prop 174.1; positivity variants below are supplied premises, not inherited (T-422 ERRATUM_Q168: full-cone domain not derived).
Notation: a = Gamma_1(4/5; 1), b = Gamma_2(1/5; 4/5, 1), c = Gamma_2(2/5; 4/5, 1); fixed(x+) <=> 2a = 2b + 3c; fixed(x-) <=> a = 2b + c (Cor 174.2).
Disclosed analytic sketch (pre-code):
 S1. psi witness: f(x+), f(x-) are entrywise positive and Gamma_2 > 0 on (0,1], but closed-cone nonnegativity fails on the pair's own tree
     at x = (1/5, 0, 2/5, 2/5): f_p = a - 2c = -1/125.
 S2. Prop 174b.1: if f_X(x) >= 0 for every x >= 0 on every carrier (supplied closed-cone nonnegativity), then the carriers
     (pair tree, x_p = 0, m_u = m_v = 2/5), (p with children 1/5,1/5,2/5, x_p = 0) and (p with four children 1/5, x_p = 0), each with x_o = 1/5,
     give a >= 2c, a >= 2b + c, a >= 4b. Then fixed(x+) forces a = 2c = 2b + c, and fixed(x-) forces a = 4b = 2c; either gives c = 2b and both fixed.
     So every closed-cone-nonnegative member is blind on the pair.
 S3. c != 2b does not by itself separate: positive member Gamma_1 = m, Gamma_2 = m(1+r)/3 has c != 2b and neither point fixed.
 S4. Open-cone witness (nonnegativity only for x > 0 entrywise, and on I-images of such x): Gamma_1 = m, phi(M) = M,
     Gamma_2(m; m_p, M) = m h(m/m_p) with h(1/4) = 2/5, h(1/2) = 6/5, h = 1/100 otherwise; Gamma_d (d >= 3) = m h(r of the depth-2 ancestor).
     Predicted: x+ fixed, x- not fixed; strictly positive output on strictly positive input; fails closed-cone nonnegativity (two children of mass m_p/2, x_p = 0).
     If Gamma_2(.; 4/5, 1) is continuous at 1/5 and 2/5, open-cone positivity implies the S2 inequalities by limits, so S4 needs a discontinuity.
PASS: S1-S4 numbers reproduce exactly (Fractions); S4 witness and S3 member give 0 P1, 0 I and 0 relabel residuals on seeded carriers up to depth 3;
 S4 gives 0 negative entries on >= 200 seeded strictly positive grades on >= 4 carriers; S2 algebra verified on seeded (a, b, c) satisfying the
 inequalities (no separating triple) and a direct LP-style exact check over a rational grid.
Rejecting controls: the psi witness MUST show a negative entry under closed-cone sampling; the S4 witness MUST show a negative entry at the closed-cone point;
 a sibling-dependent flux MUST give P1 residuals; a name-dependent map MUST give relabel residuals.
FAIL: any mismatch, any negative S4 entry on the open cone, or a separating (a, b, c) that satisfies the three S2 inequalities.
Limits fixed in advance: S2 is a proof for the pair only; checks are finite; nothing physical; NOT_DERIVED; scientific_breakthrough false.
