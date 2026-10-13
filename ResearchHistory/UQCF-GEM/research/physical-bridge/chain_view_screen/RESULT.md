# Single-address views: profile blindness and a surviving conditional record

Date: 2026-10-13 UTC.
Immutable source parent: `68784b317391bd35c460b535fffef0aa19bf2f0f`.

**Scoped analytical corollaries and source assessment. Native event action and receiver access remain OPEN.** These deductions use the inherited finite-tree incidence representation and an already-published source pair. There is no new preparation, numerical experiment, originality claim, physical law, or numbered-stage certification. Independent argument review and publication evidence are preserved separately.

## 1. Why inspect an ancestry chain?

The approved question asks what follows from information already justified as available to a native event. The inspected v15.56 source modules conditionally bind a source event to a Genesis identity and full lineage address. A full address supplies structural ancestry; the immediate prefix is an incidence parent when retained. They do not supply a current indexed view, its physical update, or a receiver's access to its output.

A possible minimal representation is to assign one bound address to each indexed view and take that view to be exactly the address's ancestor chain. Given that representation contract, one address determines the complete mathematical view. However, adopting this as the actual event-to-view representation is a further premise: a localization address is not automatically an entire retained view. Certification, current membership, index/reference binding and actual update/access remain separate obligations. A historical or foreign address alone is not evidence of present same-carrier membership.

This note asks what that candidate representation would permit. It finds two distinct answers:

1. Same-carrier pruning of chain-valued views is invisible to the entire local hitting profile. A positive hitting increment requires the edited view to span at least two sibling children at the affected parent.
2. This is not blindness of every retained record. In the previously published five-vertex raw-membership example, all views are chains and every proper same-carrier pruning already separates the two prepared sources at the designated membership bit. This does not require completion beyond that first edit, a full-profile decoder, or an extra universal-safety restriction on the actually allowed pruning relation.

Neither conclusion supplies a physical event. The second is a useful correction to making profile change, or a branching view, a universal requirement for the user's milestone.

## 2. Inherited objects and a local zero-increment lemma

Let T be a fixed finite rooted tree with root o, P a fixed finite nonempty indexed palette, and (Y_i) a family of root-containing prefix-closed views covering T. All indices, addresses and any supplied orders are preserved. Define S_x={i:x belongs to Y_i}. Every support is nonempty and child supports are contained in parent supports. At an internal vertex v let

\[
A_i(v)=Y_i\cap\operatorname{Ch}_T(v),\qquad
h_v(Y)=\min\{|I|:I\subseteq P,\ \bigcup_{i\in I}A_i(v)=\operatorname{Ch}_T(v)\}.
\]

Use h_v=0 at leaves. Here h_v is the LOCAL child-cover/hitting number, denoted tau_v in v16.25/v16.26; it is not those sources' global consistency order h=max(1,max_v tau_v). A chain view has no two incomparable vertices, equivalently it meets at most one child at each parent.

An atomic native pruning deletes a nonroot vertex c from one view Y_i, with c terminal in that view and another view still covering c. Thus prefix closure and the literal union T are preserved. By inherited v16.26 locality only h_v, where v is the parent of c, can change. Refinement monotonicity makes it nondecreasing; its possible increment is zero or one.

**Local lemma.** If A_i(v)={c} before this edit, its increment is zero.

Proof. Choose any old minimum cover I of the children of v, of size t. If i is absent from I, the same cover survives. If i belongs to I, same-union admissibility supplies an index j other than i still containing c. Since i covered no other child, (I minus {i}) union {j} covers every child after the edit and has cardinality at most t. Hence the new minimum is at most t. Monotonicity gives the reverse inequality, so it equals t. If j were already in I, the proposed smaller cover would also cover the old family, contradicting old minimality; no hidden cardinality exception arises. All other h coordinates are unchanged. QED.

Consequently, a positive atomic increment requires |A_i(v)|>=2 BEFORE that edit. This condition is necessary, not sufficient. The inherited exact criterion remains that every old minimum cover is destroyed by the deletion. The local lemma is an elementary corollary of those same cover arguments, not a replacement for their exact criterion.

## 3. Chain pruning leaves the whole profile fixed

**Chain-pruning corollary.** Let Z_i be a same-union prefix-closed refinement of Y_i. Suppose every index whose view changes had a chain view initially. Then h_v(Z)=h_v(Y) at every vertex. Other, unchanged views may branch arbitrarily.

