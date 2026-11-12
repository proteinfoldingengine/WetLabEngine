# Q173 RESULT_RELABEL addendum (2026-11-11 23:03 MST): relabeling naturality checked numerically, 0 residuals
Closes the Q173 RESULT limit "relabel naturality is checked by construction, not numerically". PREREG.md, q173.py, stdout.txt and RESULT.md are unchanged.
Script q173_relabel.py (sha256 5ecf632a46ee260584061b6e44ecc3acac02ddea4c8929fb15326839b19234b1), output stdout_relabel.txt (sha256 3d3b865588084e4494fbf70136b7f6e6bf18e4620d1a371adb93bc1b9dbd266c).
Run with system python3 3.13.5 / sympy 1.14.0, bytecode off (same deviation as Q173: the scratch venv has no sympy). Exact sympy Rationals throughout.
Check: f(pi T, pi x)[pi v] = f(T, x)[v] for every vertex v, with dict insertion order shuffled. f is q173.py's own make() (defs reused unchanged).
 - Tree flux form, psi = 16r-7 and psi = 8r-3: every prefix subtree of the 6-vertex depth-3 carrier x 5 seeded rational grades x (all sibling
   permutations + all non-root renamings): 1255 relabelings per witness, residual count 0 for both.
 - Frozen carrier (o,p,u,v), x+ and x-, both witnesses: 16 relabelings each, residual 0; the u<->v swap maps f(x+) to f(x-) exactly (residual 0).
 - Star form f_c = x_c(1 + eps psi(x_c/M)), f_root = M - sum_c f_c, 4-leaf star, all 24 leaf permutations x 5 grades (zeros included): 120 per witness, residual 0.
 - Rejecting control (map depending on a vertex NAME): 8 nonzero residuals, rejected as required.
Verdict: ALL_RELABEL_RESIDUALS_ZERO. Limits: finite checks on the stated carriers; not a proof for all carriers. Flux-form completeness beyond stars stays unproved.
Native bridge NOT_DERIVED; physical result Not claimed; scientific_breakthrough false.
