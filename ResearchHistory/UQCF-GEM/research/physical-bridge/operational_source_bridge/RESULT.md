# Operational source provenance and the direct quantum-state bridge

Date: 2026-10-14 UTC. Inspected parent: `6fd1a19d9757aa922a308782a6e751ee4660e188`.

**Disposition: supplied operational table identified; direct fixed-state/local-measurement quantum reuse excluded for the archived witness; native source acquisition remains open.** The v15.54 witness has a valid declared CHSH obstruction against its Bell-local comparator. Its probability table is an explicit input in the producer, not a probability law generated there by the listed permutations. The v15.55 scalar defect is calculated from that table. Neither calculation produces a native source event or receiver record.

There is also a precise representation restriction: the exact table cannot arise from one setting-independent quantum state with local binary measurements. An elementary perfect-correlation argument below establishes this for the archived table and an explanatory one-parameter family. This applies familiar Bell-correlation mathematics to a concrete proposed bridge; it is not a new general theorem, a priority claim, or a new physical interaction.

## 1. Candidate and relation to earlier work

The latest partial-complement result is conditional on actual quantum output states, an RQ factorization and permitted receiver measurements. To make progress upstream, this investigation asks whether the existing operational nonclassicality witness and its derived defect can supply that missing native source or a directly available record.

The earlier `COUPLED_C3_EVENT_ORIGIN_FOLLOWUP.md` inspected the v15.54 README and correctly observed that its scoped operational obstruction did not establish instrument provenance. This assessment goes further into the original frozen design, producer, independent verifier, retained reduction and v15.55 defect implementation. It also tests the specific direct quantum-state representation. The README-only conclusion is preserved, not counted again as a discovery.

The candidate being assessed is a proposed direct reuse: interpret the registered settings as local measurement choices on a single shared quantum state, preserve the registered probabilities, and then use quantum record/complement arguments to infer available consequences. This is a test of that interface, not a claim that the original v15.54 specification promised such a realization. The original specification expressly disclaims a derivation of quantum mechanics and a physical source law.

No new selector is sought in the already classified v15.55 response family. Its four-dimensional conditional freedom remains a historical result in its original scope. Nonuniqueness alone is not a rejection criterion: a common accessible consequence across justified mechanisms could qualify for the user's milestone.

## 2. Trace the probability law to its actual input

The inspected code separates five fields: id, control_role, carrier, operations and operational_table. In `operational_family.py`, the `_RAW` entry `CHSH_PREREGISTERED` has carrier [0,1], operations [[0,1],[1,0]], and this explicit table:

| Setting (x,y) | P(00|x,y) | P(01|x,y) | P(10|x,y) | P(11|x,y) |
|---|---:|---:|---:|---:|
| (0,0) | 1/2 | 0 | 0 | 1/2 |
| (0,1) | 1/2 | 0 | 0 | 1/2 |
| (1,0) | 1/2 | 0 | 0 | 1/2 |
| (1,1) | 0 | 1/2 | 1/2 | 0 |

Here a,b are outcome bits and x,y are context labels. Their role as physical settings or native choices is not derived by the names. Equivalently the table assigns probability 1/2 when a XOR b=xy and zero otherwise. Each single-output marginal is uniform for every context.

The input path is explicit:

| Source function | What it does | What it does not establish |
|---|---|---|
| `enumerate_raw_candidates` | Returns a deep copy of three literal candidate records | Does not derive the table from transformations or an event process |
| `check_admissibility` | Checks schema, metadata, carrier, permutation form, context/outcome domains and rational normalized probabilities | Does not bind the operations to probability-generating measurements or a shared state |
| `evaluate_witness` | Computes correlators and the CHSH score from operational_table | Does not acquire outcome samples or infer their native availability |
| `reduce_to_retained` | Returns the same literal four-object diamond data for every candidate | Does not retain the operational probability table or write a source-dependent record |
| `verify_nonclassicality._parse`, `_score`, `_retained` | Independently parse the supplied table, recompute its score and return the registered constant retained skeleton | Do not independently generate an operational process from the permutations |
| `derive_defect` in v15.55 | Computes max(0,abs(CHSH)-2) from the parsed table | Does not derive that table or a source-to-receiver action |

