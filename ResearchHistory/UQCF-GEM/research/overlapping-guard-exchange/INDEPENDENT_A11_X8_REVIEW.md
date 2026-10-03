# Independent analytical review — A11.X8

**Reviewer:** independent Codex review agent `/root/a11_x6_review`
**Decision:** **ACCEPT — no mathematical corrections requested**
**Scope:** analytical composition and dependency applicability; no numerical execution or implementation certification.

## Exact sources

I independently fetched the immutable scope and candidate through GitHub.

Repository: `proteinfoldingengine/WetLabEngine`
Subtree: `ResearchHistory/UQCF-GEM/research/overlapping-guard-exchange/`

| Source | Commit | UTF-8 bytes | SHA-256 | Git blob SHA |
| --- | --- | ---: | --- | --- |
| A11_X8_SCOPE.md | 8010f4e04b616d89cc2227cd53f7960a502d5af6 | 2624 | c219cc9ff7fe39f7c05443768bea03ade35feaa61f122e61a4074a1d3080eaae | db4c8d154b3f7fb8e92dd87a3f5c68afe91386d5 |
| A11_X8_ONE_OVERLAP_INCIDENCE_REPAIR.md | 6c5b2159080486b83fd005d42e0bbd719561f9f2 | 12645 | ee966487ab7b5de20574af2af127e3a7e1caf40040e8f0c4f732db3e8edb50ed | 5fd714a1e170c06490cbcc49f75a846bc8acf66f |

Hashing the fetched UTF-8 contents reproduced both Git blob identities.

GitHub comparison from parent `7b475d5c904fb5bbba1888b9944be98ee1ad74b1` to candidate `6c5b2159080486b83fd005d42e0bbd719561f9f2` shows two commits ahead, no divergence, and exactly these two additions. Inherited sources, certificates, implementations and workflows remain unchanged.

## Accepted theorem

For a fixed uniform original floor `h`, palette size `k`, labelled slot count `r`, and feasible exact-`q` endpoints with `q>=3`, put

\[
N=\left\lfloor\frac{r(k-h)}k\right\rfloor.
\]

If `r>=2N−1`, every endpoint pair admits finite native primitive repair in `{q−1,q}`, restoring the original labelled destination including every noncompact incidence.

The endpoint-sensitive sufficient condition is also correct: after exact uniform compaction, selected maximum incidence degrees satisfying `d_A+d_C>=r−1` imply the same conclusion for that pair.

For seven labels, floor three, target four, this closes all endpoint pairs at **r=13,15,17**. Together with prior sufficient results, the remaining universal carrier obligations at seven labels are confined to **r=14,16,18**, before further endpoint-class exclusions.

## Proof checks

1. **Exact preparation and inherited guard availability.**
   Minimum-cover-retaining compaction is legal and exact at every primitive. Its excess-incidence measure decreases with an eligible deletion whenever needed. Accepted X7G supplies actual guards of sizes `m_A=r−d_A`, `m_C=r−d_C`, each at most `N`. No X7 disjoint-slot criterion is improperly imported.

2. **Slot allocation.**
   Either hypothesis gives `r>=m_A+m_C−1`. The destination guard can therefore occupy existing slots with zero or one shared index. In the one-overlap case, an index in the nonempty source guard supplies that shared slot. Uniform floors make the full exact-endpoint root permutation admissible; no unprotected bare guard is permuted.

3. **Shared comparison guard.**
   A set with at most `q−2` labels hitting all exclusive source and destination supports must miss the old shared support and the destination shared support. It consequently misses their union, contradicting a cover of the comparison family. Thus the comparison family has transversal at least `q−1`. This correctly uses a single shared index and does not generalize the argument to arbitrary overlap.

4. **All primary pair witnesses.**
   At target four, every label pair misses some support of the comparison family. During shared-root handover, each current support is a subset of its corresponding comparison support. Its actual root therefore retains the missed-pair witness. Anchor-only, residual-only and mixed pairs are all covered by this argument.

5. **Primitive legality.**
   Destination-only additions preserve the old support's floor. Old-only deletions occur after the destination support is installed and retain its floor. Shared expansion and contraction obey the same checks. Every edit toggles one legal incidence in one existing root.

6. **Renewal and next-move existence.**
   The unchanged source guard protects exclusive destination preparation. The comparison guard protects the shared-root handover. The fully installed destination guard then protects every remaining repair. No exact-target reset is needed at handover. Any unfinished root has either a missing destination incidence or an old-only incidence, furnishing the next legal primitive.

7. **Finite progress.**
   Every middle primitive decreases the total symmetric difference from the permuted destination by exactly one. The phase restrictions retain an eligible edit until each phase is finished. The preliminary route therefore terminates at the exact permuted destination.

8. **Upper conversion and full restoration.**
   The preliminary path supplies the required lower guard; it is not falsely asserted to stay below `q`. Its uniform upper bound is `k−h+1`, equal to five in the primary case. Inherited Theorem A applies to this actual finite path between exact endpoints. Source compaction, converted middle path, reversed endpoint permutation and reversed destination compaction join at exact `q` and restore the complete original labelled destination.

9. **Nonvacuity.**
   X6's explicit thirteen-slot exact-four construction supplies feasibility at `r=13`. Filling two or four additional existing slots with the full palette preserves exactness and original floor three, supplying feasibility at `r=15,17`. No additional slot is inserted into any repair carrier.

10. **Residual arithmetic.**
    Substitution into `N=floor(4r/7)` verifies the stated incidence criterion for `r=4…13,15,17,19`, and its failure at `14,16,18`. The prior uniform O1 bound covers every `r>=19`. These are sufficient connectivity statements; they neither assert feasibility at every smaller slot count nor infer disconnection from inequality failure.

## Dependency and acceptance checks

I independently fetched `GUARD_HANDOVER.md` at frozen candidate `fa71695118731da7f0e17bf8a31f0142e4c76267`. Its exact fetched source has:

- UTF-8 bytes: **7457**
- SHA-256: **963a9a1c03f90c449e5703fd31c309d389eb47740ac4a149dd4a92642dc8468c**
- Git blob: **806bb76a50c8b5e7e7234f71296b3968ec53ac86**

I fetched `INDEPENDENT_REVIEW.md` at X8's parent `7b475d5c904fb5bbba1888b9944be98ee1ad74b1`. It attributes **ACCEPT** to reviewer `/root/overlap_handover_review` for that exact O1 candidate. Its recorded O1 SHA-256 matches the independently fetched source.

The relevant accepted dependency domains hold:

- **X7G:** exact uniform compaction and actual omitted-label guard availability.
- **O1:** actual endpoint guards intersecting in at most one index; the shared comparison proof applies exactly.
- **Baseline Lemma M:** full exact-endpoint root permutation with compatible destination floors, supplied by uniform `h`.
- **Baseline Theorem A:** an actual finite lower-guard native path between exact endpoints on the fixed carrier.

Baseline M/A were independently read earlier in this review session at `466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f`. These are applicability checks, not recertification.

## Publication assessment

X8 is a valid incremental analytical extension: it removes one required disjoint guard slot from X7's sufficient budget by composing established guard availability with established one-overlap handover.

It does not weaken X5, contradict X6, claim multiple-overlap repair, certify original destination-directed scheduling, or establish unrestricted nested universality. No numerical campaign, physical implication or implementation certification is claimed.

**Recommendation:** publish the exact reviewed candidate and receipt as an accepted complete analytical theorem within its stated parameter class, retaining the explicit remaining obligations.
