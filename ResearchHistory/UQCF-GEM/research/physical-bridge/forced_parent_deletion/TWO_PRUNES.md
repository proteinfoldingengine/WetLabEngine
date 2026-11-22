# Two native grade transfers can reproduce the single recorded slope

The original V1687.16 comparison changed the site-2 to site-3 slope from −270 in B4 to −63 in B3. Two elementary P1 transfers applied to the original B4 inputs produce exactly the same change of +207 without changing the grouping, grades by hand, or gates. The entire response still differs. This supplies an explicit ambiguity for one proposed read and a second port that resolves it within this comparison.

## Exact example

In the B4 operation, keep J2 and J4 fixed. On J3, delete slot **3 into 4**, then slot **9 into 4**, with the inherited sum at the retained parent and literal zero extension at each deleted slot. Both moves can act on one rooted carrier with 3 and 9 as distinct leaves of 4. This shows admissibility for that supplied placement. The archive supplies no physical association between the cyclic slots and these tree addresses.

The right operand after the two transfers, multiplied by 21 for exact integer display, is
[
(-1323,840,21,-441,672,43659,-47376,3150,-378,210,84,0).
]
It has q[3]=−21, the exact B3 value there. The outer gate is 3, so the original fixed probe has slope −63 in both cases. At the second read, probe input **1** and read output **2**, again compensating at input 10 and subtracting each baseline. The slope is 3 q[2]. It is **3** after these two transfers and **0** in B3. This uses the same outer operation and existing slots in both arms. The scalar match therefore does not identify the grouping or transfer history. The second read distinguishes these specific alternatives and is not established as a universally identifying measurement.

## Complete test of two edits at the original input

The run tested each fixed grouping against the other originally computed right operand. Each first choice has 396 possibilities (three operands and 132 directed leaf-parent choices). A second edit may use 110 choices on that same operand, so both its slots still exist, or 264 choices across the other two operands. The original grade at the second edit includes any earlier incoming transfer. This tests 148,104 ordered histories for each grouping, 296,208 total. Placements in distinct operands are independently allowed. This includes a permissive domain larger than the class for any single specified tree. Zero-grade deletions and differing orders are counted as distinct histories.

| Fixed grouping | Target | Complete matches | Same site-3 slope | Fewest coordinates still different |
|---|---|---:|---:|---:|
| B3 | Original B4 | 0 | 28 | 9 |
| B4 | Original B3 | 0 | 6 | 8 |

At nonzero fixed outer gate the full left response matrix identifies each entry of its right operand by the corresponding off-diagonal cycle entry. Exact equality of the operand therefore tests the original full matrix without reconstructing that matrix for each trial. A scalar match means the same baseline-subtracted slope at the selected port, with no claim that the raw baselines agree.

The replay uses exact integer arrays with denominator 21 for both arms and applies the original rational function independently to 3,202 comparisons, including all 34 scalar hits. It checks sign, per-input total conservation, admissible deletion order, and the integer range. The complete per-arm ordered result is bound by its digest. The evidence retains all scalar witnesses and all closest histories. The earlier one-prune proof and this two-prune replay leave the fixed-operator full contrast unexplained under the tested literal input binding. Actual event selection, physical receiver access and gravitational interpretation remain open. [Protocol](TWO_PRUNE_PROTOCOL.md) · [Checker](check_two_prunes.py) · [Exact results](evidence/two_prunes/result.json).
