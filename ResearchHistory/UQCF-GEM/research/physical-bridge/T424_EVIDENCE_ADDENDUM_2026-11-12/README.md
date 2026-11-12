# T-424 evidence addendum (Q174, Q175, Q174b: flux-form completeness, the c = 2b condition, positivity) — 2026-11-12

Status: NOT_DERIVED; Not claimed; scientific_breakthrough false. SUPPLIED->DERIVED: none.
No novelty claim and no necessity claim; no prior-art statement in either direction.
This is not a numbered retained-research closure stage (no CI run, no CLOSED/CERTIFIED status). It is a sibling addendum to
`T423_EVIDENCE_ADDENDUM_2026-11-11` (commit 06d0a96f4d5c19eb5b5ef52c09e11dcf0a8c5d4a), which is left unedited. It archives the local evidence
behind thread entry T-424 (grok/agent-thread). All files are copied byte-for-byte from the local run folders (nothing edited).
Integrity: `sha256sum -c MANIFEST.sha256` from this directory.

## Contents
| folder / file | content |
|---|---|
| independent_2026-11-11_2335_q174/PREREG.md | preregistration (analytic sketch done before code, disclosed) |
| independent_2026-11-11_2335_q174/q174.py, stdout.txt | exact flux reconstruction and P1 residuals for 4 flux maps; sibling-dependent control; a, b, c guard criteria vs direct evaluation |
| independent_2026-11-11_2335_q174/RESULT.md | Prop 174.1 (flux form, proof under the supplied P1 + I + relabel premises) and Cor 174.2 |
| independent_2026-11-12_0005_q175/PREREG.md, RESULT.md | line-cited audit: no inherited clause forces c = 2b; it enters only through the A6 F-linearity premise |
| independent_2026-11-12_0005_q175/stdout.txt | two witness lines (b, c for psi = 16r - 7 and for the linear member). DISCLOSED: the inline command that printed them was not saved; the psi values are recomputed by q174b.py (S1 line "a b c 4/5 97/500 101/250"), and the linear member (Gamma_2 = m) gives b = 1/5, c = 2/5 by direct substitution |
| independent_2026-11-12_0008_q174b/PREREG.md | preregistration for the positivity question (written before q174b code; analytic sketch disclosed) |
| independent_2026-11-12_0008_q174b/q174b.py, stdout.txt | S1-S4 exact checks, P1 / I / relabel residuals, rejecting controls |
| independent_2026-11-12_0008_q174b/q174b_run1_FAILED.py, stdout_run1_FAILED.txt | preserved failed first run (SyntaxError in an eval string after S1 printed; S1 lines identical to the passing run) |
| independent_2026-11-12_0008_q174b/RESULT.md | Q174b result: positivity finding, Prop 174b.1, open-cone witness |

## Result, stated conditionally (every premise below is SUPPLIED)
- Prop 174.1 (proof, under supplied premises P1 + I + relabel): a reference commuting with fiber pushforward P (FCV TYPE_LEDGER L7),
  zero extension I (FCV L8) and admitted relabelings (v16.22 TYPE_LEDGER line 19) has the flux form f = phi(M) delta_root + div e,
  e_c = Gamma_d(m_c; ancestor subtree masses), Gamma(0; .) = 0; conversely (argument) every such (phi, Gamma) commutes with those arrows.
- Cor 174.2: on the frozen pair, a = Gamma_1(4/5; 1), b = Gamma_2(1/5; 4/5, 1), c = Gamma_2(2/5; 4/5, 1); fixed(x+) iff 2a = 2b + 3c,
  fixed(x-) iff a = 2b + c. With a free, the class is blind on the pair iff c = 2b (two-point additivity, weaker than linearity).
- Q175: c = 2b is not forced by any inherited clause found; it follows from the supplied A6 F-linearity premise.
- Q174b positivity: the psi = 16r - 7 witness is positive on x+ and x- but not closed-cone nonnegative (f_p = -1/125 at (1/5, 0, 2/5, 2/5)).
  Under supplied closed-cone nonnegativity every member is blind on the pair (Prop 174b.1). Under supplied open-cone positivity only, a
  discontinuous member separates; with continuity of Gamma_2 at 1/5 and 2/5 it is blind. Which positivity premise, if any, is inherited
  for guard references is open (Q176).

## Limits
Pair only. Finite checks except the stated proofs. The Q175 audit is text search plus reading of named clauses, not proof-assistant level.
A4 (R, H on W) type gap unchanged. No physical claim. Interpreter: system python3 3.13.5, Fractions only, PYTHONDONTWRITEBYTECODE=1.
