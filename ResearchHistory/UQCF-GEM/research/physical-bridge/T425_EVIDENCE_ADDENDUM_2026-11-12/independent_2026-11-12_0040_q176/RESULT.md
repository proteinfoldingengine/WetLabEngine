# Q176 RESULT: PASS. No positivity premise for guard references is inherited; on the minimal map-stable positive domain, positivity does not decide the verdict.
Run 2026-11-12 00:45 MST, python3 3.13.5, Fractions (exact), bytecode off. Script q176.py, output stdout.txt.
A. Audit at research 70aa8c08:
- F^+ = Q_{≥0}^X is inherited as a SOURCE cone ("explicitly analyzed submonoid/cone", v16.23 TYPE_LEDGER C; "conditional formal ... not physical attainability", v16.24 C3). P and I preserve it (v16.23 O5).
- No ledger clause types a REFERENCE's outputs as cone-valued. A grep of FCV TYPE_LEDGER, v16.22–v16.39 TYPE/PROOFS for "continu", "faithful" and "strictly positive" returned no hits.
- The only positivity in the route is Q157's typing of the guard reference as a faithful trace (w > 0 where the guard is read). That is a premise of the SUPPLIED recoverability-guard route.
B. Prop 176.1 (argument plus exact check): D_dc := {x ≥ 0 : zero set descendant-closed} equals the I-closure of strictly positive states.
  Its support is ancestor-closed, so x is the zero extension of a positive state. D_dc is stable under P1 (fiber sums of nonnegatives keep descendant-closed zeros), I and relabeling.
  Checks: 320 seeded D_dc points plus all prefix P1 images and leaf/chain I-extensions gave 0 violations. 50 random P1/I orbits from strictly positive states never left D_dc (0 violations).
  The Q174b closed-cone point (1/5, 0, 2/5, 2/5) is NOT in D_dc. Interior zeros are not produced by inherited maps from positive states.
C. The S4 member (Q174b) is nonnegative on D_dc (0 negative entries over all of the above points and images) and separates: x+ is fixed, f = (1/5, 6/25, 12/25, 2/25); x− is not.
Conclusion (self-check labels): positivity on the inherited-map-stable domain D_dc leaves the direction free. Blindness (Prop 174b.1) needs EITHER
  the supplied closed-cone domain (interior zeros; the same kind of domain promotion withdrawn in ERRATUM_Q168), OR
  supplied continuity of Γ_2 at 1/5 and 2/5 (no ledger clause; A1 fixes F = Q, with R conditional).
  Both are SUPPLIED premises, and neither is derived or rejected here.
Limits: pair only; finite checks plus stated arguments; S4 is discontinuous (a formal witness, not a proposed reference); audit by text search plus reading of named clauses.
Not physical; native bridge NOT_DERIVED; Not claimed; scientific_breakthrough false.
