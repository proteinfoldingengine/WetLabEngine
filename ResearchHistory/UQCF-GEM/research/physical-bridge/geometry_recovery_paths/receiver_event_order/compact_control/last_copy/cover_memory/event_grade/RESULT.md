# Which retained chart remembers the size of an earlier geometric change?

In the five-chart example from [PR 162](https://github.com/proteinfoldingengine/WetLabEngine/pull/162), B withdrew from a site that it shared with F. Under the two positive grade assignments from the [private-swap control](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-7177091301), all ten current pairwise work entries agree once F has completed its edit. Yet B's earlier withdrawal changed the B–F work by either +1 or +9. F's current numerical P1 determines which magnitude occurred. A comparison of admissible numerical records for the original B view can use the historical overlap routine directly.

## What is inherited and what is supplied

**Inherited.** v16.26 emits and verifies an ordinary union-preserving withdrawal. v16.23 supplies ancestral P1, overlap compatibility and gluing. The historical forced-parent geometry code uses squared subtree totals on the symmetric difference of chart views. Its one-cut update formula already appears in degree_candidates. v15.40 computes the same work from the supplied source and response coordinates. These sources are pinned at e61d5b0e827f7b412824ad46021e2ad6cc6f7875 in the checker. The increment formula and additive P1 precede this note.

**Supplied.** A fixed rooted tree, compatible addressed chart views, a common time-independent fine grading for each comparison, the choice of historical work and the specified original event. In the five-chart replay the two grades are alternative preparations of the same named sites. In each original source arm the same preparation and F edit as PR 162 occur. We use successive atlas states as ordered edits. The comparison and reconstruction calls are made by the research harness. A mechanism that induces those calls within a chart, creates grades, or grants physical access remains open.

## Retrospective reconstruction on a rooted tree

Write t(v) for the sum of fine grades in the whole subtree rooted at v. For the inherited work, a site v contributes t(v)^2 to a pair exactly when one member of the pair retains v. Suppose chart B withdraws from one site v and all other memberships stay fixed. For another chart C, the after-minus-before change obeys

    ΔW(B,C) = +t(v)^2 if C held v at the event
    ΔW(B,C) = −t(v)^2 otherwise.

Pairs excluding B are unchanged. The sign follows because B's membership at v switches from present to absent. Duplicate chart rows or zero work between distinct charts are allowed in this work identity. For zero subtree total the work change vanishes even at an actual edit. For signed grades the magnitude alone loses the sign of t(v).

Any later chart retaining v can reconstruct t(v) by summing its addressed P1 entries at and below v. Each fine site below v retracts to v or to a deeper retained descendant, and no site outside that subtree can retract into it. For unrestricted positive grades, retention is also necessary for reconstruction from a single chart's P1 alone. When v is absent, its parent and v retract to the same coordinate. Move a sufficiently small positive amount from the parent to v. The whole chart P1 stays fixed while t(v) and its square increase. The same perturbation works for an entire collection of charts all missing v. Auxiliary information such as past geometric readings may supply a value independently.

Under ordinary fixed-union withdrawals some holder must continue to cover v. Thus at least one contemporaneous chart has sufficient numerical information for the magnitude even after other sites or holders change. Reconstructing all signs requires the original event's coholder incidences. No ordinary edit or automatic current observer is known here to evaluate the reconstruction.

## Fixed-incidence intervention on F

The site is 5, selected by B's actual earlier withdrawal. On the two source arms F finishes with private sites (2,5) or (4,5). Write j for the first one. Swap grades 1 and 3 between j and 5, retaining grade 1 elsewhere, including the Pin. Write u for the grade at 5. The state's total stays 10. In both arms B and F held site 5 at the original event and F was the only other holder. The complete subsequent withdrawal graph is the same for both grades.

| u | Written F row, ordered Pin, j, 5 | Old B row, ordered Pin, 5, 6 | Original B work changes against A, E, F, X |
|---|---|---|---|
| 1 | (6,3,1) | (8,1,1) | (−1,−1,+1,−1) |
| 3 | (6,1,3) | (6,3,1) | (−9,−9,+9,−9) |

In each of the nine later states in each arm all current chart P1 records outside F and the complete current work object coincide between preparations. Equality includes the minimum, neighbor set and metric flags. The post-write history graph and its joint receipts are grade-independent. B's original cover increment is 0 in the first arm and 1 in the second, separately from the grade choice. The original B–F work change varies by grade in both arms. Earlier geometry traces need not agree.

## A historical numerical operation with opposite verdicts

Use the addressed F P1 as the first numerical argument of v16.23 glue. Compare it against either candidate historical B row in the table on B's actual old footprint. The common sites are exactly the Pin and 5. Pushing either record to that overlap gives (10−u,u) for its own value of u. With the B proposal held fixed, changing F's numerical input flips the original routine between a successful positive glue and its 'incompatible overlap sources' error. In each of the two honest pairings compatibility holds. Each mismatched pairing is an explicitly counterfactual consistency test. No B incidence is restored.

The historical B row can also be reconstructed without providing a candidate numerical B row or a fine source to the reconstruction. Glue the current F record with any current chart that retains 6. Push the resulting joint source to the original B addresses (Pin,5,6). This yields (9−u,u,1). Using only current chart P1 inputs and known addresses, the minimal sufficient coalitions for arbitrary positive grades are F and one existing holder of 6. Full coverage keeps 6 on A or B. Necessity follows by transferring grade between each missing target and the Pin. This calculation gives an old mathematical marginal. The ordinary atom's argument list still contains no numerical P1.

## Cross-scale check

On a nonnegative grading, define M(v) as the magnitude of one incident pair-work jump when v is withdrawn. For any comparable set of actual one-site cuts on this fixed grade, square roots obey the local branch identity

    √M(v) = g(v) + Σ_child √M(child).

It follows directly from subtree additivity. A two-level experiment uses the same tree, grade 1 at the parent, grade 1 at the Pin, two initially identical charts, and the same verified sequence of three cuts (children, then parent). Child grades (2,2) give child work changes (4,4). The equal-total split (1,3) gives (1,9). Both have parent work change 25. This establishes one relation between scales. A specific split, self-similarity, fractal dimension, quantum dynamics and a physical gravitational field require further structure and evidence.

## Replay

Run python3 -B check.py /path/to/WetLabEngine --raw raw.json with the historical checkout at the commit above and the fixture and previous checker in their repository positions. result.json and raw.json.xz contain the summary and per-state comparisons. The test uses the actual atom and its verifier, a separately enumerated state graph, exact P1 and glue, and two implementations of the work. It also tests P1 sufficiency and the missing-site counterexample on all 33 increasing-parent arrays of sizes 2–5 (272 retained rows, 527 holder tests and 506 missing-site tests; the sufficiency test uses a signed grading). For an internal site with subtree total +10, −10 or 0 the measured work changes have the predicted sign symmetry and cancellation. Two local runs under different hash seeds reproduced identical raw and summary bytes.
