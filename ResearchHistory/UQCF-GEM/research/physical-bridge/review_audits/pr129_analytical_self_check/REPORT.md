# PR129 analytical self-check and exact remaining corrections

Date: 2026-11-01 (America/Phoenix).
Assessed PR head: 85db2dde33896e3de68c4b4623c09a58e65a8c5d.
Disposition: REVISE wording/domain record; corrected mathematical core survives this self-check.
Native bridge: NOT_DERIVED. No physical advance claimed.

## Review identity and limits

A fresh-context reviewer reconstructed the package without receiving past review verdicts, then the coordinating session checked the findings against the exact sources. The reviewer inspected RESULT.md, CORRECTION_T241.md, CORRECTION_T242.md, PREREGISTRATION.md and successor_t241/{README.md,produce_s.py,verify_s.py,test_controls_s.py}, plus the source interfaces listed below.

This is same-agent-lineage SELF-CHECK, not independent external acceptance. The coordinating session previously contributed the range-theorem repair; that contribution is another reason not to count this as independent acceptance of the whole proof. The existing Gemini response remains separate, with its seven affirmative findings and failed empty-findings gate preserved by review_audits/t246. No new model request, numerical experiment, producer run or certification is claimed.

## Finding 1: signed statistic versus absolute contrast

CORRECTION_T241.md §3 RD-7(ii), lines 24 and 28, calls the expression (f_p-f_v)/5 the pair contrast. successor_t241/README.md line 19 and both implementations define a fixed effect's contrast using an absolute value.

Exact counterexample: take the legitimate effect F=pi_v tensor I_K. For every implementing realization, its retained diagonal blocks are F_p=0 and F_v=I_K. The benchmark pair therefore gives

    s_F(W) = Tr[F W(rho_plus-rho_minus)W*] = -1/5,
    c_F(W) = |s_F(W)| = 1/5.

Negative contrast is not consistent with the frozen absolute convention. This does not refute the scalar-block classification.

Precise repair for Hermitian observables (in particular effects):

1. Define s_F as the signed statistic and c_F=|s_F| as the absolute contrast.
2. RD-7(ii)'s invariant signed value is (f_p-f_v)/5; its invariant absolute contrast is |f_p-f_v|/5.
3. To apply the signed necessity proof to absolute invariance, insert the following argument. The implementing realization class is the continuous image of connected U(K) acting on a fixed isometry. Thus it is connected. For Hermitian F, s_F is continuous and real. If |s_F| is a fixed positive constant c, its image lies in {-c,c}; connectedness forces one sign. If c=0, s_F=0. Absolute invariance therefore implies signed invariance on this class.
4. The original common-orthogonal-vector proof then applies when dim K>=3. For dim K=2, the signed condition F_p+F_v scalar also characterizes absolute invariance after the same argument.

This supplies the missing argument, rather than merely changing the displayed sign. The listed implementation examples use abs correctly; their positive/sign-insensitive fixtures did not expose the text mismatch. No old numerical output needs to be changed.

Related typing repair: RD-7 starts with unrestricted F in B(H_S tensor K) but calls the representative an effect. Either restrict the effect statement to 0<=F<=I, or call it an operator/statistical representative in the unrestricted statement. F=2I has representative 2I on the retained subspace, which is not an effect. For genuine effects, scalar retained blocks satisfy 0<=f_j<=1; extend the representative with zero on the unused u coordinate to obtain an effect on H_S.

## Finding 2: a disclosed finite-domain amendment

CORRECTION_T241.md §4 V5(i) asks for three exact non-basis realizations from the V2 family. successor_t241/README.md lines 15–16 accurately discloses that the third implemented realization is W_N, outside that family: its e_0=(3|00>+4|11>)/5, whereas V2 fixes e_0=|00>.

The disclosure should be classified as a pre-execution domain amendment/deviation, not an option the frozen family condition left open. V2's four frozen sample points include only two non-basis points, but the continuous family has other exact points (e.g. cosine 5/13). This observation is not a request to add a new sampled campaign.

The existing computation verifies its actual six-realization domain and remains valid bounded evidence. Preserve the original plan, disclosure and outputs. Amend the compliance description; do not relabel the substituted domain as literal satisfaction of the original V5(i). The W_X choice in V5(ii) is different: that item had not specified the two named realizations, so the disclosed choice is compatible with its wording.

