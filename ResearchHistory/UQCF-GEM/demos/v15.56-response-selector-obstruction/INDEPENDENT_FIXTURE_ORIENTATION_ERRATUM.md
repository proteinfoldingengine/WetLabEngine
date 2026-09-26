# Stage-A orientation correction

Run 98 exposed that the initial pair extractor sorted the wrap edge (2,0), so its diagnostic compared opposite orientations and the selector failed to enforce the preregistered cyclic-identical oriented-pair condition. No hidden response had been evaluated. This correction preserves oriented edge order explicitly and adds cyclic_pair_difference <= 1e-12 as a hard admissibility gate. No response threshold, response code, or target value is introduced.
