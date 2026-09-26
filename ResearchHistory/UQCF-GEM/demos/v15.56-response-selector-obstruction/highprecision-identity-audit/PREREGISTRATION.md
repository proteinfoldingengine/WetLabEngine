# v15.67 High-precision identity audit — preregistration

Date: 2026-09-26.

## Purpose

Locate the first semantic divergence between the float64 v15.64 path and the 80-digit v15.66 path. This is an implementation audit, not a physics test.

## Frozen case

Use asymmetric candidate index 13 only.

Freeze:
- hidden sign +1;
- source sign +1;
- eta=1e-4;
- t=1e-3;
- v15.64 XXX hidden tangent and global symmetric-null Y.

Construct the same finite corner in both implementations.

## Layer-by-layer comparisons

A. State matrix:
- max absolute entry difference after converting high precision to float64;
- trace;
- minimum eigenvalue (float64 diagnostic).

B. For every site and Pauli axis:
- one-body expectation values.

C. For every edge and axis pair:
- raw two-body expectation;
- connected correlation C_ab = <sigma_a sigma_b> - <sigma_a><sigma_b>.

D. For each edge:
- C^T C;
- eigenvalues of C^T C.

E. Polar factor:
- float64 SVD polar factor;
- high-precision formula O=C(C^TC)^(-1/2), converted to float64;
- Frobenius difference;
- orthogonality and determinant.

## Frozen tolerances

State/moment/C agreement <=1e-13 after conversion.
C^TC eigenvalue agreement <=1e-12 relative.
Polar-factor agreement <=1e-11 Frobenius.

Verdict is the first failing layer:
STATE_MISMATCH
MOMENT_MISMATCH
CORRELATION_MISMATCH
GRAM_MISMATCH
POLAR_MISMATCH
PATHS_IDENTICAL_AT_FROZEN_CORNER
INVALID

No tolerance is changed after execution.

## Follow-up rule

If a layer fails, fix/audit only that layer before rerunning the full v15.66 high-precision adjudication. Do not reinterpret v15.66 until identity is restored.
