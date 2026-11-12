# Q171 PREREG (2026-11-11 22:05 MST). Written after reading the challenges and sketching the argument (disclosed); before any code was run.
Trigger: Dot 6814643598 and GPT 6814798658/6814814058 (countermodel f=id+ε(E_{1,0}+(2/5)E_{2,0}), ε=1/100, A_X={x≥0: f_X(x)≥0}) challenge T-421/Q168:
the full-cone domain was not derived.
Q: (1) Is the countermodel exactly right? (2) Can a SOURCED requirement replace the full-cone premise? Candidate: v16.22 TYPE_LEDGER A3/A6. Candidate maps
there must commute with BOTH P (fiber sum) and I (literal zero extension), and "naturality means commuting with every arrow in the declared class".
Q166 imposed only P1 and relabeling. Test (2a) I-naturality of the reference, f_X∘I_YX = I_YX∘f_Y, and (2b) I-stability of the positivity domain
(x∈A_Y ⇒ I x∈A_X) together with positivity on it, on the depth≤2 family f = b·T_0 + Σ a(d,j)E_{d,j} with zero-extended carriers up to depth 3.
Premises: P, I, relabeling INHERITED as operations (v16.22 A3; FCV P1–P2). Requiring the guard REFERENCE to be I-natural is SUPPLIED by analogy with
v16.22's declared standard for candidate maps; it is not inherited for references. The guard and the pair are SUPPLIED (Q157).
PASS: (1) all countermodel numbers reproduce; (2a) I-naturality forces a10=a20=a21=0, hence blind; (2b) I-stable domains containing x± plus positivity force
the same. FAIL: a surviving ancestor-weighted α under (2a) or (2b), or a countermodel mismatch.
Mutation controls: the GPT countermodel must FAIL (2a) and (2b); a pure truncation mixture (id) must PASS (2a).
