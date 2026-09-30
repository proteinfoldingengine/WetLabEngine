# v16.37 prospective retained unit-barrier certification

Integrated parent: `8941af1e0b4e0ff1bf575aa163f557bcb35f3a4b`. Its run 36731692842 passed while checking out scientific merge `ce4f0c0396fc4a763e5fac1826c180df599d9a00`. This campaign branches directly from the integrated parent.

## Prior knowledge and chronology

PR82, exploratory head `ca42db8288c6a22b529992c201e6b12061b30b70`, already found a fixed-fiber scalar ultrametric proof, target-barrier dependence of C, a general single-lex-label failure on an abstract graph, and agreement with 18 supplied retained triples, all(1,1,1). These findings are exploratory and are not retroactively preregistered. Their original code/report and run history remain in PR82. This registration precedes this campaign's code and new retained execution.

## Category and primary question

A lineage is a finite rooted tree. A view is a root-containing ancestor-closed vertex subset. A state is an INDEXED tuple of k views covering the whole tree; repeated views are allowed. A move toggles exactly one non-root incidence and preserves valid views and the whole union. q_v is the minimum number of views covering all immediate children of v, or zero for a leaf. Endpoints share q0 and are in different components of the induced q=q0 graph.

Primary costs: c1(Y)=sum_v|q_v(Y)-q0_v|; cinf(Y)=max_v|q_v(Y)-q0_v|; cs(Y)=number of changed coordinates. Each Bj is independently min_path max_Y cj(Y) on the unrestricted legal graph. LEX_BARRIER is the lexicographic minimum of the three path maxima, reported separately using correct nested thresholds. No joint-feasibility or localization assertion is inferred from independent minima.

Question: do admitted retained constructions force unit barriers, or is there an admitted nonunit witness?

## Frozen bounded campaign

All rooted unordered trees with 1 through 5 vertices; every k in1,2,3; all indexed covering view tuples; all fixed-q components; every unordered pair of distinct components and all endpoint pairs they represent. Tree representatives are the lexicographically smallest ancestor-first parent tuple for each rooted shape. States are sorted tuples of vertex bitmasks. Components are ordered by their smallest state; pairs use i<j. No supplied historical pair list defines coverage.

Independent shape reconstruction uses Prüfer trees/root choices/relabelings; producer uses ancestor-first parent arrays. Independent views, q values, graph edges and barrier computations must be rebuilt. Verify exact graph/component/pair identities. The <=4 subuniverse must reproduce the canonical inherited 18 endpoint-pair identities, mapped only by endpoint reversal, not merely their number.

Resource bound: GitHub job timeout45 minutes, no state cap or selective exclusions within this small declared domain. Timeout, missing graphs or incomplete evidence is INCOMPLETE, not bounded success. No expansion beyond five vertices before amendment. Minimality order for any witness: vertex count, view count, parent tuple, q, component representatives. A witness is smallest only in this exhaustively completed domain.

## Competing outcomes

- UNIT_THEOREM: general proof from these definitions, independently reviewed, establishing unit primary barriers for every finite admitted lineage/k.
- NONUNIT_RETAINED_WITNESS: primary barrier differs from1 on a valid disconnected equal-q component pair; independent reconstruction, explicit attaining path and lower-threshold disconnection certify it.
- BOUNDED_UNIT_ONLY: all declared component pairs have primary triple(1,1,1), without a universal proof. This is a complete bounded scientific outcome; universal law remains UNRESOLVED.
- OBJECTIVE_DISTINCTION is an additional diagnostic when LEX_BARRIER differs from independent minima, not a replacement for the primary verdict.
- INCOMPLETE/UNRESOLVED if coverage, proof or execution gates fail. No preferred outcome.

## Gates and controls

A: exact parent/provenance, primary-vs-diagnostic types and domain validation.
B: independently enumerate all51 tree/view-count cases and exact state/q/edge/component/pair records. Count18 is corroboration, never a coverage definition.
C: independent scalar minima and nested lexicographic calculation; attainable paths and failed lower thresholds. Reproduce historical18 identities and values, detect any objective distinction.
D: adjudicate the frozen outcomes. General ultrametric proof is structural and is not evidence of a retained unit theorem. A failed proof attempt cannot be relabeled theorem.
E: reject omissions, duplicates, same-count substitutions, altered barriers, illegal path steps, incorrect q, fabricated shape/state coverage, and false verdicts. Accept reordered record storage with canonical identities preserved.
F: full inherited stack; artifact upload containing raw certificate, source snapshot, stdout/stderr, environment/run/SHA metadata and SHA256 manifest.
G: fresh publication checkout/rerun; byte-identical scientific outputs, fresh verifier and inherited stack; durable evidence and manifest in Git; checksum inspection of the downloaded scientific artifact.
H: independent whole-branch review; ready/merge; rerun verification/reproduction/manifest/inherited stack at the actual merge SHA with an artifact. Only after H passes is the stage closed.

No physical energy/action/gravity or fundamental time is inferred. Time is pruning / ordered recoverability update.
