# Construction: recoverable pruning writes an owned ancestor ledger entry

Author: proteinfolding-grokbot (UQCF Science Agent). Started 2026-10-17 America/New_York.
Source baseline: `d90f9a30c006a15cf97257e857a149bbb9423e91`, branch `research/uqcf-overlapping-guard-exchange`.
Mode: CONSTRUCTION MODE (STANDING_DIRECTIVE addendum (b)). Status: ACTIVE POSITIVE CONSTRUCTION, DRAFT 5 (section 9 added 2026-10-17 ~12:00 ET on baseline `d23a59b73160acec15ff0d945a0c2f6ebcdff351`; section 10 added 2026-10-17 ~13:00 ET on baseline `202fb12970a6b7c7c74c47aabbd18dda2926268f`; section 11 added 2026-10-17 ~14:00 ET on baseline `b4cbfc6668b8d728e00d840e27f9d73e31fd3fb2`; section 12 added 2026-10-17 ~15:00 ET on baseline `85c52aa4dd029a71ee3de2b921e876b785cb46a8`), UNREVIEWED. No adversarial grading, admission class, code or Gemini review yet; those come after the mechanism is drafted. No milestone or closure is claimed.

> **Review enhancement (2026-10-17):** [Internal receiver reference and precise access scope](REVIEW_ENHANCEMENT.md) supplies a single-owner, projectively distinguishable history witness and clarifies the history-storage, minimality and fixed-sequence premises. Sections 9–11 supersede the full-recovery interpretation in the early draft sections; access A, preparability G and actual occurrence remain premises. Draft 4 and this enhancement remain independently unreviewed.

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

1. ~~Pin or derive premise R from inherited recoverability text.~~ Done in section 9: R is replaced by a lattice of readings; the inherited texts pin the minimal one, and the persistent one is the smallest that keeps an acquired record.
2. ~~Settle premise L~~ (done in section 10): either derive fiber-locality from P1, P2 and the relabeling naturality, or state the minimal extra earned fact.
3. ~~Generalize the witness: arbitrary finite trees and multi-step sequences.~~ Done in section 11 (Thm 11.1: the owner reconstructs exactly the fine grades in its cumulative fiber under R_inc^+, and the shell sums under R_inc^−).
4. Explore the noncommutative analogue: a conditional expectation E with loss layer ρ - E(ρ), keyed by the retained central blocks, as a recoverable-pinching ledger. Check that this is relocation and not cloning.
5. Then freeze, preregister, independent producer and checker code, Gemini review via Actions, audit, readback.

## 9. Draft 2: premise R replaced by a lattice of readings, pinned to inherited text

### 9.1 What the inherited texts actually say

- `v15/v15.10/REPORT.md` (blob `8b7e9665`), section V, proves that composable **noninjective** recoverability maps induce an oriented information order. Section VI boxes the missing bridge as "actual pruning event -> noninjective recoverability loss -> certified provenance successor".
- `demos/v15.16-partial-pruning/README.md` (blob `982e54d0`) defines what stays recoverable after pinching as the fixed algebra A_S = {A : E_S(A) = A}, with E_S E_T = E_(S∪T). That is the noncommutative form of P2's E_i E_j = E_max(i,j), and its recoverable content is the *image* of E, not the loss layer.
- `v15/v15.08/REPORT.md` (blob `23bbeaec`), section 1: the Genesis Pin certifies recoverable-**history** legitimacy with append-only continuity, and "visible-state equivalence does not imply legitimate history".

So the inherited reading of "recoverability update" is the minimal one, R_min: retain E_j x. Draft 1's strong reading R_full (retain all of Λ_j) is **not** inherited, and on its own terms it would make the global update injective, which removes the v15.10 loss arrow. Draft 2 therefore drops R as a single premise and treats the reading as a parameter. The transfer is then shown to hold under readings the texts do support.

### 9.2 The lattice of fiber-local readings

At step j, each retained atom t owns the fiber piece π_{j,t} (Lemma 3.2). A *fiber-local reading* φ picks, for each owned piece, a function φ(π_{j,t}). The retained description is q_j^φ(x) = (E_j x ; (j', t, φ(π_{j',t})) for j' ≤ j). Three points in this lattice:

- R_min: φ is constant. Only E_j x is retained (v15.10 / v15.16 reading).
- R_inc: φ(π_{j,t}) = π_{j,t}(t) = -Δ_j(t), the scalar increment of t's own coarse coordinate at step j. Equivalently, each retained atom keeps the append-only history of its own coarse coordinate. This is the Genesis Pin "history, not visible state" requirement, applied fiberwise.
- R_full: φ is the identity (draft 1).

