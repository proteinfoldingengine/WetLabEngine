# Implementation review and dispositions

Date: 2026-11-09 America/Phoenix.
Scope: review pipeline code only. This fresh-context author-side code review is not the independent Gemini scientific review.

The reviewer inspected the controller, archive script, workflow, independent checker, tests, frozen manuscript, plan and freeze file. It found no Critical issue and three Important issues:

1. Failure evidence was not durably archived because archive depended on successful publication.
   Fixed: archive now runs after all three predecessor jobs under always(), preserves every available original artifact across attempts and completed logs, and distinguishes preservation status, pipeline completion and mathematical acceptance. Adverse or malformed reviews cannot be relabeled accepted.
2. Retries could mismatch artifact attempts or trigger another generation.
   Fixed: verification and review execute only on originating attempt 1. Publication retries explicitly reuse verification-1 and review-1; their identities retain the originating attempt. A pre-call guard rejects a prior attempted review of the same manuscript hash in an earlier workflow run. The archive includes original-attempt artifacts on later publication/archive retries.
3. Immutable source identity was checked only after generation.
   Fixed: verification now reads all six path@commit sources from GitHub before review, checking content, byte count, SHA-256 and Git blob. Publication repeats the readback.

Regression evidence: reviewer_fixes_red.log contains four failures/errors before these features existed; reviewer_fixes_green.log records all nine contract tests passing. Initial tests_red.log and tests_green.log preserve the first five-test development cycle. The independent Fraction checker reproduces the original SymPy stdout exactly; no mathematical expected value was changed.

Remaining live checks: actual remote ancestry, Actions/helper execution, API artifact behavior and source readback are checked by the workflow, not certified by local code inspection. The inherited model caller was separately read: it performs a model availability GET, one generation, strict returned-model/STOP parsing, and never exposes the key in output. The scientific verdict remains pending until the actual raw response is inspected.

No unresolved Critical/Important issue or deferred minor was reported. No second author-side code-review round or duplicate Gemini review is requested.
