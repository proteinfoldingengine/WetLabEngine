# A historical layer repair constructs the receiver-first path

The v16.54 M1 layers routine takes the upper branch supports and a cover-number bound. It computes both endpoints, a preliminary path, and a replacement for the segment that exceeds the bound. On the post-prune upper supports of the v16.51 witness, the replacement writes to receiver 4 before releasing the source at 1. No source address, receiver address, message label or endpoint is passed to the layer routine. This is a construction of a path in upper-branch incidence. Its execution on a full retained tree and its invocation from the v16.26 event API are distinct questions.

| Step | Preliminary tree masks | Returned tree masks |
|---|---|---|
| Start | [499,655] | [499,655] |
| First edit | [497,655], remove 0 at node 1 | [499,671], add 1 at node 4 |
| Second edit | [497,671], add 1 at node 4 | [497,671], remove 0 at node 1 |

The table lifts the upper rows back to the unchanged descendants of this witness. Every branch stays nonempty and nested under this lift. The upper cover numbers on the preliminary path are 1,2,1. On the returned path they are 1,1,1. The invocation starts from the middle configuration of the preliminary path. It does not intercept a live deletion or send a message backward through an existing execution.

## Which decisions the original routine makes

At the peak the supports are {1}, {0}, {0,1}. A minimum cover must contain both labels. The routine takes that cover, constructs two legs by copying one cover label into all rows holding the other, and concatenates the reversed first leg and the forward second leg. These operations generate the endpoints. Its clipping loop then replaces peak configurations and joins the surviving ones, adding incidences before removing them. Calling the same routine on the same peak with bound 2 produces only the unchanged peak. The decision to preserve rank 1 has observable content.

An original campaign-domain comparison uses four singleton rows {0},{1},{2},{3} and one row holding all four labels, with bound 3. There the preliminary path removes 0 from the second row and adds 3 to the third row. The returned path adds 3 first and releases 0 second. The original record verifier accepted replay of all 304 M1 layers specifications defined in the v16.54 producer domain for four through six labels. The two-label witness is a new input to the same code, outside that campaign domain.

## Which direction belongs to the recorded source

Two original atomic records enter the same peak. One deletes 0 at node 1 from [499,655]. The other deletes 1 at node 4 from [497,671]. Both have a true local trigger and move the upper cover number from 1 to 2. The layers routine sees the same peak and gives the same default direction in both cases. The prior tree in each event record identifies exactly one endpoint. Starting the returned path at that endpoint produces opposite transfers for the two actual histories. Matching the endpoint and passing the event's prior cover number as the bound are **new composition choices** in our checker. Neither interface automatically calls the other.

For two labels x,y, suppose x was common and its deletion at s destroys that common cover. At the peak, s is the only row missing x and at least one other row lacks y. The two natural completions either restore x at s or fill y at every row missing it. The former is the actual predecessor. To get to the latter while retaining rank one, all of those y writes must be complete before x can be released. This proves a lower bound of one edit per missing y followed by one source release. Across all 600 indexed triggering star histories with two through six nonempty branches the stock layer path, oriented from the actual predecessor, attained that bound, and the last edit was the original signed deletion. The exact receiving set is independent of label names; the order between multiple recipient writes can depend on row order.

The stock source for this result is a path planner. It establishes an inherited construction for a receiver-first path under a bound. Deriving the bound's priority, dispatching the result on the full retained state and identifying a P1-grade receipt remain open.

[Historical routine](https://github.com/proteinfoldingengine/WetLabEngine/blob/7abbb1b85dc71110498c4a2998b8536c70770891/ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/mechanisms.py) · [Checker](layer_handoff.py) · [Results](layer_handoff_results.json)

From the repository root run the following with Python assertions enabled.

```sh
python ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/layer_handoff.py ResearchHistory/UQCF-GEM/demos
```
