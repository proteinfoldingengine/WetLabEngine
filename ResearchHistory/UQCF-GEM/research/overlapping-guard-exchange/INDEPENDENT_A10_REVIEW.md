# Independent analytical review — A10 recovery trap and move completeness

Reviewer: independent mathematical review agent `/root/a10_recovery_review`, dispatched by `/root` under the requesting-code-review workflow. Date: 2026-10-03. The reviewer did not author or modify the candidate proof.

**Decision: ACCEPT both scoped analytical theorems T10-M and T10-W.** No Critical, Important, or Minor mathematical issue was found. No source revision is required for analytical acceptance. This decision concerns recovery completeness of the specified macro method and completeness of single-incidence local certificates, separately. It does not establish universal primitive connectivity or settle exact-endpoint-only connectivity of M.

## Frozen source and provenance

Repository: `proteinfoldingengine/WetLabEngine`. Frozen candidate: `45cf9131f79e19d4e1ae7450731bcd9fca497d7d`. Declared comparison parent: `69d0ec47822ba133ab4a6148c41f2a128b912fea`.

The reviewer fetched the full immutable remote `ResearchHistory/UQCF-GEM/research/overlapping-guard-exchange/A10_RECOVERY_TRAP_AND_MOVE_COMPLETENESS.md` and its Git blob. Both fetches return the same complete UTF-8 content. Encoding that content as UTF-8 gives exactly the supplied local proof bytes: 11,611 bytes, SHA-256 `d8632a8a282cc6d0a767e381e69ed3d616f85e2fbccbd673a0e9eb23efea9c70`. Recomputing the Git blob hash from those bytes gives `36a03b8bafb039af8ca33538fa62211dfc3785b0`, matching the remote file metadata. This verifies exact bytes, not merely rendered text or an abbreviated diff.

The reviewer fetched `A10_SCOPE.md` at both candidate and parent. It is unchanged: Git blob `97379ce729d27394881642cd18e7ba58d7aae9cc`; 2,692 UTF-8 bytes; SHA-256 `4e1ae9f7d865c70f8f72cd66b02f971f35c1c0395f72fd6d6f8c4f911d17102d`. Its historical parent `8074847d1702e060b547e110834ea5fd3e6659dc` and integrated baseline `466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f` are not asserted to be the candidate's immediate comparison parent.

The immutable comparison reports one commit ahead, zero behind, merge base equal to the declared parent, and only the 87-line A10 proof added. The fetched candidate commit identifies the same proof addition. No scope change or unrelated source change is present in this comparison.

The reviewer also fetched A9's frozen proof at `3c8443e34e8f185398946c1df00f82f4c888d1bd`: Git blob `896ff61a4ea2265a2b7521a84945b9227ad59a49`, matching the supplied local A9 bytes. The published independent A9 ACCEPT receipt was fetched at `8074847d1702e060b547e110834ea5fd3e6659dc`, Git blob `d2af73e2b67dc8e1a88137370bbb09b120d1e2e6`. A9's four-case hitting-set identity, saturation criterion, and critical-witness equivalence are the declared accepted dependency; their use in A10 was checked directly. No external design classification is assumed.

Review consisted of manual mathematical reasoning, read-only source/dependency retrieval, and byte/provenance checks. No scientific computation, configuration enumeration, tests, workflows, numerical campaign, implementation, source edits, or remote publication was performed. Only this local review receipt was written.

## Exact source, defective destination, and legal primitive reachability

At E, every three-set is the complement of a root and therefore fails to hit that root. Every four-set hits every size-four root on a seven-label palette. These statements exclude all smaller hitting sets as well and prove tau(E)=4. The seven displayed triples partition the pairs; hence every pair misses one of their complementary roots. A three-set such as {1,2,4}, unequal to any displayed triple, meets each complement, proving the seven-root guard has transversal exactly three.

D is specified at labelled slots: its seven designated original slots retain those guard roots, while the other 28 slots receive four further copies of each type in the stated order. This produces five copies of every type, 35 slots, and tau(D)=3. No unlabelled identification is substituted for the native tuple.

