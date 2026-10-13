# First-response separation under view-local carrier safety

Date: 2026-10-12 America/Phoenix / 2026-10-13 UTC.
Immutable source parent: `c96ff8b9ae0d3b3c07d4e56b51c28e4f256f3f5a`.

**Conditional analytical result. Native input availability, action and receiver access remain OPEN.** This note constructs a mathematical witness family and proves its entire permitted-output claim. It does not construct or discover a physical law. Independent argument review and publication evidence are preserved separately.

## 1. Question and advance over saturation

The preceding saturation theorem fixes the total deficit of every unextendible pruning path in a declared interval. It does not require a unique endpoint, but it still conditions its conclusion on reaching a sink. Its source pair permits an initial zero-response deletion in source one.

Can a source difference constrain the **first proper response**, without selecting a deletion location, requiring all commands to be available, or requiring completed pruning?

The answer is yes in the explicitly conditional information class below. For every integer m>=2 there are two preparations with:

- the same literal tree, ordered palette, partial current-carrier evidence K, initial internal supports and local hitting profile;
- a difference only in global-leaf incidences of the SAME indexed view a;
- a retained internal-profile bit R that is zero initially in both preparations;
- R=0 after every proper output of source zero, and R=1 after every proper output of source one, whenever the output satisfies the inherited universal independent-view safety bounds.

For a single native incidence deletion, the total deficit is exactly zero versus one. The unit-band inequality follows for that first step from the inherited atomic increment bound; a runtime full-state band filter is not needed to prove that inequality. For larger proper contractions the bit still separates the sources, but the unit band need not hold.

On this family the same bit also has a decoder using just the retained a-view at the known children of p in K. It does not require a full joint hitting-profile read. This is a mathematical reduction of the readout input, not a derivation that an event or receiver has access to that input.

This removes completion, a chosen site and maximal availability of commands from this conditional response. It does **not** derive the input certificates, event access, the physical applicability of the information/safety contract, occurrence of a proper action, or receiver access to R. An actually carrier-preserving deletion outside this information contract can fail the source separation. The explicit control below is essential.

## 2. Exact inherited information and safety contract

Use the native finite rooted-tree support representation: root support P, nonempty supports at every vertex, and child supports contained in parent supports. A label i defines a complete prefix-closed view Y_i; their union is the carrier T. The palette has at least two indices. Existing order and address identities are retained.

The positive-extension theorem supplies the following conditional class. An indexed rule has the COMPLETE own view Y_i and a common finite prefix-closed set K certified to belong to the same CURRENT carrier. It has no other view memberships or additional carrier description. It contracts its view, and carrier preservation must hold for every compatible finite carrier and cover. In the nondeterministic product version it must hold for every Cartesian combination of permitted local outputs. No source-family, fixed-profile or witness-ownership promise is inserted into that universal quantifier.

For Q=K union Y define

\[
B_K(Y)=\{o\}\cup\operatorname{Anc}_Q\bigl(Y\cap L(Q)\bigr).
\]

The inherited necessary-and-sufficient safety bound is

\[
B_K(Y_i)\subseteq Z_i\subseteq Y_i.
\]

Equivalently, a nonroot own-view leaf v can be deleted atomically with universal safety from this input if and only if K contains a strict descendant of v. A positive fact that v itself exists is insufficient. These are inherited results, not new theorems of this note.

We prove the response for EVERY joint output satisfying these bounds. Once the bounds hold, the proof does not care how the allowed outputs were chosen or correlated. We do not assert that the bounds are necessary for correlated or cross-view architectures outside the inherited information class. Nor do we assert that this class describes an already derived physical event.

A **proper output** changes at least one indexed incidence. Identity is allowed by safety and is kept separate. The one-incidence specialization uses the existing native primitive, not a newly introduced simultaneous-update rule. No scheduler, priority, largest-deletion instruction, probability distribution or guaranteed proper outcome is adopted.

## 3. One indexed source difference, with identical internal records

Fix m>=2 and an ordered palette

\[
P=\{a,c,b_1,\ldots,b_m\}.
\]

Arbitrary m here uses the inherited finite-tree definitions and the proof below. It does not extend a certified bounded-arity normalization or connectivity campaign.

