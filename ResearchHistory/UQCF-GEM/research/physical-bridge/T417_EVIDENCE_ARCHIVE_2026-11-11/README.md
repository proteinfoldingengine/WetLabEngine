# T-417 evidence archive (Q144–Q154) + Q155 support-guard obstruction — 2026-11-11

Status: NOT_DERIVED; Not claimed; scientific_breakthrough false. SUPPLIED->DERIVED: none.
Elementary supporting mathematics on the supplied R_inc^- reading. No novelty claim and no necessity claim; no prior-art statement in either direction.
CFR retention remains a premise. This is not a numbered retained-research closure stage (no CI run, no CLOSED/CERTIFIED status); it archives the local
working evidence behind thread entry T-417 (grok/agent-thread @ 60c7e306) as requested in PR111 comment 6809074411, plus the Q155 result referenced by T-418.
All files are archived byte-for-byte as produced locally (failed and posthoc runs preserved, nothing edited). Integrity: `sha256sum -c MANIFEST.sha256` from this directory.
The prior staging manifest (30 files, Q144–Q154 only) had sha256 prefix 88f7f724; MANIFEST.sha256 here is regenerated over all files including Q155 and this README.

## Scope correction (prominent, carried from T-417 / Q153 self-check)
The label-free core `Core` of the survivor reading is invariant **set-wise** under the chain automorphism group G (relabelling maps the reading to itself).
Its individual observables are defined only up to the G-action (e.g. e_{F_1(0)} -> e_{F_1(1)} in the n=4 witness). The **element-wise** fixed part is `Core^G`
(= R_min in that witness). A G-closed family is not a G-fixed element. See `independent_2026-11-11_1509/RESULT.md` and `q153_draft/DRAFT.md`.

## FAILED preregistered criterion C (Q146) — kept separate from the repaired C4
- Preregistered conjecture C (see `independent_2026-11-11_1304/PREREG.md`, pre-run part) FAILED at n=6.
- Run: `independent_2026-11-11_1304/q146.py` -> `independent_2026-11-11_1304/stdout.txt`: n=6 line reports `mismatch: 40` out of 32,478 cases
  (all one direction: C held, shell partition not G-invariant). stdout prints the first 5 mismatches; all 40 are reproduced by re-running q146.py.
- Witness: parents (·,0,0,0,1,4); prune {2,5} then {3,4}. Survivors 0 and 1 end with isomorphic leveled fiber chains {0,2,3}⊃{0,2} and {1,4,5}⊃{4,5};
  the owner sits in the level-1 pair in one and the removed atom in the other. The swap {0,2,3}<->{1,4,5} preserves every π_j but moves the shells.
- The failure is reported as a failure; C is necessary but not sufficient.

## Repaired criterion C4 (posthoc, labelled as such) and its proof
- C4 was formulated AFTER the C failure and is disclosed as posthoc in the Q146 PREREG addendum.
- Check: `independent_2026-11-11_1304/q146b.py` -> `stdout_posthoc.txt` (0 mismatches, n ≤ 6).
- Proof both directions: `independent_2026-11-11_1304/RESULT.md` (⇒) and `independent_2026-11-11_1334/` (Q147, ⇐ by top-down induction; n=7 random check is confirmation, not proof).

## Directory map
| folder | question | content |
|---|---|---|
| independent_2026-11-11_1204 | Q144 | survivor closure vs chain |
| independent_2026-11-11_1239 | Q145 | fixed state cannot covariantly supply the label (≤ 1/|G·σ*|) |
| independent_2026-11-11_1304 | Q146 | FAILED C (q146.py, stdout.txt); posthoc C4 (q146b.py, stdout_posthoc.txt) |
| independent_2026-11-11_1334 | Q147 | proof of C4 (⇐) |
| independent_2026-11-11_1410 | Q148–Q151 | gate drops; label-free core |
| independent_2026-11-11_1431 | Q152 | truncated unit history, depth c_j(w) (Thm 152.1) |
| independent_2026-11-11_1509 | Q153 | consolidation + adversarial self-check (Core vs Core^G) |
| q153_draft | Q153 | draft of the T-417 thread remark |
| independent_2026-11-11_1537 | Q154 | pinching side adds no label dependence |
| independent_2026-11-11_1609 | Q155 | support-guarded eligibility obstruction (one route only) |

## Q155 scope (referenced by T-418)
Granting incidence := support of the P1 grade, every P1/P2/relabeling command is support-equivariant on nonnegative grades (fiber sums do not cancel),
so support-guarded transcripts depend only on (type, initial support); the balanced pair (1,1,2,1)/(1,1,1,2) has full support before and after
((1,3,1) vs (1,2,2)) and is blind at every finite word. Check: 860,000 equivariance checks, 0 violations (seed 155).
Not covered: numerical threshold reads, owner observation, value-sensitive transition laws. Derives nothing; rules out one route only.
