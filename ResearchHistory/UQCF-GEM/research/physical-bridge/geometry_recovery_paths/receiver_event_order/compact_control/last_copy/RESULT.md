# What the five-chart network can retain at chart B

Two different facts coexist on the same supplied five-chart network. The joint history records whether B's deletion of tip 5 increased the minimum cover. Chart B's own P1 root can permanently distinguish who relinquished tip 6. All four combinations occur under the original pruning rules, including when the tip-6 decision is made immediately after the tip-5 probe.

## Before the two histories rejoin

Use the exact unit-grade fixture and the two source histories from [the frozen control](../README.md). Its charts are B, A, E, F and X. In both histories B releases tip 5. Its own row then contains the Pin and tip 6. Charts A and B are the only holders of 6. The P1 root at B is 7 because seven units of the eight-unit fine input already map to the root. The remaining unit stays at tip 6.

| Earlier increment at B's tip 5 | Chart that next relinquishes 6 | New joint cover increment | Minimum cover after that edit | B's retained root |
|---:|---|---:|---:|---:|
| 0 | A | 1 | 4 | 7 |
| 1 | A | 0 | 4 | 7 |
| 0 | B | 0 | 3 | 8 |
| 1 | B | 0 | 4 | 8 |

The same later A edit returns the complement of the earlier B increment. It can do so with the first receipt withheld from its inputs. The mathematical reason is visible in the current cover. After the zero-increment B probe the sole minimum is AFX. Dropping A from tip 6 makes B compulsory and destroys AFX. Four charts now suffice. After the unit-increment B probe the minimum already has size four. BEFX remains sufficient when A releases 6. If B releases 6 instead, AFX in the first arm and AEFX in the second still suffice. Applying the two outstanding source edits from the frozen pair is legal after every one of these four cases.

The B root depends on which chart acted at tip 6. When A releases 6, the remaining B copy cannot be deleted under union-preserving pruning. When B releases 6, its unit goes into B's root, and deletion-only histories cannot put it back. B has no other nonroot site after the probe. Thus the retained grade is stable under every further ordinary deletion, with the given fine grades. This is a distinction in the actual indexed B input to P1. The same later A edit yields different joint certificates with exactly the same B root. Nor does a rule in this comparison select A or B from the value of the earlier certificate.

## After the histories rejoin

Complete the two original paths without touching 6. The identical joined holder sets for tips 1 through 7 are X, EF, E, XF, F, AB, X. Only tips 2, 4 and 6 can still change. Each has three possible subsequent states, namely its original two holders or either one remaining. Therefore there are exactly 27 states, 54 directed single-deletion steps, eight terminal states and 48 maximal paths. For either earlier bit, exactly 24 maximal paths leave B's root at 7 and 24 leave it at 8. These are counts of legal histories. Occurrence or sampling probabilities are unspecified. Every maximal path resolves tip 6, whatever the ordering of unrelated deletions.

All 54 subsequent changes have cover increment zero and a false trigger. X, E and F are individually required by tips 1, 3 and 5. Tip 6 requires a fourth chart, A or B. Together those four cover every remaining tip. The replay compared the complete certificates of every corresponding edge from both old histories, including the whole indexed before and after states. They are identical. The v16.27 event map still returns the distinct earlier values when the earlier paths are retained.

The successor step in v16.26 `factor` and v16.27 `paths` reads the `after` entry of an emitted certificate. Running both routines on all eight terminal destinations recorded 24 and 120 such reads respectively. Both routines also retain path data for their callers. The original `event_map` explicitly reads `delta_h` for attribution. These functions establish where the old bit is available to the joint history caller. They provide no write from that field to B.

## Why the two kinds of order differ

Consider two ordinary v16.26 deletions by different charts, both initially legal on the same fixed rooted tree. Each chart's local tip test depends only on its own row. For deletions at distinct sites, the remaining-holder test at either site is unaffected by the other deletion. Both orders succeed and end with the same indexed rows. The same is true at a shared site with at least three original holders. Any difference in the historical attribution of those two successful edits is lost to functions of that common endpoint alone.

If the two edits concern the same site with exactly two original holders, the first deletion leaves the other chart holding the only copy. The second deletion would change the union and is illegal. All further ordinary deletions preserve that survivor. This proves the distinction for every initially enabled pair by different charts under this primitive. The bit at tip 6 records the identity of the successful withdrawal. It does not encode a relative ordering of two executions at tip 6, since only one can execute. The earlier bit at tip 5 concerns the relative order of two successful edits at different sites.

## Provenance and replay

- **Inherited.** The unmodified [v16.26 atom and verifier](https://github.com/proteinfoldingengine/WetLabEngine/tree/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law), [P1 pushforward](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py) and [v16.27 path and event readers](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/engine.py). Replay checks the Git blob identities for all four Python inputs and the frozen fixture.
- **Supplied.** The five-chart star, unit grades and two source paths from [PR #159](https://github.com/proteinfoldingengine/WetLabEngine/pull/159). The decisive initiator at 6 can be either A or B. Ordinary deletions preserve the union. No additions or changes to fine grades are included.
- **Verification.** The predicted post-join outcomes and independent enumeration contract were [posted before replay](https://github.com/proteinfoldingengine/WetLabEngine/pull/159#issuecomment-7172400564). The immediate four-way comparison is a subsequent exploratory extension. A Cartesian enumeration of holder subsets checked the full identities of all states and edges obtained from the historical atom. The historical verifier checked every emitted edge. The checker rejects a false receipt, a missing successor and attempted deletion of the last copy. Two fresh runs with different Python hash seeds reproduced all result and raw certificate bytes.
- **Open.** The ordinary rules permit either chart to relinquish 6 after either earlier bit. Whether another inherited operation makes that choice depend on the old bit, or grants a physical receiver access to the stored grade, remains open. This supplied star has no archived degree-four geometry or scaling claim. Independent scientific review of this continuation is pending.

From this directory, with Python 3.11+ and SymPy, use the historical checkout at `e61d5b0e827f7b412824ad46021e2ad6cc6f7875`.

```bash
python3 -B check.py /path/to/WetLabEngine --raw actual_raw.json > actual.json
cmp actual.json result.json
cmp actual_raw.json raw.json
```

[Checker](check.py) · [Exact results](result.json) · [All four immediate and 54 post-join certificates](raw.json)
