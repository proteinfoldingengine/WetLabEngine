# v16.23 — Overlap descent: complete findings

| Question | Adjudicated answer |
|---|---|
| Which operation is now closed? | Compatible signed source data and response classes on overlapping actual retained subsets glue uniquely on their union. The set lattice, exact source/response sequences, associativity and finite-cover refinement are proved in O1–O4. The shared prefix-tree/Genesis and signed-rational assumptions remain explicit. |
| What happens to lost information? | Joint observations of Y and Z inside a larger X lose exactly ker P_X,Y-union-Z. Gluing does not recover information outside that union. The earlier cumulative fixed-target non-descent result is unchanged, not replaced by this construction. |
| Does the retained structure provide the construction? | Yes: actual source zero extension and fiber pushforward give signed inclusion-exclusion; actual potential restriction and ancestral pullback give quotient-response gluing. No missing splitting is invented or old inclusion discarded. |
| Does this further select the v16.22 response? | No. Every comparison-compatible family preserves the gluing equations. All four vectors of the complete certified bounded parent solution basis satisfy them. This is a proved consequence of existing naturality, not a no-canonical-map claim. The fixed unweighted inverse remains unique under its definition. |
| What happens for nonnegative sources? | Overlap agreement alone is insufficient. The unique signed gluing must additionally satisfy exact nonnegativity inequalities. There are admissible two-view and three-view counterexamples; in the latter every pair has a nonnegative gluing but the whole cover does not. O5–O6. |
| What was genuinely checked? | 25 new and 57 inherited tests; complete pair/triple coverage, exact equalizers, cone membership against independently enumerated global sources, the parent response basis, changed coordinates and explicit rejecting controls. Counts below. |
| What remains open? | Physical realization of these formal source grades, physical selection of the response law, extensions beyond the admitted shared prefix-tree category, and any quantum/geometric interpretation. No physical consequence follows merely from naming a gluing obstruction. |

## Main scientific distinction

The strongest result is not another fitted readout. It is a precise distinction between two kinds of completion:

**Compatible signed information closes uniquely. Compatible nonnegative information may fail global realization.**

The formal signed space permits subtraction, so an inclusion-exclusion reconstruction can exist even when one coefficient is negative. Requiring actual membership in the nonnegative cone is a separate mathematical condition. Neither category is silently substituted for the other.

The outcome against an optimistic response-selection expectation is also clear: these overlap relations do not remove v16.22's depth freedom. They are already implied by the comparison diagrams. This does not make the original Green inverse ambiguous: retaining its defining inverse equation still singles it out.

## 1. What the retained information determines

Fix one common-Genesis finite prefix tree X. Let Y,Z be actual root-containing, prefix-closed subsets. Their union U and intersection J are again admissible retained carriers. No common origin is inferred for unrelated constructions.

For E_Y=I_YX P_XY, the actual ancestor maps imply

    E_Y E_Z=E_Z E_Y=E_J,
    E_Y+E_Z-E_J=E_U.

For compatible signed sources, c=P_YJ x_Y=P_ZJ x_Z, define

    x_U=I_YU x_Y+I_ZU x_Z-I_JU c.

The proof checks both required marginals and proves uniqueness by the second projector identity. Thus F_U is isomorphic to the fiber product F_Y x_(F_J) F_Z, with the actual pushforwards defining compatibility. The same statement holds on the balanced signed source spaces. No equal-dimension identification supplies a map.

For arbitrary finite covers, subtree-source totals are compatible coordinates: c_root=sum x, c_v=sum over descendants of v. They restrict under pruning and invert by x_v=c_v-sum_children c_child. These identities prove finite-cover reconstruction, repeated-view consistency and associativity. The implementation checks both binary parenthesizations on a complete basis of global source and response data for every declared triple; the general proof supplies the equivalence to all compatible triple data.

Joint readout of views inside a larger X has kernel ker P_XU. The union is the reconstruction domain; discarded information outside it is not recovered.

## 2. Response classes and the unchanged parent family

The response quotient is W_X=Q^X/Q1. Because every view retains the same root, equality of classes on an overlap can be checked using their unique root-zero representatives. Compatible representatives glue on U independently of the constants originally used to represent the classes.

Equivalently the quotient gluing is

    phi_U=H_YU phi_Y+H_ZU phi_Z-H_JU phi_J.

