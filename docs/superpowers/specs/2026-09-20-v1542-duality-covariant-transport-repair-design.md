# UQCF-GEM v15.42 — Duality-Covariant Transport Repair

**Date:** 2026-09-20  
**Parent:** UQCF-GEM v15.41 transport-protocol erratum  
**Parent head:** `b9c5f29d8687a7dbc2af0595430aa73fbc5b8553`  
**Original v15.41 design blob:** `6d35aae0ccb6c2584d26d5a83d522b3cc7036728`  
**v15.41 erratum blob:** `d40d03d9d2498ce54839b15dad00c1505c1a586a`  
**Status:** design awaiting review; implementation is not authorized  
**Pillar 3:** `OPEN`

## 1. Purpose and claim boundary

v15.41 stopped with `PROTOCOL_INVALID` because its frozen text mixed tangent/coframe language,
reverse transport, direct matrix action, and a positive conformal variation. The literal typed system
was exactly inconsistent. The executed forward/positive ansatz was consistent but forced zero
linearized face holonomy for every scalar field tested, so it survives only as a non-adjudicating
no-go theorem for that ansatz.

v15.42 repairs only the transport layer. It asks:

> Can the operational square complex support one fully typed, duality-covariant, metric-compatible
> linearized transport rule that is fixed before source data are read and that passes an exact
> manufactured nonflat curvature control?

This stage does **not** query the v15.40 response fields, construct a source target, compare curvature
to source, infer physical gravity, or complete Pillar 2 or Pillar 3. A successful result certifies a
mathematical transport protocol only.

The only successful status allowed here is

```text
TRANSPORT_PROTOCOL_CERTIFIED
```

with next required object

```text
APPLY_CERTIFIED_TRANSPORT_TO_RESPONSE_GEOMETRY_WITHOUT_SOURCE_ADJUDICATION
```

## 2. Design decision and rejected alternatives

### Selected: one connection, paired tangent/cotangent presentations

The protocol is derived from the linearized metric-compatibility and Koszul identities on the
already certified operational tangent complex. Tangent vectors and covectors are not alternative
models. They are dual representations of the same edge transport and must agree before any
curvature result can be admitted.

### Rejected: choose whichever v15.41 convention is consistent

Forward/direct/positive and reverse/direct/negative presentations can both be made algebraically
consistent. Consistency after observing output does not select a connection. Neither convention may
be adopted merely because it avoids the v15.41 rank defect.

### Rejected: reuse face closure as the connection constructor

The v15.41 diagnostic theorem shows that the executed face-closure ansatz places every face
circulation row in the closure row space and therefore forces linearized face holonomy to vanish.
That ansatz remains a valuable no-go result, not the v15.42 constructor.

### Rejected: introduce coordinates, fitted coefficients, or a source-shaped stencil

The construction may use only labels, adjacency, certified direction classes, opposite-neighbor
relations, the baseline transport, the metric, and an arbitrary exact scalar control field.
Coordinates, spectra, v15.40 responses, source targets, historical result selection, fitting, and
floating tolerances are forbidden.

## 3. Frozen mathematical types

For each vertex $x$:

```text
T_x                 tangent carrier
T_x*                cotangent carrier
g_x                 positive symmetric bilinear form on T_x
P_xy^0 : T_x -> T_y certified flat baseline transport
u_x                 exact scalar conformal perturbation
```

The perturbed metric is

$$
g_x(\varepsilon)=e^{\varepsilon u_x}g_x^0.
$$

The forward tangent transport is factored relative to the baseline:

$$
P_{xy}(\varepsilon)
 =P_{xy}^0\bigl(I+\varepsilon B_{xy}\bigr)+O(\varepsilon^2),
\qquad B_{xy}\in\operatorname{End}(T_x).
$$

The reverse tangent transport is the inverse $P_{yx}(\varepsilon)=P_{xy}(\varepsilon)^{-1}$.
The transport of a covector at $y$ back to $x$ is the pullback

$$
P_{xy}(\varepsilon)^*:T_y^*\rightarrow T_x^*.
$$

No code path may infer one of these actions from matrix shape. Domain, codomain, direction, action,
carrier, dualization, base point, cycle orientation, and conformal sign must all be explicit.

## 4. Sign and symmetric part are derived, not selected

Metric compatibility is

$$
P_{xy}(\varepsilon)^Tg_y(\varepsilon)P_{xy}(\varepsilon)
 =g_x(\varepsilon).
