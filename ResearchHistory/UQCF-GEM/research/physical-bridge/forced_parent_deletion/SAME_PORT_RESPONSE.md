# Response at two sites that exist in both comparison arms

The previous tree test gave zero change in coupling when a chart acquired a terminal leaf. We looked for an operation that can change the coefficient relating a probe at one existing site to a readout at another. The V1687.16 executable contains such a comparison in its own vector space. A separate composition of record pinching with a joint response probe shows why the order and physical availability of the probe also matter. These are distinct calculations. No map between their inputs, or from the earlier v16.48 event, is used.

## Historical outer operation with a changed response

The [archived V1687.16 script](../../../../../Tmp/TOE/Einstein_13_V1720%20retained_bridge_core/History/H4_rock_test/v1687_16.py), blob 090a03bf665b97d7784f688c8294a348ad20507f, uses twelve cyclic coordinates. Its native operation is

    R_i(x,q;γ) = x_i + q_i + γ(x_{i−1} q_i − x_i q_{i+1}).

The original top-level build_base() uses its default seed 1 to produce four fixed inputs and a gate dictionary. The script separately uses seed 168716 in other audits. The original bracket4_all evaluates both B3 and B4. In both arms the outer operation has left input J1 and gate γ=3. The right inputs are produced internally:

    q3 = R(R(J2,J3;g23), J4;g234)
    q4 = R(J2, R(J3,J4;g34);g234)

Here g23=2/3, g34=8/7 and g234=1. B3 and B4 name bracketings. Their coordinates are existing slots in the program, without a derived spatial interpretation. The computation enumerates both histories. It does not select one as an actual event.

To measure response, subtract the output of the same arm at zero probe and divide by the signed probe magnitude. Use +h at coordinate 2 and −h at coordinate 10, keeping the total input fixed. The compensating site is outside the output-3 stencil. For any h≠0 the result at 3 is γq_3, where the subscript 3 now denotes the **coordinate** of the right input. The right inputs from B3 and B4 have values −21 and −90 at that coordinate:

| Same probe and readout | B3 | B4 | B3 minus B4 |
|---|---:|---:|---:|
| Unprobed output at 3 | 42 | 180 | −138 |
| Probe response at 3, per unit h | −63 | −270 | +207 |
| Probe response at 2, per unit h | 64 | 271 | −207 |

Both unprobed values were subtracted. The nonzero slopes already existed in each arm. The comparison changes their strength. For example, input h=1/2 gives baseline-subtracted responses −31.5 and −135 at the same output. The full response difference obeys

    ΔJ_ij = γ(s_i δ_{j,i−1} − s_{i+1} δ_{j,i}),   s = q3 − q4.

Each column sums to zero. All 144 entries were reconstructed using independent rational coordinate arithmetic and checked by applying the original bracket function to unit input changes. Finite signed balanced probes and the native default floating-point inputs also reproduce the displayed slopes. With the same effective right input, the difference matrix vanishes. With all three inner gates set equal to 1, the difference at 3 is still 207. At equal inner gates of 0, 1/2, 1 and −1 it is 0, 207/4, 207 and 207 respectively. The outer gate stays 3 in these controls. The recombination product's bilinear correction makes the common-gate associator quadratic in that gate: linear terms cancel by bilinearity. The exact response difference has rank 10 on the default gates and rank 8 in the matched-unit control. Its nonvanishing survives a common invertible change of input basis and a common invertible change of output basis across the arms. The individual coefficient 207 refers to the specified coordinates and scales.

The original caller consumes the recombined inner amplitude in the outer operation. The balanced probes and gain comparisons were added in this study. A physical receiver, a physical bracketing selection, identification of chart leaf 9 with a vector input, and units of force or curvature remain open.

## Logical susceptibility of a surviving record

A separate test connects two original functions. V15.16's reduce_input implements a **supplied** sharp record pinching in the completed encoding basis. Its original audit enumerates all five schedules and sixteen masks. V13.27's bkm_covariance computes the derivative of an expectation value in the normalized family exp(log ρ+hP)/Tr exp(log ρ+hP), at h=0 for a faithful state. Its default geometry_snapshot uses one-site reductions and Pauli probes. The combined call and the two-record covariance below are our tests. Neither historical caller hands a v15.16 output to v13.27 as an autonomous physical probe.