The source and response glue operations are different typed constructions. For every v16.22 compatible family T:S->W, the source gluing and response gluing commute with T by the already-proved restriction/inclusion equations and uniqueness on U. No rerooting, depth-shift arrow or physical equation was added.

The verifier loads the checksum-bound complete v16.22 certificate and verifies its unrestricted solution basis, constraint compliance and dimension. It tests every basis vector on the new overlap diagrams in U1 after an explicit rooted identification. All **8,056** original-plus-relabeled basis/gluing diagrams pass. The bounded dimension remains **4**; it is not a universal four-parameter physical model. The general family continues to have one coefficient per lineage depth.

## 3. The nonnegative-source criterion and counterexamples

For nonnegative local rational sources, a global nonnegative source exists precisely when the unique signed candidate is nonnegative. Outside J, its components are already nonnegative. At each shared vertex v the exact additional condition is

    x_Y(v)+x_Z(v)>=c(v).

This is the membership condition derived from actual fiber aggregation, not a tolerance or a fitted physical law.

### Two compatible nonnegative views with no nonnegative completion

Use the three-node star X={root,a,b}, views {root,a} and {root,b}. Each local vector is (0,1), total 1. Both prune to source 1 at the shared root. The unique signed global vector is

    (-1,1,1).

The parent maps return the two declared local vectors, but the root amount is negative. Uniqueness in the signed space rules out a different rational nonnegative completion. Adding a constant to the source is not a potential-gauge transformation: it changes source total and local data.

### Every pair can succeed while the full cover fails

Use X={root,a,b,c} and views {root,a}, {root,b}, {root,c}. Every local vector is (1,1), total 2. Every pair has the nonnegative source (0,1,1) on its union. All three require the unique signed vector

    (-1,1,1,1),

so no global nonnegative source exists. This is a checkable counterexample to the universal implication 'every pair has a nonnegative gluing, therefore the whole cover does.' The verifier reconstructs the actual marginals, checks uniqueness, and enumerates all possible global nonnegative integer sources at the fixed total.

For a general finite cover, the glued subtree totals c determine the exact global inequalities c_v>=sum_children-in-U c_child at every vertex. Individual views or every pair can miss the combined inequality. These are extensive aggregation constraints. We do not call them quantum contextuality, a new physical mechanism, or geometry.

## 4. Exact computational coverage

U1: every rooted unordered tree shape with one through five vertices, counts 1,1,2,4,9. U2: the four historical fine trees, independently tagged. Each instance includes every actual root-containing ancestor-closed subset, all ordered pairs, and all ordered triples, including repeated and nested views. Isomorphic actual subsets are not deduplicated. The size bound is an implementation bound, not a physical cutoff.

| Original-coordinate coverage | U1 | U2 | Total |
|---|---:|---:|---:|
| Initial instances | 17 | 4 | 21 |
| Ordered retained-view pairs | 1,007 | 1,902 | 2,909 |
| Ordered retained-view triples | 10,495 | 48,052 | 58,547 |
| Compatible nonnegative local-source pairs, totals 0–2 | 16,626 | 52,336 | 68,962 |
| Pairs with nonnegative global source | 14,568 | 46,164 | 60,732 |
| Pairs with no nonnegative global source | 2,058 | 6,172 | 8,230 |

Every instance is repeated after the declared root-fixed reversal of nonroot identities and reversed retained-array storage order. Combined: **42 instances, 5,818 pair diagrams, 117,094 triples, 137,924 compatible nonnegative local-source pairs**, of which **16,460** have no nonnegative completion. These counts include deliberate repetitions from different views/coordinate variants and are not independent physical observations.

The verifier performs **5,818 balanced-source equalizer checks**, **11,636 non-permutation coordinate diagram checks**, and the **8,056 parent-basis overlap checks**. Its final count is **3,083,939 executed assertions**, not a replacement for the general proofs.

The producer uses ancestor-first parent arrays, longest-prefix fibers and inclusion-exclusion. The verifier imports neither producer nor its enumerator: it reconstructs rooted shapes through Pruefer words, follows parents directly, reconstructs exact compatibility matrices, and solves their equalizers. Nonnegative feasibility is compared to independently enumerated GLOBAL sources rather than trusting the producer's positivity flag.

