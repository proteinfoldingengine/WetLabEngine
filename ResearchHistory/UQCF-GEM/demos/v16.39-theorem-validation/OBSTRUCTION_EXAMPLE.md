# Nested restricted support does not itself force a nonunit barrier

Status: hand-derived mathematical example, independently reviewed. No numerical execution; no smallest-witness claim.

Use k=3 with root r, children u and v, and children a,b of u. Vertices v,a,b are leaves. The initial supports are

| Vertex | r | u | v | a | b |
|---|---|---|---|---|---|
| X | 123 | 12 | 3 | 1 | 2 |
| Z | 123 | 12 | 3 | 2 | 1 |

Here 12 denotes {1,2}, etc. Both endpoints have q_r=q_u=2 and all leaf coordinates zero. The active vertices r,u are nested; neither is saturated (q=3). The support S_u=12 is proper, so SC and the endpoint full-support condition fail.

Each endpoint is an isolated vertex in the exact fiber. With two children, q_r=2 requires S_u and S_v to be disjoint. Meanwhile q_u=2 requires |S_u|>=2. Since k=3 and S_v is nonempty, S_u has exactly two labels and S_v the remaining one. Neither support admits a legal single-label change preserving q. The two nonempty disjoint child supports inside S_u must then be its two distinct singletons, which likewise cannot change in the exact fiber.

Nevertheless a four-move path changes only the child coordinate:

    (S_a,S_b): (1,2) -> (12,2) -> (12,12) -> (2,12) -> (2,1).

All other supports stay fixed. At the three intermediate states q_u=1 and q_r=2. This proves all primary barriers and LEX_BARRIER equal 1, using the zero-cost disconnection just proved for the lower bound.

There is also an eight-move path that moves the deficit to the parent while preserving q_u=2:

1. Add label 3 to S_u: q_r becomes 1.
2. Change S_a: 1 -> 13 -> 3 (two moves).
3. Change S_b: 2 -> 12 -> 1 (two moves).
4. Change S_a: 3 -> 23 -> 2 (two moves).
5. Remove label 3 from S_u: q_r returns to 2.

The child supports remain disjoint throughout this second route, so q_u remains 2. Every move preserves nonempty nested supports. The spare label is NOT necessary for a unit barrier in this example; its role is to move the temporary deficit from the child to its parent.

The next proof problem is therefore stronger than finding nested activity or a restricted palette. It must determine whether local changes can always be scheduled with one temporary coordinate deviation, possibly moving that deviation between ancestor and descendant, or whether some admitted structure forces simultaneous deviations or magnitude at least two. Failure of one chosen repair strategy would not prove failure of every unit path.
