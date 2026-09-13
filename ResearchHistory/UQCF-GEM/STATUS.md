# UQCF-GEM Current Status

**As of:** 2026-09-13  
**Latest completed gate:** v15.09 — Quantum Carrier Origin / Tensor-Factorization Blindness Gate  
**Primary adjudication:** `CANONICAL_NEUTRAL_STRUCTURE_DOES_NOT_DERIVE_RETAINED_QUANTUM_CARRIER`  
**Secondary:** `FRAME_NEUTRAL_REFERENCE_IS_TENSOR_FACTORIZATION_BLIND`  
**Tertiary:** `SUPPLIED_SITE_FINGERPRINTS_DO_NOT_DEFINE_CROSS_DOMAIN_NODE_SITE_FUNCTOR`  
**Major structural result:** `true`  
**Scientific breakthrough:** `false`  
**Pillar 3:** `OPEN`

## Current scientific picture

The recent v15 sequence has separated three problems that previously risked being conflated:

```text
A. local quantum information structure
B. physical source semantics
C. retained-relation -> quantum-carrier representation
```

They now have distinct statuses.

```text
local covariance (v15.04)
    -> qubit traceless source family a(r)(rho-I/2)
    -> covariance alone leaves a(r) free

composition (v15.05)
    -> arbitrary already-selected local a(r) composes naturally
    -> generic composition does not select a(r)
    -> stronger functional-calculus tensor law would select log shape

recoverability multiplicativity (v15.06)
    -> root fidelity multiplicative
    -> -log fidelity additive
    -> scalar comparison generator does not select local Hermitian source

frame-neutral quantum structure (v15.07)
    -> tau_d=I_d/d uniquely selected by full local-frame invariance
    -> Q_d(rho)=d rho canonical and multiplicative
    -> centered log rho is the canonical additive Hermitian information generator

source semantics (v15.08)
    -> Genesis Pin = history legitimacy boundary, not quantum reference state
    -> ternary source role = legitimacy information, not Hermitian generator
    -> same frozen provenance permits multiple inequivalent lawful source rays
    -> physical-source identification is irreducible relative to frozen ontology

carrier origin (v15.09)
    -> tau_D=I_D/D factorizes under every supplied tensor decomposition
    -> neutral structure therefore cannot select subsystem decomposition
    -> supplied five-qubit neutral reference preserves all 120 site permutations
    -> even rigid graph nodes + rigid quantum-site spectra leave 120 cross-domain bijections
    -> C125 still has no five-nontrivial-factor decomposition
    -> v15.07 does not reopen v15.02-v15.03 representation shortcuts
```

The present upstream chain is therefore

```text
retained relational/provenance carrier
    -X-> canonical retained-node -> quantum-site functor
quantum Hilbert carrier (once supplied)
    -> unique frame-neutral state tau_d=I/d
    -> canonical relative-density operator Q_d=d rho
    -> centered-log information generator
    -X-> physical-source semantics under frozen ontology
    -X-> natural five-site -> C125 compatibility-parent map
```

The positive quantum mathematics is preserved. The missing arrows are now typed representation/semantics primitives rather than unspecified numerical fits.

## Latest result — v15.09

### A. Tensor-factorization blindness

For every factorization

```text
D = product_i d_i
```

the frame-neutral state satisfies

```text
tau_D = I_D/D = tensor_i(I_di/d_i).
```

Therefore `tau_D` is compatible with every supplied tensor decomposition and cannot select one.

For `D=32`, the full unordered nontrivial factorization list is

```text
[32]
[2,16]
[4,8]
[2,2,8]
[2,4,4]
[2,2,2,4]
[2,2,2,2,2]
```

with

```text
unordered factorization count      = 7
max neutral factorization error    = 0.0
five-factor decomposition count    = 1
five-factor decomposition          = [2,2,2,2,2]
```

The last line is conditional on first supplying the requirement “five factors.” It is not selected by the neutral state.

Classification:

```text
FRAME_NEUTRAL_REFERENCE_IS_TENSOR_FACTORIZATION_BLIND
```

### B. Neutral five-qubit state does not label sites

On a supplied five-qubit carrier,

```text
tau_32 = (I_2/2)^tensor5.
```

All `5! = 120` site permutations were enumerated.

```text
permutations tested                 = 120
permutations preserving neutral tau = 120
max permutation error               = 0.0
```

Classification:

```text
NEUTRAL_FIVE_QUBIT_REFERENCE_HAS_FULL_S5_SITE_PERMUTATION_SYMMETRY
```

### C. Rigid graph + rigid quantum sites still do not define a cross-domain map

The retained directed graph has exact automorphism order

