# Independent source-escape code review

Verdict: **ACCEPTED** for the implementation reviewed below. No Critical or Important blocking issue found. This is a code review, not an attestation of the pending full campaign, prospective-freeze publication, future CI/Gemini results, or final publication.

## Scope and evidence

Read RESULT.md, VERIFICATION_SCOPE.md, PLAN.md, producer.py, independent.py, test_escape.py, the retained missing-producer RED, the initial test syntax failure, and tests_attempt1.log. Compared the inherited source-family definitions against cover_static/VERIFICATION_SCOPE.md and cover_static/producer.py. The supplied prospective freeze is 62b2ed7f62571e0259fb8d3dadfc92aea920e88a and supplied parent is fd505492f7118c664b9cbc61d9c8a85b095c9789; this local code review did not independently retrieve those remote Git objects.

The retained new-suite log reports 42 passing tests. It preserves both the genuine ModuleNotFoundError RED and the earlier syntax failure separately. The full 7,360-source producer/checker, fresh reproduction, and 413 inherited tests were not rerun or certified by this reviewer. Their completed evidence remains a separate required gate.

Small read-only reviewer checks passed: exact equality and uniqueness of both 7,360-source declarations; independent reconstruction agreement for all eight frozen fixtures; brute union-cover enumeration over actual labels for all 5,084 fixture evaluation records; one-bit/native-operation verification of all 99 fixture routes; and direct union checks of the original protected-mask universe, containing 35,166 masks summed over the eight source identities. No implementation file was modified.

## Findings

- **Declared scope:** The five inherited families retain their specified graphs and profiles. Adding the isolated-zero K23 saturation contributes 64, K4 plus leaf contributes 4,096, and K23 disjoint K2 contributes 128, giving 7,360 unique sources. The K5 saturated-star fixture is explicitly one of eight separate frozen controls and is not falsely included in the full matrix.
- **Candidate completeness:** Both programs enumerate each actual label's empty endpoint and every nonempty subset of its own original star paired with every root outside that star. Unsafe candidates remain in the records. The direct enumeration does not filter on the gate, trace, singleton shape, or neighbor degree. Successful actual-label identities are compared to complete V/X predictions, not merely source existence or counts. All covers up to four, including nonminimum covers, are retained.
- **Direct safety and sharing:** Safety computes original floor counts, domination by any original star, fixed palette, and direct minimum union-cover size. Independent reconstruction uses sets and combinations and does not import the producer. Sharing an evaluation by original type and modified footprint is valid: changing a different copy of the same original type permutes labels without altering any safety predicate. Removing identical/empty footprints from the cover-number calculation preserves minimum cover cardinality. Actual candidate, route, and state identities remain explicit.
- **Routes and first events:** Reconstruction starts at the original labelled state, removes roots in the declared order, preserves the X singleton, and adds its outside root last. Each slice is safe; unedited labels are checked unchanged; the escape predicate is false at every earlier slice and true at the endpoint. X additionally checks that every label remains nonempty. Operation records and slices are compared against independent canonical reconstruction. The achieved cost is the source degree, with no optimality claim.
- **Hidden masks:** The protected family is exactly the hidden footprints whose exposed complement is nonempty and is contained in no original star. Since the source core has hitting number three or four, this is equivalent to original full-system lower-three protection. Both programs enumerate every such mask, retain exact distinct state and mask identities, and check that no current footprint covers any exposed complement. The producer uses submask bitsets and the checker explicit set containment. Current core two-label coverage is also excluded by verified original-star domination and source lower-three; upper-four follows from the checked core cover. Sharing repeated footprint truth evaluations loses no state/mask pair. The Cartesian-product count is appropriately separated from slice occurrences.
- **Controls and fail-closed behavior:** The tests cover the pinned static witness, duplicated donor, nonminimum upper-four cover, saturated K2 boundary, leaf/equal-star cases, omitted unsafe candidates, identity and route mutations, source-domain errors, missing/truncated/extra/corrupt streams, and optimized-runtime rejection. Whole records are reconstructed and compared before hashes. Both modules explicitly fail under Python -O, preventing their assertion-based checks from silently disappearing.
- **Scientific scope:** The implementation supports the first-event gate and the declared canonical one-label constructions. The proof distinguishes first escape from later vacancy reachability, sufficient locking from necessary classification, and finite one-hidden checks from the analytical arbitrary-hidden argument. No complete native-component enumeration, arbitrary-path normalization after escape, acquisition mechanism, or broad C3/C4 closure is inferred. Frozen documents' prospective language is historical scope, not evidence that pending runs passed.

## Reviewed file identities (SHA-256)

| File | SHA-256 |
| --- | --- |
| RESULT.md | 1647359880b6261b2c81ab562c6f97b7e98a34e0036915eb3a74d1686f381e43 |
| VERIFICATION_SCOPE.md | c64ee832ae80227f2a92792536edb1e1dce00df7e70306e4ddfe400fb1b55615 |
| PLAN.md | bb68e3701ae48db46873a3d922799066e90ef49d4365f8bf96b4953c6944bac9 |
| producer.py | 9292bcb927e5e30ae2ab84e291afdab6c75db2fd62925ffb0ad0c2b0c1e83b4f |
| independent.py | aa5ef30d27531fe140ab0ce75c08098d07d2f9d007ff440aebd43fe19575cad7 |
| test_escape.py | 0e539621f5755646c5f43a849df27b3c89550a521c40acf42eae619a26630d10 |
