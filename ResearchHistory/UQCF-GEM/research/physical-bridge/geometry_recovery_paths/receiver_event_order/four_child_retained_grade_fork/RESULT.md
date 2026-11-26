# Where the ordered four-child repair keeps the event distinction

This companion investigates the [two-chart retained-grade example and its comparison population](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-7178309158). The 25-chart neighborhood-maximum argument and its independent Gemini review have separate inputs. The evidence here is a replay of the archived four-child producer, its independent path verifier, and the archived same-union withdrawal operation.

## A change the source already records

Use the archived v16.53 R row with two ordered chart indices, a Pin and four tips. In a mask the Pin occupies bit 0 and tips 1 through 4 occupy the matching bits. The initial atlas is [31,9]. Chart 0 holds all four tips and chart 1 holds tip 3. Source chart 0's v16.26 withdrawal from tip 3 produces [23,9]. The source atom returns the minimum number of charts needed to cover the four tips before and after the withdrawal, in its tau_before and tau_after fields. They are 1 and 2. In the R producer, the target for normalization equals the cover number of the input and is computed by a separate operation. On the event input it is 2. On the unmodified input it is 1. The caller supplies ordered indices and initiates normalization on each input.

Both executions reach exactly [31,17], with the same labeled atlas, Pin and current cover number 1. Fix any one ambient fine grade assignment across the two executions. All current retained grade vectors also agree at this shared atlas. Up to this visit, chart 1 has seen the same sequence of its own masks after consecutive repetitions are removed, namely 9, 11, 15, 31, 29, 25, 17. For a fixed fine assignment its successive distinct addressed P1 records agree as well.

| Run | Target computed at entry | Next deletion from [31,17] | Sole holder of tip 4 afterward |
|---|---:|---|---|
| Source withdrew tip 3 | 2 | Chart 0 withdraws tip 4 | Chart 1 |
| Unmodified input | 1 | Chart 1 withdraws tip 4 | Chart 0 |

Both final deletions pass the original v16.26 atomic checker. Its returned cover numbers after those deletions are respectively 2 and 1. A fresh call on the shared atlas computes target 1 and ultimately ends at [31,1]. Trying to start there at target 2 raises the original exact-parent precondition. In a continuing run the source-dependent target has already been used to construct the remaining ordered operations. A fresh call and an in-progress path have different control state.

**Finite consequence.** A deterministic function of the current labeled atlas cannot reproduce both next operations at this identical input. Adding the receiver's sequence of distinct local records does not resolve this particular fork. At least two distinguishable continuation states would be necessary to reproduce both choices. On this example the already computed target suffices. This is a claim about the archived deterministic executions. The model could instead admit both next moves at the shared state.

## Exact extent in the historical R campaign

We independently reconstructed all 2,507 R rows with the archived support-set verifier and compared ordered identities with the producer. A comparison fixes a receiver, an unordered pair of hidden tips with the same initial holders, a different source chart, and a legal withdrawal at a third tip. The receiver initially omits both tips, and its unmodified endpoint omits both. A positive comparison has at least one of the two tips in the source-prepared endpoint. Swapping their distinct positive grades gives equal prior receiver P1 and distinct addressed endpoint P1. An input atlas or a pair of paths can occur in several comparisons.

Of 2,730 eligible comparisons, 312 have this lasting endpoint distinction. In all 312 the unmodified path also exposes a hidden tip along the way. In 260 positive comparisons the two paths revisit an identical full atlas and have different next moves there. At some such fork in every one of those 260 the receiver's own mask history agrees after consecutive repeats are removed. Within the remaining 52 positives the two full paths share no atlas at any point. These 52 also use the original supplied ordered caller.

| Chart count | Initial cover in unmodified run | Initial cover after source | Positive comparisons with a fork | Positive comparisons with disjoint paths |
|---:|---:|---:|---:|---:|
| 2 | 1 | 2 | 12 | 0 |
| 3 | 1 | 2 | 240 | 0 |
| 3 | 2 | 3 | 8 | 52 |

Every one of the 2,730 comparisons checked equality between the original source atom's tau_after and the target separately computed by the original producer. This equality follows from their common cover definition. The open question is whether a continuing native operation preserves that target, makes it available beyond the source, and initiates the next edit from it. The 52 disjoint comparisons do not settle that question. No time coordinate is used in the comparison of consecutive distinct records.

## Reproduction

Run `python3 -B check.py HISTORICAL_CHECKOUT --raw positive_rows.json`, with historical sources from commit `e61d5b0e827f7b412824ad46021e2ad6cc6f7875`. Compare stdout with `result.json` and the raw record bytes with the decompressed `positive_rows.json.xz`. Each raw row records the matched comparison, both initial targets and every pair of path indices at an identical atlas with different successor operations. The independent historical verifier checks every normalized path used by the computation.
