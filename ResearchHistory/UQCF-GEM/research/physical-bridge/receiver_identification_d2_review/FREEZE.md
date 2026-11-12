# receiver_identification draft 2: analytical freeze and prospective preregistration

Author: proteinfolding-grokbot (UQCF Science Agent). Date: 2026-10-18 America/New_York (~04:00 ET loop).
Baseline research head: `05844073b59332776fe522d174908f12e9f9a8fa`.
Frozen argument: `RESULT.md` is the byte-exact copy of `constructions/receiver_identification/CONSTRUCTION.md` at commit `f366da8b` (git blob `ea7b02f828195fde8670fe48b2fc6ba1c04e363e`, 24005 bytes, sha256 `833c011b6c623dfb1d3fdb6e1214015e047e71a5b1a3d1ebc2160eb663b8eb24`). Sections 0 to 8 (with the revision note) are the frozen argument; section 9 discloses exploratory scratch checks; section 10 is a plan and makes no claim.

This file is committed BEFORE any producer, checker, comparator or control code for this freeze exists in the repository and before any of it is executed in Actions. The scratch checks `/tmp/rid/chk1.py`, `chk2.py`, `chk3.py` (RESULT.md section 9) were exploratory, ran before this freeze, and are NOT relabelled as preregistered. The expected values in section 2 were computed by hand and confirmed with a short throwaway script (`/tmp/rid2/exp.py`, not committed) before this commit; that is disclosed here and is not part of the campaign.

Why a new freeze: the draft 1 campaign (`receiver_identification_review/`, run 39106192684) passed and was ACCEPTED, but proteinfolding-gpt's `GPT_DRAFT1_FOLLOWUP.md` (`2d3ec376`) found that draft 1's Proposition 4(b) was wrong when other removed atoms share the owner's fiber. That draft 1 grid had no second fiber member, so it could not detect the error. This preregistration therefore puts **multi-member fibers inside the exhaustive universe** (section 3, P4F) and requires the universe to contain cases where the draft 1 formula is false (non-vacuity).

Disclosure on the review prompt: RESULT.md line 4 states that draft 1 was Gemini ACCEPTED. That sentence is part of the frozen bytes and cannot be removed; the reviewer is told that such statements are not evidence, and that the same sentence records that the earlier acceptance missed an error.

## 1. What is frozen and what is reviewed

- **General proofs (analytic, for Gemini review):** Proposition 1(a)-(c); Theorem 2(a)-(d); Theorem 3 with its multiple-difference remark; Proposition 4(a)-(c) as corrected (owner law nu_a * p_u); Corollary 4.1 (injectivity on Z_{>=0}, no uniform lower bound); Proposition 4.2 (max nu_a <= TV <= 1 for a definite source pair, sharp); Proposition 5(a)-(c); the revision note's receiver-scope correction (unique minimal holder); the section 7 status table and the I*-b paragraph (reviewed for whether anything is presented as derived that is supplied).
- **Exact finite instances (producer and checker):** section 2.
- **Exhaustive declared universes (producer and checker, independently implemented, with exact identity digests):** section 3.
- **Bounded evidence (randomized, checker only, NOT universal):** section 4.
- **Not reviewed:** literature priority statements beyond checking them for overstatement.

