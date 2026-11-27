# Which other chart loses a possible withdrawal?

All four genuine receipts saved in the original v16.27 campaign affected an identifiable other chart under the v16.26 withdrawal rule. Whenever chart 2 released site 1, chart 0 became obliged to retain it. Whenever chart 2 released site 2, chart 1 became obliged to retain it. Reversing the order reversed the receipt's trigger for each named release. The affected chart and the lost action stayed the same. Both remote charts had the same holdings immediately before and after each source event.

| Original logged path | First release by chart 2 | Second release by chart 2 |
| --- | --- | --- |
| A | Site 1, trigger true, chart 0 loses release 1 | Site 2, trigger false, chart 1 loses release 2 |
| B | Site 2, trigger true, chart 1 loses release 2 | Site 1, trigger false, chart 0 loses release 1 |

The log stores the four source receipts. The remote consequence in this table is a new counterfactual calculation on their exact before/after states. In separate tests of each logged step the affected chart could release that site beforehand. The same original call after the event raised the historical same-union exception and left every supplied row intact. The log contains no such challenge calls.

## Exact criterion for a single successful cut

Let U be the finite covered rooted tree, possibly a proper subtree of the ambient tree. Views are ancestor-closed and contain the root. Fix a legal v16.26 withdrawal by chart A at vertex x, and any other chart R. A possible word at R is a finite sequence of its own successful withdrawals, obtained from any finite valid continuation by erasing every other chart's actions. Stopping immediately gives the empty word. This definition uses existential possibilities and has no clock, fairness rule, command scheduler or chosen terminal endpoint.

**Theorem.** The set of possible words at R shrinks precisely when x is a leaf of U and its holders immediately before the cut were exactly A and R. In that case it loses exactly the old words containing x, including the one-letter word x. Otherwise it keeps every old word. A single successful cut can therefore constrain at most one other chart in this sense. At the instant of the cut R's stored holdings always stay the same.

**Proof.** Any word realized with interleavings can be replayed in its original order at R while all the other charts retain their initial holdings. Its successive local leaf tests are identical. Each intermediate union still contains the whole original U because the exterior was only allowed to shrink in the interleaved run. Conversely, the replay with fixed exterior is itself a legal continuation. Thus the possible words at R depend only on its own initial row and the union of the other initial rows.

A's cut only removes x from one exterior row. If R does not hold x, legality of A's cut requires another exterior holder. If a third chart holds x, the exterior union at R is also unchanged. Otherwise A and R were the only holders and the exterior union at R loses precisely x. Exactly the old words deleting x would fail under this change. If x is a leaf of U then R can delete x immediately before A's cut. If x has any covered child c, A cannot hold c because x was an eligible local leaf at A. Every holder of c must also hold x. Consequently R is c's only holder even before A's cut. The conserved union and ancestry compel R to keep c and x throughout every continuation. There was never a word at R deleting x. This proves the criterion including internal vertices. It applies to withdrawals only.

The result refines the earlier terminal-leaf ownership calculation to the complete set of finite action sequences, with arbitrarily interleaved cuts by other charts. It describes what the historical same-union test enforces. The cover-number trigger tests a different property, whether any former minimum cover of the parent's children survives. [Original operation and returned fields](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py#L23) · [Earlier terminal ownership result](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/P1_TERMINAL_OWNERSHIP_RESULT.md).

## Full historical census

The original bound includes every shape through five vertices and its historical starting families of up to four distinct views covering the tree. Each row below counts a starting family and one successful addressed cut. The digital record includes each other chart's identity, its before/after number of possible words, and all lost words.

| Receipt trigger | Global height increase | No other chart loses a word | One other chart loses words |
| --- | --- | ---: | ---: |
| False | 0 | 8,209 | 7,675 |
| True | 0 | 4 | 17 |
| True | 1 | 1,472 | 2,618 |

The two predicates disagree on 9,151 of 19,995 cuts. Of the 21 true triggers hidden in the global height, 17 constrain a remote chart and four leave all remote action possibilities unchanged. A criterion based on exactly two holders without the union-leaf requirement gives 379 false positives.

The [five-site archived control](../receipt_trigger_fidelity/RESULT.md) compares two different earlier cuts by chart A. On the subsequent marked C−2 event, E (archive index 0) loses its only nonempty word in record 1392. No other chart loses a word from the marked event in record 1393. C itself has exactly the empty word and the one-step release 2 available before the marked cut in either history. Afterwards C has only the empty word in both, even when other charts may continue pruning. The archive recorded the two profiles centrally. C's identical holdings and entire remaining local action histories cannot encode which of its two triggers occurred.

## Provenance and reproduction

[Prospective scope](SCOPE.md) · [Earlier campaign custody trace and hash](../geometry_recovery_paths/receiver_event_order/receipt_provenance_log/RESULT.md) · [Original logged receipts](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/completion/evidence/historical-producer.log).

Run these commands with DEMOS set to ResearchHistory/UQCF-GEM/demos from historical checkout e61d5b0e827f7b412824ad46021e2ad6cc6f7875.

```bash
set -euo pipefail
python -B replay.py "$DEMOS" fresh-records.json.xz | cmp - results.json
python -B verify.py fresh-records.json.xz | cmp - verification.json
xz -dc fresh-records.json.xz | sha256sum
```

The native pass reproduces the archived event digest for every shape, including its receipt fields, and validates the four saved returns against the original implementation. The separate mask enumerator compares the entire 1,996,520-byte uncompressed certificate. It independently traverses the full interleaving graphs through four sites, covering 4,441 state/chart pairs over 1,198 states, including states reached from the original starting families. The larger finite check uses the proved interleaving reduction. The exact certificate SHA-256 is bdd88eb845306aadc18aa4cfce448d97a31228cd06a5e1240aba34cb664f935e.

**Receiver-owned delivery remains open.** The native rule determines which chart must keep a site and which future actions disappear. The source operation makes no write on that chart. The historical refusal is an exception to a caller, with no participant-side refusal record. Neither the census nor the theorem promotes the changed option to an observation or an event receipt in that chart's retained state.
