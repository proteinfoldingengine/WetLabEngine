# Independent mathematical and source review — raw record

Review date: 2026-10-13 UTC.
Reviewer role: independent adversarial mathematical/source reviewer, dispatched separately from the author and publication auditor. This record does not modify the reviewed drafts or source packet.

**Verdict: ACCEPTED for the bounded analytical-corollary and source-assessment scope stated below.** No blocking mathematical defect, source contradiction, or physical milestone overclaim was found in the exact reviewed drafts. This verdict does not certify publication closure, authenticate a remote Git tree, recertify historical scientific executions, or establish native input/action/access.

## Exact reviewed bytes and source scope

The review was conducted against these local immutable inputs:

| Input | SHA256 |
|---|---|
| `RESULT.md` | `386fd5536936c703c6fc696920c3f7d28666f2aab1a973de636e353c5244eb0a` |
| `INDEX_APPEND.md` | `17e6f38881a4cd38f4e06b477528c954704c8650db0de9abc82bee04efc7f817` |
| `source_packet.json` | `5a2448b606cf412efdd59c4b1b7018d6b8015602ac23bc77b27891d2f64d46a0` |
| `source_identities.json` | `ba65585959d48e2054da9157f1728b20405023ff11a7a3d752da4ea5ea17dafb` |

Declared source parent: `68784b317391bd35c460b535fffef0aa19bf2f0f`.
Declared source tree: `95adde3efe81e51c362624ba2a5002282f871586`.

I inspected the texts embedded in the packet, including the applicable `ResearchHistory/UQCF-GEM/AGENTS.md`, all three v15.56 source-address modules, both v16.25/v16.26 proof ledgers, the view-local result, native-information boundary, first-response result, pruning-interaction attempt, pruning-record bridge, and continuation index. Long texts were read in segments where needed; truncated output of the older bridge's last sections was subsequently read separately. These are twelve packet sources. I independently recomputed each embedded source's UTF-8 byte length, SHA256 and Git blob object ID and confirmed equality with its identity entry. This is byte/object-identity consistency checking, not a scientific test campaign. I did not independently retrieve the GitHub parent tree or inspect source files outside the packet. Consequently, parent/tree membership and remote publication integrity require the separate publication audit; statements about missing connections are limited to these inspected texts/interfaces. Linked implementation files absent from the packet were not newly inspected and are not represented as newly audited.

AGENTS distinguishes typed general proofs from bounded execution and prohibits converting pruning into energy, action, metric, gravity or fundamental time. The report is explicitly an analytical clarification, not a numbered retained-research stage. It does not claim the scientific execution/closure requirements for such a stage have been satisfied. Its known proof/control findings must not later be represented as unknown prospective findings.

## Proof checks and adversarial findings

### 1. Singleton-child zero increment — correct

Fix a terminal-in-own-view deletion of nonroot c from index i, let v be its carrier parent, and assume A_i(v)={c}. With the carrier and index palette fixed, shrinking the incidence sets makes the child-cover minimum nondecreasing. For an old minimum cover I of size t, either i is absent and I survives, or i is present. In the latter case same-union admissibility gives a different index j retaining c. Replace i by j: all children formerly supplied by i are just c, so the replacement covers the children after deletion with at most t indices. Thus the new minimum is at most t and at least t. If j was already in I, I minus {i} would have covered the old children with fewer indices, contradicting old minimality. This closes the potential replacement-cardinality loophole.

Only the parent coordinate changes: membership of c contributes to the immediate-child family of its parent, while terminality ensures that prefix closure permits the edit. This agrees with v16.26 P1-P3. The lemma uses terminality, another covering index, fixed T, and indexed sets; none is silently omitted. A positive local atomic increment requires an edited view with at least two children of that parent before the edit. It is a necessary condition, and the report does not assert sufficiency. The notation distinction between local h_v/tau_v and the inherited global h=max(1,max tau_v) is explicit and correct.

### 2. Chain-refinement invariance, including unedited branching views — correct

For any stated endpoint Z, choose terminal vertices in current Y_i minus Z_i and retain Z_i throughout. A vertex chosen for removal is not in Z_i, and final cover of T supplies another Z_j containing it. That index retains the vertex at every intervening step. A deepest differing vertex is terminal in the current view: a descendant in Z_i would force its ancestor into Z_i by prefix closure, while a descendant outside Z_i would contradict depth choice. This supplies the advertised legal factorization rather than assuming arbitrary incidence order.

