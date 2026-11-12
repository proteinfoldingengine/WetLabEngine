# Q166 RESULT (2026-11-11 20:02 MST) — PREREG PASS: natural linear families classified (depth ≤3); positivity lemma
Q165's unexplained 6th family is E_{2,1}(x) = Σ_{|c|=2} m_{parent(c)}(x)(δ_c − δ_parent) (dipole weighted by the parent's subtree mass).
Classification found (stdout.txt): natural (pruning + child relabeling) linear families = span{T_0} ⊕ span{E_{d,j}: 1≤d≤D, 0≤j≤d},
E_{d,j}(x) = Σ_{edges (q,c),|c|=d} m_{anc_j(c)}(x)(δ_c − δ_q). Integer residual 0 for every candidate, candidate rank = nullity:
depth1/arity3 3=3; depth2/binary full 6=6; depth2/arity3 (≤6 vertices) 6=6; depth3/binary (≤7 vertices) 10=10.
Naturality proof (all depths): a pruning removes leaf edges, whose dipoles P maps to 0; subtree masses of ancestors of surviving
vertices are unchanged by P; relabelings preserve depth/ancestry. Completeness for D>3 is NOT proved (computational, D≤3 only).
Contains Q165's families: E_{d,0}=D_d (M-weighted), Σ_{j=d}: E_{d,d}=T_d−T_{d−1}.
Lemma 166.1 (positivity ⇒ truncations only). If f=βT_0+Σα(d,j)E_{d,j} has f(x)≥0 for all states on all carriers with unbounded
arity, then α(d,j)=0 for j<d. Proof: put x=δ_a, |a|=j; with S(d,j)=Σ_{i≤j}α(d,i): a leaf c below a at depth d gives S(d,j)≥0;
the same c with k children gives S(d,j)−kS(d+1,j)≥0 ∀k ⇒ S(d+1,j)≤0; hence S(d,j)=0 for d≥j+2; at a itself S(j,j)−kS(j+1,j)≥0 ∀k
with S(j+1,j)≥0 ⇒ S(j+1,j)=0. So S(d,j)=0 ∀ d>j, i.e. α(d,i)=0 for i<d. ∎ Positive natural refs = positive cone in span{T_k}.
Consequence (with Q165 q165_guard.py): on the balanced pair, fiber {p,u}, every globally positive natural linear reference is
A·x+B·T_1 on the fiber ⇒ guard BLIND. Separation requires an ancestor-mass-weighted dipole (j<d), which is only fiber-positive and
carries free coefficients α(d,j) — the Q157 free ratio relocated, now fully parametrized.
Scope: linear; classification complete only to depth 3; "global positivity" is the reading of a reference measure, and whether the
Petz guard needs only fiber-local faithfulness is open (Q167). Native bridge NOT_DERIVED; Not claimed.
Adversarial check: Q165 claimed blindness conditional on the 6th family; that family (E_{2,1}) is killed by Lemma 166.1, so the
condition is discharged at depth ≤2 (and ≤3). A nonlinear natural reference is outside this result.
Posting: clean single-route obstruction; batch with Q165 for the next combined reply.
