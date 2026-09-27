# v15.90 — the Choi ceiling does not extend unchanged to arbitrary inputs

The frozen gate returned:

- **UNIVERSAL_INPUT_NEGATIVITY_BOUND_CONFIRMED**
- **CHOI_CEILING_EXTENSION_FALSIFIED**
- **OPTIMAL_LINEAR_NEGATIVITY_CONSTANT_CONFIRMED**

`all_valid` was true. All three tests, eight new exact symbolic checks, 22 inherited exact checks and 114 state/channel rows passed their prescribed adjudication. No implementation repair or postmeasurement criterion change was needed. The falsification is a valid scientific NO to a broader proposition; it does not revise v15.89's Choi theorem.

## Earned distinction

For a qubit CPTP channel with linear Bloch part T and delta=s_min(T), v15.89 proves N(J/2)<=delta/2. Its input is maximally entangled. For arbitrary finite reference/input states, the bound established here is

    N((id_R tensor Phi)(rho_RQ)) <= min(delta,1/2).

The coefficient 1 in the uniform linear inequality N_out<=delta is optimal over all such channels and input states. This does not mean the bound is attained for every fixed nonzero delta, or that the experiment globally optimized inputs for each channel.

For pure two-qubit inputs there is a more informative statement:

    N_out <= delta lambda_max(rho_reference).

The largest Schmidt weight equals 1/2 for a maximally entangled input, recovering the Choi ceiling. It can exceed 1/2 for other inputs. The output bound changes even though the channel is unchanged.

## Proof and reproducible certificate

Write a pure input as (A tensor I)|Omega>, with Tr(A^dagger A)=2. The v15.89 operator inequality J^Gamma>=-delta I gives

    rho_out^Gamma >= -(delta/2)(A* A^T tensor I).

Using the at-most-one-negative-eigenvalue property of a two-qubit partial transpose gives the Schmidt-dependent bound. Every pure state of a finite reference and a qubit has Schmidt rank at most two, so a reference isometry reduces it to this case. Convexity extends the uniform bound to mixed inputs; the standard qubit maximum negativity of 1/2 supplies the cap. [DERIVATION.md](DERIVATION.md) gives the argument and limits.

The universal claim follows from this proof, not from the finite sample. The new exact certificate independently verifies the damping output, its partial transpose and characteristic polynomial, Kraus trace preservation, the stationary negativity equations, the strict Choi-ceiling gap identity, and the limiting coefficient. Twenty-two inherited coefficient/norm/Bell checks are recomputed.

The numerical audit uses direct channel block action, independent filter reconstruction for pure inputs, independent Kraus reconstruction for damping channels, and explicit mixed-state convexity controls. Normalized-state negativity is summed directly over negative PT eigenvalues, without the extra factor of 1/2 used to normalize an unnormalized Choi matrix.

## Counterexamples and asymptotic coefficient

For amplitude damping, q=1-gamma and delta=q. The prepared family is sqrt(1-p)|00>+sqrt(p)|11>. Its analytic family optimum is

    p*=sqrt(q)/(1-q+2sqrt(q)),
    N_out=q/(1-q+2sqrt(q)).

| q=delta | Choi-input negativity q/2 | Family-optimum output negativity | Excess over Choi ceiling | N_out/delta |
|---|---:|---:|---:|---:|
| 0.5 | 0.25 | 0.261203875 | 0.011203875 | 0.522407750 |
| 0.25 | 0.125 | 0.142857143 | 0.017857143 | 0.571428571 |
| 0.01 | 0.005 | 0.00840336134 | 0.00340336134 | 0.840336134 |
| 0.0001 | 0.00005 | 0.0000980488283 | 0.0000480488283 | 0.980488283 |
| 0.000001 | 0.0000005 | 0.000000998004988 | 0.000000498004988 | 0.998004988 |

The prescribed q=0.5 and q=0.25 witnesses exceeded the old ceiling by more than the frozen 1e-4 margin. All 14 damping rows, including q=0 and q=1 endpoints, matched the analytic formulas. At q=0 the ratio is not evaluated; the output negativity is zero. At q=1 both inputs reduce to the maximally entangled optimum with negativity 1/2.

