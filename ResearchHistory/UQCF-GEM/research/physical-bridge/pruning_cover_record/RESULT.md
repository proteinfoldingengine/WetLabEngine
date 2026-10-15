# A Boolean cover record for pure-pruning unit guards

Date: 2026-10-14 America/Phoenix / 2026-10-15 UTC.
Immutable source parent: `c65db96eedbcd354c4b96ad9d617f97c2aeb9283`.

**Conditional analytical result, not a native acquisition or interaction law.** The preceding `unit_guard_inputs` assessment showed that the current complete hitting profile, a truthful deficit counter and the declared local inputs do not determine the next deletion's cost. This continuation tests the existing richer miss-count record on the pruning-only event grammar. There is a useful positive reduction: exact cover-validity bits are closed under supplied contractions, and two cardinality levels at each parent suffice for exact fixed-reference unit-band decisions after an exact starting profile.

The reduction removes miss multiplicities from this particular future task. It does not remove correct initialization, current active-support input, actual-event visibility, or the need to derive why a unit-band constraint applies. Its elementary monotonicity argument is a specialization of the inherited cover and miss-count definitions, not a claim to a new general information theorem or physical force.

## 1. Declared carrier, reference and information contract

Let T be a fixed finite rooted tree and P a fixed nonempty finite palette. Each vertex v has a nonempty support S_v subset P, child supports lie in parent supports, and S_root=P. At an internal vertex x define h_x as the minimum size of a palette subset hitting every immediate child support.

Fix a feasible target profile q. The actual initial state has h_x=q_x at every internal x. Thereafter the allowed history in this result contains only actual single-incidence deletions preserving nonemptiness, nesting and the fixed carrier. Other indexed views are unchanged during each atomic edit. No support addition, root creation/removal, tree change or reference reset is included. The broader inherited native category permits additions; restricting to contractions here is a candidate-specific premise, not a claim that all native dynamics already obey it.

Write

    D_q = sum over internal x of |h_x-q_x|.

The proposed guard asks whether a supplied prospective deletion leaves D_q<=1. Its physical enforcement is not assumed to have been derived.

The conditional evaluator is supplied the correct initial record defined below, the same literal T,P,q, and the named active vertex's actual current support S_v together with the requested deletion. Native syntax/carrier safety must be justified separately; it can use the previously established positive-extension certificate when applicable. The evaluator is not granted an unmentioned read of sibling supports. Accepted record updates are tied to actual committed deletions; an unchanged outcome leaves the record unchanged. Command submission alone is not an actual-event receipt.

The initial record may be obtained by taking the zero set of a legitimately initialized miss-count field. That is a conditional source, not an initialization mechanism. The previous same-profile pair already shows why knowing an exact initial PROFILE is weaker than knowing this record.

## 2. The zero set is closed under contraction

For a fixed family of child slots at x and a nonempty H subset P, retain

    C_x(H) = 1[H intersects every S_w, w a child of x].

Equivalently, C_x(H)=1[M_x(H)=0], where M_x counts child supports disjoint from H. C records the truth of each named cover, not an existential statement that some cover containing a named pair exists. In particular it is not the older F_R table rejected by the dynamic-residual result.

Suppose the only changed support is S_v, with parent p, and it contracts to S_v' subset S_v. Then for every retained H,

    C_p'(H) = C_p(H) AND 1[H intersects S_v'],          (1)
    C_x'(H) = C_x(H) for x != p.                       (2)

Proof: if H failed to cover before, an unchanged child still misses H, or the old active support missed H and its subset still does. A false cover cannot become true under contraction. If H covered before, every unchanged child still meets it, so only the new active support must be checked. Other parents have identical immediate-child support families. This proves (1)-(2), including an unchanged active support.

Thus the correct zero set is closed under any supplied sequence of these contractions, without storing miss multiplicities or rereading the other child supports. The proof is an induction on actual updates, not an acquisition of the initial zero set. Equation (1) describes how a correct record would have to change; it does not produce a physical record-writing interaction.

The full miss-count law remains correct and more general: it supports both additions and deletions when the active support is supplied. There is no contradiction with its necessity for some richer update tasks. For contractions, only cover loss matters and Boolean validity is enough for this record.

## 3. Two cardinality levels suffice for the one-unit task

For each internal x let a_x be its number of children and k=|P|. Feasibility ensures 1<=q_x<=min(a_x,k). Retain C_x(H) for every H of size q_x and, if q_x+1<=min(a_x,k), every H of size q_x+1. No other query sizes are needed for this particular band test.

