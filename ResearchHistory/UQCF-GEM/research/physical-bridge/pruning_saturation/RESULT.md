# Total-deficit saturation under completed pruning

Date: 2026-10-12 America/Phoenix / 2026-10-13 UTC.
Immutable source parent: `3b3b1e2d97c0381a05625fff8851cc813e8e2a24`.

**Scope: conditional analytical result. Native execution and accessible readout remain OPEN.** Independent argument review and publication evidence are recorded separately in this directory. No numbered-stage certification, numerical campaign or physical-force derivation is asserted.

## 1. Question and precise advance

The user's milestone permits an accessible consequence to be forced without uniquely selecting every microscopic detail. The earlier pruning endpoint theorem establishes reachability of a fixed endpoint, and v16.26 establishes increments and telescoping along a fixed endpoint factorization. The present question changes the endpoint quantifier: when all legal atomic deletions inside a declared retained interval remain available, do **all unextendible paths**, possibly ending at different states, have a common total consistency deficit?

The answer in the class below is exactly

\[
D_q(F_{\rm end})=\min\{B,D_q(W)\}.
\]

Here W is the least state in the declared interval, q is the initial exact local hitting profile, and B is an integer budget for the sum of local deficits. When W lies in the budget, every such path reaches W. When W lies beyond it, every such path exhausts B, even though its exact endpoint and local deficit profile may differ.

For the previously classified leaf-preserving envelope, W is the inherited leaf-generated hull H_T(S). No source-dependent pruning mask is chosen in the example below. A pair with identical initial internal supports and hitting profile then gives different completed total deficits, independently of which allowed deletion is chosen next.

This is a conditional consequence of the inherited native incidence arithmetic, not a newly selected physical response law. The occurrence of a path, restriction to this envelope, absence of extra command restrictions, actual continuation to an unextendible state, budget enforcement and access to the resulting profile are separate premises. None is obtained by naming the final scalar a record. The result therefore does **not** meet the native-event milestone by itself.

## 2. Native objects and the declared path class

Fix a finite rooted tree T and a finite nonempty indexed palette P. Every support state S has S_o=P, nonempty S_v, and S_child contained in S_parent. Equivalently, Y_i={v:i in S_v} are root-containing prefix-closed views covering T. Work on this same literal incidence carrier; no cross-carrier encoding is introduced.

At an internal vertex v, h_v(S) is the minimum number of labels meeting every immediate child support. Fix an initial state S^0 and q_v=h_v(S^0). For any native state F define the inherited total deviation

\[
D_q(F)=\sum_{v\text{ internal}}|h_v(F)-q_v|.
\]

This is the sum over local coordinates, not the maximum of them, a lexicographic barrier, energy, or physical duration. Fix an integer B>=0.

Supply a second native state W<=S^0 on the SAME T and P. The interval is W<=F<=S^0, with inclusions at every vertex. Both endpoints cover T. Consider the directed graph whose vertices are native states in that interval with D_q(F)<=B. Its edges are **all** single-incidence deletions that remain in that vertex set. A deletion removes one label at one nonroot vertex. It must preserve prefix closure and nonempty supports.

An unextendible path ends at a vertex with no outgoing edge in this graph. It need not be a longest path. Finite histories stopped earlier are also legitimate mathematical histories, but are not covered by the completed-endpoint conclusion. In the physical framework, NOOP and nonoccurrence are not removed by this definition. We do not assert that an actual event stream reaches a graph sink, supplies a terminal flag, or has any probability distribution.

There are no additional floors, command restrictions or other resource bounds here. Extra lower support floors would be harmless if W satisfies them, because every intermediate support contains W's support; otherwise they require a separate analysis. Nonnegative deviations from q automatically preserve any inherited lower hitting bound q_v-1, but that does not discharge unrelated C3 constraints.

## 3. Inherited ingredients and complete proof

### Lemma A: refinements are monotone in every local hitting coordinate

If E<=F, every label set hitting the smaller child supports also hits the larger ones. Therefore h_v(E)>=h_v(F). On this interval,

\[
q_v\le h_v(F)\le h_v(W),\qquad
0\le D_q(F)\le D_q(W).
\]

All signs in D_q are nonnegative on this interval. This is the inherited v16.25 refinement monotonicity, not a new monotonicity claim for additions or changed carriers.

### Lemma B: an atomic deletion raises total deficit by zero or one

Deleting label i at nonroot u changes only the child-support family at p(u). By monotonicity its hitting number cannot decrease. Let C be a minimum hitting set before deletion. If it still hits all children afterward, the value is unchanged. Otherwise u was hit only by i within C. Native nonemptiness supplies some remaining j in the new S_u. Then C union {j} hits every child afterward and has at most one additional label. Consequently the changed hitting number rises by at most one, and all other local coordinates are unchanged.

Because these local coordinates lie above q, the total D_q also increases by either zero or one. This is a direct application of v16.26's locality and atomic bound to the inherited summed budget.

### Lemma C: every F above W has a native atomic descent toward W

