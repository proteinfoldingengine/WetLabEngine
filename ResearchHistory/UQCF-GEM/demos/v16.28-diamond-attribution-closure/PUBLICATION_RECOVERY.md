# v16.28 publication recovery

Publication run 36630157852, job109617054828, at 76591239620d2c5347ceaed4a42e8ff944417081 stopped BEFORE fresh scientific reproduction or commit. The GitHub CLI refused to emit an original Actions log because that log includes ANSI color escape sequences. This was an archival transport failure, not a failed mathematical check.

The only publication-code correction is to pass the documented `gh api --allow-escape-sequences` option when capturing raw API responses. The bytes are captured into a Python pipe and written to archival files, not interpreted as shell code or displayed on a terminal. JSON/ZIP/log integrity and SHA checks remain unchanged. Official option documentation: https://cli.github.com/manual/gh_api .

The original failed run's metadata, log and partial archive are added to the permanent registry. The science modules, proofs, tests, input universe, original GREEN and expected scientific files are unchanged. The next publication attempt must again pass all198 tests and full byte equality before pushing.
