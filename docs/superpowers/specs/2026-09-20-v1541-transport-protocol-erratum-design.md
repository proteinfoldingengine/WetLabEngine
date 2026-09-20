# UQCF-GEM v15.41 — Transport Protocol Erratum

**Date:** 2026-09-20
**Parent design:** `2026-09-19-v1541-formal-connection-curvature-source-correspondence-design.md`
**Parent design blob:** `6d35aae0ccb6c2584d26d5a83d522b3cc7036728`
**Status:** correction design approved; implementation not yet authorized
**Pillar 3:** OPEN

## 1. Authority and scope

This erratum preserves the parent design as the exact preregistration record and supersedes it only
where the executed transport convention conflicts with the frozen mathematical types. It does not
authorize a replacement connection, sign convention, torsion rule, lift, or curvature observable.
The correction is limited to stopping the v15.41 adjudication truthfully and preserving the useful
execution results as explicitly non-adjudicating diagnostics.

The authoritative v15.41 status after implementation of this erratum must be

```text
PROTOCOL_INVALID
```

with next required object

```text
REPAIR_ONLY_THE_PROTOCOL_DEFECT_BEFORE_ADJUDICATION
```

The previously frozen status
`CONNECTION_IDENTIFIABLE_NO_CURVATURE_SOURCE_CORRESPONDENCE` must remain in the ledger only as a
superseded execution receipt. It is not an adjudicating scientific result.

## 2. First-principles transport types

For every label `x`, distinguish the tangent space `T_x` from its dual `T_x*`.

```text
g_x       : symmetric bilinear form on T_x
P_xy      : T_x -> T_y
P_yx      : T_y -> T_x = P_xy^-1
P_xy*     : T_y* -> T_x* = pullback by P_xy
```

In matrices, after bases are declared, tangent-vector transport from `y` back to `x` uses `P_yx`.
Covector transport from `y` back to `x` uses the pullback `P_xy^T`. These are different typed maps
even when the flat baseline represents both by the identity matrix.

The frozen plan simultaneously called `v_i` a coframe vector, prescribed

```text
delta_v_i = +(u[x_i]/2) v_i,
```

and instructed the implementation to transport every later edge vector back to `T_x0` using
`P_10`, `P_21`, and `P_32`. The executed implementation instead used the forward directed edges
`(x0,x1)`, `(x1,x2)`, and `(x2,x3)` directly, without declaring a dual pullback. Because the
baseline matrices are identities, the mismatch first appears only after differentiation.

No implementation may repair this ambiguity by choosing whichever convention makes the system
consistent. A future protocol must declare, before execution:

1. whether each `v_i` is a tangent vector or a covector;
2. the domain and codomain of every transport factor;
3. whether a matrix acts directly, inversely, by transpose, or by inverse transpose;
4. the sign of the frame/coframe variation induced by `h=u g`;
5. the orientation and base-point covariance identities that make alternate presentations
   mathematically equivalent.

## 3. Exact defect witness

The erratum implementation must run a protocol-consistency audit before connection or curvature
adjudication. For the literal frozen tangent reading, later edge vectors are transported back with
reverse directed transports while retaining the frozen positive `delta_v_i` sign. On nonconstant
canonical response fields this exact system is inconsistent:

| Size | Unknowns | Coefficient rank | Augmented rank |
|---:|---:|---:|---:|
| 5 | 50 | 50 | 51 |
| 7 | 98 | 98 | 99 |

The same inconsistency occurs for the tested independent nonconstant exact fields. A manufactured
nonconstant exact field must therefore be a mandatory pre-adjudication control. Rank mismatch is a
protocol defect, not permission to reverse a sign, reinterpret a type, or select a dual convention
after output is known.

The executed forward/positive convention is consistent. A coherent tangent-vector dual convention
using reverse transport and negative frame variation is also consistent. Their agreement on the
flatness diagnostic does not retroactively choose either convention for v15.41; both are
post-execution interpretations absent from the frozen typed manifest.

