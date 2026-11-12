# T-235 — Pair-delivery premise reduction: preregistration

Author: proteinfolding-grokbot (UQCF Science Agent), 2026-10-31 America/Phoenix (MST).
Authority: Aaron Spradlin's direct voice instruction of 2026-10-31 3:29 PM MST ("actively shrink the set of not-derived inputs ... derive those claims step by step ... leave the ones still out of reach explicitly labeled ... track everything on GitHub via PR on the research branch").
Verified integrated parent: research/uqcf-overlapping-guard-exchange at `0dfa5c60bd0a2838f70480035bff255428e934dd` (re-read from GitHub at 3:30 PM MST). Agent thread head `bdaa14e95691e9cebf99741447f055fe4852b051` (T-234). AGENTS.md sha256 `56d5ffb2d1f8f0d1a1660b6cc5b31ebae92b59fb48b547e7d47ea13f0bafdee0`.

This file is committed BEFORE any numerical execution for this stage. No script has been run.

## 0. Disclosure of already-known (exploratory, hand-only) findings

Everything below in sections 2-3 was worked out by hand on 2026-10-31 between 3:30 and 3:50 PM MST while reading `receiver_identification_d28_review/RESULT.md` (sections 26, 31, 33), `foundational-closure-verification/PROOFS.md` (P1, P2, P6) and `TYPE_LEDGER.md`. No code was executed. These are exploratory findings; they are NOT relabelled as preregistered predictions after the fact. What is preregistered is the frozen check that will test them, the universe, the controls and the stopping rule.

## 1. Frozen mathematical objects

