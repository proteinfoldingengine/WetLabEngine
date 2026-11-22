# An archived controller remembers a source edit and writes to a receiver

In a seven-vertex binary fork, the v16.45 controller keeps a decision made from the root's initial cover number. Two source histories can reach exactly the same tree and identical receiver histories. The stored decision then determines which index receives two right-hand leaves. Both downstream sequences appear in the original scientific certificate. [Derivation and controls](FORK_PROFILE_WRITE.md) · [Verification run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/44989685419)

Starting from the same three indexed views, the source drops either a bare right junction or one left leaf. Both are legal v16.26 operations. Immediately afterward the right leaves still belong exclusively to the third index. The receiver's first four changes under normalization are identical. At its fifth change, the receiver's own state distinguishes the alternatives.

| Single source edit | Indices needed to cover the root's branches after the edit | Receiver's fifth edit | Right leaves it holds at completion |
| --- | ---: | --- | --- |
| Drops its bare right junction | 2 | Adds right leaf 5 | 5 and 6 |
| Drops its left leaf 2 | 1 | Removes its empty right junction | Neither |

Immediately before the controller processes the right-hand leaves, all three masks match at (31,17,113). The live root cover equals one on both paths. Restarting from this common state gives the same endpoint. The original execution retains its earlier choice of which index should own the right branch. That choice directs the different write without any clock or shortest-run requirement.

The two matched source experiments were composed for this check. The archived campaign had different starting rows, numbered 0 and 6. Those original trajectories pass through the same five full membership states at the same five successive positions, then assign leaf 5 to different indices. Starting at the last shared state, each new experiment matches its corresponding original sequence through the endpoint. The exact original row data and the new source atoms are available together. [Replay archive](fork_profile_write_evidence/fork-profile-write-replay.zip)

The identity of the receiver depends partly on the controller's ordered palette of indices. Under all six orderings, at least one index other than the source has a different final bit at leaf 5. The same structurally identified receiver B has the contrast under four orderings. Dot's two-index example still coalesces on its first move, as the matched control confirms. [Original producer](../../../demos/v16.45-binary-fork-unit-barrier/producer.py) · [Local star routine](../../../demos/v16.45-binary-fork-unit-barrier/star_normalize.py) · [Dot's control](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-7074531080)

The identifiable memory here is part of the controller. The matched experiment invokes that controller after a source event. A physical derivation must still establish what retains the distinction after the tree memberships coincide, what activates the write, and why the receiving index can physically access it. The 85-vertex deletion-only result remains a separate conditional result.

## Verification record

GitHub ran the exact checker twice at `181b7fea3c82dfbd8d79457d8862ca046c7daced`. The fork producer regenerated the complete 121-state and 6,241-state graph entries and compared them to the archive. The original independent verifier accepted both. A separate local replay at the frozen commit matched both CI output files byte for byte.

Gemini 3.1 Pro Preview returned **ACCEPTED** for the software result and **OPEN** for the native physical bridge. Its response reconstructed both source masks, the five shared historical states, the divergent next edits and B's different fifth edits. The raw response SHA-256 is `ace9ca018515d52d5a1ee964e86b9066f6c74dcd193f77cf11847388373e60b0`. The raw response and publication receipt match the archived job log. [Review verdict](fork_profile_write_evidence/review_verdict.json) · [Evidence and readback](fork_profile_write_evidence/)
