# The same source pruning can yield two receiver records or no write

The v16.43 star writer reads surviving leaves from a donor and copies them to a receiver during its original execution. I tested whether an actual, fully specified pruning fixes which donor supplies that write when the views have structural identities and the program's numerical order is omitted.

Four original views give a matched control. One holds leaf 1. A reference holds leaves 2 and 3. Source A holds leaves 2 and 4. Receiver B is the unique blank view. In all three original histories below, A first deletes leaf 2. The full preparation, exact post-event holdings and unique three-view minimum cover agree by role.

| Original row | Next record in the same receiver B |
| --- | --- |
| 103 | B acquires leaf 4 from A on the next edit |
| 765 | B acquires leaf 1 from another view on the next edit |
| 3289 | B stays blank through completion |

B can receive a leaf the source never held. The three outcomes arise solely from ordering the same views differently in the original writer. Twelve of the 24 possible orderings emit the specified source deletion first. Six give leaf 4, three give leaf 1 and three stay silent. These are counts of orderings. [Proof and exact examples](STAR_ORDER.md) · [Replay certificate](star_order_evidence/star-order-replay.zip)

## The constraint supplied by the tree

With one blank view and all other views needed to cover the tree, the completed duplicate-leaf cleanup determines a partial order. A leaf's surviving owner has to precede all its original coholders. The writer can copy to B from exactly those occupied views that can come last under these constraints. If only one can come last, the tree identifies a unique possible donor whenever a write occurs. Silence remains possible by putting B last. In the previous three-view examples, conditioning on A's deletion cuts the six orderings to three. Only two of the three send the surviving leaf to B.

I replayed all 74,185 archived paths in the eleven original domains. The formula matched all 263 qualifying preparation and cleanup classes. Sixty-seven allow more than one copying donor. For an exact pruned edge with a unique receiver that stayed blank through that event, each of the 844 observed classes admits both a write and silence. Including the complete preparation gives 258 classes that force a write within the archive. Each of those identifies a single original ordered start once that event is specified. The classes use the preparation and event edge, without conditioning on the full intervening path. [Verifier](check_star_order.py) · [Verification contract and disclosed exploration](STAR_ORDER_CHECK_PLAN.md)

The historical write remains a causal software result. To use it as a physical mechanism, the model needs a rule that fixes whether a transfer occurs and which of the allowed donors supplies it. Physical access to that record also remains open.

## Review and verification

The first Gemini review reconstructed the proof and marked the physical bridge open. Its acceptance JSON put affirmative observations in the objection field, so the review job rejected the format. My first revision then embedded unescaped JSON quotes in the Python prompt and failed before requesting a review. I fixed the quoting and compile-checked the revision. The two earlier runs, including their available raw artifacts and logs, are archived. [First worked review](star_order_evidence/initial-worked-review.zip) · [Prompt syntax run](star_order_evidence/syntax-run.zip)

The final Gemini 3.1 Pro Preview review accepted the mathematical result and marked the physical bridge **OPEN**. Its coverage paragraph needs one clarification. B stays blank throughout the prefix. The audit requires uniqueness only immediately before and after the deletion, and additionally at preparation for the second grouping. The full archive was replayed. The copy theorem applies to the 263 qualifying classes. [Worked review](star_order_evidence/review_verdict.json) · [Raw final review](star_order_evidence/star-order-review.zip)

The two checks on GitHub and the separately extracted frozen checkout reproduced the same certificate SHA-256, `361c3cf6f5efcd8ed67506ab450c22fcb12c66ba5b7ee626227918bb93285a10`. The publication logs and artifacts preserve the raw analysis. [Final verification](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/45040711800) · [Readback receipt](star_order_evidence/readback.json)