- Carrier: finite rooted tree W (FCV L1: prefix-closed, common Genesis 0). Grades F^W over Q (FCV L6, relative units). P = P_{W,Y}: the FCV P1 pushforward for the single leaf pruning Y = W \ {u} (CN), so P e_u = e_p, P e_z = e_z otherwise. I: FCV P2 zero extension.
- Fork: p a vertex with two distinct leaf children u, v in W. σ: the transposition of u and v (a root- and parent-preserving bijection of W, i.e. an FCV admitted relabeling).
- Balanced pair (T-224/T-225): two preparations differing by Δ = (e_u − e_v)/5. Preparation is SUPPLIED and stays supplied.
- Read map: linear F̂_W: F^W → F^W and F̂_Y: F^Y → F^Y (holdings, the d28 setting). h_w(x) := F̂_W(x)_w.
- (PN-step): F̂_Y P = P F̂_W at this one step (d28 (PN) restricted to one pruning).
- (SX-fork): F̂_W σ = σ F̂_W (d28 section 31 (SX), applied at the record's own fork, not at a climb fork).
- (Nd): h_u(e_u) ≠ h_v(e_u) on W.
- Scalar effect family anchored at p: one linear functional ℓ_X on F^X for every carrier X ⊆ W with p ∈ X. (INV): ℓ_{X\{l}} ∘ P_{X,X\{l}} = ℓ_X for every leaf l ≠ p of X.

## 2. Claims to be tested (hand-derived, disclosed in section 0)

- O (invariant effects factor through the lineage chain). (INV) holds iff ℓ_X = α ∘ P_{X,[0,p]} for one α ∈ F^{[0,p]}; the solution space has dimension depth(p)+1. Consequently every (INV) effect gives ℓ_W(Δ) = 0 and ℓ_Y(PΔ) = 0 for every Δ ∈ ker P_{W,[0,p]} (the T-225 balanced pair included) and ℓ_Y(Px) = ℓ_W(x) for every x (no (INV) effect can witness the event, T-217).
- P (pair delivery). Under (PN-step) and (SX-fork) only: with c := (h_u(e_u) − h_v(e_u))/5,
  F̂_W(Δ) = c e_u − c e_v (receiver p and every vertex other than u, v hold 0 before the event), and
  F̂_Y(PΔ) = c e_p − c e_v (receiver p holds exactly c after the event; every vertex other than p, v holds 0).
  The receiver-coordinate contrast is 0 before and c after; it is nonzero iff (Nd).
- K (κ is not load-bearing for the pair). Both reads below satisfy (PN) on every pruning of every carrier and every admitted relabeling: F̂^tot(x) = (Σx) δ_0 has total holding κ = 1 and c = 0; F̂^dif(x) = x − (Σx) δ_0 has κ = 0 and c = 1/5.
- N (each premise of P is needed). Dropping (SX-fork) admits reads with receiver contrast ≠ 0 before the event; dropping (PN-step) admits reads whose post-event receiver contrast differs from c; (Nd) fails on a nonzero hyperplane of admissible reads (F̂^tot, the zero read).

## 3. Diagnostic (non-primary) predictions

- dim of the admissible space {F̂_W : (SX-fork) and P F̂_W (e_u − e_p) = 0} is n² − 3n + 3, n = |W| (commutant of a single transposition has dimension n² − 2n + 2; the PN-step condition imposes n − 1 independent equations; F̂_Y = P F̂_W I is then forced). A mismatch is reported as a hand error, not a failure of P.
- Case counts: n = 3, one case; n = 4, two cases (star, and root–a–{b, c}). Counts for n ≥ 5 are not hand-predicted; producer and verifier must agree exactly.
- The T-233 preregistered control: the retained cone totals (C_0, C_p) are (INV) effects, so they must FAIL to separate the pair before and after.

## 4. Universe, objectives, outcomes, resource and stopping rules

- Primary universe U_P: every rooted unlabeled tree with 3 ≤ n ≤ 7 vertices (expected 2+4+9+20+48 = 83 trees) and every unordered pair of sibling leaves {u, v} up to tree automorphism; σ swaps them, u is pruned. For each case the claims of P and the dimension are checked on an exact basis of the admissible space (linear claims, so a basis check is a complete check for that carrier, not a sample).
- Primary universe U_O: every rooted unlabeled tree with 1 ≤ n ≤ 6 vertices (expected 1+1+2+4+9+20 = 37) and every vertex p (up to automorphism); unknowns ℓ_X for every carrier X ⊆ W containing p.
- Primary objectives: O, P, K, N exactly over Q on U_O / U_P.
- Competing outcomes: (i) all GREEN; (ii) RED: any case where P's formulas fail on a basis element, O's dimension or factorisation fails, a K witness misbehaves, or an N witness is not found. RED is preserved and reported, not repaired after the fact.
- Algorithmic independence: produce.py enumerates trees by recursive multiset partitions and solves with sympy nullspaces over the stacked linear constraints; verify.py enumerates trees independently (canonical level sequences / AHU encoding, written separately), builds the admissible space by an explicit orbit parameterisation (no nullspace call for P), recomputes every reported value with fractions.Fraction, and requires exact equality of the canonical universe (same set of canonical case identities) and of every reported value.
- Rejecting controls (verify.py must reject): missing case, duplicated case, substituted tree, wrong contrast value, wrong dimension, non-prefix-closed carrier, false coverage count, false provenance (producer sha mismatch). Plus the scientific controls of section 2 (N) and section 3 (T-233 cone totals).
- Execution: GitHub Actions on branch grok/derivation-pass-t235 (ubuntu-24.04, Python 3.11, sympy==1.13.3, mpmath==1.3.0), with the inherited FCV stack run first (FCV tests/test_fcv.py, verify_certificates.py, v15.56 test_pruning_consistency_audit). Local scratch runs under /workspace/uqcf_scratch/t235/ are disclosed as such.
- Stopping rule: at most two push runs of the stage workflow after the code commit; any infrastructure fix is disclosed. One Gemini referee request, no retry.
- Finite checks are bounded evidence; the general claims rest on the typed arguments in RESULT.md. No finite no-counterexample result is presented as a universal theorem.

## 5. Scope fence (frozen)

No geometry, no fundamental clock, no dark-matter primitive, no fitting. Time is pruning / ordered recoverability update; depth is lineage-address length. A holding is not an available record: nothing here establishes receiver access, that any vertex performs a read, occurrence, or preparation. Native bridge NOT_DERIVED unless an access law is earned, which this stage does not attempt. scientific_breakthrough stays false.
