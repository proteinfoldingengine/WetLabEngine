# Hyperedge exchanges: a safe clone criterion and its structural limit

Status: candidate analytical result for independent review. Parent analytical head 72d4ac0bd5fb33b596766113bf71afdbe342fab3. No implementation, numerical search or scientific execution. Earlier accepted results remain unchanged.

## 1. Question and results

Use the same finite palette P, positive root floors a_i, nonempty supports A_i and single-incidence moves. Fix a target q>=3. We seek exchanges that change higher-floor overlap while maintaining tau>=q-1, where tau is the minimum hitting number. The previous graph proof relied on completed clones never decreasing tau, so its safe lower-guard steps could be iterated.

This document establishes an arbitrary-floor protected-star lemma and a pair-protected hyperedge cloning theorem with an explicit slot-matching condition. It also gives a symbolic floor-three counterexample to the naive claim that co-occurrence and degree control suffice to preserve tau under cloning. Repetition of that unsafe rule can leave the unit band. This is a precisely characterized failure of that rule, not a connectivity obstruction.

## 2. Arbitrary-floor star replacement

**Lemma R.** Suppose tau(A)>=q and fix a label u. Retain all roots that do not contain u. Any selected roots containing u may be replaced by arbitrary supports meeting their own floors, through single-incidence union paths, while preserving tau>=q-1.

Proof. Let F be the family of roots not containing u. Any hitting set for F together with u hits the original tuple, so tau(F)>=tau(A)-1>=q-1. Empty F would have hitting number 0 and is therefore impossible under these assumptions. All roots of F remain present. Replacing a selected support X by Y through X -> X union Y -> Y meets its floor throughout: expansion contains X, contraction contains Y. Every intermediate tuple contains the fixed constraints F, proving the lower bound.

No bound on the sizes or number of edited roots is required because slots are retained and each destination is checked against its own floor. No upper bound is claimed. To iterate R without cumulative loss, one must separately ensure each completed exchange has tau>=q. R alone only protects one step from such a starting point.

## 3. Copying a role into existing slots

Fix distinct u,v and a tuple A. Freeze all roots except those containing u but not v; call the editable slot set J. Let D be the family of DISTINCT supports

    (A_i\{v}) union {u}, for roots with v in A_i and u not in A_i.

These are the desired copies of the v-only roots. Let M=|D| and t=|J|. Each desired support must be assigned to a different editable slot whose floor is no larger than its size. Sort the editable floors as f_1<=...<=f_t and the desired support sizes as s_1<=...<=s_M.

**Lemma S (slot criterion).** Such an assignment exists if and only if M<=t and f_j<=s_j for every 1<=j<=M.

Sufficiency assigns the sorted demands to the M smallest-floor slots. For necessity, restrict any successful assignment to the j smallest demands. All of their assigned slots have floors at most s_j, so there are at least j eligible slots and f_j<=s_j. This includes M=0, with no inequalities to check. Distinct equal-sized supports still count as separate demands; only identical supports are deduplicated.

If the criterion holds, place one copy of each member of D in its assigned slot. Fill all unused editable slots with P. The latter supports are redundant in any nonempty root tuple and meet every floor. All v-only roots, all roots containing both u and v, and all roots containing neither remain fixed. Call the resulting tuple C_{u<-v}(A). This specifies a new tuple in the SAME r slots and palette; it does not add a root or lower a floor.

## 4. Pair protection makes the completed clone safe

Call a set I subset P independent when it contains no entire root support. Then alpha(A), its maximum size, satisfies tau(A)=k-alpha(A), by complementing hitting sets.

**Theorem T (pair-protected clone).** Suppose tau(A)>=q, the slot criterion holds, and an existing root is exactly {u,v}. Then C_{u<-v}(A) has tau at least tau(A), and the change is implementable with floors respected and tau>=q-1 throughout.

Proof of the endpoint bound. The pair root is frozen because it contains both u,v. Thus an independent set I of the new tuple cannot contain both. If u is absent from I, then I was independent in the old tuple: old roots containing u cannot lie in I, and every old root without u was retained.

If u belongs to I, then v does not. Replace u by v, obtaining an equal-sized set I'. An old root containing u cannot lie in I'. An old root containing neither u nor v is retained and therefore cannot lie in I' (on its labels I and I' agree). If an old v-only root E lay in I', its copied support (E\{v}) union {u} would lie in I and is present in the new tuple, a contradiction. These cases exhaust the old roots. Hence I' is old-independent. We have produced an old-independent set of the same size as every new-independent set, so alpha(new)<=alpha(old), equivalently tau(new)>=tau(old).

