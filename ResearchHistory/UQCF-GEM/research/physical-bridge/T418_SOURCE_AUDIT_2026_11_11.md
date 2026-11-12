# T-418 source and evidence audit

Date: 2026-11-11, America/Phoenix. Reviewer: GPT Work.
Source snapshot: `47b938e274dcabadf2bd7b1dc3f60f908dad07a5`; thread read through T-418 at `7109a28acc5fca6a1f674359274941f5aa4a8ccb`.
Status: **PROVENANCE CHECKED; Q155 SCOPED ARGUMENT CHECKED BY GPT; NATIVE DELIVERY NOT_DERIVED.**
This is a source/evidence review, not an independent Gemini acceptance, a numerical reproduction, or a numbered-stage closure.

## 1. What was verified

The archive commit adds exactly 36 files under `T417_EVIDENCE_ARCHIVE_2026-11-11/`, with parent `c72d173933926b8b90d16efcf2bb2f095d1b4a3b` and no other edits.

I retrieved all 35 files named by [MANIFEST.sha256](https://github.com/proteinfoldingengine/WetLabEngine/blob/47b938e274dcabadf2bd7b1dc3f60f908dad07a5/ResearchHistory/UQCF-GEM/research/physical-bridge/T417_EVIDENCE_ARCHIVE_2026-11-11/MANIFEST.sha256), reconstructed their UTF-8 bytes, and independently computed SHA-256 and Git blob SHA-1 (the latter hashes `blob <byte-length>\0<bytes>`). All 35 SHA-256 values matched the manifest; all 35 blob identities matched the connector's Git identities. The manifest itself also matched its Git blob. The complete identities are retained in section 5.

The archived Q146 stdout explicitly reports 40 mismatches at n=6 and prints five witnesses. Its PREREG file retains the failed C statement and a separately labelled posthoc C4 addendum. The archive therefore preserves the failed result instead of replacing it with the repaired outcome. These are checks of the archived record, not a rerun of those cases. A local timestamp in a PREREG file is not independent proof that it preceded execution; this commit publishes the files together. No claim of independently authenticated pre-run timing is made.

The names `independent_...` in these folders do not by themselves establish an independent reviewer. This audit does not promote the Q144-Q154 theorems, finite counts, or their author self-checks to independently accepted results.

## 2. Q155: valid obstruction, with precise scope

[Q155 RESULT](https://github.com/proteinfoldingengine/WetLabEngine/blob/47b938e274dcabadf2bd7b1dc3f60f908dad07a5/ResearchHistory/UQCF-GEM/research/physical-bridge/T417_EVIDENCE_ARCHIVE_2026-11-11/independent_2026-11-11_1609/RESULT.md) gives the following sound argument for nonnegative coordinate grades. Under a fixed P1 fiber sum, a destination is nonzero exactly when some source in that fiber is nonzero. Zero extension and relabeling likewise have support maps fixed by their typed commands. Composition preserves this property. Hence equal initial type and support yield equal support histories and equal support-dependent legal-command menus. A common policy using only these data has equal transcript laws by coupling its randomness.

For the declared pair `(1,1,2,1)/(1,1,1,2)`, deleting u gives `(1,3,1)/(1,2,2)`; the retained p grade differs, while both supports remain full. This particular support-guard route cannot expose that difference. The argument does not make the numerical output equal, and does not address a separately justified value-sensitive law or available numerical effect.

Two scope details should be carried forward without rewriting the raw archive:

1. **Same support is sufficient for blindness; different support alone is not a general guarantee of distinguishability.** RESULT correctly says the route can separate a pair only if its supports differ. PREREG's stronger phrase “separates exactly the pairs” requires an interface that actually exposes the differing supports, or another separating guard. If all admitted guards ignore the differing coordinates, distinct supports need not produce distinct observed transcripts. Granting full support observations is legitimate as a stronger test interface for the negative result, but is not derived native access.
2. **Nonnegativity is a scope restriction here, not a universal FCV scalar axiom.** [FCV TYPE_LEDGER](https://github.com/proteinfoldingengine/WetLabEngine/blob/47b938e274dcabadf2bd7b1dc3f60f908dad07a5/ResearchHistory/UQCF-GEM/foundational-closure-verification/TYPE_LEDGER.md) distinguishes physical additive grades from its signed rational linear diagnostic. It does not derive a universal physical scalar domain. Thus Q155's cancellation argument applies to the stated nonnegative sector. Signed cancellation is an algebraic control outside that sector, not evidence that physically preparable negative populations have been derived. The positive balanced pair remains covered either way.

I inspected q155.py and its stdout but did not execute it. Its reported 860,000 checks remain the author's bounded run evidence. The analytical induction supplies the all-finite-word claim within the stated model.

## 3. Deduplication of the next proposed routes

The carrier/probe direction does not currently add a new delivery mechanism. [CORE_PROBE_RESULT](https://github.com/proteinfoldingengine/WetLabEngine/blob/47b938e274dcabadf2bd7b1dc3f60f908dad07a5/ResearchHistory/UQCF-GEM/research/physical-bridge/COUPLED_C3_CORE_PROBE_RESULT.md) already derives a positive capacity certificate from an actually observed successful core deletion. [CORE_READOUT_RESULT](https://github.com/proteinfoldingengine/WetLabEngine/blob/47b938e274dcabadf2bd7b1dc3f60f908dad07a5/ResearchHistory/UQCF-GEM/research/physical-bridge/COUPLED_C3_CORE_READOUT_RESULT.md) already derives complementary core certificates. Both expressly retain the access/enforcement/progress premises.

[receiver_move_interface/RESULT](https://github.com/proteinfoldingengine/WetLabEngine/blob/47b938e274dcabadf2bd7b1dc3f60f908dad07a5/ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_move_interface/RESULT.md) already locates bare cross-index command dependence at external global leaves and gives a guarded internal-response control. A new illustration of changed legality does not remove these operational premises.

Q155's NEXT Q156 proposes an inherited stochastic law from RAS/RCR or v15.x. The v15.11 candidate has already been inspected in [NATIVE_RECORD_ORIGIN_DEPENDENCIES](https://github.com/proteinfoldingengine/WetLabEngine/blob/47b938e274dcabadf2bd7b1dc3f60f908dad07a5/ResearchHistory/UQCF-GEM/research/physical-bridge/COUPLED_C3_NATIVE_RECORD_ORIGIN_DEPENDENCIES.md). I checked the actual source again at this snapshot:

- [v15.11 REPORT, section 3](https://github.com/proteinfoldingengine/WetLabEngine/blob/47b938e274dcabadf2bd7b1dc3f60f908dad07a5/ResearchHistory/UQCF-GEM/v15/v15.11/REPORT.md) supplies the retained algebra under RAS and the actual positive-weight record under RCR.
- [ontology_continuity_audit.py](https://github.com/proteinfoldingengine/WetLabEngine/blob/47b938e274dcabadf2bd7b1dc3f60f908dad07a5/ResearchHistory/UQCF-GEM/v15/v15.11/ontology_continuity_audit.py), blob `8871e50f19322adbb62f34ea3837ba8e6cb16c8b`, defines `select_record(rho, projectors, record=None)`. It rejects an omitted record. It computes the selected block's weight only after the record index has been supplied, then normalizes that block. There is no sampling or grade-dependent event-address selection in that function.
- Its `record_control()` already compares projective and random-unitary instruments with the same nonselective channel but different record weights. This is an existing instrument-ambiguity control, not an earned native P1-to-owner selector.

Therefore reusing this function cannot derive the input it explicitly requires. This finding is limited to the inspected source. It does not assert that no other inherited value-sensitive law exists.

A probabilistic candidate must be judged by its **derived outcome distribution** at a fixed available owner effect. A common possible NOOP history alone does not prove equal distributions under a specified law. Conversely, choosing a new probability kernel because it creates a signal would supply the missing mechanism. Neither mistake is licensed by this audit.

## 4. Concrete next work item

For Grok's Q156, admit one candidate only when it names an exact inherited operation with a source-value-dependent transition, resolved-outcome law, or owner read. Trace the source variable into that operation and identify the owner-held object it actually changes. Keep the source pair, event, owner and effect fixed within the claim.

The response should identify:

- the immutable source path/function and its actual input/output;
- which source-dependent input is inherited, and which remains supplied;
- the resulting change at one fixed owner effect, or the first precise missing operation if no such change follows;
- a blind alternative with the same declared inputs/interface if claiming underdetermination.

Do not require full removed-u recovery, a complete decoder, or deterministic success on every realization when one justified effect contrast suffices. Do not reopen the v15.11 supplied-record function, repeat support-word sweeps, or repackage the core probes. If a different source contains a candidate, cite that exact operation before launching a campaign. A source-specific failure is an acceptable result; an archive-wide absence claim is not.

No new premise has been adopted or promoted. No Gemini submission, scientific enumeration, new research branch, merge, or hold change was made for this audit.

## 5. Verification receipt

```json
{
  "commit": "47b938e274dcabadf2bd7b1dc3f60f908dad07a5",
  "parent": "c72d173933926b8b90d16efcf2bb2f095d1b4a3b",
  "changed_files": 36,
  "all_added": true,
  "archive_path_set_matches": true,
  "no_other_edits": true,
  "manifest_sha256": "e26ce2b1cc3cc7694ad56d358a2eea5e3f41713c48342b93aca583801d0dac53",
  "manifest_git_blob": "de72584ac151efd7d248f018e12c3445fa004e3f",
  "content_sha256_matches": 35,
  "content_git_blob_matches": 35,
  "manifest_git_blob_matches": true,
  "verification_utc": "2026-11-11T23:33:26+00:00",
  "verification_phoenix": "2026-11-11T16:33:26-07:00",
  "scientific_programs_rerun": false,
  "files": [
    {
      "sha256": "fb8bbc8069b00fed0f1b8e6a45cadb3e2ba058998f3348ae8e42ac98653a28fb",
      "path": "README.md",
      "git_blob": "fc084b38c5d8396c591ba70e71cfbdbf503601bb"
    },
    {
      "sha256": "811289ff4a54e400ecd15f3b804a98efb428144f2e056d4c2be739d04c5ef93e",
      "path": "independent_2026-11-11_1204/RESULT.md",
      "git_blob": "3905858991169c1adba7b10ac9887b53d5f1f9c3"
    },
    {
      "sha256": "9f5614e92a2cee07bd31753163551eaef600710297504b5eb0ee4a35b1416ba0",
      "path": "independent_2026-11-11_1204/q144.py",
      "git_blob": "6d4596d81e310b31f5daab4df183b6253d7fb669"
    },
    {
      "sha256": "59ee71f1bf8e20c547ddb699c9dfade0fd46d809bb649646f1d83a571f1c49be",
      "path": "independent_2026-11-11_1204/stdout.txt",
      "git_blob": "dea877de660877b641fc29ff9b2bf51e17105d6e"
    },
    {
      "sha256": "c4b132fc1431085d50c84ff02dcdb0c089a7432126b583a7103cd05be650b5f5",
      "path": "independent_2026-11-11_1239/RESULT.md",
      "git_blob": "2d9f67da3fe52dd23b9285038736a78c2bcf895f"
    },
    {
      "sha256": "e2a9a75f211ea2d1170aa0c37a3dd57a66444ae9c4092c0c6a3c01928bd5f0e9",
      "path": "independent_2026-11-11_1239/q145.py",
      "git_blob": "8cc0576918a129cc111845299cae8a0fdb7b7ea1"
    },
    {
      "sha256": "079719ce63a67946d784cc426fa088a9c2eea1665b2d6e1ac063340b120fe48e",
      "path": "independent_2026-11-11_1239/stdout.txt",
      "git_blob": "c6ec5d1cc36cc961a94b4d4286ce640cc93c6006"
    },
    {
      "sha256": "46c2991e6d41a5ffc1fc073343760b71e99bf3ae1f1abef047f9303e317e4910",
      "path": "independent_2026-11-11_1304/PREREG.md",
      "git_blob": "d33b689734146d03b30b544c0fb3bb616573c468"
    },
    {
      "sha256": "b5e914bd603ced0b6ded3a20a02635e6585fa1713ae43e6ada5444cff3740c61",
      "path": "independent_2026-11-11_1304/RESULT.md",
      "git_blob": "037994e1cc5b0ba57d4c48b101b7be1015bd10a6"
    },
    {
      "sha256": "25efcbe0a6254e0532d3b276ef71dade9a8ccec916054b1ac068b8dd17e5c669",
      "path": "independent_2026-11-11_1304/q146.py",
      "git_blob": "52dfc13510dd18593e08121643bea27d415dbb6d"
    },
    {
      "sha256": "3534b969925b6c326b6835ffc400eff87b117e375bb8eff4cf5841784ce4fb8f",
      "path": "independent_2026-11-11_1304/q146b.py",
      "git_blob": "815f8cfa7a06bc8ee672e6d3b7970da2fcccfdb0"
    },
    {
      "sha256": "183c41b3e5c7f2b8ed722e6bef8d4196667da84538bb8930a4d3260fd90d3575",
      "path": "independent_2026-11-11_1304/stdout.txt",
      "git_blob": "03327e90d3b85676a9935e1bd109b329abdade39"
    },
    {
      "sha256": "dff0d1ff75e2aa125b90b4df2746254e3a0e74a770f1d77390ace41c736665d9",
      "path": "independent_2026-11-11_1304/stdout_posthoc.txt",
      "git_blob": "9a845d6b30aaba085660b9e49eb895c433b5e5b1"
    },
    {
      "sha256": "4dd6aa55e3e096f49711f79cad6a8d1e7c5068e4146114e294a93037e61aa3a3",
      "path": "independent_2026-11-11_1334/PREREG.md",
      "git_blob": "ab2609c4e1ef1aacd8745e2c9437beca95e5d3d3"
    },
    {
      "sha256": "4784256d4d73a3e28a6d4104653819e089de0ed039fc70a6f4de4c3c88c4d76f",
      "path": "independent_2026-11-11_1334/RESULT.md",
      "git_blob": "0359d27fb45a88ce7f238d138e1da350856580e5"
    },
    {
      "sha256": "69c64817b52b4892e480c162938de6f47cdc905a54e06a6ca1d42983765034dc",
      "path": "independent_2026-11-11_1334/q147_check.py",
      "git_blob": "402e551e259c479bced36a01e9a2d2a4601e3417"
    },
    {
      "sha256": "430fb4c151033df479a7c2415a056b4c851c47e35ed2b8d10d7fb323225960ad",
      "path": "independent_2026-11-11_1334/stdout.txt",
      "git_blob": "7cff141a7de7e04633cce3c88b99dd0e1e3810c0"
    },
    {
      "sha256": "5f4f1bcf1fe15914dab72d2a3d0c6785ba7a6fff0efc33ffd8771edfe472e7f4",
      "path": "independent_2026-11-11_1410/PREREG.md",
      "git_blob": "bf443d5a89848df12ee4ed41caed4027227e3ede"
    },
    {
      "sha256": "1429936b13f321757183817d4a4efc61de444f4fa303f954197ffbd96d1272fb",
      "path": "independent_2026-11-11_1410/RESULT.md",
      "git_blob": "1b2a4f1acc123715e4f676882b9803b2f60376d1"
    },
    {
      "sha256": "47661dadbff9834cc68eb6f28fb86088e56c44c9c8df8d48033c3b3d5043f44b",
      "path": "independent_2026-11-11_1410/q151.py",
      "git_blob": "d199de0e41be14ac065a296f774bc17e372770a3"
    },
    {
      "sha256": "4c42b595ce245a270e586c21e74913872d68df48a104ad049307c261d8cb9bbd",
      "path": "independent_2026-11-11_1410/stdout.txt",
      "git_blob": "df1c0660d7bc1453bd6193b1c87c733b2f1cd5e9"
    },
    {
      "sha256": "833b50be6c2ccb03ade57a50030605e44e2ef7fb418942857b04775aedb39105",
      "path": "independent_2026-11-11_1431/PREREG.md",
      "git_blob": "8fe8d0de82db8fbe8c7e260140b156b75c8d95f2"
    },
    {
      "sha256": "beaaa9dac7789b5faee7af7c0cecfcb45f855ac6b3992fa356310ea41f2bad61",
      "path": "independent_2026-11-11_1431/RESULT.md",
      "git_blob": "89ad03b588a9326f15ccbf05e212059e3a826b92"
    },
    {
      "sha256": "6040ccf5e1ae1665fa9e753eec56ded33e96512be29cf095aac33b6a95215f90",
      "path": "independent_2026-11-11_1431/q152.py",
      "git_blob": "f185cc75ab69477073caebd09d3f9bdf9671973b"
    },
    {
      "sha256": "ab4407a5565180693a4957b5fc1ca3d7bdef5e319767db7a960aaff109ab0626",
      "path": "independent_2026-11-11_1431/stdout.txt",
      "git_blob": "89960e60d6508f5ded4899885b4fd707f447775e"
    },
    {
      "sha256": "f307912879d640808b6010beff549a6e1c23db1f4e4aebbb7d388f6a9ad8ad6b",
      "path": "independent_2026-11-11_1509/RESULT.md",
      "git_blob": "39f01d4cec74f5f146a90f2609abdfc47f962249"
    },
    {
      "sha256": "c05c26d162ad5c2012164dce7b1dc5e06594584a97239072c4d36707c41f4648",
      "path": "independent_2026-11-11_1537/PREREG.md",
      "git_blob": "427e215621354785875be34ed56c7b17a69826ae"
    },
    {
      "sha256": "d10b39e84467a1494ab3317cda719c653e3f2ce046f8f26c93d5f9e64a29dded",
      "path": "independent_2026-11-11_1537/RESULT.md",
      "git_blob": "50dd7b3bdb7ecbf9d4d6707f91f7ba4b371d06a0"
    },
    {
      "sha256": "cf9eb3e3f73c4230e2aeb7f1063a794847c0fc0baae466ad21ef3a2e87664439",
      "path": "independent_2026-11-11_1537/q154.py",
      "git_blob": "1615a7dc0b0ec082ce1773a0554bb413bf7a4718"
    },
    {
      "sha256": "06eaa289fcfab647e41fad0c8e0ac609a2b9136ca3403341b79638432d4ca963",
      "path": "independent_2026-11-11_1537/stdout.txt",
      "git_blob": "5b2a9ff4b45d8fdc4fdb9cfc5040a53e851a3f34"
    },
    {
      "sha256": "9a3d7d6c817a770e4b86311b29d385aa8cb955b8028217296c812c170cc251d7",
      "path": "independent_2026-11-11_1609/PREREG.md",
      "git_blob": "0ce234d371e6652046b2663f69c97dfcb2660608"
    },
    {
      "sha256": "0a1c86f5240018f8e5f694312c3baf218d69f16dfc62b9870a1b5d1ae187cec4",
      "path": "independent_2026-11-11_1609/RESULT.md",
      "git_blob": "1295c53c4cf1847f6cc442a47b0f2be5b3a5bab0"
    },
    {
      "sha256": "83d08d7a4884dd26e1ea763f750da47be6fcb8a2b9d37251168397b847e37e6f",
      "path": "independent_2026-11-11_1609/q155.py",
      "git_blob": "f375b04d4404d15c3a546ab4e06329a652dbeb11"
    },
    {
      "sha256": "5b9a0e0fe8058bea945d5f317670644307d23d3c0b58a4917e76f0206456ef6d",
      "path": "independent_2026-11-11_1609/stdout.txt",
      "git_blob": "6e47e039b4b5177c6aaa4570c807a744354bd1c4"
    },
    {
      "sha256": "0702b08063231885e87e1b50efb5022c501027f9c44f455ea361d11f6996b6ae",
      "path": "q153_draft/DRAFT.md",
      "git_blob": "d85bbb86b24695df104c14bf2342baf7341bb417"
    }
  ]
}
```

For a checkout of the pinned archive, `sha256sum -c MANIFEST.sha256` reproduces the manifest comparison. This audit additionally checked every payload against its recorded Git blob and checked the commit's exact changed-path set.
