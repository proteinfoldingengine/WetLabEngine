# Independent analytical review — A11.X7

**Reviewer:** independent Codex review agent `/root/a11_x6_review`  
**Disposition:** **ACCEPT — no mathematical corrections requested**  
**Review type:** analytical proof and dependency-domain review; no numerical execution or implementation certification.

## Immutable sources reviewed

I independently fetched these exact GitHub sources, rather than relying on the author's transcription.

Repository: `proteinfoldingengine/WetLabEngine`  
Subtree: `ResearchHistory/UQCF-GEM/research/overlapping-guard-exchange/`

| Source | Commit | UTF-8 bytes | SHA-256 | Git blob SHA |
| --- | --- | ---: | --- | --- |
| A11_X7_SCOPE.md | 11da7b687cac61a4b9639e83af3e6bd50c14455b | 2862 | 1f7bb5d43c8e4fb0dbc096199e645c0e88e88add2160b77ef4518be4a2355256 | 2b0ab4a1c52dc3c2ad551654ce4f0dcb7a515872 |
| A11_X7_INCIDENCE_GUARD_REPAIR.md | 4e0eee45107e54d6059d00b846a666fd0cd6c00d | 14163 | 1c329cc22b9620b3df29480ae332a167a49d970b6b2f9ced89a35bde013cf1c5 | a47e286209f3728d7da9d5d46d45f5f8cc5f5e43 |

Local hashing of fetched UTF-8 contents reproduced the Git blob identities. This involved source handling and hashing only.

GitHub comparison from X6 publication `4c2b4007bb309a92f3200468c5d243e497d723cd` to X7 candidate `4e0eee45107e54d6059d00b846a666fd0cd6c00d` reports two commits ahead, no divergence, and exactly two added files: X7's scope and proof. No inherited scientific source, execution machinery, certificate, workflow or integration file changed.

## Accepted statements

After exact compaction of an exact-`q` state on a uniform-floor-`h` carrier, there is an actual `(q−1)`-guard occupying at most

N = floor(r*(k-h)/k)

existing slots.

If `2N <= r`, every pair of feasible exact-`q` endpoints on that carrier admits a finite native primitive path with transversal in `{q−1,q}`, preserving the fixed palette, original floors, labelled slots and exact destination supports.

The sufficient condition `2h >= k` follows for every slot count.

In particular, **all exact-four endpoint pairs on seven labels and twelve labelled floor-three slots are connected in `{3,4}`**, including all permitted noncompact endpoints. No cyclic-core or X5-qualification hypothesis remains.

## Mathematical checks

1. **Exact compaction.**  
   Every retained `h`-subset contains a label from the supplied minimum `q`-cover. Each deletion respects the original floor, cannot decrease transversal, and retains the upper bound `q`. An excess incidence furnishes a legal next deletion, and the finite excess-incidence count strictly decreases. Reversal restores all original noncompact supports exactly.

2. **Actual omitted-label guard.**  
   If roots avoiding label `x` had a cover of size at most `q−2`, adjoining `x` would cover the full exact-`q` tuple with at most `q−1` labels. This contradiction establishes the required guard without an assumed protective family. The family cannot be empty. Its roots are actual labelled supports; no external constraint is introduced.

3. **Incidence bound and rounding.**  
   Exact compaction yields `hr` incidences. A maximum-incidence label occurs in at least `ceil(hr/k)` roots, leaving at most
   `r−ceil(hr/k)=floor(r(k−h)/k)` actual avoiding roots. The rounding and the subsequent slot inequality are correct. For the primary carrier, `N=floor(48/7)=6`.

4. **All pair witnesses in the primary case.**  
   A guard of transversal at least three cannot be hit by any label pair. Consequently every pair has a disjoint actual guard root. This includes mixed pairs and pairs entirely inside or outside any proposed anchor triple. The proof does not allocate fictitious independent capacities to overlapping protection systems.

5. **Disjoint guard placement.**  
   `2N <= r` supplies enough existing slots outside the source guard to hold the entire destination guard. Every compact support and every original floor has size `h`; the endpoint root-support permutation is admissible. Inherited Lemma M realizes it at exact full endpoints through native primitives. No bare guard at level `q−1` is assumed movable. Reversing this permutation restores the destination's original labelled assignment.

6. **Primitive bridge legality and available progress.**  
   Each union bridge adds missing destination incidences before deleting old-only incidences. Additions preserve the current floor; deletion stages contain the floor-sized destination support. Every unfinished root has the stated eligible edit. The total symmetric difference from the permuted destination decreases by one at every primitive, establishing finite termination.

7. **Protection handover and reuse.**  
   The actual source guard stays fixed until every destination-guard root is installed. The fully installed destination guard then stays fixed while all remaining roots, including the old guard, are repaired. Handover need not restore exact `q`; the lower guard suffices. Protection is therefore available for every subsequent edit, rather than merely the first exchange.

8. **Upper bounds and maximum-layer conversion.**  
   The preliminary construction proves `tau >= q−1`; it is correctly distinguished from the final band path. The bound `tau <= k−h+1` holds for every allowed intermediate support tuple. On the primary carrier the preliminary upper bound is five. The constructed finite lower path joins exact-`q` endpoints and meets inherited Theorem A's fixed-carrier hypotheses, so upper excursions can be removed. No unproved lower path is supplied by that theorem.

9. **Exact original destination restoration.**  
   Source compaction, converted middle repair, reversed destination permutation, and reversed destination compaction concatenate at exact-`q` states. Every component respects the same palette, slots and original floor vector. The final state is the original labelled destination, including every noncompact incidence.

10. **General half-palette corollary.**  
    `2h >= k` implies `2r(k−h)/k <= r`, hence `2N <= r`. The statement is correctly sufficient rather than necessary.

## Dependency-domain review

I used the previously independently read exact baseline sources at `466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f`:

- `GUARD_BUFFER_CONNECTIVITY.md`, AB: actual disjoint-index guards at exact endpoints. X7 derives their size and compatible placement.
- `OVERLAPPING_CLIQUE_EXCHANGE.md`, M: root-support permutations with destination-compatible floors. Uniform original floors provide that compatibility.
- `GENERAL_PARENT_CONNECTIVITY.md`, A: a finite lower-guard primitive path between exact endpoints. Section 5 explicitly constructs this path.

Those inherited proofs are domain-checked, not recertified or claimed as new discoveries. The new mathematical ingredient is guard availability from exactness and incidence averaging.

## Scope and interpretation

X6's empty X5-target theorem remains intact. X7 replaces the unavailable triple-avoiding protection with an actual **single-label-avoiding guard** and thereby closes all endpoints on the twelve-slot carrier, beyond the previously accepted cyclic subclass.

No new same-slot hypothesis is needed because X7 invokes a different guard mechanism. Failure of the incidence criterion is correctly left inconclusive. Arbitrary mixed-floor permutation, universal original destination-directed scheduling, unrestricted nested universality, physical implications and implementation certification are not claimed.

The middle path's decreasing symmetric difference does not make the entire construction destination-directed relative to the original endpoints; the proof expressly preserves that distinction.

**Recommendation:** publish as an independently accepted complete analytical connectivity theorem in the declared uniform incidence class, including the universal seven-label/twelve-slot/floor-three corollary. Preserve the separate status of analytical acceptance and later integrated implementation certification.
