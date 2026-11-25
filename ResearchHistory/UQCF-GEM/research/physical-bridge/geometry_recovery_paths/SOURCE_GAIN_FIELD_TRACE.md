# The missing grade contrast can survive as a retained potential difference

The full post-pruning numerical P1 vector was identical in the five matched preparations of the [source-gain experiment](FIXED_GEOMETRY_SOURCE_GAIN.md). An older computation preserves their difference by first solving a field on the fine chart and then averaging that field onto pruning fibers. On this example the returned chart-0 field gains an exact root-to-branch contrast equal to half the change in the grade transferred by the source. Chart 12's recovery caller reads a separate work table. No call between those two software outputs has been identified here.

## Exact calculation

The pinned v15.56 Task 30 functions use the unweighted tree Laplacian L, subtract the arithmetic mean of the numerical source, and return a mean-zero potential from a pseudoinverse. They also implement fiber summation of sources and counting-fiber averaging of potentials followed by recentering. Its original run compares the direction of the averaged fine solution to the direction of a fresh coarse solution. The four original small examples were run unchanged under call-through observers. In all four the solver takes the actual returned pushed source, the averaging function takes the actual returned fine potential, and the direction comparison takes the actual returned mean field. The original four-case verdict is SYSTEMATIC_MISMATCH; the archived finding receives credit.

We then applied those unchanged numerical functions in the same sequence to the supplied chart-0 source vectors of the 25-chart geometry fixture. This is a replay on new inputs. The fine source chart has 1,308 addresses, the retained chart has 1,307, and only the root leaf T is removed. Let s be its fine grade and d=s−2 its difference from the archived value. The change of the fine numerical source is d(e_T−e_o), which has zero total. Since T has only one edge, L e_T=e_T−e_o. The change of the fine potential therefore equals d e_T modulo an additive constant.

| Retained computation on the actual chart-0 carriers | Change of root potential relative to any other retained address |
| --- | --- |
| Sum the grade by P1 and solve on the retained chart | 0, since the whole retained numerical source agrees |
| Restrict the fine solution to retained addresses | 0, since T is the only site with a relative fine change |
| Average the fine solution on each pruning fiber, then recenter | d/2, since the root fiber contains o and T and every other fiber is a singleton |

Recentering preserves each potential difference. The normalized mean fields also differ for every nonzero d on this family. The two nonroot addresses (3) and (3,4) have unequal potentials, and their mutual difference is fixed across preparations. Two proportional centered mean fields would therefore have proportionality factor 1, which contradicts the changed root contrast.

| Source grade s | Exact change in the retained mean-field contrast | Historical projective discrepancy on these inputs |
| --- | --- | --- |
| 2 | 0 | 0.002265928331 |
| 2/5 | −4/5 | 0.010644034056 |
| 14/5 | 2/5 | 0.001924309318 |
| 14/17 | −10/17 | 0.008426319205 |
| 46/17 | 6/17 | 0.001431620165 |

The discrepancy is the distance between the two unit-normalized field vectors. Its five listed values are distinct. We establish no global one-to-one calibration for that scalar. The exact root contrast has the stated linear formula.

## Scope and checks

The two rooted solves were independently reconstructed with rational subtree flows. At every coordinate the exact potentials satisfy the corresponding Laplacian equations, and the historical NumPy 2.3.5 outputs agreed with the exact fields, summed grades, restriction and scalar within the frozen absolute tolerance of 1e-8. The complete input vectors and carrier identities are preserved in the source-gain universe. The field evidence includes the actual numerical errors.

The counting-fiber mean is the specific convention implemented by v15.56 Task 30. Literal retained restriction erases this contrast. The freshly solved post-P1 field is a genuine software consumer of the pushed numeric array and is identical on these matched preparations. The fine-to-mean route preserves an additional event-dependent numerical difference at a retained address of the source chart. Preparation, inherited diagnostic invocation, identification of a local observer and acquisition by another chart are distinct assumptions. No physical field or gravity identification follows from the choice of mean.
