# v15.83 — Support crossing survives; lossless loop composition does not

All frozen validity checks passed. The three scientific verdicts are:

- **SUPPORT_RESTRICTED_CROSSING_CONFIRMED**
- **SUPPORT_LOOP_COMPOSITION_OBSTRUCTED**
- **LOSSLESS_LOOP_CORE_TRIVIAL**

This is a diagnostic of the same candidate 46, lambda=-1 crossing near
ordered strength u*=0.75821740030905194884. It is not a held-out ensemble
result. v15.81's finite-window NO and v15.82's full-polar continuation
obstruction remain unchanged.

## What survives the crossing

At the critical slice, the source edge has a rank-two partial isometry V_01.
The other two edge polar factors remain regular, with smallest singular
values approximately 0.0342390 and 0.0252955. The existing triangle defines
L=V_01 O_12 O_20, based at node 0. Its initial projector P=L^T L is determined
by this retained structure; no comparison frame or plane is fitted.

The full regular loops on the two sides retain a jump of Frobenius norm
approximately 2. Restricting their input to P makes that difference converge
to zero and both restricted loops converge to L:

| Side distance in ordered strength | Before-side error | After-side error | Restricted side difference |
| --- | --- | --- | --- |
| 1e-3 | 6.2441e-4 | 2.2658e-4 | 7.8370e-4 |
| 1e-5 | 6.2437e-6 | 2.2673e-6 | 7.8372e-6 |
| 1e-7 | 6.2437e-8 | 2.2673e-8 | 7.8372e-8 |

The smallest frozen separation passes the preregistered 1e-5 criterion.
This continuity is obtained by discarding the missing input sector. It
does not restore the uncompressed orthogonal link.

Cross-slice differences use the inherited common node frames. Their norms
are invariant under a common frame rotation of root and sides, not under
independently selected frames at each slice. No realignment is performed.
Pointwise based-loop spectra are independently gauge invariant because
local endpoint frame changes conjugate L at node 0.

## Why raw composition attenuates

The loop's initial and final planes differ. Their projector commutator has
Frobenius norm 0.6001830607, and their kernel-normal squared overlap is
c^2=0.2356325533. The predicted L^2 singular values (1,c,0) are measured as
(1,0.4854199763,0).

The nonzero fractional singular value makes L^2 fail the partial-isometry
condition. Its projector defect is 0.1801098531, matching both
c^2(1-c^2) and half the squared projector-commutator norm at 80-digit
precision. The defect is far above the frozen 1e-8 obstruction threshold.
No polar decomposition or renormalization is inserted between traversals.

| Spatial loop traversals | Singular values of L^n | Norm-preserving input dimension |
| --- | --- | --- |
| 1 | (1, 1, 0) | 2 |
| 2 | (1, 0.485420, 0) | 1 |
| 3 | (0.725503, 0.324785, 0) | 0 |
| 4 | (0.370763, 0.308501, 0) | 0 |

Tiny singular values at about 1e-82 are displayed as zero in this table;
the complete values are preserved in RESULT.json. Every lossless dimension
agrees at thresholds 1e-9, 1e-10 and 1e-11, using fixed identity scale 1.
The independent stacked-constraint calculation agrees too.

For G_n=I-(L^n)^T L^n, the minimum eigenvalue of G_3 is 0.4736453890.
Cayley-Hamilton establishes that ker G_3 is the maximal indefinitely
norm-preserving subspace in dimension three. Here that subspace is trivial.
Writing r=||L^3||_2 approximately 0.7255030055 gives the analytic bound

||L^n||_2 <= r^floor(n/3),

and hence asymptotic attenuation under repeated traversal of this same
fixed loop. This bound follows from submultiplicativity and ||L||_2=1;
it is not a fitted decay law.

The powers remain nonzero and retain two substantial singular values at
all four measured traversals. A trivial isometric core does **not** mean
a zero map, rank-zero transport, or additional finite-step erasure of
all information. Attenuation alone does not establish Shannon-information
loss or prevent inversion on the surviving image. No noise or finite
measurement-resolution axiom has been added.

## What this does and does not constrain