For ρ=(I+xX)/2 with |x|<1 and a surviving ±1 observable Z, the native logarithmic mean at eigenvalues (1±x)/2 gives χ_before=k=x/atanh x, with k=1 at zero. After dephasing Z the state is I/2 and χ_after=1. Ordinary Z outcome probabilities and undriven mean and variance are identical. At x=3/5 the response change is 0.134382975. Applying the tilt before pinching gives the old slope because the pinching fixes Z. A fresh tilt of the pinched state gives the new slope. This calculation concerns a declared equilibrium-style drive of fixed dimensionless strength.

The actual default v15.16 fixture has minimum input eigenvalue 0.00625. For each of its five schedules and sixteen masks we compared all four logical one-record reductions. All 160 pinched-bit probes had positive changes, repeating four values by record. All 160 unpinched-bit probes had zero change within tolerance. The nonzero values rounded to nine decimal places are 0.004358008, 0.217265277, 0.169769780 and 0.092825992 in A1,A2,B1,B2 order. These are repeated comparisons on one historical fixture. The BKM evaluation is a new diagnostic. Both single encoded copies are already diagonal in the output record basis before pinching. Pinching the completed joint encoding leaves each copy marginal identical.

## Two distinct record ports and three controls on probe order

Let A1 and B1 be the first and third factors of the four-bit record representation, with the other factors maximally mixed. On A1,B1 take the supplied faithful state

    ρ = (I+x X_A X_B)(I+z Z_A Z_B)/4,       |x|,|z|<1.

Apply the original mask 1000 that pinches A1. Both fixed generators Z_A,Z_B survive, as do the diagonals and the ordinary correlation z. Both logical one-site marginals are I/2 in both arms. The full joint BKM covariance evaluated by the generic native helper is a different object from either site's marginal BKM. To compute it, split into sectors of Z_A Z_B with sign p=±1 and probabilities (1+p z)/2. Within each sector Z_B=p Z_A and the transverse two-level state has coherence x. The zero-field means vanish. The pre-pinch cross susceptibility is therefore zk. After pinching it is z.

At x=3/5 and z=1/2 the cross response is 0.432808512 before versus 0.5 after, an increase of 0.067191488. Reversing z reverses the change. At x=0 or z=0 the change vanishes. This is a change in predicted response to a **joint normalized logarithmic tilt**, not an undriven change in the readout. For a finite signed h, writing b=atanh x and t=sqrt(b²+h²), the receiver means are z h tanh(t)/t in the coherent case and z tanh(h) in the pinched case. Equal partition-function factors in the two parity sectors leave their weights fixed. These formulas reproduced the direct native exponential-matrix calculation.

| Actual or specified read on B1 | Increment in source-to-readout slope from A1 pinching |
|---|---:|
| Fresh joint logarithmic tilt by h Z_A in each logical state | +0.067191488 |
| Tilt the original logical state, then pinch or omit pinching and read | 0 |
| Selected local filter proportional to exp(h Z_A/2), normalized, in each arm | 0 |
| Same joint BKM diagnostic on either single encoded output copy in each arm | 0 |

For the filter the conditional mean is z tanh(h) in both arms because its trace weights depend only on the fixed diagonal populations. Its nonzero slope z is present in both. A deterministic trace-preserving local map on A cannot change B's reduced state: its adjoint leaves I_A fixed. The physical output registers of the sharp encoding each have marginal diag(ρ) in record coordinates. Their pre/post cross BKM is z in this fixture. Access to a joint retilting of the coherent logical state is therefore substantive. It is not supplied by measuring a surviving bit. No communication or gravitational detection follows from this conditional response difference.

All five encoding schedules were checked for the faithful analytical families. Complete artifacts retain numeric checks to nine decimals, with independent finite-field evaluations and identity/unrelated-mask, signed and zero controls. No data from a detector or spatial calibration enter either calculation.

## Evidence and research status

The registration files disclose prior analytic/exploratory results: [record protocol](RECORD_RESPONSE_PROTOCOL.md) and [recombination protocol](BRACKET_PORT_PROTOCOL.md). Replays: [original bracket / full matrix](evidence/same_port/bracket.json), [single records](evidence/same_port/single.json), [two records and copy controls](evidence/same_port/paired.json). The branch comparison provides a named operation that can change a fixed-port transfer coefficient in its test program, and the pruning comparison identifies a precise readout-order dependency. An inherited map from the actual pruning event to one of these changes, and an amplitude-sensitive read available to its receiver, remain to be derived.
