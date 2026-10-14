# Independent analytical review: exponential operation bridge

Date: 2026-10-14 UTC.
Reviewer: independent mathematical/source-scope review agent.
Repository named by the packet: proteinfoldingengine/WetLabEngine.
Branch named by the packet: research/uqcf-overlapping-guard-exchange.
Bound parent: 912fc7607cddd1583bb4bc80fe9c16f2e43ff331.
Bound tree: 22672152c9a35873b2efd5702750e1ae01b6ab31.

## Verdict and exact reviewed inputs

**ACCEPT for the exposed analytical argument and its bounded source interpretation. No substantive mathematical or source-scope defect found.** This acceptance is not native-interaction milestone acceptance, empirical validation, remote provenance verification, publication closure, or numbered-stage certification. The report's native milestone remains NOT ACHIEVED.

I reviewed these exact local inputs, independently recomputing their lengths and SHA256 values:

| Input | Bytes | SHA256 |
|---|---:|---|
| RESULT.md | 19166 | 3251b340ebee1d4241344b2a9608d4f485ca95477d429170f2a06b8de0749e04 |
| INDEX_APPEND.md | 2405 | 3107d7f6e097e1243b42f019d756d98360187349a4f2e851a1b5106c022bfa15 |
| source_packet.json | 182636 | deead2849f7f8457f7959a39c98dfb142237822afb54476227badd544f1d3bfd |
| source_identities.json | 3270 | 4fea8f54dcf6ab391a3e22c8eb7c7bbce66c0883d6b33ed68e9fd568fced5128 |

All twelve content strings in the packet agree internally with the manifest's UTF-8 byte counts, SHA256 values, and Git blob identities. I independently recomputed the blob identity as SHA1 of the standard blob header followed by the content bytes. This checks internal packet identity only. A separate auditor owns fresh remote parent/tree membership and publication provenance; I do not certify either from packet metadata or from matching internal hashes.

I read the packet's ResearchHistory/UQCF-GEM/AGENTS.md, the claim-bearing v13.04, v13.11, v13.22, v15.07 and v15.08 report bodies, and the actual v15.07 functions _pgrl_state, _neutral_to_state_endpoint_controls and _source_identification_boundary. I also checked the native milestone and physical-frontier decision, the finite-interaction assessment, the operational-source assessment's relevant implementation/scope discussion, and relevant continuation-index passages. Reading prior assessments supports the report's descriptions of those assessments; it is not independent recovery of every older source cited inside them or an archive-wide absence audit.

## Nonblocking precision notes

1. Step 1 says "For epsilon>0" before calling rho_(i,epsilon) faithful. Literally, arbitrary positive epsilon is too broad: the i population is 1-epsilon+epsilon/d. Take 0<epsilon<1, or simply sufficiently small epsilon>0, as is already required by the displayed limit. The proof uses only that valid neighborhood and is unaffected. This is a local domain-wording correction, not a loophole in the proposition.
2. The h=0 rejecting control correctly removes the success-conditioned B contrast. At exactly h=0, however, the failure effect is zero and its probability is zero, so no failure-conditioned state exists. The displayed failure formula is valid on the report's stated h>0 domain and has a limit as h approaches zero. The report does not rely on an actual failure event at h=0. If discussing that endpoint further, keep this distinction explicit.

Neither note requires a change to the theorem, the instrument example on its stated domain, the disposition, or the index's substantive claims. I have not edited RESULT.md or INDEX_APPEND.md.

## 1. Candidate, quantifiers, and operational meaning

The tested object is T_K(rho)=exp(log rho+K)/Tr exp(log rho+K), with fixed finite Hermitian K, on every faithful density matrix of one finite-dimensional complex Hilbert space. A successful branch must be one fixed nonzero completely positive trace-nonincreasing linear map from that input system to the specified output system. The quantifiers are important: the same E must work for all faithful rho, and K cannot change with rho.

The positive state-valuedness claim is correct. Hermiticity of log rho+K gives a positive definite exponential, and its finite positive trace gives a faithful normalized output. State-valuedness is not an operation theorem.

