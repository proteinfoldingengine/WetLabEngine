# Phased retained-event interface theorem

Date: 2026-10-06 (America/Phoenix).
Status: ANALYTICAL RESULT CANDIDATE WITH COMPLETE ARGUMENT.
Scope freeze: PHASED_EVENT_INTERFACE_SCOPE.md at 66556bbeb7c49a17e1a53f6efa59da8bda8c94d9.
Evidence: written mathematics only.

## 1. Retained phased-event system

Let X be a declared class of protected full labelled incidence states with original floors and 3<=tau<=4. Let pi:X->R be a retained-record map.

A repair instance has a finite set N of native endpoint-differing incidence events and a finite set H of proof-only handoff markers. Markers alter no incidence.

Each native event belongs to one labelled endpoint obligation. The event set is COMPLETE: executing every native event exactly once, while no event is undone, produces the declared exact labelled destination.

At retained state r, derive a finite directed graph
    K(r)
on the unfinished vertices N union H using retained certificate/address/phase data only.

An indegree-zero native event is executable. An indegree-zero marker may fire as a bookkeeping/certificate transition.

For every reachable retained state require:

H1. Fiber-uniform native legality:
every authorized native event is syntactically legal, respects its original root floor and stays in 3<=tau<=4 for every hidden full state represented by r.

H2. Uniform retained update:
every authorized native event or marker v has one deterministic successor
    r'=Phi_v(r)
for every hidden full state in the retained fiber.

H3. Exact event accounting:
native vertices are distinct endpoint-differing incidence toggles, executed once; markers toggle nothing.

H4. Renewal:
after v, the retained-derived unfinished graph is exactly K(r) with v deleted, or an explicitly isomorphic retained-derived residual graph.

H5. Hidden-invariant preservation when declared:
events neither read nor alter the hidden invariant incidence family.

## 2. Acyclic phased completion theorem

**Theorem E.**
If initial K(r0) is acyclic and H1-H4 hold at every reachable retained state, repeated execution of ANY indegree-zero vertex terminates with an exact protected native repair.

### Proof

A finite nonempty DAG has an indegree-zero vertex.

If that vertex is native, H1 makes its primitive legal for every hidden full state in the current retained fiber. If it is a marker, it changes no incidence.

H2 gives one next retained record without identifying the hidden state.

H3 prevents repeated/opposite bookkeeping from corrupting the endpoint accounting.

H4 deletes the executed vertex. An induced/residual subgraph of a DAG remains acyclic.

Thus the argument repeats until no vertices remain.

Rank
    rho=number of unfinished native events + markers
decreases by one at each step, so termination is finite.

All native endpoint-differing events have then occurred exactly once and no marker altered the state. By completeness of N, the exact labelled destination is reached. Every native primitive was protected and floor-legal by H1. QED.

## 3. No hidden-state read

At each step the controller sees only retained r and K(r).

The selected vertex is legal for every hidden state in the fiber by H1, and all hidden successors share one retained record by H2.

Therefore neither event choice nor retained update requires identifying the actual full incidence state.

If H5 applies, hidden invariant distinctions may remain non-injective through the entire exact repair.

## 4. Atomic macro policy is strictly stronger

Partition native event vertices by endpoint obligation.

Define the ATOMIC-CONTIGUITY policy:

Once the first native event belonging to obligation v is executed, every remaining native event belonging to v must execute consecutively before any native event of another obligation. Proof-only markers may not be used to insert another obligation's native preparation inside that atomic block.

This is stronger than event-DAG legality.

An acyclic event graph may have no topological order satisfying atomic contiguity. In that case the phased retained repair exists while the atomic macro abstraction deadlocks or requires a different coarse policy.

This statement is about a scheduling constraint. It is NOT ordinary graph contraction, and no theorem here says contraction of an event DAG must be cyclic.

## 5. Concrete embedding of the closed macro-cycle carrier

Use MACRO_CYCLE_RESULT.md at
    956d270b653a2c7eb23683de356674dd17027188.

Native events:

    Pp  = Add b to p
    Pq  = Add b to q
    Fr  = Delete a from r
    Fp  = Delete c from p
    Fq1 = Delete c from q
    Fq2 = Delete f from q.

Proof-only marker:
    H = replacement-cover handoff.

Retained event graph edges:

    Pp -> H
    Pq -> H
    H  -> Fr
    H  -> Fp
    H  -> Fq1
    Fq1 -> Fq2.

