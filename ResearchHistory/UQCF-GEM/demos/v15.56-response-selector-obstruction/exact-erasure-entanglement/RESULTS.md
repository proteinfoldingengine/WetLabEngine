# v15.88 — exact qubit erasure breaks entanglement; small transmission can survive

The frozen gate returned **EXACT_ERASURE_ENTANGLEMENT_BREAKING_CONFIRMED** and **SOFT_ERASURE_ENTANGLEMENT_SURVIVES**, with `all_valid: true`. Three tests and all eighteen exact symbolic checks passed. One implementation-only defect was repaired without changing preregistration, tests, amplitudes, or thresholds.

## Earned conclusion and prior art

Every qubit CPTP map whose linear Bloch part has a nonzero kernel is entanglement breaking, including nonunital maps. This is an **established quantum-information result**, explicitly stated for plane/line images in Horodecki, Shor and Ruskai (2003), not a novel theorem claimed by this program. v15.88 supplies a reproducible algebraic certificate and applies it to the inherited retained-loop maps beyond v15.87's chosen optimum.

In coordinates where the erased direction is Z, the third column of T vanishes. The Choi matrix then obeys

    J^(Gamma_input) = (X tensor I) J (X tensor I).

The implementation verifies this identity on all ten independent affine coefficients, including all three translation components. The input partial transpose is therefore positive whenever J is positive. For the two-qubit Choi state, PPT implies separability; separability of that state is equivalent to an entanglement-breaking channel. The universal result follows from this exact algebra and the established equivalences, not from six examples passing.

Sources, inspected before preregistration:

