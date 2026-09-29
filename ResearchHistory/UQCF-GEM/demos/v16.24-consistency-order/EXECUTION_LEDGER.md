# v16.24 execution ledger

Scope and proofs were committed before production at 1335532db55062af83fbe2bfd875c18eecb7d490. GitHub wiring RED 36583580004: setup succeeded; all 28 tests failed because engine.py was absent; no scientific result was taken from RED.

Initial implementation f838bd86596db5884a9d3b33f245b127c55f56c8, run 36584333728: 28 new tests and 82 inherited tests passed, with complete producer and independently reconstructing verifier. Initial certificate bytes: 6,426,004, SHA256 d5354333bab67ee84bcd8e1a108d93ff6767d6f37e0fa8842af139a0cf60ee6b.

Self-review identified an input-validation defect, not a change to the scientific claim: parents (-1,2,99) could be followed before all targets were range checked, producing IndexError instead of explicit invalid-input ValueError. Test-only commit 3e50f0fb4930502214bc43ed91ee1fc96596a7aa / run 36584604280 reproduced the defect. The existing 28 tests passed; the new malformed-target test failed and the reordered-valid-lineage control passed.

The correction moves range validation of ALL parent targets ahead of traversal. No admitted input, mathematical equation, case universe, witness construction or verifier is changed. The next GREEN must rerun the complete campaign and publication must compare the original and corrected scientific bytes. Old GREEN is not retroactively described as covering later guards.

Review is self-review. No separately executing reviewer was available/claimed. Published proof arguments remain scoped to the inherited formal cone; algorithmic verifier independence is not independent authorship.
