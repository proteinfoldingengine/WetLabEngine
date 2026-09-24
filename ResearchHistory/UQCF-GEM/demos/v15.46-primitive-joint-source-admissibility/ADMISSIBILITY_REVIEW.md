# v15.46 — Native-input and incidence-typing review

**Review date:** 2026-09-23 (America/Los_Angeles).  
**Reviewed repository head:** `20650af8d9583383925efc570026666b47d12788`.  
**Preserved v15.45 head:** `23cc8642ca484e23a3a4e809cf83ed325d9f25ba`.  
**Status:** bounded source-admissibility investigation; local exact mathematical checks and scoped source review. Not full v15.46 certification, a new adopted source law, or independent peer review.

## Decision

The conditional modular operator remains a mathematically defined candidate when the joint state and subsystem inclusions are supplied. The reviewed records do not establish the complete native-input-to-incidence chain for it. The immediate decision is:

`SOURCE_OPERATOR_DEFINED_BUT_INCIDENCE_COUPLING_UNSPECIFIED`

with the separate provenance status:

`NATIVE_JOINT_INPUT_NOT_CERTIFIED_IN_SCOPED_INVENTORY`.

This does **not** mean that the repository has no joint quantum states. It has several. It means that mathematical state construction, primitive provenance, subsystem identification, and incidence coupling are distinct obligations. The inventory below must not be represented as an exhaustive search of every historical file or connected account.

No new curvature simulation is warranted by this review. No old source rule, response operator, result ledger, workflow, or v15.45 branch is changed.

## 1. What is actually present

Every path and Git blob used for this review is in `docs/INPUT_TYPE_INVENTORY.json`. The inventory is a source-review record, not a machine proof that no other archive contains a missing law.

| Candidate / record | Supplied mathematical object | What remains unearned for this candidate |
|---|---|---|
| Compatibility laboratory | Explicit tripartite `(C^5)^tensor3` parent and partial traces; `build_completion` selects a feasible representative | The code itself labels the representative a mathematical selection, not a physical selection rule. The audited parent has dimension 125 and support 25. Full-parent faithfulness is absent in that audited configuration; no primitive source covector was certified. |
| Six-qubit demo | Explicit dimension-64 thermal joint state `exp(-beta H)/Tr exp(-beta H)` and tensor sites | The graph, couplings, fields and source operator are supplied demo choices. It is a usable conditional state, not a Genesis-derived joint preparation or incidence dictionary. |
| Coherent-record simulator | An isometry from four system qubits into four system plus four initially blank record qubits | The registers, gates and schedules are diagnostic supplied structure. The complete joint image has rank at most 16 in dimension 256. Classical record data do not uniquely specify the coherent dilation. A separately chosen reduced triplet may be faithful, but its selection/inclusions must be supplied. |
| Canonical neutral-reference structure | `I_d/d` and centered `log rho` once a Hilbert space and state are supplied | v15.09 records that this does not select a tensor decomposition or a retained-node/site identification. |
| v15.39 incidence source | An oriented occurrence `(f,e,a)` with a boundary source proportional to `B2 e_f` | A face address exists in this conditional model. There is no reviewed certified relation saying which quantum joint-state/overlap record belongs to that occurrence, or which scalar/operator functional becomes its amplitude. |
| v15.46 parity/noncommuting examples | Faithful tripartite test states and declared subsystem inclusions | These are explicit mathematical fixtures. They establish candidate properties and a no-descent counterexample, not primitive source provenance. |

**Important distinction about support.** A logarithm on a 25-dimensional support is not automatically the same object as the four logarithms lifted from tripartite subalgebras on a 125-dimensional parent. Compression must preserve or explicitly replace the subsystem/inclusion structure. It cannot be treated as an invisible dimensional relabeling. No epsilon regulator, maximum-entropy completion or downstream-selected support is introduced.

The support limitation of the coherent model follows from the isometry: `rank(V rho V^dagger)=rank(rho)<=16`. It concerns the complete eight-qubit joint state, not every possible reduction of it.

