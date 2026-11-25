# When a joint cover increment remains in chart B

On the five-chart star, a single inherited withdrawal can both change the minimum cover and leave that very increment identifiable in B's retained P1 grade. After the preparations below, the root grade at B equals **8 minus the increment at tip 6**, permanently under subsequent ordinary deletions. Both increments occur. The relation survives every ordering of the other edits. The earlier increment at B's tip 5 can independently be 0 or 1.

## Exact criterion on stars

Fix a finite rooted star covered by labelled charts and a designated tip held by exactly A and B. Other tips have nonempty holder sets. Allow ordinary single-chart, union-preserving tip deletions by any chart. Consider every history up to the first withdrawal at the designated tip. The two possible withdrawals are ordinary-legal while A and B both hold it. Write h for the minimum number of charts covering all tips.

**Claim.** At every such pre-withdrawal state, the increment in h is 1 if A releases the tip and 0 if B releases it, exactly when these two conditions hold at the starting state:

1. A is the sole holder of at least one other tip.
2. B has no other tip.

**Sufficiency.** The private tip keeps A in every cover throughout further pruning. B can cover only the contested tip, which A already covers. Thus B occurs in no minimum cover before the withdrawal. If B releases, every old minimum survives. If A releases, B becomes compulsory too. Every old minimum fails and adjoining B to any one of them gives a cover exactly one larger. The surviving copy thereafter cannot be removed. The same proof with the chart names exchanged gives the opposite orientation.

**Necessity.** If A has no other private tip, designate a non-A keeper for each other tip and prune its other holders until only that keeper remains. These are legal operations while the contested tip stays untouched. If B already owns one of those singleton tips, it is mandatory and can cover the contested tip when A releases it. Otherwise the contested tip required one of A or B and still requires only one. In either case A's withdrawal has increment zero. Separately, if B holds another tip, delete all of its other holders at that tip, retaining B there. B then appears in every cover and A's withdrawal again has zero increment. These witnesses disprove the promised fixed orientation in each excluded case. This claim concerns all ordinary continuations on stars. On a deeper tree the global height can also depend on other parents.

## Two source histories and a common way to prepare the condition

Use the [frozen five-chart fixture](../../README.md) with charts B,A,E,F,X and unit grades. Start immediately after the first B-at-5 probe in its source-(1,2) or source-(3,4) history. B holds the Pin and tip 6 in both. Apart from 6, A holds tips 3 and 4 in the first history, and 1 and 2 in the second.

| Old B-at-5 increment | A's other tips and current coholders | Unique single unrelated edit that makes the criterion hold |
|---:|---|---|
| 0 | 3 with E, 4 with X and F | E releases 3 |
| 1 | 1 with X, 2 with E and F | X releases 1 |

There are seven candidate unrelated single deletions in each case. The original source choices fix which one-step preparation works. Both preparations leave B's own P1 vector at (7,1), and B's only legal deletion at tip 6.

There is also a common, branch-independent procedure on this fixture. Let a fixed subset of E,F,X prune until none of its members has a legal deletion, while A, B and the remaining charts stay fixed. The procedure is a supplied ordering condition. No chart needs to consult the earlier increment to determine the set of permitted editors. A becomes the sole holder of an additional tip exactly if the chosen set contains *all* coholders at one of A's other tips. In that case each such coholder can still leave as long as A remains, so maximality forces all of them to leave. In the opposite case a fixed coholder remains at every such tip.

| Permitted outside editors | Guaranteed in old-0 history | Guaranteed in old-1 history |
|---|---|---|
| E alone | Yes | No |
| F alone | No | No |
| X alone | No | Yes |
| Any two, or all three | Yes | Yes |

Two editors suffice and are necessary for a fixed choice guaranteeing both cases in this protocol. A common permission rule differs from a prescribed common word of *successful* edits. There are nine paired states and twelve edges obtainable by identical successful commands before the contest. None prepares either arm. The non-A holder sets agree between arms, and each other tip that A owns in one arm lacks A in the other. Removing all non-A holders at it would violate union preservation in the other arm.

## What the receiver retains

| Withdrawal at tip 6 | Joint increment | Remaining B row | P1 at B |
|---|---:|---|---|
| A releases | 1 | Pin and 6 | (7,1) |
| B releases | 0 | Pin only | (8) |

After preparation every maximal continuation must resolve the shared tip because either withdrawal remains legal while the tip stays shared. The identity of the withdrawing chart remains free. The minimum-cover certificate and the P1 value follow from the same deletion; no function copies a certificate into B. Knowing the contest occurred, the root value alone determines the increment. B's own vector is already (7,1) before A releases, so this vector cannot tell B whether that release has happened. The legal B menu becomes empty after either outcome; a B-owned way to query that menu has not been established.

This is a retained record of the variable-actor contest at 6. The old fixed-receiver B-at-5 certificate is [a different measured quantity](../RESULT.md). The two old values each permit both B root values, and neither the release nor the preparation phase is selected by the old certificate. Physical observation, initiation, and a geometry or gravity interpretation remain open.

## Evidence

The [test contract](https://github.com/proteinfoldingengine/WetLabEngine/pull/160#issuecomment-7175040454) recorded the first-arm candidate and predictions before native replay. The second source arm, the exterior-only procedure, and the common-command comparison were exploratory extensions. This is author-verified continuation mathematics. Independent review of this new argument is pending.

The checker loads the frozen fixture and verified historical source blobs through the pinned parent checker. It replays the ordinary emitter, separately checks every certificate and compares states and edges against the product of nonempty tip-holder subsets. For **each** single-edit preparation it checked 63 states, 165 legal steps, 21 pre-contest states, 42 distinct contest steps and 12 terminal states. Each arm has 288 maximal orders, 144 for each root value. Counts do not define probabilities. Without preparation a permitted continuation makes both withdrawals yield zero, even as they leave different roots. The exterior-editor test traversed every permitted state for all eight subsets in each source arm. A separate direct recursion on all 4,056 ordered stars with two to four charts and zero to three other tips agreed with the general criterion, including all 169 positive cases in the stated orientation. Two runs with different Python hash seeds produced identical summary and raw certificate bytes.

From this directory, using Python 3.11+ with SymPy, point the replay at historical checkout `e61d5b0e827f7b412824ad46021e2ad6cc6f7875`.

```bash
python3 -B check_memory.py /path/to/WetLabEngine --raw actual_raw.json > actual.json
cmp actual.json result.json
xz -dc raw.json.xz | cmp - actual_raw.json
```

[Checker](check_memory.py) · [Exact results](result.json) · [Historical certificates](raw.json.xz)
