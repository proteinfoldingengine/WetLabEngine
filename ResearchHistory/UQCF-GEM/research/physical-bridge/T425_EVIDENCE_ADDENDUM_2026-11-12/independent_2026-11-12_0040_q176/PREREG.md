# Q176 PREREG (2026-11-12 00:45 MST; analytic sketch before code, disclosed)
Q: is any positivity premise (closed-cone nonnegativity, open-cone positivity, or continuity that converts the second into the first) inherited for guard references?
Method A, cited audit at research 70aa8c08: FCV TYPE_LEDGER L6–L8; v16.22 A1/A3/A6; v16.23 C, O5; v16.24 C3; v16.25–v16.39 TYPE/PROOFS. Search terms: nonnegativ, cone, positive, continu, faithful, strictly.
Method B, domain: D_dc := {x ≥ 0 : zero set is descendant-closed}. Sketch: D_dc is the closure of the open cone under I (zero extension of strictly positive states),
it is stable under P1, I and relabeling, it contains x±, and it excludes the Q174b closed-cone point (1/5, 0, 2/5, 2/5).
Prediction: the S4 (Q174b) discontinuous member is nonnegative on D_dc and separates x±. So positivity on the minimal inherited map-stable domain does not, by itself, decide the verdict.
Prop 174b.1's blindness then needs EITHER the supplied closed cone (interior zeros, which no inherited map produces from positive states) OR supplied continuity of Γ_2 (over F = Q, A1).
PASS: (i) exact D_dc stability over all prefix-subtree P1 images and leaf/chain I-extensions on seeded D_dc points; (ii) a seeded P1/I-orbit from strictly positive points never leaves D_dc;
(iii) S4 output ≥ 0 on ≥ 300 seeded D_dc points, including zero subtrees and atom-hitting ratios; (iv) x+ fixed and x− not.
Control: (1/5, 0, 2/5, 2/5) ∉ D_dc, and S4 is negative there. FAIL: any D_dc violation or negative S4 output on D_dc.
Self-check: positivity "where read" (Q157 faithful-trace typing) is a premise of the SUPPLIED guard route, not a ledger clause. State absences as absences.
