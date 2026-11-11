# Q146 PREREG (2026-11-11T13:04:49-07:00) — written before q146.py is run
Question: on the P1 tree, when does an automorphism-invariant retention selection (built from the restriction chain {B_j} alone) give the
survivor closure R_inc^- (ledger Thm 13.3(3))? Lemma (to prove): such a σ exists iff every shell partition 𝒮_j is G-invariant,
G = permutations of X_0 preserving every fiber partition π_j.
Conjecture C: 𝒮 is G-invariant for all j iff there is no step j, survivor t, and atom s removed into t at step j with F_{j-1}(t) ≅ F_{j-1}(s)
(isomorphic as leveled sub-dendrograms over levels 0..j-1), EXCEPT when both are singletons and s is the only atom removed into t at step j.
Universe: all rooted trees with n ≤ 6 atoms (parent arrays, root 0), all closed pruning sequences (each step removes any nonempty set
whose complement is prefix-closed and keeps the root; simultaneous multi-node removals included), G by brute force over S_n.
Pass: conjecture C matches invariance on every case. Fail: any mismatch is reported as a counterexample and C is revised posthoc (labelled).
Supplied/inherited: P1 chain, (E1),(E2), Thm 11.1, Lemma 11.4, Thm 13.3 inherited. NOT_DERIVED; local only.
POSTHOC (2026-11-11T13:06:44-07:00): Conjecture C FAILED at n=6 (40 mismatches). Revised criterion C4 tested posthoc, labelled as such: no owner-child/removed-child plain isomorphism within a node (with the singleton/unique-removal exception) AND every pair of plain-isomorphic sibling blocks (at every node, including the virtual root over pi_m) has equal owner-decorated canonical form.
