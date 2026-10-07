# Post-A12 selection/completion: argument audit and scoped analytical closeout

Date: 2026-10-06 (America/Phoenix).
Disposition: ANALYTICALLY COMPLETE FOR THE BINARY-SINGLETON LABELLED SELECTION CLASS.
Evidence: written mathematical proof with author-side audit and immutable readback. Not independent peer review, proof-assistant certification, numerical PASS, benchmark, or physical validation.

## Immutable record

Scope:
- eff1e50769c4e73bd325fe8b1ff06a72ea06d2ee
- POST_A12_SELECTION_COMPLETION_SCOPE.md

Result:
- 1e89814d397763cbfe8157b7cc484a3ba45b5819
- POST_A12_SELECTION_COMPLETION_RESULT.md

Parent dynamic-residual closeout:
- 46ccf73fafb974d8721bfd6736de7201d4cb95d7

## Audit findings

1. Every selected prepared source has tau3 or4. Both singleton types present force a,b,c,d and tau4; one type only gives a three-cover with c,d.
2. During {b}->{a,b}->{a}, anchors c,d and the guard requirement keep tau>=3, while c,d plus a suitable one of a,b always give a cover of size3 or4. Floors remain valid.
3. The complete M_R field depends only on counts n_a,n_b, not labelled ownership.
4. The n=2,m=1 swapped-root pair therefore has identical M_R and immutable metadata but disjoint available first macros. M_R-only deterministic selection fails.
5. Q supplies exact syntax for the selected macro and decreases by one per completed macro. The exact labelled target is reached in 2|Q| primitive edits.
6. The fixed-m lower bound handles adaptive aggregate observations: if two distinct Q,Q' share supplemental record, only a common mismatched root can be legally selected in both; repairing it produces the same aggregate M update and deterministic record update. After their intersection is exhausted, no common valid root remains.
7. Therefore size-m mismatch sets require binomial(n,m) distinguishable initial address records under this policy, requiring ceil(log2 binomial(n,m)) fixed-length bits.
8. Q itself uses n membership bits and, in this deliberately binary class, reconstructs the entire residual state. The result does NOT claim a nontrivial compression here.
9. The lower bound is not extended to probing edits, randomized protocols, external reads, temporary off-target moves, or arbitrary native repair.

No mathematical correction was required in this author-side audit.

## Scientific advancement

The result proves an exact separation between:
- aggregate CERTIFICATE information, which can determine protected legality once a move is named;
- labelled ADDRESS information, which can be required to identify the component that still differs from an exact labelled destination.

This is the first terminating retained-information controller in the dynamic-residual line, but only for the bounded binary-singleton endpoint class.

## Next frontier

The next target is a richer support class where the address record does NOT reconstruct the complete residual incidence state.

The desired theorem is a genuine factorization:
    aggregate certificate field + reduced labelled difference/address state
    -> legal terminating exact completion.

A valid result should quantify both the hidden full-state count and the retained address-state count, prove exact floors/band legality, and supply a counterexample or lower bound showing which distinctions cannot be discarded.

No new numerical campaign is authorized by this closeout.

Closed A12.1-A12.5, certified v16.54/v16.55 and accepted A11 remain unchanged. No A12.6 or physical force/geometry/energy/GR/ADM/dark-matter/continuum/fundamental-time claim.