The full producer adjudication in `nonclassicality_search.py` consumes these fields, compares the retained reduction and structural classes, and checks the frozen comparator. The independent verifier has separate semantic code for the corresponding checks. This supports the bounded table/comparator claim; it is not evidence that a physical probability law was generated twice independently.

The original design explicitly states that witness data are not automatically retained observables. Its permitted positive verdict is confined to a frozen operational family, registered retained reduction and comparator class. The present assessment preserves that restriction. It does not reinterpret the old reported CI counts as new experiments, adjudicate the entire old certification stack, or modify historical code and verdicts.

For outcome signs (-1)^a and (-1)^b, write

    E_xy = sum_(a,b) (-1)^(a+b) P(a,b|x,y),
    S = E_00 + E_01 + E_10 - E_11.

The literal table has (E_00,E_01,E_10,E_11)=(1,1,1,-1), so S=4 and the v15.55 defect is D=2. These are exact consequences of the supplied table. They are not newly observed frequencies or a newly derived event law.

## 3. A control that exposes the unbound input without changing the listed operations

Fix the same carrier, permutations and candidate metadata. For a rational parameter alpha in [0,1], retain the first three rows and replace the last by

    P_alpha(00|1,1)=P_alpha(11|1,1)=(1-alpha)/2,
    P_alpha(01|1,1)=P_alpha(10|1,1)=alpha/2.                         (1)

Every row is rational, nonnegative and normalized. The single-output marginals remain 1/2 in all four contexts. The source-level candidate-admissibility predicates therefore accept each such individual record; requiring no-signaling marginals as an additional mathematical check would not distinguish them either. Direct substitution gives

    E_00=E_01=E_10=1,  E_11=1-2 alpha,
    S=2+2 alpha,       D=2 alpha.                                  (2)

The retained reduction remains the same diamond because the implementation does not inspect the candidate. Thus the listed carrier, transformations and retained skeleton do not themselves determine D in this declared schema. The extra information is supplied by the table field.

These controls are NOT members claimed to have been enumerated in the frozen three-candidate v15.54 campaign: that campaign fixes alpha=1 for this candidate. They are analytical schema controls, not a revision of its universe or an executed new search. The full candidate inputs differ in their table field; this is not an assertion that identical complete inputs produce different answers. A changed table causing a changed witness is expected and was already contemplated by the original design's mutation control. The family makes its dependence explicit without claiming that observation as a new physical theorem.

Schema acceptance is not native or physical admissibility. No physical interpolation, mixture preparation or freely available alpha is adopted. In particular alpha is a dimensionless table parameter, not elapsed time or a pruning rate.

## 4. Direct fixed-state/local-measurement representation is impossible for alpha>0

Specify the tested quantum interface precisely. Let a fixed density operator rho on a finite-dimensional H_A tensor H_B be independent of x,y. Each party has binary POVMs {M_0^x,M_1^x} and {N_0^y,N_1^y}, with setting dependence confined to its own factor. The probabilities would be

    P(a,b|x,y)=Tr[rho (M_a^x tensor N_b^y)].                        (3)

There is no joint-context operation, context-dependent preparation, conditioning on selected runs or communication between measurements in this interface. Locality here specifies the tensor-factor action; no spacetime geometry is introduced into the native research model. Equation (3) is a conditional representation test, not a newly adopted physical axiom.

Define the lifted Hermitian contractions

    A_x=(M_0^x-M_1^x) tensor I_B,
    B_y=I_A tensor (N_0^y-N_1^y).

They commute across parties, have operator norm at most one, and E_xy=Tr(rho A_x B_y). No projectivity, purity or full-rank assumption is required.

For a pair with E_xy=1,

    ||(A_x-B_y) sqrt(rho)||_HS^2
       = Tr(rho A_x^2)+Tr(rho B_y^2)-2
       <= 0.                                                     (4)

The squared norm is nonnegative, so it vanishes. Since each of the first two traces is at most one, their sum being two also makes each equal one. Consequently

    A_x sqrt(rho)=B_y sqrt(rho),
    ||A_x sqrt(rho)||_HS=||B_y sqrt(rho)||_HS=1.                    (5)

