# What another index can learn from native move admissibility

Date: 2026-10-14 America/Phoenix / 2026-10-15 UTC.
Immutable source parent: `c63bc3ea9b92241fb96d52fe5e47dde16fd97c6b`.

**Conditional analytical classification; physical enforcement and access remain open.** The preceding assessment ruled out reading the first-response bit from other indices' unchanged membership views. This note tests a different candidate: whether the internal incidence change alters the receiver's available native moves and thereby supplies an indirect response.

The answer separates two facts. In the bare fixed-carrier nested-support category, all external information affecting a coalition's atomic moves is whether another index covers each global leaf. Changes confined to other indices' internal incidences leave the coalition's entire command interface unchanged. Global-leaf coverage differences can change that interface, but a physical mechanism enforcing the relation and delivering a readable outcome remains an additional obligation.

These are elementary deductions from the inherited move definition. They are not a new physical interaction, a mathematical priority claim, or an obstruction to all richer event laws.

## 1. Exact category and proposed interface

Fix a finite rooted tree T with root o and a fixed finite palette P. Each support S_v is nonempty, S_o=P, and child supports are contained in parent supports. Write

    Y_i = {v in T : i in S_v}.

The inherited atomic primitive adds or deletes one index incidence at one nonroot vertex while preserving those conditions. T and P stay fixed. This is the bare native admissibility of the cited v16.53 definition. Its separately stated hitting-profile path budget is NOT part of this transition relation. Neither C3 floors, protected supports, a scheduler, event rates, guaranteed acceptance, nor a physical legality oracle is inferred from the definition.

Fix a nonempty proper coalition C of receiver indices. The mathematical interface under test consists of its complete own views (Y_i) for i in C, the common T,P and references, and the admissibility of named atomic commands on those indices. To give the candidate its strongest version, one may hypothetically allow exact legality queries, execution of any admitted command, and observation of the resulting own views. This is a test interface, not already-earned native access. A rejected command leaves the state unchanged in that hypothetical query protocol; rejection flags are not supplied by the native category itself.

Only indices in C act during a receiver experiment. Indices outside C are held fixed in each compared state. Exogenous events, changing carriers, rates, timing, notifications and extra guards are separate interfaces.

Let L_*(T) be the nonroot global leaves of T, and define the external coverage set

    E_C(F) = {l in L_*(T) : some j outside C belongs to S_l(F)}.

This records existence of outside coverage, not the identities or number of outside owners. It is a sufficient mathematical description of external influence on this relation; the receiver is not assumed to start knowing E_C.

## 2. Exact one-command conditions

For i in C and v != o, addition +i(v) is admitted exactly when

    v not in Y_i,                 parent(v) in Y_i.

Nonemptiness is preserved by an addition. Nesting at the parent requires the second condition. Since i was absent from v, nesting in the initial valid state already excludes i from all children of v. Hence no other index membership is consulted.

Deletion -i(v) is admitted exactly when v belongs to Y_i, v is a tip of Y_i, and one of the following holds:

- v is internal in T; or
- v is a global leaf and either another coalition index contains v or v belongs to E_C(F).

The tip condition means no immediate child of v belongs to Y_i; prefix closure makes this equivalent to absence of all strict own-view descendants. It is precisely the nesting condition after deletion.

For the internal-vertex case, choose any child w of v. Its support is nonempty. Since i is absent from every child, some j != i belongs to S_w, and nesting gives j in S_v. Thus another index necessarily retains v; nonemptiness at v is automatic. For a global leaf there is no such descendant witness, and the displayed coverage condition is exactly S_v minus {i} being nonempty. This proves necessity and sufficiency in every case.

The argument is about valid mathematical states, not an event obtaining the terminal fact, the carrier, or the outside-coverage fact. In particular, a fact forced in a full-state proof need not be available as an executable local certificate.

## 3. Exact receiver interface through finite command histories

Suppose F and G have the same T,P, the same own views for every i in C, and the same E_C. Then:

