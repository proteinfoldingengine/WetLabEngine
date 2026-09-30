# v16.33 — Pre-adjudication proofs

K1. A legal deletion of leaf c from view i changes child-incidence data only at v=parent(c). Therefore q is unchanged iff tau_v is unchanged.

K2. Let t=tau_v before deletion. Since deletion cannot decrease tau_v, q is unchanged iff a t-view child cover remains after deletion. Equivalently at least one old minimum cover survives. This is the exact one-step invisible-incidence criterion.

K3. q-equivalence itself does not imply that the straight deletion path between comparable covers stays in the q-class unless every deleted incidence satisfies K2 at the state where it is removed. Gate B must therefore be adjudicated rather than assumed.

K4. A canonical minimal representative requires uniqueness in the incidence partial order, not merely a deterministic algorithm. If two incomparable inclusion-minimal covers have the same q, no choice between them is earned from q alone.

K5. Relabeling-equivalence of minima must be tested separately from labeled uniqueness. A symmetry orbit is not literal uniqueness.

No physical gauge interpretation is assumed.