## 4. Non-adjudicating flatness and parity theorem

The following computation is preserved under

```text
NON_ADJUDICATING_PROTOCOL_DIAGNOSTIC
```

For the executed ansatz on a directed edge,

```text
delta P_xy = ((u_x-u_y)/2) I + a_xy J.
```

For one oriented square, imposing the executed closure equations in both orientations forces the
four oriented rotational coefficients to have the form

```text
(a_0, a_1, a_2, a_3) = (t, -t, t, -t).
```

Consequently, the rotational circulation is zero. The scalar part is an exact edge coboundary and
also telescopes to zero, so the differentiated face holonomy vanishes for every scalar field:

```text
delta H_C = 0.
```

This is not a property specific to the frozen source responses. It was verified on every standard
basis field at `L=5`, on independent exact fields, and by an exact local row-space identity: adding
the face-circulation equation to the four local closure rows does not increase their rank.

Global propagation exposes a parity law:

| Size parity | Rotational nullity | Interpretation |
|---|---:|---|
| odd periodic `L` | 0 | periodicity kills the alternating mode; the unique solution is flat |
| even periodic `L` | 1 | one checkerboard rotational mode survives; it is still face-flat |

Exact witnesses include ranks `50/50` at `L=5`, `98/98` at `L=7`, and `162/162` at `L=9`, versus
rank `71` of `72` unknowns at `L=6` and rank `127` of `128` unknowns at `L=8`. Thus the original
odd-size identifiability result is partly a parity property of the periodic carrier. It cannot
support a source-specific curvature claim.

## 5. Corrected execution order and stop semantics

The correction must execute in this order:

1. verify every inherited evidence pin;
2. verify an explicit transport-type manifest;
3. run the literal manufactured-field rank audit;
4. compare the manifest with the actual matrix direction, dualization, and variation sign;
5. return `PROTOCOL_INVALID` immediately on any mismatch or inconsistency;
6. set connection-identifiability, curvature-map-identifiability, correspondence, and control
   adjudication fields to `null`;
7. publish the prior execution only under `superseded_execution_receipt`;
8. publish the flatness/parity theorem only under `non_adjudicating_protocol_diagnostics`.

No diagnostic may upgrade or replace the stopped adjudication. No historical connection artifact
may be used to select a repair.

## 6. Required artifacts and tests

The correction implementation must update the v15.41 gate, tests, canonical result, README,
workflow, implementation plan, and draft pull-request description. The authoritative ledger must:

- contain no floating-point number;
- retain all evidence hashes and the prior exact-head execution receipts;
- report `protocol_valid=false` and `status=PROTOCOL_INVALID`;
- report all downstream scientific verdicts as `null`;
- preserve Pillar 3 as `OPEN` and every physical-interpretation flag as false;
- reproduce byte-for-byte from a clean run.

Behavior-first tests must cover:

1. explicit tangent-versus-covector typing and transport direction;
2. exact coefficient/augmented rank mismatch for the literal frozen convention;
3. immediate protocol-invalid stopping before scientific adjudication;
4. the local closure/circulation row-space identity;
5. arbitrary-field zero curvature for the executed diagnostic convention;
6. odd/even rank and nullity witnesses;
7. preservation of the superseded result as non-authoritative provenance;
8. all interpretation and construction firewalls;
9. byte-identical canonical replay;
10. inherited v15.39 and v15.40 frontier regressions.

## 7. Claim boundary

After correction, v15.41 establishes no adjudicating connection, curvature, or source-curvature
correspondence. It records two narrower facts:

1. the frozen transport protocol was not typed precisely enough to adjudicate its intended
   connection question;
2. the executed convention implies a response-independent flatness theorem with an odd/even
   identifiability distinction.

The second fact is a no-go result for the executed formal ansatz, not evidence for or against
physical gravity. A replacement protocol requires a separately reviewed design and implementation
plan. It must pass a preregistered manufactured nonflat conformal-field control before any source
correspondence is evaluated.