The report correctly distinguishes deterministic channels from conditional branches. A conditional normalized output need not be affine because its denominator is a state-dependent success probability. Therefore the deterministic midpoint example is properly treated as insufficient to exclude all postselection, and the stronger proof addresses CP branches directly.

The iff statement has the right nonzero condition. For a nonzero CP map, choose a Kraus representation and let F=sum_l A_l^dagger A_l. Then F is positive and nonzero. For any faithful rho with smallest eigenvalue lambda>0, Tr E(rho)=Tr(F rho)>=lambda Tr F>0. Thus faithful-input success positivity follows automatically, without assuming positive success at a pure-state boundary. In finite dimension a finite Kraus representation always exists. Trace-nonincreasingness is appropriate to an instrument branch, although the contradiction in fact does not require that additional bound.

The scalar direction is immediate and correct: if K=kI then T_K(rho)=rho, and E=id is CP, trace preserving, and nonzero. The report does not claim uniqueness of its realizing operation, which is unnecessary.

The resources covered by a fixed CP branch are described accurately. Aggregated outcomes, fixed independent ancillas, and fixed outcome-conditioned processing can all be absorbed into such a map when the final output is the specified system. Extra copies, input-dependent apparatus, matrix-aware control, approximate implementation, and restricted input families are distinct interfaces. A correlated ancillary resource changing with the input would not be a fixed independent ancilla under this premise. Nothing in the proof establishes a no-go for those excluded interfaces or for a nonquantum native theory.

## 2. Independent reconstruction of the all-input obstruction

### Boundary step and vanishing-success issue

Choose any orthonormal eigenbasis of K, writing its rank-one projectors Q_i and eigenvalues k_i. Repeated eigenvalues do not prevent this choice. For small positive eta, rho_(i,eta)=(1-eta)Q_i+eta I/d is faithful and diagonal in that basis. Its commuting tilt has populations proportional to exp(k_j) times its input populations, and therefore converges to Q_i as eta tends to zero.

Use the hypothesized identity without division:

E(rho_(i,eta)) = Tr E(rho_(i,eta)) T_K(rho_(i,eta)).

All quantities on the left and the scalar trace are continuous because E is a fixed linear map in finite dimension. The known normalized target tends to Q_i. Hence E(Q_i)=c_i Q_i with c_i=Tr E(Q_i)>=0. This conclusion remains valid when c_i=0. No boundary success was silently assumed, and no division by a vanishing boundary probability occurs.

Linearity now gives E(I/d)=(1/d)sum_i c_i Q_i. Its trace is positive by the nonzero-CP observation above. The target at I/d is exp K/Tr exp K. Matching its normalized diagonal entries forces

c_i = c exp(k_i), where c=(sum_j c_j)/(sum_j exp(k_j))>0.

In particular every c_i is strictly positive. A map whose success dies on selected eigenvectors therefore cannot evade the later ratio constraint. This explicitly resolves the most plausible boundary-success loophole.

### Complete positivity and multiple Kraus operators

For each i, E(Q_i)=sum_l |A_l i><A_l i| has support contained in the one-dimensional range of Q_i. For any vector v orthogonal to |i>, its expectation is sum_l |<v|A_l|i>|^2=0. Every nonnegative term must vanish. Thus every A_l|i> lies in span{|i>}, for each l and i. Each Kraus operator is diagonal in this eigenbasis.

This argument handles arbitrarily many Kraus terms in a finite representation. There is no cancellation of off-support vectors between Kraus terms because the summands are positive. It is therefore stronger than a single-filter calculation and not invalidated by aggregating outcomes.

Writing the diagonal Kraus entries a_(l,i), the diagonal output is

E(rho)_(ii)=sum_l |a_(l,i)|^2 rho_(ii)=c_i rho_(ii).

Thus for any density matrix with rho_(ii)=rho_(jj)=1/d, the output population ratio is exp(k_i-k_j). Normalization cannot change it. Off-diagonal dephasing or phase choices across the Kraus operators are irrelevant to this necessary diagonal relation.

Degeneracy causes no gap. Rank-one boundary projectors can be chosen inside every degenerate eigenspace, and the argument above holds in that chosen complete basis. If K is noncentral, at least one pair of distinct eigenvalues still exists; the final contradiction uses that pair. No assertion that all eigenvalues are distinct is needed.