Declared inputs, unchanged and NOT claimed derived: occurrence of each contraction (Aaron's empirical-input rule); which retained set is kept; the preparation pair and premise G; the identification I*-b, stated in RESULT.md as an operational definition. No native access closure, agent or consumer, collapse cause, clock, geometry, dark-matter primitive or fitted parameter is claimed. No CLOSED/CERTIFIED status; no main merge.

Conventions for code: a rooted tree on n nodes is a parent array with parent[0] = none and parent[i] < i. A retained set is ancestor-closed and contains node 0. r(z) is the nearest retained ancestor of z (r(t) = t on retained t). Retained coordinates are listed in increasing node order. D6 is the ordered list of the six distributions on {0,1,2} with probabilities in {0, 1/2, 1}: index 0 = (1,0,0), 1 = (0,1,0), 2 = (0,0,1), 3 = (1/2,1/2,0), 4 = (1/2,0,1/2), 5 = (0,1/2,1/2). Fractions are written in lowest terms as "a/b", integers as "a".

## 2. Preregistered exact instances (PASS requires producer = expected exactly and checker = expected exactly, identical key sets)

Unchanged from the draft 1 preregistration (the statements they test are unchanged in draft 2):

| Key | Object | Expected |
| --- | --- | --- |
| E1.mu_x, E1.mu_xp, E1.owner | Thm 2(c): path 0-1-2, retain {0,1}, x = (1,0,1), x' = (1,0,0) | (1,1), (1,0), [1] |
| E2.owner, E2.equal | Thm 2(d): star 0 with children 1,2, retain {0}, x = (0,1,0), x' = (0,0,1) | [], true |
| E3.holders, E3.diffs | Thm 3: path 0-1-2-3, retain {0,1,2} then {0,1} then {0}; single difference x_3 - x'_3 = 1 | [2,1,0], [1,1,1] |
| E3.merge_step | Thm 3 remark: star 0 with children 1,2; differences +1 at 1 and -1 at 2; retain {0,1} then {0} | 2 |
| E4a.tv_src, E4a.tv_owner, E4a.tv_point | Prop 4 with the owner prior as the only nuisance (nu_a = p_a): p_u = delta_0, q_u = delta_1; nu_a = (1/2,1/2); point-mass nu_a | 1, 1/2, 1 |
| E4b.tv_src, E4b.tv_owner | p_u = (1/2,1/2), q_u = (1/4,3/4), nu_a = (1/2,1/2) | 1/4, 1/8 |
| E4c.tv_src_marg, E4c.tv_owner, E4c.tv_joint_before | correlated boundary (outside Prop 4's hypothesis): x_a uniform on {0,1}, under p x_u = x_a, under q x_u = 1 - x_a | 0, 1, 1 |
| E5.cnot, E5.owner_reduced | Prop 5(c): controlled-add mod 2 equals CNOT; owner reduced state for control \|+> and blank owner | true, [[1/2,0],[0,1/2]] |
| P1.factor | Prop 1(a),(b) for Omega = {0,1} x {0,1,2} | true |

New for draft 2:

| Key | Object | Expected |
| --- | --- | --- |
| E6.tv_src, E6.tv_owner, E6.tv_draft1_formula | GPT counterexample, computed by the full pushforward of the joint: root 0 retained alone, removed children u = 1, v = 2; x_0 = 0; p_u = delta_0, q_u = delta_1; v uniform on {0,1} under both. tv_draft1_formula = TV(p_a * p_u, p_a * q_u) with p_a = delta_0 | 1, 1/2, 1 |
| E7.tv | Cor 4.1 no uniform bound: delta_0 vs delta_1, nu_a uniform on {0..5} | 1/6 |
| E8.tv, E8.max_nu | Prop 4.2 with k = 2: nu_a = (1/4,1/2,1/4), delta_0 vs delta_2 | 3/4, 1/2 |
| E9.tv | Cor 4.1 with non-point sources: nu_a = (1/2,1/2), p_u = (1/2,0,1/2), q_u = delta_1 | 1/2 |

## 3. Preregistered exhaustive universes (producer AND checker; counts and identity digests must agree exactly; violations must be 0)

- **T2, T3:** exactly the draft 1 universes (all 34 rooted trees with n <= 5, all ancestor-closed retained sets, grades in {0,1,2}; T2 every uninformed pair and every subset W; T3 every strictly decreasing chain of 1 to 3 retained sets below the full tree, every eventually removed u, every base grade and second value), with the same claims as draft 1 FREEZE section 3.
- **P4F (multi-member fibers, new):** all 10 rooted trees with n <= 4, every ancestor-closed retained set, every removed atom u; every assignment of a D6 distribution to each node z != u (the same under p and q; all nodes are independent); every ordered pair (p_u, q_u) in D6 x D6. For each case, with a = r(u) and nu_a = the convolution of the laws of all z != u with r(z) = a (the owner's own prior included), the claims are: (i) the owner's law, computed from the full product joint by the pushforward, equals nu_a * p_u (and likewise for q); (ii) every non-owner retained marginal has the same law under p and q, and the TV of the full retained joint equals the owner's TV; (iii) owner TV <= TV(p_u, q_u); (iv) equality when nu_a is a point mass; (v) owner TV > 0 whenever p_u != q_u (Cor 4.1); (vi) owner TV >= max nu_a whenever p_u, q_u are distinct point masses (Prop 4.2). Non-vacuity (required): the number of cases whose owner fiber has at least two nuisance members must be > 0, and the number of cases where the draft 1 formula TV(p_a * p_u, p_a * q_u) (p_a = the owner's own prior alone) differs from the true owner TV must be > 0. Identity digest: sha256 of the sorted lines "parent|retained|u|assignment|pu|qu|ownerTV" (parent with "-" for none, lists comma-separated, assignment = D6 indices of nodes z != u in node order).
- **P42 (new):** every law nu on {0,...,5} with probabilities in multiples of 1/6 (462 laws) and every shift k = 1,...,6 (2772 cases): max nu <= TV(nu * delta_0, nu * delta_k) <= 1. The number of cases attaining the lower bound must be > 0 and must include nu uniform with k = 1. Identity digest: sha256 of the sorted lines "c_0,...,c_5|k|TV" with c_j = 6 nu(j).

## 4. Preregistered bounded evidence (checker only, numpy pinned, seed 20261018)

B2, B3, B5a, B5b exactly as in the draft 1 preregistration. B4 replaced by **B4F**: 2000 random cases, each with 1 to 4 nuisance members with random exact-rational laws on {0..3} and random exact-rational p_u, q_u on {0..3}: Prop 4(b) bound, data processing on the joint, Cor 4.1 positivity when p_u != q_u. **B6**: 2000 random exact-rational nuisance laws on {0..7} and random shifts k in {1..8}: Prop 4.2.

## 5. Preregistered rejecting controls (each must be REJECTED; any acceptance is RED)

R1 to R7 exactly as in the draft 1 preregistration (with the R3 interpretation disclosed in that campaign's STATUS.md). New:
R8 the draft 1 owner law p_a * p_u claimed equal to the true owner law on E6. R9 the draft 1 equality clause (point-mass owner prior implies equal TV) claimed on E6. R10 a uniform lower bound TV >= 1/2 for distinct point-mass sources claimed for every nuisance law (refuted by E7). R11 injectivity claimed for wrapping addition: nu uniform on Z_3, delta_0 vs delta_1 with addition mod 3, claimed TV > 0. R12 Prop 4.2 strengthened to TV >= 2 max nu (refuted by nu uniform on {0..5}, k = 1). Certificate tampering: missing key, duplicated key, substituted value, wrong value, universe-count mismatch, digest mismatch and false provenance (wrong RESULT.md hash) must each make the comparator fail.

## 6. Resource and stopping rules

One Actions run per pushed head, ubuntu-24.04, Python 3.12, pinned `sympy==1.14.0`, `numpy==2.3.5`, `mpmath==1.3.0`. Job order: verify (producer, checker, comparator, controls) then Gemini argument review (`gemini-3.1-pro-preview`, temperature 0, no fallback model) then publication readback (immutable GitHub readback of the frozen bytes at the run's SHA). A RED verify result stops the run before review and is preserved. A REVISE or FAIL verdict is preserved and answered by a new freeze, never by editing this one. Raw reviewer output stays in Actions artifacts; only a summarized receipt is committed.
