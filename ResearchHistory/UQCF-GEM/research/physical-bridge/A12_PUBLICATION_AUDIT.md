# A12.1-A12.5 repository publication and evidence audit

Date: 2026-10-06 UTC.
Attribution: ChatGPT author-side reporting/source audit, separate in purpose from the mathematical argument audit; NOT independent peer review.
Status: SOURCE/EVIDENCE/REPORTING AUDIT SATISFIED FOR THE RETAINED R1 CLAIMS. Final integrated readback and reconciled closeout publication follow this record.

## 1. Authority, source and scope

The self-contained process amendment is 62b6bec4bea5e6446680aec5694fbd0d8f096165. The prospectively frozen verification protocol is 291425d273412a65e98facc79bc368616200d7a1, file A12_SELF_CONTAINED_AUDIT_PROTOCOL.md, blob db1e349268f7b864219bf37d1f5917abbc3e1fef. The five-label clarification for the original upper-bound controls was published before execution. No primary-universe or resource-budget change was made.

The final mathematical/implementation source is b2085eb1fdca0bbe754743e6bd74ef6fda6bdbef, tree ce3ca529f4d84434632b5e10d0ed4e93f88b1cd9. Its R1 consolidated proof is A12_CONSOLIDATED_PROOF_AND_AUDIT.md, blob f670e9a6687aec49b18429655285f937404e1a36, SHA-256 82dba56d65f80dcb53c010ced48c3dfb4880ebb6e523975672b656b18bbe74ad.

The mathematical source, reference calculation and certificate implementation are not being altered by this evidence/reporting publication. A future mathematical change would need a newly frozen candidate and affected checks, not silent reuse of this run.

## 2. Mathematical/reporting reconciliation

The complete written arguments and dependency ledger are Sections 1-7 of the R1 consolidated source. This audit checks how those conclusions are reported, rather than treating the computational status as a proof.

| Result | Retained conclusion and reporting restriction | Evidence reconciliation |
| --- | --- | --- |
| A12.1 | Four signed one-update response quadrants, original floor effects, cross-root qualification, relabeling covariance and S/F/Q/M invariance. First move must be legal; candidate must change a different incidence and retain syntax. | All four original strict controls have exact direct tau values; bounded response and covariance checks pass. Floor legality is not silently removed from the candidate set. |
| A12.2 | General-n irreducible candidate-response family; listed construction has n+3 roots. Empty coefficient is 1, nonempty proper coefficients 0, full coefficient -1. No fixed finite-order truncation is exact uniformly over growing root count. | All n=2,...,8 cubes, 508 subsets and 1,792 intervention edges pass. The broader full-labelled-response-graph descriptor impossibility claim is withdrawn as unproved, not declared false. |
| A12.3 | Exact W/C incidence updates, coordinate counts, protected-band decomposition, bounds and covariance with explicit palette/root/floor conventions. | The p=1 vacuous-pair counterexample remains recorded. Complete declared-domain and diagnostic update comparisons pass. No conserved scalar is asserted. |
| A12.4 | Addition A>=2 iff; deletion D>=1 plus original floor iff. The particular global pair (mu_-,N4) is insufficient, even holding candidate identity fixed in the supplied controls. | Both fixed-candidate comparisons pass. Same-root shadow changes are explicit; A can increase from 2 to infinity under an addition while legality stays unchanged. No all-scalar-encoding, minimality, observability or scalar-monotonicity theorem is claimed. |
| A12.5 | No exact legality rule restricted to the supplied overlap component and matched side information, over the stated protected class. | The original six-root L and I fixtures are restored exactly; source-fidelity test passes; direct tau values are (3,3,3,2) for (L,I,gL,gI), with both bounds in the proof. This is not an impossibility for all locality notions. |

R1 source correction is material to traceability: the earlier consolidation at 5541843b2539cd714796d2e9c94d05741b2a49d8 had substituted several A12.5 supports while saying it reproduced the originals. The RED source-fidelity test rejected that transcription. R1 restores original L=({d},{a,c},{c,e},{a},{a,c,e},{a,b}) and I=({d},{a,b,e},{a,b,e},{a,c,e},{b},{c}). The original proof/scope bytes were never changed. The common-palette and original witness arguments apply to these exact restored inputs.

The original ten documents retain historical candidate-status language. The source registry and consolidated R1 result control current claims; original statements are not retroactively rewritten. The implementation ledger's 'not yet completed' sentence is explicitly a freeze-time checkpoint, not the terminal run state recorded here. The workflow's contract-step name still contains 'RED until implementation'; actual test output and terminal step conclusion determine its result.

## 3. Executed bounded evidence

[Successful run 37502203890](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/37502203890), attempt 1, job 112401765007, executed source b2085eb1fdca0bbe754743e6bd74ef6fda6bdbef. The terminal run and job were read back as completed/success, with all required stages successful. Full decoded platform logs and repository-published command logs were inspected.

The unchanged contract suite passed all 10 tests. Eleven deliberately bad records/claims were rejected before full execution. Each of the nine primary blocks additionally rejected removal of a valid identity and insertion of a duplicate. The exit-23 logging-pipeline regression passed.

Complete primary domain: every ordered support/floor state at p=2,3,4 and m=1,2,3, totaling 35,792 identities. Exact set equality with the separately constructed reference universe and no duplicates were required. Of these identities, only 102 are protected-band states: 6 at p=3,m=3 and 96 at p=4,m=3. Do not describe 35,792 as a protected-state count. The primary domain has no 4-to-5 upper-band exit; the separately declared higher-root fixtures cover that boundary without creating a larger exhaustive-domain claim.

