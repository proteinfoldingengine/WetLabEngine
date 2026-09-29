# v16.24 publication transport failure and recovery

The scientific GREEN remains `19c7069bad79ff361d612f742ad5e79dbfef1dc6`, run 36585110111. No scientific module, test, proof or preregistered criterion changed in this recovery.

Publication run **36586143978**, job **109466876778**, attempt 1, executed at `940dd7a2733436249f453531bde14aab6cca0691`. All original archive/source checks, all 112 fresh tests, full production, independent verification and complete-byte comparisons passed. Every publication file hash also passed. The subsequent `git push` was rejected by GitHub with `Internal Server Error`; that attempt is FAILURE, not successful publication.

Its complete generated evidence survived in artifact **11041313392**, 440,085 bytes, SHA256 `720dbc055bd93579cf993e0ae0754a86a2944163e6eedb5e34c52a81b178c4cf`. The recovery workflow reuses only this hash-pinned evidence, verifies every original manifest entry against the unchanged source, preserves the failed-run artifact/metadata/logs, reruns the complete pipeline, checks scientific bytes again, then publishes with a bounded non-force-push retry. Any unexpected remote ref stops publication rather than overwriting it.

The final publication receipt records the NEW successful execution and commit separately. The failed job is not rerun in place or relabeled successful. This is a transport recovery, not a scientific result change or a weakened verification gate.
