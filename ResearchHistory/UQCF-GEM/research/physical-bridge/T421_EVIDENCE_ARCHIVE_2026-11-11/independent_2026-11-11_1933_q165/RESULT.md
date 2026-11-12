# Q165 RESULT (2026-11-11 19:38 MST) — prereg FAILED; natural linear families classified (partially); guard consequence
Prereg PASS criterion was "natural linear families = span{id, δ_root⊗sum}" (dim 2). **FAILED.**
Exact sympy nullspaces (stdout.txt, stdout_c.txt, stdout_d.txt; float rank stdout_b.txt):
- depth≤1, arity 2/3/4/5: dim 3 = span{id, T0, D1}.
- depth≤2, arity 2 (all 25 carriers): dim 6; span{id, T0, T1, D1, D2} has rank 5 and lies in it. ONE family unexplained.
- depth≤2, arity 3, carriers ≤6 vertices (float): nullity 6 (bounded-size universe; may contain boundary artifacts).
Families (verified natural under prunings P and child relabelings):
- T_k(x) = I∘P onto depth≤k truncation (mass of each depth-k subtree collected at its top). T0 = δ_root⊗sum.
- D_g(x) = M(x)·ν_g, ν_g(v) = g(|v|) − k_v·g(|v|+1) = g(0)δ_root + Σ_edges g(depth child)(δ_child − δ_parent).
  Proof of naturality: P kills the dipole of a removed leaf edge; other edges unchanged; prunings compose from leaf removals.
Lemma 165.1 (positivity): with unbounded arity (Genesis tokens are arbitrary nonneg ints), ν_g ≥ 0 on all carriers forces
g(d)=0 for d≥1 (leaves need g(d)≥0; a vertex with k children needs g(d)−k g(d+1)≥0 ∀k). Evaluating any family in
span{id,T_k,D_g} at x=δ_root shows the D_g part must itself be ≥0, so globally positive members have no dipole part.
Guard consequence (q165_guard.py, exact Fractions, balanced pair x±, fiber {p,u}):
- references A·x + B·T1(x) (globally positive): x± fixed together iff B=0 → BLIND (4/4 cases).
- references with dipole profile g (only locally positive on the fiber): w_p/w_u = (g(1)−2g(2))/g(2) at A=B=0;
  g(1)=3g(2) reproduces the counting ratio 1 and SEPARATES (fixes x−, not x+). The ratio is a free profile parameter.
Reading: naturality relocates, not removes, the Q157 obstruction: the unearned ratio w_p/w_u becomes the unearned depth
profile g, and a globally positive natural reference has g=0 and is blind. No guard is derived.
Scope/limits: linear families only; finite depth/arity universes; one depth-2 family unexplained (could be a binary or
boundary artifact or a genuine family) — the blindness statement is conditional on it. Native bridge NOT_DERIVED; Not claimed.
Adversarial self-check: (i) bounded-universe artifacts are real (depth-1 D1 looked like a carrier-size-dependent map before
its edge-dipole form was found); (ii) local positivity may be all a Petz guard needs — then the result is "free parameter",
not "blind"; stated both ways above. Below the posting bar alone; batch with Q166.