### Coherent faithful witness in arbitrary dimension

For k_i>k_j, let delta=(k_i-k_j)/2>0 and 0<r<1. The candidate rho_r=[I+r(|i><j|+|j><i|)]/d has eigenvalues (1+r)/d, (1-r)/d, and 1/d in all remaining directions. Its trace is one and it is faithful for every d>=2. In particular all its diagonal entries are exactly 1/d, so the forced ratio applies.

The i,j block of log rho_r is

[-log d + (1/2)log(1-r^2)]I + artanh(r) X.

Adding K on that block gives bI+uX+delta Z, with u=artanh(r)>0 and b=-log d+(1/2)log(1-r^2)+(k_i+k_j)/2. The remaining d-2 directions form separate scalar blocks and cannot alter the ratio of these two populations. This justifies the arbitrary-dimension reduction rather than merely proving a qubit special case.

Let R=sqrt(u^2+delta^2)>delta. Since X and Z anticommute and square to I,

exp(uX+delta Z)=cosh R I+(sinh R/R)(uX+delta Z).

Its two diagonal entries have ratio (1+a)/(1-a), where a=delta tanh R/R. The common scalar exp b and the full-state normalization both cancel. Also 0<a<1, so the ratio is well defined.

For x>0, the derivative of tanh x/x has numerator x sech^2 x-tanh x. Multiplying by positive cosh^2 x gives x-sinh x cosh x<0, since sinh(2x)>2x. Thus tanh x/x is strictly decreasing. With R>delta this implies

0<a<tanh delta.

The function (1+a)/(1-a) is strictly increasing on (-1,1), so the target population ratio is strictly smaller than (1+tanh delta)/(1-tanh delta)=exp(2delta)=exp(k_i-k_j). This contradicts the CP branch's forced ratio. The inequality is strict for every chosen r in (0,1), however small the eigenvalue gap, without numerical tolerance or genericity assumption.

This establishes the noncentral direction and, with the scalar construction, the entire iff proposition. It is a general exact finite-dimensional theorem for the declared interface, not a finite no-counterexample conclusion. No approximation, series truncation, simulation, or input-boundary extrapolation beyond continuity is needed.

## 3. Deterministic rejecting control

For K=diag(log 3,0) and rho_p=diag(p,1-p), direct commuting evaluation gives f(p)=3p/(1+2p). The reported values f(1/4)=1/2, f(3/4)=9/10, f(1/2)=3/4 are correct. The average of the first two is 7/10, differing by 1/20 from the midpoint output. All three input states are faithful, and rho_(1/2) is their equal mixture. A deterministic linear channel cannot produce that behavior.

The report does not overextend this control. Conditional output states are allowed the very nonlinear normalization used here; their unnormalized branches remain linear. This distinction is scientifically useful and correctly retained by the stronger theorem and positive filter.

## 4. Restricted commuting realization and complete instrument

For k_max=max spec K, A_s=exp[(K-k_max I)/2] is positive and invertible, with eigenvalues in (0,1]. Its effect F_s=exp(K-k_max I) satisfies 0<F_s<=I. The positive square root A_f=sqrt(I-F_s) is defined and F_s+A_f^dagger A_f=I. Therefore the pair specifies a complete trace-preserving instrument when its outcome is retained or ignored as appropriate.

If [rho,K]=0, then rho also commutes with A_s, and

A_s rho A_s^dagger=exp(-k_max) exp K rho=exp(-k_max) exp(log rho+K).

Its trace is p_s=exp(-k_max) Tr(exp K rho), proving the conditional identity and exact success law. For a faithful input, p_s>0. Coherences inside a degenerate eigenspace are allowed: the condition is commutation with K, not diagonalization in a privileged fixed basis. This is an actual restricted-domain operation, conditional on the supplied apparatus and event interface.

For the qubit midpoint control, the stated A_s=diag(1,1/sqrt 3) and p_s=(1+2p)/3 follow directly. In particular the two equally likely mixture components have success probabilities 1/2 and 5/6. The conditional mixture weights become 3/8 and 5/8; combining their output populations 1/2 and 9/10 gives 3/4, agreeing with the midpoint branch output. Thus the success probability resolves the apparent affine conflict exactly.

