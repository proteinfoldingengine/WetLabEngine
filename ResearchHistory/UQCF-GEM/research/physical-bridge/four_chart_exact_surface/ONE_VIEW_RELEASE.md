# An archived receiver write certifies release of a specific source bit

In v16.51 case 50, label row 0 changes from 497 to 499 by gaining site 1. Before that edit, its holdings are compatible with label row 1 either holding or lacking site 8. Afterward, every admissible completion has row 1 clear at site 8. Row 1 initially held site 8, so the receiver's stored holdings and the known initial condition certify a specific prior release. The certification uses the historical allowance of one unit of total profile deviation. The post-write state itself uses that unit.

Here “receiver” and “source” name the two different label-indexed rows in the original representation. The rows consist of holdings at tree sites. The theorem concerns what the existing receiver row determines when interpreted with the model's rules. Participant-local access and a writer that takes a source event receipt as input remain open.

## Short proof

**Inherited inputs.** The archived preparation has two labels and tree T. The root has children 1, 4 and 7. Node 7 has children 8 and 9. Every site has a nonempty support, each child's support lies in its parent's support, a primitive changes one bit of one label row, and the root contains both labels. A node's hitting number is the minimum number of labels needed to cover all of its children. The nominal hitting numbers of nodes 0, 1, 4 and 7 are respectively 2, 1, 1 and 2. The original verifier requires the sum of their absolute deviations to be at most one at every frame.

**Deduction.** After the write, row 0 holds sites 1, 4 and 8. Nesting gives it site 7. Thus row 0 alone covers all three children of the root. The root's hitting number is one and uses the entire allowed deviation. Node 7 must therefore have its nominal hitting number two. Its children 8 and 9 have disjoint, nonempty supports. If row 1 also held site 8, that site would have both available labels and would overlap any nonempty support of site 9. So row 1 lacks site 8. Row 0 alone holds site 8, and row 1 alone holds site 9. The primitive that writes row 0 leaves row 1 fixed, so the release must already have happened. The inference needs no observation of row 1 after preparation, no frame number, no designated endpoint and no assumption of shortest paths.

## What changed in the original history

| Frame | Receiver, row 0 | Source, row 1 | Original primitive | Total deviation |
| --- | ---: | ---: | --- | ---: |
| 0 | 753 | 399 | Archived starting state | 0 |
| 1 | 1009 | 399 | Receiver gains 8 | 1 |
| 2 | 1009 | 143 | Source releases 8 | 1 |
| 3 | 1009 | 655 | Source gains 9 | 1 |
| 4 | 497 | 655 | Receiver releases 9 | 0 |
| 5 | 499 | 655 | Receiver gains 1 | 1 |

The exhaustive check considers all 19,683 assignments of nonempty label supports to the nine non-root sites, fixes the shared root, then applies the original nesting and profile checks. Exactly 210 states pass. All 210 are reachable from the archived start by admissible single-bit edits. The counts below describe possible completions, without any probability distribution over them.

| Stored receiver row | Compatible source rows | Rows still holding 8 |
| ---: | --- | ---: |
| 497 | 655, 671, 703, 735, 767, 911 | 1 |
| 499 | 655, 671, 703, 735, 767 | 0 |

Among tests of site membership with values as observed in row 499, three sites suffice and no one or two suffice. Sites 1, 4 and 8 give an all-positive test. The check also enumerates every three-site alternative. This minimum concerns these raw site tests on the specified tree and profile.

## Controls and implementation

1. **Delay the source release.** From exactly the archived prior, move the release of site 8 past the receiver gain at site 1. Retain the other edits in their relative order, the same endpoint, and the full subsequent history. All frames are structurally valid, and the receiver sees the same word after consecutive duplicates are removed. The deviation peaks at two precisely at the proposed write from (497, 911) to (499, 911). The original verifier rejects the path at that frame. Before it, (497, 911) is an admissible state with exactly the receiver holdings of archived frame 4.
2. **Call the original writer.** In the historical normalization, the full-palette third child is normalized through frame 4. The next phase transports a role in child 1. We captured the actual helper arguments at that call and replayed the unmodified helper with source mask 655, then with 911. Those two masks differ only at site 8. The helper emits the same receiver edit from 497 to 499 in each call. The archived phase order produces a legal path. The verifier enforces the global restriction, and this particular writer can emit the edit independently of the remote bit. The paired helper calls are interventions at the same phase boundary. Only the 655 call was made by the historical run.
3. **Test whether the record identifies a unique occurrence.** Insert one restoration and repeated release of source site 8 immediately after its original release. The stock path verifier accepts this complete control with the original prior and endpoint. The complete receiver word remains identical after removal of consecutive duplicates. The original and control now have respectively one and two source releases before the first receiver row 499. The receiver certifies a release has occurred, while its local word leaves the occurrence count ambiguous.

## Archive context

A single site edit changes child support for only one parent, so a nonzero deviation can change location only through a fully exact intermediate frame. In the 2,592 archived v16.51 paths we counted 1,412 three-frame windows with deviations at distinct locations on either side of one exact frame. In 245 of those windows the locations are in different top branches and different label rows perform the edits. Applying the later edit first produces total deviation two in each of the 245. These window counts concern restrictions on edit order. The address-specific inference above was proved separately for case 50.

## Reproduction

The historical sources used here are pinned below. The audit regenerates the entire compressed certificate to its exact archived Git blob, checks case 50 with the stock verifier, enumerates the admissible state graph, reruns both helper invocations and checks the full census. Run against a checkout containing the v16.51 demo and its sibling v16.50 binary dependency.

```bash
set -euo pipefail
python -B one_view_release.py "$DEMOS/v16.51-ternary-interface" | diff - one_view_release.txt
```

[Original producer and verifier](https://github.com/proteinfoldingengine/WetLabEngine/tree/7abbb1b85dc71110498c4a2998b8536c70770891/ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface) · [Runnable check](one_view_release.py) · [Recorded output](one_view_release.txt) · [Earlier exact-coverage leaf result](LEAF_WITNESS.md)
