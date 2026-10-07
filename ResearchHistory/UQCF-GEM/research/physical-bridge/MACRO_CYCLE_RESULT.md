# Retained macro-cycle realizability and interleaving escape theorem

Date: 2026-10-06 (America/Phoenix).
Status: ANALYTICAL RESULT CANDIDATE WITH COMPLETE ARGUMENT.
Scope freeze: MACRO_CYCLE_SCOPE.md at a0a1f6a9205375f2ca2c844702d7264791650487.
Evidence: written mathematics only.

## 1. Carrier

Residual core universe is U={a,b,c,f}. Full palette additionally contains forced anchors d,e and spectator set T.

Controlled singleton anchors:
    A={d}, B={e}.

Residual fixed roots:
    s={a};
    t={b,c,f} union Z,
where Z is any subseteq T and spectator labels occur nowhere else.

Payload source roots:
    p={c};
    q={c,f};
    r={a,b}.

All floors are1.

Targets:
    p*={b};
    q*={b};
    r*={b}.

Fixed roots and Z are unchanged.

Because d,e occur only in their singleton anchors and no residual support contains them, every full hitting set contains d,e. Removing them leaves exactly a residual hitting set. Therefore

    tau_full = 2 + tau_residual

at every state of the declared repair.

## 2. Exact source and target covers

### Source

Root s={a} forces a in every residual hitting set.
Root p={c} forces c.

Thus every residual cover has at least {a,c}.

Set {a,c} hits:
- s through a;
- t through c;
- p through c;
- q through c;
- r through a.

Therefore residual tau=2 and {a,c} is the UNIQUE size-two residual cover: any two-cover must contain forced a and c.

Hence full source tau=4.

### Target

At target, s={a} forces a and p*={b} forces b. Thus every residual cover has at least {a,b}.

Set {a,b} hits t through b and p*,q*,r* through b. Therefore target residual tau=2 and {a,b} is the unique size-two residual cover.

Hence full target tau=4.

The spectator set Z does not enter either argument.

## 3. Every complete macro is initially unsafe

Declared macros are:

p:
    {c}->{b,c}->{b}.

q:
    {c,f}->{b,c,f}->{b,f}->{b}.

r:
    {a,b}->{b}.

We evaluate the prepared state after completing each macro alone while leaving the other payloads at source.

### Complete p alone

Residual roots include
    s={a}, p={b}, q={c,f}.

Any hitting set must contain:
- a for s;
- b for p;
- c or f for q.

These are three distinct labels. Set {a,b,c} hits every residual root, including t and r. Therefore residual tau=3 and full tau=5.

### Complete q alone

Residual roots include
    s={a}, p={c}, q={b}.

They force distinct a,c,b. Set {a,b,c} hits t and r as well. Therefore residual tau=3 and full tau=5.

### Complete r alone

Residual roots include
    s={a}, p={c}, r={b}.

They force a,c,b. Again {a,b,c} hits t and q. Therefore residual tau=3 and full tau=5.

Thus NO complete macro can be executed first while remaining in the target-four protected band.

## 4. Exact complete-macro deadlock

Under the retained precedence interface, an atomic macro is authorized only when all of its primitives can be completed consecutively while staying protected.

Section3 proves that the initial eligible set is empty although all three obligations remain unfinished.

Therefore the complete-macro policy is deadlocked at the source.

If one insists on representing this eligibility relation by a directed graph on {p,q,r} with the interface convention
    authorized iff indegree zero,
then every vertex must have indegree at least one. Every finite directed graph in which every vertex has indegree at least one contains a directed cycle: starting from any vertex and repeatedly following an incoming edge must eventually repeat a vertex.

Hence ANY faithful three-vertex precedence-graph representation of this empty-source macro state contains a directed cycle.

The certificate does NOT select a unique orientation such as p->q->r->p. Claiming a canonical 3-cycle would exceed the evidence. What is proved is genuine cyclic precedence/deadlock in the complete-macro representation.

## 5. Native interleaving escape

Now execute individual primitives rather than atomic macros:

1. Add b to p:
       p={b,c}.
2. Add b to q:
       q={b,c,f}.
3. Delete a from r:
       r={b}.
4. Delete c from p:
       p={b}.
5. Delete c from q:
       q={b,f}.
