# C3 four-root coupled deadlock — author-side whole-argument audit

Date: 2026-10-07.
Status: AUTHOR-SIDE AUDIT PASSED; INDEPENDENT MATHEMATICAL REVIEW REQUIRED.

Frozen prospective scope COUPLED_C3_DEADLOCK_SCOPE.md at 08eb9dada9c5d4665453768810522303119d2fe6.
Proof candidate COUPLED_C3_DEADLOCK_RESULT.md at a2346862f2aa9c1a4b03b986b2ae3abf2381ec37.

## Independent obligations checked by author

1. Source triangle ab,bc,ac and disjoint de give tau=3.
2. Target triangle bd,bc,cd and disjoint ae give tau=3.
3. Every root begins at floor2. All first endpoint-only deletions are forbidden.
4. First endpoint additions +d(r1), +d(r3), +a(r4) respectively create two-covers {c,d}, {b,d}, {a,b}. No legal endpoint-only first move.
5. Eight native edits +w(r4),-d(r4),+d(r1),-a(r1),+d(r3),-a(r3),+a(r4),-w(r4) reach exact target.
6. At all nine states, first three roots have hitting number2 and r4 is disjoint from their union. Therefore tau=3 exactly.
7. All root supports remain size>=2; auxiliary w appears only in r4 and is absent at exact target.
8. Six endpoint differences plus at least two off-endpoint toggles give a lower bound of eight sequential native edits, attained by the path. This is carrier-specific.
9. Unlike passive padding, r4 actively mediates legality of two distinct +d endpoint changes and its +a is coupled to their -a deletions.
10. The theorem does not prove a compressed retained host-selection rule or general renewable handoff across arbitrary coupled cycles. C3 remains OPEN beyond this carrier.

## Rejecting controls

- The no-first-move proof is native endpoint-only, not a macro-policy obstruction.
- A claim that all four-root overlapping carriers require an auxiliary is rejected by independently accepted C2, which has an endpoint-only eight-edit path.
- A claim that a single auxiliary always suffices for arbitrary coupled supports is not made.

No numerical campaign, formal verification or independent review is claimed by this author-side audit.
