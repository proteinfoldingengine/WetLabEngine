# UQCF-GEM v9.67 — Operational Identity and Gluing Rigidity Gate

Classification: PHYSICAL_ASSUMPTIONS_SEPARATED__AFFINE_FIXED_LOCAL_STATE_GLUING_IS_RIGID__NEW_SOURCE_LAW_NOT_SELECTED.

## 1. Purpose: improve the reason for an axiom

The user approved improving the physical motivation of the next canary, rather than continuing to invent convenient deformations. This report therefore starts with a consistency principle and audits its strength before adopting any new law.

The target remains gravity's existence in an atemporal relational world. No time, pruning, entropy, or information-loss mechanism enters. The question is whether a source can change which global relations coexist while preserving a coherent meaning for shared subsystems.

The proposed motivating principle is: when two relational descriptions refer to the same subsystem, their local operational content should be consistently identified. This expresses consistency of subsystem identity; by itself it neither freezes local state values nor specifies a gravitational coupling.

This gate proves that a stronger, superficially similar requirement would make a large class of source-dependent gluing maps trivial. That distinction should govern future axiom selection.

## 2. Three requirements that must not be conflated

### A. Fixed local operational labels

The local Hilbert space, observable algebra, and rules for evaluating a local state are specified. This tells us what a local observable means. It does not say its value is independent of a source.

### B. Agreement across overlapping descriptions

For an edge e={i,j}, a proposed source-dependent output F_(e,s)(rho) should have a local reduction at i that agrees with the reduction obtained from any other incident edge describing i. One may write the common local state as f_(i,s)(rho).

This condition allows the common value to depend on source. It is a compatibility requirement, not by itself a constitutive source law.

### C. Equality with every frozen local marginal

The stronger condition sets

\[
f_{i,s}(\rho)=\operatorname{Tr}_{\bar i}\rho
\quad\text{for every old global state }\rho\text{ and every }s.
\]

This does more than preserve identity or covariance: it forbids source dependence of every local state value relative to the same global input representation. It is not established here as a physical necessity for pre-time gravity. We test its consequences explicitly rather than treating it as an innocent synonym for local consistency.

## 3. Frozen mathematical assumptions for the theorem

Let H_G be a finite tensor product of the existing subsystem Hilbert spaces, and let D_G be the FULL set of density operators on it. Fix an edge e={i,j} and a source label s. Suppose

\[
F_{e,s}:\mathcal D_G\longrightarrow\mathcal D(H_i\otimes H_j)
\]

has the following properties:

1. It is affine on D_G: F(t rho+(1-t)eta)=t F(rho)+(1-t)F(eta) for 0<=t<=1.
2. Every output is positive semidefinite and trace one.
3. It preserves both frozen endpoint marginals for every global input:

\[
\operatorname{Tr}_jF_{e,s}(\rho)=\operatorname{Tr}_{\bar i}\rho,
\quad
\operatorname{Tr}_iF_{e,s}(\rho)=\operatorname{Tr}_{\bar j}\rho.
\]

Affinity is a static requirement on representing density states, not a physical mixing process or an entropy assumption. It is stronger than allowing a map only on a selected nonconvex pure-state set. No complete positivity, channel implementation, covariance, or source-composition law is needed for the theorem.

## 4. Exact rigidity theorem

**Theorem.** Under the three assumptions,

\[
\boxed{F_{e,s}(\rho)=\operatorname{Tr}_{\bar e}\rho
\quad\text{for every }\rho\in\mathcal D_G.}
\]

Since s was arbitrary, no source dependence remains in any such edge map.

### Lemma: a pure marginal fixes a tensor factor

Let tau>=0 be a bipartite density operator with tau_i=P_i a rank-one projector. Put Q=(I-P_i) tensor I. Then Tr(Q tau)=0. Positivity implies tau has support in the kernel of Q, namely range(P_i) tensor H_j. Therefore tau=P_i tensor tau_j. If both endpoint marginals are pure, tau is their product.

### Step 1: agreement on every global product-pure state

For rho=tensor_k P_k with every P_k rank one, the two endpoint marginal conditions give P_i and P_j. The lemma forces

\[
F_{e,s}(\textstyle\bigotimes_kP_k)=P_i\otimes P_j
=\operatorname{Tr}_{\bar e}(\textstyle\bigotimes_kP_k).
\]

### Step 2: product-pure projectors affinely span the state hyperplane

On a d-dimensional local space, rank-one projectors span Hermitian operators. For example use the computational projectors and, for each a<b, the projectors onto (|a>+|b>)/sqrt(2) and (|a>+i|b>)/sqrt(2). Subtracting diagonal projectors isolates the real and imaginary off-diagonal Hermitian directions. There are d^2 independent projectors in this construction.

Tensor products of these local projector bases give a basis of global Hermitian operators, all consisting of product-pure projectors. Since each has trace one, their affine span is the full trace-one Hermitian hyperplane.

### Step 3: affine extension

An affine map on the density body, which has nonempty relative interior in that hyperplane, has a unique affine extension to its affine hull. Thus two affine maps agreeing on the spanning product-pure projectors agree on the whole density body. Apply this to F_(e,s) and the ordinary partial trace. QED.

