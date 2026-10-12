# View-local pruning: exact universal safety envelope and a conditional record

Date: 2026-10-12 UTC / 2026-10-11 Phoenix.
Immutable inspected parent: 768fbc9f379bf3966632f0e511bdb24f22723ba1.
Status: author-side analytical result awaiting separate adversarial review. No numerical campaign, native event law or numbered-stage certification.

## 1. Question and inherited premises

The preceding uniform-retraction attempt cannot change support at a surviving vertex. The later event-source audit did not find a native event-to-indexed-view action. This note tests a different, precisely limited architecture: each view is pruned using its own contents and the same known common tree, without reading other views. Can such an operation preserve the common carrier for every cover, and can it produce a source-dependent conditional record?

The initially considered request-induced descendant deletion is already proved in COUPLED_C3_PRUNING_RECORD_BRIDGE.md section 3. It is not a new finding here. The new object is the complete universal safety envelope of independently applied view maps and its least retained member. The elementary order-theoretic arguments carry no originality/priority claim.

Inherited objects are a finite rooted tree T with root o, a fixed indexed palette P with |P| >= 2, and views Y_i that contain o, are prefix closed, and cover T. Their support representation is S_v={i : v in Y_i}. The root support is P. Different indices may carry identical views or root-only views. Tree and palette orders, if supplied, are retained; no symmetry argument discards them. No branching bound is needed for the classification.

Fix T and P. For each i, a deterministic mathematical map F_i takes a single root-containing prefix-closed view Y and returns such a view F_i(Y) contained in Y. F_i may depend on i and on the full T and P, but not on the other views. Define universal carrier safety by

    union_i F_i(Y_i) = T for EVERY indexed cover (Y_i) of T.

This quantifier ranges over all native covers, not a fixed hitting profile, a promised source family or a supplied correlated event record. The word local here means only this declared information restriction. It is not a derived physical locality principle. We have not shown that an actual observer has access to the complete T, P or even its entire Y_i.

Let L(T) be the global leaves of T. Define the leaf-generated hull

    H_T(Y) = {o} union {v : v is an ancestor of some l in Y intersect L(T)}.

An ancestor includes the vertex itself. This is a root-containing prefix-closed subview of Y. It can be only {o} when Y contains no global leaf; it is always Y when T has only its root.

## 2. Exact classification of universal carrier safety

**Theorem 1.** The family (F_i) is universally carrier safe if and only if

    H_T(Y) subseteq F_i(Y) subseteq Y

for every index i and every root-containing prefix-closed Y. The right inclusion and prefix/root properties are the declared operation type. Thus H_T is the unique componentwise least retained output in this class, equivalently the greatest deletion permitted by universal safety under the stated inputs.

**Necessity.** Fix i, Y and a global nonroot leaf l in Y. Set every other view Y_j=T minus {l}. Because l is a global leaf, these are root-containing prefix-closed views. There is at least one such j, and together with Y they cover T. None of their contracted outputs can contain l. Universal carrier safety therefore forces l in F_i(Y). Its prefix closure forces all ancestors of l. Root membership is already mandatory. This proves H_T(Y) subseteq F_i(Y). If T is root-only, root membership directly proves the result.

**Sufficiency.** For any cover and every global leaf l, at least one input view Y_i contains l. The assumed inclusion makes its output retain l and every ancestor. Every vertex of a finite rooted tree is an ancestor of a global leaf. Therefore the outputs cover T. QED.

The extremal operation H_T is defined for every native cover, produces individually determined subviews Z_i=H_T(Y_i), and preserves their union without consulting the other views. It does not take a separately selected mask Z_i as input. It keeps exactly the global-leaf incidences each view already had:

    H_T(Y) intersect L(T) = Y intersect L(T).

It is monotone in Y, idempotent, and commutes with transport by rooted-tree isomorphisms (and relabelling of the indexed family). These follow directly from taking ancestors of the same retained global leaves. Idempotence means repeating this operation on the unchanged carrier produces no further change; it is not a continuing event generator.

In support coordinates its complete output is

    S'_o = P,
    S'_v = union_{l in L(T), v ancestor of l} S_l   for v != o.

These unions are nonempty, nested, and contained in S_v. The formula is the same incidence transposition used by the inherited bridge, not an identification of quantum blocks or extensive source amounts with view labels.

