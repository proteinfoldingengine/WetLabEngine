# The original program can generate a unique overlap and revisit it in the same call

Two exact preparations of the v16.53 tree normalizer differ in one bit at a parent. All nine sites in its three descendant branches start identically across the two runs. In both, the original program generates a withdrawal of label 2 at the parent and first replaces 2 with 0 wherever its descendants still hold 2. In the default order this writes six sites in one run and three other sites in the other. Later in each call the ternary routine reads a unique overlap between two branches that initially shared no label. The complete paths pass the independent historical verifier.

These are new preparations on a supported arity-2/3/4 tree. The code, thresholds and transitions come from the historical implementation. The supplied inputs are the tree, start holdings, nominal profile, palette order and invocation. No caller passes a withdrawal instruction, destination, replacement label, intermediate path or second invocation to the top-level normalizer.

## Matched inputs and stored writes

The root has four children. One is a parent of three binary forks A, B and C. The remaining three are leaves holding 0, 1 and 2 respectively. The root holds all four labels. Both leaves of each fork start with the support given below.

| Quantity | Parent lacks label 1 | Parent holds label 1 |
| --- | --- | --- |
| Parent support | {2,3} | {1,2,3} |
| Fork roots A, B, C | {2}, {2,3}, {3} | {2}, {2,3}, {3} |
| Leaf support under A, B, C | {2}, {2}, {3} | {2}, {2}, {3} |
| Initial hitting profile | (3,2,1,1,1) | (3,2,1,1,1) |
| Fork roots after the first recursive visit | {2}, {3}, {2} | {1}, {2}, {1} |
| Sites receiving the generated 2 → 0 replacement | All six sites of A and C | All three sites of B |
| Available replacement labels at that moment | 0 or 1 | 0 or 3 |
| Fork roots at the second recursive visit | {0}, {1}, {0} | {1}, {0}, {1} |
| Edits in that second visit | 0 | 18 |

The parent routine first normalizes its children. Its cover reconfiguration then generates a step that will remove 2 from the parent. To preserve nesting it must clear 2 from every descendant that still holds it. The routine scans the current holdings, chooses the first available replacement label, adds it throughout the occupied sites, then deletes 2 at those sites before completing the parent withdrawal. Label 0 is absent from every proper descendant immediately before these two replacements. In each arm the occupied sites are singletons, so each must receive a label before releasing 2 if supports are to remain nonempty. The actual replacement takes the minimum two edits per occupied site. Replaying the other available label in the original clearance helper preserves every interior hitting number and the same set of sites releasing 2.

The stored trace shows the six-site clearance at frames 28–40 and the three-site clearance at frames 25–31, including the pre-edit frame. The outer cover routine, parent clearance, additions to descendants, parent withdrawal and recursive revisit occur in one invocation. The first visit's endpoint is verified from the stored whole-tree path. The second visit starts at frame 57 or frame 42. The complete final holdings agree. These are software frame indices, with no assumed physical clock.

## What the second visit reads

At entry, A and B share 2, and B and C share 3. A and C share nothing. In the default order, the second visit finds that only A and C share a label, respectively 0 or 1 in the two arms. Capturing the original call arguments, selected pair and local-to-global label map verifies this read without modifying the writer.

The second visit's three child-normalization phases all emit zero edits. Each fork is already monochrome, so putting its shared label first cannot alter its singleton palette. The 18 edits arise in subsequent role transport to the canonical assignment. This directly bounds the causal interpretation of the second read. The actual receiver writes driven by the retiring label occurred earlier, in the clearance.

## Why this generator chooses positions

For a compact ternary canonical assignment at hitting target two, let the three positive child widths sum to S. The producer fills consecutive blocks of those widths cyclically on M labels, where M is the larger of the largest child width and the ceiling of S/2. Each block fits once around the palette. Every label occurs once or twice, since the consecutive blocks together have length S between M and 2M. Hence the number of child-pair/shared-label incidences is exactly S − M.

Equivalently, this count is the smaller of S minus the largest width and the floor of S/2. The former is at least two because the other two widths are positive. Therefore the count equals one exactly for widths (1,1,1). In that case the child blocks are {p₀}, {p₁}, {p₀} in traversal order. A completed clearance which substitutes a previously unused label throughout the proper descendants preserves this incidence pattern. The theorem applies to compact canonical assignments and their complete injective relabelings. The earlier four-arm experiment used noncompact inputs.

Thus the generated pair at the revisit has a unique label, but the canonical generator placed it in the first and third positions. The script also checks the formula against the stock assignment for all 4,096 positive width triples up to 16 in each position.

## Controls

All 24 palette orders crossed with all six permutations of the named inner forks give 144 paired comparisons, or 288 complete verified paths. The outer branches keep their original order. The normalizer emits the specific 2 → 0 clearance in both arms of 18 comparisons. In six of those, the named recipient sets differ between the arms. The shared label read on the second visit differs in 36 of the 144 comparisons. The number of subsequent edits differs in 36. These are enumeration counts.

In all six inner orders at the default palette, the first and third positions receive the clearance in the arm lacking label 1. The middle position receives it in the arm holding label 1. Moving B to a different position changes which named fork is selected. The identity of the required recipients *at the instant of withdrawal* follows from their holdings. Their earlier placement and the choice of replacement still depend on the original ordering conventions.

## Reproduction

Use the pinned v16.53 sources below. The script checks the source Git blobs, intercepts calls for observation only, compares the primitive edits with the actual path, verifies every path against the independent verifier and records the order controls.

```bash
set -euo pipefail
python -B generated_overlap.py "$DEMOS/v16.53-four-child-boundary" | diff - generated_overlap.txt
```

[Original v16.53 implementation](https://github.com/proteinfoldingengine/WetLabEngine/tree/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary) · [Executable](generated_overlap.py) · [Output](generated_overlap.txt) · [Previous overlap writer](OVERLAP_WRITE.md)