Proof. Use the inherited v16.26 factorization: remove terminal vertices outside each target Z_i, retaining every target view throughout. Because the target family covers T, every removed vertex remains covered by another target view. Only the designated changed indices need editing, and every subview of an initial chain remains a chain. Each atomic deletion therefore satisfies the local lemma. Finiteness and composition give equality of the entire profile at the endpoint and at every step. QED.

In particular, if all views are chains then

\[
h_v=|\operatorname{Ch}_T(v)|
\]

for every v. Indeed, each selected view covers at most one child, so at least the number of children is necessary. The covering assumption supplies a view for every child; these indices must be distinct because no chain contains two siblings. This supplies a cover of exactly that size. At leaves both sides are zero. Thus this profile depends only on the carrier's arities throughout any same-union chain refinement. Any scalar function of the profile, including the inherited global consistency order, is also unchanged.

This is a restricted invariance statement. It says nothing about changing the carrier, adding incidences, reassigning indices, or modifying a branching view. It also does not say that the supports themselves cannot change.

Two analytical controls make the boundary explicit. These are hand-proved controls, not new executed tests or prepared physical models.

**Branching can matter.** On a star with two children x,y take Y_a={o,x,y}, Y_b={o,x}, Y_c={o,y}. Removing x from a preserves the union and changes the root hitting number from one to two. The edited view initially spans both siblings, as required.

**Branching is insufficient.** On the same star take Y_a=Y_b={o,x,y}. Removing x from a preserves the union, but b still covers both children and the hitting number remains one. Thus the necessary condition is not promoted to an event trigger.

## 4. The existing chain-valued record has exactly one proper pruning per source

Reuse section 4 of `COUPLED_C3_VIEW_LOCAL_PRUNING_RESULT.md` verbatim at the level of mathematical preparation. No vertex, support, source assignment or consumer is changed. T has root o with children u,C, and u has leaf children r,w. The ordered palette is P={a,b,c,d}. Initial supports are:

| Vertex | Source zero | Source one |
|---|---|---|
| o | {a,b,c,d} | {a,b,c,d} |
| u | {a,b,c} | {a,b,c} |
| r | {a} | {b} |
| w | {c} | {c} |
| C | {d} | {d} |

All four views are chains. In source zero they are Anc(r), Anc(u), Anc(w), Anc(C) for a,b,c,d respectively. In source one the a and b views exchange their endpoints r and u. The common internal profile is (h_o,h_u)=(2,2), in agreement with the arity formula. The restricted memory R=1[a absent at u] starts at zero in both preparations. The complete inputs already differ at r; this is not a claim of source separation from identical complete inputs. Unlike the later first-response family, the source preparation here changes TWO indexed views at the leaf r, not only one.

**Complete endpoint classification.** In source zero, every same-union pruning retains a at r, c at w and d at C because their singleton supports cannot become empty. Prefix closure therefore forces a and c at u. The root is fixed. The only optional initial incidence is b at u. Thus there are exactly two pruning endpoints: identity and -b(u). In source one the same argument protects b at r, c at w and d at C, forcing b and c at u. The only optional incidence is a at u, so the two endpoints are identity and -a(u).

Both nonidentity endpoints are single native leaf deletions. They preserve the carrier and the profile (2,2), and their total deficit relative to that initial profile is zero. These are all proper same-union contractions, so no choice of pruning site, completion rule, maximal-command availability, or additional band enforcement is needed to prove this finite-family statement. Every proper pruning gives

\[
R_{\mathrm{out}}=0\quad\text{for source zero},\qquad
R_{\mathrm{out}}=1\quad\text{for source one}.
\]

The old result already exhibited these edits under H_T and proved positive-record soundness under pruning. The present observation is the exhaustive two-endpoint classification and its chain/profile interpretation; it is an analytical clarification of that existing witness, not a new physical mechanism or a newly prepared source pair.

**A partial certificate is enough to justify the optional local edit conditionally.** Set K=Anc(r)={o,u,r}, positively certified to lie in the current T. It is a strict subset of this T, with no ownership information. The inherited positive-extension theorem gives B_K(Y)={o} union Anc_{K union Y}(Y intersect Leaves(K union Y)). For the view ending at u this mandatory subview is {o}; for each view ending at r,w or C it is the entire input view. Hence its universal independent-view safety bounds permit exactly identity or that one optional edit in this preparation. Full T is not needed as the input to this conditional safety calculation.

