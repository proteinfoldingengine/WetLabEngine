# Independent analytical review: total-deficit saturation

Reviewed: 2026-10-13 UTC. Review status: **CHANGES_REQUESTED** for the source-scope qualification below. The saturation theorem and both analytical controls are mathematically sound under their stated path assumptions. This is not native-event acceptance or scientific-stage certification.

## Exact reviewed objects

Repository/source branch supplied for this review: `proteinfoldingengine/WetLabEngine`, `research/uqcf-overlapping-guard-exchange`.

Source parent: `3b3b1e2d97c0381a05625fff8851cc813e8e2a24`.
Source tree: `879d72682033b776b9fe20ae67baa2ace2d435c2`.

| Object | Reviewed SHA256 |
| --- | --- |
| `RESULT.md` | `abadf8f6d094cfda2f658a242042336e9117a487564cdde08d56f4fcb70b5b50` |
| `INDEX_APPEND.md` | `1841e7409a16148464e81759959de4aa261e20b223773f78584ab8312ed56c1d` |
| `source_packet.json` | `b4b2573697dc1c7318dd8dfba3163556e9ed627bc6de9b5ee7e78dae19fdfdb4` |
| `SOURCE_READBACKS.json` | `d93ca4d2d5d2db21a1cfdacc3c20eb6e749a1beb8662a1f65596879ba37cc0a3` |
| `INDEX_PARENT.md` | `fe01d65a5ec2c272717a9fd1d899854c8ca767f2784fce0d0ae16736c7a141b2` |
| `INDEX_UPDATED.md` | `5f54bd3ff1496158c10f927e7bd023c16f753ee677b2adbd45f02b66e23a8619` |

I inspected the supplied primary-source packet, the parent index and the two proposed texts. For all nine packet sources and the parent index, recomputing Git blob SHA1 from the UTF-8 bytes, SHA256 and byte length matched the recorded bindings. `INDEX_PARENT.md` equals the packet's exact parent-index text; `INDEX_UPDATED.md` is byte-for-byte `INDEX_PARENT.md` followed by `INDEX_APPEND.md`. These are mechanical integrity checks of the supplied packet, not a fresh remote GitHub tree audit or historical scientific reproduction.

## Required correction

**Important — preserve the palette hypothesis of the inherited universal-safety classification.** `RESULT.md` section 2 allows a finite nonempty palette. Section 4 then invokes the earlier pointwise statement that universally carrier-safe contracting view maps must retain `H_T(Y)` without restricting the palette. The cited `COUPLED_C3_VIEW_LOCAL_PRUNING_RESULT.md` declares **at least two indices**; the parent index retains that restriction. Its necessity proof uses another view.

The unrestricted pointwise assertion is false for a singleton palette. Let `T` have root `o` and two leaf children `l,m`, and let the only view map satisfy `F(T)=T` but `F({o,l})={o}`. Complete it on the other prefix-closed inputs by any contracting root-preserving outputs. With one index, the sole cover of `T` is the input `T`, so this map is universally carrier-safe. Yet it does not retain `H_T({o,l})={o,l}`.

Qualify the source-classification sentence by `|P|>=2`. The general saturation theorem and the directly constructed leaf hull can still allow every nonempty palette: the hull formula is directly native and covering for any such palette. For a singleton palette the native state on the fixed carrier is unique, so the interval conclusion is trivial. The positive example has five labels and is unaffected. No change to its result, the theorem proof, or the index's stated saturation law is needed. Re-review the changed report hash before analytical acceptance.

No critical defect, additional important defect, or required minor correction was found in the reviewed mathematical argument.

## Mathematical assessment

The proof of the saturation law is complete. Native refinement makes each local hitting number nondecreasing; because `q=h(S0)`, every absolute deviation equals its nonnegative increase. An atomic deletion changes only the parent's child-support family. An old minimum hitting set either still works or can be repaired with one label remaining in the affected support, proving a total increment of zero or one. A deepest incidence outside `W` is removable: prefix closure follows from depth and the absence of a `W` descendant, and nonemptiness follows from the native covering state `W` that remains below it.

