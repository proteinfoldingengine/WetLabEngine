# Construction: recoverable pruning writes an owned ancestor ledger entry

Author: proteinfolding-grokbot (UQCF Science Agent). Started 2026-10-17 America/New_York.
Source baseline: `d90f9a30c006a15cf97257e857a149bbb9423e91`, branch `research/uqcf-overlapping-guard-exchange`.
Mode: CONSTRUCTION MODE (STANDING_DIRECTIVE addendum (b)). Status: ACTIVE POSITIVE CONSTRUCTION, DRAFT 3 (section 9 added 2026-10-17 ~12:00 ET on baseline `d23a59b73160acec15ff0d945a0c2f6ebcdff351`; section 10 added 2026-10-17 ~13:00 ET on baseline `202fb12970a6b7c7c74c47aabbd18dda2926268f`), UNREVIEWED. No adversarial grading, admission class, code or Gemini review yet; those come after the mechanism is drafted. No milestone or closure is claimed.

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
2. Settle premise L: either derive fiber-locality from P1, P2 and the relabeling naturality, or state the minimal extra earned fact.
3. Generalize the witness: arbitrary finite trees and multi-step sequences. Prove that each owner's ledger reconstructs exactly the fine grades of the removed atoms in its cumulative fiber, which follows by telescoping.
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
