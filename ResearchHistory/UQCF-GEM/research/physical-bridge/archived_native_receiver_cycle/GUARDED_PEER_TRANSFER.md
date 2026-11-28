# An original source release is required for the next peer write

In v16.53 four-leaf case 390, one ordinary call selects label 0, removes it from physical node 3, and adds it to physical node 2 in the very next edit. Node 2 retains it through the canonical endpoint. The caller supplies the four initial supports and palette size. It computes entry rank three from those supports. The call uses its inherited ordering and canonical target. No per-transfer source, receiver, payload, next command or restart is supplied.

| Archived frame | Indexed tree | Holding at node 3 | Holding at node 2 |
|---|---|---|---|
| 5 | [27,29,29] | {0,1,2} | {1,2} |
| 6 | [19,29,29] | {1,2} | {1,2} |
| 7 | [23,29,29] | {1,2} | {0,1,2} |
| 12 (endpoint) | [7,9,17] | {1} | {0} |

## Why this interaction runs

The stock rank-three planner works with the *missing* labels at each physical site. After its initial cleanup, each label is missing at exactly one site. The planner compares the current owner of each missing label with the owner it computes from the canonical target. Direct inspection of the original live tables in case 390 gives physical sites (2,1,1) as current owners for labels (0,1,2), and (3,1,1) as desired owners. Thus only 0 qualifies, and site 3 has capacity. Original transfer code first makes 0 absent at 3, then ends its absence at 2. Original lifting code applies those changes to the indexed tree. The positive write at site 2 is an acquisition of the source's actual outgoing label.

There is an order constraint visible in the physical tree. Immediately before the exchange, 2 is the only site lacking 0. A receiver-first write would place 0 on every branch. A single label would then cover the four branches, two units below the entry rank of three. The original verifier allows at most a one-unit excursion. After the source releases 0, it can legally be added at 2. In the full tree the previous and current masks identify the released label, the source, and the only *other* site lacking that label. These data specify which bit the stock writer sets. This arithmetic does not require reading the target. The choice to initiate this particular transfer does use the target.

Case 684 provides a routing comparison. Node 3 again holds all three labels and releases 0. This time node 1 is its unique prior nonholder. The next stock edit installs 0 there, and it remains there to the endpoint. The initial masks differ between cases; the comparison holds the releasing site's pre-edit support and the released label fixed.

## Two interventions in the actual call

1. **Planner control.** At entry to the original second half of the transfer, remove just the newly established absence of 0 at the source from the planner's live bins. Keep the program counter, payload and pending receiver unchanged. The genuine receiver guard raises `cover deletion` before performing the write. With the release present it succeeds. This tests why a planned receiver write is enabled.
2. **Physical writer control.** Keep the entire previously generated path and its next target frame. After the historical lift has applied the release and immediately before it reads the actual tree to work out its next primitive, restore only the source bit. The genuine lift raises `root step not primitive`: from this altered tree the next target would require changing two sites. In a separate test, swapping the two edits in the archived physical path also fails the original independent verifier with `total excursion exceeds one`.

The first guard reads the planner's live missing-label sets. The second guard reads the tree. The planner decides the two edits before the lift executes them. These interventions show that execution depends on the preceding release. They do not change the fact that a parent computes the route, or imply that the physical edge calls the entry-point dispatcher or that the receiver reads an external journal.

## A positive rank trigger actually enters the rank-three child routine

Dot previously traced a committed restoring deletion into a binary child's call and counted nested cases with an active receiver. Here we checked the four-leaf receiver in tree G. This directly tests whether the specific rank-three routine from the flat dispatch study can actually be invoked in an uninterrupted trajectory. [Prior guard replay and census](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-7235371210)

In original compact identity case 2847, edit 16 removes label 1 from site 8, passing from [79,403,291] to [79,147,291]. The original atom verifier confirms a true local trigger. The parent rises from two to three and the global maximum stays three. The four-leaf subtree at child 1 is identical on both sides. The original parent reads the post-release tree through its exact-rank guard, then calls the rank-three four-leaf normalizer there. Its first edit adds label 1 at leaf 3, giving [79,155,291]. All ten child edits and all eleven projected child states match flat original case 348 exactly. The nested call receives its stored child rank; the parent tests the actual current parent rank. No new top-level invocation is needed. Six original G runs, indices 2847–2852, share this seam and child response.

In each run we intervened only at the first outer guard after the genuine lift returned. Passing the authentic pre-release tree to that guard leaves the actual path, child data, stored targets and pending call intact. The unchanged program then fails the guard, its recorded path stops at the release, and the rank-three child receives no call. This is a direct test of live event-enabled dispatch. The ten child edits end with the original child state; their first gain is transient.

There is also a limit on what this particular guard could convey. At the same full seam, each of the three singleton siblings could have lost either of its two absent labels. We constructed all six one-bit predecessor states. Each original atom has a true local trigger, every predecessor has profile [2,3], the unchanged physical lift accepts each one-step path, and every result is exactly [79,147,291]. All six have identical receiver priors. Only the documented edit at site 8 is asserted to be from case 2847. The fixed post-state and child call cannot tell the six event identities apart. The fact that this child's first added label matches the stock source label does not establish receipt transmission through the guard.

## Scope of the closure

The complete compressed v16.53 certificate regenerated to Git blob `9dd2e4445bca36dfe59f10fc7b7debd1ee2bc81e`. Instrumentation at the original transfer worker located 226 transfers in 124 of the 132 rank-three R runs. Each full path matched the archive and passed its original independent verifier. For all 226 the original v16.26 atom and its verifier reproduced the source deletion exactly. The same label was acquired by the unique prior nonholder on the next physical edit. Every receiver-first alternative would give cover number one. In 132 transfers the receiver kept the label through the run's endpoint.

The software-level statement is existential and constructive: an original uninterrupted operation can select a source release, require it for the next remote write, and retain the released distinction at the destination. None of these 226 source deletions raised the local cover number. They operate *within* a rank-three call. The separate nested G witness supplies an actual child call after a 2→3 rise through the parent guard. In the previously checked three-label flat corpus every actual 2→3 rise ended that trajectory. These cases do not establish transmission of a full v16.26 receipt or of its P1 grade. The payload proved here is the outgoing physical label.

[Stock transfer and its guard](https://github.com/proteinfoldingengine/WetLabEngine/blob/7abbb1b85dc71110498c4a2998b8536c70770891/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/cover.py) · [Physical writer](https://github.com/proteinfoldingengine/WetLabEngine/blob/7abbb1b85dc71110498c4a2998b8536c70770891/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py) · [Checker](guarded_peer_transfer.py) · [All event locations and focal traces](guarded_peer_transfer_results.json) · [Prior entry-dispatch test](RANK_DISPATCH.md)

From the repository root run with Python assertions enabled:

```sh
python ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/guarded_peer_transfer.py ResearchHistory/UQCF-GEM/demos
```
