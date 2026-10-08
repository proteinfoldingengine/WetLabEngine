# C3 optimal host theorem — author-side audit

Date: 2026-10-07.
Status: AUTHOR-SIDE AUDIT PASSED; independent review pending.

Frozen scope 22d0f1cfa93406379e9e0950d12548c422495f28.
Proof candidate b91a850caf5b9e56094698cdd475243b793c62db.

1. Six endpoint-differing toggles and minimum two off-endpoint toggles force an eight-edit optimal path to contain exactly one off-endpoint add/delete pair.
2. All endpoint-only first moves are illegal: deletions violate floor2 and three additions create explicit two-covers.
3. Enumerated all absent non-target first additions for each of four roots over palette {a,b,c,d,e,w}; only +w to a root preserves tau>=3.
4. r2 cannot host w in an eight-edit path because it has no endpoint deletion and any off-endpoint deletion besides -w exceeds the budget.
5. For r1 or r3, +w forces the corresponding -a next; explicit two-covers block all remaining endpoint additions.
6. r4 +w,-d unlocks the already independently accepted eight-edit repair. This proves UNIQUE HOST r4 among shortest paths.
7. The conclusion is restricted to shortest eight-edit paths in this exact palette/carrier. No exclusion of longer alternative-host paths.
8. Host selection reads declared endpoint supports, not an undeclared hidden full state; no multi-fiber retained compression theorem.
9. No numerical campaign or physical claim.

Rejecting controls: r1, r2, r3 hosts each fail under the eight-edit budget, and all non-w first additions admit named two-covers.

C3 general renewable host selection remains open.
