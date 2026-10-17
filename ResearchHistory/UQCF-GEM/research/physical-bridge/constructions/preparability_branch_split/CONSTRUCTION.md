# Construction: preparability as native reachability by a pinned branch split (draft 1)

Author: proteinfolding-grokbot (UQCF Science Agent).
Date: 2026-10-17 America/New_York.
Mode: CONSTRUCTION MODE (STANDING_DIRECTIVE addendum (b)); Aaron's 2026-10-17 17:45 ET preparability directive (G as native reachability, not an external preparer).
Base: the frozen, Gemini-ACCEPTED [recoverable pruning ledger](../recoverable_pruning_ledger/FROZEN_ARGUMENT.md) (freeze `0fbea1c3`, review run 39070100916, native_bridge NOT_DERIVED). Notation (carrier tree, retraction \(r_j\), fibers \(F_j(t)\), shells \(A_l(t)\), readings \(R_{\min}<R_{\mathrm{inc}}^-<R_{\mathrm{full}}\)) is that document's.
Status: UNREVIEWED analytical draft. No milestone, no CLOSED status, no preparation mechanism in code. No geometry, clock, dark-matter primitive or fitting. Time = pruning / ordered recoverability update.

---

## 0. Result first

The ledger's Witnesses A–D *wrote down* two source assignments. Here both histories are **exhibited** as admissible append-only extensions of one Genesis-pinned prefix \(P\), so the pair is reachable rather than assigned. The receiver identity (its pinned ancestry path) and its initial accessible record are identical in both, because append-only extension leaves every entry of \(P\) unchanged. One common inherited operation \(\Omega\) (a fixed sequence of subtree retractions on addresses of \(P\)) then gives distinct receiver records. The exact criterion (Theorem 2.2) is that the two appended entries reach the receiver's fiber at different pruning steps.

Two witnesses come out of it:

- **W1 (inside vs outside).** One extra entry is appended either inside the receiver's future fiber or outside it. The two sources are distinct as pinned trees (no relabeling maps one to the other), the global total grade is equal, and the receiver separates them even under \(R_{\min}\). This works for **every** common operation that eventually retracts the inside branch into the receiver, including any content-covariant forced order.
- **W2 (Aaron's grade pair \((g,h)\) vs \((h,g)\)).** The extra entry is appended under sibling \(u\) or sibling \(v\). Both histories are exhibited, with equal total grade, the same receiver and the same initial record. They are separated under \(R_{\mathrm{inc}}^-\) by the common order "retract \(u\) then \(v\)", and not by any order derived covariantly from content (Proposition 3.2). This sharpens G against premise (2): **a fully forced, content-equivariant pruning order destroys the symmetric swap witness**. Forcing the *occurrence* of pruning, and the order of comparable (ancestor-related) retractions, does not.

What stays assumed is **N**, the Genesis-Pin legitimacy of append-only extensions that does not depend on where the append lands (§1). Access A/R\(_{\mathrm{inc}}^-\) is inherited open from the ledger. G is upgraded from *assumed preparation* to *exhibited reachability conditional on N*. It is not closed.

## 1. Native ingredients

Inherited and earned (cited, not re-proved):

- **E-pin.** Genesis Pin (V997 claim boundaries; V994 minimality): legitimacy is a property of the *history*. It requires a pinned registry and anchor root, quorum witness participation, append-only continuity and no circular bootstrap. After genesis, updates are governed recursively. v15.08: it certifies history legitimacy, not a reference state. v13.23 / site: it is "a ledger, not a selector".
- **E-addr.** Stable addresses \(r_{XY}(t)=t\). An entry's address is its pinned ancestry path. Append-only extension changes no existing address or grade.
- **E-ret.** Ledger P1/P2: closed ancestral retractions, fiber pushforward to the nearest retained ancestor, \(x=E_m x+\sum_l D_l x\), and Theorem 11.1 (owner record = pushforward onto block / shells / singletons). Theorem 11.5 (global nonincreasing, receiver nondecreasing) holds for any **fixed, source-independent** retraction sequence.
- **E-anc.** v15.10 intrinsic ancestry order. v15.13: incomparable events commute, and dependency arrows are declared. The only order constraint on retractions is ancestry (a descendant is removed no later than its ancestor). This is exactly the frozen ledger's class of closed pruning sequences.

Premise used here (not derived):

- **N (pinned append legitimacy, location-free).** (N1) Admissible histories are append-only extensions of a Genesis-pinned prefix satisfying the E-pin conditions. (N2) The E-pin conditions do not refer to the parent location of an appended entry: if appending an entry of type \(\tau\) (grade \(w>0\)) under \(\ell\in P\) is legitimate, so is appending the same type under any \(\ell'\in P\). (N3) At least one legitimate append beyond \(P\) exists. N1 is the inherited definition. N2 is a reading of "ledger, not selector": no pin condition mentions location. N3 is witnessed in the V997 toy, where quorum and witnesses are supplied.

**Reachability vs emission.** G as reachability is the *modal* claim that both histories are admissible. It is not the *causal* claim that some native law emits one of them. The earlier append-only provenance screen (`73d78836`) found the causal version needs a native emission law \(P_{\mathrm{emit}}\), which is still missing. This construction needs only N, not \(P_{\mathrm{emit}}\).

## 2. Branch-split histories and the separation criterion

**Setup.** Take a pinned prefix tree \(P\) with root \(o\) (the pin anchor), nonnegative grades \(x\) on \(P\), and a receiver \(a\in P\setminus\{o\}\). For \(\ell\in P\), let \(T_\ell=P\cup\{e\}\) with \(e\) a new leaf under \(\ell\) of grade \(w>0\). By N, every \(T_\ell\) is admissible, anchored to the same pin.

**Lemma 2.1 (blind start, same identity).** For all \(\ell,\ell'\): \(a\)'s address, grade and fiber \(F_0(a)=\{a\}\) are identical in \(T_\ell\) and \(T_{\ell'}\). So the receiver's initial accessible record, under any reading, is the same.
*Proof.* E-addr: append-only extension changes no existing entry, and \(e\notin F_0(a)\). ∎

**Common operation.** \(\Omega=(p_1,\dots,p_m)\) with \(p_j\in P\), and \(a\) not in any subtree of a \(p_j\). Step \(j\) retracts the currently retained part of the subtree at \(p_j\) into its nearest retained proper ancestor. This is a closed ancestral retraction (E-ret, E-anc). It is written in addresses of \(P\) only, so it is the *same* operation on every \(T_\ell\), and it is source-independent as Theorem 11.5 requires. The appended leaf goes with its parent's subtree.

Define the **arrival step** \(s_a(\ell)=\min\{j:\ e\in F_j(a)\}\in\{1,\dots,m,\infty\}\).

**Theorem 2.2 (separation criterion).** Under \(\Omega\), with \(w=w'\) (same entry type):
1. (\(R_{\mathrm{inc}}^-\), raw) \(a\)'s records on \(T_\ell, T_{\ell'}\) differ iff \(s_a(\ell)\neq s_a(\ell')\).
2. (\(R_{\min}\), at step \(j\)) they differ iff exactly one of \(s_a(\ell), s_a(\ell')\) is \(\le j\).
3. (\(R_{\mathrm{inc}}^-\), projective, GPT's ratio contract) if both arrival steps are finite, the records differ projectively iff \(s_a(\ell)\neq s_a(\ell')\). If exactly one is finite, they differ projectively unless the base shell-sum vector of \(a\) is supported on that single shell.

*Proof.* Theorem 11.1 with additivity of the pushforward: the shell-sum vector of \(a\) on \(T_\ell\) is \(\mathbf w_P+w\,\delta_{s_a(\ell)}\), where \(\mathbf w_P\) is the vector for \(P\) and \(\delta_\infty=0\). That \(e\)'s grade enters exactly one shell, at its arrival, follows from fiber pushforward: before \(e\) is removed its owner is \(e\); afterwards its owner is \(r_j(e)\), and fibers only merge. Parts (1) and (2) are immediate. For (3), two vectors with equal positive totals are proportional iff they are equal. With unequal totals \(M\) (for \(s=\infty\)) and \(M+w\) (finite \(s\)), proportionality means \(\mathbf w_P+w\delta_s=\lambda\mathbf w_P\) with \(\lambda=(M+w)/M\), i.e. \((\lambda-1)\mathbf w_P=w\delta_s\), so \(\mathbf w_P=M\delta_s\) is supported on shell \(s\) alone, which is the stated exception. ∎

**Ledger point (Theorem 11.5 applies).** The source variable \(S=\ell\) is fixed at the split, and \(\Omega\) is source-independent. So global distinguishability of \(S\) is nonincreasing along \(\Omega\), while \(a\)'s rises from 0 (Lemma 2.1) to 1 bit at step \(\min(s_a(\ell),s_a(\ell'))\) under a balanced prior. **The receiver gains information by redistribution, and none is created globally.** The bit was in the ledger from the split, as the location of an append. Pruning relocates it into the receiver's fiber.

## 3. The two witnesses

Use unit (counting) grades for display. Theorem 2.2 needs only \(w>0\) and equal type. Take \(P=\{o,a,u,v\}\) with \(a\) under \(o\), \(u,v\) under \(a\), receiver \(a\).

**W1 (inside vs outside).** Sources \(T_u\) (append under \(u\)) and \(T_o\) (append under \(o\)). No pinned isomorphism fixing \(o,a\) maps one to the other: the appended entry sits at depth 3 vs depth 1. So the distinction is native and gauge-invariant. The global total grade is equal (5 = 5). With \(\Omega=(u,v)\), \(a\)'s cumulative history is \((1,3,4)\) vs \((1,2,3)\), so \(s_a(u)=1\) and \(s_a(o)=\infty\). It separates under \(R_{\min}\) at every step \(\ge1\), and under \(R_{\mathrm{inc}}^-\) raw and projectively.

**Proposition 3.1 (robustness).** For any common \(\Omega\) that eventually retracts \(u\)'s subtree with \(a\) retained, \(s_a(u)<\infty=s_a(o)\). This includes every content-covariant forced rule, provided it does this in both histories. So W1's separation does not depend on how the order arises.

**W2 (Aaron's grade pair).** Sources \(T_u\) and \(T_v\). By N2 they come from the same pinned prefix, are equally legitimate, and have the same receiver and the same initial record. With counting grades, the sibling-branch grades are \((g,h)=(2,1)\) vs \((h,g)=(1,2)\). Generally they are \((x_u+w,x_v)\) vs \((x_u,x_v+w)\), an exact swap iff \(x_u=x_v\). Both histories are now **exhibited**, not merely assigned. With common \(\Omega=(u,v)\): \((1,3,4)\) vs \((1,2,4)\). \(R_{\min}\) at the end is \(4=4\), not separated. \(R_{\mathrm{inc}}^-\) separates, with projective ratio \(q=2/3\) vs \(1/3\). With the simultaneous step \(\Omega=(\{u,v\})\), \(s_a(u)=s_a(v)\), so W2 is not separated (Theorem 2.2).

**Gauge.** The pinned automorphism \(\sigma\) (swap \(u\leftrightarrow v\), fix \(o,a\)) maps \(T_u\) to \(T_v\), so the two *sources alone* are gauge-equivalent. The *histories* \((T_u,\Omega)\) and \((T_v,\Omega)\) are not: \(\sigma(T_v,(u,v))=(T_u,(v,u))\neq(T_u,(u,v))\), and \(\sigma\) is the only nontrivial pinned automorphism. The gauge-invariant source distinction in W2 is therefore relational: *whether the append landed in the first-retracted or the second-retracted sibling branch*. The receiver acquires a fact about content relative to pruning order, that is, temporal-order information. This answers Aaron's symmetry condition. \(\sigma\) is admissible (N2, E-addr: sibling indices are chart, not provenance), and the two cases stay distinct modulo \(\sigma\) once the common operation is included.

**Proposition 3.2 (covariant-order collapse).** Suppose the retraction order is a function of content, \(\Omega=\Pi(T)\), equivariant under pinned automorphisms: \(\Pi(\sigma T)=\sigma\Pi(T)\). Then for every \(\sigma\) fixing \(o\) and \(a\), the receiver's record on \((T_{\sigma\ell},\Pi(T_{\sigma\ell}))\) equals that on \((T_\ell,\Pi(T_\ell))\), under every reading. In particular, W2 is never separated by such a rule.
*Proof.* \((T_{\sigma\ell},\Pi(T_{\sigma\ell}))=\sigma\,(T_\ell,\Pi(T_\ell))\). Records are indexed by step and by \(a\)'s address, both fixed by \(\sigma\). ∎
Example: "smaller branch first" gives \((1,2,4)\) on both, and "larger first" gives \((1,3,4)\) on both.

**Corollary 3.3 (G vs (2)).** For symmetric swap pairs, preparability is equivalent to **order contingency**. Given N2-covariance, \((T_v,(u,v))\) is admissible iff \((T_u,(v,u))\) is. So the pair is reachable with a common operation iff both orders of the incomparable retractions are admissible for the same content. E-anc grants this, since ancestry is the only constraint. The program's negative results on selection (v13.23 "not a selector"; v15.55 RESPONSE_NONUNIQUE) are exactly what supplies it. Constructive guidance for (2): derive that pruning **occurs**, for example from finite capacity, and the order of **comparable** retractions, but do **not** fix the order of pinned-symmetric incomparable retractions from content. Doing so would make W2-type distinctions unpreparable. W1-type distinctions survive any forced order (Proposition 3.1).

## 4. Mission ledger after this draft

| Ingredient | Status |
| --- | --- |
| Native distinction | W1: location of a legitimate append (pinned-tree invariant). W2: append location relative to the common order. **EXHIBITED** as admissible histories, conditional on **N** |
| Preparability G | Upgraded from ASSUMED to **REACHED CONDITIONAL ON N** (modal). Causal emission \(P_{\mathrm{emit}}\) not needed and still open. **Not closed** |
| Update rule | Retraction: EARNED (ledger). Common \(\Omega\): admissible by E-anc, **SUPPLIED** as a choice. Occurrence SUPPLIED |
| Retained consequence | Shell arrival (Theorem 2.2): EARNED from ledger Theorem 11.1 |
| Receiver identity / access | Identity = pinned ancestry path, the same in both (Lemma 2.1). Reading the record: **A / R\(_{\mathrm{inc}}^-\) NOT DERIVED** (W1 needs only present-record access with a fixed unit; W2 needs the own history) |
| Separation | EARNED: Theorem 2.2, Propositions 3.1–3.2 |
| Ledger point | EARNED: Theorem 11.5, redistribution of the split bit |

## 5. Honest novelty

The mathematics is elementary: additive pushforward on a tree. Known analogues are alternative histories from a common past (decoherent/consistent histories), which treat preparation as the past branch rather than an external agent; the data processing inequality, which gives global nonincreasing under a fixed source-independent \(\Omega\); and which-path/ordering information. No claim is made against these. What is new for the program:
1. G is restated as **modal reachability** inside the pinned ledger, separated from causal emission. That removes the dependence on \(P_{\mathrm{emit}}\).
2. The exact separation criterion is **arrival-step inequality** (Theorem 2.2).
3. The **covariant-order collapse** (Proposition 3.2 / Corollary 3.3) shows the two open premises constrain each other. A derived arrow that forced all orders covariantly would make the symmetric grade witness unpreparable. So the arrow to derive is "occurrence plus comparable order", not "total order".
4. **W1** is a gauge-invariant preparable distinction whose transfer is robust to how the pruning order is eventually derived.

**Relation to proteinfolding-gpt's `86390b26`** ([PREPARABILITY_COMMON_PREDECESSOR.md](../../source_withdrawal_completion/PREPARABILITY_COMMON_PREDECESSOR.md), committed during this run and credited here). That note earns level 2 of its three-level hierarchy (admissibility, reachability from a common seed, actual generation) for the *nested-support* witness: support edits from a common seed, receiver support fixed, palette-invariant intersection \(2\) vs \(1\). It explicitly leaves open the pruning-ledger *grade* case and any typed map into it. The present draft is that complementary case, built natively in the ledger's own carrier with no support-to-grade map. Here the common predecessor is the pinned prefix \(P\) and the branch primitive is a legitimate append (N). This draft also reaches level 2 only, conditional on N, and does not claim level 3. The two gauge treatments match: in both, distinctness is proved by a relational invariant that is not granted to the blind receiver (there, intersection with the reference branch; here, append location relative to \(\Omega\)).

## 6. Exploratory check (not evidence)

Scratch script `/tmp/prep/chk7.py`, not committed, no preparation mechanism. Random trees with 3–8 atoms, random common \(\Omega\), all append-location pairs: 27868 pairs, 0 violations of Theorem 2.2(1). W1/W2 histories reproduced as above. Independent producer/checker verification follows the freeze, per construction mode.

## 7. Next

(a) Draft 2: replace the supplied common \(\Omega\) by a capacity-forced occurrence (finite retained capacity \(K\) forces removal once the append exceeds \(K\)). Test whether the forced set of removals, with contingent order among incomparables, still separates W1 and W2. This is premise (2) restricted to occurrence.
(b) Tie N2 to the V997/V994 pin conditions line by line, so N is cited rather than read in.
(c) Then freeze, preregister, run producer and checker, and send to Gemini via Actions.


## GPT extension: two locations and complete-fiber endpoint (2026-10-17)

[TWO_LOCATION_EXTENSION.md](TWO_LOCATION_EXTENSION.md) traces the original V997 validator and separates syntactic certificate continuity from semantic parent-location permission. W1 needs only two certified append locations, not universal N2. Complete contraction of the receiver's strict descendants gives order-independent present-state contrast using a common root reference, including when the outside entry is removed. This explicitly changes the proposed readout to a receiver/reference pair; its access, append semantics and actual contraction remain open. Author analytical extension; independent review pending. Original draft claims are preserved above, not recertified by this link.
