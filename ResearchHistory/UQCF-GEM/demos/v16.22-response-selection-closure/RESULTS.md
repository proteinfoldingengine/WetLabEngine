# v16.22 — Retained response-selection closure: complete findings

| Question | Answer, assumptions and evidence |
|---|---|
| What is now classified? | All linear response families on the admitted finite common-Genesis prefix-tree category that obey both retained comparison diagrams and every admitted relabeling. General arguments T1–T3; unrestricted exact solve and independent solution-space verification. |
| What is forced? | In the explicitly derived edge-source/edge-difference coordinates, the response cannot mix distinct lineage edges. Entries at the same lineage depth agree across trees. No diagonal ansatz was imposed. |
| What is not fixed by those diagrams? | One scalar coefficient per positive lineage depth. On trees of at most five vertices the complete solution space has dimension 4; fixing the first-edge unit leaves dimension 3. |
| What happens when the full fixed-inverse definition is retained? | Uniqueness: the original unweighted Green response is the ONLY solution of l_X T_X=id. All depth coefficients then equal 1. The earlier diagnostic is not made nonunique or replaced. T4. |
| Can these responses be compared and composed? | Yes under the actual P/I/R/H arrows from v16.21. Every candidate in the classified family obeys both diagrams; their generated compositions and insertion of intermediate legal prunings preserve the equations. No new response transport is supplied. |
| What was checked by code? | 189 unrestricted unknown entries, 998 independent-of-ansatz constraint rows (rank 185), 200 retained embeddings including automorphisms, 2,813 composable embedding pairs, 800 changed-coordinate diagram checks, complete solution basis, fixed inverse and explicit counterexample candidates. 20 new tests plus 15 and 22 inherited tests; 12 deliberate corruptions rejected. |
| What remains open? | Physical source attainability and physical justification of a response-selection equation; extensions to additional genuinely earned morphisms or carrier types. No metric, source law, quantum primitive, connection, curvature or gravity is inferred. |

## Bottom line

**Comparison compatibility and inverse uniqueness are different statements.** The existing retained operations impose a strong exact structure but do not, by those equations alone, force the specific unweighted inverse. Once that inverse's defining equation is included, it is unique. Both conclusions are positive classifications of their respective premise sets, not a generic declaration that the foundation is underdetermined.

The test does not discard the v16.21 Green response. It preserves it as the fixed reference and asks whether its defining property is a consequence of the other earned comparison relations. The answer is no for that implication, with an explicit full classification and nonproportional witnesses. It is not a theorem that no canonical construction exists. In particular, the original unweighted construction remains available and unique under its definition.

## 1. The two premise sets

Inherited types are S_X, the rational zero-total formal source arrays, and W_X, potential arrays modulo constants. The maps P and I are source fiber pushforward and retained zero extension; R and H are potential restriction and ancestral pullback. These are the actual supplied maps from v16.21, not equal-dimension identifications. TYPE_LEDGER.md records all definitions and their parent provenance.

C requires a linear family T_X:S_X->W_X with

    R_XY T_X = T_Y P_XY,
    T_X I_YX = H_YX T_Y,

and covariance under every admitted rooted/parent-preserving relabeling.

C+INV additionally retains l_X T_X=id, with l_X the already-fixed unweighted incidence Laplacian. No assumptions of invertibility, positivity, response-matrix symmetry or a diagonal ansatz enter C. The statement about C+INV does not remove its defining equation to create a no-go.

The rational signed source space is an inherited diagnostic. Finite additivity of physical positive grades alone does not establish that every formal signed direction is physically realizable. Real-scalar extension is conditional and justified by the general algebraic proof, not rational sample density.

## 2. What the information forces

For edge e=(p(v),v), b_X maps its unit coordinate to delta_v-delta_p(v). Its inverse takes subtree sums of a balanced source. The map d_X takes a potential class to its parent-child differences; its inverse integrates along the unique ancestral path. These are derived isomorphisms, not a geometric embedding or an added metric.

In those coordinates M_X=d_X T_X b_X. A retained subtree acts by deleting edge coordinates and inserting zeros. The two comparison equations force every entry between a retained and a discarded edge to vanish in both directions. Any two distinct edges can be separated by a legal retained prefix subtree, so M_X must be diagonal. Restricting to an edge's ancestral path and using rooted isomorphisms then equates the diagonal entries for all edges at the same depth.

The complete result is

    M_X = diag(a_depth(e)),
    T_X = d_X^{-1} diag(a_depth(e)) b_X^{-1}.

Conversely, every scalar sequence a_1,a_2,... satisfies every comparison and relabeling equation in C. Therefore the classification is complete over the stated category. Lineage depth is inherited address length, not a fundamental time coordinate. No sequence is chosen as a physical coupling.

With trees through N vertices, there are N-1 free parameters. On all finite trees there is an arbitrary scalar sequence, not four universal parameters. The bounded test's four-dimensional result is an implementation check of the general argument, not a physical cutoff.

## 3. Why the fixed inverse remains unique

The inherited unweighted incidence law is l_X=b_X d_X. Consequently

    l_X T_X = b_X diag(a_depth(e)) b_X^{-1}.

The defining inverse equation holds precisely when all a_k=1. The complete C+INV solution is therefore T_X=l_X^{-1}, the same Green response used in v16.21. Its physical interpretation is not supplied by this algebraic identity.

The strongest correction to an overly pessimistic expectation is that an exact selection statement DOES exist when its defining premise is retained. The strongest limitation on an overly optimistic expectation is that all comparison diagrams alone still admit nonproportional alternatives.

## 4. Checkable counterexample to selection by C alone

Predeclared candidates a_k=1 and a_k=k both obey all C diagrams and agree on the first-edge unit. On a three-node path, in independent nonroot source coordinates and root-zero potential coordinates, they are

    T_unit  = [[1,1],[1,2]],
    T_depth = [[1,1],[1,3]].

