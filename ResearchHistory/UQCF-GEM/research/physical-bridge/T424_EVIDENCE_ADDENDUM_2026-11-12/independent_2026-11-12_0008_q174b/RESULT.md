# Q174b RESULT: PASS (all preregistered predictions S1-S4 reproduce; all controls rejected as preregistered). Run 2026-11-12 00:09 MST.
Interpreter: system python3 3.13.5, Fractions only (exact), PYTHONDONTWRITEBYTECODE=1. Script q174b.py, output stdout.txt.
Preserved failed run: q174b_run1_FAILED.py / stdout_run1_FAILED.txt (SyntaxError in an eval string "a-2c" in the S2 block, after S1 had printed;
fix = "a-2*c", "a-2*b-c", "a-4*b" only; the S1 lines are byte-identical between the two runs).
Premises (SUPPLIED, none promoted): the reference commutes with P (FCV TYPE_LEDGER L7), I (FCV L8) and admitted relabelings (v16.22 TYPE_LEDGER
line 19); flux form from Prop 174.1. Every positivity variant below is a SUPPLIED premise; T-422 ERRATUM_Q168 records that the full-cone domain is not derived.

S1 (psi = 16r - 7 witness, Q173/Q175 member). Exact: a = 4/5, b = 97/500, c = 101/250 (c != 2b; Q175 values recomputed).
 f(x+) = (1/5, 101/500, 101/250, 97/500), f(x-) = (1/5, 101/500, 97/500, 101/250): entrywise positive on x+ and x-. x+ fixed, x- not.
 The Gamma_2 factor 1 + psi/100 lies in [93/100, 109/100] on (0,1], so Gamma_2 > 0 although psi < 0 for r < 7/16.
 Closed-cone nonnegativity FAILS on the pair's own tree: x = (1/5, 0, 2/5, 2/5) gives f_p = a - 2c = -1/125; 185 of 300 closed-cone samples
 on the depth-3 carrier have a negative entry. So the witness is positive where the guard reads it (x+, x-) but is NOT a member of a
 full-cone-positive reference class.
S2 (Prop 174b.1, proof for the pair). Under supplied closed-cone nonnegativity (f_X(x) >= 0 for every x >= 0 on every carrier), with Gamma
 shared across carriers by Prop 174.1: carrier (pair tree, x = (1/5, 0, 2/5, 2/5)) gives f_p = a - 2c >= 0; carrier (p with children
 1/5, 1/5, 2/5, x_o = 1/5, x_p = 0) gives a - 2b - c >= 0; carrier (p with four children 1/5, x_o = 1/5, x_p = 0) gives a - 4b >= 0
 (f_p formulas verified, 0 mismatches over 20 seeded triples each). fixed(x+): 2a = 2b + 3c = (2b + c) + 2c <= 2a, so a = 2b + c = 2c, hence
 c = 2b and x- fixed. fixed(x-): a = 2b + c with a >= 4b gives c >= 2b, with a >= 2c gives c <= 2b, so c = 2b, a = 4b and x+ fixed.
 Hence every closed-cone-nonnegative member of the P1 + I + relabel class is blind on the pair (both fixed or neither).
 Exact grid check (25^3 rational triples, 777 satisfying the three inequalities): 0 separating, 0 fixed with c != 2b.
S3. c != 2b alone does not separate: Gamma_1 = m, Gamma_2 = m(1+r)/3 (closed-cone nonnegative since h <= 2/3) gives a = 4/5, b = 1/12,
 c = 1/5 and neither point fixed. Cor 174.2's "blind iff c = 2b" is a statement about the class with a free; positivity constrains a.
S4 (open-cone witness, discontinuous). Gamma_1 = m, phi(M) = M, Gamma_2 = m h(m/m_p) with h(1/4) = 2/5, h(1/2) = 6/5, h = 1/100 otherwise,
 Gamma_d (d >= 3) = m h(ratio of the depth-2 ancestor). a = 4/5, b = 2/25, c = 12/25: x+ fixed, x- not fixed. f(x+) = (1/5, 6/25, 12/25, 2/25).
 Strictly positive output for strictly positive input (proof: f_root = x_o, depth-2 f_v = H x_v, leaves Gamma > 0, depth-1
 f_q = m_q(1 - sum r_c h(r_c)) > 0 because sum r_c < 1 allows at most one child at r = 1/2 and then at most one at 1/4, so sum r_c h(r_c)
 < 3/5 + 1/10 + 1/400 < 1, and without an r = 1/2 child at most three at 1/4, giving < 3/10 + 1/400); 315 open-cone samples, incl. atom-hitting
 near-boundary points, 0 non-positive entries. Nonnegative also on I-images of such points (zero extension commutes, 0 I residuals), so it is
 positive on an I-stable domain containing x+-; T-422's I-stable-positivity statement was scoped to the linear depth <= 2 family and is unaffected.
 Closed-cone control: (1/5, 0, 2/5, 2/5) gives f_p = -4/25 (rejected as preregistered). If Gamma_2(.; 4/5, 1) is continuous at 1/5 and 2/5,
 open-cone positivity gives the S2 inequalities by limits x_p -> 0+, so this separation needs the discontinuity (argument, not computed).
Naturality: psi, S3 and S4 references give 0 P1, 0 I, 0 relabel residuals on two 6-vertex depth-3 carriers (seeded and all-ones grades,
 all prefix subtrees, 20 random relabelings each). Controls: sibling-dependent flux 69 P1 residuals; name-dependent map 150 relabel residuals.
Conclusion (labels as required by the self-check rule): absent supplied full-cone positivity, the P1 + I + relabel class separates x+- exactly
 when c != 2b (Cor 174.2; S1 witness). Under supplied closed-cone nonnegativity, the class is blind on the pair (Prop 174b.1). Under supplied
 open-cone positivity only, a discontinuous member separates (S4); with continuity at 1/5, 2/5 it is blind. Which positivity premise, if any,
 is inherited for guard references is OPEN (Q176); no inherited clause supplying any of them was found (ERRATUM_Q168; Q175 audit).
Limits: pair only; finite checks except the stated proofs; A4 (R, H on W) type gap unchanged (does not apply to grade -> grade references);
 not physical; native bridge NOT_DERIVED; Not claimed; scientific_breakthrough false. No novelty or necessity claim.
