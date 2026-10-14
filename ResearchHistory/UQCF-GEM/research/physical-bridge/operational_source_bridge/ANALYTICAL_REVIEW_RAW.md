# Independent analytical and source-scope review

Review date: 2026-10-14 UTC, the declared investigation date. Reviewer: independent ChatGPT/Codex analytical subagent dispatched under the requesting-code-review workflow. This is the complete raw review, not a scientific execution or a publication receipt.

**Disposition: ACCEPTED. No unresolved mathematical correctness or source-scope issue was identified in the four bound inputs.** Native milestone achievement is not accepted or claimed: the reviewed report correctly retains NOT ACHIEVED. This acceptance covers the exposed argument and its bounded source assessment only.

## Immutable review inputs

Repository: `proteinfoldingengine/WetLabEngine`. Intended research branch: `research/uqcf-overlapping-guard-exchange`. Inspected parent: `6fd1a19d9757aa922a308782a6e751ee4660e188`. Declared parent tree: `2eedf55ed91cddf4d9c7b0eeb35add1e78f91d80`.

| Input | Exact bytes | SHA256 |
|---|---:|---|
| `RESULT.md` | 19741 | `914afa251924aeeb444fa47f5abefd2d6ce79ce22ec6f2213db14920ab78b94c` |
| `INDEX_APPEND.md` | 2523 | `7dd71aaa4073cda951383ed5029bb94ff3b642b4b074e84ffe04b6c8411daac2` |
| `source_packet.json` | 142383 | `b6322b27383969ef80b2aeeeb6ec810a582eb4dcf5aeae15a9da5a1b76f2fae0` |
| `source_identities.json` | 5532 | `8bf7a8786ecab70236478371838dd68ff7a4da31479c20ce973743c7fae89e0b` |

All four actual local lengths and SHA256 digests were checked against these bindings. The packet contains 19 source records. For each embedded UTF-8 source, its byte length and SHA256 match `source_identities.json`, and its independently recomputed Git blob SHA1 matches both the packet's `sha` and the identity record's `git_blob`. This establishes internal source-packet identity consistency. It does not establish remote tree membership, branch-head identity, publication completeness, or historical certification; those belong to the separate source/publication auditor.

I read the packet's `ResearchHistory/UQCF-GEM/AGENTS.md`. Its numbered retained-stage closure chain is not asserted to have been completed here. This report declares an analytical source/representation assessment, executes no new scientific campaign, preserves historical results without replay, and claims no numbered-stage CLOSED/CERTIFIED status. The native-event milestone and physical-frontier source records explicitly permit a derived probabilistic consequence and do not require unique microscopic dynamics, deterministic outcome selection, guaranteed progress, the entire C3 protocol, or gravity closure. The reviewed report follows those distinctions.

## Mathematical review

### Registered table and scalar defect

The probability rows stated in section 2 match the literal `CHSH_PREREGISTERED` candidate in `operational_family.py`: the first three contexts assign one half to each equal-output pair, and the last assigns one half to each unequal-output pair. The equivalent condition `a XOR b = xy` is correct for binary settings. With outcome signs `(-1)^a` and `(-1)^b`, the four correlators are `(1,1,1,-1)`, the stated CHSH convention gives `S=4`, and the source implementation's `max(0,abs(S)-2)` gives `D=2`.

These arithmetic facts follow from the supplied table. They do not infer frequencies, native sampling, preparation, or measurement semantics. The report consistently makes that distinction.

### The explanatory P_alpha family: equations (1) and (2)

For rational `alpha` in `[0,1]`, the replacement fourth row is nonnegative, rational and normalized. Summing either output over the other gives one half, including at both endpoints. The unchanged first three rows have correlator one; the fourth has `(1-alpha)-alpha=1-2alpha`. Therefore `S=3-(1-2alpha)=2+2alpha` and, on this parameter domain, `D=max(0,abs(S)-2)=2alpha`.

The specified fixed carrier `[0,1]`, operations `[[0,1],[1,0]]`, candidate ID and control role continue to pass the producer's candidate schema conditions. Rational entries can be represented by integer numerator/positive denominator lists, as required by both parsing paths. Neither path binds them to an operation-generated law. The retained reduction ignores its candidate argument, so its constant diamond is unchanged.

The report correctly separates this analytical schema family from the original frozen three-record campaign. It does not claim those altered candidates were enumerated, that alpha is a native physical control, or that identical complete inputs give different answers. It acknowledges the old mutation control and does not promote table dependence to a new scientific discovery.

### Tested quantum interface: equation (3)