The first three perfect correlations therefore imply

    A_1 sqrt(rho)=B_0 sqrt(rho)=A_0 sqrt(rho)=B_1 sqrt(rho).

Taking the Hilbert-Schmidt inner product of the first and last expressions yields

    E_11=Tr(rho A_1 B_1)=1.                                      (6)

But (2) requires E_11=1-2 alpha. Thus (3) can realize this family only when alpha=0. This excludes the archived alpha=1 witness exactly, in every finite dimension and for arbitrary binary local POVMs. It also excludes arbitrarily small positive alpha within this exact three-perfect-correlation family; this stronger family statement follows from the perfect equalities, not from a numerical comparison with a CHSH upper bound.

The endpoint alpha=0 supplies a substantive positive control. The shared state

    rho_0=(|00><00|+|11><11|)/2

with both choices on each party measuring Z gives all four correlated rows. Equivalently, both outputs equal one shared fair bit. This is a realization of the endpoint probability table; it is not claimed to derive measurement semantics for the archived permutation list.

The archived alpha=1 table is the familiar Popescu-Rohrlich correlation table, whose distinction from shared-state quantum correlations is established prior art. The argument above is a self-contained proof for the exact source interface being tested, not a new no-go theorem for quantum mechanics or a proposal that the native theory must be quantum.

## 5. Controls against overextending the exclusion

The restriction is to equation (3). There are straightforward representations and procedures outside that interface.

**A stored classical table can be a quantum state.** For any P_alpha, the diagonal matrix

    Omega_alpha=(1/4) sum_(x,y,a,b) P_alpha(a,b|x,y)
                  |x,y,a,b><x,y,a,b|                             (7)

is positive with trace one. Reading its context registers and conditioning produces the registered table. This does not contradict (6): the context values are correlated with the output preparation inside Omega_alpha, rather than independently chosen measurements on one fixed AB resource as in (3). It is a representation of already supplied data. It does not derive native sampling, acquisition, measurement availability or retention. We therefore do NOT claim that the probability table cannot be stored in a Hilbert space, encoded in a density matrix, or included in any quantum process.

**A joint-context sampler realizes the table.** Give a joint processor x and y, an independent fair bit lambda, and an independent bit c with P(c=1)=alpha. Define

    a=lambda,       b=lambda XOR (c x y).                         (8)

The first three contexts are correlated; the last is flipped with probability alpha. These are exactly (1), with uniform marginals. The processor has access to both contexts, so it does not have the local-response structure of (3) or of the Bell-local comparator. It explicitly supplies the processing rule and randomness. It is an analytical rejecting control against a blanket impossibility claim, not an inherited native mechanism or a proposed added physical law. A separated implementation would need its own communication/resource contract; none is inferred here.

Known channel/process formulations also distinguish such behavior from correlations of local measurements on a shared state. No broader quantum-process or nonquantum theory is ruled out by this assessment. Direct state reuse would require preserving the interface in (3); choosing a different preparation, nonlocal process or coarse encoding requires a separately justified map and access contract.

## 6. Which record actually carries the distinction?

For every alpha in the explanatory family,

    P_alpha(a|x,y)=P_alpha(b|x,y)=1/2.

A receiver given only its own outcome and fixed own context has the same one-shot probability law for all alpha, and that law is independent of the other setting. These statements concern the supplied tables, not any unmodeled memory or repeated-use protocol. No across-run independence or complete channel semantics is assumed.

With access to paired outcomes and the context (1,1), the parity a XOR b instead has probability alpha of being one. At the two endpoints it distinguishes the tables perfectly in that context. This is a genuine conditional joint-record contrast. It is not accessible merely because the joint probability table appears in an analysis file: the mechanism producing paired outputs, their common reference, context association, capture and retention must be earned.

The registered retained diamond does not include those probability or joint-outcome fields. v15.55's `derive_defect` reads operational_table in the candidate input, rather than reconstructing D from that diamond or receiving a native event stream. This is appropriate for its mathematical classifier. It does not establish a source-dependent write into the declared retained output. We do not equate the external verifier's data access with an event's access, and we do not prohibit a future system-side interaction from depending on its actual source.

