# Native owner correspondence verification implementation plan

> For agentic workers: execute this bounded plan inline under Aaron's existing research and review authorization. Use the executing-plans workflow. No new mechanism or thermal-bath test is authorized by this plan.

**Goal:** independently verify the existing T-277 argument and preserve its complete review trail.
**Architecture:** frozen argument/source packet; algorithmically independent producer and verifier; inherited FCV stack; one Gemini whole-argument review; fresh replay and durable archive.
**Tech stack:** Python 3.11, sympy 1.13.3 and mpmath 1.3.0 for the unchanged inherited stack, GitHub Actions.
**Spec:** ANALYTICAL_BOUNDARY.md at 20fedca0242791266e9851c1dc6cb4591888be15.

## Prospective contract and disclosed knowledge

The analytical result and three-vertex witness were already derived and published in T-277. Expected result: both P-report and S-report completions satisfy the stated weak consistency conditions, and only P preserves calibration and delivers the declared witness. This is prospective verification of a known analytical claim, not a preregistered discovery. No new scientific program or physical postulate is introduced.

Freeze all source/script/workflow bytes before execution. Record the argument SHA, reference SHA 750554de424a1e12e2d14c6665920bda31163dfc, execution/workflow SHA, run ID, attempt and model. Never edit the frozen argument to obtain acceptance.

## Fixed universe and evidence obligations

- All canonical plane rooted prefix trees of sizes 1 through 5 (children indexed consecutively in each full tree), all nonempty root-containing prefix-closed retained subsets, and all nested triples X >= Y >= Z. Retained subsets preserve ORIGINAL addresses; no renumbering.
- Producer enumerates ordered rooted trees by recursive ordered forests and constructs P by repeatedly removing the final token until a retained ancestor is reached.
- Independent checker enumerates Dyck words and reconstructs trees by stack traversal; constructs the expected action on each atom by ancestor comparisons. It imports no producer decision code.
- Certificate contains every (X,Y) identity and complete P/S integer matrices, plus the fixed receiver witness and provenance. Exact identity equality, not count-only or supplied-record validation, is required.
- Check identity, composition of P/S across every nested triple, retained-relabel covariance under a fixed injective token renaming and reversed storage, leaf locality, initial and final receiver values, native totals, and calibration graph preservation. Matrix identities establish all-input linear-map equality; numerical grade sampling is not called a general proof.
- Controls: empty universe; missing, duplicate, substituted and invalid carrier records; wrong P value; wrong S value; false source revision; false receiver witness. Each must be rejected and the genuine failures preserved.
- Full unchanged inherited FCV tests, parent tests, historical tests/reproduction, producer, independent verifier and their rejecting controls run on GitHub. Fresh publication replay must reproduce deterministic new and inherited certificate bytes.
- One Gemini request after verification, using exact whole argument and source definitions. Ask for strongest positive reconstruction, counterexamples, circular assumptions, input/output type checks and whether the result is only a restatement. Return ACCEPTED/REVISE/FAIL with findings and limitations. No retries for a more favorable verdict.
- A syntactically valid adverse verdict is preserved and adjudicated, not silently converted into acceptance. Review completion and scientific acceptance are separate.
- Preserve raw prompt/request/response, model metadata, source snapshots, outputs, logs, artifact ZIPs, API digests, member hashes and immutable readback. Secrets remain in Actions secrets.
- No default-branch merge; PR133 stays draft pending adjudication. No physical claimStatus change, no CLOSED/CERTIFIED claim.

## Implementation tasks

- [ ] Write the independent certificate checker and rejecting-control definitions first.
- [ ] Implement producer with a separate tree-generation and atom-action algorithm.
- [ ] Add source freeze/integrity checks and the inherited-stack runner.
- [ ] Configure verification -> Gemini review -> replay -> durable archive, with one model call.
- [ ] Execute the declared RED/positive controls and all inherited checks on GitHub.
- [ ] Read the raw Gemini response; reconstruct each substantive finding against the frozen proof.
- [ ] Complete publication byte comparisons, download/archive integrity, final readback, and bot-thread report.

## Review focus

1. Report b is an extra interpretation, not inherited extensive grade: never promote it.
2. Exact core non-entailment is not archive-wide insufficiency or physical realizability.
3. Initial receiver blindness is relative to the explicitly fixed b_a interface.
4. No theorem under arbitrary mixed linear morphisms is claimed.
5. P/S composition alone does not prove their physical applicability.
6. Full owner-state correspondence is stronger than the weaker receiver-effect target.
7. Existing T-242 full-owner exclusion is prior work and must not be rediscovered.

## Stop conditions

Failure of integrity, checker, rejecting controls or inherited verification prevents Gemini.
An incomplete model request is not retried automatically. Preserve its evidence and report the failure.
A substantive mathematical error is recorded and corrected only in a separately identified revision.
An accepted scoped theorem still does not derive native receiver delivery.
