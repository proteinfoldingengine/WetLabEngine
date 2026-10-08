# C3 safe-probe theorem — closed-world and fixed-root observation clarification

Date: 2026-10-08.
Status: AUTHOR-SIDE CLARIFICATION FOLLOWING GEMINI REVISE; fresh independent review required.
Parent scope COUPLED_C3_SAFE_PROBE_SCOPE.md at d562bd602c2c7f87bface370717ddcfa2a84d0c5.
Parent proof COUPLED_C3_SAFE_PROBE_RESULT.md at 47cdacc799be131d5ae7db73884dcd2823ac3992.
First GitHub Actions bounded controls PASS (8 spectator states, 31 safe prefixes, 4 rejecting controls), run 37846599455. Gemini review REVISE; evidence artifact 11579972976, manifest response SHA256 5e8920141d755ce8a3d327bf028f36621686f9ed139efd7344840b8caf1340ca.

## Explicit closed-world and transcript contract

Between successive declared controller commits, there are NO autonomous spectator updates, hidden external edits, root insertions/deletions, label reassignments, or changes to original floors. The only transitions are exactly the controller's chosen uniformly valid spectator toggles on r4. Every such chosen edit commits exactly once. Its acknowledgement contains only the already-known signed root-label command identity and a constant successful-commit flag; no root cardinality, capacity, state-dependent timing, failure/legality response, hidden occupancy or extra side channel is exposed. The controller's policy, stopping decision and internal state depend only on the common observed transcript and its own random seed, not on the hidden full state.

These are explicit restrictions of the bounded model, NOT native physical laws or proven observer capabilities.

## Exact core-only miss-count definition

Fix the labelled residual-root index family R={r4} at EVERY slice (no dynamic selection of residual slots). Let P0={a,b,c,d,e}. For each nonempty H subseteq P0 with |H|<=4 define
  M_core(H;Z) = sum_{r in R} 1[S_r(Z) intersect H = empty].
Since S_r4(Z)={d,e} union Z and Z subseteq T is disjoint from P0, we have
  S_r4(Z) intersect H = {d,e} intersect H.
Thus
  M_core(H;Z)=1[ {d,e} intersect H = empty ],
independent of Z for EVERY retained H. This is a literal fixed-slot count; no hidden global predicate is allowed to change which roots belong to R. The same independence also holds for any other explicitly fixed set of labelled roots with spectator changes confined to r4, but that extension is not needed here.

The labelled core projections are also fixed, the triangle has hitting number2, the disjoint fourth root contributes1, and all original floors2 remain valid. Hence O_core is invariant under every declared valid spectator toggle.

## Induction and information boundary

For the two initial worlds Z_A=empty and Z_B={u}, the observation transcripts agree initially. At each step a transcript-only policy chooses the same labelled command; uniform validity permits it in both; closed-world semantics guarantee no intervening hidden transition; identical state-independent success records are returned; and the fixed-slot formula proves identical next observations. By induction the entire observable transcript agrees. The exact count offset |Z_B|-|Z_A|=1 persists under identical signed edits, even when the current positivity bits converge.

A command -u with a state-dependent failure response would separate the worlds but violates the uniform-safe guaranteed-commit interface. Full root4 size or initialized full-palette miss counts would also separate and are excluded. This result is limited to the stated model and does not prove a physical observer, force, geometry, energy or fundamental time.

## Audit disposition

This addendum resolves the two stated review ambiguities at the author level; it does NOT itself certify the theorem. Require new GitHub-native bounded controls and independent adversarial Gemini verdict. Preserve earlier REVISE in the evidence ledger.