There were 33 fixture-state evaluations in addition to the primary domain, plus the separate 508-subset collective campaign. Counts that combine primary and fixture evaluations include 419,037 syntactic toggle comparisons, 2,464,007 W-coordinate update comparisons, 6,572,906 C-coordinate update comparisons and 8,940 ordered response comparisons. These are different obligation counts, not independent theorem counts or a larger number of primary states. The full JSON retains all counters and finite collective coefficient arrays.

Primary and fresh-process reproduction used the SAME source commit with PYTHONHASHSEED 0 and 1 respectively. Their 10,057-byte scientific JSON files are byte-identical in the runner and resolve to the same published Git blob 4e4431c56d11348fc5f0833b3b341319861f2470. Scientific-file SHA-256 is e0ef0a032d2070057e7feb573872bf24a09686a9dd012f1114952ee37ec37b57. The separate deterministic check-stream digest is 650851cf5ad2f91ef2be7c60bd549039aa5e9daee79f9a6eedff21c003a9ea3c; these two digests describe different objects and must not be interchanged.

Direct reference tau is obtained from actual set-intersection transversal enumeration, not W/C/A/D. The certificate route uses incidence formulas. Both were authored in this workflow and share the documented integer-mask input representation; that is separately specified calculation, not independent human/model authorship. Pure support caching does not remove floor identities. General-n and other unrestricted mathematical conclusions rely on the written proofs, not finite PASS.

## 4. Preserved failures and actual fixes

| Run/attempt | Input source | Actual disposition | Original durable evidence |
| --- | --- | --- | --- |
| 37500570046/1 | 4928457ebe247382a714584a478fe057ddbad5d8 | RED: 9 failed contracts, 1 preservation pass. A missing pipefail setting masked pipeline exit statuses; final missing-output check failed the job. No primary verifier existed, so nominal downstream step successes are NOT scientific successes. | c008c2679ce4c0f6747ca10ec0279a754c551820 |
| 37500792495/1 | 8be884e9793e5ba69f456f61a434f6f086d75ad5 | Repaired RED: pipeline control passes, the same 9 contracts fail, subsequent scientific stages correctly skipped. | 89f956ff96e514092000b785faac1c7414f5f3d3 |
| 37502203890/1 | b2085eb1fdca0bbe754743e6bd74ef6fda6bdbef | GREEN: 10 contracts, rejecting controls, full bounded run, fresh-process reproduction, byte comparison and durable publication all pass. | 90ef3d6daa0b09b1b8de0ee28403bb396db98931 |

The failures remain separate unchanged evidence trees, not overwritten by the later pass. Explicit Bash -eo pipefail and a real nonzero-exit regression repair the failure propagation. No mathematical failure was discarded to obtain GREEN.

## 5. Publication, source preservation and resources

All three original evidence subtrees are integrated by their EXISTING Git tree identities, rather than retyping or regenerating their contents. A12_EVIDENCE_MANIFEST.json records the original commits, subtree IDs, successful file blobs/sizes and source identities. The green subtree has 12 files totaling 34,357 bytes, below the 2 MiB frozen text-evidence budget. Primary and reproduction took about 24 seconds each in the platform logs; the run was created at 17:15:59Z and last updated terminally at 17:17:05Z, comfortably within the limits. These are observed run resource facts, not a standalone efficiency benchmark.

Environment: Ubuntu 22.04.5, CPython 3.11.16, Linux x86_64/glibc 2.35; exact versions and source SHA-256 map are in context.json. Nonblocking platform warnings concern Node 20 action declarations forced to Node 24 and deprecated Node APIs; no Python verification warning or test failure occurred in GREEN. No third-party scientific input or outside-AI service was used.

The runtime context's source SHA-256 map is preserved unchanged. The contract suite checked all ten frozen A12 source blob identities, the protocol and original review archive. Git comparison from 89aeab82272f163c0e3045e05c6224c4c81e34a8 to the implementation source lists only the new workflow, verifier/ledger files and disclosed consolidated-source correction. No certified v16.54/v16.55 or accepted A11 file changed. The approved isolated dependency boundary imports no historical certified engine, so no whole-history replay or recertification is claimed.

The green evidence commit is one evidence-only child of b2085eb; its compare lists precisely the 12 evidence files. Repository readback confirms primary/reproduction blob equality. jobs_snapshot.json was captured before job termination, and is NOT the terminal success record; the later live run/job reads and full logs establish terminal success. Raw outputs still say OPEN_PENDING_REPORTING_AUDIT because that was their correct execution-time status. They must not be edited to say CLOSED after this audit.

Artifact 11430296564 is the provider's secondary ZIP copy, 11,210 bytes, with platform-reported SHA-256 aeb5c6f282c3adfc39c0f641c25934f48646c6707c8fd62029a9fed27f052585. This audit uses the durable repository member files as primary evidence and does not claim independent reconstruction of the provider's ZIP bytes. Whole-output digests supplement replayable enumeration; raw per-state output is not retained or implied.

## 6. Historical external review and exit condition

The external review at c120223a4ea7eaa9a383de9ab7109826ca5b5cd9 remains unchanged with its original verdicts. Its missing job_id and null sources provenance qualification remain documented in the amended governance file. No external verdict is repurposed as approval of R1, and no old remote job is polled or claimed cancelled.

No unresolved obligation remains in this audit's retained proof, declared finite verification or reporting scope. Before issue #104 is resolved, read the integrated evidence tree and this audit back at the publication commit, then publish one reconciled A12.1-A12.5 closeout/status record and read that back as well. This is a self-contained repository closeout, not independent peer review, proof-assistant certification, numbered v16 certification or physical validation. No A12.6 or physical extension is authorized by this audit.
