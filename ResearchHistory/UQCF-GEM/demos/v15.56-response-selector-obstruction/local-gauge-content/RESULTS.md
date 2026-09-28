# 16.13 — Local gauge content of the continuous normal response

Completed 2026-09-28. **LOCAL_NORMAL_SIGN_GAUGE_CLASSIFIED.** All scientific validity controls passed. The local normal sign is removable by a proper endpoint-frame rotation in **90 of 144 cases**. The remaining **54 cases** have an exact SO(3)-invariant orientation witness, but it depends on the tiny rank-two baseline component and collapses at the rank-one boundary. Gauge-invariant amplitude differences distinguish all 48 nonidentity order pairs.

This narrows the revised program: a signed matrix response is not automatically a locally invariant sign. The next network test must establish whether additional intrinsic edge information supplies a meaningful reference. The small rank-two determinant witness is not evidence of a robust physical canary.

## Frozen inputs and gauge

The inputs are all 144 normalized physical path families from 16.12: 12 candidates, three inherited binary middle-channel parameters a, two preparation arms and two orders. C is the sixth-edge baseline connected matrix; N=N+ is its projected normal derivative at source coherence +1. At general coherence the normal derivative is λN and vanishes at λ=0.

Independent unitary changes of local Pauli frames induce **SO(3)×SO(3)**: C→GCHᵀ and N→GNHᵀ. We also report O(3)×O(3) as an explicitly larger comparison group. Reflections are not silently treated as proper physical frame rotations.

The classification concerns only the local pair **(C,N)**. It does not classify complete physical paths, tangential responses, neighboring edges, global states or source channels.

## Exact sign-orbit result

Let P=CC⁺ and J=2P−I. Every exact case satisfies JᵀJ=I, JC=C and JN=−N. This witness is constructed from the baseline projector without choosing a frame or an alignment.

| Preparation | Baseline rank | Normal rank | Cases | Local sign under SO(3)×SO(3) |
|---|---:|---:|---:|---|
| Plane | 1 | 1 | 72 | Equivalent; proper sign-flip witness |
| Isotropic | 1 | 2 | 18 | Equivalent; proper sign-flip witness |
| Isotropic | 2 | 1 | 54 | Distinguished by an odd determinant coefficient |

At rank one, det J=+1. Thus every invariant function of this local pair must agree on N and −N, not merely the particular invariants sampled in the audit.

At rank two, det J=−1, so that witness is improper. Here

`det(C+tN)=t alpha`, with `alpha=cof(C):N ≠ 0`.

Determinant is unchanged by independent proper endpoint rotations, so its odd coefficient distinguishes the two signs. At rank one with normal rank two, the determinant pencil instead has the sign-even form t² beta; for the planar cases it vanishes identically.

All 144 signs become equivalent under the larger O(3)×O(3) group. Therefore a downstream construction that admits full O(3), rather than proper Pauli-frame rotations, cannot use this local orientation witness as an invariant sign.

## Check against actual physical paths

The normal pencil C+tN is a diagnostic, not a claim about a physical density path. The audit separately used the actual coefficients of

`C(s,λ)=C+s(V0+λV1)+s²(W0+λW1+λ²W2)`.

For every case, the first s-coefficient of its determinant is λ alpha. For every rank-one case, the second s-coefficient is λ² beta. These were checked by exact polynomial algebra. Thus the orientation conclusions are tied to the actual derivatives without declaring the normal pencil itself to be a CPTP path.

## Amplitude remains invariant

The scalar ||N||F² is invariant and sign-even. All 72 before/after pairs satisfy N_before=a N_after and therefore

`||N_before||F²=a² ||N_after||F²`.

All **48 nonidentity pairs** have unequal amplitude coefficients. All **24 identity-middle pairs** coincide. The actual normal-energy coefficient is λ²||N||F²; at zero coherence it vanishes. Losing an isolated sign does not erase the magnitude distinction, but magnitude alone cannot restore that sign.

## Spectral-edge qualification

The orientation-sensitive cases have baseline rank two only through a very small second singular direction. No input was truncated or repaired. We measured the unnormalized witness and its spectral dependence:

| Rank-two quantity, absolute values | Minimum | Maximum |
|---|---:|---:|
| alpha | 6.9695470e-32 | 9.6792565e-26 |
| ||cof(C)||F | 8.2291563e-27 | 1.0256767e-22 |
| |alpha| / (||C||F² ||N||F) | 5.3194371e-15 | 1.4943759e-14 |
| sigma2 / sigma1 | 5.3194371e-15 | 1.4943759e-14 |

