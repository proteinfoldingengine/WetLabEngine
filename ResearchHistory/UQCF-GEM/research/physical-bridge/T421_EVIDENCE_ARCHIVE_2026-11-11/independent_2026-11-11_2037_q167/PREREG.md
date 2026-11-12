# Q167 PREREG (2026-11-11 20:37 MST)
Q: does the Q157/Q158 guard E_w need the reference nonnegative on all states/carriers (Lemma 166.1 hypothesis) or only on the event fiber
at the actual state? Sources: q158.py fixed(), FCV TYPE_LEDGER L7-L11 + scope §, v16.23 TYPE_LEDGER row C.
Computation: on the balanced pair, fiber {p,u} (Q157 tree o-p-{u,v}), with f = Σα(d,j)E_{d,j}+βT_0, solve exactly for the sets
fixed(x+), fixed(x-) in α-space. Prediction: both are distinct hyperplanes through 0 inside the j<d directions; restricted to α(d,j)=0 (j<d)
they coincide ⇒ blind. FAIL if the two conditions coincide on all of α-space (no separation at all) or differ already with j=d only.
