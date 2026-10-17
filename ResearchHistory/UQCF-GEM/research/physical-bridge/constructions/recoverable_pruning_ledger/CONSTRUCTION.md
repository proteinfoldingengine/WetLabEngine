# Construction: recoverable pruning writes an owned ancestor ledger entry

Author: proteinfolding-grokbot (UQCF Science Agent). Started 2026-10-17 America/New_York.
Source baseline: `d90f9a30c006a15cf97257e857a149bbb9423e91`, branch `research/uqcf-overlapping-guard-exchange`.
Mode: CONSTRUCTION MODE (STANDING_DIRECTIVE addendum (b)). Status: ACTIVE POSITIVE CONSTRUCTION, DRAFT 1, UNREVIEWED. No adversarial grading, admission class, code or Gemini review yet; those come after the mechanism is drafted. No milestone or closure is claimed.

## 0. Result first

Read "time is pruning / ordered recoverability update" literally: a pruning step X_{j-1} -> X_j is admissible as an update only if the source grade remains recoverable from what is retained. The inherited split loss sequence (FCV-1 P2) then *forces* the retained structure to carry, at step j, the loss layer

    D_j x = (E_{j-1} - E_j) x .

That layer splits canonically along the fibers of the inherited retraction r_{j-1,j}. Each fiber piece is owned by exactly one retained atom, the longest retained prefix of the atoms removed under it. So one pruning step, the same step in both preparations, writes a new entry into a retained ancestor's own record. The entry carries the removed fine grades below that ancestor.

In the witness below, the receiver a starts with an identical record in both preparations. After any pruning step that removes its descendant u, it holds the entry (j, u, x_u), with x_u = g in one preparation and x_u = h != g in the other. The receiver goes from 0 to 1 bit about the preparation (balanced prior). The joint retained structure (retained state plus full ledger) is in bijection with x before and after, so no information is created globally. Information is *redistributed*: the distinction that sat on u's own coordinate is now owned by a. The step is the ledger point of addendum (b), made concrete with inherited maps.

This is offered as the positive answer to the 2026-10-17 priority addendum: an inherited native operation (pruning under the ordered recoverability update) that itself writes a retained record. It also supplies the emission law P_emit that my append-only provenance screen (73d78836) found missing, conditionally on the bridge premises in section 6.

## 1. Earned ingredients used (inherited, not re-proved)

All in `foundational-closure-verification/PROOFS.md` (blob `a21acad73c80cb748f2e42c244f6db53146c2bf2`) and `TYPE_LEDGER.md` (blob `aa2d66adbfd552188dd3dec9270824fd605981d8`):

- Finite prefix-closed carriers X_0 ⊇ X_1 ⊇ ... with one Genesis root; r_XY(x) = longest prefix of x in Y; r_YZ r_XY = r_XZ (P1).
- Fiber pushforward P_XY of finitely additive grades; total grade preserved; disjoint fiber identity under composition (P1).
- Retention section I_YX (zero extension), P_XY I_YX = id (P2).
- Cumulative E_j = I_{0j} P_{0j}, E_i E_j = E_j E_i = E_j for i <= j; D_j = E_{j-1} - E_j idempotent, D_i D_j = 0 for i != j, im D_j = I_{0,j-1}(ker P_{j-1,j}), and the telescoping identity (P2).
- Implementations: `demos/v15.56-response-selector-obstruction/pruning_morphism.py` (blob `2540fd6f`) and `source_pushforward.py` (blob `0219c09b`).

Nothing below adds a channel, gate, copy, coupling, metric, clock or response kernel.

## 2. The ordered recoverability update as a split, and what it retains

For x in F_{X_0} and any finite pruning sequence X_0 ⊇ ... ⊇ X_m, P2 gives the exact decomposition

    x = E_m x + sum_{l=1..m} D_l x ,                         (2.1)

with the m+1 pieces in mutually complementary images. So x is recoverable from the ordered tuple

    Λ_m(x) = (E_m x ; D_1 x, D_2 x, ..., D_m x) .            (2.2)

Map (2.1) inverts (2.2), and the map x -> Λ_m(x) is linear and injective. **Strongest reading (premise R, section 6):** the ordered recoverability update *is* the replacement of x by Λ_j(x) at step j. The coarse retained state E_j x (equivalently P_{0j} x on X_j) is the part GPT's ancestral-grade note studies. The loss layers are the part that pruning alone would discard, and that recoverability keeps. The index l is the pruning order, which is the ordering of the update and not a duration.

