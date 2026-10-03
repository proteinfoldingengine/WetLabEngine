# Independent exact-source analytical review of A11.X3

Reviewer: independent Codex review agent `/root/a11_residual_review`.
Signed: 2026-10-03 (UTC).
Verdict: ACCEPT revised exact candidate `d2f79a71983a135eb035ef4d4c1289bdf6409814`: the new X3 sufficient class and the explicitly conditional general anchor-lift principle, within the disclosed inherited native width-floor dependencies. No blocking scientific gap found. The initial nonblocking wording issue is resolved in the independently fetched revision.

## Immutable source and change boundary

Repository: `proteinfoldingengine/WetLabEngine`.
Accepted revised candidate: `d2f79a71983a135eb035ef4d4c1289bdf6409814`.
Initial reviewed candidate and revision parent: `cf61a4f8832284eacc387990e5781b14b1ebdc9a`.
Scope parent: `d6728a23537dcb59ae875ce9d0a62377e2c8c3bf`.
Prior X2 publication: `436529e1a3f85abdf2800120e255773f66487e85`.
Integrated dependency baseline: `466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f`.

I independently fetched the GitHub bytes of `ResearchHistory/UQCF-GEM/research/overlapping-guard-exchange/A11_RESIDUAL_THREE_ANCHOR_LIFT.md` at the initial and revised candidates, and independently fetched `A11_RESIDUAL_THREE_SCOPE.md` at both candidates and scope parent. The scope blobs are identical (`8c722db41786070f68690e5e226e3236d54503d8`).

Accepted revised proof Git blob: `5f541b6502bcfb1ab7882fb98946cb3ee60ad8cf`.
Accepted revised proof SHA256: `45ba555e7b556870193f7fdda65a295a22de7c4bdc2d5d4dd8759f2f3b01d4be`.
Initial proof Git blob: `11cca16d073c6b4cf2e9e5c739b49a2504affbeb`.
Initial proof SHA256: `2724d6262a598c6fe142b7c82b11d003613c88963fc31ba2546106f7cd117eb2`.
Both SHA256 values were computed from independently fetched UTF-8 content and match the requested immutable hashes.

An independent GitHub comparison of scope parent to initial candidate shows one commit ahead, zero behind, with exactly one changed file: the proof added with 143 additions and zero deletions. An independent comparison of initial to revised candidate shows one commit ahead, zero behind, with only that proof modified (one addition and two deletions). Direct comparison of independently fetched contents confirms exactly the Section 7 paragraph-line clarification plus removal of one trailing blank line; all other proof bytes are unchanged. No earlier source or receipt is modified by these candidate diffs.

I also fetched the prior X2 proof at its stated publication and fetched the two inherited sources at the baseline. The inherited sources reside in `ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/`, rather than the new research subtree:

- `GENERAL_PARENT_CONNECTIVITY.md`, blob `922ae44713c6810c5a99716c52ecb37738a880a6`.
- `OVERLAPPING_CLIQUE_EXCHANGE.md`, blob `865f0797892a2e5e869ec2180d3c842026889445`.

This review checks their stated domains against the new uses. It does not independently recertify their proofs or replay historical certification.

## Scientific obligations checked

1. **All exact-q endpoints.** The hypothesis concerns original floors, not already-singleton endpoint supports. Choosing the same `m=q-3` labelled floor-one slots is valid at both endpoints. Exact feasibility implies `k,r>=q`; no compactness or separation assumption is imposed on other supports.

2. **Normalization and distinctness.** Individual contraction of selected floor-one roots preserves all floors and cannot decrease transversal. A duplicated singleton can be changed through `{p}->{p,t}->{t}` while another `{p}` stays fixed. The union step imposes no weaker requirement because p is already forced; the final deletion cannot reduce transversal. An unused t exists until all m selected labels are distinct. Distinctness strictly increases and the procedure terminates with transversal at least q.

3. **Canonical alignment through actual primitives.** The ordered injection of normalized anchor labels into canonical U extends to a whole-palette permutation. Inherited Lemma L applies to arbitrary overlapping supports, positive floors and an exact level t; t need not equal the original target q. Each completed transposition is exact t, and each internal state is at least `t-1>=q-1`. Thus the two endpoint constructions finish with the same canonical singleton labels at the same chosen slots. The whole tuple moves, so no unjustified assumption that nonanchor supports remain unchanged is used.

