# Polar/Sylvester origin of rank-three response — preregistration

Frozen after the generic mixed-orthogonality explanation failed.

Question: is the 243-to-3 PURE_SKEW image already imposed locally by the differentiated polar/Sylvester map, or does rank collapse occur only after the three edge responses are assembled into loop holonomy?

For every one of the same 11 states and all 27 hidden x 9 source basis pairs, use the existing closed-form chain to retain the three edge-level mixed polar responses O_es together with first responses O_e and O_s.

At each edge left-translate the mixed response by O^T and decompose its 3x3 matrix into trace, skew, and symmetric-traceless sectors. Build the complete edge response operators and the combined three-edge operator before holonomy multiplication.

Measure:
- rank of each edge mixed-response operator;
- rank of the direct-sum three-edge operator;
- rank of each edge skew projection and non-skew projection;
- whether the final loop rank-three image can be reconstructed from only edge skew components;
- whether non-skew edge components cancel only during loop assembly;
- singular spectra and nullities at each stage.

Controls:
- exact reconstruction of the previously certified loop K from retained edge terms <=1e-10 relative;
- basis-change invariance of ranks/spectra <=1e-8;
- no finite-difference response columns and no fitted parameters.

Verdicts:
LOCAL_SYLVESTER_RANK3 if every edge operator is already rank <=3 and final response is reconstructed from its local skew image.
LOOP_CANCELLATION_RANK3 if edge/direct-sum rank exceeds 3 but loop assembly cancels to the certified rank-three PURE_SKEW image.
HYBRID_POLAR_LOOP_REDUCTION if local reduction exists but additional loop reduction is required.
NO_STABLE_ORIGIN if none of the above is stable across all fixtures.
INVALID if controls fail.

This gate localizes the algebraic origin of the certified rank-three response. It does not assign physical gravity meaning.
