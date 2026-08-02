# Independent W-Holonomy Replication

This package independently reconstructs the pair-marginal BKM
observable-response holonomy pipeline for generalized three-qubit W states.

## Confirmed result

For every pure generalized W state

\[
a|100\rangle+b|010\rangle+c|001\rangle,\qquad abc\neq0,
\]

the canonical pair-derived BKM polar loop is lossless and has reflection
spectrum

\[
\{-1,+1,+1\}.
\]

The result survives random amplitudes, phases, local unitaries, source-basis
changes, and qubit permutations.

## Important correction

The earlier blanket claim of white-noise regularization independence is false.

For

\[
\rho_\epsilon=(1-\epsilon)|W\rangle\langle W|+\epsilon I/8,
\]

the transverse \(XY\) loop remains trivial, but the population sector is
controlled by the signs of

\[
q_{ij}(\epsilon)
=
\epsilon(1-2p_i)(1-2p_j)-4p_ip_j,
\qquad p_i=|a_i|^2.
\]

The loop is:

- a reflection when \(\prod_{ij}\operatorname{sgn}q_{ij}=-1\);
- the identity when that product is \(+1\);
- rank deficient when any \(q_{ij}=0\).

If one probability \(p_k>1/2\), the edge opposite node \(k\) changes sign at

\[
\epsilon_\ast=
\frac{4p_ip_j}{(1-2p_i)(1-2p_j)}.
\]

For \(p=(0.8,0.1,0.1)\), \(\epsilon_\ast=1/16\).

This produces an exact reflection → rank-loss → identity transition.

## Run

```bash
python -m pip install -r requirements.txt
python w_holonomy_replication.py --trials 100
pytest -q
```

## Claim boundary

This is a finite quantum-information result about canonical observable-response
transport derived from pair marginals. It is not a theorem about spacetime,
physical gauge fields, or gravity.
