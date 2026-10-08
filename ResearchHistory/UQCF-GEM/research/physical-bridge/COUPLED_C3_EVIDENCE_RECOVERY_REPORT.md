# C3 evidence recovery and publisher repair — verified operational report

Date: 2026-10-08.
Disposition: APPROVED OPERATIONAL RECOVERY COMPLETE; FINAL GITHUB WORKFLOW SUCCESS; IMMUTABLE EVIDENCE READBACK VERIFIED.
Scientific disposition unchanged: core-probe theorem remains a candidate without a fresh independent mathematical acceptance. This is not a mathematical closeout or its post-acceptance publication audit.

## 1. Exact execution and source

Repository: proteinfoldingengine/WetLabEngine.
Research branch: research/uqcf-overlapping-guard-exchange.
Starting verified parent: cac8f8888e329e1bdee25f8a6bce39e83f8363b2.
Approved recovery scope: 191196636c0e20cba3c459fcd4f4199747e0ebc2.
Initial tests-first commit: 74e592293e107600f0b30601dc5fe92054ac0990.
Initial publisher: d05614d9a7585db98c2c4bbef49225da200cab78.
Preserved local pre-implementation RED log: d08a49239d9f4ebbfbf74f21ecf4f4db1feb59fd.
Workflow integration: df1960d92fe00eeaf0074743036c3e25c1eeae29.
Readback-regression tests-first commit: 41a706ca9bc8a1ea88c675903851f7a982b766fa.
Final implemented and executed source: bbe0c397b2b380f0aa511b804aefecb9aeac73b1.

Final run: https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/37835621311
Attempt 1; numeric job 113511769089. The complete job and all its steps concluded SUCCESS, including publication and artifact upload. Full job logs were fetched and inspected.

Workflow and checked-out scientific SHA are both bbe0c397b2b380f0aa511b804aefecb9aeac73b1. Workflow .github/workflows/uqcf-a12-self-contained.yml has blob a13af4e5cae5b8988bd6e9caf09c47696a9668ee. Actual execution used CPython 3.11.17 on Ubuntu 22.04.5; local publication tests used Python 3.13.5.

## 2. Historical artifacts recovered in full

Permanent archive branch: research/c3-artifact-recovery-20261008.
Permanent archive commit: 475919b55dc2f27867b98aa87ba6d5ab5e3c5ecf.
Its only parent is df1960d92fe00eeaf0074743036c3e25c1eeae29. The exact comparison shows one new commit containing ONLY twenty added evidence files: the two original ZIPs, all seventeen extracted members, and one manifest. No original source, workflow, or historical evidence file was modified.

Archive directory: ResearchHistory/UQCF-GEM/research/physical-bridge/evidence/c3-artifact-recovery-20261008/.

| Original run / attempt | Original artifact | ZIP bytes | Members | Original scientific SHA |
|---|---:|---:|---:|---|
| 37832509819 / 1 | 11574560540 | 11406 | 5 | 6a4ba75ca3a1ce332e6481e383bfecf6046f31b9 |
| 37832751396 / 1 | 11574595760 | 18798 | 12 | ad42d751f69c6fba7af585e6ba15b00941bc201f |

The original ZIP SHA-256 values are, respectively:

    c2b4645fa1c066b3c606c80f55a112e35d67cef5177edbff8644e8b978344312
    d04fda1889c362d3ed590cf953bf3e42bf9e0625a0bd4f8788589201ad244246

The archive preserves empty logs as actual empty files, not omitted records. Total durable payload including its manifest is 140143 bytes. Artifact metadata and embedded execution context were checked against the pinned run, attempt and source identities. Every original ZIP and member byte was compared locally with the manifest, not merely its displayed count.

Manifest blob: 81b472ec0a31f046b8481c2ea480e76b78aa4e52.
Manifest SHA-256: 456d5321f44c86bca147b3857e00cf4d8ba54e4e98b2fe41a81f33862adcd651.
The independently computed directory trees matched immutable connector readback: first archive directory 4f1080a7d775b91e16e2d5c64573c0b14ef61266, second a74890877622e5a0b6287e8d56a827c971674c5c. The publisher additionally fetched and compared every immutable blob before and after publication. Subsequent executions validate this permanent archive rather than needing the original expiring Actions artifacts.

Both original workflow conclusions remain FAILURE. The first contains the expected pre-implementation C3 failures; the second passed science but failed evidence publication. Recovery does not rewrite either historical outcome.

## 3. Publisher failure diagnosis and correction

The old failure occurred at server acceptance of git push creating an evidence branch. Its workflow-permission-check timeout was not sufficient evidence that token permissions were missing. The approved repair uses the documented Git Database API with the SAME GITHUB_TOKEN and unchanged contents:write/actions:read permissions.

The publisher first seeds an evidence reference at an already-published source commit, then creates a single-parent evidence-only commit and performs a non-force reference update. Exact added-path/blob identity equality and immutable byte readback are checked before and after the update. Unexpected paths, modified existing files, collisions, corrupt data and denied API operations fail closed. Artifact redirects do not receive the GitHub authorization header. No token permission, branch protection, or scientific requirement was weakened.

