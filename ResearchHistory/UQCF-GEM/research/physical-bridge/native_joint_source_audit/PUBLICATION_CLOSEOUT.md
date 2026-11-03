# Original source-audit publication completion

Date: 2026-11-02 America/Phoenix. Publication-only completion of T-283-dot/T-284/T-286.

The original source audit's evidence is durably published at commit 363298eea7f498b972fa1e74a82e9de0e29a6027, with immutable remote readback in [archive run 41566294628](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/41566294628), job 125688542238. The job verified all 95 manifest-listed stored files and independently rechecked the three original ZIP digests. The evidence directory also contains SHA256SUMS, for 96 files in total.

The original verification/publication artifacts contain 36 and 37 manifest entries; review contains 12. All 85 member digests match. The ten deterministic outputs of the original verification and fresh publication jobs agree byte for byte. Three complete original job logs are stored as downloaded bytes. Exact source/controller snapshots, model request, response, metadata and parsed result are retained.

Original run: 41486442606; source 2f7a788f551face7b69521b0d07d2ec3e3ea3871; controller 340a9465a92e8ffd387bd26d31c8fe2f5e33f3fe. Archival controller: 4fb1fd497b708713fb9135b65990b6416023a3cb. No scientific rerun or model request occurred during this publication completion.

The original test logs report 22 FCV, 15 parent and two historical tests passing, plus the original verification and rejecting-control suites. These are original results preserved and inspected here, not new executions. The publication utility was locally checked against the downloaded artifacts and a deliberately corrupted response member, which was rejected.

ADJUDICATION.md remains byte-identical, Git blob 2dcb74c47022db10753b4e1556f0f11837e8a860. Gemini's raw NO_CANDIDATE response still contains material ownership/classification errors and incomplete coverage. Publication does not turn it into an accepted theorem or exhaustive source audit. Scientific acceptance remains false and native delivery remains NOT_DERIVED.

The old pending receipt is preserved as PUBLICATION_PENDING_ORIGINAL.json and in history. PUBLICATION.json now identifies the completed evidence/readback. The archive job's complete decoded UTF-8 log is stored in ARCHIVE_JOB_125688542238.log (SHA256 020c7ad374d2cc157f52dcc30eabcdc06017a0e68848b5f2cf66801f8f9dcbbf); original job logs in evidence retain the raw API bytes.

This closes durable archival work on the review branch. Research-branch integration is checked separately against evidence subtree b43a637a9ba778bfc1488db8a518e09bb3458784; no claim of a merged state is made by this pre-merge record.
