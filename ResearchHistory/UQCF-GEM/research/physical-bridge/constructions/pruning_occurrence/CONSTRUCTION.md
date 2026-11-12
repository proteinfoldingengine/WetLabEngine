# Construction: forced occurrence of pruning under monotone retention (draft 2)

Author: proteinfolding-grokbot (UQCF Science Agent).
Date: 2026-10-17 America/New_York.
Mode: CONSTRUCTION MODE (STANDING_DIRECTIVE addendum (b)); open premise (2) of Aaron's 2026-10-17 17:33 ET focus: derive the OCCURRENCE of pruning rather than supply it step by step.
Base: the frozen, Gemini-ACCEPTED [recoverable pruning ledger](../recoverable_pruning_ledger/FROZEN_ARGUMENT.md) (freeze `0fbea1c3`, run 39070100916, native_bridge NOT_DERIVED), and the branch-split preparation pair [CONSTRUCTION.md](../preparability_branch_split/CONSTRUCTION.md) with GPT's [TWO_LOCATION_EXTENSION.md](../preparability_branch_split/TWO_LOCATION_EXTENSION.md) (accepted conditional scope, run 39076009238). Notation (carrier tree \(T\), retained ancestor-closed set \(R\ni o\), nearest-retained-ancestor retraction \(r\), fibers, owner grades \(X(y)=\sum_{r(x)=y}x(x)\)) is the ledger's.
Status: UNREVIEWED analytical draft (draft 2 adds §§9–14, written to Aaron's 2026-10-17 19:56 ET correction; §14 supersedes §0 items 1–2 and §5 where they conflict). No milestone, no CLOSED status, no mechanism in code. No geometry, clock, dark-matter primitive or fitting. Time = pruning / ordered recoverability update.

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

---

# Draft 2 (2026-10-17 ~20:00 ET): where M comes from, what it forces, and what it does not

Written to Aaron's 2026-10-17 19:56 ET correction: derive M before adding any access assumption; reconcile with the inherited pruning explanation; find the weakest condition that forces a concrete pruning event; keep (i) occurrence, (ii) receiver-state change and (iii) accessibility separate; report "allowed but not forced" as CONDITIONALLY RESOLVED. No access assumption is used anywhere in §§9–13.

## 9. Deriving M as far as the inherited rules go

Inherited, used below: (D1) the pruning stack's carriers decrease, \(X_0\supseteq X_1\supseteq\cdots\), with retained algebras nested (v15.16, \(E_SE_T=E_{S\cup T}\)) on a **fixed** ambient; (D2) the update is **ordered**: the realized retained carrier is \(X_{j(t)}\) with \(j\) nondecreasing; (E-addr) existing addresses are fixed; (FP) fiber pushforward, an atom's owner is its nearest retained ancestor. Appends come from the separate append-only provenance write (V997 / admission decision 2026-10-17-append-only-provenance-write), not from the pruning stack.

**Proposition 9.1 (transport is unique; earned).** Let \(T'=T\sqcup E\) be an append of leaves. The unital injective \(*\)-homomorphisms \(\ell^\infty(T)\to\ell^\infty(T')\) that fix every old address are exactly the pullbacks \(\varphi^*\) of maps \(\varphi:T'\to T\) with \(\varphi|_T=\mathrm{id}\). Among them, those carrying the retained algebra \(B=r^*\ell^\infty(R)\) to an algebra that obeys FP with the same owner set (owner of \(e\) = nearest retained ancestor) are exactly those with \(r(\varphi(e))=r(\mathrm{parent}(e))\), and all of them give the same algebra, \(\varphi^*B=\pi^*B=\hat r^*\ell^\infty(R)\).
*Proof.* Unital \(*\)-homomorphisms of finite commutative algebras are pullbacks of maps of spectra; injectivity is surjectivity of \(\varphi\), and E-addr fixes \(\varphi\) on \(T\). \(\varphi^*B\) is the fiber algebra of \(r\circ\varphi\); FP with owner set \(R\) demands \(r\circ\varphi=\hat r\), i.e. \(r(\varphi(e))=\hat r(e)=r(\mathrm{parent}(e))\). The algebra depends on \(\varphi\) only through \(r\circ\varphi\). ∎

So the comparison across an append is not a choice. Lemma 1.1's \(\pi\) is one representative of a canonical transport.

**Proposition 9.2 (M is exactly the order read across appends).** For ancestor-closed \(R'\ni o\) on \(T'\): \(\hat r'^*\ell^\infty(R')\subseteq\pi^*B\iff R'\subseteq R\).
*Proof.* (⇐) Between \(x\) and \(\hat r(x)\) no vertex lies in \(R\supseteq R'\), so the nearest \(R'\)-ancestor of \(x\) is that of \(\hat r(x)\): \(\hat r'\) factors through \(\hat r\). (⇒) If \(y\in R'\setminus R\), the indicator of \(y\)'s \(R'\)-fiber (descendants of \(y\) only) separates \(y\) from its strict ancestor \(\hat r(y)\), which shares \(y\)'s \(\hat r\)-fiber. ∎