```text
1.
```

Using the frozen v15.03 control-A local spectra, all five quantum sites are spectrally distinct under independent local-unitary gauge, so the site spectral stabilizer also has order

```text
1.
```

Nevertheless there is no frozen relation connecting the graph sort to the quantum-site sort.

Every bijection

```text
phi : retained nodes -> quantum sites
```

is therefore an additional expansion of the same two-sort reduct.

```text
node-site bijections       = 120
inequivalent bijections    = 120
certified cross-domain map = NONE
```

Classification:

```text
TWO_SORT_REDUCT_DOES_NOT_DEFINE_NODE_SITE_BIJECTION
```

This rules out the argument that individual rigidity on both sides somehow creates a canonical correspondence between them.

### D. `C^125` parent mismatch remains exact

The certified compatibility parent has dimension 125.

Its complete unordered nontrivial multiplicative decompositions are

```text
[125]
[5,25]
[5,5,5].
```

Therefore

```text
five nontrivial factor decomposition count = 0.
```

A supplied five-qubit carrier has dimension 32, and no frozen natural `H32 -> C125` carrier map is certified.

Classification:

```text
V15_07_NEUTRAL_STRUCTURE_DOES_NOT_REPAIR_C125_PARENT_TYPE_MISMATCH
```

## What v15.09 changes

v15.09 answers the strongest native reassessment after v15.07:

```text
Could the new canonical neutral/reference structure itself provide the missing carrier origin?
```

No.

The reason is structural rather than numerical:

1. `I_D/D` is deliberately blind to tensor decomposition;
2. distinct local state spectra exist only after a site factorization is already supplied;
3. within-sort rigidity does not create a cross-sort relation;
4. the existing compatibility parent has the wrong factor arithmetic for five nontrivial sites.

Thus the new canonical quantum structure is **intrasort**. It is canonical once a Hilbert carrier is specified, but it does not originate that carrier from retained provenance.

## Relation to earlier gates

- **v15.08:** preserved. The source-semantics branch remains stopped and is not reused as a representation selector.
- **v15.07:** preserved positively. `tau_d=I/d`, `Q_d=d rho`, and centered `log rho` remain canonical quantum information objects.
- **v15.03:** not reopened. Exact retained graph -> five-site quantum factorization remains underived; five nontrivial sites still cannot equal `C^125`.
- **v15.02:** not reopened. The node↔quantum-label correspondence remains extra cross-domain information.
- **v15.01:** preserved. `C^125 -> C^25` compression is exact once a lawful parent object exists, but provenance does not supply that parent representation.
- **v14.04:** preserved. A representation/intertwiner from richer provenance into the compatibility source carrier remains missing.
- **v14.03:** preserved conditional. A supplied positive projective support source still selects hidden first contact and the intrinsic dual ray.
- **v13.25-v13.28:** preserved. Absolute source calibration and absolute source-to-geometry coupling remain underived.

## Preserved pillar status

- Pillar 1 — Global Atlas Closure: **COMPLETE**.
- Pillar 2 — Retained Curvature / Source-Current Compatibility: **CLOSED CONDITIONAL**.
- Pillar 3 — GR/ADM Correspondence: **OPEN**.

## Still not derived

- a retained-node-to-quantum-site functor;
- a five-site quantum carrier from retained provenance;
- a natural graph/site -> `C^125/C^25` compatibility map;
- a physical rule matching graph invariants to quantum spectral invariants;
- physical-source semantics for centered `log rho`;
- Genesis/provenance -> v14.03 projective support source `[P]_+`;
- absolute source magnitude / observer calibration;
- physical stress-energy;
- source-to-solder/coframe law;
- absolute source-to-geometry coupling;
- physical metric/coframe/spacetime;
- ontology-native quantum continuum refinement;
- Einstein equations;
- a physical time primitive;
- Pillar 3 closure.

## Stop rule / next lawful frontier

Do **not** continue the carrier-origin branch by:

```text
reading subsystem labels out of I/d;
choosing five qubits because 32 happens to admit 2^5;
matching graph nodes to distinct site spectra by sorted rank;
choosing a favorite one of the 120 bijections;
reusing the stopped v15.08 source semantics as a representation law;
padding or reshaping H32 into C125;
inventing an SVD/PCA/random embedding;
selecting a carrier map by downstream gravity/ADM/Einstein performance.
```

A continuation of this branch requires an independently motivated **NEW CROSS-DOMAIN CARRIER/FUNCTOR PRINCIPLE**.

Under current governance, the default is to preserve the canonical quantum information structure and redirect to a genuinely independent unresolved bridge rather than invent that principle.