If F!=W, choose a deepest vertex in Y_i^F minus Y_i^W for some differing view. It is a nonroot leaf of Y_i^F: any retained descendant belonging to W would force its ancestor into W, and a deeper descendant outside W contradicts the choice. Remove that incidence. Prefix closure is preserved. W still contains each vertex in some view, so the removal cannot empty a support or change the common union. The result F' remains in [W,F].

This lemma does not yet impose the budget. It is the constructive atomic-factorization argument of v16.26 and the earlier endpoint theorem.

### Theorem: every unextendible budget-admitted path has the same total deficit

Write L=D_q(W). Any path has at most sum_v |S_v^0 minus W_v| proper deletions, so no infinite sequence of proper edges exists. This gives a combinatorial length bound, not a physical progress law.

If L<=B, Lemma A makes every native state in the interval budget-admitted. Every F!=W has a further admitted deletion by Lemma C. The only sink is W, so every unextendible path ends there and has deficit L.

If L>B, a budget-admitted endpoint F cannot equal W. Lemma C supplies a native next deletion F'. If D_q(F)<B, integrality gives D_q(F)<=B-1; Lemma B then gives D_q(F')<=B. That edge would be admitted, contradicting unextendibility. Thus every sink satisfies D_q(F)=B.

In both cases D_q(F_end)=min(B,L). A path to some sink exists: whenever an outgoing edge is available, choose one; the strictly decreasing finite incidence count eventually terminates. This existence construction does not select the physically realized command or require actual continuation. QED.

The new conclusion concerns a variable terminal endpoint. It is stronger than telescoping after a final state has already been fixed. It remains an elementary consequence of the inherited finite order and unit increment; no mathematical novelty priority or new law of nature is claimed.

## 4. Specialization to the inherited leaf-preserving envelope

For the same supplied T, define H_T(Y) as the root together with all ancestors of the global leaves of T that Y contains. When |P|>=2, the earlier view-local safety classification proves that an independently applied contracting view map, universally preserving T over every cover, must retain H_T(Y). Its componentwise least output at the initial cover is

\[
W_o=P,\qquad
W_v=\bigcup_{\ell\in L(T),\ v\preceq\ell} S^0_\ell
\quad(v\ne o).
\]

The hull is native and covers T, so the saturation theorem applies to the interval W<=F<=S^0. With a singleton palette, every actual covering view is all of T, the hull is T, and S^0=W; the interval is trivial. No pointwise universal-safety classification on non-cover singleton inputs is inferred. Every state in the hull interval preserves every original global-leaf incidence. Conversely, any refinement of S^0 preserving those incidences must contain W by prefix closure.

The hull remains the same along this interval because the global-leaf incidences do not change. W is therefore a mathematical bound on the allowed retained states, not a prescribed exact endpoint when its deficit exceeds the budget. The theorem does not demand that an inadmissible hull be reached.

The local universal-safety envelope does not derive the separately imposed global band check or a scheduler. Filtering its atomic deletions by the band may require information unavailable to a native event. In particular this note does not relabel a full-state verifier as a local guard or derive actual independent physical processing.

## 5. Source pair: a common coarse result with different microscopic endpoints

Use T with root o, children u_1,u_2,u_3, and two global leaves r_j,w_j below each u_j. Let P={a,b_1,b_2,b_3,d}. Both preparations have the same ordered tree, palette, reference convention, budget B=1, and internal supports:

| Vertex | Source zero | Source one |
| --- | --- | --- |
| o | P | P |
| u_1 | {a,b_1,d} | {a,b_1,d} |
| u_2 | {a,b_2} | {a,b_2} |
| u_3 | {a,b_3} | {a,b_3} |
| r_j and w_j, each j=1,2,3 | {a,b_j} | {b_j} |

All supports are nonempty and nested. At the root, a hits all three child supports. At each u_j the two child supports are equal and have hitting number one. Thus both initial profiles are

\[
q=(h_o,h_{u_1},h_{u_2},h_{u_3})=(1,1,1,1).
\]

The entire initial internal support record is identical, not only its total deficit. The complete preparations differ in the leaf incidences; their native physical initialization is not derived here.

For source zero, the hull removes only d at u_1. The label a occurs in global leaves under every u_j, and every b_j is similarly retained. The hull has profile q and L_0=0. There is one unextendible endpoint, reached by that one zero-deficit deletion.

For source one, the hull removes d at u_1 and a at each u_j. It leaves S_{u_j}={b_j}, so its root hitting number is three and the other three coordinates remain one: L_1=2. The hull lies outside B=1.

The only potentially removable incidences in source one's hull interval are d at u_1 and a at the three u_j. Deleting d never changes the hitting profile. Deleting the first a raises the root hitting number from one to two. Deleting a at a second u_j would require three labels to hit the three child supports, irrespective of whether d is still present, so it violates B=1. An endpoint with no a deletion still has an admitted a deletion; an endpoint retaining d still has its admitted deletion. Thus there are exactly three unextendible endpoints: d is removed and a is removed at exactly one of the three u_j. These are deductive cases, not numerical test counts.