Under R, step j does more than coarsen. It appends one new component D_j x to the retained tuple, and the earlier components are untouched: D_j D_l = 0 for l != j, and E_j D_l = 0 for l <= j (because E_j E_{l-1} = E_j E_l = E_j). The ledger is append-only *as a consequence of P2*, not by fiat.

## 3. Canonical ownership of a loss layer

Fix step j and write r = r_{j-1,j} : X_{j-1} -> X_j, y = P_{0,j-1} x on X_{j-1}. For each retained atom t in X_j let Φ_t = r^{-1}(t) ⊆ X_{j-1}; the fibers partition X_{j-1}, and t ∈ Φ_t.

**Lemma 3.1 (layer formula).** Read in X_{j-1} coordinates, D_j x = y - I P y (with P = P_{j-1,j}, I = I_{j-1,j}). Explicitly, for z in X_{j-1}:

    (D_j x)_z = y_z                          if z ∉ X_j (removed),
    (D_j x)_t = - sum_{z ∈ Φ_t, z != t} y_z  if t ∈ X_j.

*Proof.* E_{j-1} - E_j = I_{0,j-1}(id - I P) P_{0,j-1}. This uses I_{0j} = I_{0,j-1} I and P_{0j} = P P_{0,j-1} (P1, composition of retractions and of zero extensions). Then (I P y)_t = sum_{z ∈ Φ_t} y_z on retained t and 0 on removed z. ∎

**Lemma 3.2 (fiber pieces).** Write D_j x = sum_{t ∈ X_j} π_t, where π_t is the restriction of D_j x to Φ_t. Then each π_t is supported in Φ_t, has total grade 0, and lies in ker P. π_t = 0 iff every removed z in Φ_t has y_z = 0, and in particular whenever Φ_t = {t}. π_t is determined by, and determines, the tuple (y_z)_{z ∈ Φ_t \ {t}}.

*Proof.* Lemma 3.1 plus the fact that the fibers partition X_{j-1}. Each piece sums to zero by construction, so P π_t = 0. ∎

**Ownership.** Assign π_t to t. Under the locality premise L (section 6), whatever is retained about an atom is indexed by the retained address its lineage now lives at, namely r(z). Then the assignment is *forced*: π_t is the unique decomposition of D_j x into pieces each supported inside a single fiber and indexed by that fiber's retained atom. The owner is selected by the inherited retraction, not by the construction. Coarser keyings, such as keying all loss to the Genesis root, are excluded because a piece would then be supported outside its owner's fiber.

**Persistence and inheritance (from P1).** If t survives later steps, π_t is untouched, by section 2. If t is itself removed at a later step k, the canonical re-keying of its entries is r_{j,k}(t). The disjoint fiber identity of P1 shows the fibers of r_{j-1,k} are unions of the fibers of r_{j-1,j}, so the ownership of a recorded piece moves up the lineage to the longest retained prefix and never splits. A record is lost from every owner only if the Genesis root is pruned, which is excluded.

## 4. The derived transfer (witness)

Carrier X_0 = {o, a, b, u, w}, with o = (), a = (0), b = (1), u = (0,0), w = (1,0). Retained references o, a, b are identical in both preparations; there is no cross-Genesis identification.

| atom | x^(0) | x^(1) |
| --- | --- | --- |
| o | c | c |
| a | 0 | 0 |
| b | 0 | 0 |
| u | g | h |
| w | h | g |

c > 0, g, h > 0 and g != h, in relative units (the declared graded instance; same convention as `constructive_candidates/ancestral_grade_transfer/WORKING_NOTE.md`, credit proteinfolding-gpt). Both preparations have the same total and the same literal restriction (c,0,0) to {o,a,b}.

**Receiver.** The retained atom a, with record R_a = (own coarse grade, owned ledger pieces). Initially R_a^(s) = (0, ∅) for s = 0, 1, identical.

**Update.** One pruning step X_0 -> X_1 = X_0 \ D, with D ∋ u and a ∈ X_1. The same D in both preparations, so no source-informed selection.

**Consequence (Lemma 3.1).** π_a = x_u (e_u - e_a). So after the step

    R_a^(0) = (g, [(1, u, g)]),    R_a^(1) = (h, [(1, u, h)]),

and they differ. Both the coarse coordinate and the owned entry separate the preparations. The entry additionally carries the removed address u, the step index, and the sum-zero dipole form that certifies it as relocated rather than created grade.

If D = {w} only, a's record is unchanged and the distinction is written to b instead: π_b = x_w (e_w - e_b). Every proper D writes a separating entry to at least one retained owner among {a, b}. Which owner gets it is left unresolved, as addendum (b) allows.

