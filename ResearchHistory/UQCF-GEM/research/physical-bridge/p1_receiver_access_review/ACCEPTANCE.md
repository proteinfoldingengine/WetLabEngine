# Independent review acceptance — P1 receiver-access correction

## Frozen object

The reviewed scientific object is commit `6d230eb9efc4ddf3c4b12132c0dbbd693d0915bc`, containing the corrected P1 conditional acquisition theorem and the separation of event typing, receiver access, and preparability. The workflow checkout is `ef2b4ede36570298f202772c8855c9706b3be835`.

## Result

Gemini 3.1 Pro Preview returned **ACCEPTED** with no findings, missing assumptions, or counterexamples. The separate publication audit returned **PASS**. All three attempt-2 jobs completed successfully.

The acceptance covers:

- the conditional P1 acquisition result;
- uniqueness of typed pruning under the stated interface;
- the ancestry-retention consequence forcing P1 under its premises;
- the T-156 correction that centrality is not operational access and that the acquisition claim is presentation-relative.

It does **not** establish a physical receiver or close the native event bridge. The reviewer explicitly records `native_bridge_status: NOT_DERIVED`.

## Remaining assumptions

1. **EB — event typing:** identify an actual pruning event with the typed contraction on the same provenance-bound object.
2. **AB — receiver access:** show that an inherited native receiver interface gains the relevant post-event distinction without an added observer query, selector, table, copy operation, READS graph, or instrument.
3. **Preparability:** establish the physically permitted pre-event comparison states/records where required.

The later T-157 access-functor lemma and PR #120 event-loss inversion theorem were not in this frozen review object. They remain separate and unreviewed.

## Evidence

Raw prompt, request, response, structured verdict, model metadata, review identity, complete job logs, artifact manifests, workflow identity, and the independent publication audit are retained in `evidence/attempt-2/`.
