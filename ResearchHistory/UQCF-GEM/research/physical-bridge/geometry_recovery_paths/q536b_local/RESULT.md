# Depth-two recovery enumeration

Only view 12 deleting leaf 2 begins a recovering continuation within two further deletions. That move recovers in one deletion. There are zero recovering endpoints at depth two for both the fixed-minimum and free-minimum degree-four predicates. The search reproduced the outcome previously derived in the analytical proof on PR #156. That expected answer was known before this implementation ran.

| Coverage | Count |
|---|---:|
| Views serving as first actor | 25 |
| Legal first moves, raw feature indices | 32,575 |
| Legal first moves, equivalent features grouped | 15,456 |
| Ordered two-edit paths, raw indices | 1,061,098,050 |
| Ordered two-edit paths, with equivalent copies grouped | 239,000,956 |
| Recovering first moves within two edits | 1 |
| Recovering paths ending at exactly two edits | 0 |

The initial cover, requested source event and recovery gate come from the [prospective registration](https://github.com/proteinfoldingengine/WetLabEngine/blob/7abbb1b85dc71110498c4a2998b8536c70770891/ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/PREREG_Q536b.md). The frozen scientific parent was e7e01bab68ba5171dacd91333f98d208d810dac3. The code reads the fixture and original v16.26 engine pinned at 4538a663258f169ad60c252daef11fe1a1447e13. PEAK memory and timings are in RESOURCES.json. The search ran locally under the preregistered resource limits. No GitHub workflow executed this enumeration.

The producer evaluates both orders and distinguishes two deletions of the same original feature from deletions of different copies of one feature class. It updates work by row and tests all eligible class pairs using NumPy arrays. The verifier reconstructs the class universe, legal moves and work from column cuts in pure Python. Off-editor edges and mandatory neighbor degrees eliminate impossible completions. The two codes compare full recovering record identities, the raw and class counts for each first actor, first class identities, and the full ordered actor-pair coverage table. A regular minimum graph must have an edge avoiding the two editors. Both calculations use that fact to check the actual minimum without fixing it in the diagnostic. Negative controls and the 200 from-scratch reconstructions are in the raw outputs.

The unmodified original engine accepted the source event and all 600 sampled legal actions, and rejected all five illegal controls. The comparator rejected missing, duplicated and substituted records, incorrect first-move coverage, an incomplete class list and a wrong two-step coverage total. Since the actual two-step success set was empty, the duplicate/removal tests used the known one-step positive and a control starting before the source event. The fresh replay reproduced the original result records, complete sample identities and control results after excluding timing metadata.

RESULTS.json gives all 25 individual actor outcomes and both diagnostic fields. To repeat the run, place all files in one folder, install the dependencies listed in RESOURCES.json, and run python run_local.py on Linux. Inputs are hash-checked before the search. The ZIP includes the original immutable fixture, source and run outputs, and a per-file SHA-256 manifest.

This is local bounded verification of the supplied fixture. The proof in PR #156 has an independent analytical review. Stage certification would additionally require the repository's GitHub foundational stack, execution and fresh publication jobs, readiness review, merge and post-merge audit. The numerical run covered depths one and two. Recovery enforcement, receiver access and a physical gravity correspondence are open.
