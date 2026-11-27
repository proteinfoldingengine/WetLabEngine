# The original witness verifier read four event fields

Two original v16.27 execution paths read different things. The campaign runner opened historical-producer.log and compared four totals. Earlier in that campaign, the original test_complete_bounded_search called produce(4) and passed its in-memory return directly to verify_document. The archived historical-v1627.log records that test passing. The verifier reads first_witness, validates both event paths, and returns four totals and one digest. This locates an executed reader of individual event data beyond the comparison of totals. The earlier test and later file-producing command run in separate processes. [Campaign commands](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/completion/run_campaign.py#L17) · [Historical test](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/test_gate.py#L14) · [Recorded test transcript](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/completion/evidence/historical-v1627.log).

The follow-up passes the archived log document to the unchanged verifier five times. It holds every outer summary field fixed. Each call executes the full historical four-site enumerator. The reader reconstructs the next state from the current state, chart index and site, then computes the global height increment. It also checks the shared endpoint, increment sum and which addressed increments differ across the two paths. [Original verifier](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/verify.py#L13).

| Contents of the four step receipts | Unchanged v16.27 document verifier |
| --- | --- |
| Original log | Accepted |
| Reverse all four trigger bits | Accepted, identical returned document |
| Keep only before, index, leaf and delta_h in each step | Accepted, identical returned document |
| Change one delta_h | Rejected with delta |
| Change one step's before row | Rejected with chain |

The original v16.26 per-atom verifier rejected all four reversed triggers individually. Thus a field can be retained in a genuine receipt, and meaningful to its originating validator, yet omitted by the downstream historical path check. The comparison that read the saved file used four totals. The older per-event verifier returned a global validation summary. Neither inspected operation posts a receipt to a chart or changes that chart's retained view. The mutations are this follow-up's tests, independent of the historical transcript. [Prospective control scope](SCOPE.md) · [Complete outputs](results.json) · [Runnable check](check.py).

A second source check searched the 1,548 tracked UQCF Python files at the same historical SHA for literal first_witness. The only matching files were the v16.27 engine and verifier. A search for explicit factor calls also located a route from factor steps to retained numerical grades in the historical research checks. In check_minimal_completion, the caller supplies B's endpoint, reads each step's after into a mask path and checks delta_h separately. The grade traversal receives the successive masks and a supplied initial grade. On a deletion it updates only the actor's own grade by the P1 push. The field-to-input trace ends at the after masks here, with no chart-owned receipt passed to the grade update. These searches bound the inspected spellings and revision. [Factor caller](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_minimal_completion.py#L131) · [Grade update](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_routed_grade.py#L66).

To reproduce, set DEMOS to the demos directory in historical checkout e61d5b0e827f7b412824ad46021e2ad6cc6f7875.

```bash
set -euo pipefail
python -B check.py "$DEMOS" | cmp - results.json
```