Each of the 28 support replacements adds up to U union V before deleting down to V. Every intermediate support contains its own starting or destination size-four support, so the floor holds. The seven unchanged guard roots force tau>=3 throughout. Any fixed four-set hits every intermediate support because all supports have size at least four, giving tau<=4 independently of upper normalization. Two size-four subsets of a seven-set differ in at most three labels in either direction, so six toggles per slot and 168 overall are valid bounds. This proves a finite primitive path E to D, and reversing it proves primitive recovery to E within the same unit band. No additional slot or label is used.

## M: exclusion of every completed method choice

For any label pair at D, inactivity means the complementary triple contains that pair. Pair uniqueness leaves exactly the five copies of one nonempty root in the actual inactive family. Its transversal is one. For q=4, A9 requires at least two for a common-saturation exchange. Thus no pair is eligible, including arbitrary adaptive pair choices.

Completed root transpositions preserve the multiset. Therefore every tuple reached by such transpositions again has inactive transversal one for every pair and transversal three. Inductively no eligible saturation exchange can first appear in that component.

Conversely every transposition is certified here: at most two slots change, leaving at least three copies of each displayed root intact. Those copies retain the entire guard and force tau>=3 along the two-slot union realization. Each expansion or contraction half contains its corresponding endpoint, whose transversal is three, and therefore has tau<=3. Uniform floor four makes every exchanged destination admissible. All transpositions are consequently available and connect precisely the labelled reorderings of the multiset.

The macro M-component is exactly those reorderings, all at level three, with no exact-four vertex. This excludes every completed M recovery route, including routes that might otherwise have used higher levels. It is stronger than failure of a schedule. The review preserves the scope's definition of M as certified macro exchanges and completed root transpositions; it does not insert arbitrary incidence moves or permit unrequested changes of method at internal points of a macro realization. Such a larger relation would be a different question.

T10-M therefore answers the declared recovery question negatively for a legally reachable and primitive-recoverable defect. It does not refute primitive connectivity or connectivity between all pairs of exact M endpoints. A path selected between exact endpoints may avoid D.

## W: both directions of single-incidence equivalence

For a lower source in an A6 fiber, A9's formula forces lambda_0>=q-1 and g>=q-3. In the safe case g>=q-2, each residual family contains F, so both residual transversal terms are also large enough; every admissible destination in that fiber is lower-safe. In the critical case g=q-3, A9's witness equivalence applies because lambda_0 is fixed and already large enough. Requiring both pure-role witnesses missed by every minimum inactive transversal is exactly the missing lower-bound condition. These facts establish that every certified, floor-valid candidate incidence edge is a legal lower edge.

For the reverse direction, an addition retains a companion v from the old support, and a deletion retains one from the new support. Positive floors ensure that support is nonempty. It lacks the toggled label u, so v is distinct from u. The changed slot remains active because it contains v; every other slot is unchanged. Backgrounds outside {u,v} and the active-slot union are therefore fixed, giving exactly the permitted A6 fiber, without altering the original palette, slots, or floors.

The same source identity gives g>=q-3. Integer transversal values leave only the safe case or the critical case. If critical, the supplied destination's lower level implies all minimum inactive transversals have both required witnesses by A9. Thus every original legal lower incidence edge receives a certificate. The argument also covers repeated backgrounds and unequal positive floors; auxiliary empty backgrounds use A9's stated conventions.

T10-W is exact equality of single-incidence edge sets. Choosing the least retained companion makes certification deterministic for a supplied move, but selects no improving move. Quantifying over all minimum inactive transversals is essential; one chosen witness cover would not suffice. No efficient search procedure, global path selection, progress measure, or connectivity theorem follows from this equivalence, and the candidate makes none of those claims.

## Acceptance limits

Both distinct scoped analytical obligations are fulfilled. The floor-four repeated-support diagnostic does not resolve the earlier q=4/floor-three diagnostic. Universal higher-target primitive connectivity, global progress, exact-endpoint-only M connectivity, and full nested lifting remain open or conditional as stated. The complementary covering discussion supplies necessary endpoint/lower constraints rather than a new sufficiency theorem.

This receipt approves only the exact frozen proof and declared scope above. Accepted earlier connectivity/interface results are dependencies, not recertified universal conclusions. This receipt does not itself fulfill the separate publication/status gate. No numerical, implementation, efficiency, novelty/originality, or physical-law certification is supplied.
