# UQCF-GEM v13.16 — Quantum Markov / Conditional-Mutual-Information Selection Gate

**Date:** 2026-09-12

## Adjudication

Exact quantum Markovity is **not** selected by the existing ontology.

That was already established upstream by v9.41: among 13,104 native ordered overlap triples, none had exact Petz reconstruction and none had a nontrivial exact recovery algebra.

So v13.16 does not reopen exact Markov selection.

Instead it closes a more useful result:

**small conditional mutual information can certify approximate locality with an explicit square-root error scale, provided the source/observable response is regular and the recovery map is available.**

## 1. Exact Markovity is a restricted sector, not a universal ontology law

The archived v9.41 result found:

- native ordered triples: 13,104;
- exact Petz gluing: 0;
- nontrivial recovery algebra: 0;
- every tested triple had `I(A:C|B)>0`.

Therefore global coherence in the retained architecture is not equivalent to exact local Markov gluing.

This settles the selection question negatively.

## 2. Exact Markovity is source-stable only for compatible sources

Take a strictly positive classical/commuting Markov chain

`p(a,b,c) ∝ exp[h_A a+h_B b+h_C c+J_AB ab+J_BC bc]`.

Its conditional mutual information is numerical zero.

Apply ETL source tilts supported on the existing cliques:

- `A`;
- `B`;
- `C`;
- `AB`;
- `BC`.

Across finite source strengths up to absolute `s=1`, maximum CMI remained

`6.661e-16`

and maximum Petz reconstruction trace distance remained

`8.674e-17`.

Thus the Markov sector is exactly invariant under clique-compatible commuting ETL sources.

But a non-clique `AC` source breaks Markovity.

At `s=0.4`:

`I(A:C|B) = 0.0606309640094`.

So exact Markov locality is not stable under arbitrary PGRL/ETL sources.

## 3. Exact parity-hidden family

Define

`p_eps(a,b,c)=1/8(1+eps abc)`.

For every `eps`:
- the `AB` marginal is uniform;
- the `BC` marginal is uniform;
- the classical Petz/Markov reconstruction is the uniform distribution.

Yet the hidden three-body parity differs.

Its exact conditional mutual information is

`I = 1/2[(1+eps)ln(1+eps)+(1-eps)ln(1-eps)]`.

For small eps,

`I = eps^2/2 + O(eps^4)`.

Now retain the local observable

`O=AB`

and use the one-site ETL source

`P=C`.

Because ETL differentiation in the commuting sector is covariance,

`d_s <O>|_0 = Cov(O,P)`.

For the true state,

`Cov(AB,C)=<ABC>=eps`.

For the Markov-recovered state it is zero.

Therefore the exact local-response error is

`Delta dot O = eps`.

Hence

`Delta dot O = sqrt(2 I)+O(I^(3/2))`.

The executed small-epsilon mean of

`response_error/sqrt(2 CMI)`

was

`0.999985968496`.

This is essentially unity.

## 4. Sharp consequence: linear-in-CMI locality error is impossible

The previous family gives

`response error ~ eps`

while

`CMI ~ eps^2/2`.

Therefore no universal bound

`response_error <= C * CMI`

with finite state-independent C can hold arbitrarily close to exact Markovity.

The natural scale is instead

`O(sqrt(CMI))`.

This is an exact no-go on an overly optimistic locality error law.

## 5. Certified recoverability route

A standard quantum recoverability theorem gives, for some recovery channel,

`F_root(rho_ABC, R(rho_AB)) >= exp[-I(A:C|B)/2]`.

Using the fidelity/trace-distance relation,

`T(rho,recovered) <= sqrt(1-exp[-I])`.

For commuting ETL response,

`dot <O> = Cov(O,P)`.

For any two normalized states rho and sigma,

`|Cov_rho(O,P)-Cov_sigma(O,P)|`

is bounded by

`6 T(rho,sigma) ||O||_inf ||P||_inf`.

Therefore a recovered local model has the certified response error

`<= 6 ||O|| ||P|| sqrt(1-exp[-I(A:C|B)])`.

For small CMI this is

`O(sqrt(I))`.

Five hundred random commuting controls were used to check the covariance/trace-distance lemma.

Maximum observed error/bound ratio:

`0.152235278777`.

So the bound is conservative but valid in the tested controls.

## 6. What this does and does not give us

It gives a principled approximate locality statement:

**if separator CMI is small, then there exists a recovered state whose bounded-observable ETL response is close to the true response with an explicit error bar.**

This is not a heuristic truncation.

But important boundaries remain:

1. The general recoverability theorem is existential.
2. It does not say the canonical Petz map is always the optimal recovery map.
3. Small CMI is not protected under arbitrary source insertion.
4. We have not yet propagated the state error through BKM metric and polar-transport conditioning.

So this is not yet a complete approximate QMAR geometry theorem.

## 7. Architecture

The result now reads:

`global quantum completion`
-> if exact Markov + compatible source: **exact separator locality**

and more generally

`small separator CMI`
-> **recoverable local approximation with O(sqrt(CMI)) state/response error**

provided the downstream response map is regular.

The remaining mathematical job is to calculate those regularity constants for the actual BKM/polar geometric maps.

## Status

- exact Markovity selected by ontology: **NO**
- exact Markov sector: **EXISTS**
- exact sector stable under clique-compatible ETL: **YES**
- exact sector stable under arbitrary ETL: **NO**
- small-CMI approximate locality: **CERTIFIED CONDITIONALLY**
- linear CMI error law: **FALSE**
- square-root CMI scaling: **SHARP IN EXECUTED COMMUTING CONTROL**
- canonical Petz generic QMAR closure: **NO**
- Pillar 3: **OPEN**

No broad scientific breakthrough is declared.

This is a **major approximate-locality theorem plus exact Markov-selection no-go**.

## Next — v13.17

### Recoverability-to-QMAR Geometric Error Propagation Gate

The next step is to propagate the recoverability error through the actual retained geometry.

On faithful states with:
- a lower eigenvalue floor for local marginals;
- a singular-value gap for pair correlation polar decomposition;

derive explicit Lipschitz/conditioning bounds for:

- BKM metrics `K_i`;
- polar transports `O_ij`;
- nonmetricity `Q_ij`;
- loop holonomy `H`.

Then combine those constants with the v13.16 `O(sqrt(CMI))` state-recovery error.

If that closes, we will have the first certified **approximate local geometric response theorem** in the pre-time branch.
