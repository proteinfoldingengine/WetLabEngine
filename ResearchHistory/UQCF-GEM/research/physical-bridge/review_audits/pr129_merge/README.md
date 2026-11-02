# PR129 actual-merge audit

The actual scientific merge passed the complete integration and publication
replay. **Native receiver delivery remains NOT_DERIVED.** This closes the
post-merge verification obligation for the corrected conditional package; it
does not close the physical interaction bridge or establish a new physical law.

| Record | Immutable identity |
|---|---|
| Scientific merge | `084617b4c392b8955f0a19d2c2b2c02dfa8d9d91` |
| Reviewed PR head | `324183d11baec30926e8e995ce033d0c07ea06af` |
| Frozen audit controller | `899793e16f360435af6cf86d1451cc9b81d57ce3` |
| Verification and independent-job replay | [Actions 41367189521](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/41367189521), both jobs successful, attempt 1 |
| Durable publication and readback | [Actions 41367701007](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/41367701007), successful, attempt 1 |
| Archived evidence commit | `cc7d46fb998901a9884339745398ca397e679698` |

## What was verified

- All 67 merged PR paths retain their reviewed-head blobs. The audit's additions
  leave scientific and previously reviewed files unchanged.
- All 61 document records across the three preserved reviews match merged
  source bytes and original prompts. Review manifests and the preserved T249
  review/failure ZIPs pass integrity checks.
- Python 3.11.17, Sympy 1.13.3 and mpmath 1.3.0: 22 FCV tests, 15 inherited
  pruning tests and 2 historical tests pass in each job. Full FCV production and
  independent reconstruction cover 21 instances, 197 carriers, 1,028 prunings,
  5,049 chains and 13,725 steps in each original/relabeled universe; all 9
  deliberately defective certificates are rejected.
- Original and successor producer, independent stdlib verifier, and control
  outputs reproduce published bytes exactly. All 10 original and 12 successor
  rejecting controls pass. Replaying the original computation does not revive
  withdrawn prose: CORRECTION_T241/T242/T249 govern the accepted scope.
- A separate fresh job reproduces all ten deterministic scientific files
  byte-for-byte. Both downloaded artifact ZIPs pass their GitHub API digests and
  all member manifests. Their complete source snapshots are identical.
- Post-execution local readback checks the exact declared snapshot scope and
  all 1,295 contained files against Git blob identities at the scientific merge.
  This includes the complete scripts directory and transitive review helpers.
- Durable publication reads back 84 evidence files plus their manifest. The
  original large ZIPs are preserved without recompression as ordered 32 MiB
  parts. `run-41367189521/DOWNLOAD_AUDIT.json` records order, lengths and digests;
  `EXTRACTION_POLICY.json` explains reconstruction. Complete source ZIPs remain
  inside those original archives; other evidence also has browsable copies.

The reproducible post-execution checker is `readback_sources.py`; its result is
`LOCAL_READBACK.json`. `GIT_PUBLICATION_READBACK.json` records separate Git
publication verification. The original publication receipt ZIP and its extracted
receipt are preserved beside this report.

## Independent review and scientific boundary

The existing fresh Gemini review [41356747755](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/41356747755)
accepted the whole corrected argument with empty findings, missing assumptions
and counterexamples, and `native_bridge_status=NOT_DERIVED`. Its raw response
SHA256 is `22e78de96d3d7bcdf28d84e6d25e729ee84c3167e7c9c693f38ecb70b3b1327d`.
This integration audit made **no new Gemini request** because no reviewed
scientific bytes changed. Earlier adverse/qualified reviews and the pre-model
infrastructure failure remain intact.

The [T252 analytical response](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6566172877)
accepts the Bell-state challenge in its supplied coherent-channel domain:
`tau_u = tau_0 = I/2` but `mu = Z/2`. Consequently, source influence on coherent
inputs does not force receiver contrast on the diagonal P1 benchmark. W_Bell
must supplement W_R/W_E when screening a non-invariant candidate constraint.

For an owned source effect F, the reduced-channel identity fixes
`Tr[(F tensor I) W Delta-rho W*] = Tr[F C(Delta-rho)]` across realizations.
Variable optimized receiver contrast does not invalidate that fixed witness.
But membership of such an effect in this designated complementary receiver's
interface is still missing. Adopting OA* changes the supplied interface; it is
not an inherited derivation of delivery to that receiver.

INHERITED: the existing source contracts and repository closure requirements.
DERIVED: integration and byte-reproduction results, plus the scoped analytical
checks in T252-work-a. SUPPLIED: quantum encodings/channel, joint-realization
class, ordered factors, receiver interface and access. NEW ASSUMPTION: none
adopted. No accessible native receiver distinction or physical realization is
established. No claimStatus change or default-branch merge.

Local tooling disclosure: an optional batched Git blob prefetch failed; the
already running sequential exact-commit readback completed successfully for all
84 files and the manifest. `LOCAL_PREFETCH_FAILURE.json` preserves that error.
No scientific or Actions run was repeated.