Pointwise support restriction is sufficient to remove this polar sign jump,
but it is insufficient to make the resulting loop isometric under repeated
composition. Native support compatibility therefore matters if the desired
geometry requires lossless transport.

Linear composition is still associative and well-defined. A more general
contractive transport geometry is not excluded. These traversals compose
spatial retained links at one frozen slice; they are not further quantum
source updates or fundamental time steps. The result neither falsifies
CPTP composition nor selects a physical source law.

## Exact reproducibility evidence

Parent documentation SHA: `b7e472378b907c7ff95a44cd8611d11c7fdaa2f5`.
Preregistration/tests SHA: `83adad316a7af388956d4f5e545f767aae341f86`.
Scientific implementation SHA: `0e29f68556255869472c7bf86b998550927d108a`.
Branch: `research/v15.83-support-loop-composition`.

- [Expected RED run 36350282733](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36350282733), job `108707518365`.
  Setup passed; the missing gate.py assertion failed as preregistered.
  [Artifact 10941498489](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36350282733/artifacts/10941498489).
  ZIP SHA-256: `c89d418416336ff592050f82c1fed01d3ff39350b60da714f2359a0c46866ac0`.
- [GREEN run 36350562203](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36350562203), job `108708305465`.
  Three tests passed; the actual result JSON reports the three verdicts
  above and `all_valid: true`.
  [Artifact 10941972741](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36350562203/artifacts/10941972741).
  ZIP SHA-256: `08a994bf9701c24a66070f598050b13e0bad85e358eb7dcbb4221370958e76c2`.
- Lossless [RESULT.json](RESULT.json) SHA-256:
  `bb2299a633e857beeabce7b05208b9c924d88b3bbceb1f033f772657457c7166`.
  [SUMMARY.json](SUMMARY.json), [EVIDENCE.json](EVIDENCE.json),
  [TEST_LOG.txt](TEST_LOG.txt) and [SHA256SUMS](SHA256SUMS) accompany it.
  SHA256SUMS names the artifact's `result.json`, preserved here as `RESULT.json`.

The parent RESULT.json hash is pinned and verified:
`a60feb6ab4506e8049d72c6a4e85627ae6f9137e3509aa9da44e14f6f151df56`.
Its complete complex input is preserved. Selector and complex roundtrip
errors are zero; root source-edge identity error is 3.83e-81 or less.
This remains a calculation on the stored binary64 matrix, with inherited
trace error 8.33e-17. Root data are evaluated at the rational isolating
interval midpoint, an approximation to the algebraic root.

All quantum-state positivity/trace/Hermiticity checks passed. Projector
residuals are at most 1.69e-80, full-polar residuals at most 1.48e-80, and
Gramian reconstruction errors at most 2.11e-81. All synthetic preservation,
attenuation and nilpotent controls passed. Mathematical, implementation
and artifact-interpretation reviews found no critical or important issue.

Exact job logs, downloaded ZIP hashes, execution SHAs, frozen source bytes,
and every artifact checksum were inspected. There were no implementation
repairs or changes to scientific criteria after measurement.

Reproduce from the tested scientific implementation SHA with Python 3.11:

```sh
python -m pip install numpy==2.3.5 sympy==1.13.3 mpmath==1.3.0
cd ResearchHistory/UQCF-GEM/demos/v15.56-response-selector-obstruction/support-loop-composition
OPENBLAS_NUM_THREADS=1 python -m unittest -v test_gate
OPENBLAS_NUM_THREADS=1 python gate.py > result.json
```

The final documentation commit is separate and uses `[skip ci]`; no merge
to main is performed. Historical files and verdicts are unchanged.

## Next research boundary

The remaining question is what physical recoverability content, beyond
norm preservation of this extracted link, is carried by the contractive
transport. Its retained rank and its isometric core are different objects.
Any next claim about pruning or information loss must make that distinction
explicit rather than treating attenuation itself as physical erasure.

Geometry remains exhaust of retained structure. Genesis Pin remains
foundational. No external alignment, heuristic fitting, fundamental time,
dark-matter primitive, admissible-world modification or gravity derivation
is introduced.
