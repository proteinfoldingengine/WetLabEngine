# Unique joint instrument for the retained record and P1 channel

Author construction, November 20, 2026 America/Phoenix. This strengthens the bounded source screen without changing its physical conclusion. It is a mathematical compatibility theorem in the existing supplied representation, not an identification of an actual event, a receiver, or a probability law.

## Fixed premises

Work on the ordered basis `(o,p,u,v)`. Let `pi_u=|u><u|`, `pi_p=|p><p|`, and `Q=I-pi_u`. The existing P1 benchmark is

`C(rho)=Q rho Q + rho_uu pi_p`.

Its identification with a physical pruning event and this matrix representation remain supplied. The original v15.11 actual-record routine supplies the following conditional semantics only after record `Q` is explicitly selected: with `tau=Q rho Q` and `q=Tr(tau)>0`, the selected state is `tau/q`. The original source does not choose the record.

The new theorem additionally fixes exactly two outcomes and requires their nonselective sum to be `C` on every input. These are theorem hypotheses, not physical conclusions.

## Theorem

There is exactly one two-outcome completely positive instrument `{M_Q,M_u}` satisfying both:

1. the `Q` outcome has probability `q=Tr(Q rho)` and conditional state `Q rho Q/q` whenever `q>0`; and
2. `M_Q+M_u=C` on all inputs.

It is

`M_Q(rho)=Q rho Q`,

`M_u(rho)=|p><u| rho |u><p| = rho_uu pi_p`.

### Proof

The specified probability and conditional state fix the unnormalized first branch:

`M_Q(rho)=q (Q rho Q/q)=Q rho Q` for every positive `rho` with `q>0`. Linearity extends the identity to the full matrix space; at `q=0` positivity already forces the branch to be zero. Subtracting this branch from the fixed nonselective channel gives

`M_u(rho)=C(rho)-M_Q(rho)=rho_uu pi_p`.

This map has the single Kraus operator `K=|p><u|`, so it is completely positive. Moreover

`Q^*Q+K^*K=Q+pi_u=I`,

so the sum is trace preserving. Existence and uniqueness follow.

The theorem remains true for arbitrary valid coherences, because the equalities are linear identities on all sixteen source matrix units.

## Strongest positive interpretation

The retained conditional record and the P1 channel do not have to be the same function. They are mathematically compatible as one joint instrument: the old retained record is one conditional branch, while the P1 contraction is the nonselective channel. This removes the false extra requirement that conditioning itself equal pushforward.

For the existing canonical diagonal preparations `(1,1,2,1)/5` and `(1,1,1,2)/5`, the `Q` outcome probabilities are `3/5` and `4/5`; its conditional parent populations are `1/3` and `1/4`; the complementary branch has conditional output `pi_p`; and the total P1 parent populations are `3/5` and `2/5`.

## Adversarial boundary

The original pinching instrument has complementary branch `rho_uu pi_u`, not `rho_uu pi_p`. In the fixed source/output encoding, changing it into the compatible instrument requires the branch action `u -> p`; relabelling the outcome does not change its state. The mathematical P1 benchmark contains that reset, but the actual-record source does not identify the accepted empirical occurrence with this instrument.

The uniqueness statement also depends on its exact contract. With more than two outcomes only the sum of the complementary branches is fixed. With equality required only on a restricted state family, other extensions may exist. Changing the source/output encoding changes the comparison.

Therefore the first unsupported correspondence is now exact: source evidence must identify the actual event with the `u -> p` branch action (or another producing operation) and separately justify availability of its retained record to a receiver. The theorem supplies neither correspondence. Actual atemporal occurrence remains accepted input; event typing, preparations, owner access, and any physical outcome law remain supplied.

## Sources inspected

- `ResearchHistory/UQCF-GEM/v15/v15.11/ontology_continuity_audit.py`, blob `8871e50f19322adbb62f34ea3837ba8e6cb16c8b`: complete pinching and explicit selected-record semantics.
- `ResearchHistory/UQCF-GEM/v15/v15.11/REPORT.md`, blob `255a62a329cc4ebb445122a8c5602df6e2dabc9c`: RAS/RCR conditional scope and instrument ambiguity.
- `ResearchHistory/UQCF-GEM/research/physical-bridge/record_selection_binding/ASSESSMENT.md`, blob `0f2159b84e00f6b5718eaa7ee01812767ad2fb18`: direct equality boundary and canonical preparations.
- `ResearchHistory/UQCF-GEM/research/physical-bridge/record_selection_binding/verification.json`, blob `3e41266a65f0d3f60a2a11d8f46e900907fe5c87`: exact bounded replay.
- `ResearchHistory/UQCF-GEM/research/physical-bridge/measurement_first_review/RESULT.md`, blob `e8523368d50c366150221c5210ea6192534008d7`: conditioning/pushforward compatibility is a comparison of compositions, not an identity of operations.