**A sharp limitation of this class.** Every universally safe view-local operation preserves EVERY global-leaf incidence, not merely one source witness. Hence no operation in this class can implement the preceding five-vertex write -a(w), -a(u), where w is a global leaf initially containing a. Preserving a at w forces a at u. The restriction on that old consumer is stronger than the uniform-retraction failure but has a different premise: independent view-only processing with a universal cover guarantee. It does not exclude actions using justified cross-view information or a restricted input promise.

## 3. What changes if the common carrier is not an input

**Theorem 2.** Suppose F_i takes only the concrete view Y and the fixed palette/index data, is independent of the surrounding common tree, contracts Y as above, and must preserve union for every finite common tree and every cover. Then F_i(Y)=Y for every Y and i.

Proof. For the given Y choose the common carrier T=Y, put Y_i=Y and every other input view equal to {o}. Their outputs are contained in {o}. The only way to preserve union Y is for F_i(Y) to retain every vertex of Y. QED.

This elementary witness identifies the information enabling Theorem 1's nonidentity operation: knowledge of which endpoints of a view are genuinely global leaves, rather than merely terminal within that view. In the absence of that common-carrier input, no nonidentity independently applied contraction is universally safe in this larger class. If common tree, external event data, compatible-state promises, label roles or cross-view certificates are supplied, they change the input class; Theorem 2 cannot silently discard them.

This is an information-restricted structural theorem, not a universal physical impossibility result. For example, an actual justified witness that another view retains a global leaf would support a different architecture. We have not derived acquisition or retention of such a witness.

## 4. Conditional record on a separately declared consumer

The old two-edit consumer is excluded by Theorem 1, so it is not relabelled as successful. The following different consumer is explicitly declared for this analytical construction before any numerical campaign. It is not the C3 restored-marker increment contract or the earlier swapped-root diagnostic.

Use T with o having children u,C and u having leaves r,w. Let P={a,b,c,d}; reference label a and vertex u are fixed in both preparations. Define the complete preparations:

| Vertex | Source zero | Source one |
| --- | --- | --- |
| o | {a,b,c,d} | {a,b,c,d} |
| u | {a,b,c} | {a,b,c} |
| r | {a} | {b} |
| w | {c} | {c} |
| C | {d} | {d} |

Both have the same internal hitting profile (h_o,h_u)=(2,2). The initial memory at u is identical. Apply the SAME operator H_T, derived without choosing a source bit, target profile, reference label or desired answer.