The root o has children p and v. Vertex p has children u_1,...,u_m. Every u_j has two global leaves r_j,w_j; vertex v has two global leaves r_v,w_v. All addresses and the distinguished position u_1 are part of the common declared tree/reference, identical in both preparations.

Both preparations have these internal supports:

| Vertex | Common support |
| --- | --- |
| o | P |
| p | P |
| v | {a,c} |
| u_1 | {a,b_1,c} |
| u_j, j>=2 | {a,b_j} |

Only the global-leaf incidences of label a differ:

| Each indicated leaf | Source zero | Source one |
| --- | --- | --- |
| r_1,w_1 | {a,b_1,c} | {b_1,c} |
| r_j,w_j, j>=2 | {a,b_j} | {b_j} |
| r_v,w_v | {c} | {a,c} |

The complete views of c and every b_j are identical across the preparations. The complete view of a differs, so the complete system-side inputs are not indistinguishable. All supports are nonempty and nested, and the common carrier is exactly the same T.

Take the SAME partial evidence in both preparations:

\[
K=\operatorname{Anc}_T\{r_1,\ldots,r_m,r_v\}.
\]

K contains every internal vertex and one of the two leaves below each bottom parent. It omits w_1,...,w_m,w_v and therefore is strictly smaller than T. Its assertions concern current address membership, not ownership by a label. It does not contain the source answer through an a-membership field. Its validity and availability are still premises, not generated by this construction.

At o the two child supports share c (and initially a). At p all u_j supports share a. Each bottom parent has two identical child supports. Therefore the initial exact profile q is one at every internal vertex in BOTH sources. This equality includes the entire internal support record, not merely the hitting numbers.

The declared mathematical consumer is

\[
R(F)=\mathbf 1[h_p(F)>1]
     =\mathbf 1\!\left[\bigcap_{j=1}^{m} S_{u_j}(F)=\varnothing\right].
\]

Initially R=0. This is a specified internal incidence property, not an implemented sensor or a new C3 restored-marker decoder. Access to the child supports, the hitting value or this one bit is not inferred from writing the formula.

## 4. Complete permitted-output classification and proof

Every nonroot tip of each non-a view is a global leaf of T. No address in K can strictly extend such a tip. Thus B_K(Y_i)=Y_i for i!=a: the safety bounds force all non-a views to remain unchanged. This includes c, whose retained presence supplies the common cover at o.

For source zero, view a contains every node below p, and contains v but neither of v's leaves. All its p-branch tips are global leaves and therefore mandatory. The tip v is strictly extended by r_v in K. Hence

\[
B_K(Y_a^0)=Y_a^0\setminus\{v\}.
\]

There are exactly two permitted joint outputs: identity and the deletion of a at v. The unique proper output keeps c in v and in p, so h_o stays one. Every other local child-support family is unchanged. Consequently h_p=1, R=0 and total deficit D_q=0 despite a genuine nonidentity incidence change.

For source one, view a contains the p-branch internal vertices p,u_1,...,u_m but no leaf below any u_j. Its other branch contains v,r_v,w_v. Each u_j is an own-view tip strictly extended by r_j in K, whereas r_v,w_v are global leaves. Thus

\[
B_K(Y_a^1)=\{o,v,r_v,w_v\}.
\]

Every output retains that v branch. Let J be the set of u_j from which a is removed. If J is not all of {1,...,m}, prefix closure forces a to remain at p. If J is all of that set, a at p may be retained or removed. This describes all permitted outputs. The only output with J empty is identity. In particular, a proper output necessarily removes a from at least one u_j; it cannot consist solely of removing a at p while retaining a below it.

Write k=|J|. If k<m, each of the k changed child supports of p needs its own label, and none of those labels covers an unchanged child. The unchanged children share a. Thus h_p=k+1. If k=m, the remaining child supports {b_1,c},{b_2},...,{b_m} are pairwise disjoint, so h_p=m. In both cases,

\[
h_p=\min\{k+1,m\}.
\]

The c incidence remains in both p and v even when a at p is removed, so h_o stays one. All global-leaf supports remain unchanged, and every bottom hitting number stays one. Therefore

\[
D_q=\sum_{x\text{ internal}}|h_x-q_x|
   =\min\{k,m-1\}.
\]