These are two different justifications and should not be conflated: the complete endpoint classification is true for the actual prepared states under bare same-union pruning; the K calculation specifies information that would suffice for an independent local rule to justify the edit across all compatible carriers and covers. Neither mathematical fact establishes that an event possesses K or must act. For a two-state comparison, one certified current extension is sufficient for safety of the optional edit, but a stored address unconnected to current retention is not that certificate.

The accessible-input requirement of the declared decoder is small: retained a-membership at the fixed vertex u. No joint hitting-profile read is required. This is a formula for what a receiver would have to read, not evidence that any receiver can read it. Identity remains allowed in both preparations. A zero observation does not identify source zero without a separately justified proper-occurrence condition. Positive R remains a sound source-one record in this restricted prepared family and pruning relation.

## 5. What the source-address route does and does not supply

The source packet binds each inspected file to the immutable parent and its Git blob. Relevant inspected declarations are:

| Source | Positive supplied structure | Remaining connection |
|---|---|---|
| v15.56 `source_binding.py` | A certified record explicitly binding (Genesis, source event, full address) types localization | No assignment of that record to a complete current indexed view or physical update |
| v15.56 `product_identity.py` | Origin, provenance certification and structural ancestry are separately typed | A provenance hash is not a branch coordinate or a present retained-membership certificate |
| v15.56 `retained_incidence.py` | A full address gives its prefix parent when retained; other relations have distinct premises | No derivation of current view ownership, pruning occurrence or output access |
| v16.25/v16.26 proof ledgers | Same-union refinement, monotonicity, locality and factorization | An admissible comparison does not select actual transitions |
| Prior view-local and native-information results | Existing conditional membership record; exact safety envelope with current positive K | Physical acquisition, actual event coupling and receiver access remain open |

These are bounded statements about the inspected interfaces, not an archive-wide absence proof. No additional sweep of the previously audited supplied quantum instruments is counted as discovery here.

For the latest `first_event_separation/RESULT.md` family, m>=2 siblings u_j all initially belong to the same view a, and the profile decoder depends on their shared coverage. That particular prepared a-view is not one ancestor chain. One full bound address plus its prefixes cannot instantiate it by itself. Realizing that profile route would require a justified representation including multiple sibling branches under one index, or another justified architecture. Branching alone still would not cause a response.

However, section 4 shows why this requirement must NOT become a general physical admission gate. A raw membership consumer can work on chains, and this already-published example has a stronger all-proper-prunings property than merely exhibiting H_T. The immediate native questions for that simpler consumer are: does an existing event actually carry the complete chain and a truthful current extension; is a proper same-carrier pruning an earned event relation; and does its output supply retained a-membership at u to a receiver? Address typing alone answers none of those physical questions.

The candidate definition Y=Anc(address) would make complete own-view information computable from a single address IF that equality were established for the actual object. The three inspected source modules establish localization and prefix ancestry, not that equality, its present retention, a physical address-to-view mutation, or receiver access. No additional same-index grouping of unrelated event addresses is inserted here. Other justified representations remain eligible.

## 6. Disposition and next scientific obligation

Disposition: **CHAIN_PRUNING_PROFILE_INVARIANCE; EXISTING_RAW_RECORD_PRESERVED; NATIVE_ACTION_ACCESS_UNRESOLVED.**

This work derives a decoder-specific limit and sharpens the conditional content of an existing record. It does not derive a force, gravity, a metric, energy, an event probability, or the user's native informational-difference milestone. It neither assumes a fundamental clock nor turns combinatorial invariance into a physical conservation law. Time remains pruning / ordered recoverability update.

The next eligible input is a justified native representation/update/access connection. For the chain-valued raw-record route, one must establish current address retention and the relevant same-carrier pruning/output relation; multi-branch aggregation is not required. For the hitting-profile route, the actual edited view must additionally span sibling branches if a positive increment is the intended consumer. Another prepared pruning example cannot settle those obligations.

No numerical scientific execution, historical test replay, GitHub Actions campaign, main merge, or numbered-stage CLOSED/CERTIFIED status is claimed. This proof and its controls were developed by direct reasoning before publication; they must not later be relabelled as unknown preregistered findings. Prior scientific counts and reviewed results are unchanged. Broad C3/C4-C6 and physical origin/access remain OPEN.