6. Delete f from q:
       q={b}.

We prove residual tau=2 after every primitive.

### Initial and first addition

Initially {a,c} is the unique two-cover.

After step1, {a,c} still hits p through c and every other residual root as before. No one-label cover exists because s forces a while p has no a. Hence residual tau=2.

### Second addition: cover overlap

After step2:
    p={b,c}, q={b,c,f}.

Old cover {a,c} still hits all residual roots.

New cover {a,b} ALSO hits all residual roots:
- s through a;
- t through b;
- p,q through b;
- r through a or b.

Thus both source and target cover families coexist at this prepared state.

Residual tau is still2 because s forces a while p lacks a, so no singleton can cover all roots.

### Remaining deletions

Steps3-6 never remove b from p,q,r or t and never remove a from s.

Therefore {a,b} remains a residual two-cover through every remaining primitive.

No singleton can cover s and p simultaneously because s={a} and p contains b but not a after step4; before step4 q/r similarly prevent a universal singleton. Directly, throughout steps3-6 there remain roots requiring a and roots disjoint from a.

Hence residual tau=2 after every step.

Therefore full tau is exactly4 throughout the six-primitive interleaved path.

## 6. Floors, syntax and exact destination

p has sizes
    1->2->1.

q has sizes
    2->3->2->1.

r has sizes
    2->1.

All floors are1, so every deletion is floor-legal.

Each addition inserts an absent b and each deletion removes a present source-only incidence.

After step6:
    p=q=r={b},
with s,t,A,B and Z unchanged.

This is the exact labelled destination.

Thus the complete-macro deadlock is NOT native disconnection.

## 7. Retained certificate trajectory

Let C_2(E) denote the set of residual two-label covers at state E, or retain its Boolean indicator over all two-sets of U.

At source:
    C_2={{a,c}}.

After preparing p only, {a,c} remains.

After preparing p and q:
    {a,c} and {a,b}
are both covers.

After r deletes a and through all finishing deletions:
    {a,b}
remains a cover; {a,c} may disappear as source incidences are removed.

Therefore the interleaving escape is visible in retained certificate space as

    old cover
       -> old cover retained
       -> old + new cover overlap
       -> new cover retained.

The crucial operation is PREPARATION without immediate completion. The atomic macro abstraction hides this intermediate overlap state and therefore creates the deadlock.

## 8. Hidden spectator multiplicity

Z is an arbitrary subset of spectator labels T on fixed root t={b,c,f} union Z.

Spectator labels occur nowhere else.

Any hitting set H using z in Z solely to hit t can replace z by b (or c or f when appropriate) without increasing cardinality:
- z hits no root other than t;
- b also hits t and may hit additional payload roots.

Thus spectator labels cannot reduce any hitting number established above.

All 2^|T| choices of Z have:
- the same residual core cover certificates;
- the same complete-macro deadlock;
- the same six-primitive escape schedule;
- the same hitting-number sequence;
while remaining distinct full labelled states.

Z is never read or changed.

## 9. What has been proved about cycles

This carrier answers cycle realizability positively at the level justified by the retained data:

- all declared endpoints are protected;
- the complete-macro policy has no eligible initial vertex;
- every faithful indegree-zero precedence representation therefore contains a directed cycle;
- the deadlock is caused by atomic completion hiding a safe prepare-overlap-finish route;
- an explicit native interleaving path bypasses the deadlock.

What is NOT proved is a unique retained-data-derived orientation p->q->r->p. The correct invariant statement is empty-source cyclic precedence for the atomic macro policy.

## 10. Advancement and next frontier

The retained scheduling hierarchy is now:

    atomic macro DAG
        works when a source macro exists;

    atomic macro cycle/deadlock
        can occur even between protected endpoints;

    event-level preparation
        can create overlap of old/new certificate families;

    finishing deletions
        can then complete the exact destination.

The next theorem should therefore refine the retained quotient interface from whole macros to PHASED EVENTS:

    PREPARE -> COVER SWITCH -> FINISH.

It should derive event-level precedence from retained cover/witness certificates, prove an acyclic event schedule when available, and show how it projects to a cyclic whole-macro graph.

This is the retained-information analogue of the earlier multi-unfinished-root repair phenomenon.

No physical force, geometry, energy, observer field or fundamental time is inferred.
