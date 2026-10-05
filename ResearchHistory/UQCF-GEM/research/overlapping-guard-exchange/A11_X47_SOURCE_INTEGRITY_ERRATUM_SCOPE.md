# A11.X47 source-integrity erratum scope

Date: 2026-10-05 UTC.
Accepted X47 publication head: 6414a606bba86712faa89222ef5f7d5203085acd.
Integration branch remains: 0a1cd7019762daa71a8982322ed9a4a74c04ac53.

## Incident

The X47 mathematical result was accepted, but its LaTeX-bearing Markdown was serialized through ordinary JavaScript template literals. JavaScript escape processing converted sequences beginning with backslash-b, backslash-v, backslash-f and backslash-r into C0 control bytes and removed other intended backslashes before GitHub received the content.

A live-source scan at the accepted head gives:

- A11_X47_REDUNDANCY_ORBIT_OBSTRUCTION.md: 39 forbidden C0 controls;
- INDEPENDENT_A11_X47_WHOLE_REVIEW.md: 19 forbidden C0 controls;
- A11_X47_CLOSEOUT.md: 4 forbidden C0 controls;
- KNOWN_RESULTS.md X47 addition: 5 forbidden C0 controls;
- NEXT_OBLIGATION.md X47 addition: 5 forbidden C0 controls;
- A11_PROGRESS.md X47 addition: 5 forbidden C0 controls.

The affected proof and review also contain zero literal backslashes, confirming that intended mathematical commands were not preserved. The publication readback compared GitHub against the already-escaped in-memory strings and therefore verified byte identity without detecting semantic rendering damage.

The accepted candidate, reviews and branch history remain immutable evidence of the incident. They will not be deleted, rewritten in place or relabelled.

## Authorized correction

Publish a new authoritative ASCII-math rendering of the exact accepted X47 argument under a new filename. Do not alter the theorem, hypotheses, family, calculations, controls, dependencies or limitations. Publish a source-integrity erratum identifying the superseded rendering and exact affected blobs.

Before publication, require a failing scan on the historical files and a passing scan on every new erratum file:

1. no C0 character other than newline, carriage return or tab;
2. no replacement character;
3. required literal tokens for beta, Gamma, rho, empty intersection, X40L-before-Theorem-A and non-disconnection;
4. exact GitHub byte readback after each commit.

Use ASCII mathematics throughout the correction. This follows the working X40-X46 publication pattern and removes the escaping boundary entirely.

## Review and reporting gate

Freeze the corrected proof before a fresh independent whole-argument/source-integrity review. The reviewer must verify mathematical equivalence to the accepted theorem, all exact formulas and limitations, the incident diagnosis, and absence of control-byte corruption.

After acceptance, append an erratum note to STATUS.json, KNOWN_RESULTS.md, NEXT_OBLIGATION.md and A11_PROGRESS.md; publish an erratum closeout; obtain a distinct reporting review; append only that review; then perform immutable readbacks, full-tree comparison and a non-force live-branch fast-forward.

This is a publication-integrity repair only. It authorizes no new theorem, numerical execution, workflow, implementation, benchmark, integration merge or numbered certification. v16.55/v16.54, frozen evidence and the separately scoped unstarted efficiency work remain unchanged. X48 research resumes only after this gate closes.
