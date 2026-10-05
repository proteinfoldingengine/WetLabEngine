# Independent A11.X48 whole-argument review

Review date: 2026-10-05 UTC.

Exact candidate commit: 04c4f4ff452459d63ec39609fbdb878d9a724459.
Exact candidate tree: 306d32b1ade50443c122906fbfd1538a8f037ae7.

Reviewed files:

- A11_X48_SCOPE.md;
- A11_X48_MIXED_PREFIX_COVER_RELAY.md;
- A11_X47_REDUNDANCY_ORBIT_OBSTRUCTION_CORRECTED.md;
- inherited A11_X40_SPARSE_WITNESS_RENEWAL.md;
- inherited A11_X45_ORBIT_COVER_TRANSPORT.md;
- inherited A11_X46_CYCLE_GAP_TRANSPORT.md.

## Verdict

ACCEPTED.

The revised candidate proves its stated general mixed-prefix upper interface and its d = 1 alternating-window application. I found no mathematical correction still required. The requested renewal qualification was incorporated: finite-chain reuse is restricted to the same declared cyclic role order or an explicitly template-preserving automorphic order with the required even covers and odd complementary roots. The candidate also now disclaims arbitrary reordered-cycle renewal.

This is analytical acceptance only. It is not numerical execution, an implementation result, an integration merge or a numbered certification.

## Primitive-by-primitive upper proof

For root i = sigma_(p+1), each addition leaves A_i contained in the active support. The mixed-prefix cover K_p therefore hits the active root through A_i, all completed roots through their C supports and all remaining roots through their A supports.

At the union state A_i union C_i, K_p hits through A_i and K_(p+1) hits through C_i. Selecting the latter existential witness changes no incidence and requires no primitive.

Each deletion leaves C_i contained in the active support. K_(p+1) then hits the active root through C_i, completed roots through C and remaining roots through A. Thus tau is at most four at every addition, union and deletion state. The argument uses the exact same endpoint-containing primitive path and root order as the lower theorem.

## Two-cover exception order

The candidate defines

    U = {i : K_plus misses A_i},
    V = {i : K_minus misses C_i}.

K_minus hits every source support and every destination support outside V. Hence it covers every mixed prefix before the first V root completes. If every U root precedes every V root, then when the first V root completes all U roots are already completed. K_plus hits all destination supports and every source support outside U, so it covers that prefix and every later prefix. During processing of the first V root, K_minus protects additions and K_plus protects deletions. Empty exception sets are harmless. The order condition is sufficient exactly as stated.

## Alternating-family orientation

For d = 1, the odd-window complementary roots are

    R_j = Q_(W_(2j+1)).

No cyclic list of distinct total-order positions can satisfy pos(R_(j-1)) greater than pos(R_j) for every j. Therefore some j has the reverse strict inequality. With t = 2j, this is precisely

    Q_(W_(t-1)) before Q_(W_(t+1)).

The physical labels from W_t have source owner set W_t, an even cover, and destination owner set W_(t+1), an odd noncover. In the complementary-root template they miss exactly the destination root Q_(W_(t+1)). Thus this set is K_minus and V is that singleton root.

The physical labels from W_(t-1) have source owner set W_(t-1), missing exactly Q_(W_(t-1)), and destination owner set W_t, an even cover. Thus this set is K_plus and U is the other singleton root. The cyclic ascent gives the exact U-before-V orientation required by the relay lemma.

## Lower and upper arguments on one order

Corrected X47 supplies, for d = 1,

    rho = C(m-2,2) - 2 >= m-2

and the strict X40L central-binomial margin. X40L therefore supplies the lower-safe whole-root order, actual pair witnesses at every primitive, same-floor legality at saturation, literal eligible edits, finite completion, full labelled and noncompact destination restoration, and one toggle for every endpoint-differing incidence.

The cyclic-ascent argument applies to every total root order, so it applies after that exact X40L order is known. X48 changes neither the order nor any primitive. The lower bound tau at least three and the mixed-prefix upper bound tau at most four therefore hold on the same path. Maximum-layer Theorem A is not invoked. Because no edit is added, the endpoint-toggle minimum and common-incidence retention are preserved.

## Renewal

One completed rotation restores the singleton partition, masks, saturated floors and exact-four endpoint. The relay is reconstructed from the next leg's total root order rather than consumed.

The initial candidate overstated this finite-chain claim by allowing an unspecified new cyclic role order on the fixed alternating template. That order need not preserve H_alt. The revised candidate resolves the issue completely: every leg uses the same declared order, or an explicitly template-preserving automorphic order whose even windows are H_alt and whose odd windows have the declared complementary roots. Under that qualification the same cyclic-ascent proof applies on each leg. Per-leg event minimality is correct; no outermost global minimum is claimed for a chain that revisits incidences.

## Separations and limits

The inherited facts remain correctly used:

- H_alt is the complete four-cover family;
- beta = Gamma = m/2 for d = 1;
- H_alt intersect pi^(-1)(H_alt) is empty;
- X45's same-representative lift therefore fails;
- X46's strict scalar condition fails at equality;
- the new relay succeeds because its four-label witness changes across mixed prefixes.

The candidate correctly restricts the positive family theorem to d = 1. With duplicates, a singleton cyclic ascent does not force every copy of U before every copy of V. The prior-method separations, saturated private-support obstruction, unsafe whole-union control and every-root-changes control agree with corrected X47. They are presented only as method controls, not as disconnection claims.

The candidate does not claim arbitrary relay accessibility, below-X40 lower repair, arbitrary cycle reorderings, duplicated-family repair, unrestricted mixed-floor or directed universality, higher-target or nested universality, literature originality or physical interpretation. The proposed next obligation, a multi-stage relay through overlapping exception sets, is properly left open.

## Source integrity

I independently read the exact revised commit and verified its Git tree SHA. The two new X48 sources have no forbidden C0 control characters, no replacement characters and no backslashes. The scope blob is b6c22f3344e3b0970098ba71bef35cad51cb7d83. The revised proof blob is e5b587dbef941647adff24b74111684a150823f1.

Final result: ACCEPTED without further mathematical correction.
