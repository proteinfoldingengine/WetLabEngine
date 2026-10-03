# Independent analytical review — A11.X6

**Reviewer:** independent Codex review agent `/root/a11_x6_review`  
**Disposition:** **ACCEPT — no mathematical corrections requested**  
**Review type:** analytical source review, not numerical execution or implementation certification.

## Immutable reviewed sources

Repository: `proteinfoldingengine/WetLabEngine`  
Subtree: `ResearchHistory/UQCF-GEM/research/overlapping-guard-exchange/`

| Source | Commit | UTF-8 bytes | SHA-256 | Git blob SHA |
| --- | --- | ---: | --- | --- |
| A11_X6_SCOPE.md | ed2da70fc8c59748e8598362dc88d2bace8cf6b1 | 2468 | 0c97677eff3be2fb956704a6b3e944075e8ae4f479724adba476c74c53798d59 | 85eca0f2f954519e4179270bbda271ccaf03d0fa |
| A11_X6_GUARD_ACCESSIBILITY.md | 442fb7b839425a96b2ae248616b944f56f1229a0 | 12089 | 635043f42e58feb336cb10732c6162bb72d2f332fb142547abe7480e66a756ae | 7678a7fd79ae756910664f8fed0a3c5fade49128 |

I fetched both immutable sources independently through GitHub; this review does not rely on the author's transcription. Local hashing of the fetched UTF-8 contents reproduced the supplied Git blob identities. No scientific enumeration or numerical experiment was performed.

GitHub comparison from accepted X5 publication `02b15a4787cc592e354b539095acf1ed1d6b295f` to candidate `442fb7b839425a96b2ae248616b944f56f1229a0` reports two added commits, no divergence, and exactly two added files: the scope and candidate proof. No inherited scientific source, workflow, implementation, certificate or integration file changed.

## Accepted mathematical statement

On a fixed seven-label palette with labelled slots, all original floors three, and all supports of size at least three permitted, X5's qualified exact-four class `G_s` is nonempty **if and only if `r >= 13`**, for every selected slot `s`.

Exact-four states exist with twelve slots. Nevertheless, **no exact-four state on that carrier qualifies for X5 at any slot**, including states with noncompact supports. Consequently Route A cannot supply an X5-qualified exact-four target there.

This is a target-class existence obstruction. It proves neither native exact-endpoint disconnection nor a higher nested barrier.

The six-label precheck is also accepted: exact-four feasibility requires all twenty complementary triple supports, hence at least twenty slots; X5's class is empty there for every slot regardless of slot count.

## Detailed checks

1. **X5 hypothesis fidelity and same-slot condition.**  
   The definition of `G_s` matches the frozen X5 proof: original floor-three slot; a triple contained in its actual support; a supplied four-label hitting set intersecting that triple; and the actual other roots avoiding the triple with residual transversal at least two. The counting reduction retains the selected slot and supplied cover. The sharp construction assigns its anchor to any specified slot. No accessibility or arbitrary slot-alignment theorem is assumed.

2. **All-support-size reduction.**  
   Exact compaction preserves a label of the supplied four-cover in every root. Every individual deletion respects floor three, cannot decrease transversal, and retains the upper bound four. Original avoiding roots remain avoiding; their transversal cannot decrease under deletions. Newly avoiding roots cannot lower the family's transversal. Thus a qualifying noncompact state produces a qualifying compact state. The lower bound genuinely applies to all native support sizes, without restricting the reconfiguration graph.

3. **Actual guard roots.**  
   For a four-label residual palette, compact avoiding roots are its four possible triples. Residual transversal at least two requires empty intersection, forcing all four distinct residual triples on distinct nonanchor slots. Together with the anchor this consumes five existing slots.

4. **Shared-capacity counting.**  
   The eighteen triples with one anchor and two residual labels require actual avoidance witnesses. Neither the anchor nor a residual triple witnesses them. A two-anchor support serves one anchor-indexed system; a one-anchor support serves at most two obligations across all three systems. The proof explicitly counts those shared slots once.  
   With `m_t` two-anchor slots and `p` one-anchor slots, the established bound
   `2p >= Σ f(m_t)`, where `f = 6,3,1,0`, gives `m+p >= 8` through `f(u) >= 5−2u`. Duplicates and additional support types cannot improve this bound. Hence thirteen slots are necessary.