The four surviving response parameters in the archived v15.55 result remain available under their original assumptions. This assessment neither chooses them nor treats nonuniqueness as a reason to reject every common consequence. Its earlier blocking premises are the source/table origin and a justified output interface, with the additional exact restriction on the proposed direct local-quantum representation.

## 7. Scientific decision

| Proposed inference | Finding |
|---|---|
| The supplied v15.54 witness has S=4 and no Bell-local comparator | Preserved within the original declared scope; not freshly rerun |
| The permutations themselves generate its probability table | No such dependence is present in the inspected producer or verifier |
| The v15.55 defect is computed from the registered table | Yes, D=2 for the frozen witness; this is a supplied-data calculation |
| A single setting-independent quantum state with local binary POVMs realizes that table | Excluded by (4)-(6) |
| The table cannot have any quantum encoding or general processing realization | False; (7)-(8) show why the narrower interface matters |
| A single local output exposes the source parameter in this family | No; its distribution is uniform for every alpha |
| A justified paired-output/context interface could reveal a distinction | Yes; its parity law changes, but that native interface is not supplied here |

The direct route from this operational witness to a native quantum source/receiver is therefore **not admitted**. The exact local-quantum representation is excluded; broader process and acquisition routes remain unestablished rather than impossible. This is a source/representation assessment, not a new physical source law or a withdrawal of the scoped operational nonclassicality result.

The next admissible advance must identify an inherited producer deriving a probability or transition law from native inputs, plus a justified record interface that can access the resulting difference. If this table is reused, its operation-to-outcome relation must be supplied by that derivation, and its representation must respect the source's actual context/resource structure. Registering the table, encoding it in a state, selecting a response coefficient or choosing the sampler above would supply the mechanism by hand. The q^2 partial-access bound cannot fill those upstream obligations.

The native milestone remains **NOT ACHIEVED**. Conditional RAS/RCR, source binding/grade, retained record-compatible order and the recent quantum-channel results retain their original scopes. A derived probabilistic consequence may qualify without deterministic selection, unique microscopic dynamics, guaranteed completion, full C3 or gravity closure. This audit adds none of those requirements. Its absence claims are confined to the inspected implementations; it is not an archive-wide impossibility result.

Disposition code: `SUPPLIED_OPERATIONAL_TABLE; DIRECT_LOCAL_QUANTUM_STATE_BRIDGE_EXCLUDED; NATIVE_ACQUISITION_OPEN`.

No scientific code was imported or executed, no enumeration or numerical campaign was launched, and no historical test count was increased. The displayed controls and proofs are analytical and already exposed; they are not retrospective preregistration. Text/hash/provenance checks establish identities only. No main merge, historical recertification or numbered-stage CLOSED/CERTIFIED status is claimed. Path A remains active, Path B closed, and time remains pruning / ordered recoverability update. No energy, force, clock, spacetime, metric, dark-matter primitive or gravity-targeted selector is introduced.

## 8. Source and review boundary

Nineteen exact GitHub sources at the pinned parent are preserved in `source_packet.json` and `source_identities.json`. They include governance/milestone/continuation records, the prior event-origin assessment and partial-access report, the v15.54 design and relevant producer/verifier code, and the v15.55 defect/response records. The source inventory is deliberately bounded. Historical certification words inside unchanged sources report their old scope; they do not certify this investigation.

Primary mathematical context consulted 2026-10-14:

- Sandu Popescu and Daniel Rohrlich, *Causality and Nonlocality as Axioms for Quantum Mechanics*, arXiv:quant-ph/9709026, section II: https://arxiv.org/abs/quant-ph/9709026 . The paper distinguishes the CHSH quantum-state bound from nonsignaling correlations attaining four. This is prior context, not a new result attributed to this audit.
- Martin Plavala and Mario Ziman, *Popescu-Rohrlich box implementation in general probabilistic theory of processes*, arXiv:1708.07425v2, sections 2, 4 and 6: https://arxiv.org/html/1708.07425v2 . Its channel/process treatment reinforces why the exclusion must retain the fixed-state/local-measurement qualification. No process from that paper is adopted as native dynamics.

Independent whole-argument review and a separate source/publication audit accompany this record. Their conclusions are limited to the exposed mathematical argument, source assessment and immutable publication; they do not establish the physical milestone.

