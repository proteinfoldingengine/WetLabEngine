# receiver_identification d27 freeze: amendment 1 to FREEZE.md section 5 (review transport only)

Author: proteinfolding-grokbot, 2026-10-19 ~18:00 ET. Committed together with the review-script change it describes, before
any dispatch under it. FREEZE.md itself is unchanged (sha256 `e7aae7e0105dccf9fac53847e7c4096659244aac29f16ce4df8a9c8af5bb1d83`),
and so are RESULT.md (`2fe553f9…`), the producer, checker and comparator, and the workflow file.

## Why

Under FREEZE section 5 the review was dispatched once (run 39325925419) and re-run once at the same SHA. Both requests were
rejected by the Gemini API with HTTP 429 Too Many Requests before any model output; no verdict exists. The prompt was 425,777
bytes, of which 375,524 bytes were the whole of RESULT.md (sections 0 to 32 and every revision note). Aaron Spradlin's standing
approval to send repo documents to Gemini (2026-10-17) covers a new dispatch; the parent agent confirmed (2026-10-19 17:28 ET)
that no new OK is needed and asked for a leaner prompt.

## What changes (review script `uqcf_rid27_review.py` and the file list of `uqcf_rid27_publication.py` only)

1. The review script still asserts that the whole RESULT.md equals the frozen bytes (sha256 `2fe553f9…`). It sends two exact,
   contiguous byte excerpts of it instead of the whole file: E1 = bytes [0, 44853), the header lines of every draft (including
   the draft-27 line under review), the revision notes and the credit section; E2 = bytes [265609, 375524), sections 26 to 32 in
   full (section 26 and 27 define the read ledger, the address class and the climb used in sections 28-32; sections 28-30 are the
   cited inputs nearest to the argument). Each excerpt is sent with its offsets, length and sha256. Sections 0 to 25 are not sent;
   they were reviewed under earlier freezes and are cited inputs only. The referee is told that they are omitted and that a step
   it cannot check for that reason must be reported as a missing assumption, not assumed true. The review scope (sections 31 and
   32 with [D26] and [D27], and the draft-27 header line) and the task list are unchanged.
2. The prompt also carries this amendment, FREEZE.md and the full compare.json as before. The script asserts that compare.json
   has the sha256 of the preregistered push run 39325886792 (`be2c1952ef33f4a7eca39aa1b794915beabb8a715734c73b8e87e6cc737cb233`);
   since producer, checker, comparator and FREEZE.md are byte-identical, any other value is a RED and nothing is sent.
3. Transport: if the generateContent request returns HTTP 429 or 503, the script waits a preregistered 300 s and sends the same
   request bytes once more; every attempt's HTTP status and the API's error body (no credentials) are kept in `transport.json`.
   At most two requests per job. No other status is retried.
4. Stopping rule: one dispatch with review = true at the commit that adds this file; a transport failure without a verdict may be
   re-run once at the same SHA. Both are recorded. A verdict of any kind is final for this freeze and is reported as returned.
   No prior verdict exists, so none is shown.
5. The publication audit additionally reads back this file at the run SHA.

Disclosure: the prompt assembly was run once locally with the network call stubbed out (no request sent, no key used); the
assembled prompt was about 209 KB, about half the earlier size. Nothing about the argument, the preregistered values or the
controls changes.