For the primitive path, only J roots are edited and all initially contain u. Lemma R implements their assigned replacements and P fillers, preserving tau>=q-1 and their individual floors. No degree heuristic substitutes for the explicit slot test.

A finite sequence of such clones, with the hypotheses checked at every completed tuple, retains tau>=q at every completed exchange and tau>=q-1 between them. If its original and final endpoints are exact-q, the earlier Theorem A converts that finite lower-guard path to a {q-1,q} path. We do not prove that such a sequence always exists, reaches a canonical tuple, or has a universally decreasing progress measure. The number of remaining replacements gives termination for each individual clone only.

The pair root is a real hypothesis on the existing tuple. It cannot be introduced as an extra constraint in the native carrier. In particular this theorem does not apply to all-floor-three tuples, whose supports can never be pairs.

## 5. Why the independent-set protection does not follow from co-occurrence

Every independent set excludes simultaneous u and v exactly when at least one root support is a subset of {u,v}. In one direction such a root is forbidden inside an independent set containing the pair. Conversely, if no root is a subset of {u,v}, the pair itself is independent. For nonempty roots, these possible guards are {u}, {v} or {u,v}. Singleton guards are handled by the earlier anchor reductions; T uses the frozen pair guard.

This characterizes the protection used by the equal-size replacement argument. It does NOT say that every safe clone requires a pair root: a particular larger-root tuple may preserve tau for other reasons. It says that merely retaining a hyperedge containing u and v does not supply the independent-set exclusion used by the graph proof.

## 6. Exact floor-three failure of the naive rule

Take nine distinct labels u,v,w,a,b,c,d,e,f and four roots, each of floor 3:

    A_1={u,v,w}, A_2={u,a,b},
    A_3={v,c,d}, A_4={w,e,f}.

The last three roots are pairwise disjoint, so tau(A)>=3. The set {u,v,w} hits all roots, so tau(A)=3. Both u and v have incidence degree 2, and they co-occur in A_1.

Apply the naive hyperedge analogue of the clone: retain A_1, A_3, A_4 and replace A_2 by {u,c,d}, the copy of the v-only root. The slot condition is satisfied (one size-3 demand in one floor-3 slot), and degrees of u and v stay 2. The new tuple has hitting set {w,c}, so tau<=2. It has no one-label hitting set: A_1 intersect {u,c,d} is {u}, which is disjoint from A_3. Thus tau(new)=2.

This does not contradict T because there is no pair root {u,v}. It shows that co-occurrence in a retained triple, equal clone-label degrees, and a valid slot assignment do not imply that the completed clone preserves the old hitting number. For example, a maximum new-independent set can contain both u and v, which prevents the equal-cardinality u-to-v substitution used in the graph proof.

The replacement itself is a legal one-unit step sequence for target 3: expand A_2 to {u,a,b,c,d}, then delete a,b. The fixed roots retain cover number 2, while expansion is below the original hitting number and contraction is below that of the final tuple. All primitive states remain in {2,3}. Thus the first loss of one unit is permitted; the problem is iteration.

To see accumulation without any numerical experiment, take two disjoint copies of the entire nine-label construction. Their palettes are disjoint, so hitting numbers add. The eight-root, eighteen-label tuple has all floors 3 and exact target q=6. Apply the same naive clone first in one copy, then in the other. The successive completed hitting numbers are 6,5,4. The final value violates the target-6 lower bound 5. No primitive implementation of this prescribed endpoint sequence can avoid that failure because its final tuple itself has tau=4.

This is not a counterexample to exact-endpoint unit connectivity: the prescribed final tuple is not exact-6. Nor is it a native barrier claim. It refutes the proposed unguarded iteration of graph-style cloning on higher hyperedges. It is a symbolic proof, not a sampled case count or locally executed numerical search.

## 7. What remains

We now have an arbitrary-floor local exchange rule with two separately explicit obligations: enough compatible root slots for the copied supports, and a guard establishing that completed clones do not lower tau. An existing pair root supplies that guard even when other roots are larger. The root-slot criterion handles heterogeneous floors without assuming that a scalar degree count is enough.

In genuinely higher-floor regions with no pair/singleton guards, the graph proof's guard is absent. A future universal argument must either replace it by a different completed-exchange invariant or restore exactness before spending another lower unit. No such restoration or global termination theorem is proved here. General higher-floor connectivity remains OPEN beyond the earlier scoped results.

Conditional native lifting, certification boundaries and the lack of physical interpretation remain unchanged. Independent review must check the arbitrary-floor star guard, sorted slot criterion, equal-cardinality independent-set argument, use of an EXISTING pair root, the exact symbolic hitting numbers, and the distinction between failure of an iteration and disconnected exact/native states. No implementation or numerical campaign is initiated.