Every source-one endpoint has profile (2,1,1,1). Applying the SAME path-class definition to both preparations forces

\[
R(F_{\rm end}):=D_q(F_{\rm end})=
\begin{cases}0,&\text{source zero},\\1,&\text{source one}.\end{cases}
\]

Both completed paths involve actual nonidentity edits, so this example does not compare an unchanged zero source with an edited one source. The source-one result is independent of which branch receives the a deletion and whether d is removed first or second. No probability or preferred branch is supplied. D_q is invariant under simultaneous transport of the full tree, labels and initial profile; the response is not just a renamed endpoint.

This is a **conditional source-to-profile consequence**. R is a mathematical quantity computed from internal supports, not an earned physical observation. The initial internal memory agrees, but the complete source states differ. The theorem moves that distinction into a coarser internal profile only for the declared completed histories. It does not derive acquisition by a native receiver or implement the C3 restored-marker consumer.

## 6. Controls and limits

**Early stopping.** Source one can remove d and stop with D_q=0, exactly the internal endpoint record of completed source zero. Hence R=0 does not identify source zero without the completion premise. A positive R=1 is sound for source one within this leaf-preserving interval even before completion, since source zero cannot reach positive deficit there. Actual receipt of that positive signal is not guaranteed by admissibility. This is a control on this theorem's quantifier, not a new all-NOOP obstruction.

**Leaving the leaf-preserving envelope.** Under unrestricted same-union native pruning, source zero can delete a from all six global leaves, keeping every h_v=1, and thereby reach source one's initial state. It can then delete d and one a at a u_j to reach the SAME full positive endpoint within B=1. The eight-edit counterhistory is deduced directly. Thus the source comparison is not sound for all pruning histories. This is consistent with the earlier protected-record theorem: source one is a substate of source zero, so its endpoint is reachable from source zero in the unrestricted class. The universal view-local leaf constraint, if physically earned, would exclude that counterhistory; this note does not earn it.

**The fixed scalar does not imply a fixed local profile.** In the general interval theorem, take root children p and z with disjoint fixed supports {a,b,c} and {d,e,f}. Give p two leaves with supports {a,b} and {a,c}; give z two leaves {d,e} and {d,f}. Let W remove a from both p leaves and d from both z leaves, leaving the internal supports fixed. Initial profile is (2,1,1), W's profile is (2,2,2), and B=1. Completing either arm uses the budget; the other arm's first deletion is then forbidden. The two sinks have profiles (2,2,1) and (2,1,2), both with D_q=1. This control belongs to the general interval theorem, not the H_T specialization; its global-leaf incidences change.

**All atomic edges and integer unit budget matter.** The theorem's sink is defined using every native interval deletion passing the band check. An added command restriction can create a false sink below min(B,L); a procedure allowing only the full source-one hull update would have none of its proper atomic alternatives and would be blocked at deficit zero. Weighted costs or larger indivisible moves need their own increment argument. No such additional premise is silently included.

## 7. Scientific disposition and next obligation

The analytical advance is a common total response across all completed legal pruning orders, including cases with different final states, plus a source pair showing how that common response can distinguish initially identical internal profiles. It removes the need to select a particular deletion order **for this scalar conclusion**. It does not remove the need to derive the actual interaction class, completion or receiver access.

The next physical question is therefore more specific than choosing a useful update: does any already justified native event enforce this retained envelope and budget, produce the relevant completed or positive partial response, and make that response available to a retained receiver? A justified positive partial response could qualify without proving universal completion. Maximal pruning, a terminal flag, global profile access, an acknowledgment or a probability law may not be inserted to answer that question.

The current native-event milestone remains OPEN / NOT ACHIEVED. Conditional RAS/RCR, source binding and grade, actual retained inclusions and positive response results remain intact. No stopped absolute source-to-GR route is reopened. Path A remains active; Path B remains closed. Time is pruning / ordered recoverability update; the finite edit bound is not a fundamental clock.

The formulas and controls in this document are analytical findings known before any possible future numerical preregistration. No scientific code was run, no historical test count increased, and no full inherited suite, physical force, main merge or numbered-stage CLOSED/CERTIFIED status is claimed. Any later numerical campaign must prospectively freeze its scope and satisfy AGENTS.md; it cannot retroactively call these deductions unknown predictions. This note relies on complete proofs and separate argument/publication review, with no claim of archive-wide novelty.

## Exact source trail

`source_packet.json` preserves the exact current source texts and parent index. `SOURCE_READBACKS.json` binds their bytes to Git blob IDs and SHA256 digests at the source parent. The mathematical dependencies are v16.25 TYPE_AND_PROOF, v16.26 TYPE_AND_PROOF, v16.53 NATIVE_ADMISSIBILITY, COUPLED_C3_PRUNING_RECORD_BRIDGE and COUPLED_C3_VIEW_LOCAL_PRUNING_RESULT. The remaining sources supply the user's milestone, frontier/gate boundaries and repository scientific requirements. Previously established monotonicity, atomic bounds, endpoint reachability and hull classification are used explicitly rather than counted again as discoveries.
