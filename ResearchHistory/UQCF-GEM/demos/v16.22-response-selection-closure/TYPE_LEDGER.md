# v16.22 — Types, premises and provenance

All parent paths below are at `6a9fe4450c4a711a4c0d3b2170e7e31eff550ee6` in `ResearchHistory/UQCF-GEM/`. The complete previous ledger is `foundational-closure-verification/TYPE_LEDGER.md`, L1–L17; arguments are its PROOFS.md P0–P7. The new analysis does not remove or change that diagnostic.

| ID | Actual object / type | Status and provenance |
|---|---|---|
| A0 | (g,X), one fixed Genesis g and a finite rooted prefix tree X; retention Y is an actual root-containing ancestor-closed subset | Inherited L1–L5; full addresses, not hash equality. Source of parent incidence: `demos/v15.56-response-selector-obstruction/retained_incidence.py`. |
| A1 | F=Q; V_X=F^X as formal signed singleton grades; S_X=ker(sum:V_X->F) | Conditional inherited linear diagnostic, not arbitrary physically preparable signed grades. Parent L6/P0 and `lineage_laplacian.py` explicitly `Map(K_R,Q)`. F=R is only a conditional theorem extension. |
| A2 | W_X=F^X/F1_X; q_X:V_X->W_X the quotient by constant potentials | Inherited L13/P4. Not S_X by equal dimensions. Root-zero representatives and nonroot source coordinates are separate explicit coordinate isomorphisms. |
| A3 | P_XY:S_X->S_Y is fiber summation for ancestral r; I_YX:S_Y->S_X is source zero extension | Inherited L7–L8/P1–P2, supplied actual section PI=id. No arbitrary coarse map A is introduced. |
| A4 | R_XY:W_X->W_Y is restriction; H_YX:W_Y->W_X is pullback by r | Inherited L16–L17/P6. Both preserve constant equivalence. RH=id. Do not identify H with source I. |
| A5 | l_X:W_X->S_X induced by already-fixed unweighted L_X; T^G_X=l_X^{-1}=q_XG_X restricted to S_X | Inherited L11/L14/P4. This definition uniquely specifies the reference T^G. It remains intact in both analyses. |
| A6 | Candidate family T_X:S_X->W_X, F-linear, satisfying all A3–A4 diagrams and relabeling covariance | New logical classification variable, not a supplied physical source or an adopted replacement of A5. Premise set C. |
| A7 | C+INV additionally requires l_X T_X=id on S_X | Explicit defining property of A5. Audit distinguishes uniqueness given this property from selection by C alone. |
| D1 | b_X:F^{E_X}->S_X, b_X(e_v)=delta_v-delta_parent(v) | Derived coordinate isomorphism from A0–A1; proof T1. No geometry or new force inserted. |
| D2 | d_X:W_X->F^{E_X}, d_X[phi]_v=phi(v)-phi(parent(v)) | Derived coordinate isomorphism from A0–A2; proof T1. Integrate along the unique ancestral path to invert. |
| D3 | M_X=d_X T_X b_X:F^{E_X}->F^{E_X} | Representation of A6 in D1/D2. The two coordinate spaces have different physical meanings; their bases are related by named constructions, not dimensions. |

Admitted bijections preserve root, ancestry and the common Genesis. Depth is the number of ancestral edges and is preserved by those bijections and by retention of an edge. Re-rooting, identifying different Genesis anchors, suppressing a retained ancestor, or adding a fundamental time coordinate are not admitted arrows. Naturality means commuting with every arrow in the declared class, not just one convenient labeling.

The source/potential arithmetic is rational throughout. No Frobenius norm, new positive form, invertibility assumption on candidates, or fitted weight is used to define C. Depth-indexed coefficients that arise in a classification are degrees of freedom, not physically selected couplings. In C+INV the inherited unweighted law is kept, rather than discarded to produce an artificial no-go.