The exact ratio 1/(1-q+2sqrt(q)) tends to 1 as q decreases to zero. Therefore any constant c<1 fails as a universal coefficient in N_out<=c delta. The finite ratio ladder checks the implementation; the exact limit supplies the sharp-coefficient argument. No optimizer or fitted coefficient was used.

## Native inputs and numerical validity

All 25 stored v15.89 channels were reevaluated in their original coordinates. Each received three pure inputs with p=0,0.25,0.5 and phase i, plus the prescribed mixed input. These 100 rows test complex transport and convexity. Fourteen canonical damping rows complete the 114-row gate. All 32 channel occurrences passed CPTP checks, and all prepared input/output states passed physicality checks.

The 25 p=0.5 inputs matched their archived Choi negativities within 2.90e-81. Maximum archived channel discrepancy was 1.01e-80 (rounded upward); maximum identity/reconstruction residual was 4.22e-81; maximum damping formula discrepancy was 3.69e-81. The damping delta reconstruction error was zero. Every measured PT had at most one eigenvalue below -1e-40.

Minimum signed uniform-bound slack was -4.22e-81; minimum Schmidt-bound slack was -5.28e-81; minimum operator-bound eigenvalue was -4.22e-81 (upward rounding of magnitudes). Minimum mixed-state convexity slack was zero. Minimum physical-state eigenvalue was -5.28e-81. These roundoff residuals are far inside the frozen -1e-40 allowance. Raw eigenvalues/slacks are preserved, with no classification clipping or adjusted thresholds.

## Prior art and interpretation boundary

The advantage of nonmaximally entangled inputs for amplitude damping is established quantum-information theory. [Streltsov, Augusiak, Demianowicz and Lewenstein, PRA 92, 012335 (2015)](https://arxiv.org/abs/1412.5885), Section IV.C and Eq. (67), gives the same analytic family optimizer. That paper uses twice our negativity normalization and also discusses logarithmic negativity; the input ordering and optimizer are unchanged. This gate reproduces that known effect and connects it to the certified weakest-transmission bound. No novelty or priority claim is made.

The reference filter is a mathematical representation of a prepared input, not a physical postselection step attached to the channel. The canonical damping controls do not supply an external alignment mechanism for emergent geometry. The universal proof permits arbitrary finite reference dimensions; numerical examples here use a two-dimensional reference.

These results concern negativity after one channel use. They are not a quantum-capacity formula, a source-to-admissible-world law, or a gravity derivation. They complete the input-choice/normalization check for the conditional channel interpretation; physical source-law selection and the original polar-skew response mechanism remain separate open questions. Geometry has not been introduced as an explanatory primitive. Time remains pruning/ordered recoverability; Genesis Pin and all historical verdicts remain intact.

## Exact provenance

- Branch: `research/v15.90-arbitrary-input-negativity`.
- Certified parent: `44ca8cf73e39ef1e66fda684ddabdf0ce6a1d5bf`.
- Preregistration, derivation, tests and workflow: `7ad9f297e19b91c56950a38f372c621d71373fa7`.
- Expected RED: [run 36359794738](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36359794738), job `108734554317`, artifact `10945017861`. Setup succeeded; the explicit missing-implementation assertion failed.
- RED ZIP SHA-256: `9d18711a8bca954b1f3b454de8e17041c9ed5f4dda1f7aa2e2bc32e83250c8ae`.
- Tested implementation: `08631fa1c2002032d0c310cc058ccc27d62af222`.
- GREEN: [run 36359958996](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36359958996), job `108735040770`, [artifact 10944883691](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36359958996/artifacts/10944883691).
- GREEN ZIP SHA-256: `70d9deff56328d86af9c00f402e091d5f44565d4b7467145da8dd0a9b1e57c2c`.
- Lossless [RESULT.json](RESULT.json) SHA-256: `1d32ccbeb45912540b5eacceb5c0f1d0ca596873fe20265c2c80168adb20a7d4`.

Both exact job logs and downloaded ZIP artifacts were inspected. ZIP digests, execution heads, frozen preregistration/derivation/test bytes and tested implementation bytes were verified. Every GREEN SHA256SUMS entry matched; parsed job-log scientific JSON was identical to the artifact JSON. SHA256SUMS retains the artifact filename `result.json`, published here unchanged as `RESULT.json`. [EVIDENCE.json](EVIDENCE.json) records machine-readable provenance. Documentation is an additive follow-up commit. No merge to main.