$$

Differentiation at the certified flat baseline gives

$$
B_{xy}+B_{xy}^{\dagger}=(u_x-u_y)I.
$$

Therefore

$$
\operatorname{sym}B_{xy}=\frac{u_x-u_y}{2}I.
$$

The signs of frame and coframe variation follow from duality:

$$
\delta e_a(x)=-\frac{u_x}{2}e_a(x),\qquad
\delta\theta^a(x)=+\frac{u_x}{2}\theta^a(x).
$$

These are not configurable manifest fields. A tangent implementation using the positive frame sign,
or a cotangent implementation using the negative coframe sign, is invalid.

## 5. Canonical operational derivative

At each $x$, the operational complex supplies one neighbor in each of the four direction classes
$\{\pm d_1,\pm d_2\}$. Define the exact centered derivative $q_x\in T_x$ by

$$
g_x^0(q_x,d_i)
 =\frac{u(x+d_i)-u(x-d_i)}{2},
\qquad i=1,2.
$$

This definition is basis-free once the operational metric and opposite direction pairs are fixed.
It is the unique radius-one linear stencil satisfying all of the following:

1. annihilates constants;
2. changes sign when $d_i$ is reversed;
3. is exact on an affine field on the lifted square patch;
4. is equivariant under the full local $D_4$ action;
5. gives equal weight to the two opposite samples.

For an oriented edge $x\to y$, let $d_{xy}\in T_x$ be its certified unit direction and transport
the endpoint derivative back before averaging:

$$
\bar q_{xy}
 =\frac12\left(q_x+P_{yx}^0q_y\right)\in T_x.
$$

## 6. Frozen linearized transport rule

The source-space endomorphism in the baseline factorization is

$$
B_{xy}
 =\frac{u_x-u_y}{2}I
 +\frac12\left(
   \bar q_{xy}\otimes d_{xy}^{\flat}
   -d_{xy}\otimes\bar q_{xy}^{\flat}
  \right).
$$

The first term is forced by exact metric compatibility. The second is the orientation-free skew part
of the linearized Koszul connection. It is fixed by the centered derivative and the unique
endpoint-symmetric linear average. No free coefficient remains.

Required identities include:

$$
B_{yx}
 =-P_{xy}^0B_{xy}P_{yx}^0,
$$

and, for any local frame change $G_x\in D_4$,

$$
B_{xy}\mapsto G_xB_{xy}G_x^{-1},\qquad
P_{xy}^0\mapsto G_yP_{xy}^0G_x^{-1},\qquad
P_{xy}(\varepsilon)\mapsto G_yP_{xy}(\varepsilon)G_x^{-1}.
$$

The cotangent implementation is generated mechanically by pullback from the tangent transport. It
is forbidden to maintain an independently adjustable cotangent constructor.

## 7. Holonomy and presentation covariance

For an oriented square
$C=(x_0,x_1,x_2,x_3)$, column-vector composition is frozen as

$$
H_C(\varepsilon)
 =P_{x_3x_0}(\varepsilon)
  P_{x_2x_3}(\varepsilon)
  P_{x_1x_2}(\varepsilon)
  P_{x_0x_1}(\varepsilon)
 :T_{x_0}\rightarrow T_{x_0}.
$$

The linearized curvature carrier is $K_C=\delta H_C|_{\varepsilon=0}$. It remains an
endomorphism; no supplied orientation may turn it into a signed scalar.

The implementation must prove exactly:

- cyclic base-point changes conjugate $K_C$ by the intervening baseline transport;
- reversal gives the derivative of inverse holonomy, and at flat baseline $K_{C^{-1}}=-K_C$;
- local $D_4$ frame changes conjugate the based curvature;
- tangent holonomy and cotangent pullback holonomy are exact duals;
- the zero/nonzero classification and
  $\kappa_C^2=-\tfrac12\operatorname{tr}(K_C^2)$ are presentation invariant.

## 8. Mandatory source-blind controls

All controls use `Fraction` arithmetic and run before any response artifact is importable.

### 8.1 Constant-field null

For every tested carrier size and every exact constant $c$,

$$
u_x=c\quad\Longrightarrow\quad B_{xy}=0,\quad K_C=0.
$$

### 8.2 Manufactured nonflat vertex impulse

On the periodic operational square carrier, mark a vertex $r$ and define