For every proper source-one output, k>=1 and m>=2, so h_p>=2 and R=1. This proves the separation for all permitted proper outputs. The output need not be the least retained state, maximal, terminal, unique or chosen by any particular algorithm. QED.

### Decoder using one retained view

Let U=Ch_K(p)={u_1,...,u_m}. This finite address set is available from the already supplied K and the same reference p. On this exact family and all its permitted outputs, including identity,

\[
R(F)=\mathbf 1[U\not\subseteq Z_a].
\]

For source zero, every u_j remains in Z_a even when v is deleted, giving zero. For source one, U fails to be contained in Z_a exactly when J is nonempty, which is exactly the condition h_p>1 just proved. Removing p as well when J is all does not change the conclusion. Identity gives zero in both sources.

Thus a receiver supplied with the restricted retained record Z_a intersect U and the fixed reference (a,p,K) can decode the same bit without other views, global-leaf incidence reads or a complete joint hitting-profile computation. The initial restricted record is U in both preparations; a proper source-one response changes it and a proper source-zero response does not. This is a concrete same-carrier decoder, not an arbitrary dictionary between quantum event bits and incidence labels.

The equality is family-scoped. Positive K alone does not certify that U lists every actual child of p in an arbitrary completion used by the universal safety quantifier. We do not infer a general hitting-number decoder from positive membership data. Under simultaneous transport of the tree, palette, reference (a,p,K) and Z_a, U and containment transport together, so the bit is covariant and its value unchanged. The source comparison is not a mere relabelling: the same initial internal record evolves to different values with the reference fixed.

This supplies a decoder's mathematical input requirement, not physical delivery or observation of that record. Post-event access to Z_a intersect U by a receiver, or even access to the complete own view by the putative event processor, remains unearned. A processor already supplied with the complete initial a-view already knows the source distinction; the new statement concerns its projection into an initially identical restricted record.

The displayed cases are deductive characterizations, not numerical enumeration or new test counts. The proof is elementary and uses the inherited positive-extension classification; no archive-wide novelty priority is claimed.

## 5. First native atomic response and the unit band

The complete universally certified atomic option sets at the two initial states are

\[
\mathcal A_0=\{-a(v)\},\qquad
\mathcal A_1=\{-a(u_j):1\le j\le m\}.
\]

The same indexed view acts in both cases. No event index is assigned the source value and no deletion location is prescribed. All m source-one alternatives give the same changed h_p=2 and D_q=1; source zero gives D_q=0. A mechanism may permit only a subset of these options: whenever it produces a proper output in this class, the response conclusion still holds. Unlike the saturation theorem, maximal availability of all admitted commands is unnecessary.

The inherited atomic locality and increment bound give a second, general reason the FIRST atomic deletion from an exact initial profile cannot exceed the unit total band. Only the parent coordinate can change, and its increment is zero or one, so D_q<=1. In this family the exact values are computed above. This proves the first-step inequality given the native primitive, same-carrier safety and q=h(initial); it does not implement a physical guard, initialize q, or justify those premises' availability to an event.

There is no completion premise. Source one can stop immediately after any one of the m alternatives and already has R=1. For example, with m=3 it need not reach its much smaller hull, whose total deficit is two. The theorem does not require a terminal flag or a longest path. The word "first" refers to this ordered update from the declared initial state, not a fundamental clock.

Any probability law supported on identity and these certified atomic options inherits the same source-conditioned conclusion after a proper outcome. No such law, positive event probability, actual selected record or proper-outcome acknowledgment is derived here. A positive R=1 is sound for source one within the declared comparison class. An observed zero cannot distinguish source zero from source one's identity outcome without additional occurrence information.

## 6. Decisive controls

**Actual carrier preservation alone is insufficient.** In source one, delete a at the global leaf r_v. This is a legal native one-incidence deletion in the actual state: c still covers that leaf, prefix closure is preserved and supports stay nonempty. The two child supports of v become {c} and {a,c}, with hitting number one. All other local values stay one, so this proper first deletion has R=0 and D_q=0. It defeats the universal first-response assertion if one broadens the action class to all actually safe pruning, even within the unit band and using the same view a.

