# v15.09 — Quantum Carrier Origin / Tensor-Factorization Blindness Gate

**Status:** CLOSED ON BRANCH / integration pending  
**Primary outcome:** `CANONICAL_NEUTRAL_STRUCTURE_DOES_NOT_DERIVE_RETAINED_QUANTUM_CARRIER`  
**Secondary:** `FRAME_NEUTRAL_REFERENCE_IS_TENSOR_FACTORIZATION_BLIND`  
**Tertiary:** `SUPPLIED_SITE_FINGERPRINTS_DO_NOT_DEFINE_CROSS_DOMAIN_NODE_SITE_FUNCTOR`  
**Major structural result:** `true`  
**Scientific breakthrough:** `false`  
**Pillar 3:** `OPEN`

## Question

v15.07 added genuinely new canonical quantum structure:

\[
\tau_d=I_d/d,
\qquad
Q_d(\rho)=d\rho,
\qquad
K_d^0(\rho)=\log\rho-\frac{\operatorname{Tr}\log\rho}{d}I.
\]

v15.08 then proved that the frozen Genesis/source ontology does not identify the centered-log generator as the physical source.

That leaves an independent representation question:

> Does the v15.07 canonical quantum structure itself repair the older v15.02-v15.03 carrier-origin obstruction and canonically identify the retained five-node relational graph with a five-site quantum carrier?

The answer is no.

The stronger result is

\[
\boxed{
\texttt{CANONICAL\_NEUTRAL\_STRUCTURE\_DOES\_NOT\_DERIVE\_RETAINED\_QUANTUM\_CARRIER}
}.
\]

The obstruction separates into three exact layers:

1. the frame-neutral state does not select a tensor decomposition;
2. even a supplied five-site quantum factorization does not define a retained-node-to-site bijection;
3. a five-nontrivial-site carrier still cannot equal the certified \(\mathbb C^{125}\) compatibility parent.

No source-semantics axiom, pruning rule, entropy criterion, gravity target, ADM residual, Einstein equation, or cosmological fit is used in this gate.

---

# I. TENSOR-FACTORIZATION BLINDNESS THEOREM

## 1. The neutral state is compatible with every supplied tensor decomposition

Let

\[
D=\prod_{i=1}^n d_i,
\qquad d_i\ge2.
\]

The v15.07 neutral state is

\[
\tau_D=\frac{I_D}{D}.
\]

For every supplied tensor decomposition

\[
\mathcal H_D\cong\bigotimes_i\mathbb C^{d_i},
\]

we have the exact identity

\[
\begin{aligned}
\bigotimes_i\tau_{d_i}
&=\bigotimes_i\frac{I_{d_i}}{d_i}\\
&=\frac{\bigotimes_i I_{d_i}}{\prod_i d_i}\\
&=\frac{I_D}{D}\\
&=\tau_D.
\end{aligned}
\]

Therefore

\[
\boxed{
\tau_D\text{ is compatible with every supplied tensor factorization of }D.
}
\]

It cannot select one.

This is not a numerical observation. It is an algebraic identity.

The classification is

```text
FRAME_NEUTRAL_REFERENCE_IS_TENSOR_FACTORIZATION_BLIND
```

## 2. Exact `D=32` control

The supplied five-qubit theorem fixture used in v15.03 has total dimension

```text
D = 32.
```

All unordered multiplicative decompositions with nontrivial factors are

```text
[32]
[2,16]
[4,8]
[2,2,8]
[2,4,4]
[2,2,2,4]
[2,2,2,2,2]
```

so

```text
unordered decomposition count = 7.
```

For every one of those decompositions the reconstructed product neutral state agrees with \(I_{32}/32\) exactly in the pinned numerical environment:

```text
max neutral factorization error = 0.0.
```

Only one decomposition contains exactly five nontrivial factors:

```text
[2,2,2,2,2].
```

That fact is arithmetic. It does not mean the neutral state selected five sites. The number of factors had to be specified before filtering the list.

Thus the implication