**Theorem 9.3 (reduction of M).** Assume D1, D2, E-addr, FP and Proposition 9.1. Then M is equivalent to
> **P0 (one stack per Genesis Pin).** The pruning stack's initial carrier \(X_0\) is the Genesis-pinned prefix carrier, and an append extends the ambient by the canonical transport only. It does not start a new stack, so appended entries are never members of any \(X_j\).

*Proof.* (P0 ⇒ M) Every realized \(R_t=X_{j(t)}\subseteq X_0\), so no appended entry is ever retained; across a pure append \(R\) is unchanged (transport); across a pruning step \(R\) shrinks (D1, D2); combined steps factor as transport followed by a fixed-ambient pruning step on \(T'\). (M ⇒ P0) Under M no appended entry is ever in \(R_t\), and \(R_t\subseteq R_0\), so \(X_0:=R_0\) is a single stack for the whole history. ∎

**Proposition 9.4 (P0 is not derivable from D1, D2, E-addr, FP).** The *re-initializing* reading, in which each append extends the stack to \(X_0\cup\{e\}\) (an appended entry is retained on arrival and pruned later, as branch-split draft 1 §2 allowed), satisfies D1 and D2 on every fixed-ambient segment, satisfies E-addr and FP, and violates M whenever \(\mathrm{parent}(e)\in R\).
*Proof.* \(R\cup\{e\}\) is ancestor-closed iff \(\mathrm{parent}(e)\in R\); then \(R\cup\{e\}\not\subseteq R\). Between appends, nothing changes in the inherited rules. ∎

**Proposition 9.5 (record compatibility over-derives).** Read v15.11 §4's condition \(Z(A)\subseteq B\subseteq A\) at every provenance step, with \(A=\pi^*B_t\). Its right inclusion is Proposition 9.2, so it yields M. Its left inclusion, in the commutative \(R_{\min}\) frame where \(Z(A)=A\), forces \(B=A\): no optional removal ever (this is §12.5 of the ledger in this setting). Under the persistent reading \(R_{\mathrm{inc}}^-\), the record closure gains the new singleton shell \(\{e\}\) at every absorption, so its record algebra is **not** contained in the transported one. Appends there are acquisitions, and v15.11's descent condition does not apply to them.

**What §9 establishes.** M is not a new law about retention dynamics. Given the inherited order, it is equivalent to one structural statement about appends (P0), and P0 is independent of the inherited rules (Prop 9.4). v15.11 implies M only at the price of freezing retention. **Status of M: REDUCED to P0, NOT DERIVED.** P0 sits exactly where Aaron's v15.08 qualification says the work is: the correspondence between the Genesis Pin (provenance legitimacy) and the retained state.

## 10. Reconciliation with the inherited pruning explanation

| Source | What it establishes | What it does not supply |
| --- | --- | --- |
| v15.10 | A conditional theorem: composable noninjective recoverability maps give an ordering arrow. Noninjectivity alone does not make succession acyclic (two-cycle `(0,1,2)->(1,0,0)`); strict descent is load-bearing | Occurrence of any noninjective step; an ambient that grows |
| v15.16 | Nested conditional expectations on a fixed algebra, \(E_SE_T=E_{S\cup T}\); the \(R_{\min}\) reading | Appends; why a step happens |
| v15.11 §4 | \(Z(A)\subseteq B\subseteq A\) is sufficient for central records to persist | Selection of \(B\); in the commutative case it forbids strict removal (Prop 9.5) |
| V1153 | A supplied weight update (`exp(-BETA*(U-min U))`) with no final filter | Derivation of that law (admission decision 2026-10-17) |
| Ledger (frozen) | Split \(x=E_mx+\sum D_lx\); fiber ownership; reading lattice; no global creation; Prop 11.6 loss criterion | **Order and occurrence SUPPLIED** |
| This construction | Unique transport (9.1); M ⟺ order across appends (9.2) ⟺ P0 (9.3); forced absorption given M (Thm 1.2); forced order-erasure (§11) | P0; access A |

The extra premise this construction needs beyond the inherited model is **P0** (equivalently M), together with the choice of reading (§11) and the semantic append permission GPT flagged.

## 11. Weakest condition that forces a concrete pruning event

Two senses of "pruning event" have been conflated, including in draft 1 (§1, "an append IS a pruning event").
- **Ambient-relative (ledger P2 sense):** a nonzero loss-layer component. A distinction present in the ambient is never carried by the record.
- **Record-relative (v15.10 sense):** a distinction that the record **did** separate at some earlier step is no longer separated. This is a noninjective recoverability map on what was retained.

**Lemma 11.1 (one absorption loses nothing previously recorded).** Under M and \(R_{\min}\), take a single append with fixed data (parent \(\ell\), grade \(w\)) and no removal. The record map \(X\mapsto X+w\,\delta_{r(\ell)}\) is a translation, hence injective. It is an ambient-relative event: the attachment point inside \(r(\ell)\)'s fiber is never recorded. It is not a record-relative one, and in transported terms \(B_{t+1}=\pi^*B_t\), with no strict descent.

So draft 1's Theorem 1.2 forces the ambient-relative event at every append. That does not yet give v15.10's arrow.

**Theorem 11.2 (order erasure, forced; R_min).** Assume M (or only P0 for the two appended atoms; call this M_loc), the \(R_{\min}\) reading, and no removal between the two appends. Take two deliveries \(d_1=(y,g)\) and \(d_2=(z,h)\) into the fibers of retained owners \(y,z\), with \(y\neq z\), or \(y=z\) and \(g\neq h\). Let \(H\) deliver \(d_1\) at step \(s\) and \(d_2\) at step \(t>s\), and let \(H'\) deliver them in the opposite order, both from the same Genesis-pinned prefix. Then:
1. at step \(s\) the records differ, \(X+g\delta_y\neq X+h\delta_z\), so the order is recorded;
2. at step \(t\) the records coincide, \(X+g\delta_y+h\delta_z\), and they coincide at every later step under any common continuation;
3. the provenance logs of \(H\) and \(H'\) still differ (append-only), so the order is kept in the history and erased from the retained state.

*Proof.* Theorem 1.2 at each append; addition commutes; later common updates act identically. ∎

This is a concrete, reached pruning event in v15.10's sense. The fixed map \((X_s,d_s,d_t)\mapsto X_s+d_s+d_t\) is invariant under swapping the deliveries, hence noninjective on \(\{H,H'\}\). The merged state is **reached** at step \(t\) in both histories, not only shown to persist. Acyclicity of the resulting succession comes from the append-only provenance order, not from noninjectivity (the v15.10 caveat is respected).

**Proposition 11.3 (minimality).** Under M and \(R_{\min}\), with no removal, a record-relative loss needs at least two absorptions between the compared records (Lemma 11.1). Two suffice (Theorem 11.2). The condition is local: two atoms, one or two owners, two steps. It needs no global shrinking, no capacity bound and no optional removal.

**Proposition 11.4 (persistent reading: allowed, not forced).** Under \(R_{\mathrm{inc}}^-\), absorptions are recorded as shells keyed by arrival step, so \(H\) and \(H'\) stay separated (owner \(y\) holds shell \((s,g)\) vs \((t,g)\)). No number of absorptions alone causes a record-relative loss. Such a loss needs Prop 11.6(b), the removal of an owner that had absorbed a shell, and that removal is optional under M. Simultaneous arrivals (Prop 11.6(a)) lose only distinctions that were never recorded. **Under \(R_{\mathrm{inc}}^-\), occurrence of a record-relative pruning event is CONDITIONALLY RESOLVED: allowed, not forced.**

**Proposition 11.5 (capacity forces nothing new here).** Under M, \(|R_t|\) never grows, so an owner-count bound \(K\ge|R_0|\) never binds, and a bound \(K<|R_0|\) forces only finitely many removals, all before any append matters. A record-dimension bound under \(R_{\mathrm{inc}}^-\) forces shells to merge once it is saturated. Merging the new shell into an old one with known data is again a translation (Lemma 11.1), so even this forces a record-relative loss only through an unforced choice of which shells merge. This is Bennett's finite-memory erasure; it does not single out an event.

Reading consequence, stated plainly: the inherited reading \(R_{\min}\) forgets **when** deliveries arrived and keeps **how much** arrived; the persistent reading \(R_{\mathrm{inc}}^-\) keeps both. Choosing the reading is choosing whether the retained record keeps provenance order. Under \(R_{\min}\) the arrow is forced by two appends; under \(R_{\mathrm{inc}}^-\) it is not.

**Link to W2.** Aaron's \((g,h)\) vs \((h,g)\) pair is Theorem 11.2 with \(y=u\), \(z=v\), read at the owner that absorbs both (complete \(a\)). The blindness of W2 at completeness (§3), and branch-split Proposition 3.2's collapse, are this forced order-erasure event viewed from the receiver. They are the occurrence result, not a failed separation.

## 12. The three obligations, kept separate

| Obligation | Status after draft 2 | Premises |
| --- | --- | --- |
| (i) A pruning event occurs | Ambient-relative: **FORCED** at every append (Thm 1.2, Lemma 11.1). Record-relative: **FORCED under \(R_{\min}\)** by two appends (Thm 11.2), minimal (Prop 11.3); **CONDITIONALLY RESOLVED (allowed, not forced) under \(R_{\mathrm{inc}}^-\)** (Prop 11.4) | P0 (≡ M), reading choice, append permission |
| (ii) Aggregation changes the receiver's state | **FORCED** for the owner of the parent: \(X(r(\ell))\mapsto X(r(\ell))+w\) at the arrival step. Under completeness every inside append reaches \(a\) (Thm 3.2(2)), but reaching completeness is **not** forced (Thm 3.2(3)): a persistent merged state is not thereby reached | P0, plus completeness for the \(a\)-only reading |
| (iii) The change is accessible to the receiver | **NOT ADDRESSED; A NOT DERIVED.** No step in §§9–12 uses or implies a readout | — |

## 13. Honest novelty (draft 2)

Known: sums forget summands (Landauer/Bennett logical irreversibility); coarse-graining loses order information; decreasing filtrations and data processing (§6). Not claimed against these. What is new for the program: (1) the transport across an append is unique given E-addr and FP (9.1), so M becomes a precise, testable statement (9.2) and reduces to a single Genesis-Pin premise P0 that is provably independent of the inherited rules (9.3–9.4); (2) v15.11 compatibility across appends implies M only by freezing retention (9.5); (3) separating ambient-relative from record-relative events shows that one absorption is never a v15.10 loss (11.1), while two absorptions force one under the inherited reading (11.2–11.3); this is the minimal local forcing, and it is an erasure of **provenance order** from the retained state with the order kept in the pinned history, which is v15.08's "history is not visible state" obtained as a consequence; (4) the reading lattice is identified as the switch between a forced and an unforced arrow (11.4).

## 14. Corrections to draft 1, and next

- §0 item 1 and §1 "an append IS a pruning event": true in the ambient-relative sense only (Lemma 11.1). §0 item 2 and Theorem 2.1: \(D_t\) is an ambient-relative counter; it is not v15.10's record-relative arrow. The record-relative arrow is Theorem 11.2 (\(R_{\min}\)).
- §5's "Occurrence: FORCED CONDITIONAL ON M" now reads: ambient-relative forced given P0; record-relative forced given P0 and \(R_{\min}\); conditionally resolved under \(R_{\mathrm{inc}}^-\).
- Exploratory scratch check `/tmp/occ2/chk9.py` (not committed, not evidence, no mechanism): 3000 random trees with 2–7 atoms. It found 0 violations of transport uniqueness (9.1), inclusion iff \(R'\subseteq R\) (9.2), abelian v15.11 rigidity (9.5), translation injectivity (11.1), order erasure under \(R_{\min}\) (11.2) and order retention under \(R_{\mathrm{inc}}^-\) (11.4), and the re-initializing countermodel violated M in every case where \(\mathrm{parent}(e)\in R\) (9.4).
- **Next:** freeze §§0–14 with the corrections; preregister; independent producer and checker for 9.1, 9.2, 9.4, 9.5, 11.1–11.4; Gemini review via Actions with the exact frozen text. After that, attempt to derive P0 from the Genesis Pin correspondence (v15.08) or show it independent there too. Access (iii) stays untouched until then, per Aaron's correction.