The failure completion is a substantive rejecting control against treating a conditional map as an unconditional physical update. It also prevents silently retaining successful outcomes while omitting the operational price of knowing which outcomes succeeded. The report appropriately says that its chosen filter is an existence construction, not a derived native operation or uniqueness theorem. Preparing one classically specified target by a replacement channel is likewise a different supplied-resource problem and does not refute or solve the unknown-input proposition.

## 5. Two-qubit calculation, flags, and accessible consequences

Let q=exp(-2h), with h>0. In the Z_A eigenbasis, the local filter is diag(1,sqrt q), its effect is diag(1,q), and the failure operator is sqrt(1-q) times the negative-Z projector. The preparations rho_sigma=[I+sigma epsilon Z_A Z_B]/4, sigma in {+1,-1}, are faithful for 0<epsilon<1. Both have A and B marginals I/2. They commute with K=h Z_A tensor I_B.

Since the A marginal is the same, success has probability p_s=(1+q)/2=exp(-h)cosh h for either sign. On success, expanding (I+t Z_A)(I+sigma epsilon Z_A Z_B), t=tanh h=(1-q)/(1+q), gives exactly the report's normalized joint state:

[I+t Z_A+sigma epsilon Z_A Z_B+sigma epsilon t Z_B]/4.

Its B marginal is [I+sigma epsilon t Z_B]/2. The difference of the plus and minus B states is epsilon t Z_B; its trace norm is 2 epsilon t. Therefore the trace distance is epsilon tanh h>0, and Z_B readout has the reported conditional probability (1+sigma b epsilon tanh h)/2. Faithfulness and finite h ensure both b outcomes are possible for either sign. The report correctly presents a statistical difference rather than perfect one-event decoding.

The failure branch fixes A to negative Z, with probability p_f=(1-q)/2>0 and B marginal [I-sigma epsilon Z_B]/2. This verifies the signs and normalization in the failure formula. Since p_s t=p_f, averaging the two B marginals with their true probabilities gives exactly I/2 for either preparation.

One can see the record obligation directly in the complete flag-and-B law:

Pr(s,b|sigma)=p_s(1+sigma b epsilon t)/2,
Pr(f,b|sigma)=p_f(1-sigma b epsilon)/2.

Summing over b gives the same flag law for both signs; summing over the flag gives Pr(b|sigma)=1/2. The paired law differs because its flag-B correlations differ. In particular success-conditioned B contrast requires knowing the relevant subensemble or an equivalent justified heralded/joint interface. Mere receipt of unassociated B outcomes has no sign-dependent marginal. The report correctly leaves any physical link needed to associate separated records as an explicit resource obligation.

The unchanged B marginal is consistent with the general no-signaling property of a local trace-preserving instrument after its outcome is discarded. This is not a ban on conditional steering with communicated records. Nor is it a ban on a receiver obtaining a statistical consequence from a genuinely justified native restricted process. The text makes those boundaries explicit.

The epsilon=0 control correctly removes the preparation difference. The h=0 control correctly makes the success filter identity and the success-conditioned B contrast vanish, with the zero-probability failure caveat already recorded above. No independence of repeated trials, outcome guarantee, retention protocol, sampling error rate, or finite completion theorem follows from the single-use formulas; none is asserted.

## 6. Source interpretation and preservation of earlier positives

The source table is supported by the inspected claim-bearing texts. v13.04 section 1 explicitly places PGRL/ETL at a supplied faithful baseline and distinguishes its source coordinate from refinement. v13.11 gives the exponential family, first-order linearity, and the full-state/nonautonomous/kinematic boundaries. v13.22's exact tensor identity concerns supplied rho tensor tau and P tensor I; its positive CPTP refinement construction does not turn the nonlinear tilt itself into a general quantum operation or select a native event.

The actual _pgrl_state body receives base, generator and s, computes _logm_pos(base)+float(s)*generator, exponentiates that matrix, and trace-normalizes. The report's description of it is exact. It is not an implementation of an unknown-input quantum instrument: the matrix description is already supplied to an external calculation.

