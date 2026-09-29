# Foundational closure verification — intake and evidence status

**Status: assignment handoff and preliminary source review only. The new bounded campaign has not been executed. No new closure verdict is certified here.**

The governing task is [WORKER_ASSIGNMENT.md](WORKER_ASSIGNMENT.md). This note does not weaken, replace, or pre-adjudicate that assignment. It preserves the original numbered F directories and records why their earlier GREEN runs cannot be treated as certification of the complete mathematical claims.

## Verified lineage and additive scope

The reviewed snapshot was `fb9e57e180fbc876598eafbd3f258a941ec469b8`, the 16.14F publication. A later foundational stage already exists: `research/v16.15F-graded-obstruction-descent` at `45963c9f6d297f99d26b920a1161e2baf3c15fd6`. GitHub's compare endpoint reports this as five commits ahead, zero behind, with the reviewed snapshot as merge base.

The assignment branch `research/foundational-closure-verification` starts from that later F head. The present changes add handoff documents only. They do not renumber stages, alter historical reports or executable source, merge to main, or touch protein-engine files. The worker must recheck branch state before execution and audit any later relevant work instead of duplicating it.

Historical F publication heads:

| Stage | Publication commit |
|---|---|
| 16.13F | `154a7c504327d1131f701d4108168c14f5c4cbd3` |
| 16.14F | `fb9e57e180fbc876598eafbd3f258a941ec469b8` |
| 16.15F | `45963c9f6d297f99d26b920a1161e2baf3c15fd6` |

The complete user-specified worker assignment was first committed at `bb1ffc7b3aefd3cb6806eedc65859bb17de047ce` on this additive branch.

## Evidence-status correction

### ES-13F — Assertion ledger, not an executed mathematical certificate

