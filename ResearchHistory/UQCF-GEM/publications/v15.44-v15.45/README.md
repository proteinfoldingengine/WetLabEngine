# Selective publication of v15.44 and v15.45

## Purpose and source identity

Publish the two completed research snapshots into the default repository view without merging the divergent historical research branch. The publication starts from main commit `dcf493aa898b286d500c2693925038747096042f`. Its only source snapshot is `23cc8642ca484e23a3a4e809cf83ed325d9f25ba`, which includes the unchanged v15.44 tree.

| Snapshot | Exact original tree | Original certification |
|---|---|---|
| v15.44 | `d37f88b98d38aad864e22146ad7dcd2d00f89cd4` | [35814970929](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/35814970929), source head `9085e4fa0bec3dbd700f759a8a9629b230d226ff` |
| v15.45 | `775e5549303c1276d3458ec34b553a604436bf0f` | [35933791472](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/35933791472), source head `23cc8642ca484e23a3a4e809cf83ed325d9f25ba` |

Both complete version directories, including code, tests, proofs and result ledgers, are copied by Git object identity, not regenerated. [MANIFEST.json](MANIFEST.json) specifies every permitted import. The scientific source branches and PR #55/#56 are retained as provenance; they are not merged wholesale into main. No v15.46 files are imported.

## Dependency closure, not a historical branch merge

The manifest includes the seven executable modules and the two v15.43 input/result files named by v15.44 `dependencies.json`. v15.45 additionally consumes the pinned v15.40 `response_generation.py` as source-definition evidence, not by executing its historical NumPy-dependent runtime. The v15.44/v15.45 approved specifications and implementation plans are preserved with their exact blobs.

Consequently, the v15.40, v15.42 and v15.43 directories on this publication are **support-only subsets**, not complete independent stage releases. Earlier stage source, proof context and historical workflows remain available on the pinned [source research tree](https://github.com/proteinfoldingengine/WetLabEngine/tree/23cc8642ca484e23a3a4e809cf83ed325d9f25ba/ResearchHistory/UQCF-GEM/demos). No unrelated protein code or historical lab removals are reverted.

The main research README and STATUS are the only replaced existing files. Their prior blobs are retained intact at `HISTORICAL_INDEX_v15.03.md` and `HISTORICAL_STATUS_v15.03.md` in the same directory, preserving relative links and the old dated record. No existing scientific file is changed or deleted. Old auto-publishing and per-task workflows are deliberately not imported.

## Verification and reproduction

Publication integrity is not a fresh full scientific certification. `verify_publication.py` checks complete Git inventories, exact directory tree hashes, every dependency blob, preservation of the old indices, the main baseline ancestry, the requested head and absence of unrelated/working-tree edits. It does not use GitHub's capped compare-file listing.

Ten focused tests use real temporary Git repositories. They first failed because the checker was absent, then passed locally on CPython 3.13.5. These are checker tests, not a claim that the full repository or either original scientific suite was run locally. The working container could not clone the remote repository; real-checkout verification occurs in the publication Actions job.

From the repository root:

```sh
python ResearchHistory/UQCF-GEM/publications/v15.44-v15.45/verify_publication.py --root .
```

The read-only publication workflow also runs the copied v15.45 factorization, spectral, archive-binding, dependency, source-firewall and gate tests, rejects skipped/expected-failure tests, and byte-replays its existing `docs/RESULTS.json`. It does not rewrite that file or push a generated commit.

The expensive full presentation suite is not rerun by this publication check: its exact code is preserved and the historical full-suite receipt remains the source of that evidence. Likewise, the original `test_ci` ancestry checks and v15.44 coordinator require their original research-branch ancestry and are not silently weakened to accept this main-based branch. Reproduce the original full certifications by checking out their recorded source commits and following the original workflows. Running every historical ancestry-bound checker directly on main is not the publication contract.

## Interpretation and remaining limitations

The copied v15.45 ledger records `FACTORIZATION_CERTIFIED_WITH_EXPLICIT_SPECTRAL_BOUNDARY`. It preserves the odd/even kernel obstruction and labels the 592 response distinctions as dependent on centered injectivity plus distinct inputs. The canonical unit-scale source identity is construction-dependent, not independent validation. Formula implications can be predictions; comparing two mutually constructed quantities is not an independent observation.

Frozen README statements that Task 7 was pending describe an earlier execution point; the successful final run above is the later receipt. The snapshots are not edited merely to modernize that wording. Historical limitations of those implementations are not erased by a publication pass. No independent scientific peer review is claimed here.

Source correspondence stays `NOT_EVALUATED`; no physical curvature, gravity, stress-energy, Einstein equations, continuum limit or foundational uniqueness is established. No new time or dark-matter primitive is introduced. **Pillar 3 remains OPEN.**
