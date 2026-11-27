# One archived balancing relocation generates a second and writes six previously untouched rows

**Scope.** Actual v16.54 M5 campaign record, replayed by the original program and independent verifier. The inherited scheduler generates a forward continuation inside one call. The initial directed cycle and sizes, access to shared holdings, and the call to balance remain supplied. The report does not derive physical access, a persistent occurrence record, or a native origin for the balancing rule.

## Archive and producing rule

The original campaign run 37059520424, science 0ba1284ade581267997882de2d4c723f2b9ee3a4, shard 6 artifact 11251270737, contains the exact unmodified row at shard ordinal 268575 / global ordinal 2063662 (zero-based). ZIP SHA-256 `7aeba6bc0f45b721b73cebf48129b60e17651bc63b8772e49e24ddd5668257ea`; compressed records member SHA-256 `ef3f762064c2d02389ce448e777de8ed544018e0e39173f6c51a5b32f15bf468` matches the scientific manifest. The 53,980-byte original record including newline has SHA-256 `13a954e573fbd21fac158163827069d766cf3a014a78a2b20c99debb324587fd`. The independent replay loads the actual identity and verifies entire record equality, not just the two moves.

The identity is M5 balance, cyclic form, widths (1,4,3), h=3, k=8, q=5, d=0, extras P, floor three at each of 26 rows, and empty choice. Let A={0}, B={1,2,3,4}, C={5,6,7}. The inherited code initializes the groups from the supplied sizes, keeps a mutable copy, and on each pass selects a directed successor whose width is at least two lower. In the original archive:

| Input widths | Eligible directed move | Actual materialized relocation | Frames |
| --- | --- | --- | --- |
| (1,4,3) | C→A only | move label 5 | 0→36 |
| (2,4,2) | B→C only | move label 1 | 36→70 |
| (2,3,3) | none; loop terminates | canonicalization follows | 70→228 |

The fallback is not reached in either active step. B originally exceeds C by one, below the threshold; once the first relocation completes and removes one member from C, B exceeds C by two. The loop recomputes the test from the mutated groups and actually calls the newly selected next relocation. There is no supplied second operation, second receiver index, desired row holding or rewrite of a preliminary path. The stored frames are the original producer's own path. All 70 relocation primitives preserve floor three and have cover four or five; at each of the three boundaries it equals five.

## An order-insensitive population must change

Fix the generated first moved label x in C and the second moved label y in B. Before the first operation, each triple {y,z,t} with z in B excluding y and t in C excluding x belongs to the cyclic core (two labels in B and one in its successor C). There are 3×2=6 such triples. They avoid x, so the first relocation never edits those storage rows. They all contain y. After the second relocation they would have two labels in C and one in B, which is not C's successor. Therefore the old holdings are no longer valid core triples. The inherited replacement of all y-containing old-core slots replaces them with a new star triple or the full palette; either way every one of those six old storage rows changes during the second relocation. This argument is invariant to row or label enumeration in the sense of guaranteeing a set of six after the generated labels x,y are used; it does not promise the same labels, the same individual rows, or identical replacement supports under arbitrary renaming. The code itself uses numeric order to select the moved label and pairs sorted slot indices with sorted new core triples.

In the archived numbering the six rows are exactly [6,7,10,11,13,14]. For example, row 11 initially holds {1,3,7} and keeps it through all of the first operation. In the second, it becomes {1,3,6,7}, then {1,6,7}. This particular row is unchanged before the generated second operation, not a row carrying the first label 5. At full return the old storage coordinate has {0,6,7}; stock canonicalization has renamed and reordered supports. Its changed terminal value is not by itself an occurrence record.

## Controls and limits

- If the original helper is called out of order with B→C at the initial state, bypassing only the scheduler, it still has floor three and covers four or five with final cover five. Thus availability in this sense is a property of the actual scheduler, not a primitive impossibility or prohibition of the early edits. This override is a separate control, not archived behavior.
- Starting a separate stock call from the exact completed-after-first rows, with the groups encoded contiguously to meet the input convention, omits the first relocation in that call. Once labels are translated back for that second relocation, it reproduces row 11's same local word [137,1367,167] (strings denote sets of symbols), though the full raw suffix is not identical. Both returned canonical full states are exactly equal. Therefore that partial local word and final canonical tuple are not exclusive signatures of the first operation's occurrence.
- All three core boundaries uniquely determine the directed partition of eight labels up to rotation among 1,932 nonempty partitions (excluding full-palette padding before matching). This is an independent reconstruction property; the real scheduler uses its mutable group metadata rather than reconstructing a partition from a receiver's row. It grants neither local access nor native genesis of the cycle.

`python -B replay_balance.py /path/to/v16.54-parent-support-connectivity` verifies the exact row hash, stock pins, both stock replay/checker, ground-rule proof obligations, the codes of the two controls and rejecting tampered-record control. Compare with expected.json. This is a bounded historical replay and proof, not a new numbered campaign or a claim that balancing naturally initiates.