5. **Sharp construction and exact-four entry.**  
   The thirteen specified triples meet the supplied cover `{a,b,x,y}`. The proof exhausts every triple type and supplies an actual disjoint root for each. Smaller hitting sets extend to triples, so this establishes the lower bound four as well as the supplied upper bound. The four residual triples supply the actual X5 guard. Additional existing slots filled with the whole palette do not change exactness or guard availability.

6. **Guard-creation illustration.**  
   Adding `c` to `R minus x` can destroy only the listed old triple-avoidance witnesses; the displayed alternative actual roots preserve each obligation. The cover persists. At the fixed anchor, the remaining avoiding residual roots have intersection `{x}`, so qualification there fails. Deleting the added incidence restores qualification in one legal exact-four primitive. This is correctly presented as an illustration, not a universal accessibility theorem, and it does not exclude qualifying entries elsewhere.

7. **Twelve-slot feasibility and solved-case classification.**  
   The cyclic `(3,2,2)` core has exactly twelve roots. Every four-set contains a core triple; a triple taking one label from each part is independent. Therefore its transversal is exactly four. It satisfies the inherited cyclic theorem's endpoint hypotheses. It is correctly classified as an already-covered cyclic endpoint, not a newly disconnected example or a new connectivity class.

8. **Safety, progress and endpoint restoration boundaries.**  
   The exact-compaction portion has legal next deletions and a strictly decreasing finite incidence count. The guard illustration has its explicit primitive and restored qualification. The principal counting theorem supplies no new general repair sequence, renewing exchange procedure or arbitrary destination restoration; the candidate says this explicitly. No progress measure is used to imply an unproved eligible move. X5's complete repair theorem remains unchanged.

## Inherited domains checked

I independently read the relevant immutable sources:

- X5's full triple-anchor theorem at `02b15a4787cc592e354b539095acf1ed1d6b295f`;
- X4's pair-anchor theorem and method-limit discussion at that publication;
- the accepted-result ledger there;
- `AGENTS.md` at integrated baseline `466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f`;
- baseline `GENERAL_PARENT_CONNECTIVITY.md`, `GUARD_BUFFER_CONNECTIVITY.md`, `CYCLIC_TRIPLE_CONNECTIVITY.md`, `OVERLAPPING_CLIQUE_EXCHANGE.md`, and `PALETTE_SLACK_CONNECTIVITY.md`.

The dependency dispositions are correct:

- Exact compaction is proved directly with the supplied minimum cover.
- AC covers the six-label twenty-triples control: `h=3`, `q=4`, `N=10`, `r=20`.
- AA covers the displayed cyclic core only within its declared class.
- Maximum-layer removal requires an actual finite lower-guard path and is not used to manufacture one.
- Symmetry preserves the carrier and cannot make an empty target class nonempty.
- No arbitrary mixed-floor root permutation is assumed.
- Disjoint-guard buffering requires actual compatible guards.
- Palette room requires `k >= Σ a_i`; it does not apply to `k=7,r=12`, uniform floor three.
- Element-cover connectivity alone is not promoted to pair-cover renewal.
- Root-level target emptiness is not promoted to nested disconnection.

These are applicability checks, not recertification of the inherited proofs.

## Closeout recommendation

Publish this as an **independently accepted analytical existence obstruction**, with the reviewed statement and explicit boundaries above. Preserve the distinction between accepted analytical work and integrated implementation certification.

The substantive new conclusion is that **X5 protection cannot always be created as a qualified exact-four endpoint on a feasible carrier**: at seven labels and twelve slots its target class does not exist. A universal explanation must therefore use another accepted class or a replacement mechanism carrying the coupled pair obligations directly. Universal repair, arbitrary accessibility for `r>=13`, and remaining larger-palette cases stay open.
