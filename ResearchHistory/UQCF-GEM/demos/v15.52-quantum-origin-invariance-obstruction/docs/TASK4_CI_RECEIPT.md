# v15.52 Task-4 independent audit — execution receipt

Date: 2026-09-24. Scope: proof documentation, finite implementation regression, and rejection of the archived Task-3 packet. **Not positive quantum-origin certification and not completion of Task 5.**

## Authoritative GREEN

Executed code-and-proof head: `6c155744fe93ddbab88d87dcea3a5b9953cd4319`.

[GitHub Actions run 36010367976](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36010367976), job `107669190694`, completed SUCCESS. Exact-checkout verification passed. Test output completed on 2026-09-24 at 14:06:50 UTC under CPython 3.13.5 / ubuntu-24.04.

| Discovered suite | Tests passed |
| --- | ---: |
| v15.52 | 52 |
| v15.46 | 63 |
| v15.47 | 31 |
| v15.48 | 15 |
| v15.49 | 15 |
| v15.50 | 28 |
| v15.51 | 27 |
| Total | 231 |

No skipped or expected-failure tests were accepted. These are the current directory-discovered suites, not a full-repository regression or a claim to reproduce every historical campaign's test count.

The v15.52 tests include 1,555 exhaustive finite observation/target tables checked against all corresponding finite decoders, all 24 source relabelings, and adversarial premise/contract/readout/type mutations. These checks supplement the written proof; they are not a proof assistant.

The independent audit ran twice, verified nine archived Git blobs, and emitted byte-identical JSON. The recorded file `VERIFICATION.json` is the same canonical report; its SHA256, computed locally after matching the logged report, is `b77597f9ece04d93592339febf0d497e6516a2368c3a558f1e278678bc10b96b`.

Compilation, tracked-tree immutability, original six v15.52 source/test byte preservation, and no changed UQCF research files outside v15.52 all passed. The existing action pins emitted a Node-runtime deprecation warning; it did not fail execution. No action upgrade or unrelated changes were made.

## Authoritative RED

[Run 36009511693](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36009511693), job `107666284298`, on `62667ec83e311b47c759495b83a398d9dccee424`: 50 tests ran, 17 archived tests passed and 33 new tests failed because the independent verifier was absent. No unrelated test errors were observed. Downstream workflow stages were skipped at this expected RED boundary.

Two further exact-type regressions first failed locally, were repaired, and passed in the authoritative 52-test GREEN suite. Published implementation/test/proof Git blob hashes match the locally executed/reviewed files.

## Scientific output

`status=WITNESS_REJECTED`; `quantum_origin_certified=false`; `T2=NOT_CERTIFIED`.

Reasons: shared mutable observation records, label-only quantum output records, and no registered quantum admissibility/reduction validator. T1 has the general factorization proof in `TASK4_THEOREM_AUDIT.md`; T3 is conditional on a valid target witness. No exhaustive quantum-model search was performed, and no nonexistence-of-witness theorem is asserted.

This receipt and the stored report are evidence additions after the executed code head. They do not alter executable scientific code or retroactively change its verdict. Any subsequent documentation-head run is a separate execution, not silently substituted for the run above.

Source correspondence remains `NOT_EVALUATED`; Pillar 3 remains OPEN. This work is on the research branch; no merge to main or independent human review is claimed.