**Information bookkeeping (balanced prior on s).**
- Receiver: I(S; R_a) goes from 0 before to 1 bit after any step with u ∈ D.
- Global: Λ_1 is injective (section 2), so I(S; Λ_1(x)) = I(S; x) = I(S; Λ_0(x)). Total grade is preserved, and every π_t has total 0.
- The change is a relocation of an existing distinction. It moves from the unowned coordinate x_u, an atom that is no longer retained, into an entry owned by the retained atom a. Nothing is created globally. This is the ledger correction's possibility (`admission_decisions/2026-10-17-ledger-screen-scope-correction.md`, section 1) realized by inherited maps instead of a supplied entry E = S.

**Occurrence.** A nonempty owned entry is itself a witness that a pruning touching a's fiber occurred, with its order index. No external acknowledgment, event counter or completion flag is used. No probability that u is pruned is derived. All statements are conditional on the step, and they hold pointwise for any distribution over steps with u ∈ D.

## 5. Mission ledger: earned vs assumed

| Mission ingredient | Status in this draft |
| --- | --- |
| Native distinction | Fine descendant grade relative to shared retained references. It is a declared instance of the inherited graded model, and preparability is ASSUMED (premise G). |
| Justified update rule | Pruning plus the P2 split. The maps are EARNED. Reading the time axiom as "retain Λ_j" is premise R. |
| Retained consequence | Owned fiber piece π_a, which is append-only and persists and inherits up the lineage. This is EARNED given R and L. |
| Identifiable receiver with access | Retained atom a. The owner is selected by the inherited retraction, given L. Access means the owner reads its own record, which is definitional once L holds (premise A). |
| Separation of preparations | g != h, with the same carrier, references, total and retained restriction. Separation is EARNED. |

## 6. Bridge premises (stated, not hidden)

- **R (recoverability reading).** An admissible pruning step keeps x recoverable, i.e. it retains Λ_j(x) and not just E_j x. This is the strongest literal reading of "ordered recoverability update". Next task: pin it to an inherited text (the v13.21 recoverability atlas, the Genesis Pin "recoverable-history legitimacy" semantics in v15.08, the v15.16 partial-pruning recoverability). Alternatively, show that the weaker reading (discard ker P) contradicts some earned recoverability statement.
- **L (locality of retained indexing).** After step j, every retained datum is indexed by an atom of X_j, and a datum about an atom z is indexed by r(z). Next task: test whether L follows from naturality under the admissible relabelings of P2 together with P1 composition. A first observation is that root-keying also composes, so naturality alone may not force L, and an additional earned "an atom's lineage lives at its retraction" statement is needed.
- **A (access).** A retained atom's record consists of its own coarse coordinate and its owned pieces. Given L this is a definition, not a channel.
- **G (preparability).** Two preparations with unequal positive descendant grades under shared references exist. This is shared with the ancestral-grade note and remains open.

The draft does not assume a copying gate, a supplied entry E = S, a source-dependent pruning choice, a receiver policy or a clock.

## 7. Relation to concurrent constructions (no duplication)

- *Ancestral grade transfer* (proteinfolding-gpt): uses only the coarse E_j x / P x at the receiver, and leaves open whether aggregation is the receiver's accessible state or only a coarse description. Here the coarse state and the fine loss are *both* retained (2.1). That gap is replaced by premises R and L, which are sharper and checkable, and the receiver additionally gets the removed address and an occurrence witness.
- *Source-withdrawal completion* (proteinfolding-gpt): forcing by nested-support compatibility on label incidences, with enactment and access open. Different state variable and different mechanism (forcing rather than redistribution). Not used here.
- *My append-only provenance screen* (73d78836): the ledger there had no native emission. Here emission is the pruning step itself, and the entry content D_j x is derived, not supplied.

## 8. Next construction steps (one per run)

1. Pin or derive premise R from inherited recoverability text, as in section 6.
2. Settle premise L: either derive fiber-locality from P1, P2 and the relabeling naturality, or state the minimal extra earned fact.
3. Generalize the witness: arbitrary finite trees and multi-step sequences. Prove that each owner's ledger reconstructs exactly the fine grades of the removed atoms in its cumulative fiber, which follows by telescoping.
4. Explore the noncommutative analogue: a conditional expectation E with loss layer ρ - E(ρ), keyed by the retained central blocks, as a recoverable-pinching ledger. Check that this is relocation and not cloning.
5. Then freeze, preregister, independent producer and checker code, Gemini review via Actions, audit, readback.
