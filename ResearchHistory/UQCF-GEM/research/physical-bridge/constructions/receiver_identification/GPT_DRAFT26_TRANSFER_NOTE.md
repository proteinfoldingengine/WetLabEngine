# Actual leaf-pruning transfer does not require sibling exchange

Author: proteinfolding-gpt.

Status: additive analytical support, UNREVIEWED BY GEMINI; no independent certification. Prepared on 2026-10-19 from section 32 at `8d9c8d0afe343cadfcf26fc45bfcf41e05467a63`. No scientific code was executed, no numerical campaign was launched, and the owner's planned combined sections 31-32 freeze is unchanged. The mathematical observations and witnesses below are already known analytical findings; they must be disclosed in any later prospective verification contract.

## Positive result first

The actual transfer in Corollary 32.3 needs no sibling comparison (SE), and hence no full sibling exchange (SX). Under (PN), (Bl_D^a), and exactly section 32's restricted positivity (POS_T), every permitted leaf-pruning event along the climb transfers its one-location distinction from the leaf's formal read to its parent's formal read. The scalar exchange is needed for the stronger all-carrier faithful-column conclusion, but is unnecessary for this event-specific conclusion.

Keep section 32's addressed carrier class, linear maps F_W, climb a_0 = 0, ..., a_D, and positivity test class T_D. In particular, positivity includes every side-child fork F(m,u), the chains through every address, Genesis alone, and the separate deepest-source condition on every F(D-1,u). Do not silently replace these by only the designated D exchange forks or the one realized history. No (SE_m) is assumed in the result below.

## Proposition: the actual source pair and its transfer

Let 1 <= d <= D, l = a_d, p = a_(d-1), and let W be any carrier in which l is a leaf. Set Y = W minus {l}, with the P1 pruning map P. Let kappa = A_0(0).

Then kappa >= 0 and

F_W e_l = kappa e_l,

F_Y(P e_l) = F_Y e_p = kappa e_p.

Consequently, for two admitted preparations x and x' = x + g e_l on W, their post-event preparations are P x and P x' = P x + g e_p. Their formal read differences are kappa g e_l before and kappa g e_p after. When kappa > 0 and g != 0, the receiver p has the same formal read in both preparations before the event and different reads afterward, separated by exactly kappa g. Every other retained read has zero contrast afterward. The total holding is conserved separately in each preparation by PN. If nonnegative grades are required, one may take x >= 0 and g > 0; preparability is still a separate premise.

### Proof

Blindness on the climb gives A_(a_i)(a_i) = kappa for 0 <= i <= D. Positivity on {0} gives kappa >= 0.

For m < D and any child u of a_m other than a_(m+1), evaluate the fork F(m,u) on the unit e_(a_(m+1)). The sibling u holds A_u(a_m), while a_m holds kappa minus kappa minus A_u(a_m) = -A_u(a_m). Both are nonnegative under POS_T, including its special deepest-unit clause when m = D-1. Thus A_u(a_m) = 0.

For any descendant c of u, positivity on the chain [0,c] with source e_(a_m) gives 0 <= A_c(a_m) <= A_(parent(c))(a_m). Induction therefore gives A_c(a_m) = 0 throughout every side subtree of a_m. This part of Theorem 31.1 never uses SE.

Now evaluate e_l on the actual pre-event W. Because l is a leaf, its own holding is A_l(l) = kappa. For each proper ancestor a_i of l, the holding is kappa minus kappa minus the sum of its side-child entries A_u(a_i), hence zero. Every vertex incomparable with l branches from some a_i; its holding and the subtracted child terms involve precisely the side-subtree entries just proved zero. There is no strict descendant of l in W. The address-table formula therefore gives F_W e_l = kappa e_l.

Finally PN gives the entire post-event vector directly:

F_Y e_p = F_Y P e_l = P F_W e_l = P(kappa e_l) = kappa e_p.

No all-carrier faithfulness theorem for the parent column, and no sibling comparison, is used. QED.

Under full POS, the before-step proof is even shorter: the leaf already holds kappa, composite PN fixes total holding at kappa, and nonnegativity makes every other holding zero. The same PN equation then supplies the post-event vector without SE.

## Discriminating controls

### 1. Exchange and full-column faithfulness can fail while every permitted transfer succeeds

Take D = 1 on the address tree 0 -> {a,u}, kappa = 1, and 0 < t <= 1. Set A_0(0) = A_a(a) = 1, A_a(0) = t, A_u(0) = 0, and A_u(u) = 1-t. On the four rooted subcarriers the maps, in the displayed vertex order, are:

- {0}: (x_0).
- {0,a}: ((1-t)x_0, t x_0 + x_a).
- {0,u}: (x_0 + t x_u, (1-t)x_u).
- {0,a,u}: ((1-t)x_0, t x_0 + x_a + t x_u, (1-t)x_u).

They satisfy PN, full POS, and Bl_1^a. On the fork, the two children hold t and 0 of e_0, so SE fails, and F e_0 = (1-t,t,0) violates FC. Nevertheless, both permitted events succeed: pruning a from {0,a} sends the read contrast (0,1) to (1); pruning a from {0,a,u} sends (0,1,0) to (1,0) on {0,u}. This is the D = 1 instance of Theorem 31.1(d).

The uncontrolled next-child leak concerns a parent's unit while that child is still present. It does not obstruct the event that removes the child. After that event the branch supporting that leak is absent.

### 2. Event transfer is strictly weaker than FC and POS_T, even with SE

Take D = 1 on 0 -> {a -> c,u}, all diagonal entries A_v(v) = 1, and every strict-ancestor entry zero except A_c(0) = s > 0. This address table defines a PN family. The climb chain and its fork have identity maps, so Bl_1^a and SE hold.

Every permitted event prunes a only when a is a leaf; therefore c is absent. Both permitted event carriers and their post-event carriers have identity maps, so every required transfer succeeds. Yet on the full carrier, ordered (0,a,c,u),

F e_0 = (1,-s,s,0),

so FC and POS_T fail. The displayed equivalence in Theorem 32.1 remains correct under its stated premises. The phrase in its Reading paragraph suggesting equivalence to event transfer should be read as an implication, not as a converse: all-carrier column faithfulness is stronger than the actual leaf-pruning transfer property.

### 3. The deepest-source fork positivity clause must still be retained

Take D = 1 on 0 -> {a,u}, all diagonals 1, and A_a(0) = A_u(0) = epsilon with 0 < epsilon <= 1/2. PN, Bl and SE hold; every test holding of e_0 is nonnegative. But on the fork,

F e_a = (-epsilon,1,epsilon).

The omitted deepest-source positivity clause fails, and the receiver is already informed before pruning. After pruning a, the read contrast on {0,u} is (1-epsilon,epsilon), so the distinction is not confined to the receiver. Removing SE does not license dropping the remaining source-specific positivity conditions.

## Earned consequence and remaining boundary

This removes a supplied symmetry premise from the particular one-transfer target. It does not derive PN, typed climb blindness, the remaining lineage-unit positivity, preparation, actual P1 event occurrence, or an available receiver-owned record. The read maps are still formal. Equality of the proposed receiver coordinate before the event is not yet equality of its complete independently available record, and a nonzero post-event coordinate difference is not itself physical access.

This is a sufficient event-transfer theorem and a strict separation from the stronger FC property, not a new classification of every possible transfer mechanism or a minimality theorem for every possible positivity certificate. Off-climb read entries remain subject to PN and linearity even where positivity is not imposed.

No native milestone, fundamental time, geometry, dark-matter primitive, or closure of broad C3/C4-C6 follows. Native bridge: NOT_DERIVED.

[Immutable source: section 32 and its premises](https://github.com/proteinfoldingengine/WetLabEngine/blob/8d9c8d0afe343cadfcf26fc45bfcf41e05467a63/ResearchHistory/UQCF-GEM/research/physical-bridge/constructions/receiver_identification/CONSTRUCTION.md#L1232-L1263).

[Earlier adopted D25 note](https://github.com/proteinfoldingengine/WetLabEngine/blob/f7807fe675eae4f2c5b697433f9e2cba418e129b/ResearchHistory/UQCF-GEM/research/physical-bridge/constructions/receiver_identification/GPT_DRAFT25_PREFREEZE_NOTE.md). Its SE-based proof remains valid; the direct PN argument above shows that SE is unnecessary for the event-specific transfer.

## Independent review update (2026-10-19)

The argument above is preserved in the exact scientific freeze `443f5148022cb7652842c53426e56a10c8f82c02` at [leaf_transfer_without_exchange/RESULT.md](../../leaf_transfer_without_exchange/RESULT.md). Gemini run 39321243644 returned ACCEPTED with empty substantive objection arrays; integrity and separate publication audit passed. See [acceptance and complete original evidence](../../leaf_transfer_without_exchange/ACCEPTANCE.md). The original UNREVIEWED label records the status when this note was prepared; it is superseded for this argument by that review. This does not certify every claim in sections 31-32. Native bridge remains NOT_DERIVED.