All global-leaf supports are unchanged. At u the output is {a,c} from source zero and {b,c} from source one. Thus the projection

    R(S') = 1[a absent at u]

is respectively zero and one, having been zero in both initial preparations. The two outputs still have profile (2,2); the hitting profile alone does not expose this record. Each complete update is a single inherited legal deletion: -b(u) for source zero and -a(u) for source one. Nesting permits it because the deleted label is absent from both children; the remaining support is nonempty. Both paths have zero excursion and exactly one changed incidence. This is a hand-derived witness, not a new execution count.

Source-one-exclusive incidence (r,b) remains at its original coordinate, consistent with the inherited no-full-source-erasure limit. Under every later legal same-union deletion, the positive absence at u persists. From source zero, singleton {a} at r remains protected by nonemptiness, so prefix closure forces a at u on every such history. Hence this projection is universally sound for these two prepared sources within the inherited pruning-only path class, even without assuming H_T occurs. Nonvacuous attainment in the example is conditional on the actual H_T update (or the displayed legal deletion), not guaranteed by admissibility.

This is a concrete source-dependent mathematical input/output map whose masks follow from its definition, rather than a supplied answer-dependent pair of masks. Its use as a physical interaction is NOT established: the source preparations, common carrier, indexed reference, availability of the whole relevant view, choice to apply H_T, pruning-only restriction and accessibility of R remain premises. An observer is not granted the full verifier state. Simultaneously swapping source and reference labels transports the construction; changing the source while keeping reference a fixed is the comparison above.

## 5. Rejecting analytical controls and band limits

**No common-tree knowledge.** In source one above, Y_a={o,u}. Under common T, u is not a global leaf, so H_T(Y_a)={o}. Under the different compatible carrier T'=Y_a, u is a global leaf, so H_T'(Y_a)=Y_a. The same local view alone cannot distinguish these contexts. Treating local endpoints as global leaves would silently change the operation or assume missing carrier data. This is a concrete instance of Theorem 2.

**Deleting a global leaf without a redundancy premise.** For any purported local rule removing l from Y_i, the completion with all other Y_j=T minus {l} is a genuine cover whose output would lose l. This is the rejecting family used in Theorem 1; it is a proof witness for every violating rule, not a numerical test.

**Universal union safety does not guarantee a protected hitting band.** Let o have three children u_1,u_2,u_3, each with two leaf children. Take P={a,b_1,b_2,b_3}; set S_{u_j}={a,b_j}, both leaves below u_j to {b_j}, and S_o=P. The initial profile is h_o=1 and h_{u_j}=1. H_T removes a from all three u_j, so the final root hitting number is 3 while all child profiles remain 1. Relative to the initial exact profile q, D_q changes from 0 to 2. Thus the full extremal update cannot always lie in budget B=1. This carrier uses only arities 2 and 3. No full-state band-checking fallback is inserted into the local rule.

For a particular initial S, H_T(S) is always a same-union refinement. The already proved endpoint criterion gives a legal deletion factorization within budget B exactly when D_{h(S)}(H_T(S))<=B. This is an inherited conditional admissibility test, not a new theorem or a physical enforcement mechanism. It provides the zero-excursion check for the positive example and rejects the ternary control from the unit band. Atomic factors are ordered by view-prefix dependencies; the theorem supplies no physical clock or scheduler.

**Safety and idempotence do not select this map.** Identity is universally safe and idempotent too. More strongly, for any fixed root-containing prefix-closed A subseteq T,

    F_A(Y) = H_T(Y) union (Y intersect A)

is universally safe, monotone and idempotent. It retains the same global leaves as Y, so H_T(F_A(Y))=H_T(Y); intersecting again with A proves idempotence. A={o} gives H_T and A=T gives identity. A rooted-isomorphism-covariant intermediate example is A={vertices of depth at most 1}, when it differs from both endpoints. Tree depth here is structural lineage depth, not duration. This family is an analytical nonuniqueness control, not a proposed physical law or an extra adopted retained set.

Choosing H_T means choosing the maximal-deletion member of the universal safety class. That extremal characterization determines the member mathematically; the inherited requirements do not force a real event to choose it. Calling it canonical, safe or idempotent does not close this gap.

## 6. Scientific disposition and continuation

Author-side disposition: CONDITIONAL_VIEW_LOCAL_ACTION_CLASSIFIED; NATIVE_EVENT_AND_ACCESS_NOT_DERIVED.

This is a conditional mathematical advance: a complete information-restricted safety classification, an explicit least-retained nonuniform map, an exact boundary when common-carrier information is absent, and a worked source-to-memory response on a separately typed consumer. It is more than evaluating an arbitrary supplied mask, but less than deriving an event that applies the map. It does not convert the previous source audit into physical closure or demonstrate a new force.

The next physical obligation is specific: justify access to the common-carrier/global-leaf information and an event mechanism whose action is H_T (or a separately justified member/relation), together with retained use of its output. A proof of universal safety alone is insufficient, and adding maximal deletion as an axiom is not authorized. The old consumer additionally needs justified cross-view redundancy information if its global-leaf deletion is retained as the goal. Which information is physically available must be derived before treating either architecture as native.

All formulas, the positive fixture and the counterexamples above were worked out analytically before review. No prospective numerical preregistration, enumeration, runtime benchmark, historical 527-test replay, GitHub Actions scientific run or Gemini review is claimed. No claim of archive-wide novelty or mechanism absence is made. Any future verification campaign requires a prospective universe, independent reconstruction and rejecting controls under AGENTS.md. No numbered-stage CLOSED/CERTIFIED label, merge to main, physical source correspondence, broad C3/C4-C6 closure, fundamental time, geometry or dark-matter variable is introduced. Path A remains active; time is pruning / ordered recoverability update.

Exact inspected sources are in source_readbacks.json. The use of the old pruning-cone and endpoint theorems is explicit, and their historical execution status is not recertified here.