The operation is excluded by the stated information contract, because r_v has no strict descendant in K. A rule seeing only its complete own view and positive carrier addresses lacks the additional ownership fact needed to certify that global-leaf deletion across every compatible cover. A different, justified joint or richer-information mechanism may use that fact. The proof does not forbid it. The new response is therefore a consequence of the particular universal information/safety contract, not of bare native admissibility.

**One-step budget safety does not supply ongoing enforcement.** With m=3 in source one, a second deletion at a different u_j after the first makes h_p=3 and D_q=2. It is still carrier-safe under the positive-extension bounds, but is outside the unit band. Likewise a single larger contraction removing a from two u_j can exceed the band. The binary bit R remains one, but the total is no longer one. Atomic size and exact initial q are essential to the automatic first-step band statement. No repeated-event global guard follows.

**Identity remains permitted.** Both preparations admit identity under the same safety bounds. This familiar boundary is not a new obstruction theorem. The result is conditional on a proper response; it proves neither its occurrence nor a nonzero probability. It cannot turn a source-one zero response into evidence for source zero without an earned occurrence contract.

**The complete source input already differs.** A processor supplied with the whole a-view can already distinguish the two preparations. The theorem relocates that difference into an initially identical internal profile. It does not create information for that already informed processor. A distinct receiver restricted initially to the internal record would require a justified coupling and retained access to gain the distinction; neither is supplied by the proof.

## 7. Scientific disposition and remaining native question

This is a constructive witness for a derived conditional statement: once the inherited universal view-local safety bounds hold, every proper output in this family has a source-specific internal bit. It replaces the earlier need for completed pruning with an immediate-response conclusion, allows arbitrary permitted choice of location, and avoids a runtime global band filter for the first native atomic step. The complete safety classification, atomic bound and supplied native objects themselves are inherited, not counted again as new discoveries.

The family-scoped decoder additionally reduces the required retained readout to one view's membership on the finite address set Ch_K(p). It does not grant a receiver access to that record, but it avoids making a full joint-profile sensor an unnecessary premise of this candidate.

The work discovers a consequence of stated assumptions and constructs preparations witnessing it. It does not discover the physical applicability or origin of those assumptions. In particular, the latest native-information and event-source audits still do not give an event both a complete current own view (or equivalent terminal evidence) and current same-carrier extension evidence with an actual incidence update and receiver connection. This note does not change that source finding or encode an existing quantum event bit as an incidence operation.

The next physical obligation is now narrower: identify a previously justified native event that can use the relevant terminal/extension facts, realize an action in the justified class, and expose the positive internal response to a retained receiver. Universal completion and a uniquely selected deletion site need not be demanded. A genuinely derived probabilistic or positive partial accessible response remains eligible under the user's milestone. The information contract and R cannot be promoted to a physical mechanism or sensor by definition.

Disposition: **CONDITIONAL_SUBBRIDGE_ONLY; FIRST_PROPER_RESPONSE_SEPARATED.** The native-event milestone remains OPEN / NOT ACHIEVED. This is an alternate mathematical consumer, not the C3 restored-marker implementation. Broad C3/C4-C6 and physical origin remain open. Path A remains active; Path B remains closed. Time remains pruning / ordered recoverability update; no force, geometry, fundamental time or dark-matter primitive is introduced.

These analytical findings precede any future numerical preregistration. No scientific code, state enumeration, simulation, historical replay, test-count increase, GitHub Actions campaign, main merge or numbered-stage CLOSED/CERTIFIED claim occurs here. Any later numerical work must satisfy AGENTS.md prospectively. Independent whole-argument review and separate publication auditing are required for this analytical publication and are recorded alongside it.

## Exact source trail

`source_packet.json` preserves ten source texts and the parent continuation index at the immutable parent. `SOURCE_READBACKS.json` records their Git blob IDs, lengths and SHA256 digests. The mathematical dependencies are the native positive-extension information boundary, v16.26 atomic proof ledger, v16.53 native support/move definition, and the preceding saturation result for the question being strengthened. The native dependency ledger, event candidate C3, target-blind gate, physical-frontier decision, milestone assessment and AGENTS.md preserve the input/access and scientific boundaries. Source audit findings are reused, not claimed as new implementation discoveries.