$$
u_r=1,\qquad u_x=0\quad(x\ne r).
$$

The mark is control metadata, not a physical source, and must be carried under every relabeling.
For $L=5$, the exact multiset of the invariant $\kappa_C^2$ over all 25 faces is frozen as

| Exact value | Face count |
|---:|---:|
| (1/16) | 4 |
| (1/64) | 8 |
| (0) | 13 |

The held-out $L=7$ result is frozen as

| Exact value | Face count |
|---:|---:|
| (1/16) | 4 |
| (1/64) | 8 |
| (0) | 37 |

Every choice of marked vertex must produce the same multiset. At least one $K_C$ must be nonzero.
This is the mandatory nonflat canary.

### 8.3 Scale and superposition

For exact amplitudes (lambda\in\{1,7/3}),

$$
B[\lambda u]=\lambda B[u],\qquad
K[\lambda u]=\lambda K[u],\qquad
\kappa^2[\lambda u]=\lambda^2\kappa^2[u].
$$

For two independently chosen exact fields and exact coefficients, transport and curvature must obey
linear superposition.

### 8.4 Covariance controls

The complete control family must pass:

- arbitrary label permutations with transported marked vertex;
- all local (D_4) frame changes, including reflections;
- all four cyclic base points for every face;
- both face orientations;
- tangent/cotangent dual execution;
- direct construction versus independently expanded product differentiation.

Any post-output frame, orientation, sign, normalization, or contraction choice is forbidden.

## 9. Status logic and hard stops

The implementation must evaluate gates in this order:

1. evidence and parent-blob verification;
2. operational-complex and baseline verification;
3. manifest/type completeness;
4. uniqueness of the centered derivative and edge average under the frozen axioms;
5. tangent/cotangent duality and exact metric compatibility;
6. reversal, basepoint, orientation, frame, and relabeling covariance;
7. constant null;
8. nonflat L=5 canary;
9. held-out L=7 canary;
10. scale and superposition.

Outcome mapping is mechanical:

| Condition | Status | Next object |
|---|---|---|
| Type, evidence, covariance, or exact-control failure | `PROTOCOL_INVALID` | `REPAIR_PROTOCOL_BEFORE_ANY_APPLICATION` |
| Frozen axioms fail to select one derivative/edge rule | `PROTOCOL_NOT_IDENTIFIABLE` | `ADD_FIRST_PRINCIPLES_SELECTION_AXIOM` |
| Every gate passes | `TRANSPORT_PROTOCOL_CERTIFIED` | `APPLY_CERTIFIED_TRANSPORT_TO_RESPONSE_GEOMETRY_WITHOUT_SOURCE_ADJUDICATION` |

No outcome may populate a source correspondence, stress-energy, Einstein, continuum, spacetime, or
physical-gravity verdict.

## 10. Evidence firewall and prohibited inputs

The transport constructor and every manufactured control must expose zero queries to:

- v15.40 response arrays or response-generation code;
- source targets, support signs, or source labels;
- historical connection or curvature outputs;
- graph spectra, fitted parameters, coordinates, or external embeddings;
- Newtonian, Einstein, or observational targets;
- floating-point tolerances;
- post-output convention selectors.

The implementation plan must name the exact import firewall and tests that prove these counts are
zero. Hashes for the parent design, erratum, corrected ledger, and certified parent head must be
verified before execution.

## 11. Future artifact boundary

After this design is separately approved, the next action is to write an implementation plan. The
plan may propose a new additive directory

```text
ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/
```

with exact algebra, typed transport, manufactured controls, tests, README, ledger, and a dedicated
GitHub Actions workflow. It must use behavior-first RED tests and retain the v15.39-v15.41 inherited
regressions.

This design does not authorize those files, the implementation plan, execution, or changes to the
v15.41 artifacts.

## 12. Completion and scientific interpretation

v15.42 is complete only if one predeclared typed rule passes every exact gate, including the nonflat
canary, without reading source or response data. A pass means that the protocol can represent
nonzero operational curvature without convention ambiguity. It does not show that the frozen
responses generate curvature, that curvature corresponds to source, or that physical gravity has
emerged.

A failure is also informative: it means the proposed operational metric/tangent data do not yet
select a usable transport protocol under these axioms. No convention may be repaired after output.

In every outcome:

```text
Pillar_3 = OPEN
scientific_breakthrough = false
```
