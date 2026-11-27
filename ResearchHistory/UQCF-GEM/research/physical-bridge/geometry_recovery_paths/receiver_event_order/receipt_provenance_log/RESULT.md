# The historical campaign saved four original atom receipts

The v16.27 completion campaign contains two distinct routes to the same numerical witness. The independent completion producer constructs dictionaries from its path arrays for WITNESS.json. A second path actually calls the v16.26 atom, carries its returned dictionary through the original v16.27 engine, and serializes it in historical-producer.log. This second file establishes durable campaign custody for four original receipts.

The [recorded historical run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36626045181) completed at 59a74b96c715d539925d494dfe89597a78bd81ed. Its command record lists the old engine.py in the v16.27 parent directory with exit code zero. Its execution metadata pins the source hashes of that engine, the v16.26 atom and the campaign's run_campaign.py. The retained 1,509-byte log matches the original SHA-256 manifest. In this audit the historical checkout was e61d5b0e827f7b412824ad46021e2ad6cc6f7875.

| Stage | Verified operation |
| --- | --- |
| Atom | v16.26 returns a dictionary containing index, leaf, before, after, trigger and delta_h. |
| Enumeration | v16.27 legal_steps appends that dictionary. paths places the same object in the path and takes its after views into the recursion. |
| Selection | witness retains the two paths. produce retains the first differing witness encountered by its bounded endpoint enumeration. |
| Publication | The old engine writes its complete JSON to stdout. The campaign redirects the subprocess's stdout to historical-producer.log. |
| Subsequent read | The campaign loads that file and compares four aggregate counts. This comparison does not consume a chart's receipt. |

[Historical engine](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/engine.py#L4) · [Process and output redirection](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/completion/run_campaign.py#L32) · [Original logged result](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/completion/evidence/historical-producer.log) · [Separate completion producer](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/completion/producer.py#L137).

## Same addressed event in the two recorded histories

The historical log contains a three-chart, two-leaf witness. Chart 2 can withdraw leaves 1 and 2 in either order, reaching the same full endpoint. The first withdrawal always raises the cover number from one to two. The second keeps it at two. Thus its receipt for the same named leaf 1 reports an increment of one when first and zero when second. The two complete height histories are identical.

Chart 2 has different local holdings before it acts on leaf 1 in the two paths, either root plus both leaves or root plus leaf 1 only. This archive supplies no stronger comparison fixing chart 2's complete prior to that particular event. It also does not archive the six-chart witness cited in the live thread. The index 2 identifies the actor inside each global record. The destination of serialization is the campaign file. No recipient inbox, participant-owned retained object or actor-facing reader is present on this route. The enumerator generated alternative paths and saved a representative. This is provenance for an executed software call and its campaign serialization.

## Controls and search scope

An uninstrumented rerun of the complete original 3,486-endpoint enumeration reproduced the archived stdout byte for byte. On a separate full run, a wrapper around the original atom returned the exact same dictionary it received on every successful call. We held references and tested Python object identity on the four rows inside produce's final first_witness. All four were original returns. Deep-copying the same rows preserved equality and failed the identity test. The independently constructed WITNESS.json also matched the parsed witness and carried no such live identities in the audit. Changing one trigger bit failed the raw replay comparison. The original command directory and three source digests independently distinguish the historical invocation from the separate completion producer. Object identity applies in process. The durable claim rests on the traced serialization route, command, source, manifest and exact replay.

The literal filename and alias scan opened all 1,548 tracked Python files under ResearchHistory/UQCF-GEM at the pinned revision. Only the campaign runner mentions historical-producer.log or ORIGINAL_LOGGED_RESULT.json by those literal names. It compares endpoints, paths, multi-path endpoints and path-dependent endpoints. The additional attribute-call inventory records 31 explicit .atomic calls across 20 files, including 18 research-check files. The original demos with this syntax were the v16.26 tests and the v16.27 engine. Filename and call spelling scans do not establish repository-wide absence of indirect, external or differently named readers.

Several later research checks also retain original atomic returns in global certificates. For example the donor-read checker returns the verified dictionary and saves it under source_certificate in its campaign output. The fork-profile checker stores a source_atom and receiver mask data in a common case record. These are additional examples of research records indexed by actor or case. Neither inspected destination binds the receipt to the participant's retained state. The actor-side handoff is still open.

[Donor-read certificate writer](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_donor_read.py#L77) · [Fork-profile case record](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_fork_profile_write.py#L101).

## Reproduce

Use a Git checkout at the historical SHA above with all tracked UQCF Python files, the v16.27 completion metadata, checksum manifest, historical log and WITNESS.json present. From the audit directory run the following command, with HISTORICAL set to the root of that historical checkout.

```bash
set -euo pipefail
python -B replay.py "$HISTORICAL" | cmp - results.json
```
