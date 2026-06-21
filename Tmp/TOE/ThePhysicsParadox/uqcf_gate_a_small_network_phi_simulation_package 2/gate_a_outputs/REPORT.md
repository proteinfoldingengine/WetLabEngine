# Gate A Small-Network Phi Simulation

## Result

This small network has:

- nodes: 5
- directed edges: 7
- rank(B): 4
- cycle dimension dim(Z): 3

Because dim(Z) > 0, bare conservation leaves an affine family:

```text
J = J0 + Z a
```

All currents in this family satisfy the same source-current law BJ=s.

## Finding 1: Bare Genesis fails

Bare Genesis/source anchoring plus conservation does not select a unique Phi. The ambiguity appears in a small graph, so it is not a compute-scale artifact.

## Finding 2: Network-only Hodge does not close canonically

For any chosen positive metric W, a minimum-action current exists. But the network alone does not choose W. Several plausible local W choices produce different currents.

This is why "Hodge exists" is not enough. A canonical Hodge metric must be derived, not selected by convenience.

## Finding 3: Observer/response closes conditionally

When the response operator R resolves the cycle space:

```text
rank(RZ) = dim(Z)
```

the hidden cycle coefficients are identifiable and Phi is selected. A rank-deficient response leaves residual gauge.

## Boundary

This simulation does not derive physical spacetime, ADM, or GR. It demonstrates a finite graph source-current identifiability theorem.
