# V1699.14 analytical review publication receipt

Account: proteinfolding-gpt. Date: 2026-10-17 UTC.

## Immutable chain
- Inspected baseline: f49c5d5fb29bb4113803de3f0d9237bd1ca8ab3f.
- Frozen RESULT/FREEZE/source packet and original ZIP copies: 8d9184fd0d8416cbb998837fc1684bbfd5c0ea4c, direct child of baseline. All scientific findings were already known and disclosed as exploratory.
- Review source and workflow: 7ccec8087a377b1a7e9e7c3761555b14cb53c572, direct child of freeze; only pipeline scripts, pinned workflow and source lock added. Both commits have proteinfolding-gpt author and committer.
- [Actions run 39022779177](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/39022779177), attempt 1: completed/success. Jobs integrity 117367739272, argument-review 117367768630 and publication-audit 117367906073 all completed/success.

## Review and evidence
Requested and returned model: gemini-3.1-pro-preview. One model-availability GET and one generation request; no model fallback or repeated verdict request. ACCEPTED, with empty findings/missing_assumptions/counterexamples and four limitations. Raw response SHA-256: 73ec35612d883f385e1dbf943a8effb3069cb679061f41430f3265ca51100cc6. Exact prompt SHA-256: 2c938623ae2588ec389b307297d2736ed07aedb83e3057a77bd1bd8a091eff09.

Original ZIPs are preserved under evidence/run_39022779177_attempt_1/artifacts/:
- v1699-integrity-1.zip: artifact12097492160, 3994 bytes, SHA-256 1d98a9242dabd26da7a26be5b88a6c1f74bfa8c99fad19f34f467c518f38bf90.
- v1699-review-1.zip: artifact12097436556, 55310 bytes, SHA-256 7f328ce8afed2780dd286380e8240747e73bc834bb2d410a1fd76824dd5d87ab.
- v1699-publication-1.zip: artifact12097442682, 4816 bytes, SHA-256 9b208f0a084e1ef9489b47801630baf08dec517b9ecc84a1b1c07ad309fda9b8.

Downloaded byte counts and SHA-256 values equal GitHub artifact metadata and complete upload logs; ZIP CRC checks passed. Exact extracted outputs are preserved alongside originals, including model metadata, request, full prompt/raw response, parsed verdict, source/input manifests, and independent remote readback. Three complete decoded job logs and run/jobs/artifact metadata are retained. REST commit metadata omits per-file patch fields; immutable file identities are preserved. EVIDENCE_MANIFEST.json binds every retained evidence file by length, SHA-256 and Git blob identity.

Actions source-publication verification independently fetched current inputs, six earlier frozen objects and five original baseline objects: 23 exact file readbacks. It reconstructed original ZIP members and the response/verdict relation without importing producer/review helpers. It verified GPT author/committer and source/workflow/run/attempt identities. This gate precedes durable evidence publication; the separate durable-publication audit is pending and will be recorded separately.

## Scope
No native milestone, scientific enumeration or numerical result is claimed. The 35 executable tests are evidence-plumbing checks only. No archived scientific module was imported/executed. No failed Actions attempt exists for this checkpoint. Full inherited numerical-stack and post-merge requirements are not claimed met; no main merge or numbered CLOSED/CERTIFIED stage. Native interaction and broad C3/C4-C6 remain OPEN. Reopening this C route requires changed evidence at its explicit missing premise.
