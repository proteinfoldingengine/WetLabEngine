# Construction: forced occurrence of pruning under monotone retention (draft 1)

Author: proteinfolding-grokbot (UQCF Science Agent).
Date: 2026-10-17 America/New_York.
Mode: CONSTRUCTION MODE (STANDING_DIRECTIVE addendum (b)); open premise (2) of Aaron's 2026-10-17 17:33 ET focus: derive the OCCURRENCE of pruning rather than supply it step by step.
Base: the frozen, Gemini-ACCEPTED [recoverable pruning ledger](../recoverable_pruning_ledger/FROZEN_ARGUMENT.md) (freeze `0fbea1c3`, run 39070100916, native_bridge NOT_DERIVED), and the branch-split preparation pair [CONSTRUCTION.md](../preparability_branch_split/CONSTRUCTION.md) with GPT's [TWO_LOCATION_EXTENSION.md](../preparability_branch_split/TWO_LOCATION_EXTENSION.md) (accepted conditional scope, run 39076009238). Notation (carrier tree \(T\), retained ancestor-closed set \(R\ni o\), nearest-retained-ancestor retraction \(r\), fibers, owner grades \(X(y)=\sum_{r(x)=y}x(x)\)) is the ledger's.
Status: UNREVIEWED analytical draft. No milestone, no CLOSED status, no mechanism in code. No geometry, clock, dark-matter primitive or fitting. Time = pruning / ordered recoverability update.

---

## 0. Result first

GPT's accepted review left three open items for the branch-split pair; item R3 reads "complete-fiber contraction is allowed but not forced; a capacity story is not enough." This draft answers R3 positively, under one identified premise **M**, and shows exactly where a capacity story fails.

**Premise M (monotone retention along provenance).** The retained record is a single decreasing filtration along the whole provenance order, appends included: \(R_{t+1}\subseteq R_t\) as address sets (address stability \(r_{XY}(t)=t\)).

M is the v15.16 nesting \(A_{k+1}\subseteq A_k\) applied across a provenance append, using the ledger's own extension of the retraction to the new carrier (Lemma 1.1). It is the program's definition of time (an ordered recoverability update is monotone), read across appends. It is an identification, not a deduction from the inherited texts; it is stated as a premise.

From M alone:

1. **Forced absorption (Theorem 1.2).** Every append is pruned at the step it occurs: its grade is delivered to the current owner of its parent, and nothing else changes. Occurrence is forced; no step-by-step supply.
2. **Forced arrow (Theorem 2.1).** The recoverability defect \(D_t=|T_t|-|R_t|\) rises by at least one per append. Optional (retained-set-shrinking) prunings are finite in any history, so in the long run every update that raises \(D\) is a forced absorption, ordered by provenance.
3. **Forced endpoint (Theorem 3.2).** The subtree charge \(S_a=\sum_{x\preceq a}x(x)\) is schedule-independent. Complete-fiber status of a receiver is absorbing, and while it holds, \(X(a)=S_a\) and every inside append is delivered to \(a\) at once. This is R3's endpoint, reached without any choice of order.
4. **Selection boundary (Proposition 4.1).** In the capacity reading (\(|R|\le K\)) instead of M, the endpoint is forced iff the slack is zero; at slack one an admissible retention choice makes W1's receiver/reference pair coincide (counting grades: \((3,1)=(3,1)\)). This is the exact sense in which "capacity is not enough."

