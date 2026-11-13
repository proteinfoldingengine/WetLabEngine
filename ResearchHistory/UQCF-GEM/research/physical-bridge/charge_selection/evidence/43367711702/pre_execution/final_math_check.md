# Final draft mathematical check

Status: **NO MATHEMATICAL BLOCKER FOUND** in the inspected `package/ResearchHistory/UQCF-GEM/research/physical-bridge/charge_selection/ARGUMENT.md`.

This was a pre-freeze editorial check against the earlier analytical proof, not a repeat external review. The draft itself was not modified. Only local text was inspected; no scientific computation, external API/model calls, or GitHub writes were performed.

Verified:

- Global charge blocks have the correct shift sign. Unit-gap exclusion kills whole bath operators before any restriction to `supp(tau)`, so arbitrary coherent, mixed, rank-deficient, and non-invariant bath supports are covered.
- Pure source marginals confine every occupied bath summand; linearity extends the confinement across the bath support. The stated positivity argument then establishes `M=pi_u` for all coherent source inputs.
- `W_R` is a globally conserving, exact-channel witness. The resonant-bath SWAP control is exactly conserving and makes the entire receiver state equal to arbitrary `tau`. The Hadamard control preserves exact C and gives fixed-pair blindness only; its all-input formula `1/2-Re(rho_pu)` is correct.
- Equal source charge `q_u=q_p` forces a blank receiver. The rank-`2k` input and rank-at-most-`d` output prove the finite-bath condition `2k<=d` and full-rank emptiness. The nondegenerate spectrum `{0,1/2}` correctly shows that this dimension condition is not sufficient. The degenerate pure-bath construction correctly supplies a nonempty blank boundary.
- The dual-channel formula for diagonal source charges and the statements `C*(I)=I`, `C*(pi_u)=0` are correct. The native/NEW distinctions and non-necessity boundaries remain explicit.

The historical writer identity was also checked against `old_attempt` embedded in `sources.json`: the earlier note explicitly sets `Q_R=delta*pi_1` with `delta=q_u-q_p`, and `J_R=I_SE tensor pi_1`. Hence the quoted identity `W†J_R W=pi_u` for nonzero delta has the required normalization and is correct.

Optional readability refinement, not a required mathematical correction: in the historical comparison, define `J_R` when first used and say “all-input first-moment balance with no E contribution” rather than “no-environment” balance. The older argument includes E as a Hilbert factor but excludes its contribution to that balance.

This check does not authenticate remote Git object identities, external literature, or an archive-wide novelty claim; those are outside its mathematical scope.