4. **Active-family additivity.** With fixed distinct singleton anchors, every transversal contains U. Exactly the nonanchor roots disjoint from U need extra residual labels. Hence the actual active family has residual transversal `g>=3`. Its members meet their original floors and lie in R. The active index set can differ between endpoints; the proof explicitly avoids treating those varying index sets as a common carrier.

5. **Fixed flexible/high-floor partition.** `F={i not in J:a_i<=n}` and `Z={i not in J:a_i>n}`, with `n=k-m`, depend only on original floors and canonical R. Every active root belongs to F. Every permitted Z root necessarily meets U because a support inside R has size at most n. No floor is weakened to fit R.

6. **Inactive flexible-root completion.** The original active roots remain fixed while each inactive flexible root is replaced by the whole R through expansion to its union with R and contraction to R. Floors hold because both endpoints are permitted. An original minimum residual transversal H, nonempty since g>=3, together with U hits every intermediate support: expansion retains the old U-intersecting support, while contraction retains R. The fixed active family and anchors give the matching lower bound. Previously completed R roots meet H and unconverted inactive roots meet U. Consequently every primitive in this stage has exact level `m+g`. Using the whole R, rather than a smaller arbitrary floor-sized residual support, is essential and correctly handled.

7. **High-floor preparation and common residual carrier.** Expanding Z roots to P preserves floors and leaves them redundant. The two endpoint preparations now have the same labelled F slots and the same original floors on the same R palette. For every permitted residual tuple, including every residual primitive, exact additivity is `tau(full)=m+tau_R`. The high roots are redundant because m>=1 and anchors force U; flexible roots contain only residual labels. The statement uses actual native slots, without merging slots or introducing virtual roots.

8. **Higher levels descend to exact three.** The prepared endpoints need not be exact residual three. Adding missing R incidences cannot increase residual transversal and decreases it by at most one per primitive, because an old positive-floor root can be hit by adding one old label to a new transversal. Filling all nonempty F supports to R gives transversal one. Integer descent therefore reaches three before dropping below it. The number of missing incidences strictly decreases; the finite process cannot stall above three. Floors hold throughout expansion, and the lift stays at least q.

9. **Inherited D is called in domain.** At its invocation both residual endpoints are exact three on the same finite palette R, with `n>=3`, the same positive original floor vector bounded by n, and the same labelled root set F with `|F|>=3`. Inherited D has arbitrary feasible arity and floors, so no floor-two or special-arity restriction is imported. Its `{2,3}` residual path lifts primitive by primitive to `{q-1,q}` through exact additivity.

10. **Restoration and final upper removal.** Reversing the complete C construction, including its residual descent and whole-tuple palette permutation, restores every original labelled support and palette label. Every reverse primitive inherits the original lower bound. The concatenation is finite, stays on the original width-floor carrier, has original exact-q endpoints and maintains `tau>=q-1`. Inherited A has precisely these hypotheses and supplies `{q-1,q}` after one final invocation. Its output need not retain the anchored form, and the proof does not assume it does.

11. **Conditional lifting principle.** For s>=2 and q>s, m=q-s is positive. The same normalization, fixed residual carrier, integer descent to exact s and additivity arguments remain valid. The premise explicitly demands exact-s connectivity for every finite palette and positive floor vector in the native one-incidence carrier. This is sufficient for the residual invocation; no universal theorem for s>=4 is silently assumed. X3 uses the inherited universal s=3 result.

## Scope and minor wording

The new count q-3 strictly strengthens X2's sufficient count q-2; X2 remains correct. The target-four corollary follows with m=1 and arbitrary positive remaining floors. Target-three connectivity is treated as inherited, already closed work. Sufficiency does not prove anchor-count minimality, arbitrary monotone destination-directed A11 schedules, the zero-anchor uniform-floor-three target-four case, or unrestricted root/nested universality. Temporary incidences, repeated toggles and the inherited child-interface conditions are explicitly retained.

Resolved initial wording issue: the initial Section 7 described every forbidden `(q-2)`-set as containing U, although sets omitting an anchor also fail. The revised exact source now states that any *candidate hitting set* of that size must contain U and explicitly excludes sets omitting an anchor. Thus the intended `U union {x}` coverage reduction is precise. The independently verified correction changes no scientific obligation or accepted conclusion. There are no outstanding review gaps for the revised candidate within this bounded scope.

No enumeration, numerical campaign, implementation, scientific tests, workflows or publication was performed by this review. GitHub reads, exact-source hashing and analytical inspection were the verification methods. No new efficiency, physical, primitive-time or originality claim is certified.

Signed: independent Codex review agent `/root/a11_residual_review`, 2026-10-03 UTC.
