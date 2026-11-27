# A unique overlap selects a peer and changes its first leaf write

In four constructed preparations, the unmodified v16.51 normalizer computes which of two peer branches shares a label with the source. The first edit at each leaf of that peer adds precisely the shared label. At the end of child normalization both leaves and their parent retain only that label. We read these facts from the stored integer masks. The caller provides the tree, holdings, palette and nominal hitting profile. It supplies no peer index, anchor label or sequence of receiver edits.

## Matched preparations

Use the archived tree T, with a ternary root and two leaves under each of its three children. The shared root holds all seven labels. The table gives the preparation at the three branches. In these experiments the branch called the source is distinguished by the site at which the four preparations differ.

| Branch | Parent support | Initial support of each of its two leaves |
| --- | --- | --- |
| Source | {6, x} | {6} |
| Left peer | {0, 1, 4} | {4} |
| Right peer | {2, 3, 5} | {5} |

Choose x from 0, 1, 2, 3 for the matched comparison. No other site changes. The full tree, peer holdings and four measured hitting numbers (2, 1, 1, 1) agree. Any two arms also have a common exact predecessor with both candidate labels at the source parent. Releasing either candidate at that one site gives the corresponding exact input by one primitive bit change. These alternative cuts are interventions. The four primary calls start with the indicated single candidate present.

| x at source | Unique overlapping peer | First change at either of its leaves | Leaf support after all three child normalizations |
| ---: | --- | --- | --- |
| 0 | Left | {4} → {4, 0} | {0} |
| 1 | Left | {4} → {4, 1} | {1} |
| 2 | Right | {5} → {5, 2} | {2} |
| 3 | Right | {5} → {5, 3} | {3} |

## Why the original program makes the write

For root target two, the existing routine searches for a pair of children with a common label. In each primary input there is exactly one such pair and one shared label. Inside each member of that pair, the routine places the shared label first in its local palette when the branch width is smaller than the total palette. All three branch widths are one here. The inherited binary routine adds each missing parent label to each child in that order. Both peer leaves initially hold only their private label. The first addition must therefore be x. The binary routine then removes excess labels, keeping the first label at each leaf. The ternary routine trims the parent to the same width. These are actual one-bit changes in the normalizer's path. The computation reads the joint holdings once to establish the anchor. The leaf inherits its priority from that calculation.

The unselected peer also normalizes. At any fixed palette order its stored result is the first of its own three labels and is independent of which of the two values the source directs to the other peer. When private labels 4 and 5 each come first in their respective peer palettes, only the addressed private label row changes **between preparation and the end of child normalization**. It loses all three sites of its own branch. The other private label row is identical at those two observations. Both raw rows have identical priors across all four arms. This additional address readout depends on the stated palette condition. The selected leaf's first write and retained value hold for every palette order.

## Order tests, lifetime and source generation

- Four preparations crossed with all six orders of the top branches and all 5,040 orders of seven labels give 120,960 complete stock calls. The two leaves of each branch have identical priors and predicted first writes and outcomes. Both leaves were checked on every call. In 13,440 calls both private labels come first locally.
- We checked the complete primitive paths with the original verifier for 1,224 calls spanning all four preparations, all six branch orders and 51 palette orders. We verified every claimed first leaf edit, the stored branch supports at the phase boundary and endpoint agreement across the four source values for each order in the entire sweep. The prepared states and six common two-candidate priors are exact.
- In 60,480 calls the selected peer is processed before the source branch. Its leaf writes can therefore precede every edit to the source branch inside the call. The mechanism acts on the source's holdings at entry. It provides no general event-order claim about a prior source release.
- Later role transport takes all four runs to the same final holdings for each fixed order. The source distinction has a measured lifetime in the stored trajectory. The experiment observes that trajectory externally.
- Run the original program directly on the common prior with candidates 0 and 2. Processing order (source, left, right) selects left/0. Exchanging the two peer positions while transporting their holdings selects right/2. With candidates 0 and 1, reversing the palette changes the selected value from 0 to 1 at the same left peer. These calls test the ambiguity at its origin. The inherited program accepts a nominal profile and an invocation. The experiment does not derive initiation, a unique source release at the common prior, or access by a local participant to its own record.
- The historical 2,592-case compressed certificate regenerates to Git blob `571d38f08006b7023a65ec64cac77fe23e0db52a`. At 12 archived root-target-two starts there is exactly one initial pair and shared label. None of those pairs has a width-one endpoint initially holding multiple labels. The four-arm finding is a new experiment using original code. The count applies to archived starting states; it does not classify every intermediate frame.

## Reproduction

From a checkout containing the pinned demo and its sibling binary dependency, run the following with this script and output in the current directory.

```bash
set -euo pipefail
python -B overlap_write.py "$DEMOS/v16.51-ternary-interface" | diff - overlap_write.txt
```

[Original ternary writer](https://github.com/proteinfoldingengine/WetLabEngine/blob/7abbb1b85dc71110498c4a2998b8536c70770891/ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface/producer.py) · [Original binary writer](https://github.com/proteinfoldingengine/WetLabEngine/blob/7abbb1b85dc71110498c4a2998b8536c70770891/ResearchHistory/UQCF-GEM/demos/v16.50-recursive-binary-composition/producer.py) · [Exact check](overlap_write.py) · [Recorded output](overlap_write.txt) · [Case 50 control](ONE_VIEW_RELEASE.md)
