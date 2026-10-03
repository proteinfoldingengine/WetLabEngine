# Engineering decision ledger

Status: PROPOSED / UNEXECUTED. Scientific certified base: 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.

| ID | Evidence / requirement | Decision | Risk and acceptance boundary |
|---|---|---|---|
| A1 | Three completed campaigns, exact workflow/job APIs and execution ledger | Freeze historical timing baseline, all reported attempts/pages and steps | Job spans are not CPU attribution; unknown phases remain null |
| A2 | Workflow inherited needs domains; actual merge inherited spans 798s after slowest domain | Propose inherited needs development alongside complete domain matrix | Seven domain slots may delay a shard; speedup unmeasured |
| A2-cap | Existing domains max-parallel 8 | Domains max 7, inherited max 1, total science max 8 | Must enforce a controller-wide budget, including duplicate deliveries |
| A2-gates | Existing aggregation checks complete target run success; an in-run aggregate cannot check its own run terminal state | Check exact upstream jobset at aggregate readiness; retain final whole-run terminal audit downstream | No circular whole-run success prerequisite; no certification before downstream audit |
| A2-binding | Existing helpers/source and request/source ancestry guards are explicit | Bind immutable workflow/scientific/preregistration/protocol/helper objects before execution | Unknown or mismatched binding refuses work |
| A2-events | Callbacks can duplicate or arrive late | Idempotency key (run_id, attempt, stage), immutable input digest and compare-and-set transition | Same key/different bytes rejects; unknown publication outcome readback before retry |
| A2-failure | Existing scientific runner retains checkpoint and first failure | Preserve FAIL / INCOMPLETE receipts for rejection, timeout, cancellation and transport errors | No assertion retry or incomplete-to-PASS conversion |
| A2-publish | Privileged evidence stage currently creates an isolated evidence branch | Consume artifacts as data only; execute approved pinned helper and enforce allowed prefix and absent-ref lease | No artifact-supplied code, executable hooks, paths or helper substitution |
| A3 | campaign.py independently matches and stores the full universe in each shard | Defer prepared-universe chunking and broader platform work | No phase timing supports benefit estimate; requires separate interface/verification freeze |
| V1 | Later validation needs reviewable success and refusal semantics | Design tiny synthetic end-to-end success and independently corrupted fixture controls | Design only; no fixture/workflow/scientific execution now |

The certified scientific campaign remains complete; A2 is not an extension of its theorem claims. No domain reduction is proposed. No source or workflow changes and no GitHub write occur in this packet. Historical chain evidence is in timing_baseline.json and BASELINE.md; every claimed delay is calculated from cited UTC fields. The 77m57s actual-merge aggregation launch interval has no proven causal attribution.