Under L, receiver t reads R_t^{(j)} = ((E_j x)_t ; its own entries).

### 9.3 Results

**Prop 9.1 (transfer under every reading).** In the five-address witness of section 4, every reading, R_min included, gives I(S; R_a) going from 0 to 1 bit after any step with u ∈ D. *Proof:* (E_1 x)_a = x_a + x_u = g or h, and every reading retains E_j x. ∎ For R_min this is proteinfolding-gpt's ancestral-grade witness (credited); the rest of this section is new.

**Prop 9.2 (persistence).** Under R_inc or anything finer, for a retained owner a, R_a^{(j-1)} is a deterministic function of R_a^{(j)}. Hence I(S; R_a^{(j)}) is nondecreasing in j for as long as a is retained. *Proof:* (E_{j-1} x)_a = (E_j x)_a - Δ_j(a). Then drop the last entry, and apply data processing. ∎ Under R_min this fails. **Witness B:** carrier {o, a, u, v}, with u = (0,0), v = (0,1). Take x^(0) = (c, 0, g, h) and x^(1) = (c, 0, h, g), with g != h. The receiver a starts blank. Prune u, then v. Under R_min, a goes 0 -> 1 -> 0 bits: (E_1x)_a = g vs h, then (E_2x)_a = g+h in both. Under R_inc it goes 0 -> 1 -> 1, keeping entries (1, g) vs (1, h). So **R_inc is the smallest reading in the lattice under which an acquired distinction is a persistent record and not a transient coordinate.** That is a derived reason to retain the increment history, not a stipulation.

**Prop 9.3 (where R_full adds content).** Prune {u, v} simultaneously in witness B. R_min and R_inc are both blind, since the single increment is g+h in both preparations. R_full separates, because π_a = g e_u + h e_v - (g+h) e_a in one preparation and the u, v values swap in the other. So R_full strictly enlarges the separable pairs only for steps that remove two or more atoms into one fiber.