## 2. The candidate and its existing boundary

For supplied faithful `rho_ABC` and supplied tensor inclusions,

    D = log rho_ABC - log rho_AB - log rho_BC + log rho_B

is Hermitian, with the standard identity embeddings understood. The logarithmic equality condition and recovery/quantum-Markov interpretation are prior art [R1,R2]. The prior research decision establishes the precise scope of the candidate; this review does not invent that operator.

For `rho_r=(I+r Z tensor Z tensor Z)/8`, all proper one- and two-body marginals are independent of r, while D differs at r=0 and r=1/2. The prior exact 195-check output was rerun in this session and matched its committed companion output byte-for-byte. Thus pairwise-only data cannot determine this D across all faithful completions. An actual joint-state input avoids that particular ambiguity; choosing a convenient completion is an additional rule.

Independent-copy additivity is not signed-event linearity and not linearity in rho. The candidate is also not positive in operator order in general. Taking a trace, an expectation, a norm, or an exponential is a new interface decision unless an independently justified law already supplies it.

## 3. Operator-to-scalar typing: a conditional trace-only lemma

Let `H=H_A tensor H_B tensor H_C`, `d=dim H`, and let V be a real target vector space on which independent local quantum frame changes act trivially. Suppose

    T : Herm(H) -> V

is a real-linear map of the operator alone, with no co-transforming state, observable, quantum-to-cell dictionary, or other background input, and

    T(U X U^dagger)=T(X)

for every product local unitary U. Averaging independently over the local unitary groups gives

    average_U U X U^dagger = (Tr X/d) I,

hence

    T(X) = (Tr X/d) T(I).

In particular, every traceless component is annihilated. The finite probe verifies the twirling identity on every matrix unit for one, two and three qubits: 4+16+64=84 units. Product X/Z conjugations suffice; phases converting XZ to Y cancel. This is familiar depolarization mathematics [R3], applied here as a typing constraint, not a claim of a novel general theorem.

**Limits:** this lemma does not exclude state-conditioned expressions such as `Tr(rho X)`, covariantly supplied observables, operator-valued targets or nonlinear functionals. In those cases its hypotheses change. Nor does it assert that linearity in D is already a physical axiom: linearity in signed event amplitude is a different statement. The point is to make the proposed interface explicit, not to assume it into impossibility.

## 4. No unaddressed boundary source on the homogeneous torus

There is a stronger address obstruction relevant to the existing target `B=im(B2)`.

Let G be the two-dimensional finite translation group on the oriented periodic square torus. It acts transitively on consistently oriented faces. Let `C2` be the face-coefficient space and `B2:C2->C1` the oriented boundary map. It is equivariant, and

    B2 1 = 0.

If `b=B2 c` is fixed by every translation, then

    b = average_g g b
      = B2(average_g g c)
      = B2(mean(c) 1)
      = 0.

Therefore

    (im B2)^G = {0}.

Now suppose a quantum input x — D alone, or a supplied pair `(rho,D)` — carries **no incidence address and no nontrivial cell-translation action**. Any equivariant map `kappa(x)` into B must obey `g kappa(x)=kappa(x)` for every g. Consequently `kappa(x)=0`. This address result does not require linearity of kappa.

This conclusion is conditional on the unaddressed input, independent cell symmetry and this boundary-sector target. It is NOT a theorem against all possible quantum-to-geometry laws, all graphs, or all richer inputs. In particular, v15.39 already has an addressed source occurrence; that structure is not being denied. The missing object is the link from the quantum record to such an occurrence and its amplitude rule.

The finite probe independently constructs the two boundary matrices and translation actions. It checks `B1 B2=0`, boundary rank, and the rank of the stacked translation-invariance constraints restricted to an independent boundary basis.

| Period | rank B2 | Invariance-constraint rank on B | Translation-fixed dimension in B |
|---|---:|---:|---:|
| 5 | 24 | 24 | 0 |
| 6 | 35 | 35 | 0 |
| 7 | 48 | 48 | 0 |
| 8 | 63 | 63 | 0 |