```text
tau_32 = I_32/32
therefore
five qubits
```

is invalid.

## 3. `Q_D(rho)=D rho` is also decomposition-blind as a definition

The relative-density operator from v15.07 is

\[
Q_D(\rho)=D\rho.
\]

This definition requires only the total Hilbert space and state. It does not require a tensor factorization.

For a supplied product state and supplied decomposition,

\[
Q_{d_1d_2}(\rho\otimes\sigma)
=Q_{d_1}(\rho)\otimes Q_{d_2}(\sigma),
\]

but this statement is conditional on already knowing what counts as the factors and that the state is represented as a product across them.

Hence the v15.07 product law composes a supplied factorization; it does not originate one.

---

# II. FULL FIVE-SITE PERMUTATION CONTROL

Suppose the five-qubit factorization is supplied explicitly:

\[
\mathcal H=(\mathbb C^2)^{\otimes5}.
\]

Then

\[
\tau_{32}
=\left(\frac{I_2}{2}\right)^{\otimes5}.
\]

Every site permutation \(\pi\in S_5\) leaves this state invariant.

The executable audit enumerated all

\[
5!=120
\]

factor permutations.

Results:

```text
permutations tested                 = 120
permutations preserving neutral tau = 120
max permutation error               = 0.0
```

Therefore

\[
\boxed{
\texttt{NEUTRAL\_FIVE\_QUBIT\_REFERENCE\_HAS\_FULL\_S5\_SITE\_PERMUTATION\_SYMMETRY}
}.
\]

The neutral reference contributes no site label.

This is precisely what one should expect from a frame-neutral object: its canonicality comes from refusing preferred internal structure, not from secretly encoding graph-node identities.

---

# III. DISTINCT SITE SPECTRA DO NOT CREATE A CROSS-DOMAIN FUNCTOR

A possible objection is that the actual supplied quantum state need not be neutral. Distinct local states can make the quantum factors individually distinguishable.

v15.09 therefore reuses the frozen v15.03 five-qubit product-state radii

\[
(0.15,-0.31,0.42,0.63,-0.22).
\]

Under independent local unitary gauge, the invariant local qubit information is the spectrum, equivalently \(|r_i|\).

The five spectral fingerprints are

```text
[0.425,0.575]
[0.345,0.655]
[0.290,0.710]
[0.185,0.815]
[0.390,0.610]
```

and are all distinct.

Thus the supplied five quantum sites are spectrally rigid:

```text
quantum-site spectral stabilizer order = 1.
```

The retained directed graph is also rigid. Exact edge-preserving permutation enumeration gives

```text
graph automorphism order = 1.
```

So both sorts are individually distinguishable.

That still does not identify them with each other.

## Two-sort independence theorem

Let the frozen structure consist of two sorts:

- retained nodes \(N\), with graph/source/provenance relations internal to \(N\);
- quantum sites \(Q\), with local spectral/operator relations internal to \(Q\).

Assume the frozen reduct contains no relation whose arguments include both an element of \(N\) and an element of \(Q\).

Then for every bijection

\[
\phi:N\to Q,
\]

one may expand the same reduct by adjoining \(\phi\).

Removing \(\phi\) returns exactly the same original frozen structure.

Therefore the reduct cannot entail a unique \(\phi\).

In the present five-by-five case there are

\[
5!=120
\]

such expansions.

Because the within-sort automorphism/stabilizer groups are both identity-only, none of the 120 supplied bijections are identified by earned gauge symmetry.

Thus

\[
\boxed{
\texttt{TWO\_SORT\_REDUCT\_DOES\_NOT\_DEFINE\_NODE\_SITE\_BIJECTION}
}
\]

with

```text
node-site bijections       = 120
inequivalent bijections    = 120
cross-domain relation      = NONE CERTIFIED.
```

This is stronger than saying that the neutral state is too symmetric. Even after the supplied quantum state makes every site spectrally distinct and the retained graph makes every node structurally rigid, a cross-domain identification remains an additional relation.