Every view actually edited starts as a chain, and all its intermediate subviews remain chains. Its child-incidence set at an edited parent is therefore exactly the singleton containing the removed child. The preceding lemma applies at every step, regardless of the branching pattern of unedited indices. Finite composition gives equality of all local coordinates and endpoint equality. The quantifier is correctly restricted to changed indices whose INITIAL views are chains. No restriction on unedited indices is needed. The argument does not extend to branching edits, incidence additions, changed indices or changed carrier.

### 3. Arity formula and controls — correct

When every view is a chain, each selected index meets at most one immediate child. A cover of d children needs at least d indices. Existence of a covering index for each child gives d distinct indices, since one chain cannot cover two siblings. Thus h_v=d, with leaves giving zero. Root-only views and redundant identical indexed chains do not affect this argument. Any function of this unchanged profile, including the positive global-order convention, is unchanged. This says nothing about preservation of raw incidence data.

For the first two-child-star control, the original branching a-view alone covers both children, giving one; after deleting x from it every available view covers at most one child, giving two. For the second control an unchanged branching b-view still covers both children, so the value remains one. Both deletions preserve root, prefix closure and union. These are genuine hand-derived countercontrols to an unconditional branching-trigger claim, not executed tests or physical examples.

### 4. Unchanged five-vertex pair: complete endpoint classification — correct

The support table and fixed reference (a,u) exactly match section 4 of the packet's `COUPLED_C3_VIEW_LOCAL_PRUNING_RESULT.md`. The four indices and both leaf-source assignments are unchanged. This is the four-label one-edit view-local witness, not the older three-label two-edit bridge witness.

In source zero, singleton leaf supports force a at r, c at w and d at C to survive. Their ancestors force a,c at u and each relevant root incidence; root support is fixed for all indices. Every nonroot initial incidence is thus mandatory except b at u. Since b's own view ends at u, deleting this incidence is terminal-in-own-view and a,c still cover u. Hence the entire endpoint set is identity and -b(u).

In source one, singleton supports similarly force b at r, c at w, d at C and their ancestors. The only optional incidence is a at u, so the entire endpoint set is identity and -a(u). Both nonidentity endpoints are single admissible edits. No overlooked leaf or ancestor edit remains, and every proper same-union endpoint is the listed endpoint. With initial child arities two and two, the common profile stays (2,2). Relative to that initial q, the inherited total absolute deviation D_q is zero. Band constraints are vacuous for these particular proper endpoints and add no hidden selection premise.

The output bit is zero on source zero and one on source one conditional on a proper pruning. There is no completion, site-selection, maximal-command-availability or universal local-information restriction needed for this actual-state endpoint statement. Identity remains allowed; without proper-occurrence information an observed zero also fits source one's identity. Positive absence at (u,a) is sound in the specified prepared pruning family and persists under further deletions. This property is conditional historical/source soundness, not an actual occurrence assertion.

### 5. Partial K safety calculation — correct, with the stated information premises

Let K={o,u,r}. It is prefix closed and strictly smaller than the five-vertex T. For Y=Anc(u), K union Y=K has leaf r, which is absent from Y; therefore B_K(Y)={o}. Its only root-containing prefix-closed suboutputs are {o,u} and {o}. For Y=Anc(r), the leaf r is in Y and B_K(Y)=Y. For Y=Anc(w), leaves of K union Y are r,w and Y contains w, whose ancestor hull is all of Y. For Y=Anc(C), leaves are r,C and Y contains C, again forcing all of Y. Thus every other input view is fixed and exactly the same optional local edit is allowed in either preparation.

The independently checked native-information-boundary necessity/sufficiency proof supports these bounds: necessity takes T=K union Y and makes a candidate leaf exclusive to one view; sufficiency preserves actual global leaves, which remain leaves of K union Y. The atomic condition requires a STRICT descendant in K, so r witnesses redundancy of the terminal u. Membership of u alone would not suffice. No ownership assertion for r is required, since cover and prefix closure supply another view containing u when r is absent from the edited view. Complete own-view information remains necessary for this contract's terminality/absence information. The report does not infer it from K alone.