The tested class is explicit: one setting-independent finite-dimensional bipartite density operator, local binary POVMs, and Born probabilities from tensor-product effects. Each measurement choice depends only on its own setting. Joint-context operations, setting-dependent preparation, selected-run conditioning and measurement communication are excluded from this specific interface. The tensor-factor locality assumption does not introduce spacetime into the native model.

For a binary POVM, `M_0-M_1=2M_0-I` is a Hermitian contraction; the same holds for the other party. The lifted operators commute across parties. Their product expectation gives the supplied sign correlator. These observations justify the operator setup without requiring projectivity, a pure state, invertibility, or full rank.

### Perfect-correlation proof: equations (4), (5) and (6)

For `E_xy=1`, expansion of the Hilbert-Schmidt norm gives

`|| (A_x-B_y) sqrt(rho) ||_HS^2 = Tr[rho A_x^2] + Tr[rho B_y^2] - 2`.

Cross-party commutation and trace cyclicity justify the two cross terms. Since `A_x^2<=I` and `B_y^2<=I`, each of the two remaining expectations is at most one. The squared norm is both nonnegative and at most zero; hence it is zero. Their sum is then two, so each expectation is one. Thus the two Hilbert-Schmidt vectors coincide and have norm one.

Apply this argument separately to the three perfect-correlation pairs `(0,0)`, `(0,1)` and `(1,0)`. It gives precisely

`A_1 sqrt(rho) = B_0 sqrt(rho) = A_0 sqrt(rho) = B_1 sqrt(rho)`.

Taking the inner product between the first and last vectors gives `Tr[rho A_1 B_1]=1`: both vectors are the same unit Hilbert-Schmidt vector. No division by rho or restriction to a full-rank support was used. Mixed and rank-deficient states are therefore included. The proof is valid for arbitrary binary local POVMs in every finite dimension allowed by equation (3).

Equation (2) instead demands `E_11=1-2alpha`. The conjunction is possible only at `alpha=0`. In particular the archived `alpha=1` table is excluded. Excluding every positive alpha in this exact family is justified by the three exact perfect correlations; even very small alpha cannot be rescued by observing that its CHSH value may be below `2 sqrt(2)`. The report makes no tolerance, approximate-correlation, infinite-dimensional, or broader physical impossibility claim.

### Endpoint positive control

`rho_0=(|00><00|+|11><11|)/2` is a positive unit-trace bipartite state. Both setting choices on each side may use the same Z measurement. Its four conditional tables have equal bits with probability one and equal-output rows of one half each, realizing `P_0`. A shared fair classical bit gives the same table. This is a substantive within-interface realizability control, properly separated from any claimed derivation of the archived permutation measurement semantics.

### Stored-state countercontrol: equation (7)

The displayed `Omega_alpha` is a diagonal positive operator. Its trace is `(1/4) sum_(x,y) sum_(a,b) P_alpha(a,b|x,y)=1`. The four context values have probability one quarter each, so conditioning its context registers indeed recovers each stated conditional row.

This is a fixed density operator encoding the full supplied table, but its context registers and outcomes are prepared jointly. Reading and conditioning these registers is a different interface from independently chosen local POVMs on one setting-independent AB resource in equation (3). The report therefore correctly rejects the overstatement that no density-matrix encoding is possible, while declining to treat an answer-bearing encoding as native acquisition.

### Joint-context sampler countercontrol: equation (8)

Let lambda be a fair bit independent of the Bernoulli-alpha bit c. For `xy=0`, both outputs equal lambda. For `xy=1`, c selects equality or inequality with probabilities `1-alpha` and alpha. Fair lambda splits each of those possibilities equally between its two output pairs. This reproduces exactly equation (1), with uniform single-output marginals.

The procedure explicitly receives both contexts, and supplies its processing rule and randomness. It is a valid realization outside equation (3), not a Bell-local response rule or an inherited native mechanism. No separated implementation, communication cost, or native randomness law is inferred. Together with the stored-state control it prevents a blanket quantum-process or physical impossibility interpretation.

### Local versus paired readout

Every one-shot single-output distribution is uniform for all alpha and independent of the other setting. A receiver restricted to its own output and fixed own setting therefore has no alpha-dependent one-shot law. This conclusion does not constrain unmodeled memory, setting-correlated preparations, or repeated-use channel behavior; the report explicitly avoids those extrapolations.

At context `(1,1)`, the paired parity is Bernoulli-alpha. At alpha zero and one its supports are disjoint, so one actually available paired parity record would distinguish the endpoint tables perfectly. The report correctly conditions that statement on justified pairing, context association, common reference, capture and retention. The existence of a probability table in a verifier file does not deliver such a record to a native receiver.