The actual _neutral_to_state_endpoint_controls body constructs a target-dependent logarithmic generator from _relative_density(rho), then calls _pgrl_state at the neutral reference. It does the analogous computation for a supplied product target. The report correctly calls this a conditional endpoint identity and does not accuse the source of having promised an all-input apparatus. The actual _source_identification_boundary constructs the three named local-source candidates on one common product state and compares their finite PGRL states and source rays. It supplies alternatives; it does not select a physical source law.

v15.07's canonical neutral reference, multiplicative relative-density operator, centered logarithmic generator and conditional endpoint theorem remain positive mathematical results. v15.08 expressly blocks identifying that information generator with a physical source under the frozen provenance/source-role premises and stops the repeated selector search. The new operational question keeps K supplied and does not reopen that stopped source-origin route, promote s to physical duration, or reinterpret the canonical logarithm as a native action.

The report also preserves the finite-interaction witness. That assessment uses a different supplied two-body unitary to transfer hidden global correlation into retained pair data; a no-go for universal exponential CP-branch reuse does not apply to it. Likewise a conditional channel/instrument/retained-algebra theorem remains valid when its channel, source binding and accessible outputs are genuinely premises. The inspected continuation records support preserving those conditional positives while leaving their native origin/access open.

The statement about v15.54 is properly attributed to the prior operational-source assessment, which traces its table input separately from listed permutations and confines its representation exclusion to the direct fixed-state/local-measurement interface. This review did not independently fetch v15.54 source bodies beyond that assessment's packet coverage; no broader verification is implied.

## 7. Milestone and governance scope

The user's criterion is one native informational difference forcing an accessible consequence without supplying the mechanism by hand. The milestone and physical-frontier sources explicitly permit derived probabilistic or restricted-class interactions without unique microscopic dynamics, deterministic outcome selection, guaranteed completion, full C3 closure, or gravity first. The reviewed report respects that criterion.

The universal faithful-domain proposition is framed as a specific proposed operational reuse, not a necessary demand on every native candidate. Its negative result therefore cannot be promoted to native impossibility. The commuting control gives a genuine conditional consequence but supplies qubits, preparations, frames, filter, application, occurrence flag and access/association. Because no inspected premise derives those resources natively, NOT ACHIEVED is justified for this candidate. Failure to achieve the milestone here is distinct from proving that no native mechanism can achieve it.

The next-resource discussion is appropriately scoped: earn the actual input class, operation, source/reference connection, event occurrence, record retention and readout. It does not impose all-input universality, deterministic selection, microscopic uniqueness or gravity as a new prerequisite. A native directly forced output law could establish a consequence without reproducing this particular apparatus; the report leaves broader alternatives open.

AGENTS.md requires typed arguments and forbids treating finite evidence as a universal proof. This record supplies a typed exact proof plus analytical controls. It does not run a new numbered scientific stage, relabel exposed calculations as prospective unseen tests, or claim CLOSED/CERTIFIED. No scientific import or execution, simulation, historical replay, numerical campaign, or scientific test-count increase occurred in this independent review. My only local execution parsed/read text and recomputed identity hashes. The separate publication/remote audit remains necessary for its own claims and cannot be replaced by this review.

Path A active, Path B closed, and time as pruning / ordered recoverability update are carried forward as existing program boundaries. The argument does not introduce physical energy, geometry, a Hamiltonian source identification, dark-matter variables, an entropy-based native law, an absolute scale, or a gravity-targeted selector.

## 8. Primary context and index consistency

I opened the primary PDFs cited by the report. Warmuth and Kuzmin, Bayesian generalized probability calculus for density matrices, Machine Learning 78 (2010), DOI 10.1007/s10994-009-5133-7, develops normalized log/exponential inference updates. Its introduction distinguishes that calculus from a physical quantum interpretation; sections 9 and 11 provide the update and contrast it with unitary evolution. This supports the report's limited prior-context statement, not the stronger CP-branch theorem proved here. No relative-entropy principle from that paper is adopted as native physics.

Source: https://escholarship.org/content/qt4hx9r95h/qt4hx9r95h.pdf