These are ranks of **B2**, not ranks of the v15.45 curvature operator A. No rank threshold or spectrum query is used. The obstruction occurs on both odd and even examples; it is not an attempt to eliminate the v15.45 even-grid curvature null modes.

**Target sensitivity:** nonzero translation-invariant circulations do exist in `ker(B1)` outside `im(B2)`. A horizontal periodic circulation is an explicit tested countercontrol. Thus the result must not be silently enlarged from the boundary sector to the full cycle space.

## 5. A nonzero control shows exactly what extra input changes

If a face occurrence f and scalar a are explicitly supplied, then

    kappa(f,a)=a B2 e_f

is a nonzero boundary source for a nonzero amplitude. It is closed, transforms covariantly when f is translated, and reverses sign with a. These properties were checked at L=5,6,7,8.

This is a sensitivity control: it demonstrates that the obstruction is not due to a verifier incapable of accepting a nonzero source. It does not recover the face occurrence from the quantum state or determine a from D. Merely reusing the same label on two different objects would insert the missing identification, not derive it.

Neither the trace-only lemma nor the address lemma selects a response function. The v15.31 nonuniqueness result and v15.37 frozen-selector branch stop remain in force. No old CMI selector search is restarted.

## 6. The smallest next admissible object

A candidate interface must provide all of the following before a geometry-facing test:

    native record R
       -> (joint state, subsystem algebras and overlap inclusions, support rule)
       -> declared occurrence/face identification
       -> Gamma_R(rho,D) in C2 / span{1}
       -> kappa_R = B2 Gamma_R(rho,D) in im(B2).

The quotient only states the existing kernel equivalence of face coefficients. It is not a new representative-selection rule. Gamma need not have the trace-only form when it has additional declared inputs, but every such input and its symmetry action must be explicit.

The contract must distinguish three logically different outcomes: a map derived from existing native records; a consistent map introduced as a NEW ASSUMPTION; and an absent/ill-typed map. A consistent new map is not automatically selected by physics. All variants must be fixed independently of downstream curvature results.

The next action is therefore an upstream occurrence-to-subsystem dictionary and coupling proposal, or a precise closure if no such principle is supplied. It is not another run of a source-response identity already encoded in the model.

## 7. Execution and documentation boundary

- Local runtime: CPython 3.13.5.
- Eight new focused tests first failed with eight missing-module assertion failures, then all eight passed. No skipped tests.
- The prior 195-check mathematical screen replayed identically.
- New JSON output replayed byte-for-byte. Compilation passed.
- The probe uses exact integer/Fraction arithmetic and no third-party packages.
- This is local research verification, not a full repository regression, GitHub Actions certification, or independent peer review. Newly shown examples are exposed.
- The source inventory is author analysis of the declared pinned records. Missing certification in this inventory is not a proof that all conceivable records lack it.
- No new source law, primitive state, physical stress-energy or gravity correspondence is claimed. Pillar 3 remains OPEN.

The execution hashes and local RED/GREEN records are in `docs/TYPING_EXECUTION.md`. The written v15.46 execution contract is a draft for the next implementation stage, not a claim that that stage has executed.

## References

[R1] M. B. Ruskai, *Inequalities for Quantum Entropy: A Review with Conditions for Equality*, arXiv:quant-ph/0205064. https://arxiv.org/abs/quant-ph/0205064

[R2] P. Hayden, R. Jozsa, D. Petz, A. Winter, *Structure of States Which Satisfy Strong Subadditivity of Quantum Entropy with Equality*, arXiv:quant-ph/0304007. https://arxiv.org/abs/quant-ph/0304007

[R3] IBM Quantum Learning, *Quantum channels*, completely depolarizing channel via equal Pauli conjugations. https://learning.quantum.ibm.com/course/general-formulation-of-quantum-information/quantum-channels

These sources support the information-theoretic background, not physical source identification or a novelty claim. Repository evidence and its provenance are separately recorded in `docs/INPUT_TYPE_INVENTORY.json`.
