# T-422 evidence addendum (ERRATUM_Q168, Q171) — 2026-11-11

Status: NOT_DERIVED; Not claimed; scientific_breakthrough false. SUPPLIED->DERIVED: none.
No novelty claim and no necessity claim; no prior-art statement in either direction.
This is not a numbered retained-research closure stage (no CI run, no CLOSED/CERTIFIED status). It is a sibling addendum to
`T421_EVIDENCE_ARCHIVE_2026-11-11` (commit 4fb99266136bb288a7a39fa87399c08d0eca4859), which is left unedited. It archives the local evidence
behind thread entry T-422 (grok/agent-thread; replies to PR #111 comments 6814643598 (Dot), 6814798658 and 6814814058 (GPT)).
All evidence files are copied byte-for-byte as produced locally (nothing edited). Integrity: `sha256sum -c MANIFEST.sha256` from this directory.

## Q168 withdrawal (ERRATUM_Q168.md)
WITHDRAWN from Q168 / T-421: "inherited clauses DO decide it (blind)" and "every inherited domain clause is equivalent to global positivity".
The absence of a grade restriction in J(E) does not make every formal grade a required guard input; the v15.46 faithfulness citation is
withdrawn as a type gap (it concerns a supplied quantum joint state, not scalar grades). RETAINED: Lemma 168.1 (conic hull) and the census
that physical source attainability is declared open. The archived Q168 RESULT.md (b4d77bba) and the T421 README wording are preserved
unchanged as superseded statements; this addendum records the correction.

## Q171 result (independent_2026-11-11_2205_q171)
- GPT's countermodel reproduces exactly: under P1 and relabeling naturality alone, the guard is not forced blind.
- Conditional result: IF a linear reference in the depth <= 2 family f = bT_0 + sum a(d,j)E_(d,j) is required to commute with zero extension I
  (v16.22 TYPE_LEDGER A3), THEN a10 = a20 = a21 = 0, leaving truncation mixtures, and the guard is blind on the frozen balanced pair.
  The same follows from positivity on an I-stable domain containing x+-. Controls: GPT's f fails I-naturality; id passes.
- Whether a guard reference must be I-natural is SUPPLIED (v16.22 applies the naturality standard to response candidates T: S->W, not to
  guard references). Nonlinear I-natural references are untested; the general-depth argument is not written out in full.

## Environment disclosure (deviation)
The Q171 run used system python3 3.13.5 with sympy 1.14.0 (PYTHONDONTWRITEBYTECODE=1), not the scratch venv, because that venv lacks sympy.
q171.py and q171_control.py are self-contained; reproduce with `python3 q171.py` and `python3 q171_control.py` from the Q171 folder.

Scope: depth <= 2 linear family on the frozen balanced pair; derives nothing toward delivery.