The first repaired execution, run 37835021712 / job 113509736338 at df1960d92fe00eeaf0074743036c3e25c1eeae29, recovered both historical archives and created new evidence commit e709d469dbb3368957ebe7e43d8a11043d6eddf5. It nevertheless failed its immediate final reference readback. A subsequent connector read resolved that reference to the expected commit. This establishes an immediate-versus-later readback discrepancy; a caching or replication explanation is plausible, but the server's internal cause was not proven. That run remains FAILURE.

The correction adds bounded read-only convergence: at most five reads, with 0.5/1/2/4-second waits only while the exact previous reference is observed. An unrelated reference, denied request, wrong update receipt, or exhausted bound still fails. No writes are retried or forced. Three new tests failed before implementation in actual run 37835473620 / job 113511268860; its exact log remains at evidence commit 373d576853e6086a1976a5b8941b02c8b3893468. The final implementation passes those tests. The final live publisher did not log a required stale-reference retry; the retry messages inside test output are simulated regression cases, not live server observations.

## 4. Final scientific and publication checks

The successful final run passed eleven publication safety contracts and eighteen existing C3/A12 contracts. Tests cover exact ZIP/member preservation, empty files, unsafe/duplicate/missing members, digest and budget errors, evidence-only writes, corrupt immutable readback, reference collision, denied access, bounded stale reads, unrelated references and timeout exhaustion.

The C3 algorithmically separate checker again returned exactly twelve knowledge states and 142 command/outcome edges across the two frozen spectator palettes. It still reports independent_mathematical_review=false. The underlying mathematical source and finite domain were not expanded by this engineering work.

The unchanged A12 bounded baseline passed eleven rejecting controls, 35792 primary identities, 508 family subsets and 33 fixture states. Its scientific check digest remains:

    650851cf5ad2f91ef2be7c60bd549039aa5e9daee79f9a6eedff21c003a9ea3c

Final-run primary.json and reproduction.json were independently compared after downloading the artifact: exact equality, 10057 bytes each, SHA-256:

    16443afd8d79d32a1fc69d4163e40bdae4c671bb6f39b22f44f20941ac0c14d0

This is within-run byte reproduction, not a claim that JSON containing differing implementation_commit metadata has identical bytes across different source commits. This A12 baseline is not the entire inherited v16 stack.

Pinned Actions emitted their existing Node deprecation warnings; a deliberately duplicated ZIP member emits the expected test warning. Those warnings were not hidden or described as failures. No warning-free execution claim is made.

## 5. Final evidence commit and external readback

Final evidence branch: research/a12-evidence-37835621311-1.
Final evidence commit: 3170c217dded032460643043cb41a4587332e861.
Only parent: bbe0c397b2b380f0aa511b804aefecb9aeac73b1.
Exact commit comparison: fourteen added evidence files, no other changes.

The Git evidence contains thirteen execution-output files plus MANIFEST.json. The uploaded artifact contains those same thirteen output files plus publication_receipt.json, which is written AFTER the evidence commit and therefore cannot be a member of that same commit. Both sets and their different fourteenth file were checked explicitly.

Final artifact ID: 11574858263; 20266 ZIP bytes; fourteen members.
Downloaded ZIP SHA-256, matched to the actual upload log:

    f47013acb585289f713bd99759eccf49845bc141aad4a9d4e1bef53125c73e63

The receipt names the exact source, evidence and historical-archive commits listed above and reports PUBLISHED_AND_IMMUTABLE_BYTES_VERIFIED. Local source bytes matched the source hashes in its execution context. Reconstructing the manifest from downloaded output produced exactly the immutable manifest blob 75a63014a5b3b532b484b28c8fd5356f58f08644 and SHA-256 77203aa7996a4932acebc0e2751fcaa5756b4e657ae585213452993044d911ac.

The complete locally reconstructed evidence directory tree is 98e03e82c3fa1015babb6d1424c5d6f433d414e1, exactly matching the directory identity returned by GitHub at commit 3170c217dded032460643043cb41a4587332e861. This checks the entire file set and bytes, not a partial record preview.

Final publisher blob: fb5493761c39e40e4c7941123db1514a889e718b; SHA-256 4676bf8d40d7024689416f2e100bbfbb66568b1cb03bedf11623ee5359776659.
Final test blob: ebabae257d2bbeb2a844726014b81098f01360b2; SHA-256 ac308d3224ef521e8485ccf61e169ede05bc8757484c6985ac6b8a51df8e9834.

## 6. Operational disposition and unchanged mathematical gate

The two approved engineering obligations are now verified: complete historical artifact recovery and a successful automatic evidence-publication execution with exact readback. This supersedes the earlier operational blocker only. The new report/index commits are documentation after the tested source; they are not represented as the source executed by the final run.

No separate-context mathematical verdict was obtained, no external-AI reviewer was launched, and no post-acceptance mathematical publication audit or main merge is claimed. The original core-probe proof remains a candidate. Abstract observational factorization and this engineering verification do not derive an observer-accessibility mechanism or guaranteed native progress. Broader C3 and C4-C6 remain OPEN. No physical force, geometry, energy, GR/ADM, continuum, or fundamental time is derived.
