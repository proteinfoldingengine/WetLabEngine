# Phased retained-event interface scope

Date: 2026-10-06 (America/Phoenix).
Status: PROSPECTIVE ANALYTICAL SCOPE.

Parent macro-cycle closeout:
- MACRO_CYCLE_CLOSEOUT.md at 430bf224c7e83da105e76f830d316fdf44efc269.
Parent retained precedence interface:
- PRECEDENCE_INTERFACE_CLOSEOUT.md at e81c236b707d2ed1c5e07ebe806858bac83f1f25.

## Objective

Replace atomic endpoint macros by a retained phased-event interface that can represent safe interleaving.

Each endpoint obligation may have:
- PREPARE events that install endpoint-required incidences;
- a proof-only CERTIFICATE HANDOFF marker when replacement protection becomes available;
- FINISH events that remove old incidences.

Prove that a finite acyclic retained event graph with fiber-uniform event legality/update gives exact protected completion even when no legal execution exists under the stronger rule that every obligation's prepare+finish events must occur contiguously as one atomic macro.

Do NOT identify atomicization with ordinary graph contraction. The obstruction is the extra contiguity constraint.

## Retained event system

Let pi:X->R be a retained quotient of protected full labelled incidence states.

Let E be a finite set of native incidence events partitioned among labelled endpoint obligations. Add proof-only handoff markers H that change no incidence.

A retained event graph K(r) has vertices E union H and edges derived only from retained certificate/address data.

A native event vertex is authorized when indegree zero. A marker may fire when indegree zero and only updates retained phase/certificate bookkeeping.

Required hypotheses for every reachable retained state:
1. FIBER-UNIFORM LEGALITY: every authorized native event is legal for every hidden full state in the retained fiber.
2. UNIFORM RETAINED UPDATE: every authorized event/marker has one deterministic retained successor independent of hidden state.
3. EXACT EVENT ACCOUNTING: each native endpoint-differing incidence event occurs once; markers alter no incidence.
4. RENEWAL: after an event/marker, the newly derived graph is the old graph with that vertex removed (or an explicitly equivalent retained-derived residual graph).
5. FLOOR SAFETY: event certificates include original floors.
6. HIDDEN-INVARIANT PRESERVATION when declared.

## Required theorem

A. If initial K is acyclic and the hypotheses hold, repeated indegree-zero execution terminates after all event vertices/markers, with every primitive protected and exact labelled endpoint restored.

B. Rank = number of unfinished event/marker vertices decreases.

C. No hidden-state read is required because legality/update are uniform over each retained fiber.

D. Atomic macro execution is a STRICTER policy: for each obligation, once its first native event executes, all of that obligation's remaining native events must execute consecutively before any other obligation's native event. An acyclic event graph need not admit any topological order satisfying this contiguity constraint.

E. Therefore atomic macro deadlock/cyclic precedence may coexist with an acyclic event graph. Scope this as a resolution effect, not native disconnection.

## Concrete embedding: closed macro-cycle carrier

Use MACRO_CYCLE_RESULT.md at 956d270b653a2c7eb23683de356674dd17027188.

Native event vertices:
    Pp = Add b to p
    Pq = Add b to q
    Fr = Delete a from r
    Fp = Delete c from p
    Fq1 = Delete c from q
    Fq2 = Delete f from q

Proof-only marker:
    H = replacement-cover handoff.

Derive retained event edges:
    Pp -> H
    Pq -> H
    H -> Fr
    H -> Fp
    H -> Fq1
    Fq1 -> Fq2

and any exact syntax/phase edges required by the declared q finish.

Prove:
- K is acyclic;
- its topological order Pp,Pq,H,Fr,Fp,Fq1,Fq2 gives the closed six-primitive path (marker omitted);
- before H, old residual cover {a,c} remains;
- H is enabled exactly when retained cover status shows new cover {a,b} also exists;
- after H, {a,b} protects every finish event;
- all hidden Z fibers behave identically.

## Atomic incompatibility

For the same carrier, prove no atomic complete macro p,q,r is legal first, as already closed. Therefore no topological event execution can also satisfy the declared macro-contiguity policy from the initial state.

Do not claim that graph contraction itself yields a canonical cycle. The atomic policy's empty eligible set is the exact statement.

## Next frontier if successful

Derive phased event graphs automatically from retained cover/witness changes rather than supplying the prepare/handoff partition manually. Seek a certificate-overlap criterion that says when old protection may hand off to new protection and which additions must precede which deletions.

No physical force, geometry, energy, observer field or fundamental time.