Pure contraction cannot reduce a hitting number. Since the initial profile is exactly q, every subsequent state satisfies h_x>=q_x. Existence of a q_x-cover is equivalent to h_x=q_x: any smaller cover could be extended to size q_x inside P, and the lower inequality excludes that smaller case. If no q_x-cover exists but a (q_x+1)-cover does, h_x=q_x+1. If neither exists, h_x>=q_x+2; when q_x already equals min(a_x,k), that last case is impossible in a valid native state.

Define a capped local excess

    e_x = 0  if some retained q_x-cover is true;
          1  if no q_x-cover is true but some retained (q_x+1)-cover is true;
          2  otherwise.

On the declared valid histories, e_x=min(h_x-q_x,2). Therefore

    D_q<=1  if and only if  sum_x e_x<=1.               (3)

The cap preserves this decision because any excess of at least two already violates the band. It is not an exact reconstruction of arbitrarily large D_q.

For a proposed carrier-safe atomic deletion at v, compute the prospective bits at p using (1), leave every other field unchanged, and apply (3). This gives the exact band decision from the current Boolean record and supplied active support. If the deletion actually occurs, retain the computed bits; if the actual outcome is NOOP, retain the old record. Repeating the procedure remains correct on every actual pruning prefix, regardless of whether those prefixes are themselves restricted to the band.

The q_x+1 level is needed by this sufficient construction to handle the parent that has already spent the unit. A cover that was not minimum initially can become minimum after smaller covers are lost. That is not a newly created cover: its validity was already present in the initial higher-level record. We claim neither universal minimality of these levels nor a minimal number of stored bits.

The bit count is the sum over internal x of binomial(k,q_x), plus binomial(k,q_x+1) when that level is included. This is finite but may be large. It replaces integer multiplicities by Boolean coordinates for the chosen grammar; no general efficiency or compression optimality is asserted.

For arities at most four, all required query sizes are at most four and lie within the existing degree-four miss-field definitions, applied to the appropriate named child family. On the five-label binary fixture below the reduction uses only degrees one and two. Higher-arity targets may require higher-degree initial coordinates; the old degree-four theorem is not silently extended to supply them. The proof above is direct for finite P and T, including small palettes; it does not widen the source theorem's declared target-four controller domain.

## 4. It resolves the preceding guard example when the richer record is supplied

Use the exact F/G pair in `unit_guard_inputs/RESULT.md`: P={a,b,c,d,e}; p has child supports {a,b},{a,b} in F and {a,b},{a,c} in G; the other branch has already spent one unit; q is one at every internal vertex. Both current full profiles are (1,1,1,1,2), and the same positive-extension-safe request removes a from v.

Before the request the retained singleton covers at p are:

| State | True singleton covers at p | After S_v changes to {b} |
| --- | --- | --- |
| F | {a}, {b} | {b} survives |
| G | {a} | No singleton cover survives |

Equation (1) deletes {a} in both records and preserves {b} only in F. At the z branch e_z=1 already. In F, e_p remains zero, so the prospective sum is one. In G, a pair such as {a,b} still covers the two children, so e_p becomes one and the prospective sum is two. The Boolean record therefore returns the exact different decisions missing from the previous input package.

This does not defeat the previous impossibility claim: C_p({b}) differs in the initial record, while that assessment expressly excluded such cover information. The enriched evaluator starts with the distinguishing fact. Its success establishes conditional sufficiency and maintenance, not a native source-to-receiver acquisition.

## 5. Substantive controls on the simplification

### Additions can revive a false cover

Take the same labelled child slots v,w under p and P containing a,b. Compare

    F: S_v={a}, S_w={a,b};
    G: S_v={a}, S_w={a}.

At every query size, the complete old cover-validity fields agree: H is a cover exactly when a belongs to H. The active old support {a}, parent support containing a,b, and request +b(v) also agree. This is a valid incidence addition in both states.

After the addition, F has children {a,b},{a,b}, so {b} is a cover. G has {a,b},{a}, so {b} is not a cover. Thus even the entire old Boolean cover field plus the supplied old/new active support cannot update itself exactly across arbitrary additions. The old miss counts distinguish the states: M_p({b})=1 versus two, and both decrease by one. This is also a strict information-loss control for the map M to its zero set.

The difference can affect the unit-band decision, not just an unused record coordinate. Embed p as a child of o, give p and o the common full palette {a,b,d,e}, let v,w be leaves, and add a sibling z with support {d,e} and leaves {d},{e}. Take q=(1,1,1) at (o,p,z). Both starts have h=(1,1,2), D_q=1; they are reachable from exact profiles by the same two z-leaf deletions used in the preceding assessment. The common addition +b(v) keeps h_p=1 in both. The subsequent common deletion -a(v) leaves h_p=1 in F and h_p=2 in G, hence total deficits one and two. All these mathematical edits preserve nonempty nested supports and the fixed carrier; the last G output is excluded only by the extra band. This control concerns the broader add/delete grammar and is not misreported as a pruning-only history from the chosen exact reference.