For arbitrary gluer extensions B off the compatibility domain, the verifier requires BA=id and AB=id on ker D, not equality to one chosen extension. A deliberately changed B+KD is accepted when it is the same map on compatible data. Coordinate choices are not promoted to additional physical structure.

## 5. Rejecting controls and a real correction

The primary 22-test suite contains ten logged corrupt-certificate rejections: wrong pushforward, wrong gluer on compatible data, wrong overlap, foreign origin, false positive feasibility, corrupt negative witness, missing pair, missing triple, missing map field, and inexact coefficient. A further test rejects an ordinary linear right inverse that selects a sibling and fails retained naturality under sibling exchange, while accepting the retained-root section.

A substantive review found that the initial verifier could accept an unchanged original instance merely labeled relabeled, because shape equality and aggregate-count equality alone do not prove the coordinate experiment occurred. Three new schema tests include two malicious cases and one genuine transformed positive control. In their RED run the original 22 tests passed, the two new rejection checks failed for ValueError not raised, and the true-control check passed.

The corrected verifier reconstructs the exact expected parent identities and storage order. It rejects a missing relabeling or reversal rather than accepting a variant label. The final suite is **25 new tests plus 20 v16.22, 22 v16.21, and 15 inherited exact pruning tests: 82 total**. The old GREEN is not retrospectively described as containing the later checks.

## 6. Run and publication evidence

| Role | Execution SHA | Run | Job |
|---|---|---:|---:|
| Preregistered wiring RED | d75bb1d9c043634a6f60c66d1a0153f39c7192c8 | 36568025339 | 109404706116 |
| Initial scientific GREEN | 939293191fd5bdd13a086b1d86ac15af595a1b6d | 36569139253 | 109408436653 |
| Substantive coverage RED | 54a3a1c57be3d749e86c88969b1556452235d513 | 36569553274 | 109409840157 |
| Corrected scientific GREEN | 1a1a38db702b1da47a829f08ce2740e2d578ea27 | 36570394253 | 109412645015 |

All four are attempt 1. Both REDs and both GREENs remain preserved with original archives. Corrected GREEN executes all seven declared commands successfully. The proof/type/preregistration commit is d091319bd837d5c6dccd66fcdb6b8ee139e79045, before either implementation.

The complete raw certificate is **7,011,626 bytes**, losslessly compressed to **111,376 bytes**. Raw SHA256 `a9b4d6c28dcb5ffbfcd5a997e2cb12668de37f4360846a45a6b8125985e8ff8a`; compressed SHA256 `6b27330c912ccb39f54a8e5c91d58b140d65036cf93a2e2b00c76836326b0a12`. Initial and corrected producer bytes are identical. Corrected verification SHA256 `76316091867ac1f6daf3cb8c9b5e8df3f67b23ded780afe79b853aa8568085bf`.

Publication metadata is separate in PUBLICATION_EVIDENCE.json, with its own workflow head, run/job/attempt and fresh reproduction. It must not be confused with the scientific execution head. PUBLICATION_SHA256SUMS binds the source, reports, scientific data and original archives. No expiring Actions artifact is the only copy.

Local unit/schema controls passed. A supplemental local full-verifier attempt was not completed within the 180-second tool limit after initial missing-file staging errors; it is not claimed as a second-environment full reproduction. The complete certified verification is the GitHub run and the separately recorded fresh publication reproduction. An unsupported local streaming-session request made no changes. These tooling incidents did not change scientific source or acceptance criteria.

## 7. Interpretation and next boundary

This stage closes overlap reconstruction in the specified signed retained category and derives exact constraints for membership in its nonnegative cone. It does not add a response-selection equation, change the Green inverse, or restore information beyond the observed union. Positive compatible local data can fail a genuine global feasibility condition even though their signed completion is unique.

The positive rational cone is explicitly analyzed, not equated to every physically attainable source. The parent response maps act on balanced signed sources; this is not a claim that the nonnegative balanced cone contains nonzero sources. Source feasibility and response selection remain distinct questions.

The entire campaign is **self-reviewed**, with an algorithmically independent certificate verifier but no separate human/agent reviewer. Written general proofs are not proof-assistant formalizations. Standard gluing, equalizer and extensive-aggregation mathematics is not claimed as a new universal physical law.

**Time is pruning / ordered recoverability update. No geometry, curvature, quantum primitive or gravity conclusion is inserted.**
