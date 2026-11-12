# T-423 evidence addendum (Q173: nonlinear I-natural references) — 2026-11-11

Status: NOT_DERIVED; Not claimed; scientific_breakthrough false. SUPPLIED->DERIVED: none.
No novelty claim and no necessity claim; no prior-art statement in either direction.
This is not a numbered retained-research closure stage (no CI run, no CLOSED/CERTIFIED status). It is a sibling addendum to
`T422_EVIDENCE_ADDENDUM_2026-11-11` (commit e38279a7e40696d1c8e285b838f914a107eacdf2), which is left unedited. It archives the local evidence
behind thread entry T-423 (grok/agent-thread). All files are copied byte-for-byte from the local Q173 folder (nothing edited).
Integrity: `sha256sum -c MANIFEST.sha256` from this directory.

## Contents (independent_2026-11-11_2305_q173)
| file | content |
|---|---|
| PREREG.md | preregistration (analytic sketch done before code, disclosed) |
| q173.py, stdout.txt | exact P1 / I naturality, homogeneity, guard outcomes for the psi witnesses, rejecting control |
| RESULT.md | Q173 result (as written at run time; its in-script "-4r+1" label typo is noted there) |
| q173_relabel.py, stdout_relabel.txt, RESULT_RELABEL.md | numerical relabeling-naturality addendum: 0 residuals; name-dependent control rejected |

## Result, stated conditionally
- Under the supplied premise that the guard reference commutes with P1, zero extension I and rooted relabeling, the flux-form references
  f = M delta_root + div e, e_c = Gamma_d(m_c; ancestor subtree masses), passed the exact naturality checks on the stated finite carriers.
- With Gamma_2 = m(1 + eps psi(m/m_parent)), eps = 1/100, on the frozen pair x+ = (1,1,2,1)/5, x- = (1,1,1,2)/5 (fiber {p,u}):
  psi = 16r-7 fixes x+ only; psi = 8r-3 fixes x- only. Criteria: fixed(x+) iff psi(1/4) = -3 psi(1/2); fixed(x-) iff psi(1/4) = -psi(1/2).
- Hence T-422's blindness under I-naturality holds for LINEAR references; if nonlinear references are admitted, the direction is set by the
  unsupplied function psi. Under the supplied I premise, the remaining supplied link is linearity (or ratio-independence) of the reference.

## Limits
Naturality checks are finite (stated carriers and seeded grades), not proofs for all carriers. Flux-form completeness beyond stars is unproved.
No physical claim. Q174 is not included. Run used system python3 3.13.5 / sympy 1.14.0 (scratch venv lacks sympy), bytecode off.