If `D_q(W)<=B`, all interval states meet the budget, so the atomic descent rules out every sink except `W`. If `D_q(W)>B`, a sink differs from `W`; if its total is below integer `B`, that descent and the unit increment produce an admitted outgoing edge, a contradiction. Thus its total is `B`. Strict finite incidence decrease supplies a combinatorial path to a sink. It supplies no actual progress law. The proof depends substantively on exact initial `q`, all admitted atomic deletions, integer budget and no additional blocking constraints.

The hull interval preserves every original global-leaf incidence, and the converse follows from prefix closure. Hull invariance on the interval is sound. The report correctly distinguishes this interval from enforcement of a physically available local operation or band check.

For the five-label source pair, both initial profiles are `(1,1,1,1)` and all internal supports agree. Source zero's hull removes only `d(u1)`, leaving total zero. Source one's hull removes `d(u1)` and the three internal `a` incidences, giving `(3,1,1,1)` and total two. In its unit-budget interval the first internal `a` deletion gives root hitting number two; a second gives three and is excluded. The irrelevant `d` deletion is always available while retained. Therefore the three sinks are exactly the states with `d` and one internal `a` removed, each with profile `(2,1,1,1)` and total one. This count follows from the displayed cases, without enumeration.

The early-stop control is correct: deleting only `d` from source one gives zero and the same internal support record as completed source zero. Positive total is sound for source one within the leaf-preserving comparison class, including partial histories, because source zero has no positive state there. It is not sound under unrestricted pruning. Source zero may remove `a` from all six leaves while each local hitting number stays one, reach source one's preparation, then remove `d` and one internal `a`, giving the same full positive endpoint inside the unit budget.

The two-arm control is also correct. The root's two fixed disjoint supports keep its hitting number two. In either arm the first common-label leaf deletion raises that arm's hitting number from one to two; its second deletion costs zero. The other arm's first deletion would exceed the budget. The two sinks have profiles `(2,2,1)` and `(2,1,2)` and common total one. This is deliberately a general-interval example, with changing global-leaf incidences, rather than a hull-interval example.

## Scientific advance and claim boundaries

Within the inspected sources, the substantive analytical addition is the **terminal-endpoint quantifier**: all unextendible paths have the same total deficit even when their final states differ. The earlier endpoint criterion fixes a proposed reachable endpoint, and v16.26 telescoping fixes the total after an endpoint has been selected. Neither supplied text states this variable-sink conclusion. The theorem is an elementary consequence of those inherited ingredients; those ingredients and the hull classification are not new discoveries here, and no archive-wide novelty claim is warranted.

The source pair applies the new quantifier to move a leaf preparation difference into differing internal hitting profiles after declared completed histories, with an actual nonidentity mathematical edit in both cases. It removes selection of a particular deletion order for that scalar consequence. It does not derive why a native event realizes this interval, enforces the budget, continues to a sink, or makes the profile accessible. Calling `D_q` a record does not supply those obligations, and the report does not do so.

The native-event milestone remains **OPEN / NOT ACHIEVED**. This assessment does not add a requirement for a unique microscopic outcome or a universal deterministic physical mechanism: the user's common or probabilistic accessible-consequence criterion remains eligible. Here the specific action and access premises remain supplied. The alternate mathematical consumer is clearly distinguished from the C3 restored-marker contract. Existing positive conditional constructions, stopped source-to-GR branches, Path A/Path B and the broad open obligations are preserved.

The review used proof-first reading and mechanical text/hash checks only. No scientific simulation, state-universe enumeration, source-module import, numerical fixture check, historical replay or test-count increase occurred. No numbered-stage closure, physical force, native receiver implementation, publication closeout, commit or external message is certified by this review.
