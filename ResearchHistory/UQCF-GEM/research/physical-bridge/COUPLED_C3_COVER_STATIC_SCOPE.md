# Cover-aware static reserve — prospective finite verification scope

Status: prospective only; no campaign has run. The all-positive, arbitrary-finite-H result rests on RESULT.md's proof. This finite scope is deliberately complete within the following declared carrier/saturation families, not an enumeration of all carriers or native paths.

## Carrier and saturation families

Vertices use the indicated integer labels; roots are lexicographically ordered H-edges. Distinct family identities remain present even if any computed summary coincides.

1. H=K4 on 0..3: EVERY saturation subgraph G subset H (64), EVERY source profile a in {1,2}^4 (16).
2. H=C5 with edges 01,12,23,34,04: EVERY G subset H (32), EVERY a in {1,2}^5 (32).
3. H=K5: G is empty, H, or H with all edges incident to v removed for EACH v=0..4; also G is the K23 cross graph with parts {0,1} and {2,3,4}, with or without edge01. These nine G identities each take EVERY a in {1,2}^5.
4. H=K6 minus edge45: G is empty, H, or H with all edges incident to v removed for EACH v=0..5. These eight G identities each take EVERY a in {1,2}^6.
5. H=K5 minus edge34: G is empty, H, or H with all edges incident to v removed for EACH v=0..4. These seven G identities each take EVERY a in {1,2}^5.

The declared Cartesian family has 3,072 source identities (1,024+1,024+288+512+224). This is an a priori size calculation, not an execution result. All five carriers have source hitting number three or four. The upper endpoint bound is always FOUR, including source-three cases.

## Complete static reconstruction

For every source identity, independently enumerate ALL nonnegative count vectors n indexed by the H-types with sum n<=A. Reconstruct exactly those satisfying original pair floors and an occupied-type vertex cover of size at most four. Preserve the exact feasible count identities in canonical order, their minimum active total and every minimizing vector. Do not supply outcome-selected count lists or infer completeness from a hash alone.

Independently enumerate EVERY vertex cover C of H with |C|<=4, not only minimum covers; EVERY nonempty G-independent set I; every deficient I; and EVERY eligible (C,I) satisfying |I|>|N_G(I)| and I intersect {v:a_v=1} intersect C empty. For EACH C, compare criterion existence with direct feasible-count existence with n_v>=1 on C and sum n<A. Compare unrestricted existence with the complete feasible count universe. Preserve all positive and negative per-cover identities.

For EVERY eligible pair (C,I), construct the stated unit-redistribution counts and a canonical actual endpoint: reserve the FIRST original label at each C-type as anchor; process remaining type slots in increasing type order, assigning remaining original non-anchor labels in increasing label order; remaining labels are empty. Check all actual original floors, domination, the chosen actual anchors, emptiness count exactly |I|-|N_G(I)| and actual hitting number<=4. Also verify the same contract for the LAST original label at each C-type as anchor; retain distinct anchor-choice identities even when first and last coincide, but deduplicate full endpoint states for expensive checks. This tests two fully declared choices, not every mixed first/last choice or every original label assignment. The universal anchor-choice statement is analytical.

For every distinct canonical labelled endpoint, check EVERY original protected one-hidden mask: one new hidden label outside the original core palette, placed at each possible subset of the ORIGINAL roots E(H) for which the original full source has hitting number in {3,4}. Preserve exact protected-mask and endpoint identities, count endpoint occurrences separately from distinct endpoints, and compare all canonical records before their hashes. Do not claim enumeration of arbitrary labelled endpoints, multi-hidden states or paths. Arbitrary protected hidden-completion validity follows from the explicit domination/cover proof.

## Required discriminating controls

- H=K6-minus45, G isolating0, all singleton: no static reserve; the deletion endpoint passes floors/domination but fails upper-four with hitting number5. Deficiency-only and isolated-type shortcuts must be rejected.
- Same H/G with duplicated type0: static reserve exists with the original type0 anchor retained.
- Same H, G isolating4 or5, all singleton: static reserve exists with the unique four-cover preserved.
- H=K5-minus34, G isolating0, all singleton: static reserve exists via cover1234, while the unique minimum cover012 cannot be preserved. Reject minimum-cover-only enumeration and upper-source-tau substitution.
- K5 saturated K23, duplicated types: reproduce static existence without making a reachability assertion. The known locked-family boundary must not be relabelled as accessible.
- Reject omitted carrier/G/profile/C/I/count/minimizer/canonical endpoint/protected-mask identities; shifted original floors; illegal singleton depletion inside C; wrong actual anchor; a fresh label; and a claimed reserve without the exact deficiency count.
- Validate input domain: no missing types (a_v=0), no nonedges declared saturated, no isolated H-types, source hitting number outside {3,4}, no alleged C that fails to cover or exceeds four.
- Reject missing, truncated, extra and corrupted canonical streams. Rejection may use explicit verification exceptions; do not silently accept end-of-stream. This new checker need not reproduce the inherited deferred exception-type minor.

## Scientific loop and retained scope

Publish proof, this scope and implementation plan at an immutable prospective freeze BEFORE tests/enumeration. Then retain genuine missing-implementation RED; implement distinct producer and checker; run new scientific tests plus all378 immediate inherited tests; independently reconstruct complete canonical records and reproduce certificate/companion bytes. Exact-event GitHub verification, fresh reproduction, adversarial mathematical review and separate publication review are required. Preserve all raw reviews, original ZIPs/full logs/metadata, failures and attempts. Audit originals and evidence-rejection controls separately from scientific counts; obtain a fresh separate publication reviewer, update both indices and finish immutable text/blob/head readback before scoped CLOSED.

Performance may cache only explicitly equal complete count universes and original hidden-mask universes, preserving every source identity and its original floors/profile. No runtime-dependent sampling, outcome-based exclusions, reduced scope or weakened gate is allowed. If resources require an amendment, record and prospectively freeze it before running the amended campaign.

No first-vacancy route, connectivity classification, exact labelled repair/restoration, cost optimum, progress rule, observer initialization or broad C3/C4 closure is part of this contract.