There are two different quantifiers here: actual endpoint classification on the two fixed preparations, versus independent-view safety across every compatible carrier/cover given the same input. The report separates them. It does not require universal independent-view safety as an extra restriction to obtain separation of the already prepared raw record. Its sentence about one current extension certifying safety is read with the complete-own-view/local-terminal premise maintained by the surrounding discussion; it does not license safety from an address alone.

### 6. Raw record versus profile — correct; no invented information

The complete preparations already differ at r in TWO indexed views a,b. The chain-profile theorem therefore leaves the complete informational distinction intact; it only excludes a changed hitting-profile consumer. The restricted membership record at u initially agrees, and proper pruning moves the distinction into that coordinate. A processor already given its complete relevant input view does not gain previously unavailable source information. A distinct receiver could use the stated bit only if its input delivery/access and the action coupling were justified. The report explicitly retains these missing obligations.

The record's first-proper-response property is a sharper analytical reading of an existing fixture, not a new preparation, physical mechanism or numerical campaign. The prior view-local result already displayed the same edits, profile equality and soundness under pruning. The current report claims only exhaustive endpoint classification and chain interpretation beyond those inherited facts. This avoids prior-result overcounting.

### 7. Difference from the newer first-response family — correct

In packet `first_event_separation/RESULT.md`, m>=2 children u_j of p initially all lie in the SAME a-view. This view therefore branches. The preparation changes only a's global-leaf incidences, keeping all other indexed views fixed. Its all-proper-output claim uses the universal positive-extension safety envelope; its explicit globally-leaf deletion control shows failure under bare actual same-union pruning. In the older five-vertex pair a,b both change at r, and singleton supports make bare same-union pruning sufficient for the all-proper-output record.

The newer family also already gives a one-view membership decoder equivalent to its profile bit on that family. The current report does not deny this or assert that a full-profile sensor is essential. Its branching requirement is specific to representing that shared-sibling a-view and to obtaining a positive hitting increment; it is not a general admission gate for every native accessible-record route. One address and its ancestors cannot represent multiple siblings under a single index. Other justified multi-address or other architectures remain eligible, and branching alone does not force action.

### 8. Source-address assessment — accurate within inspected interfaces

`source_binding.py` declares conditional typed localization from Genesis, source event and full lineage address, with provenance commitment separately required for certification. `product_identity.py` separates origin, ordered-history commitment and structural ancestry and requires explicit source/address binding. `retained_incidence.py` makes prefix-parent incidence conditional on retention and gives separate premises for repair succession/recoverability/dependency. These files do not assert Y_i=Anc(address), assign a complete current indexed view, generate a present-carrier certificate, implement selective indexed pruning, or deliver the membership bit to a receiver.

These are declaration/interface findings. They are not proof that no other file or actual mechanism can supply such connections. The report consistently limits its absence claim to inspected modules and refuses to turn historical/foreign addresses into current same-carrier membership. Its hypothetical Y=Anc(address) is expressly an additional representation contract. Once that equality and binding were actually established, address prefixes would compute the mathematical chain; that conditional implication is valid. No unjustified same-index grouping or permutation-based loss of existing identities is introduced.

### 9. Scientific and physical scope — maintained

The report and proposed continuation entry both preserve native representation/current retention, actual event relation, proper occurrence and receiver access as open. They derive no law forcing a nonidentity output, probability, physical force, metric, energy or gravity, and no fundamental clock. The admissible pruning relation and its safety proof do not select an actual transition. No milestone can be credited from the profile invariance or record example alone. The supplied source/address structures remain useful conditional premises; they are neither erased to manufacture an impossibility nor promoted to physical access.

No numerical scientific execution, state enumeration, simulation, historical replay, new source preparation, campaign count, main merge or numbered-stage closure was performed in this review or asserted by the reviewed drafts. The index append is a faithful concise summary of the report and adds no stronger claim. Historical numerical counts and older reviewed scientific claims are not independently recertified here.

## Independent conclusion

**ACCEPTED** for the exact reviewed drafts as a bounded analytical corollary and source assessment. The zero-increment lemma, chain-pruning invariance, arity formula, controls, fixed-pair endpoint classification and partial-certificate calculation are correct under the stated premises. The raw-membership/profile distinction and comparison with the newer first-response family are sound. No required mathematical correction was identified.

Native input/action/access and the user's native informational-difference milestone remain unresolved. Publication provenance/closure is outside this mathematical review and must be checked separately against the declared parent and final publication bytes. This review's acceptance applies only to the hashes above; it must not be silently transferred to later changed drafts.