The last two ranges agree to the shown precision, not as an asserted exact equality. The controlling bound is

`|alpha| ≤ ||cof(C)||F ||N||F`, and at rank two `||cof(C)||F=sigma1 sigma2`.

Hence the normalized sensitivity is at most sigma1 sigma2/(sigma1²+sigma2²), which tends to zero at the rank-one boundary. The diagonal regression C=diag(1,epsilon,0), N=diag(0,0,1) gives alpha=epsilon exactly and alpha=0 at epsilon=0.

Exact high-precision certification does not establish experimentally resolvable orientation information. Dividing out this small cofactor would normalize away the very fragility being tested. This loop therefore does not promote the rank-two sign witness as a robust physical signal or use it to select a source.

## Execution and numerical evidence

[Successful targeted run 36499944642](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36499944642), job 109188146634, executed scientific commit **`1a9d5d80f80385af2ba1771cadd21c5a4f8f976b`**. Five new tests and five parent tests passed, followed by the complete exact and numerical audit.

The result contains 144 exact records, 72 amplitude-order comparisons, and **576 numerical rows** at 80/120 digits in both inherited proper frames. No numerical threshold determines rank.

| Control | Maximum absolute residual |
|---|---:|
| Stabilizer identities and parity | 4.9708e-81 |
| Proper-frame identities | 1.5628e-81 |
| Cofactor covariance | 2.0874e-89 |
| Determinant coefficient identities | 3.6818e-91 |
| Normal amplitude identity | 3.2172e-86 |
| Invariant quantities across frames | 9.2145e-82 |
| Cofactor/singular-product identity | 4.0592e-89 |
| Numerical excess over Cauchy bound | 1.0900e-106 |
| Cross-precision discrepancy | 1.0576e-81 |

All meet the frozen tolerances, 1e-35 within precision and 1e-30 across precision. The tiny numerical Cauchy excess is within rounding error; the exact bound is mathematical.

Preregistered head `21f1e46234433607e071d231b602191c4ca778c0`, [RED run 36499547746](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36499547746), produced the five expected absent-implementation failures. A local syntax error was corrected before measurement; no protocol, source, input or tolerance changed. Independent pre-measurement review passed all tests and found no blockers.

## Complete publication

[Full raw result](result.json.xz): **3,311,171 uncompressed bytes**, losslessly compressed to **344,204 bytes**. It includes every exact matrix, stabilizer, determinant coefficient, physical-path coefficient, amplitude comparison, numerical matrix, singular value and control. This is not an Actions-only archive or a summary.

[Evidence](EVIDENCE.json) binds the scientific commit, run, artifact digest, metrics and hashes. [Independent verification](PUBLICATION_CHECK.json) checks all 144 stabilizers and determinant pencils, all 144 full physical determinant polynomials, all 72 amplitude pairs and every numerical record key. [The verifier](verify_publication.py) uses column-basis projectors and a direct six-term determinant formula instead of the audit's pseudoinverse and coefficient extraction routines.

Protocol, derivation, review, source manifest, code, tests and complete execution/RED logs accompany the result. Decode using `xz -dk result.json.xz`, verify `sha256sum -c SHA256SUMS`, then run `python verify_publication.py`. `SHA256SUMS-xz` checks compressed bytes. The artifact digest and executed-source/raw-result hashes were verified before publication.

## Consequence for the revised brief

16.12 retained continuous response information. 16.13 now separates its invariant amplitude from its local sign orbit. For the rank-one cases, any signed invariant needs additional intrinsic data beyond (C,N); neighboring edge structure is one candidate, whose usefulness remains to be measured. The tiny rank-two orientation exception must not bypass spectral-edge controls.

The next 16.14 test should examine predeclared closed-network traces, separating the full physical response from its normal contribution, with identity, zero-coherence, reversal and frame controls. It may find exact cancellation. A surviving invariant would still require the 16.15 interpretation gate; invariance alone is not curvature or gravity.

The source family is specified, not derived. The original five-edge null and polar boundary obstruction remain unchanged. Time is pruning / ordered recoverability update. No external alignment, fundamental time, fitted completion, dark-matter primitive or gravity law is introduced.