## Reconstructed surviving proof

All statements here retain the supplied benchmark Hilbert space, exact coherent channel C, preparation pair, blank complement and receiver-interface assumptions.

| Claim | Reconstruction and scope |
|---|---|
| RD-0/0' | Pure output marginals force product columns; retained coherences force one e_0; isometry gives e_u perpendicular to e_0. Basis completion gives one U(K) orbit, hence all-or-empty for invariant predicates. |
| RD-1 | Valid for exactly the inspected predicates factoring through native source data and C, with a nonempty admitted class. This does not classify every future inherited joint-event rule. Covariance of a supplied projector is not ownership of a fixed R projector. |
| RD-2 | Lifting source effects supplies the lower bound d_S. A common K_A state with orthogonal hidden K_B flags attains it; compression into A_S proves equality. |
| RD-3/4 | Full-complement optimized contrast is invariant, while individual fixed effects need not be. RD-4 concerns universal positive delivery in the specified product-interface class, not constant contrast or a unique physical postulate. Initial blindness remains separate. |
| Corrected range | For both factors of dimension at least two, the hidden endpoint attains d_S and the accessible flag attains 1/5. The continuous connecting family attains the interval, bounded globally by input trace distance. Constant optimized contrast occurs iff d_S=1/5. |
| RD-5/6 | Complement statistics depend on z_u, retained-source statistics on y_p=z_p+z_u. The equal-pushforward pair is blind on S after, not necessarily before. For designated R, delta_R=D(tau_u,tau_0)/5; avoiding the blind set is the exact criterion, not an independently justified new physical law. |
| RD-7(i) | Retained input point masses allow arbitrary unit e_0. Constant quadratic forms force scalar retained diagonal blocks. Off-diagonal and removed-source blocks are not constrained. Statistical equivalence does not imply algebra membership. |
| RD-7(ii) | Common orthogonal vectors in dimension at least three force F_p and F_v scalar. Use the signed/absolute repair above. |
| RD-7' | Product-interface slice maps retain positivity and membership in A_S. T242's controlled-unitary counterexample correctly prevents generalizing this owned-effect conclusion to arbitrary interfaces. |

The self-check inspected the producer and stdlib verifier without executing them. Their exact rational/radical reconstruction, V6 intersection test and V7 linear constraints are appropriate to the frozen implemented examples. This is not a general theorem verifier. Prior byte-exact replay evidence is in review_audits/t246; it is not counted as new execution in this review.

## Retained-record source trace and admission decision

At research head 56aa2ba1498195bcc9a4abb3ee5937ae9cc44bed, v15/v15.11/REPORT.md §§3–4 explicitly supplies RAS and RCR. ontology_continuity_audit.py::select_record requires the projector family and actual record index; center_persistence_control distinguishes algebra inclusion from record preservation. The sufficient condition Z(A) subset B subset A retains old central records within specified algebras; it does not assign either algebra to the designated P1 receiver.

measurement_first_review/RESULT.md §§2–4 already states the exact boundary: fiber-compatible event restriction preserves a specified event, and a fiber-cutting event requires an additional retained algebra. The event's source association and receiver ownership remain obligations. constructions/recoverable_pruning_ledger/FROZEN_ARGUMENT.md §§5–6 and its mission ledger retain A/RCR as open access premises.

Admission questions: the attacked premise is source-associated actual record delivery to R; the candidate is inherited record-compatible retention; the adversary is W_E; success would supply a changed R-owned effect; the falsifier is that the algebras, record and ownership are inputs. The inspected sources exhibit that falsifier. Neither W_R nor W_E literally instantiates an arbitrary RAS/RCR specification until that specification is typed onto the joint output. Source-only instantiations do not separate them; adding receiver-local record ownership supplies the missing premise.

This is confirmation of an already recorded boundary, not a new no-go theorem or permission to redesign the retained algebra. No new substantial work item is admitted on this chain.

## Publication disposition

The original PR files and raw Gemini response remain unchanged. These findings are a completed analytical self-check with concrete repairs. They do not confer independent acceptance, remove the Gemini schema deviation, approve PR129's merge, or close native receiver delivery. No numerical rerun is requested merely to correct terminology or document the already disclosed domain amendment.
