# Preserved review attempts

- `45540986072-attempt3-invalid-review.zip`: after the earlier HTTP 402, Gemini returned an `ACCEPTED` label but put affirmative checks in the adverse `findings` array, used boolean proof checks, and set `event_forces_distinction=true`. The integrity gate rejected it.
- `45546017200-parser-reject.zip`: after the review schema and quantifier were clarified, Gemini returned the fully scoped accepted reconstruction with empty objection arrays and `event_forces_distinction=false`. The workflow still rejected it because the parser read `proof_checks` from the top level instead of `worked.proof_checks`.

The parser-only correction at `0c178a1bcedf7399ee003eaee9101f42e225828e` produced accepted run 45546189652 without changing the proof or numerical outputs.
