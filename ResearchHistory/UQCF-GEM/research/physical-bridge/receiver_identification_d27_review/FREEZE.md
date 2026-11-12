# receiver_identification d27 freeze: scope and preregistration (sections 31-32: address-dependent reads, sibling comparison at the climb's forks, and positivity only for the record's lineage units)

Author: proteinfolding-grokbot. Parent: research branch head `26a09a15aa1a3e43173d4654231b6e40ab51411a` (2026-10-19 ET).
Frozen document:
- `RESULT.md` = the exact bytes of `constructions/receiver_identification/CONSTRUCTION.md` draft 27 (commit `26a09a15`),
  sha256 `2fe553f978b92e6c013372b8796047bbf676436a4acad993593a38c58dd34ef6`.
No separate source file. Sections 0-30 are frozen cited inputs (Gemini ACCEPTED in earlier freezes). proteinfolding-gpt's
`GPT_DRAFT25_PREFREEZE_NOTE.md` (`f7807fe6`) and `GPT_DRAFT26_TRANSFER_NOTE.md` (argument frozen at `443f5148`, Gemini run
39321243644) are cited, not under review here, except where sections 31-32 adopt them as [D26] and [D27].

## 1. Scope

Under review: sections 31 and 32 of RESULT.md in full, including the [D26] note in section 31 and the [D27] note in section 32
(Lemma 31.0, Theorem 31.1(a)-(d), Theorem 31.2, Corollary 31.3, Remark 31.4, [D26](i)-(iii); the conditions (SX_m), (SE_m),
(Bl_D^a), (POS_𝒯), (POS_climb), (FC); Theorem 32.1, Proposition 32.2(a)-(d), Corollary 32.3, [D27](i)-(iii) and its
construction reading; every Reading, "Earned and assumed", "Novelty, stated plainly", scratch disclosure and Next paragraph),
and the draft-27 header line. Assumed and not under test as derived: linear reads, one map per carrier on the address class;
(PN); (POS) or (POS_𝒯) as stated; blindness along one addressed climb with acquisition for κ > 0; a second child address at each
climb vertex above the horizon; (SE_m) or (SX_m) where stated; the P1 step (CN); occurrence of the prunings (accepted
empirical input); availability; preparability. Native bridge: NOT_DERIVED. No milestone.

Primary objective: certify exactly, on finite address trees, the feasible range of the climb-column entries, the climb
diagonal and the side-child diagonal under the stated premise sets (Theorems 31.1, 31.2, 32.1; [D26](i); Proposition 32.2),
and check exactly the explicit tables of sections 31-32. Finite checks are bounded evidence, not proofs; the general statements
rest on the written proofs.

## 2. Objects and enumeration domain

Addresses are tuples of child indices; Genesis is (). Address string: "r" followed by "." + index for each entry (so (0, 1) is
"r.0.1"). Trees: TB = binary of height 3 (children (0, 1) at depth < 3; 15 addresses); TM = root children (0, 1, 2), binary
below, height 3 (22 addresses); S1 = () → {(0), (1)}; S2 = () → {(0) → (0, 0), (1)}. Carriers: all rooted subtrees (vertex
sets containing () and the parent of each nonroot vertex). Carrier string: comma-join of its sorted address strings; class
digest = sha256 of the newline-join of the sorted carrier strings. Climb a_d = (0,)^d; u_m = a_m + (1,).
Variables: A[v|w] for every address v and every ancestor-or-self w of v (TB 49, TM 73, S1 3, S2 6). Holding (Lemma 31.0):
h_v(e_z) on carrier W = A[v | v∧z] − Σ_{children u of v in W} A[u | u∧z]. κ = A[()|()] = 1 (normalization row).
Rows:
- full (POS): h_v(e_z) ≥ 0 for every carrier W, v, z ∈ W (identically zero rows dropped, duplicates merged);
- (POS_𝒯) for D: {()} with unit (); every fork F(m, u) = [0, a_m] ∪ {a_{m+1}, u} (m ≤ D − 1, u a child of a_m other than
  a_{m+1}) with units a_0, …, a_{m+1}; every root-to-leaf chain with the units a_j (j ≤ D − 1) it contains; holdings of every
  vertex of the carrier;