### The active support cannot simply be omitted

Let p be the root with P={a,b,c}. Its children are an internal v and a leaf w. The two leaves below v have support {a} in both states, and S_w={b}. Compare S_v={a,b,c} with S_v={a,b}. At p every cover must contain b, which also hits v, so both complete old cover-validity fields are identical. At v the child field is identical as well. Both profiles are exactly q=(1,1).

The complete acting b-view is the same {p,v,w}. The request -b(v) is a universally carrier-safe own-view tip deletion because v has a strict descendant in K=T. Yet after it, H={b,c} covers p in the first state and fails in the second. The active old supports differ and were deliberately omitted in this control. Consequently the old Boolean field, own view, carrier and request alone cannot generate the exact new Boolean record. The supplied current active support in (1) remains a substantive input. Both successor hitting profiles are (2,1), so this control is explicitly about exact record update, not different immediate scalar guard values.

### Exact profile and complete command directions do not initialize cover identities

In the preceding F/G example, replacing both z leaves by {d,e} gives exact initial profiles in both worlds, and the same subsequent two actual preparation deletions lead to their common current profile and budget. The singleton cover {b} at p nevertheless exists only in F throughout. A known exact profile and common directions therefore do not initialize its truth bit. This is reuse of the preceding counterexample, not a new seed obstruction.

Initializing C from the zero set of a correct M is legitimate when M is already available. Initializing M from full support data or from a complete correctly seeded incidence ledger is likewise conditional on those inputs. The historical event-inversion result can reconstruct an active support from supplied exact count increments, but reading the later increment does not derive the earlier prospective update or guard. We do not use that inverse circularly to remove the active-support premise.

## 6. Relation to the retained-record and physical frontier

The previous dynamic-residual theorem established exact integer-field updates for declared additions and deletions. This result identifies a genuinely smaller sufficient record for the restricted contraction task and specializes it to the fixed-q unit band across a tree. The new content is the declared Boolean update contract, the two-level band criterion and the explicit grammar/input controls. Their proof is elementary; neither novelty priority nor a new physical mechanism is asserted.

The prior live-certificate source screen already explains why persistence of a central record, a source address or a source amount does not by itself bind that record to a current indexed-view predicate. The same issue remains for C_x(H): the inherited record-preservation results do not establish that an accessible record begins with these truth values or receives exactly the event-dependent update (1). Repeating those source obstructions is not counted as another discovery here.

This assessment separates four obligations:

| Obligation | Current result |
| --- | --- |
| Sufficient representation for the restricted guard task | Two levels of exact cover-validity bits suffice under the declared pruning history |
| Mathematical maintenance after supplied actual edits | Exact Boolean filtering using the current active support |
| Native origin, semantic binding and availability of record/update inputs | Unestablished in the inspected sources |
| Physical applicability, enforcement and readable consequence of the unit band | Unestablished |

A physical system could realize the relevant dependence without an observer reading every hidden support. Such a derived joint process remains eligible. The present formulas are an implementation specification under supplied inputs, not evidence that such a process occurs. A stochastic native consequence remains eligible; deterministic selection, maximal permissiveness and guaranteed completion are not imposed as universal physical requirements.

## 7. Decision and next scientific obligation

Disposition: **BOOLEAN_COVER_RECORD_SUFFICIENT_FOR_DECLARED_PURE_PRUNING_UNIT_GUARD; INITIALIZATION_ACTIVE_SUPPORT_AND_ENFORCEMENT_UNDERIVED.**

The exact guard does not require retaining miss multiplicities once the correct relevant cover bits exist and the subsequent grammar is contraction-only. This closes that conditional representation/update question. It does not close native record origin, action or access. The unit band retains its status as an additional fixed-reference path constraint; no physical principle enforcing it has been found here.

For this route, further work should identify an already justified record or joint process that actually supplies the required cover validity and event-dependent filtering, and a native reason for the constraint itself. Recomputing the same Boolean tables on larger examples would not supply either premise. If additions are to remain available, the Boolean simplification must be abandoned or augmented with enough information to support their updates. The existing miss-count field remains one conditional option.

The frontier milestone remains NOT ACHIEVED. No new physical interaction, force, gravity explanation, energy, geometry, fundamental clock, dark-matter primitive, C3/C4-C6 closure or numbered-stage CLOSED/CERTIFIED status is established. Path A remains active and Path B closed; time remains pruning / ordered recoverability update.

All displayed controls and formulas were derived analytically before review. No scientific module, enumeration, simulation, numerical campaign, inherited replay or test-count increase was performed. Executed scripts only package text and verify provenance. Independent whole-argument review and separate publication auditing accompany the final assessment; no main merge or historical recertification is claimed.