### Why sorting does not solve the problem

One could canonically sort the five quantum spectra.

One could also invent some canonical ordering of graph nodes.

Equating the two ranks would still be a new cross-domain rule. Nothing in the frozen ontology states that graph role rank, source grade, degree, provenance depth, or any other retained quantity is represented by local spectral rank.

Therefore sorting is not a derivation. It is a new representation principle disguised as bookkeeping.

---

# IV. THE `C^125` COMPATIBILITY PARENT BOUNDARY SURVIVES

v15.01 certified the compatibility parent

\[
\mathcal H_Q\cong\mathbb C^{125}
\]

with a \(25\)-dimensional support.

v15.03 proved that five nontrivial site factors cannot literally equal that parent.

v15.09 recomputes the integer factorization boundary.

The complete unordered nontrivial multiplicative decompositions of 125 are

```text
[125]
[5,25]
[5,5,5].
```

There is no five-factor decomposition with every factor dimension at least two:

```text
five-nontrivial-factor decomposition count = 0.
```

Hence

\[
\boxed{
\text{five nontrivial quantum sites}\ne\mathbb C^{125}\text{ compatibility parent}
}
\]

remains exact.

The supplied five-qubit carrier has dimension

```text
32,
```

not 125, and the audited frozen archive supplies no natural map from that carrier into the compatibility parent.

The v15.07 neutral state does not change Hilbert-space dimension and therefore cannot repair this type mismatch.

Classification:

```text
V15_07_NEUTRAL_STRUCTURE_DOES_NOT_REPAIR_C125_PARENT_TYPE_MISMATCH
```

---

# V. FROZEN DEPENDENCY REASSESSMENT

v15.09 hash-binds the exact reports needed to answer whether later results reopen the earlier representation gates:

```text
v14.04 REPORT  e5d9566bfc86c801d2933e63453d1800f60a675b
v15.01 REPORT  1afbb7aebe384a1fb761f99fd2b040e595be1fa5
v15.02 REPORT  be1281621b0e2872e555223b2c1cdb98fe9d8011
v15.03 REPORT  6c3aed73c63c9c7554107d163e15b8fae7549c1c
v15.07 REPORT  c3abb3af5b5c7210fc717392d4e2cc6fc4648284
v15.08 REPORT  23bbeaecdb81adfe1a39b3140569d23c367b8b55
```

The result is:

```text
CANONICAL_QUANTUM_INTRASORT_STRUCTURE_DOES_NOT_SUPPLY_CROSS_DOMAIN_CARRIER_ORIGIN
```

### v14.04 preserved

The provenance-to-quantum/support representation link remains missing.

### v15.01 preserved

The `C^125 -> C^25` parent/support chain remains exact, but no frozen provenance carrier is represented as the needed parent object.

### v15.02 not reopened

The 120-way node-to-quantum-label identification ambiguity is not repaired by the frame-neutral reference. The neutral reference carries less label information, not more.

### v15.03 not reopened

The exact retained graph is still not certified as a five-factor quantum system. The supplied five-qubit control remains a control, and the `C^125` arithmetic obstruction remains exact.

### v15.07 preserved positively

Nothing in v15.09 weakens the canonical quantum results:

- \(\tau_d=I/d\) remains the unique fully frame-neutral normalized state;
- \(Q_d=d\rho\) remains the canonical relative-density operator;
- centered \(\log\rho\) remains its canonical additive Hermitian generator.

The new statement is only that those objects are **intrasort**: they become available once the relevant Hilbert carrier/state is supplied. They do not originate the carrier itself.

### v15.08 preserved

The source-semantics branch stop is not reopened and is not used as a carrier selector.

---

# VI. WHAT v15.09 RULES OUT

The following proposed shortcuts are now explicitly blocked relative to the frozen ontology.

## 1. “The maximally mixed state reveals the subsystem decomposition”

False. It factorizes over every supplied tensor decomposition.

## 2. “Five qubits are canonical because 32 has a five-factor decomposition”

