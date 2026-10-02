# Independent actual-merge receipt decision — v16.53

**Decision: APPROVE CLOSED/CERTIFIED for actual merge `f6d4d792aa6ec1d7c058eeb21fa3a4de267dacb8`, conditional only on publishing this exact decision on the separate audit branch, reading back its exact bytes, and rechecking terminal workflow success before reporting closure.**

Reviewer: independent assistant `/root/v1653_receipt_review`, 2026-10-02. Scope: EXECUTION_PLAN Task4 final receipt gate. This is a read-only provenance, recorded-execution and durable-evidence audit, not a repeated proof or whole-source review. No scientific module was imported or executed locally, no scientific source was edited, and no review was delegated.

## Findings

- Critical: none.
- Important: none outstanding.
- Minor: none outstanding.

The prior exact-head review's standalone initial-preflight retention gap remains closed. The corresponding actual-merge standalone preflight is also retained separately and independently verified below.

## Independently verified evidence

1. **Actual merge identity.** Fresh raw GitHub API reads confirm PR101 is merged as `f6d4d792aa6ec1d7c058eeb21fa3a4de267dacb8`, with reviewed publication head `e84643fdb667e28c41018a56c3422f4b90ef5160`. The merge's ordered parents are `b6bf95798ec5892963c29f4020f8b75069fd2e3b`, then that exact publication head. Both merge and publication point to tree `2063d52a660a85b5a1675424d5d974b7038dad90`.

2. **Terminal GitHub execution.** Fresh run and jobs APIs show actual-merge run `36946472173`, attempt 1, completed/success at the actual merge, triggered by push to `research/v16.34-fiber-component-invariant`, using `.github/workflows/v16.53-four-child-boundary.yml`. Preflight job `110649635261`, post_merge job `110650288469` and receipt job `110653498695` are completed/success. Source-only science/publication jobs are skipped as expected for this push route. Integrated CI `36946472199` and artifact-transport run `36947746113` are also completed/success. Receipt-captured run metadata predates terminal completion; these independent live API reads resolve that timing limitation.

3. **Original execution archives.** Independently rehashed and CRC-checked the complete original actual-merge ZIP and original receipt ZIP; checked duplicate-free, path-safe membership and every extracted byte against the original ZIP member. Both digests and byte lengths match fresh raw GitHub artifact records:

   | Artifact | ID | Bytes | SHA256 |
   | --- | --- | ---: | --- |
   | Actual merge | `11202962182` | 114011394 | `1830143fd012ee2d619d2c7371df7f44a76e51b0855691da26c71c745122cf80` |
   | Receipt | `11203290048` | 228054516 | `8d1de8f57a944e755607f1cf146cbffdbb2b311591e657bd6d79a11a36e1db35` |

4. **Recorded full-stack results and source binding.** Inspected the byte/AST/log audit helper and reran it with extraction replaced by exact original-member comparisons. All 132 actual-merge manifest entries pass. The 2049 source paths bind through SHA256 source objects to the reviewed Git blobs, including inherited source, accepted proof/protocol, plan, workflow and test manifests. The recorded GitHub logs and source/assertion bindings pass for 1150 inherited checks plus 43 current controls, 1193 total, including retained intended RED signatures. This is verification of GitHub execution evidence, not local numerical execution.

5. **Deterministic scientific equality.** Independently compared all 45 scientific files across primary science, separate fresh reproduction and actual merge: every byte is identical. The 42 inherited scientific files also match integrated-baseline Git blobs. Recorded verifier output is VERIFIED with 2863 records and 34234 moves; the certificate and verifier record identities agree. Nonunit witness remains NOT_CLAIMED.

6. **Durable receipt.** Fresh immutable commit API confirms receipt commit `e85be3d4fd318bb577a101f0fdbeed9251dd9ebc`, on the separate `research/v16.53-audit-receipt` branch, has the actual merge as its sole parent and tree `12f6878e0ea8d7452d43e3d4394e3317a18637f7`. Independently fetched its complete untruncated recursive tree and checked all 8677 blob entries against the supplied map. The receipt directory `ResearchHistory/UQCF-GEM/audits/v16.53/f6d4d792aa6ec1d7c058eeb21fa3a4de267dacb8/` contains exactly 149 expected regular files: 148 manifest entries plus MANIFEST.json. Every retained byte and Git blob binding passes; all published source/evidence blob identities remain unchanged. Direct immutable readback of MANIFEST.json exactly matches the audited bytes, SHA256 `a0dcc7b4d7c8108528f7a6d45854587dcdb40ad5c90657ebd57edf1e44e8b201`. Verified chunks reconstruct the complete original actual-merge API ZIP exactly. Retained source archives/manifests equal the primary source snapshots, and retained execution files equal the audited actual-merge package. RECEIPT.json consistently records VERIFIED_ACTUAL_MERGE, the correct merge/run/attempt/PR and scientific equality.

7. **Standalone preflight supplements.** At immutable audit commit `b2241b272847f1ac4ee62a7be5142119a494b0f4`, directory `ResearchHistory/UQCF-GEM/audits/v16.53/premerge-e84643f/`, independently fetched and exactly compared the full encoded originals. INITIAL_PREFLIGHT.zip.b64 decodes to 122044 bytes, SHA256 `d8e776547ea14127afa283385426fc826318a4de95037a7f4be0f276c60c4f22`; this is the original source-run artifact previously retained at `f4361758285e2ae44afdf44cd1c66351744d2b62` and approved by the exact-head reviewer. MERGE_INITIAL_PREFLIGHT.zip.b64 decodes to 122052 bytes, SHA256 `2aba3e6022b49b64a0054cc61ebd9e6a21ec6548a7544ca7ce033848a03d4ec6`, with 59 CRC-valid members. Its immutable MERGE_INITIAL_PREFLIGHT_API.json exactly equals the fresh raw run-artifacts API record for artifact `11202860824` at the actual merge. The separate supplemental location is part of the final durable evidence record.

## Scope and final publication step

This decision accepts the actual-merge implementation, provenance and receipt gates for the exact identities above. It relies on the separately completed independent analytical and whole-source reviews for the reusable arity 2/3/4 theorem. Finite corpus and mechanism checks validate the implementation; they do not replace the proof, establish arity>=5, imply a physical interpretation, or turn expected unsafe-transport failures into a nonunit witness.

No scientific or archival finding remains open. The executor must now publish this exact decision on the separate audit branch, read back exact bytes and recheck terminal success of run 36946472173 before reporting CLOSED/CERTIFIED. That final recording step necessarily follows authorship of this decision and is the only remaining condition of this approval.
