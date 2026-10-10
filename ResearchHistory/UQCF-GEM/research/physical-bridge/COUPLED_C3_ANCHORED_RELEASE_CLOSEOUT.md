# Anchored donor release and exact-permutation restoration — scoped closeout

Status: **CLOSED for the declared two-stage monotone-release theorem and its exact verification contract.** Broad C3/general C4, native observer/core access, source admission, outcome selection, and guaranteed progress remain OPEN. This is not numbered-v16 or full-stack certification.

## Mathematical result

For a finite original core `C`, active palette `P`, fixed positive original floors, and `3 <= tau(C) <= 4`, fix an occupied reserve label `r`. A two-stage path that first adds only non-`r` donor incidences and then deletes every original `r` incidence exists uniformly over every original protected hidden completion exactly when each donor `d != r` can be assigned to an inclusion-maximal original footprint `phi(d)` such that:

1. its original footprint is contained in `phi(d)`;
2. the assigned donor incidences satisfy every original floor; and
3. at most four assigned donor footprints cover all roots.

The construction is explicit. Add donor incidences within their assigned original footprints, then delete `r`. Original floors, original-footprint domination, and an actual upper-four cover hold at every slice. This criterion is exact only for the declared monotone class; its failure is not a general connectivity obstruction.

Once `r` is absent, whole-footprint renames implement any exact palette permutation, including one moving `r`. Concatenating the release path, the rename path, and the reverse of the permuted release path reaches exactly the labelled endpoint `pi(C)`, fixes every hidden incidence, and removes all preparatory donor incidences in their prescribed images. Relabelling the same certificate renews the interface for any finite prescribed permutation sequence.

The saturated multi-donor example `({r,a},{r,b},{a,c},{b,d},{e})` shows the new mechanism: two donors protect distinct maximal regions, so a common donor backbone is unnecessary.

## Verification and independent review

The analytical result and prospective scope were frozen at `ff482f62399bdf71774baf8923008e561035a47e`. The implementation ran at `06f8e31cf286cf9da204feef038ac0153bb10bd9`; its original artifacts, full logs, internal review and publication audit were preserved before the exact-commit external campaign.

[Actions run 38062751004](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/38062751004) evaluated immutable event commit `47ebf4a717f4a9eadc7d51567b27e42bfb1e1d73`:

- 155 tests passed: 20 new and 135 inherited.
- Independent reconstruction covered 2,448 sources and all 19,584 typed source/floor/reserve identities, with 5,424 positive releases, 10,752 release toggles, and 143,520 original-hidden-slice checks.
- Three fixtures exercised all 72 declared subset permutations, 24,020 hidden-slice checks, and three renewal sequences.
- Exact event-commit provenance passed; the certificate was independently reconstructed byte-for-byte.
- Gemini 3.1 Pro adversarial mathematical review: **ACCEPTED**, zero missing assumptions and zero counterexamples.
- Separate Gemini 3.1 Pro publication audit: **ACCEPTED**, zero missing assumptions and zero counterexamples.
- The publication gate verified 27 review inputs, response hashes, exact provenance, byte-identical reproduction, and complete independent reconstruction.

All three original external-review ZIPs, complete logs, raw responses, manifests, the publication gate, archive digests, and the prior genuine local RED are preserved under `evidence/anchored-release/external-review/`. The local RED consisted of three missing-field `KeyError`s among 20 executed control-test bodies before implementation; it was not a mathematical counterexample. The final controls pass.

## Boundaries and next obligation

The theorem assumes the original protected fiber, complete active palette, supplied core/root addresses, source protection, a finite script state, actual committed edits, and progress. Optional NOOPs can still stall. An admissible relation is not promoted into an implementation or successor-selection oracle.

Next determine whether a safe nonmonotone donor handover can create the first absent label when **every** reserve fails the anchored monotone criterion. Failure for one reserve is insufficient if another reserve is releasable. A positive construction or invariant must preserve original floors, footprint domination, and the upper-four cover at every slice.
