# PR148 pre-execution plumbing review

Date: 2026-11-13. Scope: static comparison of `prepared_charge_work/package` with the PR147 baseline in `charge_selection_work/package`. No package files were edited. No API/model call, source-module import, scientific computation, or scientific execution was performed. The root agent is responsible for running the existing plumbing tests and for subsequent execution decisions.

## Disposition

**No newly introduced plumbing blocker found.** The controller, tests, and workflow retain the earlier behavior after the specified changes to paths, source locks/document IDs, prompt, and labels. The static findings support continuing the existing review process within its authorized scope; they are not scientific acceptance or native certification. The two inherited manual acceptance gates below remain mandatory.

## Verified comparison and source locks

- Controller AST is identical after excluding `REL`, `PACKET_SHA256`, `IDS`, and `HEADER`, and normalizing the success-message label. No other control-flow or executable behavior changed.
- Test AST is identical after module/path renaming. There are eight existing test methods; this reviewer inspected but did not run them.
- Workflow text is identical after normalizing the title and `charge-selection` / `charge_selection` names and paths.
- Both reused helpers are byte-identical to the PR147 package. Their Git-blob locks remain `50b1043cda14b18b962f7930cf6a4391067a2a96` and `4c8029da503ed57f404e4424ecc243eb3c609347`; these are checked before import.
- The 74,841-byte source packet has SHA-256 `c01874b23c99c53f98aa3398d20ba7c84fa096c573f7d3afe63d71e3e5828c41`, exactly matching the controller lock. It contains seven ordered documents and two helpers. Every document's embedded UTF-8 bytes and every local helper match the declared byte count, SHA-256, and Git-blob hash.
- The new argument matches the local `ARGUMENT.md`. The previous argument and adjudication match the PR147 package files. The four older contextual document records are unchanged from the PR147 packet.

| Record | Immutable ref | Git blob |
|---|---|---|
| `argument` | `45ffd6da8cace7e70a3ed56e99cc7105308b030e` | `19745d887370870ae6cc138b3e441a845361f902` |
| `previous_note` | `70b14bf9303a42da831a22ef22f1473f5d4a396d` | `b2f47d735e30c7ee8ffd5fc1bf859269626fd4d3` |
| `previous_adjudication` | `70b14bf9303a42da831a22ef22f1473f5d4a396d` | `50ac9b00f8a179c81dd3ea1ed319f09d330b4559` |
| `old_attempt` | `2ab565c3f5bf10305a96ddeef30901de49959ba5` | `460adf6765933130ca718e850992cdce92320ae7` |
| `old_response` | `2ab565c3f5bf10305a96ddeef30901de49959ba5` | `e26e6a39a1b33e74c896141694d4453d3cd9f49b` |
| `location` | `2ab565c3f5bf10305a96ddeef30901de49959ba5` | `4182ba347f8c11bad63315ffa6395c496ddfa498` |
| `owner_directive` | `2ab565c3f5bf10305a96ddeef30901de49959ba5` | `d191e8c4ba97176875a0b9cce3db8e69e6603311` |
| Integrity helper | `2ab565c3f5bf10305a96ddeef30901de49959ba5` | `50b1043cda14b18b962f7930cf6a4391067a2a96` |
| Review helper | `2ab565c3f5bf10305a96ddeef30901de49959ba5` | `4c8029da503ed57f404e4424ecc243eb3c609347` |

Remote existence and bytes were deliberately not re-fetched by this static review. Both execution modes re-fetch all nine records at their immutable refs and reject a hash/identity mismatch before proceeding (`uqcf_prepared_charge_domain_review.py:30-60,117`).

## Execution controls retained

- The sole trigger is a push on `gpt/prepared-charge-domain-20261113` changing `.github/workflows/uqcf-prepared-charge-domain-review.yml`. There is no PR, scheduled, or manual-dispatch trigger. Script/packet-only pushes do not themselves trigger this workflow.
- Review job execution requires `github.run_attempt == 1`; the controller independently requires `GITHUB_RUN_ATTEMPT == '1'` before source retrieval. A workflow rerun cannot regenerate. A distinct future push changing the workflow would be a new run and must remain within the one-review authorization.
- The only generation path calls the unchanged helper once. It performs one exact-model metadata GET, followed by one POST to `gemini-3.1-pro-preview:generateContent`; there is no retry loop, fallback model, or second generation. Request settings remain temperature 0, 32,768 maximum output tokens, JSON response.
- The separate publication job downloads the first-attempt review artifact and calls publication mode. It receives only the GitHub read token, not the model key. Publication does not call the model; it rechecks source bytes, artifact members/hashes, run identity, prompt/request, metadata, raw response, verdict equality, acceptance, and `native_bridge_status == 'NOT_DERIVED'`.
- Checkout uses the triggering SHA with persisted credentials disabled. Workflow permissions remain `contents: read` and `actions: read`. GitHub API requests are reads; the only subprocess in the invoked controller is `git rev-parse HEAD`. There is no commit, push, PR/comment write, or repository-content mutation. Output is confined to workflow evidence directories and artifact uploads.
- Credentials are used only in HTTP headers. Saved request JSON excludes those headers. Error reporting saves exception type/status and verdict only, with fixed sanitized log messages. No inspected code formats a secret into logs or artifacts.
- Source documents are inserted verbatim into the prompt, once per document ID. The prompt targets only the new argument, explicitly limits predecessor material to context, requests independent positive and adversarial reasoning, and retains the distinction between the prepared-vector counterexample and completion corollary. It expressly preserves `NOT_DERIVED` and the new/supplied premises. This is a prompt-scope observation, not a finding that the mathematics is correct.

## Manual gates that must not be dropped

1. **Substantive review:** the raw verdict must contain a meaningful `proof_checks` array and a substantive `next_native_obligation` string. Inspect the actual reasoning against the new frozen claims and preserve every stated limitation. These fields are requested by the prompt but are not validated by `parse_response()` or `audit_review()`. The existing positive fixture omits them and still passes the audit by design. An automated ACCEPTED/PASS alone is insufficient.
2. **Manifest/status/model agreement:** inspect that the archived review manifest has `status == 'ACCEPTED'`, `model_requested == 'gemini-3.1-pro-preview'`, and `model_returned` exactly matches the raw response's `modelVersion`. The parser independently admits the exact requested name or a version-suffixed name; `audit_review()` does not compare its returned model to `manifest.model_returned` and does not check manifest status. Preserve this manual agreement gate before adjudication/publication acceptance. Failed, incomplete, or adverse evidence must remain preserved and must not be converted into acceptance by a rerun.

## Reviewed file identities

| File | SHA-256 |
|---|---|
| `.github/scripts/uqcf_prepared_charge_domain_review.py` | `8526329ca50df51aeea4e7cf9a2ddad98b9542f384e4de2f80314902824002c8` |
| `.github/scripts/uqcf_prepared_charge_domain_tests.py` | `7f75dbcd00ff89fcf1e10c6f81e0a55d35187683d55f6c533096b26a03b04f8d` |
| `.github/workflows/uqcf-prepared-charge-domain-review.yml` | `c22457845b059ddbaff1bc6a8fc86afa26b51d0f9da232658844a636641c7af8` |

Static review is complete for these exact bytes. The root agent reports that all eight existing plumbing tests passed, all eleven function ASTs are unchanged after the log-label normalization, and the frozen files were read back exactly. This reviewer did not rerun those tests. Outstanding post-execution evidence is the frozen model response, separate publication audit, and both manual gates above.
