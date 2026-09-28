# v16.05 — Conditional omitted-edge localization

Status: the preregistered sufficient conditions and direct exact polynomials were confirmed for all 12 archived states; see RESULTS.md.

Let S be the span of four-site Pauli words with at least one identity on sites 2,3. The ideal historical construction rho=(rho_012 tensor I_3/2 + rho_013 tensor I_2/2)/2 lies in S. The actual archived binary state must be checked separately.

D acts only on (2,3). For a local identity its generator vanishes. For a local weight-one Pauli input, the product-depolarization commutator removes every weight-preserving output. The only possible surviving local output has weight two. Spectator indices remain unchanged. Therefore the surviving global output has weight at least two, has no one-body component, and can have global weight two only when both spectator indices are identities. Such a pair is necessarily (2,3).

The local unital diagonal preparations preserve this support. Because the D tangent has zero one-body moments, the two product terms in the connected differential vanish for this support class. Consequently the D connected direction on the first five readout edges is zero, and its contraction with any smooth five-edge readout Hessian is zero. The sixth-edge direction may be nonzero. This conclusion does not require an accidental cancellation inside that Hessian.

More generally, the same conclusion applies to a state decomposed as rho_S+rho_extra when [L_D,M_a]rho_extra=0. That sufficient condition is stronger than necessary; failure does not determine the first-five projection. Direct exact connected polynomials are the authoritative archived-state check.

This is a conditional statement about the frozen source locality, state support, preparation and selected five-edge readout. It is not a universal D-null theorem for arbitrary four-qubit states or other loop choices. In particular, a two-body input on (2,3) outside the stated support may yield a one-body commutator, whose connected subtraction can reach other edges when the baseline has nonzero one-body moments.

The preregistered computation tested the entire sufficient basis class, inspected the archived support remainder, computed exact six-edge polynomials, and compared them against independent high-precision numerical directions and the published T_D matrices. No new geometry or source is chosen.