Watrous, The Theory of Quantum Information, chapter 2, Theorem 2.22 and section 2.3.2, supports finite Kraus representations and instruments with branch probabilities Tr Phi_a(rho), conditioned outputs Phi_a(rho)/Tr Phi_a(rho), and channel-valued total operation. These operational definitions match the tested interface. They do not establish a native quantum carrier or this research program's physical origin.

Source: https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf

I have not attempted a literature-priority search. The report makes no priority claim and does not attribute its CP-branch proof to those references. Its established-prior-art qualification is appropriate.

INDEX_APPEND.md accurately compresses RESULT.md. It retains the fixed-K, one-fixed-nonzero-CP-map, EVERY-faithful-input quantifiers; the diagonal-Kraus/coherent-block obstruction; the positive commuting filter and complete instrument; and the distinction between conditioned B, flag alone, and unconditioned B. It preserves the original kinematic results and v15.08 stop and leaves restricted processes and broader interfaces eligible. Its native status and no-execution/no-certification claims agree with the report. No substantive discrepancy was found.

## Final analytical disposition

The main iff theorem is sound in every finite d>=2, including spectral degeneracy, arbitrary finite Kraus representations and potential boundary-success collapse. The commuting realization and success/failure probabilities are exact. The two-qubit example identifies a conditional statistical consequence and precisely why its flag association matters, without claiming unconditional remote signaling or native access.

**ACCEPT: UNIVERSAL_EXPONENTIAL_INSTRUMENT_EXCLUDED; COMMUTING_FILTER_REALIZATION_CONDITIONAL; NATIVE_ACTION_AND_FLAG_ACCESS_OPEN. Native milestone NOT ACHIEVED.** The two minor endpoint/domain wording notes above are nonblocking. Fresh remote provenance, immutable publication and all broader physical closures are outside this verdict.

## Reconciliation of amended report and final verdict

Date: 2026-10-14 UTC. The author incorporated both nonblocking precision notes after the original review. This section appends the reconciliation; all preceding review text, original findings and original input bindings are preserved verbatim.

I independently compared the amended RESULT.md against the auditor's frozen original at audit_work/frozen_inputs/RESULT.md. That frozen copy has 19166 bytes and SHA256 3251b340ebee1d4241344b2a9608d4f485ca95477d429170f2a06b8de0749e04, exactly matching the original reviewed input. The comparison showed exactly two changed lines:

1. Step 1 changes "For epsilon>0, define faithful diagonal states" to "For 0<epsilon<1, define faithful diagonal states". This supplies a valid neighborhood of the pure-state limit and resolves precision note 1 without changing any proof step or quantifier of the theorem.
2. The endpoint-control paragraph adds "At h=0 success is certain, so a failure-conditioned state is undefined." and changes "Neither is needed" to "Neither control is needed". This resolves precision note 2 and preserves all success/failure formulas on their stated h>0 domain.

In addition to inspecting the unified diff, I reconstructed the amended text from the frozen original using exactly those two replacements and required complete equality with the current report. No other report change was present. The amended RESULT.md is independently bound as **19248 bytes, SHA256 254ed95093baa2bef2e166d7194499d9070cce6b1bad6229755c8d1871a83026**.

INDEX_APPEND.md, source_packet.json and source_identities.json remain byte-for-byte equal to their frozen copies, with the same lengths and SHA256 identities recorded in the original review table. The existing raw review before this append was independently checked as 24602 bytes, SHA256 b7a42aa05f4ee8561ca2a1193b882710f6dd1a550e1cb6fc935a3c3b59d4743a.

No scientific module was imported or executed, and no simulation, numerical campaign or historical replay was performed for this reconciliation. I edited only this raw review. The report and index were not modified by the reviewer.

**Final verdict: ACCEPTED for the amended RESULT.md and unchanged INDEX_APPEND.md, for the exposed mathematical argument and bounded source interpretation. Both precision notes are resolved; no substantive defect or remaining requested correction is identified.** The iff theorem, arbitrary-dimension and degeneracy coverage, multiple-Kraus argument, boundary-success reasoning, commuting realization, exact two-qubit probabilities, and record-access limits retain the conclusions established above. Native milestone remains NOT ACHIEVED. Fresh remote provenance, immutable publication closure, empirical validation and broader physical certification remain outside this analytical verdict.
