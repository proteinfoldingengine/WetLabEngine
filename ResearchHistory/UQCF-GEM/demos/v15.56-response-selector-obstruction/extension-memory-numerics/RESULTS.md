# v15.72 Extension-memory descent numerical adjudication — COMPLETE

Date: 2026-09-26. Branch: `research/v15.72-extension-memory-numerics`.

## Verdict

**EXTENSION_MEMORY_CANCELLATION_CONFIRMED**

The v15.71 historical verdict remains unchanged:

**MINIMAL_EXTENSION_MEMORY_DESCENT_NOT_CONFIRMED**

v15.72 explains why that frozen float64 full-state gate missed its relative threshold.

## Frozen reproduction of v15.71

All 52,488 float64 full-state witnesses were repeated with the same states, hidden directions, source labels, signs, edges, eta and source strength.

The v15.71 failure reproduced exactly:

- maximum full-state absolute residual: **8.780832845415946e-17**
- maximum full-state relative residual: **1.7561665690834022e-9**
- frozen v15.71 threshold: **1e-9**

Thus the historical NO is preserved rather than silently converted.

## Increment-space identity

The same source equality was evaluated before adding the ~5e-8 update to the O(1) retained density matrix.

Across all 52,488 witnesses:

- maximum increment absolute residual: **3.65836056305494e-23**
- maximum nonzero increment relative residual: **7.316721126109871e-16**

This is more than six orders of magnitude below the failed full-state relative estimator.

## 80-digit full-state arithmetic

All 1,944 nonzero matching-source cases were recomputed at 80 decimal digits with full complex transport and an independent ordered partial trace.

Maximum relative full-state residual:

**7.418301692436159e-16**

Therefore the mathematical enriched-descent equality survives when the small update is not lost in float64 state addition/subtraction.

## What was learned

The v15.71 primary miss was caused by a numerical conditioning problem:

    O(1) state + O(1e-8) source increment

followed by subtraction of independently rounded full states.

The underlying increment identity is accurate at ~1e-15 relative, and high-precision full-state arithmetic reproduces the same result.

This earns the implementation statement that the 27-coordinate hidden-fiber memory is sufficient to restore the historical source-law descent on the frozen ensemble.

Combined with the v15.71 derivation:

- the exact hidden fiber has dimension 27;
- its evaluation Gram matrix has rank 27;
- a 26-coordinate compression loses a real retained response;
- therefore 27 real coordinates are minimal among linear memories that must support the complete 27-dimensional source-label family.

Combined with the independent v15.71 rebasing result:

**REBASED_NULL_INTEGRABILITY_CONFIRMED**

the symmetric-null sector survives both enriched descent and finite base-point recomputation over the tested regular neighborhood.

## Current structural conclusion

The chain is now:

1. marginal state data alone cannot support nonzero hidden-to-retained response;
2. the missing information is exactly the 27-dimensional weight-three hidden fiber for this three-qubit source family;
3. carrying that extension memory restores descent;
4. local-frame covariance survives;
5. fixed-base composition survives;
6. rebased composition/integrability survives;
7. none of these requirements forces a polar-skew rotational response.

Therefore the next bottleneck is no longer consistency of the null construction. It is the **origin/selection law for the extension memory itself**.

A foundational source law would need to explain why this hidden extension data is physically retained/generated rather than simply appended by hand.

## Reproducibility

- parent: `b59ed3bd8a96d0578beb8686a05bc29847290dc8`
- preregistration: `59219da0e806d224f9f5cd3446eae09158d1a3e6`
- RED head: `2e183ed1cf624464ebb963fad88ce1e06a1a2459`
- RED run: `36293317249`, job `108547406405`
- tested implementation: `f9c98ef6d546e131915fd93dd2c8a4ceae37c8c5`
- GREEN run: `36293385899`, job `108547602311`
- artifact: `10922783627`
- artifact SHA-256: `8234ebba8bcf3363ef42b196ee0cd7054121125ec25951bf53158fa42105f5a2`

## Boundary

This does not derive gravity or establish that 27 hidden coordinates are fundamental physical variables. The 27-D minimality statement is relative to the complete linear weight-three source-label family in the frozen three-qubit model.

The next experiment should ask whether a canonical higher-incidence/extension object already present in the global consistency structure can generate this memory covariantly, rather than postulating it as external metadata.
