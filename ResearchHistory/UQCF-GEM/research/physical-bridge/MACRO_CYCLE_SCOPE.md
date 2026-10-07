# Retained macro-cycle realizability scope

Date: 2026-10-06 (America/Phoenix).
Status: PROSPECTIVE ANALYTICAL SCOPE.

Parent three-payload closeout:
- THREE_PAYLOAD_PRECEDENCE_CLOSEOUT.md at d7394285e70d21476dadc08ffd713a4787799e35.
Parent precedence interface:
- PRECEDENCE_INTERFACE_CLOSEOUT.md at e81c236b707d2ed1c5e07ebe806858bac83f1f25.

## Objective

Determine whether a protected target-four native carrier can realize a genuine deadlock of the COMPLETE-MACRO retained policy while remaining natively connected by finer interleaving.

## Carrier

Core residual labels U={a,b,c,f}. Add forced anchor labels d,e and optional spectator labels T.

Full controlled anchors:
    A={d}, B={e}.

Residual fixed roots:
    s={a};
    t={b,c,f} union Z, where arbitrary invariant Z subseteq T.

Three labelled payload roots:
    p={c};
    q={c,f};
    r={a,b}.

All floors1.

Exact residual targets:
    p'={b};
    q'={b};
    r'={b}.

Z and fixed roots remain unchanged.

Full hitting number equals residual hitting number plus2 because singleton anchors d,e are disjoint from every residual support.

## Declared endpoint macros

p: Add b, then Delete c.
q: Add b, then delete c and f in a fixed declared order.
r: Delete a (b is already present).

A complete-macro policy may start a macro only if all its primitives can be completed consecutively while staying in 3<=tau<=4.

## Required endpoint/one-macro theorem

Prove:
- residual source tau=2 with unique size2 cover {a,c};
- residual target tau=2 with unique size2 cover {a,b};
- hence full source and target tau=4;
- completing p alone, q alone, or r alone from the source gives residual tau=3 and full tau=5.

Therefore no complete macro is initially eligible. The complete-macro retained policy deadlocks immediately.

Represent the deadlock as a cyclic/non-source precedence state; do not pretend a unique orientation is canonical if the retained certificate only proves that every macro has an unmet predecessor/preparation requirement.

## Required native interleaving escape

Prove the following primitive schedule stays at full tau4:
1. Add b to p.
2. Add b to q.
3. Delete a from r.
4. Delete c from p.
5. Delete c from q.
6. Delete f from q.

After the first two additions, both residual covers {a,c} and {a,b} are available. The remaining deletions preserve {a,b}.

Prove exact labelled destination and floors.

## Retained interpretation

Define retained cover status for residual two-sets. The source certificate records {a,c}; after p/q preparation the retained certificate records both {a,c} and {a,b}; after the deletions it records {a,b}.

Thus the escape requires a finer event/phase retained state than the atomic complete-macro DAG interface.

## Hidden multiplicity

Allow arbitrary Z only on fixed root t={b,c,f} union Z. Prove Z never lowers any relevant hitting number: any hitting set using z in Z to hit t can replace z by an element of {b,c,f} without increasing size and without losing hits on any other root, because z occurs nowhere else.

Hence all 2^|T| choices of Z share the same retained core certificate and primitive schedule while remaining distinct full states.

## Boundaries

The deadlock is for the complete-macro retained policy only. The explicit primitive path proves native connectivity in this carrier.

Do not claim a canonical directed 3-cycle if only a more general cyclic/deadlocked precedence relation is derived. State exactly what the certificate proves.

If successful, next frontier is an EVENT-LEVEL retained precedence interface that derives prepare/switch/finish phases and proves when interleaving resolves macro cycles.
