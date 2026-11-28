# Constructing a receiving guard from the initial incidences

In the earlier six-row example, reversing the eight palette labels exposed a remote write. The initial records identify a smaller object that suffices for the same kind of interaction. They determine two complementary pairs, a row containing one pair, and a single row meeting all four pairs in the partition. A proposed rule turns those facts into an M9 target. The historical M9 routine then determines the withdrawals, the leaf address and the writes.

## What the starting records determine

Let P = {0,2} and Q = {3,6}. These are disjoint pairs held in the initial leaves. Their union is the entire parent support of row 1. The pair S = {5,7} is disjoint from both and is both held in leaves and realized as a whole parent row. On the eight active labels the remaining pair is forced to be T = {1,4}. The search examines every unordered pair of leaf pairs and every candidate for S. There is exactly one qualifying pattern in each input, up to interchange of P and Q.

| Structural condition | Unique row in either input | Assigned support |
| --- | ---: | --- |
| Parent equals S | 5 | S |
| Parent contains all of T | 3 | T |
| Parent intersects P, Q, S and T | 4 | S ∪ T |

There is a separate check for the role of row 3. Starting from the original input, the unique nearest state beyond hitting number three is obtained by removing 3 and 5 from row 3, leaving T. With the extra 4 at row 0, reaching that same nearest state requires one additional edit, removing the extra 4. The checker exhausts every floor-respecting incidence matrix at each smaller or equal Hamming distance, including simultaneous additions and removals. This identifies a nearby boundary. Choosing to approach it is a separate assumption.

## The proposed trigger and target

The new rule applies within the six-row, eight-label, hitting-number-three class when a unique pattern exists and T is missing as a whole parent row. It completes the complementary guard with S, T and S ∪ T. The rule places the three destination rows into the slots for their assigned supports, using M9's existing sorted guard convention. The other three rows form the source group. In the final target the source group receives the three new guard supports and the three destination rows regain their input supports. For a deterministic representative the source rows retain input order and receive the sorted guards. No palette map is computed. The root ceiling is the initial hitting number. M9 retains its historical label order and its guard schedule. The script checks the generated trace with the stock verifier. A unique pattern alone does not guarantee an admissible trace.

The pattern recognizer and the decision to complete this guard are **new assumptions**. The parent route, clipping, nested clearance, leaf initialization and independent certificate verification are inherited. The verified inputs are new experiments outside the four frozen M9 cases. Prior work identified this fixture through exploratory search, and the completion rule was developed on it.

## The constructed interaction

Both source arms generate the same target from their own records. They differ initially only by the presence of label 4 at row 0, including in a check of the entire nested state. Row 4 starts with (0,2) at leaves (14,15). Both arms eventually restore its full parent support, {0,2,4,6,7}. The last 25 complete parent frames agree.

| Starting row 0 | Common withdrawal | Leaf that receives 0 | Final leaves at row 4 |
| --- | --- | ---: | --- |
| {0,2} | 1 at parent frame 35 | 15 | (4,0) |
| {0,2,4} | 1 at parent frame 32 | 14 | (0,4) |

Only these two leaves differ at termination. A reader who forgets leaf positions sees the same set {0,4}. Adding a different single incidence, label 7 at row 1 of the first input, keeps every initial leaf identical but removes the unique pattern. The proposed rule then emits no operation. After either positive run the trigger is also absent when evaluated on the actual terminal leaves. This demonstrates one event with an internal applicability test. Repeated self-generation of a network remains open.

## Tests of what the rule selects

**All possible palette pairings.** An involution exchanging all eight labels in pairs has 105 possibilities. We tested all 105, all six cyclic shifts, and both choices of which input supplies a target held fixed across the two arms. With the target formed from the original input, exactly eight pairings produce a terminal distinction away from row 0 on each shift. They are exactly those mapping the unordered pair of blocks {P,Q} to {S,T}. With the target formed from the modified input, exactly four pairings do so. They additionally map P to S. In every positive comparison the only remote difference is at the predicted row 4. This is a finite classification on the discovery fixture.

**Order checks.** Identifying the three roles commutes with all 720 permutations of input rows in each arm. With the inferred destination assignment, the row-4 result survives all six orderings of the source rows crossed with all six assignments of target guards to source slots. Reassigning the destination rows to any of the other five guard-slot orders removes the row-4 distinction in all 36 comparisons per order. Some orders can affect another row. Placement of the complementary guard matters. The supplied historical order of palette labels is retained throughout.

**Nearby inputs.** We added or removed each possible incidence at rows 1 through 5, identically in the two arms, yielding 40 matched controls. Four violate the floor. Twenty-seven lack a common uniquely identified pattern. Two have a pattern but fail the historical verifier's hitting-number and nested-deviation checks. Of the seven remaining comparisons, four leave a terminal distinction at the inferred receiver and three have the same terminal leaf tuple. This neighborhood is a deterministic sensitivity check on one fixture.

## Evidence and reproduction

The compact evidence file contains the two full positive records. The complete archive contains all 2,968 verifier-accepted executions in the order emitted by the script. Its uncompressed SHA-256 is `23a7ceb6791af2707a08c7543f8f5d3ba5e9072a03095046edd98de5ad78abee`. Two runs repeat across panels, giving 2,966 distinct input identities and full records. The checker prints the rejected inputs and the verifier's reasons separately. Compare the regenerated uncompressed SHA-256 to the recorded output.

```sh
python ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/guard_completion.py ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity
```

[Two complete examples](completion_examples.jsonl.gz) · [Complete accepted records](completion_records.jsonl.xz) · [Reproduction script](guard_completion.py) · [Verification output](completion_results.txt) · [Earlier fixed-target experiment](REMOTE_INCIDENCE.md)
