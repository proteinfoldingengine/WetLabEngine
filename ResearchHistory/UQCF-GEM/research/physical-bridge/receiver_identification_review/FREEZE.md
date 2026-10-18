# receiver_identification draft 1: analytical freeze and prospective preregistration

Author: proteinfolding-grokbot (UQCF Science Agent). Date: 2026-10-18 America/New_York (~03:00 ET loop).
Baseline research head: `66ccfede9c984ac9322b2df5e338022c7c7a5bf8`.
Frozen argument: `RESULT.md` is the byte-exact copy of `constructions/receiver_identification/CONSTRUCTION.md` at commit `512a863d2514df2c3af6d8b30417d33d4743482a` (git blob `85a13e9bf2cc4e2807798c30c77ee56f853f7e5a`, 18037 bytes, sha256 `0d4d68e72ec95ce06a9ddb4698bd444bd733fe114db042a9e9d9911f80bf58a0`). Sections 0 to 8 are the frozen argument; section 9 discloses exploratory scratch checks; section 10 is a plan and makes no claim.

This file is committed BEFORE any producer, checker, comparator or control code for this freeze exists in the repository and before any of it is executed in Actions. The scratch checks `/tmp/rid/chk1.py` (RESULT.md section 9) were exploratory, ran before this freeze, and are NOT relabelled as preregistered. The campaign below is executed by new code written after this commit.

## 1. What is frozen and what is reviewed

- **General proofs (analytic, for Gemini review):** Proposition 1(a)-(c); Theorem 2(a)-(d); Theorem 3 with its multiple-difference remark; Proposition 4(a)-(c); Proposition 5(a)-(c); the section 7 status table and the I*-b operational-definition paragraph (reviewed for whether anything is presented as derived that is supplied).
- **Exact finite instances (producer and checker):** section 2.
- **Exhaustive declared universe (producer and checker, independently implemented):** section 3.
- **Bounded evidence (randomized, checker only, NOT universal):** section 4.
- **Not reviewed:** literature priority statements beyond checking them for overstatement.

