# v16.15F — Graded obstruction descent

**Verdict: OBSTRUCTION_RETAINS_PRIOR_GRADE_HISTORY.**

v16.14F established the exact descent criterion: an obstruction on K_j factors through the new grade K_j/K_{j-1} iff it vanishes on K_{j-1}. v16.15F tests that condition using only the existing four exact prefix-tree fixtures and the intrinsic full-fine obstruction O_j=(QG_f)|K_j.

Each archived fine→coarse fixture was expanded into its lawful leaf-pruning chain using lineage addresses only. Across **12 pruning stages**, exact rational arithmetic gives:

- descending stages: **4** — the first loss stage of each fixture, where K_0=0 and descent is vacuous;
- history-retaining stages: **8** — every subsequent pruning stage.

At every later stage, O_j is nonzero on K_{j-1}. Therefore O_j does not factor through K_j/K_{j-1}. The intrinsic response-information obstruction at a later retained-order depth still acts on distinctions that became unrecoverable earlier.

This means the canonical filtration records *when* information is lost, while the intrinsic full-fine response obstruction records a history-coupled consequence of accumulated loss. The latter cannot be represented as independent per-step graded classes without additional structure. No splitting or transport was inserted to force such a decomposition.

This does not contradict the exact retained-boundary theorem C_c S G_f=G_c P C_f: the present O_j concerns full fine response information erased by pruning, not failure of retained-boundary response naturality.

RED run **36511295453** failed because the implementation was absent. GREEN run **36511346724** passed both tests and the complete exact audit at commit **dde059ab90d7cf2081652dd3c525653c9bf691c3**.

No geometry, quantum primitive, response coarse map A, external time, or fitted quantity was used. Time remains pruning / ordered recoverability update.
