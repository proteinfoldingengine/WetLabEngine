# Perfect-matching escape without vacancy — analytical obstruction

Date: 2026-10-11 UTC.
Prospective scope: `d18095854994928e4cc65a448600bfef2c78a161`.
Status: **SCOPED CLOSED** after verification at event commit `857803fb97e80a9d7b4f9338ebf9ef2de4d5f8e1` and exact immutable publication readback at `d1c2fc5594555764e6ec0ba333e41c3cbdff492b`.

## Theorem

Let H be K6 with the edge 45 removed. Let G be any perfect matching contained in H, and let every source multiplicity a(v) be a positive integer.

Then:

1. the source has an inherited cross-star first-escape certificate X;
2. G admits no nonempty independent set I with |I|>|N_G(I)|;
3. no static reserve exists in the cover-aware source domain;
4. therefore no safe path from the source reaches a first vacancy.

Thus a permitted first cross-star escape does not in general continue to a first vacancy. Static endpoint existence remains a logically separate necessary condition.

## Proof

### 1. Source cover and B(v)

The only independent pair of H is {4,5}. Therefore every vertex cover has size at least four, and the only size-four vertex cover is C={0,1,2,3}. The source hitting number is exactly four.

Consequently B(v), existence of a cover of size at most four excluding v, holds exactly for v in {4,5}.

### 2. Every source has a cross-star escape

Because G is a perfect matching, every vertex v has a unique saturated neighbor w and T(v)={vw}. Choose v in {4,5}. The edge vw exists because G is contained in H. Vertex w has a neighbor z distinct from v in H: H has degree four at 4 and 5 and degree five at 0,1,2,3. Hence vw and wz are H-edges for some distinct z.

Since B(v) holds, the inherited exact gate certifies X(v,w,z), regardless of whether a(v)=1 or is larger. The normalized route deletes the chosen original v-label down to {vw} and then adds wz. Every prefix is safe by the CLOSED first-source-escape theorem. Optional NOOPs may stall, but a committed first escape is reachable.

### 3. Perfect matching forbids every deficient independent set

Let p(v) be the unique matching partner of v. For any nonempty independent set I in G, p(v) lies in N_G(I) for every v in I. The map v -> p(v) is injective because matching edges are disjoint. Therefore

`|N_G(I)| >= |I|`.

So no nonempty G-independent set is deficient.

The CLOSED cover-aware static theorem states that a static reserve exists only if some size-at-most-four cover C' and some nonempty G-independent I satisfy |I|>|N_G(I)| together with the anchor eligibility condition. The required deficiency never occurs, independently of the multiplicity profile. Hence no static reserve exists.

### 4. Vacancy reachability is impossible

A state reached at the first vacancy is itself a static admissible endpoint with an empty original palette label. Since no such endpoint exists, no safe path can reach a first vacancy.

This argument excludes every possible route, not only the natural substitution attempt.

## Why the naive substitution fails

Use the named instance G={04,15,23}, a=(2,2,2,2,2,2), and X(0,4,1). The crossing label x originally of type 0 stays incident to the saturated bridge 04 throughout the X route. Completing x to the full star M(4) adds support on the other edges incident to 4 but adds no new incidence at 04: x was already counted there.

The saturated floor at 04 is a(0)+a(4)=4. Deleting the 04 incidence of an original type-4 label would lower its support from four to three. Thus x cannot substitute for that label on the bridge. The failed broad prospective scope is preserved in history; this precise floor deficit is its rejecting control.

## Bounded verification target

The prospectively frozen finite campaign covers all twelve perfect matchings of H and all 64 profiles in {1,2}^6, for 768 sources. It must reconstruct all covers, B(v), V/X candidates, independent sets and neighborhoods, actual-label X routes, route slices, floors, hitting minima, domination, and original protected one-hidden masks. Complete producer/checker identity equality and the frozen rejecting controls are required.

The finite enumeration will corroborate the bounded source matrix. The proof above establishes the arbitrary-positive-multiplicity obstruction without extrapolating from finite counts.

## Boundaries

This does not classify escape-to-vacancy reachability when a static reserve exists. It does not assert that every non-perfect-matching saturation graph has a reserve, or that static existence plus X is sufficient. It does not derive native observation, access, retention, enforcement, outcome selection, commitment, or progress.

Broad C3/C4-C6 and physical origin remain OPEN. No force, geometry, fundamental time, dark-matter variable, external alignment, or numerical heuristic is introduced.


## Independent verification

Actions run `38167992780` verified the prospectively frozen 12-matchings × 64-profiles universe: 768 sources, 96,768 candidate classifications, 48,384 independent-set rows, 19,968 actual-label X routes, 110,592 slices, and 648,680,448 protected-mask/state checks. The independent checker reconstructed the complete canonical stream at SHA-256 `b6b53398b5ec82f9552284b93cdb2e10ef357bc277e27054eda3aee41af77610`; a fresh reproduction was byte-identical. All 504 tests passed. Gemini 3.1 Pro mathematical review and separate publication audit both ACCEPTED with zero missing assumptions and zero counterexamples. See `COUPLED_C3_ESCAPE_OBSTRUCTION_REPORT.md` and the evidence index.