They are not global scalar multiples. The balanced full source (0,-1,1), represented by (-1,1), gives root-zero outputs (0,1) and (0,2), respectively. These are different classes modulo constants. Yet both are compatible with every declared pruning/inclusion relation.

For the unchanged fixed root-reduced Laplacian [[2,-1],[-1,1]], only the first is its inverse; the second gives [[1,-1],[0,2]] when multiplied by L. The verifier accepts the second as a C-family but rejects it if submitted as the original inverse. This explicitly distinguishes valid nonuniqueness evidence from a false claim about C+INV.

No new weighted physical model was run. The two sequences are algebraic witnesses inside an unrestricted classification, not proposed source dynamics or fitted parameters.

## 5. Exact computational evidence

The finite universe contains every rooted unordered shape of 1–5 vertices, counts 1,1,2,4,9, and every root/parent-preserving injection between them. Images are precisely the legal retained subsets; keeping all injections also tests every admitted automorphism. The producer uses ancestor-first parent arrays and subset enumeration. The verifier uses Prüfer enumeration and injections and imports none of the producer.

| Quantity | Exact result |
|---|---:|
| Rooted shapes | 17 |
| Retained embeddings | 200 |
| Unrestricted root-coordinate matrix entries | 189 |
| Distinct constraint rows | 998 |
| Constraint rank | 185 |
| Complete comparison solution dimension | 4 |
| Dimension after first-edge unit is fixed | 3 |
| Fixed-inverse affine freedom | 0 |
| Composable embedding pairs | 2,813 |
| Non-permutation coordinate diagram checks | 800 |
| Recorded verification checks | 12,890 |
| Deliberate defects rejected | 12 |

The 998 rows are not all linearly independent: their rank is 185. The word unrestricted refers to the initial unknown matrices, not to the class of allowed category morphisms.

The independent verifier solves ALL edge-coordinate matrix-entry constraints using equality/zero classes rather than the producer's root-coordinate nullspace calculation. It finds 136 forced-zero entries and four nonzero equality classes with 28,18,6,1 entries. The supplied complete basis is independently tested for linear independence and compliance with every root and edge constraint. The class counts are bounded combinatorial quantities, not independent physical samples.

Metamorphic controls reorder arrows and rows, change the complete kernel basis, and consistently change source and potential coordinates by non-permutation rational matrices. The check does not depend on a special computational basis being physical.

The 12 rejection records identify the exact reason for each failure: false nullity, corrupt kernel generator, incomplete basis, omitted embedding, omitted constraint, Boolean parent identifier, floating parent identifier, wrong fixed inverse, foreign Genesis, floating coefficient, missing required field, and a linear-but-nonnatural sibling-selecting response.

## 6. RED/GREEN, real review defect and corrected evidence

| Role | SHA | Run | Meaning |
|---|---|---:|---|
| Preregistered wiring RED | 310ec851211f708950f847e5a49d938637c45faa | 36519238541 | 18 missing-implementation failures with setup successful |
| Initial scientific execution | db10a265da716d4b16e10e8db42df0c5947f4207 | 36519534901 | 18 current tests, 15 inherited exact tests, 22 v16.21 tests; production and verification passed |
| Substantive schema RED | 0111d84990e93c86936f31c8d72dfce25388b6e8 | 36519735366 | Original 18 tests passed; 2 newly added malformed-parent tests failed |
| Corrected scientific GREEN | 1167e88ee38c332de27ed2d96795c036f7f521e8 | 36519952931 | 20 current + 15 inherited + 22 v16.21 tests; full production and corrected verifier passed |

The schema defect was real: Python equality allowed Boolean or floating values equal to integer parent identifiers to pass equality checks. Strict parent-type validation now precedes comparisons/caches. This repair changed neither the producer, the mathematical inputs, the criteria, nor the equations. Initial and corrected full certificate bytes are IDENTICAL. The old GREEN is not described as testing the later guards. Original archives from all four stages are retained by the publication.

The complete certificate contains 35,763 uncompressed bytes, compressed losslessly to 2,516 bytes. Raw SHA256: `59c2c2f6d1091e7102e51932ed4ee7827668d12db7f1b08ffb0724791c8df713`. Compressed SHA256: `9c7d48ba9013614567330555f3ce5bcbaf9aea93c3460d1afaf1e9e1c2ba5b3a`.

The final GitHub verification JSON SHA256 is `b4d2254cd9abedd38045bfa2c60d49ffc71b76e9e270f50e5d4eac69444f9f41`. An unchanged-source second-environment verifier run with Python 3.13.5/SymPy 1.14.0 reproduced those bytes exactly. GitHub used Python 3.11.16/SymPy 1.13.3/mpmath 1.3.0. All five final scientific command exit codes are zero. The publication run and exact durable commit are recorded separately in PUBLICATION_EVIDENCE.json.

## 7. Scope and review

Review is **self-review**. The certificate verifier is algorithmically independent, not separately authored by another person/agent. General arguments are written proofs, not proof-assistant formalizations. No global scientific novelty claim is made for standard linear or categorical constructions.

v16.21's fixed-target non-descent and constructive split-response identities remain unchanged. This stage classifies which responses obey the already-earned comparison algebra and distinguishes that class from the unique inverse of the specified operator. It does not add, remove or reinterpret old numerical results.

The next dependency for a physical claim is an independently justified physical meaning/selection of the response equation, not merely more fits or another geometry readout. Whether any further already-earned relations select across depths is not answered by pretending that re-rooting or a new arrow is already available. No such arrow or law is introduced here.

**Time is pruning / ordered recoverability update. Information first; geometry is not inserted as a target.**
