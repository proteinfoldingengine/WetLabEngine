# Escape-to-vacancy substitution — prospective verification contract

Date: 2026-10-11 UTC.
Integrated parent: `dd6b8558a395f2bad28a12c9a80853ae15937891`.
Status: **PROSPECTIVE FREEZE / NO NEW EXECUTION OR CERTIFICATION**.

This contract continues the scoped CLOSED first-source-escape theorem without changing its domain. A constructive proof lead was found while selecting the next obligation and is disclosed below before any new producer, checker, bounded enumeration, GitHub Actions run, or external review. It is not retrospectively called preregistered.

## Frozen domain

Use exactly the pair-root carrier of `COUPLED_C3_SOURCE_ESCAPE_CLOSEOUT.md`:

- finite simple isolate-free carrier graph (H) with source vertex-cover number three or four;
- positive original multiplicities (a_v);
- saturated subgraph (G);
- saturated-edge floors (a_u+a_v), nonsaturated-edge floors one;
- every current actual-label footprint contained in some original star;
- an actual current cover by at most four labels;
- original protected hidden completions fixed;
- native primitives toggle one actual label/root incidence and may resolve to NOOP.

For vertex (v), (M_v) is its incident-edge star, (T_v) its saturated trace, and (B_v) means that (H) has a vertex cover of size at most four excluding (v).

The inherited exact first-escape certificates are unchanged:

- (V(v)): (T_v=arnothing) and ((a_vge2 	ext{or} B_v)).
- (X(v,w,z)): (v,w,z) distinct, (vw,wzin E(H)), (T_vsubseteq{vw}), and ((a_vge2 	ext{or} B_v)).

## Frozen primary claim

A first vacancy is reachable **if and only if** at least one inherited (V) or (X) certificate exists.

The (V) direction is the already closed direct-vacancy construction. For every (X(v,w,z)), every chosen original actual label (x) of type (v), and every chosen original actual label (y) of type (w), freeze this canonical continuation:

1. execute the inherited normalized (X) route, ending with
   [
   F_x={vw,wz};
   ]
2. add to (x), in lexicographic root order, every edge of
   [
   M_wsetminus{vw,wz},
   ]
   so (F_x=M_w);
3. delete from (y), in lexicographic root order, every edge of (M_w), so (F_y=arnothing).

All other actual labels remain at their original stars. The final deletion is the first vacancy on this continuation. The achieved committed-edit count from the original source is
[
deg_H(v)+2deg_H(w)-2.
]
This is not an optimality claim. Optional NOOPs may stall forever; reachability is not guaranteed progress.

## Disclosed proof obligations

The analytical proof must establish, at every primitive:

1. **Floors.** Before (y) is deleted, completing (x) only adds support. While (y) is deleted, the full (M_w) footprint of (x) substitutes incidence-for-incidence. The inherited condition (T_vsubseteq{vw}) preserves every saturated edge incident to the depleted type (v); every other lost (v)-edge is nonsaturated and retains a positive label from its other endpoint.
2. **Upper-four.** If (a_vge2), a remaining original (v)-label can occupy the source cover role. If (a_v=1), use a (B_v) cover. Any cover role formerly occupied by (y) can be occupied by (x=M_w). Intermediate deletions of (y) are dominated by that full substitute.
3. **Lower-three for every original protected hidden completion.** Every current footprint remains contained in an original star; mapping any hypothetical at-most-two current cover to its original star containers would contradict the original protected lower-three condition.
4. **First-vacancy identity.** The inherited (X) route never empties (x); additions cannot empty a label; every proper deletion prefix leaves (y) nonempty.
5. **Necessity.** Any first-vacancy path has a first source escape, so the closed first-escape theorem supplies a (V) or (X) certificate.

No hidden-state legality oracle, observer output, mandatory commit rule, native input acquisition, actual-successor selector, physical force, inserted geometry, fundamental time, dark-matter variable, or numerical heuristic is introduced.

## Prospective complete bounded verification

Reuse the complete 7,360-source identity universe frozen for the first-source-escape campaign. Independently reconstruct every source, cover, (V/X) certificate, actual original (x), eligible original (y), and every canonical substitution-route slice. Retain all rejected certificate/candidate identities.

The producer and checker must independently:

- enumerate carriers, saturation graphs, multiplicity profiles, actual labels, covers, certificates, routes, and slices;
- calculate exact actual-label footprints, root-support counts, floors, hitting minima, domination witnesses, source-escape position, first-vacancy position, and achieved cost;
- compare the complete canonical record stream before hashes;
- verify every original protected one-hidden mask at every distinct declared route state;
- reconstruct every (X)-positive/(V)-negative source and require at least one such discriminator, rather than allowing the direct-(V) cases to make the primary claim vacuous;
- reproduce deterministic certificate and complete companion bytes exactly.

Finite checks corroborate the bounded universe; arbitrary positive multiplicities, arbitrary finite protected hidden completions, and the universal theorem remain proof obligations.

## Rejecting controls

Reject at least:

- omitted, duplicated, substituted, reordered, or truncated source/certificate/actual-label/route/slice/hidden-mask records;
- an invalid (X) triple, wrong original type, same (x=y), nonexistent (w)-label, or missing third vertex;
- deleting (y) before (x) has the full (M_w) footprint;
- omitting a required (M_w) addition, deleting the substitute (x), adding a root outside (M_w), or changing any third label;
- shifted floors, altered saturation, false (B_v), false upper-four cover, false lower-three claim, early vacancy, wrong final vacant label, or wrong cost;
- promotion of a safe route to mandatory progress or actual-record selection;
- any source-domain reduction chosen after observing results.

## Completion gate

Before scoped CLOSED: publish the analytical proof; obtain independent mathematical review; implement independent producer/checker and tests-first RED; execute the complete inherited stack in GitHub Actions at the exact event commit; inspect all actual logs and raw artifacts; obtain Gemini 3.1 Pro adversarial review through the proven text integration; reconcile every objection; run a separate publication audit; preserve every failure and original ZIP; publish closeout, indices, evidence, checksums, and immutable readback.

Broad C3/C4-C6, native record origin/access/retention, enforcement, actual-successor selection, and progress remain OPEN. Path A active; Path B closed.
