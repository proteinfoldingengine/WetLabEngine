# The shortest complete pruning run preserves the source address at the receiver

November 21, 2026 (Arizona). On the archived 25-view, 85-vertex tree, the original deletion grammar forces a source-specific change in the receiver on every shortest complete run. A complete run ends when no legal deletion remains. Length counts individual deletions after the source event. [Derivation and scope](P1_TERMINAL_OWNERSHIP.md) · [Frozen run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/44986431080)

The source and receiver initially share two marked leaves. The source drops one, making the receiver its only surviving holder. At this point the receiver still holds both leaves. During a shortest complete run, the receiver itself must delete the other leaf. Its remaining marked address then identifies which leaf the source dropped. The condition compares all legal runs to exhaustion without giving the procedure a target address.

| Final record at the receiver | Fewest further deletions | Most further deletions |
| --- | ---: | ---: |
| Only the address the source dropped | 1,299 | 1,332 |
| Both marked addresses | 1,300 | 1,333 |

The one-edit difference comes from the nonroot junction above the marked leaves. When each index keeps one leaf, both retain the junction. When the receiver keeps both leaves, the source must eventually delete its last copy of that junction. Every longest completion leaves the receiver holding both marked addresses, and the two source histories can then reach an identical full terminal state. Moving the same fork to the compulsory root removes the one-edit difference.

The general proof classifies every terminal family in a finite union tree. Assign each global leaf to any one of its original holders. Each indexed view then consists of the root and ancestral paths to its assigned leaves. This constructs every reachable terminal exactly once. It determines which receiver entries the source can make mandatory and when two source histories can share a full record. Even complete runs can share the receiver's entire history of local changes.

## Upstream selection and the remaining premise

The original v16.26 event code validates a requested index and leaf. Its producer enumerates deletions, and its factorizer takes an endpoint as input. Neither caller chooses shortest exhaustion. The v16.22 response-selection result classifies operators on supplied retained trees. Its inverse condition fixes an operator and supplies no next deletion. A separate v16.53 controller does make a state-driven receiver write on its four-leaf domain. On the second receiver edit it adds or removes a leaf according to the post-source cover number. That normalizer uses additions and its own profile rule. The prior nine-site minimum-incidence condition likewise comes with a frozen donor and protected junction. [v16.26 event and callers](../../../demos/v16.26-consistency-increment-law/engine.py) · [v16.22 response proof](../../../demos/v16.22-response-selection-closure/PROOFS.md) · [Four-leaf controller and fixed-site replay](ACTIVE_HOLDER_WRITE.md) · [Nine-site completion conditions](MINIMAL_COMPLETION.md)

**Native receiver delivery remains open.** The shortest-run condition is a property of the original deletion graph. Establishing that an inherited operation realizes that condition, or independently forces the same receiver write, requires an actual selection argument. Physical access to the retained address also requires evidence. Neither edit count nor graph distance supplies a physical time or gravity measurement.

## Verification

The Python checker traversed 754 starting families, verified 2,241 legal atoms across eight rooted shapes through four vertices, and tested 936 distinct within-case receiver-interval pairs. On the 85-vertex input it checked eight extremal witnesses against the old producer, including every possible outgoing deletion from each witness. Their reachability follows from the native P5 factorization theorem. The large-case path-length bounds are analytic, with explicit witnesses. The entire large graph was not enumerated.

GitHub ran the checker twice at commit `d684c0e0bf587cb2dc4e1366c8d7a16f9b2dbb09`. A separate local run on the frozen sources reproduced both output files byte for byte. Gemini 3.1 Pro Preview returned **ACCEPTED** on the conditional mathematics and **OPEN** on native delivery. Its written checks cover all four extremal lengths, the terminal counts, the nonroot junction and the missing selection principle. The archived raw response SHA-256 is `3f5666795672a8ed140b6b98582bba76f06a7d8dd6ac26c7234c9774692b866e`. The receipt and raw response match the published job log byte for byte. [Exact replay and full witnesses](p1_terminal_ownership_evidence/p1-terminal-ownership-replay.zip) · [Review](p1_terminal_ownership_evidence/review_verdict.json) · [Raw evidence and readback](p1_terminal_ownership_evidence/)