The extension step does NOT claim every entangled state is a convex mixture of product states. Affine spanning can involve negative coefficients; it is the affine-map hypothesis that permits the uniqueness argument.

## 5. Meaning for the canary

This is stronger than the vertex-coherent unitary null in v9.62: the proposed edge map need not be unitary, invertible, or completely positive. Positivity of its outputs, affinity, and exact preservation of all old local states already suffice.

It explains why a source-dependent, correlation-only rewrite of pair gluing cannot succeed on the full frozen density domain while all endpoint state values are held fixed. Positivity first fixes the outputs on pure product inputs, and affinity extends that rigidity everywhere.

This is not a prohibition against changing correlations among states with the same marginals in a particular fiber. Such distinct states certainly exist. The theorem prohibits one universal positive affine edge map on ALL global states from implementing a nontrivial change while preserving both local marginals for every input.

It also does not rule out a source-dependent admissible DOMAIN with the ordinary marginal map. In that case the source changes which joint states are allowed, and the spanning/full-domain hypothesis used here need not hold for the relevant law. The source constraint would still have to be stated and physically justified.

## 6. Pure-global and operational boundaries

The proof uses globally pure product states as witnesses; it does not substitute mixed local states for pure global ones. Its conclusion over all states uses an affine extension on the full density domain. A theory defined only on an intrinsically restricted set of pure states without such an extension is outside the theorem.

Keeping local observable labels fixed is not the same as requiring every local expectation to remain unchanged between source sectors. The former may be a reasonable comparison convention; the latter is the strong condition C above.

Likewise, agreement among incident edges does not identify their common local state with the frozen marginal unless that extra condition is imposed. Source-responsive local states could still agree across descriptions. Whether such a response is simply state reachability in the old arena or a genuine new admissibility law must be checked separately against v9.50.

This report does not assume ordinary tensor-factor identity is the final physical ontology. It states precisely what follows if that identity, the full old density domain, and affine density-state representation are retained.

## 7. Revised physical brief for the next law

The improvement is an explicit separation of motivation from constitutive assumptions:

- Require a consistent identification of shared local systems. Do not silently strengthen this into source-independent numerical local states.
- Preserve the globally pure sector as a direct test, not through mixed-state surrogate arguments.
- State whether the source changes admissible joint states, the readout map, or subsystem structure. These are different claims with different comparison rules.
- Explain why the chosen change is tied to the source's intrinsic provenance or composition, rather than selecting it because it creates a response.
- Treat disconnected-system composition as a declared operational requirement. Do not infer it from covariance alone.
- Keep the neutral sector exactly identified with the frozen architecture and specify the source-composition law before claiming a derived response.

Within fixed local quantum kinematics, a source-dependent law of JOINT EXTENDIBILITY remains a logically distinct target: specify which tuples of local relations can share a global realization. This brief does not select that law, prove its existence, or make it gravitational. A useful law must have an independent physical rationale; another arbitrary hard constraint would repeat the weakness of the earlier candidate search.

There is no new constitutive law selected in v9.67. The result prevents the research program from building its desired effect out of inconsistent assumptions, while identifying an unnecessarily strong assumption that would exclude it in advance.

## 8. Exact verification

A standard-library rational calculation verified that the 64 tensor products of four spanning pure qubit projectors have Hermitian span dimension 64 and hence affine span dimension 63 in the trace-one hyperplane. The general theorem is proved above, not inferred from this finite check. No ensemble or physical simulation was run.

```python
from fractions import Fraction as F
from itertools import product
local = [(1,0,0,1),(1,0,0,-1),(1,1,0,0),(1,0,1,0)]
rows = []
for states in product(local,repeat=3):
    rows.append([F(states[0][a]*states[1][b]*states[2][c],8)
                 for a,b,c in product(range(4),repeat=3)])
a = [r[:] for r in rows]
rank = 0
for col in range(64):
    pivot = next((i for i in range(rank,64) if a[i][col]),None)
    if pivot is None:
        continue
    a[rank],a[pivot] = a[pivot],a[rank]
    val = a[rank][col]
    a[rank] = [x/val for x in a[rank]]
    for i in range(rank+1,64):
        val = a[i][col]
        if val:
            a[i] = [x-val*y for x,y in zip(a[i],a[rank])]
    rank += 1
assert rank == 64
print('Hermitian span:',rank,'affine trace-one span:',rank-1)
```

## 9. Adjudication

- ESTABLISHED: consistent subsystem identity and fixed numerical local states are different requirements.
- EXACT THEOREM: universal positive affine gluing preserving every old endpoint marginal equals ordinary marginalization.
- NOT ESTABLISHED: that gravity must satisfy the stronger fixed-local-state premise.
- NOT SELECTED: a physically justified new source-to-joint-extendibility law.

v9.67 improves the axiom-selection discipline rather than adding a gravity signal. It is a bounded structural result, not a general no-go for atemporal gravity or every source-dependent relational theory. The next substantive hypothesis must state why a source changes joint extendibility and which comparison assumptions it retains. It should not be another map already excluded by this rigidity theorem.