- [Horodecki, Shor and Ruskai, Entanglement Breaking Channels (2003)](https://arxiv.org/html/quant-ph/0302031v2): introduction and Theorem 4.
- [Horodecki, Horodecki and Horodecki, Separability of Mixed States: Necessary and Sufficient Conditions (1996)](https://arxiv.org/abs/quant-ph/9605038): PPT sufficiency for 2x2 and 2x3 states.

## Native exact-erasure controls

All six frozen native maps were CPTP and PPT: two nonunital plane channels, a unital plane channel, the v15.87 optimum, a nonunital line channel, and a complex Pauli-Y replacement channel. Their Choi and input-partial-transpose spectra matched within 5.28e-81. Kernel-pair output distances were at most 1.35e-81; normalized Choi negativity was at most 5.79e-82. These are numerical zeros supported by the exact certificate.

The direct-coordinate reflection construction A=(I-2nn^T)diag(1,-1,1) was proper orthogonal and satisfied TA=TF within the frozen tolerance. Maximum reflection/rotation identity error was 3.59e-80; maximum affine/partial-transpose reconstruction error was 2.64e-82. Parent matching error was 5.28e-81. The minimum tested state eigenvalue -2.54e-81 was roundoff within the -1e-40 positivity tolerance. No eigenvalues were clipped for CP/PPT classification.

## Exact erasure cannot be replaced by a numerical rank cutoff

For the frozen family T_epsilon=L/2+epsilon cof(L), the retained-plane action stays fixed while the missing-direction transmission becomes epsilon. Every tested row was CPTP.

| epsilon | Minimum unnormalized Choi PT eigenvalue | Normalized Choi negativity | Entanglement breaking |
|---|---|---|---|
| 0 | numerical zero, -1.16e-81 | numerical zero, 5.79e-82 | Yes |
| 0.01 | -0.005 | 0.0025 | No |
| 0.0001 | -0.00005 | 0.000025 | No |
| 0.000001 | -0.0000005 | 0.00000025 | No |

The minimum singular value, kernel transmission norm and antipodal kernel-pair output distance all equal epsilon within 1.35e-81. The eight exact Bell eigenvector checks establish the analytic Choi and partial-transpose spectra, giving negativity epsilon/4 for every 0<epsilon<=1/2. Thus entanglement can survive arbitrarily close to this exact-erasure boundary. The finite ladder corroborates that formula; it does not by itself prove the arbitrarily-small statement.

There is no uniform positive “almost erased implies entanglement breaking” tolerance near this boundary. This does not assert that every nearly singular channel preserves entanglement or that all entanglement-breaking channels lie on a singular boundary. The full-rank depolarizing control T=I/4 was CPTP and PPT, so the converse of the exact-erasure theorem is false. Identity and amplitude damping at gamma=1/2 were CPTP and NOT_PPT, confirming that the gate detects surviving entanglement. Synthetic formula/Kraus errors were at most 2.11e-81.

## Implementation failure, preserved separately

The first implementation run ended with `TypeError: Cannot set values of ImmutableDenseMatrix` in the symbolic partial-transpose helper. SymPy's Kronecker-product matrices remained immutable after `.copy()`. It produced no result JSON or scientific verdict. The numerical gate was not redefined.

The repair changed exactly one line: symbolic inputs are copied into `sp.MutableDenseMatrix`, while mpmath inputs retain their existing copy behavior. Tensor indices, tests, equations, precision and thresholds were unchanged. The same tests then passed. The failed run and its artifact remain recorded below. A local dependency probe could not run because scratch Python lacked SymPy; the authoritative regression failure and successful fix were both observed in pinned GitHub Actions environments.

## Exact provenance

- Branch: `research/v15.88-exact-erasure-entanglement`.
- Certified parent: `38c675b1af1c9df6b926adc5d243d0a889d00f93`.
- Preregistration/tests commit: `0273837380318b8e8c5a14c302f35bb894b262b4`.
- Expected RED: [run 36356769061](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36356769061), job `108725943801`, artifact `10944501750`. Setup passed, explicit absent-implementation assertion failed.
- RED ZIP SHA-256: `6816d0be4753d40eb5a3f9ba279f9f52e00de54bfcfe3502d00cf52e56caa50c`.
- Initial implementation: `d1ec89f8d8fb68761220cee94ea1bf141106cd58`.
- Implementation-error run: [36357008287](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36357008287), job `108726645061`, artifact `10944531988`.
- Implementation-error ZIP SHA-256: `9771620c8bbe0161f4257ea5ec71db3fc53f901e4f0bb1d2649193303a184dd4`.
- Corrected, tested implementation: `1f4e3b51b3a9bda35b5f0fb4177a004c09cedf0f`.
- GREEN: [run 36357109323](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36357109323), job `108726936941`, [artifact 10944293246](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36357109323/artifacts/10944293246).
- GREEN ZIP SHA-256: `d8e2e989a656d93329edb7e18bae0870c0bc615e0560896bfc999707155f1af6`.
- Lossless [RESULT.json](RESULT.json) SHA-256: `06295e1705c9c38567ee8dc1bee10a737b0d9a8b260200867a68d01fc10130ab`.

All three exact logs and downloaded artifacts were inspected. ZIP digests, execution heads and frozen document/test bytes were verified; the repair was compared against the failed artifact and was exactly the one matrix-construction line. All GREEN SHA256SUMS entries and scientific JSON verdicts were verified. SHA256SUMS retains the artifact filename `result.json`; those same bytes are published here as `RESULT.json`. Documentation is a subsequent additive commit.

## Interpretation limits

Entanglement breaking destroys entanglement between the channel output and any external reference; it does not erase all classical distinguishability or forbid rotational statistics. This result concerns qubit input/output channels. It is not a theorem about arbitrary-dimensional quantum pruning, nor evidence that every retained geometric map must be implemented as a physical channel.

The original source-law problem remains open. No source acting on a state has thereby been shown to change admissible worlds, and no gravity law has been derived. The relation between small residual transmission and quantitatively bounded surviving entanglement is a subsequent question; v15.88 provides a family and an exact boundary, not a universal quantitative bound away from that boundary.

No fundamental time, foundational heuristic fit, external alignment, or dark-matter primitive was introduced. Genesis Pin and all historical scientific verdicts remain intact. No merge to main.
