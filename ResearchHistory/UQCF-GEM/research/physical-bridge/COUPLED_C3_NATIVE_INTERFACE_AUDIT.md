# C3 native retained-interface audit — author-side source checks

Date: 2026-10-07.
Status: AUTHOR-SIDE AUDIT / INDEPENDENT REVIEW PENDING.
Frozen scope 9e762fc7cf0354c3f5bf48e2a4cf4c79fe5d1e0e.
Proof candidate 750a6b2170bed809b64095a7f5c383b6abdc1b46.

Source checks:
1. Existing POST_A12_DYNAMIC_RESIDUAL_RESULT.md at d1aeaeba5ddb6a6748a5a80cb69d5ab76fdf8db7 explicitly defines M_R(H) for all nonempty H of size<=4 on FULL palette, including singleton spectator labels, and does not establish initialization or observer accessibility.
2. Choosing residual family {r4} gives M_R({z})=1-1[z in Z] exactly for every spectator z, so b=OR_{z in T}(1-M_R({z})).
3. Choosing all four roots residual gives M_all({z})=4-1[z in Z], because the other three roots never contain spectators.
4. Existing JOINT_RETAINED_RESULT.md at 6454074a95b526bf2125272f76bfad392e2f468f uses CORE-ONLY M_core and explicitly leaves spectator Z hidden. It cannot compute b.
5. Existing POST_A12_RICHER_FACTORIZATION_RESULT.md at eee9eba17ec2f272949051dcd7533e4424ab33f3 deliberately avoids spectator reads for structurally legal repair. That does not supply shortest-path information for C3.
6. Existing PRECEDENCE_INTERFACE_RESULT.md at 00a58b1b3d9d6b1c0c190995a18c5d5e5d19cd40 explicitly forbids choosing a hidden x by a secret full-state read; it is a conditional quotient interface, not an observation oracle.
7. Existing dynamic residual theorem assumes a named active root support for declared edits. It does not derive an autonomous hidden-root support discovery mechanism.
8. Full-palette field's initial values are not proven observer-accessible; a mathematical function of full supports is not a retained native measurement mechanism.

Rejecting control: Z empty and Z={z} have identical core R/M_core and floors2 but different full M_R({z}). No inference of b from core-only data is possible.

Scientific status: conditional mathematical derivation of b from an EXISTING full-palette field, with unresolved initialization/observer-access gate. Not a complete native observer bridge, not a universal impossibility theorem, not physical forces.
