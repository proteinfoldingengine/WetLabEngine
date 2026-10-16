# Independent infrastructure review

Date: 2026-10-16 UTC. Verdict: **REVISE before acceptance of the publication audit.**

Scope: static review of `uqcf_history_orientation_review.py`, `uqcf_history_orientation_publication.py`, `uqcf-gem-history-orientation.yml`, the reused strict-response functions in `uqcf_analytical_repair_review.py`, and this candidate's CONTRACT/RESULT. No scientific modules, numerical tests, inherited replay, model requests, remote reads or external writes were performed. This is an infrastructure judgment, not a mathematical or physical verdict.

## Required corrections

1. **The publication audit does not independently bind the reviewed prompt to the published argument.** In the publication script, the checks following `m['inputs'] == inputs` verify hashes of the supplied prompt, response and review, but never reconstruct the expected prompt from the final CONTRACT, RESULT, source packet and identity. A self-consistent artifact containing a review of a different prompt passes this portion of the audit. The upstream review script currently builds the intended prompt, so this is a missing independent verification rather than evidence that a wrong prompt was actually used. Factor deterministic prompt construction into a pure shared function, or independently reconstruct it in the publication audit, and require byte equality. Verify the frozen `source_parent`, `contract_commit`, model request and availability identity there too; merely copying these fields into the final readback is not verification.

2. **Artifact completeness is self-declared and the publication parser is weaker than the reviewer gate.** The review job compares integrity files only with their own manifest and does not require the exact expected set or compare the retained `input_manifest.json` with the checkout. The publication audit lists only immediate regular files, so additional nested files are invisible; it never reads `provenance.json` or `model_availability.json`, and omitting those files from both the directory and manifest is accepted. It also uses ordinary JSON parsing and a first-candidate extraction rather than the strict duplicate-key, exactly-one-candidate, model-role and text-only validation already available in the helper. Require exact expected artifact members, recursively reject extras and symlinks, compare the integrity input-manifest bytes, and apply the same strict response/verdict validation independently in publication. Reconcile all identity-bearing records and the availability record. These changes make the claimed complete byte audit fail closed on omissions and substitutions instead of only checking internal hash consistency.

3. **The declared ancestry must be independently checked through the source parent.** The review verifies CONTRACT is an ancestor of the head; publication verifies the head's sole parent is CONTRACT. Neither verifies that CONTRACT's own sole parent is the declared source parent. Reading original blobs at a declared source commit proves path/content membership but does not establish the claimed parent chain. Verify the exact head -> contract -> source-parent chain, preferably before model access and again through the remote commit objects. The current identifiers may in fact have that chain; this static review has not independently established it.

## Required final assembly checks

At review time, `input_manifest.json` and the inherited helper were absent from this local staging directory, which also was not a Git checkout. This is not a claim that the eventual repository lacks them. Before publication, require the completed manifest to contain the exact new source-file set plus the frozen helper and CONTRACT, with no omissions, and independently validate the helper against its original pinned bytes. In particular RESULT, source identities, source packet, both infrastructure scripts and the workflow must be covered. The new source identities and source packet currently contain 19 distinct paths; all content-derived sizes, SHA-256 values and Git blob identities agree with each other. Their equality to Git objects at the parent remains an Actions/remote check, not a locally demonstrated result.

## Positive findings

- Secrets are supplied only to the step that needs them. Gemini credentials are carried in a header, not in the URL or prompt. Transport failures retain only error type and HTTP status; exception strings, response error bodies, request headers and secret values are not printed.
- The workflow uses read-only repository permissions, immutable event-head checkout, disabled persisted checkout credentials, separate prerequisite jobs and same-run artifact downloads. The reviewer checks scientific SHA, workflow SHA, run ID and run attempt before contacting Gemini.
- Review acceptance requires a strict JSON object, a complete single candidate with model-role textual content, a recognized verdict and empty unresolved findings/assumptions/counterexamples. REVISE/FAIL and inconsistent ACCEPTED verdicts fail the job; malformed output is treated as infrastructure failure.
- Source packets are checked against declared original paths and Git blobs; publication fetches the corresponding remote path at the declared original commit before comparing full blob bytes. This avoids accepting a free-floating blob hash as proof of path provenance.
- The prompt distinguishes supplied conditional premises, historical reviews, current corrections and actual native claims. No science module is executed and no numerical count or numbered-stage closure is increased.
- Both new Python files passed AST syntax parsing. The workflow's fetch depth of three is sufficient for the intended exact two-edge ancestry only once that ancestry is established.

