# C3 capacity-bit observability: conditional extraction and exact obstruction

Date: 2026-10-07.
Status: ANALYTICAL CANDIDATE / AUTHOR-SIDE PROOF, independent review pending.
Frozen scope: COUPLED_C3_CAPACITY_OBSERVABILITY_SCOPE.md at 0b8d59969c33f77410a543b0bd997a501b717b56.

## 1. Declared family and three interfaces

Let E(Z)=({a,b},{b,c},{a,c},{d,e} union Z), C(Z)=({b,d},{b,c},{c,d},{a,e} union Z), where Z is an arbitrary invariant spectator subset disjoint from core labels and w. All original floors f_i=2; native primitives toggle one incidence and must preserve 3<=tau<=4 and floors.

The previously closed retained core record R retains only core-projected labelled endpoint supports, floors, w availability and protected band. It omits |E4|, |Z| and any flag for Z nonempty.

I0=R alone.
I1=R plus the actual source floor slack sigma4=|E4|-f4, if independently available.
I2=R plus a nondestructive Boolean native legality query for the hypothetical deletion -d(r4), if independently available.

I1 and I2 are CONDITIONAL interfaces, not declared existing observer capabilities.

## 2. Exact slack identity

Since E4={d,e} union Z, with Z disjoint from d,e,
    |E4|=2+|Z|,  f4=2,
so
    sigma4=|E4|-f4=|Z|.

Therefore
    b=1[Z nonempty]=1[sigma4>=1].

If sigma4 is genuinely already retained, b is a deterministic threshold of an existing native count and need not be separately inserted. This is a mathematical reduction, not proof that an observer has access to sigma4.

## 3. Exact legality oracle identity

At E(Z), consider the hypothetical primitive -d(r4). The resulting fourth root is {e} union Z.

The first three roots remain the source triangle {a,b},{b,c},{a,c}, with hitting number2. Since {e} union Z is nonempty and disjoint from all three triangle roots, the full hitting number is exactly3 for EVERY Z, including Z empty.

Thus the protected-band condition is ALWAYS satisfied by the hypothetical deletion. Its legality depends ONLY on the original floor:
    |{e} union Z|=1+|Z| >=2
iff
    |Z|>=1.

Consequently
    L(E(Z),-d(r4))=1
iff b=1.

A nondestructive native legality oracle, IF supplied, returns precisely the missing one-bit distinction in this family. Checking tau alone cannot distinguish the fibers because tau=3 after the hypothetical deletion even for Z empty.

## 4. I0 impossibility

For any Z and Z', the declared core projection R(E(Z),C(Z))=R(E(Z'),C(Z')).

In particular empty and nonempty Z yield identical I0 inputs but opposite b. No deterministic function g(R) can equal b for both, by equality of inputs and inequality of outputs.

The independently closed hidden-optimality theorem establishes that the shortest protected path has length8 for Z empty and length6 for Z nonempty. Thus no I0-only deterministic controller can select a shortest path in both fibers. This is an indistinguishability argument about the DECLARED projection, not a general physical observation theorem.

## 5. Conditional sufficiency of I1 or I2

If I1 supplies sigma4, compute b=1[sigma4>=1].

If I2 supplies a nondestructive legality bit L(E,-d(r4)), set b=L.

Then choose:
- b=0: the closed eight-edit +w(r4) buffer route;
- b=1: the closed six-edit endpoint-only -d(r4) first route.

Both routes are exact, floor-legal, and keep tau=3. They preserve hidden Z without inspecting its members.

This does NOT imply either I1 or I2 is available in the original retained framework. Merely knowing a formula for sigma4 is not an information-access mechanism; evaluating |E4| from hidden supports would be a full-state read unless an independently justified retained count already exists.

Likewise a hypothetical legality query is an additional observation channel unless derived from existing permitted operations. Executing -d(r4) as a probe is NOT equivalent to querying its legality: for Z empty it violates floor2, so it is forbidden. An attempted edit with feedback cannot be assumed as a harmless read.

## 6. Necessity and information boundary

At least two distinct retained input classes are required to choose a shortest repair across empty and nonempty Z. One binary distinction is sufficient. This lower bound is only for this declared two-policy family and chosen exact objective; it is not a general Shannon entropy or observer theorem.

I0 cannot derive b.
I1 and I2 each derive b CONDITIONALLY on being genuinely accessible.
Without a pre-existing justified retained slack or legality-observation channel, the result is an observability obstruction, not closure of the broader C3 observer problem.

## 7. Rejecting controls

A. Empty Z: E4={d,e}, sigma4=0. Hypothetical -d gives {e}, tau remains3 but floor2 fails. Hence L=0.
B. Nonempty Z={z}: E4={d,e,z}, sigma4=1. Hypothetical -d gives {e,z}, tau remains3 and floor2 holds. Hence L=1.
C. Both fibers have identical core R and both hypothetical states have tau=3; tau-only observations cannot distinguish them.
D. Counting hidden spectator incidences from a full state is not an R-only computation.
E. Applying the forbidden edit at empty Z to learn the outcome violates native admissibility and cannot be used as a proof of safe observation.

## 8. Next research obligation

Inspect the existing UQCF-GEM retained-data interface to determine whether original root cardinality/slack or nondestructive hypothetical-edit legality is ALREADY derived from ordered-event information. If not, record a precise interface obstruction and do not add a new observation primitive.

This is not a physical derivation of gravity, geometry, force, energy, continuum or fundamental time. The broader C3 retained host-selection and C4-C6 remain OPEN.