False. The number of factors must be supplied before selecting the unique five-factor integer partition.

## 3. “Distinct local spectra identify the retained nodes”

False. They identify quantum sites internally, not across the graph/quantum type boundary.

## 4. “Because both five-element sets are rigid, the correspondence is canonical”

False. Rigidity removes within-sort automorphisms; it does not create a cross-sort relation.

## 5. “The five-site carrier can now be viewed as the existing compatibility parent”

False. \(32\ne125\), and 125 has no five-nontrivial-factor decomposition.

## 6. “Choose the mapping that gives the best downstream geometry”

Forbidden. That would use the target as the upstream representation selector.

---

# VII. CLAIM BOUNDARY

## Derived / preserved

- the v15.07 frame-neutral reference and centered-log information generator;
- exact tensor-factorization blindness of \(I_D/D\);
- exact full \(S_5\) invariance of the supplied five-qubit neutral reference;
- graph automorphism order `1` for the retained five-node directed fixture;
- quantum-site spectral stabilizer order `1` for the supplied v15.03 control A;
- 120 distinct node-site bijection expansions of the same two-sort reduct;
- no five-nontrivial-factor decomposition of 125;
- preservation of v14.04, v15.01, v15.02, v15.03, v15.07 and v15.08 claim boundaries.

## Not derived

- a five-site quantum carrier from retained provenance;
- a retained-node-to-quantum-site functor;
- a physical meaning for matching graph invariants to quantum spectral invariants;
- a natural five-site-to-`C^125` parent map;
- a graph/provenance-to-support source representation;
- physical source semantics;
- absolute source magnitude;
- stress-energy;
- physical coframe/spacetime;
- Einstein equations;
- a physical time primitive;
- Pillar 3 closure.

No entropy, pruning, physical time, gravity, ADM, Einstein equation, cosmological target, or empirical residual is used to select the carrier.

---

# VIII. STATUS / STOP RULE

```text
v15.07 neutral state selects tensor factorization        : NO
D=32 nontrivial unordered tensor-dimension decompositions: 7
five-factor decomposition of 32                         : [2,2,2,2,2] only, conditional on asking for five factors
neutral five-qubit site permutations preserved          : 120/120
retained graph automorphism order                        : 1
supplied site spectral stabilizer order                  : 1
cross-domain node-site bijections                        : 120
inequivalent bijections                                  : 120
certified cross-domain relation                          : NONE
five nontrivial factors of C125                          : NONE
natural H32 -> C125 carrier map                          : NONE FOUND
primary outcome                                          : CANONICAL_NEUTRAL_STRUCTURE_DOES_NOT_DERIVE_RETAINED_QUANTUM_CARRIER
Pillar 3                                                 : OPEN
```

The carrier-origin branch therefore stops relative to the frozen ontology.

Do **not** continue by:

```text
reading subsystem labels out of I/d;
matching graph nodes to site spectra by sorted rank;
choosing a favorite node-site bijection;
using source semantics from the stopped v15.08 branch;
padding or reshaping H32 into C125;
inventing a random/SVD/PCA embedding;
selecting a map by downstream gravity/ADM/Einstein performance.
```

A lawful continuation requires an independently motivated cross-domain carrier/functor principle, explicitly marked **NEW ASSUMPTION**, or a redirect to an independent unresolved bridge.

---

# Scientific assessment

v15.09 is a **major structural no-go / representation irreducibility result**, not a broad scientific breakthrough.

Its significance is that v15.07's positive result does not dissolve the older representation problem. The canonical quantum information structure is real, but its canonicality is internal to an already-specified Hilbert carrier.

The remaining representation problem is no longer vague:

\[
\boxed{
\text{retained relational carrier}
\xrightarrow{\text{missing cross-domain functor}}
\text{quantum subsystem carrier}
\xrightarrow{\text{missing natural parent map}}
\mathbb C^{125}.
}
\]

Those arrows contain genuine information and cannot be recovered from frame neutrality alone.