This graph is acyclic. One topological order is

    Pp, Pq, H, Fr, Fp, Fq1, Fq2.

Deleting marker H from execution gives exactly the previously proved six-primitive native escape path.

## 6. Retained certificate meaning of the event edges

At source the residual two-cover certificate is
    {a,c}.

### Pp

After Pp, p={b,c}. Old cover {a,c} remains valid. Therefore Pp is uniformly legal.

### Pq

After Pq, q={b,c,f}. Old cover {a,c} still remains.

Now retained cover status also shows
    {a,b}
hits every residual root:
- s through a;
- t through b;
- p,q through b;
- r through a or b.

Thus the replacement cover has become available.

### H

H fires exactly at this retained certificate overlap:
    old cover {a,c} present
and
    new cover {a,b} present.

It changes no incidence. Its role is to switch which retained certificate is used to justify later deletions.

### Finish events

After H, every Fr,Fp,Fq1,Fq2 deletion preserves b in the roots needed by {a,b}; s permanently supplies a. Hence {a,b} remains a two-cover through all finishes.

Fq1->Fq2 also records q's literal finish order: c must be deleted before the declared final f deletion in this selected schedule.

All full states in the hidden-Z fiber obey the same proof because spectator labels occur only in fixed root t and cannot lower the relevant hitting numbers, as established in the macro-cycle theorem.

Thus H1-H5 hold for this concrete event graph.

## 7. Exact incompatibility with atomic contiguity

The acyclic event graph has NO topological order satisfying the declared whole-macro contiguity policy.

### p cannot be the first atomic block

Atomic p would require
    Pp immediately followed by Fp
before another obligation's native event.

But Fp has predecessor H, and H has predecessor Pq.

Therefore Pq must occur between Pp and Fp. Atomic p contiguity is impossible.

### q cannot be the first atomic block

Atomic q would require Pq followed by Fq1,Fq2 without another obligation's native event.

But Fq1 has predecessor H and H has predecessor Pp.

Therefore Pp must occur between q's prepare and finish. Atomic q contiguity is impossible.

### r cannot be first

r has only Fr, but Fr has predecessor H, which requires both Pp and Pq.

Therefore r cannot be the first atomic macro.

So the event DAG is acyclic and executable, while no obligation can supply an initial contiguous macro block.

This recovers the closed complete-macro empty-source deadlock as a RESOLUTION/CONTIGUITY effect.

## 8. Hidden multiplicity

The closed carrier allows arbitrary hidden Z subseteq T on fixed root t.

All 2^|T| choices have:
- identical retained core cover trajectory;
- identical event graph;
- identical topological event schedule;
- identical handoff point H.

No event reads or changes Z.

Therefore the phased quotient remains non-injective through exact completion.

## 9. What the handoff marker represents

H is not a physical event and not an incidence change.

It certifies a logical transition:

    before H:
        old certificate is guaranteed;

    at H:
        old and replacement certificates coexist;

    after H:
        replacement certificate is guaranteed.

The event graph therefore separates two notions that atomic macros conflated:
- installing replacement protection;
- consuming old protection.

This is why two unfinished obligations can cooperate to make progress when neither can safely finish alone.

## 10. Advancement

The retained scheduling hierarchy is now formal:

    macro DAG
        -> whole obligations can finish sequentially;

    macro deadlock
        -> no whole obligation can finish first;

    phased event DAG
        -> preparations from several obligations can coexist;

    certificate handoff
        -> replacement protection becomes valid;

    finish phase
        -> old incidences can be removed safely.

The macro-cycle carrier is a concrete case where the phased graph is acyclic while the atomic-contiguity policy has no legal first block.

## 11. Next frontier: automatic handoff derivation

The phased interface still receives its prepare/finish partition and handoff marker as supplied structure.

The next theorem should derive them from retained certificate changes.

For target-four cover protection, a natural target is:

1. identify which additions are sufficient to install a replacement <=4 cover;
2. order those additions before every deletion that can destroy the current cover;
3. place a handoff marker once the replacement cover is guaranteed over the entire retained fiber;
4. derive the remaining finish-event precedence automatically.

A dual construction should eventually handle lower pair-witness handoff as well.

The scientific question is whether certificate-overlap conditions alone generate the phased event graph, rather than a human supplying the safe interleaving.

No physical force, geometry, energy, observer field or fundamental time is inferred.
