# A uniquely legal junction withdrawal opens a live parent gate and changes what other charts retain

In an admitted ten-vertex tree the unmodified v16.53 normalizer reaches a state with exactly one legal ordinary withdrawal anywhere in the atlas. Its original code takes that withdrawal. The parent then passes its exact-cover check and the existing child routine reads the surviving holders. In a matched example two other charts exchange the leaves of a binary junction. Holding the source bit in place makes the actual gate reject. Four shortest legal alternatives can restore the same cover while keeping that bit. In each alternative the child routine runs with different holders and distributes the leaves differently.

The entire positive trace is emitted in one ordinary call on the constructed input. The target and the ordered program are supplied at entry. The program plans the root moves before applying them. Uniqueness at the reached state gives a second, independent reason for the identity of the next withdrawal, conditional on ordinary pruning continuing there. The existence of that state, the choice to continue, the program's priority and an accessible physical record have separate status.

## A reproducible example

The root's four children, in the original positional ordering, are singleton leaves X and Y, a ternary junction W, and a binary junction S. Denote S's two leaves by left and right. In the example the chart order is D, B, C. Initially C holds X and Y. Each chart holds W and one distinct W leaf. D and B hold S, with its left leaf on D and right leaf on B. The measured entry profile is (2,3,2) at the root, W and S. It is passed into the historical normalizer. The three initial chart masks are (409,681,79), with the Pin at bit zero.

Immediately before the final root-level edit, the atlas is (159,681,457). D now covers all four root children, including S, where it holds neither descendant. B holds the right S leaf and C the left. This is a reached state, including the previous transfer to C. Neither the source nor the receiver is inserted into the positive execution.

Every terminal leaf has a single holder. At W every holder has a child and cannot drop W. At S, B and C each have a child and cannot drop S. Only D's incidence at S can be withdrawn: it is terminal in D's view and B and C preserve the union. This argument uses the current holdings and ancestry and does not need their numerical priority. An addition cannot increase a minimum cover. Thus among **all** legal one-incidence additions and withdrawals, D dropping S is the unique single move that restores the root target of two. Running the original v16.26 atom and independent verifier on that actual transition gives local cover 1→2 and a true trigger. The global maximum over parents stays three because W still requires all three charts.

The v16.53 root lift changes the atlas to (31,681,457). Its subsequent parent guard independently computes the root cover from the current holdings. With S now held by B and C, the binary call actually receives local masks (5,3), meaning right on B and left on C. Its target assigns left to B and right to C. These are the next four edits of the unmodified program.

| Local order after D's withdrawal | Actual actor and write |
| --- | --- |
| 1 | B acquires left |
| 2 | C releases left |
| 3 | C acquires right |
| 4 | B releases right |

With one unit of fine grade at every vertex, C's retained grade at S goes 2→3→2 during its own two changes. The numeric value 2 recurs. The location of its unit descendant grade changes from left to right. The program uses live chart memberships; the v16.26 certificate is a separately verified description of the step, not an argument to the child writer.

## A gate veto and four equally short alternatives

The instrumented veto restores only D's S bit at the final root recording instruction. The original frame continues, and its first exact-parent check in the second pass rejects cover one. No second-pass child has been entered. The uninstrumented positive and a separate passive trace of the same call agree exactly.

Demanding the same root cover through a different legal path is a stronger control. Keep D at S. For D to stop covering the root by itself, it must lose another root child. It cannot drop W while it still holds its W descendant. X and Y each have D as sole holder. In two moves the only possibilities are to give X or Y to B or C and have D release that same leaf. These four paths exhaust the shortest possibilities. The checker enumerates the complete primitive neighborhoods to depth two and validates the deletions and the reverses of the additions with the original atom and independent verifier.

Each of the four paths restores (2,3,2). D's final withdrawal gives the same root-local increment, the same true trigger and the same zero global increment as in the positive. The historical second pass runs without a new launch and with S still held by all three charts. For a fixed bystander, choosing the other bystander to receive X or Y holds the observed chart's entire prior fixed. Two such clean alternatives exist for either receiver. In the example C gives up its left leaf but never receives right in these alternatives during this call. In the positive it acquires right. For B, the corresponding clean alternatives leave B's S record unchanged while the positive gives B left.

The alternate root assignments differ from the original canonical endpoint. Their primitive steps and the entire resulting child computation are within the original unit band. For every control a separate later run of the original normalizer gives a valid continuation to the same canonical endpoint. The original independent verifier accepts each combined path. The cited bystander observations are all made before this extra call. Exact cover and even continued activity allow other legal behavior: immediately after the actual withdrawal, copying X to a bystander retains the exact profile and leaves every S-leaf incidence untouched. The child exchange therefore relies on the ongoing recursive writer.

## Which statements survive changes of chart priority

