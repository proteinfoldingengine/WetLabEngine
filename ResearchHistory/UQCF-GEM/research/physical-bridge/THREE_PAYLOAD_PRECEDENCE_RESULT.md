# Concrete three-payload precedence realization theorem

Date: 2026-10-06 (America/Phoenix).
Status: ANALYTICAL RESULT CANDIDATE WITH COMPLETE ARGUMENT.
Final scope freeze: THREE_PAYLOAD_PRECEDENCE_SCOPE.md at 005857e5b486e07545d91bd89f161a59c0ac972d.
Evidence: written mathematics only.

## 1. Carrier

Core labels are a,b,c,d,e. T is a spectator palette of size s>=1.

Controlled roots:
    A={d}, B={e}, G={a,b,c}.

Invariant environment:
    h={b}.

Payload sources:
    p={a} union Z, arbitrary hidden Z subseteq T;
    q={a};
    r={a}.

All floors are1.

Exact targets:
    p={b} union Z,
    q={c},
    r={b}.

Each payload macro replaces a by its target core x using
    Add x, then Delete a.

Retained data are:
- labelled target address D;
- completion/phase bookkeeping;
- core-projected residual miss counts M_core(H) for nonempty H subseteq {a,b,c,d,e}, |H|<=4.

Z is not retained or read.

## 2. Deriving the graph from retained data

At source the residual roots are p,q,r,h with core states a,a,a,b.

Therefore
    M_core({b})=3,
    M_core({c})=4.

The retained carrier promise says h is the invariant environment and payload source cores are a. The strict miss-count difference identifies b as the environment core.

From D, the unfinished payloads targeting b are initially
    Bset={p,r},
and the unfinished payload targeting c is
    Cset={q}.

Derive one edge u->v for every unfinished u in Bset and v in Cset.

Thus initial graph is

    p -> q
    r -> q.

This derivation uses M_core, D and completion bookkeeping only. Z cannot affect any M_core coordinate because it is disjoint from the core palette.

After an eligible b-target macro completes, update M_core by the core miss-count formula and mark that payload complete. Recomputing Bset,Cset on the unfinished obligations gives exactly the induced graph obtained by deleting that payload vertex.

Hence graph renewal is exact.

## 3. Source and target hitting numbers

At source:
- A forces d;
- B forces e;
- q and r force a;
- h forces b.

Thus every cover contains a,b,d,e. Those four labels hit p through a and G through a or b. Therefore
    tau_source=4.

At target:
- A,B force d,e;
- q={c} forces c;
- r={b} and h={b} force b.

Set {b,c,d,e} hits p through b and G through b or c. Hence
    tau_target=4.

Z does not alter either lower bound.

## 4. Uniform legality of an eligible b-target macro

Suppose u is an unfinished b-target payload, either p or r.

Before its macro, q remains unfinished at {a}. At least q therefore forces a, while h forces b and anchors force d,e.

### Addition

After Add(u,b), q still forces a and h forces b. Therefore a,b,d,e are forced and form a four-cover. tau=4.

### Deletion

After Delete(u,a), q still forces a and h forces b. Again a,b,d,e are forced and cover every root:
- completed u through b;
- the other unfinished b-target through a if still unfinished, or b if already complete;
- q through a;
- G through a/b.

Thus tau=4.

If u=p, Z is untouched and irrelevant to the argument.

Therefore either indegree-zero b-target macro is uniformly legal over every hidden Z.

## 5. Exact renewal after one b-target

If p completes first, remaining obligations are r,q and retained graph is
    r -> q.

If r completes first, remaining graph is
    p -> q.

The completed b-target and h both contain b. The remaining unfinished b-target still has core a. q still has core a.

The same Section4 proof shows the remaining b-target is legal next.

Thus both topological prefixes p,r and r,p are protected.

## 6. q is uniformly unsafe while any b-target remains unfinished

Assume q is repaired while at least one of p,r remains unfinished.

### Addition to q

q becomes {a,c}. Since it still contains a, the previous four-cover {a,b,d,e} remains valid. The same forced anchors/environment and at least one a-containing payload give tau=4.

### Deletion from q

q becomes singleton {c}.

If r remains unfinished, r={a} forces a. Then:
- r forces a;
- h forces b;
- q forces c;
- anchors force d,e.

Five distinct core labels a,b,c,d,e are mandatory, and those five labels cover all roots. Hence tau=5.

If r is already complete, then p must be the unfinished b-target. Its support is {a} union Z. Any hitting set must contain:
- b for h (and completed r);
- c for q;
- d,e for anchors;
- and either a or one spectator z in Z to hit p.

The fifth label is distinct from b,c,d,e because Z is disjoint from the core palette. If Z is empty, a is mandatory. Thus every cover has size at least5, and a five-cover exists using a (or any z in nonempty Z) together with b,c,d,e.

Therefore tau=5.

So q's complete macro is uniformly forbidden until BOTH incoming predecessor obligations p,r are complete.

This proves both precedence edges over the entire hidden fiber.

## 7. q becomes legal after both predecessors complete

After p and r complete:
    p={b} union Z,
    r={b},
    h={b},
    q={a}.

Anchors force d,e and b is forced by r/h. q forces a, so tau=4 with cover {a,b,d,e}.

After Add(q,c), q={a,c}; the same cover remains and tau=4.

After Delete(q,a), q={c}. Now b,c,d,e are forced and form a four-cover. tau=4.

Thus q is legal exactly at the retained precedence boundary required by the policy.

## 8. Exact completion and topological orders

The initial DAG has two sources p,r.

Allowed topological macro orders are
    p,r,q
and
    r,p,q.

Sections4-7 prove every primitive in either order has tau=4 and respects floors.

Each macro completes one exact labelled target and never changes another completed payload.

After three macros=six primitive edits:
    p={b} union Z,
    q={c},
    r={b},
with h and controlled roots unchanged.

This is the exact labelled destination.

Rank |U| decreases 3->2->1->0.

## 9. Hidden multiplicity

For every Z subseteq T:
- source M_core is identical;
- D is identical;
- derived graph is identical;
- both allowed topological macro orders are identical as choices;
- M_core update trajectory depends only on core edits;
- exact hitting-number proofs above remain valid.

There are 2^s distinct full labelled source states and corresponding exact targets represented by the same retained record.

No macro reads or changes Z, so all 2^s hidden trajectories remain distinct and exact.

## 10. Why the scope was narrowed before proof

If arbitrary spectators were allowed on every payload, a spectator shared between q and the last unfinished b-target could supply one label that hits both roots after q leaves a. Then the nominal tau5 rejecting state could have a four-cover.

That would make an edge derived without spectator information non-uniform over the retained fiber, violating the precedence-interface hypothesis.

The final carrier deliberately keeps q and r spectator-free while retaining arbitrary hidden Z on p. This preserves genuine hidden multiplicity and makes both edges fiber-uniform.

This narrowing is a mathematical consequence of the retained-quotient discipline, not a cosmetic restriction.

## 11. Advancement and remaining cycle question

This is the first concrete retained graph with:
- three labelled obligations;
- two independently derived nontrivial edges;
- more than one valid topological order;
- exact graph renewal after either source macro;
- a rejecting tau5 control for violating either edge;
- non-injective hidden fibers.

It realizes the abstract precedence interface beyond the one-edge two-payload example.

A genuine directed-cycle carrier is still open. The next task is to determine whether native target-four certificate formulas can derive a cycle such as
    p->q->r->p
for a declared complete-macro policy while keeping every endpoint protected, and if so whether another native/interleaved path bypasses that macro deadlock.

No physical force, geometry, energy, observer field or fundamental time is inferred.