## Operational limitations and hardening

The publication checker implements its acceptance checks with Python `assert`; the supplied workflow does not request optimization, but `python -O` or `PYTHONOPTIMIZE` would strip those checks. Explicit rejection conditions, or an initial refusal when `__debug__` is false, avoid this runtime pitfall. The commit-files endpoint is not paginated; the current small publication should fit one page, but the auditor should reject or paginate a paginated response before calling its changed-path list complete. Mutable action version tags are an operational dependency, not an immutable action-source proof.

The contract also requires retention and inspection of original artifact archives and logs. The workflow uploads artifacts for 90 days; it does not itself complete a durable downloaded-archive/log audit. Final acceptance must therefore await the separately authorized archive/log readback and successful corrected remote audit. Neither this review nor an ACCEPTED model response certifies native interaction or mathematical priority.

## Re-review of corrections

The first correction pass added immutable review instructions, exact input and artifact sets, independent prompt reconstruction, identity/availability reconciliation, remote contract ancestry and refusal of optimized Python execution. Re-review identified four remaining details: the retained integrity input manifest still needed direct byte comparison; response/verdict validation needed the helper's full schema; local ancestry checks needed to reject extra merge parents; and recursive membership needed to exclude only the root manifest, not every file with that basename. These findings were communicated before acceptance.

The second correction pass resolves those details. Inspection confirms:

- Both jobs require the exact 11 input paths; those paths cover seven candidate documents and four pipeline/helper files. The source packet and source identities retain 19 matching unique originals.
- Integrity consumption checks the exact recursive file set, rejects symlinks, compares its input manifest with the checkout and verifies each retained source snapshot. Publication independently checks its exact seven accepted-review members plus the root manifest, rejecting nested extra files.
- Publication reconstructs the complete prompt from REVIEW_INSTRUCTIONS, the expected full identity, CONTRACT, RESULT and the full source packet, and requires exact prompt-byte equality.
- Publication independently rejects duplicate JSON keys/nonfinite constants, checks all verdict arrays, requires a complete single model-role candidate, enforces the helper's allowed text-part keys and explicit thought handling, and reconciles raw response, review text, verdict and their hashes.
- Scientific/workflow/run identities, source parent, contract, requested model and availability are checked. Both local and remote ancestry gates require the exact sole-parent chain. Remote original bytes remain path-bound at the source parent.
- Optimized invocation is explicitly rejected. Paginated remote API responses are now rejected rather than silently treated as complete.

Both revised Python files again passed AST syntax parsing. No remote/model execution or numerical science was performed in either review pass.

**Final static verdict: ACCEPTED FOR DOCUMENT-ONLY ACTIONS EXECUTION; no unresolved implementation blocker found within the reviewed scope.** This supersedes the initial REVISE as an infrastructure code-review judgment only. It is not acceptance of an unrun publication audit, ungenerated final manifest, or mathematical argument. The final input manifest must be generated after this report's bytes freeze, checked for the declared 11 members, and bound with the inherited helper and contract in the immutable commit. The actual Actions result, raw review, remote audit, downloaded archives and logs remain execution/readback obligations. The mutable action tags remain an explicitly noted operational dependency.

Reviewed implementation SHA-256 values (this report is excluded to avoid self-reference):

- `.github/scripts/uqcf_history_orientation_review.py`: `d002fe7910bd2c1785cf93c616f7ac5191bc1194fe9a3487fc94fa0fae048dd1`
- `.github/scripts/uqcf_history_orientation_publication.py`: `99c4d9231cab22d12ba480e176b935d80b268ecaad65ef281967c715ed0f125d`
- `.github/workflows/uqcf-gem-history-orientation.yml`: `462acee15216f5fc58717ab59d3dd894a194824bc2c4aaf2f0fcefeb4d1c0c80`
- `ResearchHistory/UQCF-GEM/research/physical-bridge/history_orientation/REVIEW_INSTRUCTIONS.txt`: `710a0931fd3bf15ff8360eb043c24a6475971d71df10cdcec2e7a6a6bf4df945`