The extension enumerated 432 named/order presentations, 216 distinct indexed starts. An originally distinguished chart A holds both singletons. Each W leaf has a distinct owner. Each S leaf has a different single owner, and the remaining chart may initially hold S bare. There are 72 presentations at root cover two (36 distinct numeric starts). These include all six chart priorities. For all 72 the last root withdrawal is the unique legal pruning, and the veto blocks the parent gate. In 24 presentations the two surviving S owners exchange their leaves afterward. In the other 48 their roles are already aligned and there is no later bystander write in the positive. The exchange occurs exactly when the initially distinguished A is last in the chart priority. The 360 cover-one presentations are recorded as diagnostics: 48 have two later writers, 312 have none. They are outside the root 1→2 gate claim.

Why the 24/48 split follows from the code: the ternary child uses all three labels and is aligned during the first pass. On S, the two original holders are the charts other than A. The first binary call aligns left and right on those two in local order. The root expansion and contraction end with S on chart ranks 1 and 2, using zero-based chart ranks. Rank 0 is the final withdrawing holder. When A was at rank 0, S already had the target pair. When A was at rank 1, rank 0's role moves to rank 1 and preserves the left/right alignment. When A was at rank 2, rank 0's left role moves to rank 2 while rank 1 still holds right. The subsequent binary call then has an actual exchange to make.

At the return of the second pass, either original bystander can distinguish the direct withdrawal from its two clean shortest alternatives by its own addressed holdings. Denote a readout by (position held at W, positions held at S), using one-based **child** positions. No chart ordinal is supplied to this readout.

| Route | Possible record at a bystander that held an S descendant before the source |
| --- | --- |
| Original withdrawal at S | (2,{1}) or (3,{2}) |
| Shortest alternative keeping D at S | (2,{2}) or (3,{}) |

The two sets are disjoint across all six chart priorities. The ternary leaf records the bystander's place in the ordering that the original writer used earlier. This is a distinction on addressed leaves after the child has returned. The initial child order and software access are inherited or supplied. At the unaddressed level the two pre-source descendant holders can be exchanged along with their binary and corresponding ternary leaves. A unique named first receiver need not follow from anonymous incidence. If leaf positions are forgotten, the unordered **pair** of bystanders still distinguishes the routes: both keep an S descendant in the direct route, whereas only one keeps an S descendant in the alternative.

There are 288 clean comparisons in the cover-two presentations, counting two possible observers and two clean alternatives per observer. The late distinction persists under every further ordinary withdrawal. Every W and S terminal leaf is singly held at both returned states, so union preservation and the absence of additions protect its ownership. The native endpoint has no further legal withdrawal, and each alternative has one, at the now-bare junction holder. Removing it leaves the terminal leaf records unchanged. Later operations admitting additions can erase the distinction, as the common-endpoint completions demonstrate.

## Earlier fixture, rejecting controls and provenance

In a four-child frame the first pass visits disjoint child subtrees in order. A previous sibling's recursion only projects its updates into that sibling's region. Consequently it cannot remove an incidence at S before S's first holder read in that same frame. In the previous two-binary fixture, the first S call receives all three charts. The second S call has just one label bearing both descendants, since S has width one in that fixture and the root lift finishes with its canonical S holders. This explains why the earlier injected event is absent from that particular unmodified run.

The full historical campaign again passed its independent verifier on 2,863 records and 34,234 counted R/N moves. None of the 96 released N identities met the test of a final root-lift edit withdrawing a nonterminal junction followed by a second pass. The prospectively frozen one-binary family contained 1,296 three-chart and 12,288 four-chart starts. The 324 and 3,072 respective final junction removals had 9,864 bystander comparisons in total. Restoring the bare holder left every bystander's complete suffix unchanged, including 1,388 comparisons with an actual later local move. Mere temporal order was insufficient. The stronger result required a second structured child at W. The richer fixture was constructed after inspecting the canonical widths and is outside the released N population. The [initial scope](SCOPE.md), [width extension](https://github.com/proteinfoldingengine/WetLabEngine/pull/164#issuecomment-7181776930) and [matched control disclosure](https://github.com/proteinfoldingengine/WetLabEngine/pull/164#issuecomment-7181836394) record the sequence.

The source and both algorithms are software within the admitted project model. This run removes the externally inserted withdrawal and the post-event relaunch from the positive case. It leaves open what starts the dynamics, fixes ordered roles from informational structure and gives a physical receiver access to its retained record. It establishes no physical force or quantum-computation result.

Reproduce with `python3 -B check.py HISTORICAL_CHECKOUT --raw actual.json` using historical commit e61d5b0e827f7b412824ad46021e2ad6cc6f7875. The printed JSON and raw bytes correspond to result.json and the decompressed raw.json.xz. The ledger includes starting identities, source steps, guard and label readbacks, vetoes, alternative child paths and the later completion lengths.