1. Every named coalition command is admitted in F exactly when it is admitted in G.
2. Performing the same admitted command changes the same own incidence and leaves the outside indices fixed. The two successors again have identical coalition views and E_C.
3. An exact legality query gives the same answer in both, and a rejected query changes neither state.

The first statement follows directly from section 2; the second and third preserve its premises. Induction therefore gives identical admissibility answers and own-view observations along every finite adaptive coalition-command experiment using only this interface. Equivalently, the two command transition systems are related by an observation-preserving labelled bisimulation: matching commands remain possible and lead to matching interface states.

For a common processing/randomization rule driven only by these answers, own views, and source-independent reference/local-memory inputs, the transcript laws also coincide. This does NOT mean arbitrary physical processes with the same unweighted move graph have the same probabilities. A separately justified hidden-state-dependent rate or resolution law could differ; the bare relation supplies no such law. Source-dependent timing, availability or stopping signals must not be smuggled into an allegedly identical transcript.

The external coverage set is also necessary for equivalence of the FULL command interface when initial own views agree. Suppose a nonroot global leaf l is externally covered in F but not G. Validity of G requires at least one coalition owner at l; by identical own views the same owners occur in F. Choose one such owner i. Delete each other coalition owner's incidence at l, leaving i in place. These are global-leaf deletions admitted in both states, because i continues covering l. They do not change E_C. Now -i(l) is admitted in F and forbidden in G. Thus a finite successful-command language differs, and an exact final legality query would distinguish the states.

This necessity claim assumes the full interface, including the specified admitted preparatory commands. A smaller physically available command family may reveal less. It does not promise completion, a readable rejection, or execution of every legal request.

Consequently, with fixed T,P and own-view observations, the pair

    ((Y_i) for i in C, E_C)

is an exact quotient of the bare coalition-command interface. External internal incidences carry no further information through this particular relation. This is stronger than a static unchanged-view statement because receiver actions, including additions and actual safe global-leaf deletions, are allowed throughout the comparison.

## 4. Application to the existing first-response bit

Use the inherited first-response source pair and its permitted a-view contractions. For each source separately, compare its state immediately before a proper output with its state immediately after that output.

Every other index's view is unchanged. Every global-leaf incidence of a is unchanged as well: the mandatory hull retains each such incidence and outputs only contract. The changes occur solely at internal vertices of T. Therefore, for ANY fixed C not containing a, the two states have the same coalition views and the same E_C.

Sections 2-3 apply. No finite experiment confined to the coalition's own views and the bare carrier-preserving atomic-command interface can tell whether that internal a-view change occurred. This remains true even when the candidate receiver is hypothetically granted all actual safe native commands, rather than being restricted to the earlier universal independent-view contraction class.

In source one, every proper output changes the inherited bit

    R = 1[h_p > 1] = 1[U is not a subset of Z_a]

from zero to one. The receiver-command interface above is nevertheless unchanged across that actual mathematical transition. Thus carrier-preservation admissibility cannot by itself turn this internal R change into a newly accessible receiver response. A fresh receipt or direct a-membership read would be an additional channel.

This is a BEFORE/AFTER claim within each source. It is NOT a claim that the two source preparations have identical command interfaces. They differ in global-leaf a-incidences before any action. For example choose C={b_2}, which exists for m>=2. At r_2 the supports are {a,b_2} in source zero and {b_2} in source one. The command -b_2(r_2) is already admitted in source zero and forbidden in source one. Granting an exact readable legality oracle would therefore reveal a source distinction BEFORE the first-response event. Counting that pre-existing interface difference as a record produced by the internal event would misidentify the acquisition step.

The original conditional first-response theorem and its positive restricted a-view decoder remain intact. The present result stops the specific attempt to obtain an additional receiver connection from bare carrier-safety feedback.

## 5. Controls and ways outside the result