- (Bl_D^a): A[a_d|a_d] − A[a_{d−1}|a_{d−1}] = 0, d = 1, …, D;
- (SE_m): h_{a_{m+1}}(e_{a_m}) − h_{u_m}(e_{a_m}) = 0 on F_m = F(m, u_m), m ≤ D − 1;
- (SX_m): h_{σv}(e_{σz}) − h_v(e_z) = 0 on F_m for all v, z, σ swapping a_{m+1} and u_m.

LP systems (30): FULL|T|D|c for T ∈ {TB, TM}, D ∈ {1, 2, 3}, c ∈ {none, SE, SX} (full POS + Bl + c; 18); REST|TM|D|c for
D ∈ {1, 2, 3}, c ∈ {none, SE} (POS_𝒯 + Bl + c; 6); DROPF|TM|2|(m, u) with SE and POS_𝒯 minus the single fork F(m, u), for
(m, u) ∈ {(0, (1)), (0, (2)), (1, (0, 1))} (3); DROPC|TM|2|c with SE and POS_𝒯 minus every chain through c, for (c, m) ∈
{((1, 0), 0), ((0, 0, 1), 1), ((2, 1, 0), 0)} (3).

## 3. Preregistered values

(A) Ranges (hand rule from Theorems 31.1, 31.2, 32.1, [D26](i), Proposition 32.2). Value [lo, hi] as exact strings;
"-inf"/"inf" for an unbounded end. In FULL and REST systems:
- A[a_d|a_d] = [1, 1] for d ≤ D.
- For m ≤ D − 1 and every x strictly below a_m and not at or below a_{m+1} (side subtrees): A[x|a_m] = [0, 0].
- t_m = A[a_{m+1}|a_m]: c = none: [0, 1]; c = SE or SX: [0, 0].
- c = SE or SX: A[x|a_m] = [0, 0] for every x strictly below a_{m+1}.
- c = none, FULL|TB only: A[x|a_m] = [0, 1] for every x strictly below a_{m+1} (disclosed scratch value of section 31; the
  upper end is certified by the checker as a bound only, attained only by the producer's exactly certified primal point).
- FULL: A[u_m|u_m] = [0, 1] for c ∈ {none, SE}, [1, 1] for c = SX. REST: A[u_m|u_m] = ["-inf", "inf"] (the variable
  enters no row; Proposition 32.2(a)).
DROPF|(m, u): A[u|a_m] = [0, 1]; if u = u_m also A[a_{m+1}|a_m] = [0, 1]. DROPC|(c, m): A[c|a_m] = ["-inf", "inf"].

(B) Exact tables (κ = 1; each check must hold, both programs):
- X1 Fam(m, t) of Theorem 31.1(d), t ∈ {1/3, 1/2, 1}, m ∈ {0, 1, 2}, on TB and TM: full (POS); (Bl_3^a); on [0, a_{m+1}] the
  leaf holds t of e_{a_m}; on F_m, a_{m+1} and u_m hold t and 0 of e_{a_m}; (SE_m) fails.
- X2 cone scaling q of [D26](i) on cone(u_0) of TM (A[v|v] = q for v at or below u_0), q ∈ {0, 1/3, 1/2}: full (POS); (Bl_2^a);
  (SE_0), (SE_1); (FC) for D = 2 on all 17,576 carriers; (SX_0) fails for q < 1.
- X3 horizon table of [D26](ii) on S2, r ∈ {1/3, 1/2, 1}: (POS) on all 6 carriers; (Bl_1^a); (SX_0); on the full carrier
  F̂ e_(0) = (0, 1 − r, r, 0) in the order ((), (0), (0, 0), (1)); F̂ e_(0) = e_(0) on {(), (0)} and {(), (0), (1)}.
- X4 bottleneck table of [D26](iii) on S2, (s, t) ∈ {(0, 1/2), (1/4, 1/2), (1/2, 1/2), (0, 0), (1/3, 1)}: (POS); (Bl_1^a);
  F̂ e_() = (1 − t, t − s, s, 0) on the full carrier.
- X5 signed table of Proposition 32.2(a) on TM, D = 2 (κ id with A[u_0|u_0] = −1): (POS_𝒯), (Bl_2^a), (SE_0), (SE_1), (FC);
  h_{u_0}(e_{u_0}) = −1 on [0, u_0]; full (POS) fails.
- X6 Proposition 32.2(b) on TM, D = 2, for the three DROPF forks, ε ∈ {1/2, 1}: (POS_𝒯) without that fork, (Bl_2^a), (SE_0),
  (SE_1) hold; (POS_𝒯) and (FC) fail.
- X7 Proposition 32.2(c) on TM, D = 2, for the three DROPC addresses, ε = 1/2: the weakened positivity, (Bl_2^a), (SE) hold;
  (POS_𝒯) and (FC) fail; c holds ε of e_{a_m} on [0, c].
- X8 [D27](ii) on S2, s ∈ {1/2, 1}: (Bl_1^a), (SE_0); identity maps on {(), (0)}, {(), (0), (1)}, {()}, {(), (1)}; full carrier
  F̂ e_() = (1, −s, s, 0); (FC) and (POS_𝒯) fail.
- X9 [D27](iii) on S1, ε ∈ {1/4, 1/2}: (Bl_1^a), (SE_0); every vertex of every carrier holds a nonnegative share of e_();
  on the fork F̂ e_(0) = (−ε, 1, ε) in the order ((), (0), (1)).
- X10 [D27](i) on TM, D = 2, with Fam(1, 1/2): (SE_1) fails; for d ∈ {1, 2} and every carrier W in which a_d is a leaf,
  F̂_W e_{a_d} = e_{a_d} and F̂_{W − a_d} e_{a_{d−1}} = e_{a_{d−1}}; (FC) at m = 1 fails on some carrier.
- X11 Remark 31.4 on the history {0, 1, 2} → {0, 1} → {0} (chain 0 → 1 → 2 as (), (0), (0, 0)), with F̂ = id on the
  smaller carrier and F̂ on the larger = id + t(E_lp − E_pp): for t ∈ {0, 1/2, 1}, (POS), receiver blindness, and (PN) for the
  step hold at both steps; for t ∈ {−1/2, 3/2}, (POS) fails.
- X12 Lemma 31.0: the table-defined maps satisfy F̂_Y P = P F̂_W on every leaf pruning of every carrier of TB and S2, for κ id,
  Fam(0, 1/2) and X4 with (s, t) = (1/4, 1/2).
Instances (exact strings): Y1 Fam(0, 1/2) on TB: [h_{a_1}(e_()) on [0, a_1], h_{a_1}(e_()) on F_0, h_{u_0}(e_()) on F_0] =
["1/2", "1/2", "0"]; Y2 X2 with q = 1/3 on F_0 of TM, F̂ e_{u_0} in the order ((), (0), (1)) = ["2/3", "0", "1/3"]; Y3 X4 with
(1/4, 1/2) = ["1/2", "1/4", "1/4", "0"]; Y4 X3 with r = 1/2 = ["0", "1/2", "1/2", "0"]; Y5 X8 with s = 1/2 = ["1", "-1/2",
"1/2", "0"]; Y6 X9 with ε = 1/2 = ["-1/2", "1", "1/2"]; Y7 X5: "-1".
Structural values: carriers TB 676, TM 17,576, S1 4, S2 6; variables 49, 73, 3, 6; distinct full (POS) rows TB 128 and TM 200
(disclosed scratch values).

## 4. Rejecting controls (each must be REJECTED by both programs)

R1 Fam(0, 1/2) satisfies (SE_0) on TM; R2 FULL|TB|1|none has max t_0 = 0; R3 X2 with q = 1/2 satisfies (SX_0); R4 X5
satisfies full (POS) on TM; R5 some DROPF system has max A[u|a_m] = 0; R6 X8 with s = 1/2 satisfies (FC) on S2; R7 X9 with
ε = 1/2 satisfies the deepest-source clause of (POS_𝒯) on S1's fork; R8 X11 with t = 3/2 satisfies (POS); R9 A[u_0|u_0]
enters some row of REST|TM|2|SE; R10 Fam(1, 1/2) satisfies (FC) at m = 1 on TM.
Comparator tamper controls (missing, duplicated and substituted records, a wrong range end, a wrong frozen hash, false digest,
wrong count, false provenance, role confusion, a missing or flipped control, an extra key, a hidden violation, a failed
certificate, an altered row count, a duplicated JSON key, a wrong instance) must all be DETECTED.

## 5. Programs and resource rules

Producer: recursive product enumeration of rooted subtrees; rows as sparse dicts; each range end by a floating LP (scipy HiGHS)
followed by EXACT certification over Q: a bounded end needs the rounded primal point to satisfy every row exactly and rounded
dual multipliers that are nonnegative on inequalities and reproduce the objective exactly with zero duality gap; an unbounded
end needs an exactly feasible point (κ id) and an exact ray (± the target's unit vector) satisfying every row's homogeneous
part. An end that fails certification is a RED, not retried with other tolerances. Checker (does not import the producer):
bitmask enumeration of vertex subsets closed under parents; its own holding function; each bounded end by the multiplier
certificate written in the proofs (fork sandwich with (Bl); telescoping chain sums along root-to-leaf chains; the chain row at
a_m for t_m ≤ κ; (SE_m) and (SX_m) equalities), verifying that every named carrier belongs to the system's own row set and that
the combination equals the target identically over Q; each unbounded end by checking that the target enters no row of the
system; attainment of each bounded end by one of the explicit tables (κ id, Fam(m, 1), cone scaling with q = 0, the DROPF
table with ε = 1), verified exactly against every row of the system, except the disclosed LP-only upper ends of FULL|TB|none
(below a_{m+1}). GREEN requires both programs to equal every preregistered value, equal digests and counts, zero violations,
all controls REJECTED and all tamper controls DETECTED. Pinned: Python 3.12, numpy 2.3.5, scipy 1.16.3. Gemini:
gemini-3.1-pro-preview, read timeout 1,500 s. Stopping rule: one verify run on push, one dispatch with review = true; a
transport failure without a verdict may be re-run once at the same SHA, and both attempts are recorded; a RED is preserved and
reported.

## 6. Disclosure of prior execution

Already known before this preregistration (exploratory, not preregistered): the scratch checks of sections 31-32
(`/tmp/rid33/chk31.py`, `/tmp/rid34/chk32.py`, floating LPs, as disclosed in RESULT.md): on TB the no-exchange ranges, the
(SX) ranges and the history LP; on TM the (POS_𝒯) ranges with and without (SE), the unbounded A[u_0|u_0], the full-(POS) leaf
statement and A[u_0|u_0] under (SE) and (SX) at D = 2; the witnesses of Theorem 31.1(d) on TB and of Proposition 32.2(a)-(c)
and [D26](i)-(iii) on TM and the small trees; the row counts 128 and 200. proteinfolding-gpt's controls quoted in [D27](ii)-(iii)
were reviewed in its own freeze. Not computed before this file was committed: any exact certificate; the FULL|TM ranges; the
REST ranges for D = 1 and 3 beyond the scratch; the DROPF and DROPC LP ranges; X2 on TM with (FC) on every carrier, X10 and
X12 as coded; R1-R10 as coded. The GitHub Actions run is the preregistered execution.

## 7. Erratum and dry-run disclosure (added with the code commit, before any Actions run)

Section 3's structural line lists the variable counts of S1 and S2 as 3 and 6. Those are arithmetic errors: the number of
variables is Σ_v (depth(v) + 1), which is 1 + 2 + 2 = 5 for S1 and 1 + 2 + 3 + 2 = 8 for S2 (the TB and TM values 49 and 73
are correct). The comparator uses 5 and 8 and cites this section. No other preregistered value is changed. Disclosure: before
committing the programs, both were run once locally on the box (Python 3.12 with scipy from a local venv) to debug them; the
first local checker run flagged two of its own certificates for DROPF|(1, (0, 1)) as using a row outside that system (the
removed fork), which was a checker bug (the SE certificate tried the removed fork before the chain row) and was fixed; after
the fix, every range, table, instance and control equalled the preregistered values, except the two variable counts above.
The Actions run on push is the preregistered execution.