At the pinned F head, [16.13F gate.py](https://github.com/proteinfoldingengine/WetLabEngine/blob/45963c9f6d297f99d26b920a1161e2baf3c15fd6/ResearchHistory/UQCF-GEM/demos/v16.13F-foundational-closure/gate.py) constructs a literal ledger of `DERIVED`, `ILL_TYPED`, and `UNDERDETERMINED` classifications. It returns `all_valid=True` without computing the constructions, hypotheses, or counterexamples that would establish those classifications.

Consequently its successful execution establishes that the reporting program runs; it does not independently establish the principal closure or underdetermination claims. Those claims must be treated as prior assertions/reasoning requiring the assignment's provenance, proofs, and rejecting checks—not as already-certified conclusions.

### ES-14F — A scoped quotient observation is not a complete naturality obstruction

[16.14F gate.py](https://github.com/proteinfoldingengine/WetLabEngine/blob/45963c9f6d297f99d26b920a1161e2baf3c15fd6/ResearchHistory/UQCF-GEM/demos/v16.14F-obstruction-carrier-closure/gate.py) also returns the principal conclusions and `all_valid=True` as constants. [Its tests](https://github.com/proteinfoldingengine/WetLabEngine/blob/45963c9f6d297f99d26b920a1161e2baf3c15fd6/ResearchHistory/UQCF-GEM/demos/v16.14F-obstruction-carrier-closure/test_gate.py) check one dimension-difference example and declared Boolean flags.

These tests do not prove a nonexistence or naturality theorem. The observation that the inclusion of one filtration layer becomes zero in the next quotient only evaluates that particular construction. A claim about every natural nonzero intergrade map requires a declared category and a complete argument. A claim about the full retained inventory must additionally restore its actual inclusions and retractions.

Historical explanations of the quotient descent criterion remain pointers to reasoning; the worker must establish its hypotheses for the actual obstruction. Do not retroactively describe this old GREEN run as performing the stronger checks now required.

### ES-15F — Genuine bounded computation exists; campaign-level certification does not

[16.15F gate.py](https://github.com/proteinfoldingengine/WetLabEngine/blob/45963c9f6d297f99d26b920a1161e2baf3c15fd6/ResearchHistory/UQCF-GEM/demos/v16.15F-graded-obstruction-descent/gate.py) is materially different: it actually computes rational nullspaces and ranks of the fixed full-fine operator `T=Q_0 G_0` restricted to cumulative and previously lost kernels, using four inherited prefix-tree fixtures. This work must be audited and preserved rather than dismissed or duplicated.

However, the inspected code still leaves important gaps relative to the assignment:

- `all_valid` is only `total > 0`; it does not aggregate validation of all mathematical hypotheses or completeness checks.
- The selected chain uses reverse depth/address ordering. One such chain per fixture does not test every legal factorization or naturality under relabeling.
- The result records ranks and dimensions, not explicit raw kernel vectors and their nonzero response images as independently checkable counterexample certificates.
- [The two tests](https://github.com/proteinfoldingengine/WetLabEngine/blob/45963c9f6d297f99d26b920a1161e2baf3c15fd6/ResearchHistory/UQCF-GEM/demos/v16.15F-graded-obstruction-descent/test_gate.py) check one nullspace dimension, the version, and `all_valid`; they do not challenge a corrupted pushforward, invalid section, erroneous descent, or a linear-but-nonnatural construction.
- [The workflow](https://github.com/proteinfoldingengine/WetLabEngine/blob/45963c9f6d297f99d26b920a1161e2baf3c15fd6/.github/workflows/uqcf-v1615f-graded-obstruction.yml) runs the tests and gate but has no artifact-upload step. The Actions artifact query for historical GREEN run `36511346724` returned an empty artifact list at intake. This does not erase its logs or computation; the worker must reconstruct the complete evidence record and clearly identify any new reproduction.

The code's `OBSTRUCTION_RETAINS_PRIOR_GRADE_HISTORY` label is not, by itself, proof of a new dynamical memory mechanism. The worker must test whether the observed non-descent is already an algebraic consequence of applying the same full-fine Green operator to nested source kernels, and separate that from stage-to-stage response transport or physical history claims.

## Immediate mathematical review obligations — questions, not preset answers

1. Reconstruct the scalar structure of finite additive grades before invoking vector-space kernels, linearity, or real extension. Trace `G_f` and each indexed `Q_f` to the existing finite-lineage construction rather than silently adopting a new metric or inner product.
2. Do not discard retained set inclusions. Audit whether they supply a natural source section `I` with `P I=id`, and whether this splits the cumulative-kernel exact sequence. This must be proved in the actual retained category, not inferred from matching dimensions.
3. Keep source sections, potential restriction, full response codomains, fixed-codomain descent, stage pullback, and response-quotient descent distinct. The inherited [pruning consistency correction](https://github.com/proteinfoldingengine/WetLabEngine/blob/45963c9f6d297f99d26b920a1161e2baf3c15fd6/ResearchHistory/UQCF-GEM/demos/v15.56-response-selector-obstruction/PRUNING_CONSISTENCY_AUDIT.md) and its exact implementation are starting evidence to audit, not permission to import the old unearned `A_r`.
4. For the actual cumulative obstruction, exhibit either a descended map with representative independence or an admissible nonzero old-kernel witness. Separately examine the response quotient and state exactly which information it removes.
5. Require a proof for each universal statement and an independent verifier that rejects incorrect constructions. No scientific conclusion should depend on a test simply accepting the producer's verdict fields.

## Execution and review status

This intake performed repository/ref/source inspection and publication of the assignment. It did not execute a new mathematical campaign, add an adjudication implementation, run a new RED/GREEN cycle, or claim independent mathematical review. This preliminary review is **self-reviewed**.

No separate worker session or reviewer session was launched by this handoff. Publication of a GitHub assignment is not evidence that a worker has started. The worker must record its actual execution and reviewer provenance when the campaign runs.

Do not add structure to force closure. Do not remove earned structure to force a no-go.
