# Symbolic tests of the sequential handover argument

These are hand-derived examples, not executed scientific tests or an arity campaign. They compare proof mechanisms in already solved floor-one carriers. Their role is to establish strict improvement of a sufficient method and delimit its failure; they do not assert progress by counting passing instances.

## 1. Sequential handover succeeds while the full union bridge fails

Use P={a,b,c,d,e}, four roots with floor one, q=4, t=3, and

    A=({a},{b},{c},{d}),
    C=({b},{e},{d},{c}).

Each endpoint consists of four distinct singleton supports and is exact-q. Choose I={1,2,3}, J={1,2,4}, so K={1,2}. Prepare root 4 to {c}, obtaining ({a},{b},{c},{c}) with transversal three. The fixed family F consists of roots 3 and 4, both {c}.

The full shared-slot union tuple is ({a,b},{b,e},{c},{c}); its transversal is two, witnessed by {b,c}, and cannot be lower. Thus the earlier bridge fails even on the full tuple.

For the sequential criterion, a small H hitting F must contain c and have at most one other label. H={c} gives L=R={1,2}. Adding a gives L={2}, R={1,2}; adding e gives L={1,2}, R={1}; adding d leaves L=R={1,2}. Adding b is the only disjoint case: L={1}, R={2}. Therefore the complete set of disjoint-miss obligations consists of the single precedence 2->1.

Process root 2 first: {b}->{b,e}->{e}. The other relevant supports {a} and {c} are disjoint from this edited support, so the transversal remains three. Then process root 1: {a}->{a,b}->{b}; the now fixed supports {e} and {c} again maintain transversal three. J is complete. Finally replace root 3 by {d} through {c,d}, protected by J. The final tuple is C with transversal four; every earlier state has transversal three or four and respects the floors. All changes are one incidence.

The improvement is the completion of new protection at slot 2 before removing the last old protection at slot 1. The new support survives unchanged through the second edit; no exactness assumption is silently renewed at the intermediate level three.

## 2. A forced cycle blocks every schedule in the restricted class

Return to METHOD_LIMITS.md: P={1,2,3,4}, A=({1},{2},{3},{4}), C=({2},{1},{4},{3}), q=4, and the same I={1,2,3}, J={1,2,4}. After preparation, F consists of two {3} roots and K={1,2}.

For H={1,3}, L={2}, R={1}, forcing 1->2. For H={2,3}, L={1}, R={2}, forcing 2->1. These singleton witness pairs leave no selection freedom. Every possible certificate graph contains that directed cycle. S3 therefore rules out every one-pass whole-root union order after this fixed preparation, not merely the simultaneous full union bridge.

Nevertheless the exact endpoints admit the valid pair-swap repair already exhibited in METHOD_LIMITS.md. That repair changes the schedule before this problematic preparation and interleaves the two root exchanges. The forced cycle is thus an exact obstruction for the restricted handover method, not a root or native connectivity obstruction.

## 3. Next question

For exact higher-floor endpoints, determine which forced precedence cycles can be broken by an admissible change of preparation, guard choice, or protected partial exchange within the existing slots. A complete result needs a new lower-bound certificate throughout cycle resolution, a renewable condition after it, and a progress argument that proves an eligible resolution remains available. The endpoint capacity inequalities alone have not supplied that theorem.