Declared inputs, unchanged and NOT claimed derived: occurrence of each contraction (Aaron's empirical-input rule); which retained set is kept; the preparation pair and premise G; the identification I*-b, which RESULT.md states as an operational definition. No native access closure, agent or consumer, collapse cause, clock, geometry, dark-matter primitive or fitted parameter is claimed. No CLOSED/CERTIFIED status; no main merge. Mentions in RESULT.md that other documents were accepted are context only; the reviewer is told to verify every cited ingredient a frozen claim relies on.

Conventions for code: a rooted tree on n nodes is a parent array with parent[0] = none and parent[i] < i (all 1 + 1 + 2 + 6 + 24 = 34 such labelled trees for n = 1..5). A retained set is ancestor-closed and contains node 0. r(z) is the nearest retained ancestor of z (r(t) = t on retained t). Retained coordinates are listed in increasing node order.

## 2. Preregistered exact instances (PASS requires producer = expected exactly and checker = expected exactly, identical key sets)

| Key | Object | Expected |
| --- | --- | --- |
| E1.mu_x, E1.mu_xp, E1.owner | Thm 2(c): path 0-1-2, retain {0,1}, x = (1,0,1), x' = (1,0,0) | (1,1), (1,0), [1] |
| E2.owner, E2.equal | Thm 2(d): star 0 with children 1,2, retain {0}, x = (0,1,0), x' = (0,0,1) | [], true |
| E3.holders, E3.diffs | Thm 3: path 0-1-2-3, retain {0,1,2} then {0,1} then {0}; single difference x_3 - x'_3 = 1 | [2,1,0], [1,1,1] |
| E3.merge_step | Thm 3 remark: star 0 with children 1,2; differences +1 at 1 and -1 at 2; retain {0,1} then {0}: first step at which no address holds a difference | 2 |
| E4a.tv_src, E4a.tv_owner, E4a.tv_point | Prop 4: p_u = (1,0), q_u = (0,1) on {0,1}; p_a = (1/2,1/2); point-mass prior | 1, 1/2, 1 |
| E4b.tv_src, E4b.tv_owner | Prop 4: p_u = (1/2,1/2), q_u = (1/4,3/4), p_a = (1/2,1/2) | 1/4, 1/8 |
| E4c.tv_src_marg, E4c.tv_owner, E4c.tv_joint_before | boundary: x_a uniform on {0,1}, under p x_u = x_a, under q x_u = 1 - x_a (owner prior NOT independent of x_u, outside Prop 4's hypothesis) | 0, 1, 1 |
| E5.cnot, E5.owner_reduced | Prop 5(c): controlled-add on 0/1 registers (mod 2) equals CNOT; owner reduced state for control \|+> and blank owner | true, [[1/2,0],[0,1/2]] |
| P1.factor | Prop 1(a),(b) for Omega = {0,1} x {0,1,2}: the 6 point indicators equal the 6 products of one-address indicators, and the basis map is a bijection | true |

## 3. Preregistered exhaustive universe (producer AND checker; universe counts must agree exactly; violations must be 0)

All 34 rooted trees with n <= 5, all ancestor-closed retained sets, grades in {0,1,2}.
- T2: every x and every x' agreeing with x on the retained set: (a) differing retained coordinates = O; (b) for every subset W of retained addresses, W-coordinates differ iff W meets O; (c) whenever x, x' differ at exactly one removed atom u, O = {r(u)}. Also counted: cancelling pairs (O empty with x != x'), which must be > 0.
- T3: every strictly decreasing chain of 1 to 3 ancestor-closed retained sets starting below the full tree, every u that is removed at some step, every base x in {0,1,2}^n and every second value x'_u != x_u: at every step exactly one retained address differs, it is L_k(u) (if u is still retained, L_k(u) = u), and the difference is x_u - x'_u.
- P4: every triple (p_u, q_u, p_a) of distributions on {0,1,2} with all probabilities in {0, 1/3, 2/3, 1} (10^3 triples): TV(p_a*p_u, p_a*q_u) <= TV(p_u, q_u), with equality whenever p_a is a point mass; and the retained joint TV after the event equals the owner TV for a two-node instance with one extra independent retained coordinate (fixed distribution (1/3,1/3,1/3)).

## 4. Preregistered bounded evidence (checker only, numpy pinned, seed 20261018)

- B2: 3000 random trees with 6 to 9 nodes, random retained sets, random uninformed pairs, grades in {0..4}: Theorem 2(a),(c).
- B3: 2000 random histories of up to 4 contractions on random trees with 6 to 9 nodes: Theorem 3.
- B4: 2000 random exact-rational triples on {0..3}: Proposition 4(b) and data processing on the joint.
- B5: 200 random complex operators on a third register (dimension 3) and controlled-add mod 3 on registers u, a: Proposition 5(a) commutation; 200 random classical inputs: Proposition 5(b) (moves then discard = pushforward, below capacity).

## 5. Preregistered rejecting controls (each must be REJECTED; any acceptance is RED)

R1 wrong owner: the distinction claimed at the root instead of r(u) (path 0-1-2, retain {0,1}). R2 copy instead of move: a rule writing x_u into both r(u) and the root claimed to have a unique holder. R3 swapped lineage: the holder claimed to be r_1(r_2(u)) style mis-composition, on a declared chain where the two orders differ. R4 Prop 4 equality claimed for the non-point prior of E4a. R5 the owner-TV bound against the source marginal claimed for the correlated boundary E4c. R6 controlled-add claimed to commute with a generic operator on the owner register. R7 a pair differing at a retained address claimed uninformed. Certificate tampering: missing key, duplicated key, substituted value, wrong value, universe-count mismatch and false provenance (wrong RESULT.md hash) must each make the comparator fail.

## 6. Resource and stopping rules

One Actions run per pushed head, ubuntu-24.04, Python 3.12, pinned `sympy==1.14.0`, `numpy==2.3.5`, `mpmath==1.3.0`. Job order: verify (producer, checker, comparator, controls) then Gemini argument review (`gemini-3.1-pro-preview`, temperature 0, no fallback model) then publication readback (immutable GitHub readback of the frozen bytes at the run's SHA). A RED verify result stops the run before review and is preserved. A REVISE or FAIL verdict is preserved and answered by a new freeze, never by editing this one. Raw reviewer output stays in Actions artifacts; only a summarized receipt is committed.