## Source-function and historical-scope review

The operational implementation claims are supported by inspected bodies, not merely file names:

- `enumerate_raw_candidates` returns a deep copy of three literal records. The carrier, permutation data and operational table are supplied separately.
- `check_admissibility` checks the schema, allowed metadata, carrier/permutation structure, table domain, rational nonnegative entries and row normalization. It does not compute probabilities from operations or enforce a quantum-state realization.
- `evaluate_witness` validates and scores the given table using the registered CHSH convention. It consumes no outcome stream.
- `reduce_to_retained` returns literal four-object diamond data without inspecting the candidate. Operational probabilities, identity and carrier size are deliberately omitted.
- The verifier's `_parse`, `_score` and `_retained` implement separate parsing, CHSH scoring and the same constant retained skeleton. They are independent semantic code for their declared checks, not independent physical probability producers.
- `nonclassicality_search.py` does call comparator and structural-equivalence routines, compares retained outputs, and assembles the producer verdict. The review does not infer the complete original certification from those calls alone or recertify uninspected implementation details.
- v15.55 `derive_defect` parses `operational_table`, computes absolute CHSH, subtracts its frozen bound two and clips at zero. It does not reconstruct D from retained diamond fields or consume a native event stream.

The frozen v15.54 design expressly limits its positive verdict to the operational family, registered retained reduction, target distinction and comparator class. It explicitly warns that witness probabilities are not automatically retained observables and disclaims a physical source law and derivation of quantum mechanics. The reviewed report preserves those limits. S=4 is also a valid ordinary Bell-local obstruction by the binary CHSH inequality; it does not exclude arbitrary classical joint processors or arbitrary hidden-variable theories.

The v15.55 archived result states RESPONSE_NONUNIQUE with four rational surviving parameters. Its response-space code gives seven linear coordinates with the three independent branch-swap equalities, leaving four coefficients; its naturality/composition source asserts no additional rank in the frozen scope. The report leaves that classification and its historical assumptions intact, selects none of its coefficients, and does not infer that nonuniqueness prevents every common accessible consequence.

The previous event-origin follow-up did inspect the v15.54 README and identify its source-correspondence limitation. The present report materially extends that bounded screen by tracing the literal producer table, the separate verifier parsing/scoring, the candidate-independent retained reduction, and the v15.55 defect implementation, then applying the exact direct-quantum-state representation test. The old README conclusion, the mutation-control dependence and the familiar PR distinction are explicitly acknowledged as prior information. The added work is a concrete source/interface assessment, not mathematical novelty or a newly discovered interaction.

The partial-complement report is correctly described as conditional on actual quantum output states, an RQ factorization and available measurements. Its q^2 bound does not establish these upstream prerequisites or realize a table that fails the particular quantum-state interface. Neither the new exclusion nor the partial-complement premise gaps withdraw conditional RAS/RCR, source binding/grade, record-compatible order or the inherited response results.

## Primary mathematical context checked

I opened the two cited primary papers. Popescu and Rohrlich, [arXiv:quant-ph/9709026](https://arxiv.org/abs/quant-ph/9709026), section II of the PDF, distinguishes the quantum CHSH bound `2 sqrt(2)` from nonsignaling correlations attaining four. Plavala and Ziman, [arXiv:1708.07425v2](https://arxiv.org/html/1708.07425v2), sections 2, 4 and 6, gives the binary PR table, separates shared-state measurements from process observables, and constructs a measure-and-prepare process producing its correlations. These support the report's prior-art and narrow-interface statements. The self-contained proof and controls above establish the actual reviewed exclusion without relying on an unproved general citation. No paper's process is adopted as native dynamics.

## Findings and final assessment

Critical findings: none.

Important findings: none.

Minor findings: none requiring correction.

**ACCEPTED for the exact four inputs bound above.** The direct representation exclusion is precisely bounded and supported. The report advances beyond the prior README-only source screen while identifying repeated controls and established mathematics as such. `INDEX_APPEND.md` accurately compresses the argument, source-provenance finding, controls and unchanged native status.

Acceptance does not certify a native source-to-receiver mechanism, numerical evidence, publication, historical stack replay, archive-wide absence, a main merge, or numbered-stage closure. No scientific source module was imported or executed during this review. Verification consisted of text inspection, analytical reasoning, source-identity hashing, and reading primary mathematical context. No enumeration, simulation, numerical experiment, historical test replay, author-file edit or newly counted scientific test occurred.