Receiver consequence: under M, W1 (append inside vs outside \(a\)'s branch) separates on the receiver/reference pair for every optional-pruning schedule in both histories, forever (Corollary 3.3). Ledger point: the total grade is conserved, global distinguishability of where an atom attached inside a fiber is erased, and the receiver gains the inside/outside bit. Information moves; none is created.

## 1. Monotone retention forces absorption

**Lemma 1.1 (the ledger's extension).** Let \(B=r^*\ell^\infty(R)\subseteq\ell^\infty(T)\) be the retained (fiber-constant) algebra, and append a leaf \(e\) under \(\ell\in T\). Let \(\pi:T\sqcup\{e\}\to T\) fix \(T\) and send \(e\mapsto\ell\). Then \(\pi^*B=\hat r^*\ell^\infty(R)\), where \(\hat r\) is the nearest-retained-ancestor retraction on \(T\sqcup\{e\}\) with the same \(R\), and \(\hat r(e)=r(\ell)\).
*Proof.* \(e\notin R\), so its nearest retained ancestor is that of \(\ell\), which is \(r(\ell)\) (\(=\ell\) if \(\ell\in R\)). Hence \(\hat r=r\circ\pi\). ∎

\(\pi\) is the only extension compatible with E-addr (existing addresses fixed) and with fiber pushforward (an atom's owner is its nearest retained ancestor). Sending \(e\) to another vertex would assign it an owner that is not its nearest retained ancestor.

**Premise M (formal).** The retained algebra after the update satisfies \(B'\subseteq\pi^*B\). Since \(B'\) and \(\pi^*B\) are fiber-constant algebras of retractions with retained sets \(R'\) and \(R\), and a retraction algebra contains another iff its fibers are finer, \(B'\subseteq \pi^*B\iff R'\subseteq R\).

**Theorem 1.2 (forced absorption).** Under M, at the append step: \(e\notin R'\); if no optional removal accompanies it, \(X'(r(\ell))=X(r(\ell))+w\) and \(X'(y)=X(y)\) for every other \(y\in R\).
*Proof.* \(e\notin R\supseteq R'\). With \(R'=R\), Lemma 1.1 gives \(\hat r(e)=r(\ell)\), and every old atom keeps its owner. ∎

So an append IS a pruning event: the new atom never becomes a retained sector, and its identity inside the fiber of \(r(\ell)\) is not recoverable from the retained record. This is the ordered recoverability update occurring because of provenance growth, not because a schedule asked for it.

Consequences, stated plainly. The set of possible receivers is fixed by the prefix: under M no appended entry can later become an owner. This matches Aaron's identification of receiver identity with a Genesis-pinned ancestry path. M excludes the ledger readings in which an appended entry is first retained and pruned later (branch-split draft 1 §2 used such histories; under M their arrival step is the append step itself).

## 2. A derived arrow

**Theorem 2.1 (recoverability defect).** Let \(D_t=\dim\ell^\infty(T_t)-\dim B_t=|T_t|-|R_t|\), the number of ambient atom coordinates not recoverable from the retained record. Under M:
1. \(D_{t+1}\ge D_t+n_t\), where \(n_t\) is the number of appends at step \(t\), with equality iff no optional removal occurs.
2. The total number of optional removals in any history is at most \(|R_0|-1\), and at most \(|R_0|-|\mathrm{anc}[a]|\) while a receiver \(a\) stays retained.
3. Hence, for any history with infinitely many appends, all but finitely many updates that raise \(D\) are forced absorptions. Each is non-injective from ambient to retained record under \(R_{\min}\) (\(e\) and its owner's atoms share one coordinate). Under \(R_{\mathrm{inc}}^-\) a single absorption is recorded as a new shell and is not by itself a loss arrow; by Prop 11.6 a loss arrow needs two atoms absorbed into one fiber in one step, or removal of an owner that had absorbed a shell, so the \(R_{\mathrm{inc}}^-\) arrow is forced only when appends arrive together into one fiber or an optional removal hits an absorber.
*Proof.* (1) \(|T|\) grows by \(n_t\) and \(|R|\) is nonincreasing. (2) \(R_t\) is a decreasing chain of ancestor-closed sets containing \(o\) (and \(\mathrm{anc}[a]\)). (3) From (1) and (2). ∎

The arrow's direction is the provenance order (append-only, Genesis-pinned); its occurrence is forced by M. No clock is introduced: \(D\) counts forgotten coordinates and changes only at events.

## 3. Forced endpoint and the receiver consequence

**Lemma 3.1 (subtree charge).** For a retained \(a\) and any ancestor-closed \(R\ni a\), every atom of \(\mathrm{desc}[a]\) is owned inside \(\mathrm{desc}[a]\) and no other atom is. So \(S_a=\sum_{x\in\mathrm{desc}[a]}x(x)=\sum_{y\in R\cap\mathrm{desc}[a]}X(y)\), independent of \(R\) and of the schedule that produced it. Appends change it by \(w\) iff inside.
*Proof.* Nearest retained ancestors of a descendant of \(a\) lie on its path to \(a\), and \(a\in R\); an atom outside \(\mathrm{desc}[a]\) has no ancestor in \(\mathrm{desc}[a]\). ∎

**Theorem 3.2 (forced complete-fiber endpoint).** Call \(a\) *complete* at \(t\) if \(R_t\cap\mathrm{desc}(a)=\emptyset\) (strict descendants). Under M:
1. Completeness is absorbing: once complete, complete forever.
2. While complete, \(X_t(a)=S_a(t)\), and each inside append raises \(X(a)\) by \(w\) at the step it occurs, whatever else is pruned and in whatever order.
3. Completeness is reached in finitely many optional removals (at most \(|R_0\cap\mathrm{desc}(a)|\)) or never; it holds from the start iff the prefix's retained set has no strict descendant of \(a\).
*Proof.* (1) \(R\) only shrinks. (2) Lemma 3.1 with \(R\cap\mathrm{desc}[a]=\{a\}\), and Theorem 1.2. (3) Theorem 2.1(2). ∎

What is forced and what is not: given completeness at the prefix (or once reached), the endpoint GPT's ratio proof needs is forced for all later times without any order choice. Whether an incomplete prefix becomes complete is not forced by M (item 3). So R3 is answered for complete-fiber prefixes, and reduced to "is the receiver's prefix fiber complete" otherwise.

**Corollary 3.3 (W1 under M, schedule-free).** Take W1's prefix \(P=\{o,a,u,v\}\) (\(a\) under \(o\); \(u,v\) under \(a\)), grades \(c,\alpha,\beta,\gamma\), \(A=\alpha+\beta+\gamma\). Preparation I appends \(e\) (grade \(w\)) under \(u\); O appends \(f\) (grade \(w\)) under \(o\). Under M, with \(o,a\) retained and any optional schedules in I and O independently:
- \(X_I(o)=c\) and \(X_O(o)=c+w\) at every step after the append. The pair \((X(a),X(o))\) differs in every comparison of the two histories, at all later times.
- If \(a\) is complete at the prefix (\(R_0=\{o,a\}\)), the pairs are \((A+w,c)\) and \((A,c+w)\) from the append on, so the ratio \(q_I=(A+w)/c>A/(c+w)=q_O\), and \(X(a)\) alone separates with a fixed grade unit.
*Proof.* Outside \(\mathrm{desc}[a]\) the only vertices are \(o\) and (in O) \(f\); \(f\notin R\) by M, so \(o\) owns exactly \(\{o\}\) in I and \(\{o,f\}\) in O, for every \(R\). The second item is Theorem 3.2. ∎

Counting grades (\(c=\alpha=\beta=\gamma=w=1\)), complete prefix: I gives \((4,1)\), O gives \((3,2)\). Full prefix \(R_0=P\): the \(a\)-coordinate alone can coincide across schedules (for example \((2,1)\) vs \((2,2)\)), but the reference coordinate never does.

**W2 under M.** Appends under \(u\) vs \(v\) change \(S_a\) equally. With \(a\) complete, W2 is blind. With \(u,v\) retained, separation needs a contingent order of their later removal (branch-split Proposition 3.2), which M neither forces nor forbids. This is consistent with Corollary 3.3 of the branch-split draft: forced occurrence does not erase W1, and leaves W2 to order contingency.

## 4. Why capacity alone is not enough, exactly

**Proposition 4.1 (capacity reading).** Replace M by: retained sets are ancestor-closed, contain \(\mathrm{anc}[a]\), and satisfy \(|R|\le K\). Let the slack be \(s=K-|\mathrm{anc}[a]|\).
1. If \(s=0\), the retained set is uniquely \(\mathrm{anc}[a]\) after every update; occurrence is forced at every append and the endpoint is forced and unique.
2. For W1 (\(\mathrm{anc}[a]=\{o,a\}\)) with \(s=1\), there are admissible retention choices for W1 that make the pairs coincide whenever \(\gamma=w\): I retaining \(\{o,a,v\}\) gives \((\alpha+\beta+w,c)\); O retaining \(\{o,a,f\}\) gives \((\alpha+\beta+\gamma,c)\).
*Proof.* (1) \(\mathrm{anc}[a]\) is the only ancestor-closed set of size \(|\mathrm{anc}[a]|\) containing it. (2) Direct computation. ∎

So capacity forces occurrence but leaves a selector when \(s\ge1\), and the selector can blind the receiver. M removes the selector by forbidding appended atoms from ever being retained, which is why it, and not a bare capacity bound, gives the order-free endpoint.

## 5. Mission ledger after this draft

| Ingredient | Status |
| --- | --- |
| Native distinction | W1 location of an append (pinned-tree invariant), inherited from branch-split; G still needs two certified append locations (GPT obligation (2)). Under M the obligation reduces to two permitted appends whose parents have different current owners, one of them \(a\) (Theorem 1.2: location matters only modulo fibers) |
| Update rule | Occurrence: **FORCED CONDITIONAL ON M** (Theorem 1.2). Order: not needed for W1 (Corollary 3.3). Arrow: \(D_t\), derived from M (Theorem 2.1) |
| Retained consequence | \(X(a)=S_a\) under completeness, schedule-free (Theorem 3.2); reference coordinate always separates W1 (Corollary 3.3) |
| Receiver identity / access | Identity fixed by the prefix (M). At completeness \(a\)'s coordinate is central, every later admissible update leaves its fiber intact and only adds to it: the "record in the part every retained operation leaves alone" condition holds. The readout itself (receiver state = own fiber coordinate, and the pair with the reference under one scale) is **A, NOT DERIVED** |
| Separation | EARNED given M: Corollary 3.3 for all schedules |
| Ledger point | Total grade conserved; intra-fiber attachment erased; receiver gains the inside/outside bit |
| Premises supplied | **M** (identification of v15.16 nesting across appends); completeness of the receiver's prefix fiber (or its later occurrence); semantic append permission (GPT (2)); access A |

## 6. Honest novelty

The mathematics is elementary (decreasing filtrations of fiber-constant algebras, conserved subtree sums). Known neighbours: the data processing inequality and decreasing filtrations of conditional expectations (global distinguishability nonincreasing); finite-memory observers that must erase (Bennett's reading of Landauer's principle for Maxwell's demon), which is the capacity version of Proposition 4.1; coarse-graining arrows (Boltzmann-type entropy growth under a fixed coarse graining); einselection and pointer algebras (the retained abelian algebra as the record), and quantum Darwinism (records as redundant fragment information), which concern how many copies exist rather than when a record must form. No claim is made against these.

What is new for the program:
1. Occurrence of pruning is derived, not supplied, from one premise (M) that is the program's own time definition read across appends; every append is a pruning event (Theorem 1.2).
2. An explicit arrow counter \(D_t\), with optional pruning provably finite, so the long-run arrow is the provenance order (Theorem 2.1).
3. An order-free answer to GPT's R3: the complete-fiber endpoint is absorbing and forced under M (Theorem 3.2), with W1 separated for every schedule (Corollary 3.3).
4. The exact boundary between M and a capacity bound: zero slack forces, slack one admits a blinding selector (Proposition 4.1).

## 7. Exploratory check (not evidence)

Scratch script `/tmp/occ/chk8.py`, not committed, no mechanism. 4000 random trees (3–8 atoms), random interleavings of M-appends and optional ancestor-closed removals keeping \(\mathrm{anc}[a]\): 0 violations of forced absorption (Theorem 1.2), \(D\) increment (Theorem 2.1(1)), optional-removal bound (2.1(2)), subtree charge (Lemma 3.1), and completeness persistence with \(X(a)=S_a\) (Theorem 3.2). W1 under M from the full prefix over all 16 schedule pairs: the reference coordinate differs in every pair. Proposition 4.1(2) counting example reproduced: \((3,1)\) vs \((3,1)\) at slack one; \((4,1)\) vs \((3,2)\) at slack zero. Independent producer/checker verification follows the freeze, per construction mode.

## 8. Next

(a) Justify or weaken M: test whether v15.16's nested chain plus Z(A_k)⊆A_{k+1} can be stated on the growing ambient without M, and whether any inherited text retains an appended entry as an owner (that would refute M as a reading).
(b) Access (premise A) at completeness: the receiver's coordinate is central and update-invariant up to additive delivery; find what is still missing for a readout without an added channel (next run, alternating to (1)).
(c) Then freeze §§0–7, preregister, independent producer and checker, Gemini via Actions.
