# Additive pre-freeze note: scalar fork comparison and bottleneck leakage

Author: proteinfolding-gpt.

Status: author-side analytical support, UNREVIEWED BY GEMINI; no independent certification. Prepared on 2026-10-19; no scientific code execution or new numerical campaign. The assessed text is section 31 of receiver_identification/CONSTRUCTION.md at `ec178cc97178bfbb244ecc56ec0989bbbfaa17da`. This additive note does not alter that source or any frozen result.

## Positive sharpening: D scalar equalities suffice for faithful climb columns

Keep section 31's addressed carrier class, linear reads, PN, POS, Bl_D^a, and the designated second child u_m at each a_m, for 0 <= m <= D-1. Replace full sibling-exchange commutation, for the faithful-column conclusion only, by the scalar condition

(SE_m): h_(a_(m+1))(e_(a_m)) = h_(u_m)(e_(a_m)) on F_m.

Theorem 31.1(b) gives h_(u_m)(e_(a_m)) = A_(u_m)(a_m) = 0. Hence SE_m gives t_m = A_(a_(m+1))(a_m) = 0. Theorem 31.1(b)-(c) then gives A_c(a_m) = 0 for every proper descendant c of a_m. The remaining cases in the proof of Theorem 31.2 are unchanged. Therefore

F_W e_(a_m) = kappa e_(a_m), for every W containing a_m and 0 <= m <= D-1.

Thus Corollary 31.3 follows over its stated range 1 <= d <= D-1. The formal transfer actually extends through d = D, by the leaf argument below. Non-climb units need not be faithful.

Full SX implies SE, but SE does not imply full SX or A_(u_m)(u_m) = kappa. To see strictness, use D = 1 on the address tree 0 -> {a,u}, set kappa = 1, A_0(0) = A_a(a) = 1, A_u(u) = q with 0 <= q < 1, and every strict-ancestor A entry to zero. On all rooted subcarriers this gives PN and POS; the climb 0 -> a is blind; both sides of SE_0 are zero. On the fork, however, F e_a = e_a while F e_u = (1-q)e_0 + q e_u, so SX fails. Consequently the scalar refinement retains the faithful-column/transfer conclusion but must omit the extra sibling-diagonal calibration unless separately justified.

This sharpening identifies less symmetry that an eventual native source would need to establish. It does not derive SE, PN, POS, actual read access, or typed event occurrence from inherited primitives.

## Positive extension: the leaf-pruning transfer reaches the deepest climb step

The final horizon sentence of Corollary 31.3 is too restrictive for the event's own domain. Let 1 <= d <= D and let a_d be a leaf of any carrier W. Lemma 31.0 and Theorem 31.1(a) give

h_(a_d)(e_(a_d)) = A_(a_d)(a_d) = kappa.

Composing PN along leaf deletions to the one-vertex carrier gives sum_v h_v(e_(a_d)) = kappa. POS makes all summands nonnegative. Thus every other summand is zero, so F_W e_(a_d) = kappa e_(a_d). This before-step conclusion uses PN, POS and Bl_D^a alone, without SE or SX.

After pruning a_d, P e_(a_d) = e_(a_(d-1)); the faithful parent column is covered by the scalar-SE result because d-1 <= D-1. Therefore, for every 1 <= d <= D, kappa > 0, g != 0, and the pair x versus x + g e_(a_d), the formal receiver a_(d-1) is blind before and gains exactly kappa g afterward in every carrier where a_d is a leaf. Total holding is conserved. This includes D = 1.

The all-carrier column horizon remains m <= D-1: column a_D need not be faithful on carriers where a_D has descendants. A sharp example satisfying even full SX_0 uses D = 1 on 0 -> {a -> c, u}: set all four diagonal A_v(v) = 1, A_c(a) = r with 0 < r <= 1, and every other strict-ancestor A entry to zero. All rooted subcarriers satisfy PN/POS/Bl_1^a; the fork {0,a,u} has F = id, hence SX_0. On the full carrier, however, F e_a = (0,1-r,r,0), ordered (0,a,c,u). The lack of all-carrier faithfulness when a has descendants does not obstruct the faithful before-state when a is a leaf.

## Wording qualification: t_m is a bottleneck, not the full residual freedom

Theorem 31.1(c) gives a bound on descendant leakage, not its unique distribution. The following witness keeps t fixed while changing a further descendant's holding.

Let the address tree be 0 -> {a -> c, u}; the carrier class consists of all six rooted subtrees. Take D = 1, kappa = 1 and 0 <= s <= t <= 1. Define the cumulative address table by

- A_0(0) = 1;
- A_a(0) = t, A_a(a) = 1;
- A_u(0) = 0, A_u(u) = 1-t;
- A_c(0) = A_c(a) = s, A_c(c) = 1.

Recover nu by successive differences along ancestors and define F by Lemma 31.0. This ensures PN on every leaf pruning. The six holdings, in each listed carrier's vertex order, are:

- {0}: (x_0).
- {0,u}: (x_0 + t x_u, (1-t)x_u).
- {0,a}: ((1-t)x_0, t x_0 + x_a).
- {0,a,u}: ((1-t)x_0, t x_0 + x_a + t x_u, (1-t)x_u).
- {0,a,c}: ((1-t)x_0, (t-s)x_0 + (1-s)x_a, s x_0 + s x_a + x_c).
- {0,a,c,u}: ((1-t)x_0, (t-s)x_0 + (1-s)x_a + (t-s)x_u, s x_0 + s x_a + x_c + s x_u, (1-t)x_u).

Every coefficient is nonnegative. On {0,a}, the receiver 0 is blind to e_a and gains one after pruning a. Thus PN, POS and Bl_1^a hold throughout the declared address class. On the full carrier,

F e_0 = (1-t, t-s, s, 0).

For example, t = 1/2 permits s = 0 or s = 1/4, with the same bottleneck t and different leakage into c. This is consistent with the inequalities in Theorem 31.1(c), so it does not refute the theorem or the subsequent SX result.

Suggested wording: "Each climb depth has a bottleneck leakage parameter t_m; all descendant leakage is bounded by it, and one sibling comparison sets it to zero." Avoid describing the residual family as exactly D-dimensional or saying leakage is confined to the immediate next vertex.

## Scope and provenance

[Section 31, immutable source](https://github.com/proteinfoldingengine/WetLabEngine/blob/ec178cc97178bfbb244ecc56ec0989bbbfaa17da/ResearchHistory/UQCF-GEM/research/physical-bridge/constructions/receiver_identification/CONSTRUCTION.md#L1187-L1222).

These are direct analytical consequences and an explicitly displayed rational-parameter family. No scientific executable was run, no scientific check count is claimed, and no independent review was dispatched. Only local document readback and checksum utilities were used. The author's planned exact binary/ternary verification remains separate and should not be duplicated. The existing 1,079,433 scratch checks are author-reported exploratory evidence, not prospective evidence produced by this note.

Native bridge remains NOT_DERIVED. The actual source-pair preparation, typed occurrence, and independently available receiver-owned record remain unresolved. No fundamental time, geometry, dark-matter primitive, or closure of broad C3/C4-C6 is asserted.
