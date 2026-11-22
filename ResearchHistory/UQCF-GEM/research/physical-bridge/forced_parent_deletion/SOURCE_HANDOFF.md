# Root-grade transfer on an archived repair path

The original v16.48 repair corpus contains three calls in which D deletes root leaf 9 and C acquires it on the very next edit. On these three paths, a third chart B retains the leaf throughout the handoff. Under fixed unedited chart grades (W1) and compatibility after each edit (W2), the root-grade changes on this two-edit interval are

    ΔD(0) = +g9,     ΔC(0) = −g9,     C_after(9) = g9.

Here g9 is the leaf's original grade in the coherent input family of P1 marginals. The same historic program chose both edits on the same call. The grades and the interpretation of C's own read remain assumptions for physical use.

## Prospective search and exploratory extension

The prospective search at ff52030339088898b1a5f31320e391168da48753 fixed the last preorder leaf and identified a receiver by the untouched-twin rule of the earlier nine-site example. The pinned archive is v16.48 CERTIFICATE.json.gz, Git blob ff8244239fb5ce092b07cbe775382593018b256d. We replayed its entire directed corpus, ran the original independent directed verifier, and compared every case, start, path and endpoint with the archived bytes. The separate graph-representative domain is outside this census.

| Prospective quantity | Count |
|---|---:|
| Default directed calls | 210 |
| Elementary edits | 5,698 |
| Deletions at the designated leaf | 197 |
| Deletions with exactly one untouched twin | 0 |
| Adjacent copy-then-release windows at that leaf with a unique initial and final holder | 157 in 86 calls |

The registered receiver criterion produced zero hits. The 157 controls have acquisition first. They confirm that the trace representation can expose genuine changes of holder. They do not satisfy the post-deletion primary criterion.

A concurrent exploratory search relaxed two restrictions. It considered all outer root leaves and allowed the executed next edit to identify a distinct recipient. Exactly three windows qualified. They are cases 178, 184 and 190, zero-based, all with degree sequence (3,2,3,2), reversal and four charts. They share the same program branch. These are three executions of one pattern, not independent physical replications. The last preorder leaf on these calls is 10. The three windows are at leaf 9. Preserve this distinction when comparing counts.

## Reconstruct the transfer on case 178

| Archived state | A | B | C | D |
|---|---:|---:|---:|---:|
| Before D releases leaf 9 | 1025 | 559 | 223 | 771 |
| After D releases it | 1025 | 559 | 223 | 259 |
| After C acquires it | 1025 | 559 | 735 | 259 |

The numbers encode retained vertices as bits. C has bit 9 only in the last row. All three of B, C and D retain the other, inner root child 1 in these states. They all exclude outer root leaf 10. B has bit 9 in all three rows. Vertex 9 has no children.

1. The initial grade family is the P1 pushforward of g on the full tree. D initially contains 1 and 9 and excludes 10, so its root grade is h=g0+g10 and its leaf grade is a=g9. D remains unedited up through B's gain of leaf 9. W1 therefore fixes these two values in D at that gain. The original repair introduces B's copy before D's loss.
2. At B's gain, B and D both contain 1 and 9 and exclude 10. P1 projection to their intersection preserves those root and leaf values. W2 makes the two projections equal. Hence B's root and leaf are (h,a). W1 now anchors both on B through D's loss and C's gain. No claim about the whole ambient vector along every edit is required.
3. Whenever a chart O among C,D holds 1 and excludes both 9 and 10, restricting B and O to their intersection gives O(0)=h+a. When O holds 1 and 9 and excludes 10, agreement gives O(0)=h and O(9)=a. Applying these alternatives to the three archived states proves the displayed changes. In particular these are changes in existing root coordinates of two different charts, in a single repair history. No paired high/low endpoint subtraction or minimum-incidence selector enters the equation.
4. For an exact control, start with all grades 2 and compare with an input moving 1/2 unit from root 0 to leaf 9. C's root just before acquisition is 6 in both. Immediately after acquisition its root is 4 versus 7/2 and its leaf is 2 versus 5/2. Coarsening back onto the pre-gain carrier removes that source distinction under the P1 comparison. For arbitrary compatible histories the proof fixes these specific coordinates. Other coordinates need not have been protected. A zero leaf gives zero root increments. Signed leaf amounts reverse the signs.

## What selects the outcome

The separate native v16.26 factor operation accepts the same before/after donor states as endpoints and emits the identical donor deletion as its final edit, with C untouched. Thus the deletion certificate alone permits a history in which C never acquires leaf 9. In the v16.48 history, star_normalize.py lines 17–20 finish compacting chart labels, then lines 33–37 and 22–24 use the temporary label C in a recoloring. The support routine can inspect leaf occupancy to complete that repair. Its inputs omit chart grades.

The directed producer constructs starts from a target and a permutation, then invokes normalize. Its outer-star routine compacts a palette and recolors leaves. On the three paths C is a temporary color chosen by that existing call, and C later releases leaf 9 in all three. The event ordering and chart writes are historical software facts. The running controller already chose a repair task. These traces do not establish that D's deletion itself dispatches a new process or selects C independently of that controller. The source amount is a grade on this support trace through the stated mathematical associations. The historical support-only program receives no physical source amplitude.

The relevant nulls differ. At g9=0 the root-grade transfer vanishes even along the same support path. Across fixed-source edits a shared glued potential has no change under the full fixed-ambient P1 interpretation. The weak W1/W2 argument concerns only the protected coordinates. It does not imply a new gravitational field, persistence at the endpoint, a calibrated response, or that C can physically use the number. A decisive source would have to identify the label/phase with a physical receiver, show a native operation consuming that receiver's acquired distinction, and connect it to a gravity observable.

## Verification

The registered census is check_source_handoff.py, with full case identities and all qualifying windows in evidence/source_handoff/census.json. The exploratory search and its trace controls are supplied separately. The checker correction described in MINIMAL_COMPLETION_EXACT_READOUT.md is a component-level replay. The earlier raw review and its original integer corpus are preserved. This follow-up is a bounded historical-source audit with a conditional mathematical implication.
