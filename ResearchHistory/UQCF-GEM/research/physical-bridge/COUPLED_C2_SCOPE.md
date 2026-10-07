# C2 — four-root coupled-obligation carrier, frozen scope

Date: 2026-10-07.
Status: PROSPECTIVE ANALYTICAL SCOPE / NO NUMERICAL CAMPAIGN.

Parent C1 structural lemma independently accepted: COUPLED_C1_INDEPENDENT_REVIEW.md at 29e259186a1dafb976a565a62b549b02e986ba09.
Parent C1-C6 program: COUPLED_AUXILIARY_SCOPE.md at f95cdfef30b452e1688172b978ee2e25fb1924d8.

## Objective

Prove or refute a genuinely coupled four-root endpoint carrier: the fourth root itself changes and its state controls legality of the singleton exchange, so it is NOT a passive padded root. Identify actual pair-witness/cover constraints and exact macro precedence without claiming one-auxiliary necessity.

## Exact carrier

Palette P={a,b,c,d,w}, with w globally unused at both endpoints and reserved for possible future auxiliary work.

Four labelled roots, all original floors1.

Source:
    r1={a}
    r2={b}
    r3={c}
    r4={a,d}

Target:
    r1={b}
    r2={a}
    r3={c}
    r4={b,c}

Both endpoints have three distinct singleton requirements and r4 is hit by at least one of them. The overlap changes: source r4 overlaps r1, target r4 overlaps r1 and r3.

Endpoint macro obligations:
    M1: r1 {a}->{b}, Add b then Delete a.
    M2: r2 {b}->{a}, Add a then Delete b.
    M4: r4 {a,d}->{b,c}, Add b, Add c, Delete a, Delete d.

All primitive operations are native incidence toggles; no off-endpoint w is used in the candidate schedule.

## Required analytical checks

1. Exact source/target tau=3.
2. M1 first is legal at every primitive, M2 first is not (test Add a to r2).
3. After M1, M2 is legal; after M1,M2, M4 is legal. Verify the complete 8-edit schedule and exact target.
4. M4 can complete safely at source, but after it completes, neither M1 nor M2 can begin: their first endpoint additions produce an explicit two-cover. This is the key non-passive interaction.
5. Identify the retained pair-witness changes and any macro precedence implications; distinguish sufficient schedule from necessity of a unique global order.
6. Explicitly show why r4 is not a passive padding root: it has its own endpoint difference and changes the legality of r1/r2 edits.
7. Determine whether w is necessary here (likely NOT, because an endpoint-only schedule is proposed). Do not claim auxiliary cycle-breaking from this carrier.
8. Record any counterexample to the candidate claims before publishing a result.

## Boundaries and next step

If this carrier passes, it establishes a genuine coupled-obligation dependency at four roots, NOT yet a coupled cycle requiring a temporary auxiliary. The next C3 candidate must force an auxiliary need, or prove a structural obstruction to such a construction.

No simulation, benchmarking, physics interpretation, or independent acceptance is claimed by this scope.