**A genuine leaf change can alter another index's menu.** On the binary tree T={o,l,r} and P={a,b}, start with S_l=S_r={a,b}. The admitted action -a(l) leaves S_l={b} and S_r unchanged. For receiver C={b}, -b(l) was admitted before and is forbidden afterward. Here E_C really changes. Both states remain valid and the source action is proper. The restriction to unchanged external leaf coverage is therefore essential; the theorem does not prohibit cross-index constraint dependence at global leaves.

**The inherited unit-band guard can distinguish the same bare interfaces.** In source one of the inherited family with m=2, compare the state before -a(u_1) with the state after it. Their total deficits from the same all-one reference q are respectively zero and one; both satisfy D_q<=1. Use C={b_1,c}. In both states the leaf supports at r_1,w_1 are {b_1,c}. First execute -b_1(r_1). The two child supports become {c} and {b_1,c}, so h_(u_1) remains one; both states still satisfy the unit band. Next request -c(w_1). The children would become {c} and {b_1}, making h_(u_1)=2. Both commands are bare-native admitted in both comparisons. But the final total deficit would be one before the a-event and two after it. An exact D_q<=1 transition guard therefore permits the second command in the former case and rejects it in the latter. This is a conditional two-command discriminator using the inherited band, with BOTH starting states in the band. It neither implements that global guard nor supplies readable rejection or commit-every-legal-request semantics. It identifies precisely why the bare-interface classification must not be promoted to a full C3-guarded impossibility theorem.

**Direct access and other events remain eligible.** A receiver that reads changed a-membership, an internal component of the a-view, an authentic event receipt, a derived joint operation, a changed-carrier process or a justified probability law can have more information. Their availability must be established on their own terms. The theorem does not require every receiver to be a separate palette index or every physical process to fit this transition relation.

**Admissibility is not actuation.** The leaf control and the completeness proof provide conditional admitted-command distinctions. They do not derive a mechanism that resolves requests, exposes rejection, schedules events or retains a result. The earlier nested-record screen already preserved this distinction. No repetition of an all-NOOP argument is needed here.

## 6. Scientific decision

Disposition: **BARE_MOVE_INTERFACE_CLASSIFIED_BY_EXTERNAL_LEAF_COVERAGE; INTERNAL_FIRST_RESPONSE_NOT_TRANSMITTED_BY_THIS_INTERFACE; NATIVE_ACCESS_OPEN.**

The advance is a precise location of possible cross-index dependence in the inherited bare atomic relation. External global-leaf coverage can affect a receiver's command possibilities. External internal-incidence changes cannot, even after finite receiver-command sequences, when the other stated inputs are held fixed. The first-response construction changes the internal profile while remaining in one such receiver-interface class.

This gives the next candidate a concrete test. To use carrier-safety interaction, it must justify an event that changes the relevant external leaf coverage and a readable command consequence. To use the already-proved internal response, it must justify another channel, such as actual access to a-membership or a derived guarded/joint transition law. Neither a full-state validator nor a desired hitting-profile readout supplies that mechanism. The positive-extension safety contract preserves every global-leaf incidence, so its contractions alone cannot change E_C for an untouched receiver coalition.

The result is conditional mathematical progress and a bounded receiver-candidate rejection. It does not establish a new physical force, native event, sensor, geometry, energy, clock, dark-matter variable or gravity explanation. The frontier milestone remains NOT ACHIEVED; Path A stays active and Path B closed. Time remains pruning / ordered recoverability update. Broad C3/C4-C6 and physical origin remain open.

No scientific code, enumeration, simulation or numerical campaign was run. The proof and analytical controls were developed before any possible numerical preregistration. Text/hash/source checks are provenance work and add no historical scientific test count. No main merge or numbered-stage CLOSED/CERTIFIED status is claimed. Independent whole-argument review and separate source/publication auditing are recorded alongside this note.

The ten-source packet binds the native move definition, positive-extension result, first-response theorem, own-view assessment, native dependency ledger, earlier nested-record screen, milestone, physical-frontier decision, AGENTS and parent continuation. These sources establish the declared premises and prior boundaries. No archive-wide originality or absence claim is made.

