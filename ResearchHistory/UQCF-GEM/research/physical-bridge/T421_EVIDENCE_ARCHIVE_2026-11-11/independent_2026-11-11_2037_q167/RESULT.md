# Q167 RESULT (2026-11-11 20:38 MST) — PREREG PASS; the guard is fiber-local; "global positivity" is a domain choice, not inherited
Sources read: Q158 q158.py fixed(): ω∘E_w=ω on the fiber iff x ∝ w, needing only w_p,w_u ≥ 0 not both 0 ON THE EVENT FIBER at the
actual state. FCV TYPE_LEDGER (scope §, L7–L11): inherited maps P,I,R,H are linear maps on all of F_X, natural on retained data.
v16.23 TYPE_LEDGER row C: "positive cone is a mathematical subobject, NOT every physically attainable grade".
Finding 167.1: nothing inherited requires a guard reference to be nonnegative on all states of all carriers. Lemma 166.1's hypothesis
(nonnegativity on all of F^+ with unbounded arity) is a mathematical-domain requirement; the physically attainable state set is not supplied.
Computation (q167.py, exact sympy; tree o→p→{u,v}, balanced pair, fiber {p,u}; f = βT_0 + Σ α(d,j)E_{d,j}, d≤2):
 fixed(x+) ⇔ −2a10/5 − 8a11/25 + a20 + 4a21/5 + 8a22/25 = 0
 fixed(x−) ⇔ −a10/5 − 4a11/25 + 3a20/5 + 12a21/25 + 4a22/25 = 0
 Diagonal-only (j=d, i.e. truncation mixtures): x+ condition = 2·(x− condition) ⇒ same hyperplane ⇒ BLIND (agrees with Q165/Q166).
 With ancestor-weighted terms (a10,a20,a21): two distinct hyperplanes ⇒ separation in EITHER direction, chosen by α. β drops out.
Located obstruction (sharpened): (a) reference required valid on the whole mathematical cone F^+ ⇒ Lemma 166.1 ⇒ blind;
(b) reference required valid only at the actual state on the event fiber ⇒ a 5-parameter natural family whose α picks which of x±
is lossless. Neither (a) nor (b) is supplied by the sources, and under (b) the direction is a free choice. No guard is derived.
Scope: linear, depth ≤2 instance of a classification verified to depth 3. Native bridge NOT_DERIVED; Not claimed.
Adversarial check: (i) not a restatement of Q157 — the free ratio is now tied to named natural operations, and the blind/free split is
traced to an unsupplied domain choice; (ii) the hyperplanes were derived from the classification, not chosen; (iii) Finding 167.1 rests
on the absence of a domain clause in the two ledgers read, not a full source census. Batch with Q165+Q166.