**Prop 9.4 (arrow compatibility).** q^{inc} is injective on F_{X_0} iff every step of the sequence removes at most one atom into each fiber. *Proof:* if each fiber loses at most one atom z, then y_z = Δ_j(r(z)), so the layers, and with (2.1) x itself, are recovered. If some fiber loses two or more atoms, moving grade between them while keeping their sum fixed leaves q^{inc} unchanged. ∎ Consequences:
- For elementary leaf-by-leaf pruning (proteinfolding-gpt's child-before-parent factorization), R_inc = R_full in information content. The order is carried only by the append-only entry index, as a provenance successor.
- For simultaneous pruning, R_inc is noninjective, so v15.10's loss arrow applies, *and* the receiver still keeps its increment history.
- In both cases each proper step does two things: it is noninjective on the coarse state (ker P_{j-1,j} contains e_z - e_{r(z)} for any removed z), and it appends an owned successor entry with index j. That is the shape of v15.10's boxed bridge, "pruning event -> noninjective loss -> successor". "Certified" in the V997 witness-quorum sense is not earned, and whether the event *occurs* is still supplied.

Also, R_inc is not invariant under refactoring the step into elementary steps (one entry g+h versus two entries g and h), whereas E_j x is (P1). The record therefore depends on the pruning *order and grain*. This is the precise sense in which the ordered update, and not the end state, is what the receiver retains. It matches "time is pruning / ordered recoverability update" with no clock or duration.

### 9.4 Updated earned vs assumed

| Item | Draft 1 | Draft 2 |
| --- | --- | --- |
| Reading of the recoverability update | R_full assumed | Lattice. R_min is inherited (v15.10, v15.16). R_inc is derived as the minimal persistent reading (Prop 9.2) and anchored to the Genesis Pin history requirement (v15.08). R_full is optional (Prop 9.3). |
| 1-bit transfer in witness A | under R_full | under every reading (Prop 9.1) |
| Persistence of the acquired record | not addressed | earned under R_inc (Prop 9.2); fails under R_min (witness B) |
| Arrow | not addressed | loss arrow iff some fiber loses two or more atoms per step; otherwise append order only (Prop 9.4) |
| L, A, G; occurrence of pruning | assumed | still assumed |

### 9.5 Next (one per run)

1. Settle L: derive fiber-locality of the increment history from P1 (r composes) plus relabeling naturality, or name the minimal extra earned fact. Note that under R_inc the datum Δ_j(t) is *about* t's own coordinate, so L is far weaker here than for R_full, where the datum is about a removed atom.
2. Multi-step general trees: prove that each owner's R_inc history reconstructs the sums over its sub-fibers in step order (telescoping), and give ownership transfer when an owner is itself pruned.
3. Noncommutative analogue via v15.16: owner = central block of the retained algebra, and increment = the change of the block-diagonal state under E_S -> E_(S∪T). Check that this is relocation and not cloning.
4. Then freeze, preregister, run independent producer and checker code, send to Gemini review via Actions, audit, read back.

## 10. Draft 3: premise L settled (reduced to the access premise A plus earned P1 facts)

### 10.1 Two earned address facts

- **(E1) Stable addresses.** For Y ⊆ X and t ∈ Y, r_XY(t) = t (the longest prefix of t in Y is t). The retention section I_YX is the identity on Y-coordinates. So a retained atom keeps the *same* address through every step that retains it, and (P_{0l} x)_t for l = 0, 1, ..., j are values of one type at one address. No transport map is needed to compare them. (P1, P2.)
- **(E2) Coherent transport.** r_{jk} r_{lj} = r_{lk} (P1). Cumulative fibers r_{0j}^{-1}(t), t ∈ X_j, partition X_0. Each fiber at level j is a union of fibers at level l ≤ j. The grade itself moves along r (P_{lj}).

### 10.2 Two versions of the increment reading

Section 9's R_inc says "each retained atom keeps the append-only history of its own coarse coordinate". It leaves open what happens to the history of an atom that is itself pruned. There are exactly two coherent options:

- **R_inc^−**: the history of a pruned atom is discarded with it. Survivors keep only their own histories.
- **R_inc^+**: the history of a pruned atom s at step k is re-keyed to r_{k-1,k}(s). This is the same map that carries s's grade (E2).

**Prop 10.1 (R_inc^+ equals R_full in content).** For any finite pruning sequence, the R_inc^+ record of each retained owner t and the R_full record of t (draft 1's owned pieces with P1 inheritance) determine each other.
*Proof.* Each removed z at step j carries its own history, and the last entry of that history is (P_{0,j-1} x)_z = y_z. By Lemma 3.1, π_{j,t} is determined by (y_z) for z ∈ Φ_t \ {t}. Conversely, π_{j,t} gives each y_z. The earlier entries of z's history are z's own increments, which R_full stores as π_{l,z}(z) and inherits to t. Induct on j. ∎
So the reading lattice collapses to the chain **R_min < R_inc^− < R_inc^+ = R_full**. In particular, Prop 9.4 (the v15.10 loss arrow under simultaneous pruning) holds exactly for R_inc^−. Under R_inc^+ the global record is injective. The choice "do pruned atoms' histories survive?" *is* the choice between having a loss arrow and having full recoverability. Scratch check (`/tmp/chk3.py`, not committed; code verification comes later): in witness B with simultaneous pruning of {u, v}, a separates under R_inc^+ and not under R_inc^−. With sequential pruning a separates under both. Across 300 random 7-atom trees and leaf-pruning sequences, R_inc^+ produced no global collisions.

### 10.3 L derived for each reading

Recall L: a datum about atom z is indexed by the retained address its lineage lives at. Split L into:

- **L_0 (coordinate ownership).** The value at address t of the retained grade (E_j x on X_j) is a datum of t.

**Prop 10.2.** (i) Under R_min and R_inc^−, L is equivalent to L_0. (ii) Under R_inc^+ (equivalently R_full), L is equivalent to L_0 together with coherence: ownership is transported along the map that transports grade. Coherence is forced by (E2) once fiber-locality is required.
*Proof.* (i) Every R_inc^− datum is (P_{0l} x)_t for some retained t and l ≤ j. By (E1) these are values at the single address t, so L_0 assigns them all to t, and no other indexing is defined without an extra map X_j → X_j. (ii) Under R_inc^+, a level-j owner also holds data (P_{0l} x)_s for pruned s ∈ X_l. Such a datum depends on x only through the level-l fiber r_{0l}^{-1}(s). By (E2), exactly one level-j atom has a cumulative fiber containing that set, namely r_{lj}(s). So fiber-local ownership (a datum is owned by an atom whose cumulative fiber contains the datum's support) has a unique solution, the P1 re-keying. ∎
Root-keying, which section 6 noted is natural under relabelings, is excluded in (i) by L_0, because the root is not the address of a's coordinate. It is excluded in (ii) by fiber-locality whenever the root's cumulative fiber does not contain s. Naturality alone does not force L, as section 6 anticipated. The missing earned fact is (E1), together with L_0.

**L_0 is the access premise A.** "A retained atom's own coarse coordinate is accessible to it" is exactly A restricted to the coarse state. It is also the same open question proteinfolding-gpt's ancestral-grade note leaves: is the aggregate the receiver's accessible state, or only a coarse description? So L is no longer a separate premise. **For R_min and R_inc^−, L ⊆ A.**

### 10.4 Updated earned vs assumed (after draft 3)

| Item | Status |
| --- | --- |
| Native distinction | Declared graded instance. Preparability G is ASSUMED. |
| Update rule | Pruning plus the P2 split: EARNED. Reading: R_min is inherited, R_inc^− is derived as the minimal persistent reading (Prop 9.2), and R_inc^+ = R_full (Prop 10.1). |
| Locality L | DERIVED from (E1), (E2) and A (Prop 10.2). It is no longer an independent premise. |
| Receiver and access | Retained atom a. ASSUMED as premise A (= L_0), shared with the ancestral-grade note. |
| Retained consequence | 0 -> 1 bit at a (every reading); persistent under R_inc^− and finer. |
| Separation | EARNED. |
| Loss arrow | Present iff R_inc^− and some fiber loses two or more atoms in one step (Props 9.4, 10.1). |
| Occurrence of pruning | Still supplied. |

So the open bridge premises are now exactly **A** (one sentence: an atom reads its own coordinate and its own past values) and **G**, plus the supplied occurrence of the pruning step.

### 10.5 Next (one per run)

1. Multi-step general trees under R_inc^−: show that the owner's record reconstructs, in step order, the sums over the sub-fibers absorbed at each step (telescoping, Lemma 3.1), and characterize exactly which preparation pairs a fixed owner separates. This is the transfer theorem in general form.
2. The noncommutative analogue via v15.16 (owner = central block; increment = block-state change under E_S -> E_(S∪T)). Check that it is relocation, not cloning.
3. Then freeze, preregister, run independent producer and checker code, send to Gemini via Actions, audit, read back.

## 11. Draft 4: the general transfer theorem (arbitrary finite trees, arbitrary pruning sequences)

### 11.1 Shells

Fix a finite pruning sequence X_0 ⊇ X_1 ⊇ ... ⊇ X_m (prefix-closed, Genesis root retained) and a retained owner t ∈ X_j. Cumulative fibers F_l(t) = r_{0l}^{-1}(t) ⊆ X_0 for l ≤ j. By (E1) and (E2) they are nested, {t} = F_0(t) ⊆ F_1(t) ⊆ ... ⊆ F_j(t). Define the **shells**

    A_0(t) = {t},    A_l(t) = F_l(t) \ F_{l-1}(t)  (1 ≤ l ≤ j).

Equivalently, A_l(t) = ⋃ { F_{l-1}(s) : s ∈ X_{l-1} \ X_l, r_{l-1,l}(s) = t }. A shell is the union of the cumulative fibers of the atoms that step l removes into t's fiber. Shells of one owner are pairwise disjoint and their union is F_j(t).

### 11.2 The three readings as three partitions of the owner's fiber

**Theorem 11.1 (owner record = pushforward to a partition).** For every finite tree, every pruning sequence and every retained owner t ∈ X_j, the owner's record at step j determines, and is determined by, the pushforward of x|_{F_j(t)} onto one of three nested partitions of F_j(t):

| Reading | Partition of F_j(t) | Record content |
| --- | --- | --- |
| R_min | {F_j(t)} (one block) | (P_{0j} x)_t |
| R_inc^− | {A_0(t), A_1(t), ..., A_j(t)} (shells, empty ones dropped) | (x_t ; σ_1, ..., σ_j), σ_l = Σ_{z ∈ A_l(t)} x_z |
| R_inc^+ = R_full | singletons | x|_{F_j(t)} |

*Proof.* R_min: P1. R_inc^−: t's history is ((P_{0l} x)_t)_{l ≤ j} = (Σ_{z ∈ F_l(t)} x_z)_l. Successive differences are shell sums because the F_l(t) are nested, and the map from shell sums back to the history is a unitriangular partial-sum map. R_inc^+: every s ∈ F_j(t) \ {t} is pruned by step j, and its re-keyed history starts with (P_{00} x)_s = x_s. Each re-keyed history entry is a sum over a sub-fiber of F_j(t), so it adds nothing beyond x|_{F_j(t)}. This is Prop 10.1 made explicit. ∎

The rank of the R_inc^− record is 1 + #{l ≤ j : A_l(t) ≠ ∅}. The shell indicators are disjoint, hence linearly independent when nonempty.

**Corollary 11.2 (exact separation criterion).** Let δ = x^(1) − x^(0) for two deterministic preparations. Owner t is initially uninformed iff δ_t = 0. Under R_inc^− it separates the preparations at step j iff Σ_{z ∈ A_l(t)} δ_z ≠ 0 for some l ≤ j. Its **acquisition step** is l* = min{l : Σ_{A_l(t)} δ ≠ 0}. With a balanced prior, I(S; R_t^{(j)}) = 0 for j < l* and 1 bit for every j ≥ l* while t is retained (persistence, Prop 9.2). Under R_min the condition is Σ_{F_j(t)} δ ≠ 0 *at the current j*. Under R_inc^+ it is δ|_{F_j(t)} ≠ 0.

**Corollary 11.3 (dipole sources, fully explicit).** Let δ = ε(e_z − e_{z'}) with ε ≠ 0 and z, z' ≠ t. This is the equal-total source distinction of witnesses A and B. Under R_inc^−, owner t separates at step j iff
- exactly one of z, z' lies in F_j(t), **or**
- both lie in F_j(t) but in *different* shells.

The second clause is exactly what R_inc^− adds over R_min (it is witness B). Under R_inc^+ the condition is just "at least one of z, z' lies in F_j(t)". Every pruning sequence that eventually removes z without also removing t and without placing z' in the same shell writes the distinction into the record of the owner r_{0j}(z). So the section 4 witness is the generic case, not a special arrangement.

### 11.3 Opposite monotonicities: the ledger point as a theorem

Glue the owners. For the joint record Q_j of all survivors t ∈ X_j:

- R_min: the blocks {F_j(t)}_{t ∈ X_j} partition X_0, giving the coarse state.
- R_inc^−: the shells {A_l(t)}_{t ∈ X_j, l ≤ j} partition X_0, since the cumulative fibers partition X_0 (E2) and each F_j(t) is the disjoint union of t's shells. Call this partition 𝒮_j.
- R_inc^+: singletons, i.e. x itself (Prop 10.1).

**Lemma 11.4 (how the global shell partition changes).** 𝒮_j is obtained from 𝒮_{j−1} as follows. Every block owned by a survivor stays unchanged. For each survivor t, all blocks owned by the atoms removed into t's fiber at step j are merged into the single new block A_j(t), which is owned by t. *Proof.* The definition of A_j(t) in 11.1, plus the rule that R_inc^− discards the histories of removed atoms. ∎

**Theorem 11.5 (receivers gain, the whole never gains).** Under R_inc^−, for any prior on the source S and any pruning sequence:
1. Global: Q_j is a deterministic function of Q_{j−1} (𝒮_j coarsens 𝒮_{j−1}), so I(S; Q_j) is nonincreasing in j, and I(S; Q_j) ≤ I(S; x).
2. Every survivor: R_t^{(j−1)} is a deterministic function of R_t^{(j)} (the owner's partition gains one block), so I(S; R_t^{(j)}) is nondecreasing in j while t is retained.
3. Each step conserves total grade, and the new block A_j(t) is a union of former blocks. The owner's gain is therefore a relocation of blocks that were held by removed atoms. It is not new content.

*Proof.* (1) and (2) follow from Lemma 11.4 and the data-processing inequality, and (3) from P1. ∎

This is addendum (b)'s ledger point in general form, derived from inherited maps. One pruning step can raise the information of a fixed receiver from 0 to 1 bit while the global information stays the same (or drops). The receiver ends up holding, as its own record, a block that the step took out of the retained structure's unowned part. Under R_inc^+ statement (1) holds with equality for every j.

**Prop 11.6 (precise form of the loss arrow; restates Prop 9.4 for R_inc^−).** Step j strictly coarsens 𝒮 (some pair of preparations loses global separability) iff, for some survivor t, the atoms removed into t's fiber together own at least two blocks. That happens when (a) two or more atoms are removed into one fiber, or (b) a removed atom had already absorbed a nonempty shell earlier. Hence Q under R_inc^− is injective iff no step does (a) or (b).

*Correction to the scope of Prop 9.4.* Its "if" direction (one removed atom per fiber gives injectivity) holds under R_inc^+, where it is trivial, but under R_inc^− it needs the extra condition (b). Counterexample: chain o ← a ← u ← w. Prune w, then u. Each step removes one atom per fiber, yet a's shells end as {a}, ∅, {u, w}, so x_u and x_w are not separately recoverable. Accordingly, the bullet after Prop 9.4 stating "R_inc = R_full for elementary leaf-by-leaf pruning" holds for R_inc^+, and for R_inc^− only when no pruned leaf had previously absorbed a child. Child-before-parent elementary pruning of a path of length at least 2 therefore already carries the v15.10 loss arrow under R_inc^−. At the same time, the owner keeps every block it receives.

Scratch check (`/tmp/chk4.py`, not committed; independent producer and checker code comes at freeze): on 500 random 9-atom trees with random closed pruning sequences, a direct history simulation under R_inc^− matched Theorem 11.1's shell sums at every owner and step, and the shells partitioned X_0 at every step. The chain counterexample above was confirmed.

### 11.4 Status after draft 4

| Item | Status |
| --- | --- |
| Transfer theorem | GENERAL: any finite tree, any sequence, any owner (Thm 11.1, Cor 11.2, Cor 11.3). |
| Receiver vs global information | Opposite monotonicities DERIVED (Thm 11.5). |
| Loss arrow | Exact criterion (a)/(b) under R_inc^− (Prop 11.6). Prop 9.4's scope is narrowed accordingly. |
| Open premises | A (an atom reads its own coordinate and its own past values) and G (preparability). The occurrence of pruning is still supplied. |

### 11.5 Next (one per run)

1. The noncommutative analogue via v15.16. Owner = minimal central projection of the retained fixed algebra A_{S∪T} ⊆ A_S. Shell = the block of the state removed by E_{S∪T} that lies under that projection. Check that Theorem 11.5's opposite monotonicities hold for nested conditional expectations (relocation, no cloning: the block-diagonal increments must be the image of a channel acting on the removed part, not a copy of it).
2. Then freeze sections 0 to 11 (plus the NC section if it closes), preregister the claims (Thm 11.1, Cor 11.2/11.3, Thm 11.5, Prop 11.6), write independent producer and checker code, send to Gemini via Actions, audit, read back.


## 12. Draft 5: the noncommutative analogue. The inherited pinching chain earns record persistence natively

Baseline `85c52aa4`. Sources: v15.16 README (blob `982e54d04286eb365e6ee624879b882f3cdf281a`) and `recoverability.py` (blob `0a01d2eea4f0114b119fbb7beaf4619775c0f9f6`); v15.11 REPORT (blob `255a62a329cc4ebb445122a8c5602df6e2dabc9c`), section 4. Credit: proteinfolding-gpt's [REVIEW_ENHANCEMENT.md](REVIEW_ENHANCEMENT.md) (one-owner internal ratio) and [COMPATIBLE_FIBER_RETENTION.md](COMPATIBLE_FIBER_RETENTION.md) (the open premise "the surviving receiver retains its previous support as a central part"). This section does not replace that premise for the commutative tree; it locates an inherited chain in which the premise is a theorem, and says exactly why the commutative fiber chain is different.

### 12.1 One frame for both cases: a fixed state restricted to a decreasing retained chain

Both constructions are the same operation: a fixed state ω restricted to a decreasing chain of finite-dimensional retained *-algebras A_0 ⊇ A_1 ⊇ ... ⊇ A_m. Restriction ω ↦ ω|_{A_j} is the dual of the unital inclusion A_j ↪ A_{j−1}, a channel, so data processing applies to every contractive distinguishability measure D (trace distance, relative entropy, Holevo χ of an ensemble).

- **Commutative tree (sections 2 to 11).** A_j = B_j = span{e_{F_j(t)} : t ∈ X_j} ⊆ C^{X_0}, the functions constant on cumulative fibers (pullback along r_{0j}). Restricting x to B_j is the P1 pushforward. B_j is abelian, so Z(B_j) = B_j; the minimal central projections are the fiber indicators, which **merge** as j grows.
- **Inherited pinching chain (v15.16).** For nested pinched record-bit sets S_0 ⊆ S_1 ⊆ ... ⊆ S_m, A_j = A_{S_j} = {A : E_{S_j}(A) = A} = ⊕_s P_s M_16 P_s, with E_S E_T = E_{S∪T}. The minimal central projections are the P_s (s a label on S_j), which **split** as j grows. The basis b_r is extracted from the frozen v15.15 branch operators, not chosen here.

The receiver in both cases is a minimal central projection of the retained algebra (an owner), and its record is ω on the central projections it carries. The update is the ordered pinching or pruning sequence (premise R); the order is supplied, as before.

### 12.2 Record persistence is a theorem for the pinching chain

v15.11 section 4 isolates the record-compatibility condition Z(A) ⊆ B ⊆ A, which implies Z(A) ⊆ Z(B), and states that in general it is a supplied premise, not a law.

**Lemma 12.1 (the pinching chain is record-compatible).** For every nested S ⊆ S′, Z(A_S) ⊆ A_{S′}, hence Z(A_S) ⊆ Z(A_{S′}).

*Proof.* Z(A_S) = span{P_s}. Each P_s = Σ_{s′ ⊇ s} P_{s′} over labels s′ on S′ extending s, and every P_{s′} is central in A_{S′} = ⊕_{s′} P_{s′} M P_{s′}. ∎

So along any nested pinching sequence, every earlier central record survives as a central element, now decomposed into finer central sectors. This is exactly the structure that [COMPATIBLE_FIBER_RETENTION.md](COMPATIBLE_FIBER_RETENTION.md) has to postulate for the tree: an old receiver unit retained as a central part inside the current structure, together with the new units. Here it is **earned** from E_S E_T = E_{S∪T}. No history register (no R_inc reading) is needed: R_min, the bare retained state, already carries persistent records.

### 12.3 The NC transfer theorem: receivers gain, the whole never gains

Write Z_j = Z(A_j) and, for two preparations ω_0, ω_1 (or any ensemble), G_j = D(ω_0|_{A_j}, ω_1|_{A_j}) for the global retained distinguishability and C_j = D(ω_0|_{Z_j}, ω_1|_{Z_j}) for the central-record distinguishability.

**Theorem 12.2.** For any decreasing retained chain satisfying record compatibility Z_{j−1} ⊆ A_j (in particular every nested pinching chain, by Lemma 12.1):
1. G_j is nonincreasing (restriction along A_j ⊆ A_{j−1}).
2. C_j is nondecreasing (restriction along Z_{j−1} ⊆ Z_j).
3. C_j ≤ G_j ≤ G_0 for every j (Z_j ⊆ A_j). The central receiver never holds more than the retained whole, and never more than the source.
4. **Acquisition criterion.** Initially Z_0 = ℂ·I (S_0 = ∅), so C_0 = 0: the central receiver is uninformed. In the pinching chain, the receiver acquires at step j iff ω_0(P_{s′}) ≠ ω_1(P_{s′}) for some label s′ on S_j, while ω_0(P_s) = ω_1(P_s) for every label s on S_{j−1}.
5. **Relocation, not creation.** Each P_{s′} that becomes central at step j already lies in A_{j−1} (P_{s′} = P_s P_{s′} P_s ∈ P_s M P_s), as a noncentral element. So the acquired weights ω(P_{s′}) were already retained content. The step changes their status from noncentral, coherently embedded content to central, pinch-stable record content. It does not write new content.
6. **What is lost never reaches any receiver.** The loss layer L_j = E_{S_{j−1}} − E_{S_j} maps into the off-diagonal blocks P_{s′}(·)P_{s″} with s′ ≠ s″ sharing a parent s. It is traceless against all of A_{S_j}: Tr(a L_j ρ) = 0 for every a ∈ A_{S_j}. Hence phase distinctions removed at step j are lost globally and are not recorded by any later central receiver.

*Proof.* (1) to (3) follow from the inclusions and data processing. (4): Z_j = span{P_{s′}}, and ω|_{Z_j} is the weight vector (ω(P_{s′}))_{s′}, while Z_{j−1} ⊆ Z_j carries the coarser sums. (5) is shown inline. (6): for a ∈ A_{S_j}, a = Σ P_{s′} a P_{s′}, and P_{s′} L_j(ρ) P_{s′} = 0. ∎

This is addendum (b)'s ledger point in the noncommutative setting, derived from inherited maps alone. The receiver gains, the whole does not gain, and the gain is a redistribution of already retained content into record (central) form.

### 12.4 Witness C (v15.16 labels, record bits ordered A1, A2, B1, B2)

Preparations ψ_0 = (b_0000 + b_1000)/√2 and ψ_1 = (b_0100 + b_1100)/√2. Pinch A1, then A2.

| Step | Pinched | Central receiver weights, source 0 | Central receiver weights, source 1 | C_j (trace norm) | G_j (trace norm) |
| --- | --- | --- | --- | --- | --- |
| 0 | ∅ | (1) | (1) | 0 | 2 |
| 1 | {A1} | (½, ½) on A1 = 0, 1 | (½, ½) | 0 | 2 |
| 2 | {A1, A2} | (½, 0, ½, 0) on A1A2 = 00, 01, 10, 11 | (0, ½, 0, ½) | 2 | 2 |

The receiver goes from uninformed (0 bits) to perfectly informed (1 bit at balanced prior) at step 2, while the retained whole holds the same distinguishability throughout: there is a transfer with no global creation and no global loss for this pair. The A2 population was retained at step 1 as the noncentral projections P_{00}, P_{01} inside the A1 blocks, and step 2 makes it central (Theorem 12.2, item 5).

**Internal reference, natively.** Take the owner P_{A1=0} (central after step 1). After step 2 it carries both its old unit and the new sector P_{00}, so it has the ratio q = ω(P_{00}) / ω(P_{A1=0}): q_0 = 1, q_1 = 0. A common positive rescaling cancels. This is the projective internal reference of [REVIEW_ENHANCEMENT.md](REVIEW_ENHANCEMENT.md), but here the old unit's retention is Lemma 12.1, not a premise. The direction is reversed relative to the tree: there the new unit contains the old one; here the old unit contains the new ones.

**Loss arrow on the same chain.** The pair (b_0000 ± b_1000)/√2 has G_0 = 2, G_1 = 0 and C_j = 0 for every j. Its phase distinction sits entirely in the step-1 loss layer (item 6) and never reaches any receiver.

Scratch check (`/tmp/chk5.py`, not committed; independent producer and checker code comes at freeze), on 16-dimensional random mixed-state pairs: across 300 trials of random orderings of the four bits, G_j was nonincreasing, C_j nondecreasing and C_j ≤ G_j with trace-norm D, and Tr(a L_j ρ) = 0 for random a ∈ A_{S_j}, with zero violations. Witness C and the phase pair reproduce the table values.

### 12.5 Why the commutative tree needs a premise that the pinching chain does not

For the fiber chain, Z(B_{j−1}) = B_{j−1}, which is not contained in B_j whenever some fiber grows. A decreasing abelian chain is record-compatible only if it is constant. So the commutative pruning chain is never globally record-compatible: absorbing an atom forgets the owner's previous unit, which is why sections 9 to 11 needed the R_inc readings. Lemma 11.4 says the global shell partition coarsens (globally not record-compatible), while each surviving owner's shell partition refines (record-compatible on that owner's corner, with nonunital growing support). So R_inc^− is precisely **record compatibility restricted to surviving owners' corners**, which is the premise of COMPATIBLE_FIBER_RETENTION.md in v15.11 language.

The two chains are therefore complementary:

| | Commutative pruning (P1 fibers) | Pinching (v15.16) |
| --- | --- | --- |
| Owner units as j grows | merge (absorb) | split (refine) |
| Receiver gain mechanism | relocation of removed grade into the owner's fiber (sections 4, 11) | promotion of retained noncentral weights to central records (12.3) |
| Record persistence | premise (R_inc^−, or corner record compatibility) | theorem (Lemma 12.1) |
| Loss layer | sum-zero per fiber, owned by the retained ancestor | traceless off-diagonal coherence, owned by no later receiver |

### 12.6 Mission ledger after draft 5

| Ingredient | Pinching chain status |
| --- | --- |
| Native distinction | Populations under not-yet-central sectors P_{s′}, in the inherited b_r basis. Preparability G is still assumed. |
| Update rule | Nested pinching E_{S_j}, with the composition law E_S E_T = E_{S∪T} inherited. The ordering and occurrence are supplied (premise R). |
| Retained consequence | The central weight vector, an outcome distribution over the pinched record labels. This is a change of record status, not of the complete record-label probabilities (v15.16: these are unchanged by pinching). |
| Identifiable receiver | A minimal central projection of A_{S_j}, which corresponds to the record-register projectors Q_s through Q_s V = V P_s. |
| Persistence | EARNED (Lemma 12.1). |
| Access | Still conditional. Reading central weights is an outcome distribution. An actual single record is supplied by RCR (v15.11), not derived here. |
| Separation of preparations | Exact criterion (Theorem 12.2, item 4). |

### 12.7 Next (one per run)

1. Combine the two chains. Ask whether a native step realizes both directions at once, removing an atom (merge) while pinching inside the owner's block (split). If so, the owner corner inherits record compatibility from the pinching side and the commutative R_inc^− premise would be discharged for that composite. Otherwise, state exactly which side supplies it.
2. Then freeze sections 0 to 12, preregister Thm 11.1, Cor 11.2/11.3, Thm 11.5, Prop 11.6, Lemma 12.1 and Thm 12.2, write independent producer and checker code, run Gemini review via Actions, then audit and read back.
