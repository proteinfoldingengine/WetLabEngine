# C3 semantic-commit observability — author-side argument audit

Date: 2026-10-08.
Status: AUTHOR-SIDE AUDIT; independent review pending.
Frozen scope e94d45e4299dd556d44fbd587ebfa94d9c420ef7.
Proof candidate b517c1343d707fb3a320cbd3d3664338059f66a5.

1. Initial z absent, so +z(r4) is syntactically legal as a native primitive.
2. World C commits that primitive; World R rejects the attempted command before any native change. Rejection is a no-op, NOT a native transition.
3. Same initial state and same issued signed +z(r4) record in both worlds.
4. Same core projections and every M_core(H) coordinate because spectator z lies outside P0.
5. Triangle transversal2 plus disjoint r4 gives tau3 in both; floor2 valid in both.
6. Different actual commit bits c=1 versus0, and different final capacity b=1 versus0, imply impossibility of a deterministic estimator using only attempt+O_core.
7. Stronger semantic acknowledgement, root4 cardinality/slack, or initialized full-palette singleton miss count distinguish.
8. Always-successful semantic commit guarantee would remove this pair's ambiguity but is not derived.
9. This is distinct from earlier two fully committed histories with hidden directions.
10. No universal observer or physics conclusion.

Rejecting control: counting attempted commands as committed would falsely increment q in World R. Counting rejection as a native deletion is invalid.
