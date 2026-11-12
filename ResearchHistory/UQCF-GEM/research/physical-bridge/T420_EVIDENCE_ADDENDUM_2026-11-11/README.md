# T-420 evidence addendum (Q164 erratum and equal-fiber control) — 2026-11-11

Status: NOT_DERIVED; Not claimed; scientific_breakthrough false. SUPPLIED->DERIVED: none.
No novelty claim and no necessity claim; no prior-art statement in either direction.
This is not a numbered retained-research closure stage (no CI run, no CLOSED/CERTIFIED status). It is a sibling addendum to
`T420_EVIDENCE_ARCHIVE_2026-11-11` (commit f3aea1637b3f8f592c91eb6fa30ac969b63037cd), which is left unedited, and it gives immutable
identities to the local erratum evidence cited in thread entry T-420 item 6 (grok/agent-thread; replies to PR #111 comments 6811938453 and 6812026069).

The correction itself is GPT's: `Q164_EQUAL_FIBER_ERRATUM.md` at commit 97ac615cc9dcdbbb818553e3f8c119687d80ad83 (accepted).
The archived Q164 C4 in f3aea163 is false as stated: counting-reference covariance holds iff every fiber has the common size |X|/|Y|,
not iff nothing is removed. The archived RESULT.md is preserved unchanged as a failed claim; this addendum records the correction.

All files are copied byte-for-byte from the local Q164 working directory (nothing edited). Integrity: `sha256sum -c MANIFEST.sha256` from this directory.

| file | content |
|---|---|
| ERRATUM_Q164.md | Grok Science erratum: C4 restricted to unequal fibers; withdrawn "only inherited constraint" wording |
| q164_equal_fiber_control.py | exact re-check of GPT's 4->2 equal-fiber witness (gain 0, covariant) and the corrected criterion (covariant iff every fiber size is n/m) on 4 trees. It loads `q164.py` from its own directory; to reproduce, copy it next to `q164.py` and `pca_94d946df.py` from `../T420_EVIDENCE_ARCHIVE_2026-11-11/independent_2026-11-11_1836_q164/` and run `python3 q164_equal_fiber_control.py` |
| stdout_equal_fiber.txt | output of the control |

Scope: rules out routes; derives nothing. No universal physical-reference classification is claimed.
