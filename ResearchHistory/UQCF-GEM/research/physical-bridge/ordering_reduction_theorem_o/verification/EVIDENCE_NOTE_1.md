# Evidence note 1 — meaning of `C3.wrong_first_responses` (append-only clarification)

- **Author:** proteinfolding-grokbot (Grok), 2026-10-22 (America/Phoenix).
- **Requested by:** dot's audit note on T-066 / run 39861546954 ([PR #111 comment 6352742732](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6352742732)).
- **Scope:** naming clarification only. No evidence byte is changed, nothing is rerun, and no claim changes.

The original checker report `evidence/run-39861546954/witness/checker_report.json` (SHA-256 `535a509427af30687cfcf25420668defa23aeb6379d8596535d8fef206b52770`, preserved unchanged) contains

    "C3": {"contains_displayed_restoration": true, "restoration_histories": 410, "wrong_first_responses": {"1": 480}}

The field `wrong_first_responses` is misnamed. Its value is the distribution of decoded first-response values over the 480 stopped C3-class histories from source 1 (it is copied from `independent_counts.C3_1.decoded_values`; `checker.py` line 286). `{"1": 480}` therefore means all 480 first responses decode to the correct source value 1, i.e. the number of wrong first responses is **0**. The checker's gate (`checker.py` lines 288–289) fails unless the set of decoded values is exactly `{"1"}`, so a wrong response could not have passed.

A correct name would have been `decoded_first_response_values`. Per dot's request the original bytes are preserved and the run is not repeated solely to rename the field. Any future rerun of this checker should use the corrected name; this note is the authoritative reading of the existing report.

Dot's audit also records that the report's independently computed menus are checked, but not every top-level producer metadata field. That limitation stands as stated.
