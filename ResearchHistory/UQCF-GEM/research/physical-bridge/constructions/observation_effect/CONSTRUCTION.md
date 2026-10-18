# Construction: observed vs unobserved receiver record. The effect of an ordered recoverability update

Author: proteinfolding-grokbot (UQCF Science Agent).
Draft 1, 2026-10-17 America/New_York (~22:00 ET loop). Baseline research head `bb1fd75b965f4ed8208c50a5a3d430f3c7b33aa1`.
Draft 2, 2026-10-17 America/New_York (~23:00 ET loop). Baseline research head `4de08e31f2b09cefa845f9fa4060cedcbd7ad9ce`. Adds section 12 (the occurrence record: when a receiver can read THAT an observation occurred) and adopts GPT's four accepted corrections (see "Draft 2 changes" below).
Mode: CONSTRUCTION MODE (STANDING_DIRECTIVE addendum (b)). Directives followed: Aaron's 21:46/21:47 ET pre-time vs time-constituting wording and his 21:50 ET reading: "the model contains the EFFECT of observation, not its cause: if you start to observe and prune, the network changes; absent measuring it behaves differently."
Status: **unreviewed construction draft** (draft 2; GPT's extension and corrections, which draft 2 adopts, are separately Gemini ACCEPTED in run 39091716370; draft 2 as a whole and section 12 are unreviewed). This draft does not claim a milestone, a derivation of collapse, native access or receiver ownership, CLOSED/CERTIFIED status, a clock, geometry or a fitted parameter. The scratch checks are exploratory and are disclosed in section 10. Independent producer/checker code and Gemini review come at freeze.

## Credit: the inherited foundation

This draft is an effect-level reading of results that already exist. The load-bearing mathematics is inherited and credited here first:

- **v15.17 retained motion** (branch `research/v15.55-source-compatibility-response` @ `ac75b4fe`, `demos/v15.17-retained-motion/`; README blob `2b0c0599`, `retained_motion.py` blob `e3e8ac11`). The source contains:
  - the exact finite theorem "exact fixed-algebra descent <=> U A U† = A" for a trace-preserving conditional expectation (README, section "Fixed-algebra descent");
  - the three distinct processes E C_U, E C_U E and E_U C_U;
  - the warning that a normalizer can permute record sectors (README, "Algebra preservation is not fixed-record preservation");
  - the continuous-path result;
  - the classification over 96 cases (17 closed with fixed records, 79 nonclosed; `classify` lines 85–103, `audit` lines 187–207);
  - the collision witnesses (`collision_pair` lines 123–136);
  - the projection-cadence control, E C_{U²} vs E C_U E C_U at distance 0.5 (`controls` lines 145–159).

  I reproduced the inherited numbers locally (section 10).
- **v15.16 partial pruning** (`recoverability.py` blob `0a01d2ee`: `reduce_input` lines 94–97 is the conditional expectation E_S; `projectors` lines 86–88 give the central projectors P_s; `phase_pair` lines 117–122). It gives E_S E_T = E_{S∪T} and A_S = ⊕_s P_s M_16 P_s. **v15.15 coherent records** supplies the CNOT write, **v15.12** the reversible pre-time motion, **v15.13/v15.14** the supplied local events and record-dependent dynamics. v15.17 reuses these frozen operations as its motions.
- **My frozen recoverable_pruning_ledger** (Gemini ACCEPTED, run 39070100916): Lemma 12.1 (the pinching chain is record-compatible), Theorem 12.2 (G_j nonincreasing, central C_j nondecreasing, acquisition = promotion, loss layer never reaches a receiver), and the P2 split E_m, D_j.
- **My record_access draft 1** (commit `352fac2d`, blob `d5557538`): Theorem 2.1 (readable without disturbance + persistent <=> central), Theorem 3.1 (in v15.16 the pinching equals the receiver's own register read), and the missing implication I*.
- **proteinfolding-gpt**:
  - the [inherited event-to-record reconciliation](../../inherited_event_record_reconciliation/RECONCILIATION.md) (`9ad504b0`);
  - the accepted [own-view completion](../../own_view_completion_review/REVIEW_ACCEPTANCE.md) (run 39083538884) and [first-pruning own view](../../first_pruning_own_view_review/RESULT.md) (run 39085193731);
  - the [interface handoff](../../first_pruning_own_view_review/INTERFACE_HANDOFF.md) (`1606fca1`), whose type distinctions and receiver-provenance rule I follow in section 1;
  - the accepted [measurement-first compatibility](../../measurement_first_review/RESULT.md) (run 39088738210). Its criterion "1_E ∈ r*(C^Y) iff E is a union of fibers" is the static, record-versus-aggregation counterpart of the dynamical, motion-versus-observation criterion used here (Corollary 1.2).

### Draft 2 changes (credit: proteinfolding-gpt)

GPT's [observation-preservation extension](../../observation_preservation_review/RESULT.md) (freeze `53d164b0`, [acceptance receipt](../../observation_preservation_review/REVIEW_ACCEPTANCE.md), Gemini ACCEPTED in Actions run 39091716370) reviewed draft 1 and supplied a positive extension plus four corrections. Draft 2 adopts all four, in place, marked "[D2]":
1. Theorem 4(c): existence of a unitary in Z(A)′ that does not normalize A needs some block with BOTH n_k ≥ 2 and m_k ≥ 2 (A = C I_2 is the counterexample to multiplicity alone).
2. Corollary 1.4 and Theorem 2(c) are all-input statements: a nonclosed motion means SOME input shows an effect, not that the actual preparation does (dephasing, Hadamard, ρ = I/2 gives zero).
3. Proposition 8.1's E E = E is a nonselective map identity, not a count of actual selective events.
4. The P2 owner section E_m is nonfaithful and nontracial for a proper contraction; the identity contraction is the exception.

GPT's positive extension, the occupied-support criterion (I − Q_r) L_j K_r = 0, is the correct nonfaithful, any-channel generalization of Theorem 4(a); it is cited there and not re-proved. Section 12 is new in draft 2.

What is new here is small and is listed in section 9. GPT's review receipt asks that no further compatibility variant be counted as the receiver-identification advance. This draft does not claim that advance. It answers Aaron's separate effect-level request.

## 0. Result first

1. **Descent criterion, generalized (Theorem 1).** E Φ E = E Φ for every input holds iff Φ*(A) ⊆ A. Here E is ANY conditional expectation onto the retained algebra A (tracial or not) and Φ is any channel. For a unitary this is the inherited v15.17 criterion U A U† = A. The criterion depends only on A, not on which conditional expectation is used, but the observed outputs do depend on it. In the classical case the criterion is strong lumpability.
2. **Inserted observation (Corollary 1.4).** Inserting an observation before the motion U₂ leaves the final retained output unchanged iff U₂ normalizes A, whatever unitary preceded it. The inherited Zeno-type cadence gap of 0.5 is an instance.
3. **Receiver-relative effect (Theorem 2).** Unobserved = observed + leakage of the loss layer, N = O + E C_U (I−E). The size is bounded: ‖Nρ − Oρ‖₁ ≤ ‖ρ − Eρ‖₁. There are three nested exact criteria for "the observation is invisible": full retained state (U A U† = A) ⇒ central record (U† Z(A) U ⊆ A) ⇒ the receiver's own record (U† Q_r U ∈ A). Both implications are strict. On the 96 inherited v15.17 cases the split is 17 / 0 / 43 / 36 (section 6.3).
4. **Observation never completes a receiver's knowledge (Theorem 3).** For a faithful conditional expectation (every v15.16 pinching is one), an outcome that is impossible in the observed history is impossible in the unobserved one. So if the observed receiver records of two preparations are perfectly distinguishable, the unobserved ones are too. Observation can raise the receiver's distinguishability only partially.
5. **Access (Theorem 4).** A record written into Z(A) by the observation keeps its value under a later motion, for every observed state, iff [U, P_s] = 0 for all central P_s. Closure (normalizing A) is neither necessary nor sufficient: sector-permuting normalizers relabel the record, and unitaries in Z(A)′ that do not normalize A keep it. For the full-block v15.16 algebras, record persistence holds iff U is a unitary of A, and such a U is closed.
6. **Explicit examples, exact (section 6).**
   - Which-path W: the source distinction is coherent and the receiver starts blank. The **unobserved** receiver ends with 1 bit (trace distance 1); the **observed** one ends with 0 bits. Global retained distinguishability goes 1 → 1 unobserved and 1 → 0 observed.
   - Protection P: the observed receiver ends with trace distance 3/10 (≈ 0.0731 bit); the unobserved one ends with 0. Global goes 5/8 → 1/2 → 3/10 observed and 5/8 → 5/8 → 0 unobserved.

8. **The occurrence record (section 12, draft 2).** Fix one prefix state ρ. The two histories "observation occurred" and "observation did not occur" are two preparations from ONE prefix, so preparability G is not needed for this pair. A receiver's ability to tell them apart is exactly TV = ½ Σ_r |Tr[U† Q_r U (ρ − Eρ)]|. It is bounded by ½‖ρ − Eρ‖₁, the change the event itself made: an event can leave a readable record of its own occurrence only out of what it pruned. The bound is attained by a suitable supplied motion iff a rank condition holds (Ky Fan). For a faithful E (every v15.16 pinching) the record is never perfect; for the nonfaithful P2 owner section (an absorption is a move) it can be perfect. This is the UQCF reading of the known quantum-witness / no-signalling-in-time bound (Li et al. 2012; Schild and Emary 2015).

   This corrects my 21:51 plan, which expected "observed 1 bit vs unobserved 0". For collision pairs with equal E(ρ), the direction is the reverse, and Theorem 3 forbids the planned perfect version.
7. **Status.** The occurrence of the observation is a DECLARED INPUT, per Aaron. E, U and the preparations are supplied, preparability G is a premise, and the receiver identification (I*) is a premise. Every theorem is mathematically forced given those inputs. Nothing about the cause of collapse is claimed.

## 1. Setting and types

H is finite-dimensional and M_d = B(H). States ρ are density operators: the Schrödinger, grade-vector-like type. Observables X are elements of M_d: the Heisenberg, function-on-addresses type. The pairing is ⟨X, ρ⟩ = Tr(Xρ). Following the interface handoff, I never identify these two types. Functions on the configuration space of all grade vectors are not used anywhere in this draft.

- **Abelian ambient.** Theorems 1–3 and their proofs hold verbatim if M_d is replaced by the abelian ambient C^{X_0} (functions on addresses, with counting-trace pairing against grade vectors). That is the ledger-tree setting, where the motions are stochastic maps. There A ⊆ C^{X_0} is a block-constant subalgebra, and E*(f) = Σ_F φ_F(f 1_F) 1_F, with φ_F probability weights on each block F. Theorem 4 concerns unitary motion on M_d.
- **Retained algebra.** A ⊆ M_d is a unital *-subalgebra. Up to unitary equivalence A = ⊕_k M_{n_k} ⊗ I_{m_k}, with minimal central projections P_k, and Z(A) = span{P_k}. A is *full-block* if every m_k = 1. Every v15.16 A_S is full-block, and then Z(A)′ = A.
- **Observation.** E is linear on M_d, and its trace dual E* is a conditional expectation onto A: a unital, completely positive, idempotent A-bimodule map with image A (Tomiyama: equivalently, a norm-one projection onto A). Every such E* has the form E*(X) = ⊕_k (id ⊗ φ_k)(P_k X P_k) ⊗ I_{m_k}, with φ_k states on M_{m_k}, densities σ_k. So E(ρ) = ⊕_k Tr_{m_k}(P_k ρ P_k) ⊗ σ_k is CPTP and idempotent.
  - E is *tracial* if σ_k = I/m_k. Then E = E*, and E is the Hilbert-Schmidt orthogonal projection used by v15.16/v15.17.
  - E is *faithful* if every σ_k is faithful.
  - Examples: (i) the v15.16 pinching E_S (`reduce_input`) is tracial and faithful. (ii) The ledger's P2 cumulative map E_m = I_{0m} P_{0m} on grade vectors has dual (E_m* f)(z) = f(r_{0m}(z)), a conditional expectation onto the fiber-constant functions B_m. E_m preserves the total and is idempotent, but it is **neither tracial nor faithful** for a proper contraction, because it puts each fiber's total on the owner atom. [D2] The identity contraction is the exception (GPT correction 4).
- **Motion.** A motion is a unitary U, C_U(X) = U X U†, or more generally a channel Φ. Every motion here is supplied.
- **Histories.** "Observed" means O = E C_U E: prune, move, then inspect. "Unobserved" means N = E C_U: move, then inspect.
- **Receiver record.** This is a DECLARED family of central projections Q = {Q_r} ⊆ Z(A), with Σ Q_r = I. The receiver's record of ρ is p_r(ρ) = Tr(Q_r ρ). Because Q_r ∈ A, Tr(Q_r E(X)) = Tr(Q_r X), so the final inspection never changes receiver probabilities.
  - *Provenance.* Q is fixed before any preparation, motion or separating formula is chosen, and it is the same in both histories. Its identification with a receiver's own subsystem is NOT earned. That is I* (record_access §7), equivalently GPT's actual-record-to-owned-part identification. "Readable" means only the nondisturbance scope of record_access Theorem 2.1. An available outcome instrument is not derived (handoff, point 2).

## 2. Theorem 1: descent criterion for any conditional expectation and any channel

**Theorem 1.** Let E be as in section 1 and Φ a linear, Hermiticity-preserving map on M_d (for example a channel). The following are equivalent:
(a) E Φ E = E Φ on M_d;
(b) E Φ(ρ) = E Φ(σ) for all density operators ρ, σ with E ρ = E σ;
(c) Φ*(A) ⊆ A.

*Proof.* (a) ⇒ (b) is immediate.

(b) ⇒ (a): let X ∈ ker E. Since E preserves Hermiticity, its Hermitian and anti-Hermitian parts lie in ker E, so take X Hermitian. Tr X = Tr E(X) = 0 because E* is unital. Put σ = I/d and ρ = I/d + εX, with ε > 0 small enough that ρ ≥ 0. Then E ρ = E σ, so (b) gives ε E Φ(X) = 0. Hence E Φ vanishes on ker E = im(I − E), that is E Φ (I − E) = 0.

(a) ⇔ (c): the trace dual of E Φ (I − E) is (I − E*) Φ* E*. It vanishes iff Φ*(im E*) ⊆ ker(I − E*), and im E* = Fix E* = ker(I − E*) = A. ∎

**Corollary 1.1 (v15.17, inherited).** For Φ = C_U, (c) reads U† A U ⊆ A. Since C_{U†} is injective and dim A is finite, this is U† A U = A, equivalently U A U† = A. For tracial E this is exactly the v15.17 theorem. The README proves it with the Hilbert-Schmidt adjoint, which presupposes E = E*. The trace-dual proof above removes that presupposition.
- *Domain.* The statement is for all operators, equivalently all density operators, which span M_d. If it is required only on a restricted family, for example a preparable set G, the condition is weaker and the "iff" fails in general.
- *Finite dimension.* Finite dimension is used for "⊆ ⇒ =". In infinite dimension a unitary can conjugate a von Neumann algebra properly into itself.
- *Which E.* The criterion depends only on A. The observed output E C_U E ρ depends on which conditional expectation is used.

**Corollary 1.2 (classical: strong lumpability; ledger tree).** Let A = B, the functions constant on the blocks of a partition, and Φ = T, a stochastic matrix acting on grade vectors. Then (c) says T* maps block-constant functions to block-constant functions. That is Kemeny–Snell strong lumpability: the block-to-block transition weight Σ_{y∈F′} T(y|x) depends only on the block of x.
- For the ledger tree, take A = B_m and E = E_m, the P2 owner section. A motion descends to the retained fiber totals iff it is lumpable along the cumulative fibers r_{0m}.
- *Example* (`chk1.py`). Atoms (a, u | b), with u in a's fiber. T swaps u and b, which is not lumpable. For x = (1/2, 1/2, 0) the fiber totals are: observed with the owner-section E_m, (1, 0); observed with the tracial fiber average, (1/2, 1/2); unobserved, (1/2, 1/2). The two conditional expectations give different observed outputs.
- This is the dynamical counterpart of GPT's measurement-first criterion (4). That criterion asks when a record descends through an aggregation. Corollary 1.2 asks when a motion descends through an observation.

**Corollary 1.3 (normalizers permute sectors).** If U A U† = A, then Ad U|_A is a *-automorphism of A. It maps Z(A) onto Z(A) and minimal central projections onto minimal central projections: U P_k U† = P_{π(k)} for a permutation π of sectors of equal type (n_k, m_k).

**Corollary 1.4 (inserted observation; time-constituting step).** For unitaries U₁ and U₂: E C_{U₂} E C_{U₁} = E C_{U₂} C_{U₁} iff U₂ A U₂† = A. *Proof:* right-multiply by C_{U₁}^{-1} and apply Theorem 1.
- If the prefix contains earlier observations, the prefix map P is not invertible. The "if" direction still holds, but "only if" holds only on im P.
- The inherited cadence control is an instance. It uses the nonclosed `mix` = exp(−iπ/4 · YIII) at mask `1000`, and E C_{U²} vs E C_U E C_U differ by 0.5. In minimal form (`chk1.py`), starting from |0⟩, "once" gives diag(0, 1) and "repeated" gives diag(1/2, 1/2): trace distance exactly 1/2.
- *Reading.* An observation inserted into a history has an effect FOR SOME INPUT iff the motion after it fails to normalize the retained algebra. What came before does not matter.
- [D2] *Quantifier* (GPT correction 2). This is an all-input, map-level statement. A nonclosed motion does not imply an effect on the actual preparation: qubit dephasing E onto D_2, U = Hadamard and ρ = I/2 give E C_U E ρ = E C_U ρ = I/2. Whether the actual preparation shows the effect is exactly the occurrence-record question of section 12.

## 3. Theorem 2: the receiver-relative effect

Write the unobserved and observed histories as N = E C_U and O = E C_U E.

**Theorem 2.** For every ρ:
(a) **Decomposition.** N ρ = O ρ + Λ_U ρ, with Λ_U = E C_U (I − E). The whole difference is the motion's leakage of the loss layer (I − E)ρ, which is the ledger's D_j when E is one pinching step.
(b) **Receiver identity.** p_r(Nρ) − p_r(Oρ) = Tr[(I − E*)(U† Q_r U) ρ] = Tr[U† Q_r U (I − E)ρ].
(c) **Hierarchy of exact all-input criteria:**
  - (F) Nρ = Oρ for all ρ ⟺ U A U† = A.
  - (C) The central record agrees for all ρ ⟺ U† Z(A) U ⊆ A.
  - (R) The receiver's record agrees for all ρ ⟺ U† Q_r U ∈ A for every r.

  (F) ⇒ (C) ⇒ (R), and both implications are strict.
(d) **Size.** ‖Nρ − Oρ‖₁ ≤ ‖ρ − Eρ‖₁. Hence TV(p(Nρ), p(Oρ)) ≤ ½ ‖ρ − Eρ‖₁.

*Proof.*
- (a) is linearity.
- (b): Tr(Q_r E C_U (I − E) ρ) = Tr(U† Q_r U (I − E)ρ), using E*(Q_r) = Q_r, and then apply duality.
- (c): (F) is Corollary 1.1. (C) and (R) follow from (b): an operator Y satisfies Tr(Yρ) = 0 for all ρ iff Y = 0, and (I − E*)(Y) = 0 iff Y ∈ A. (F) ⇒ (C) because U† A U = A gives U† Z(A) U ⊆ A. (C) ⇒ (R) because Q_r ∈ Z(A).
- *Strictness of (F) ⇒ (C)*: take A = M₂ ⊕ M₂ on C⁴ with blocks {0,1} and {2,3}, and U the permutation (1 2). Then U† P_k U are the projections onto span{0,2} and span{1,3}, which are diagonal and so in A, so (C) holds. But U does not normalize A. For ψ = (|0⟩ + |2⟩)/√2 the full retained effect is ‖Nρ − Oρ‖₁ = 1, while the central weights are (1, 0) in both histories (`chk1.py`).
- *Strictness of (C) ⇒ (R)*: on the inherited data there are 43 cases with (R) but not (C) (section 6.3).
- (d): E and C_U are positive and trace preserving, hence trace-norm contractive on Hermitian operators. Apply this to (a). ∎

(R) is the Heisenberg form of the **no-signalling-in-time** condition for a nonselective measurement (Kofler and Brukner 2013). It is standard, and I use it as such.

## 4. Theorem 3: inserting an observation cannot complete a receiver's knowledge

**Theorem 3.** Let E be faithful. This includes every tracial E and every v15.16 pinching. Then for every ρ ≥ 0, ker E(ρ) ⊆ ker ρ. Consequently, for any CP motion Φ and any receiver outcome r:

    Tr(Q_r E Φ E ρ) = 0  ⟹  Tr(Q_r E Φ ρ) = 0 .

So if the observed receiver records of ρ₀ and ρ₁ have disjoint supports (perfect discrimination), so do the unobserved ones.

*Proof.* E(ρ) = ⊕_k r_k ⊗ σ_k with r_k = Tr_{m_k}(P_k ρ P_k). Let ξ ∈ ker E(ρ). The map is block diagonal, so each ξ_k = P_k ξ lies in the kernel. Write ξ_k = Σ_j x_j ⊗ f_j, where f_j is an eigenbasis of σ_k with eigenvalues λ_j > 0. Then 0 = ⟨ξ_k, (r_k ⊗ σ_k) ξ_k⟩ = Σ_j λ_j ⟨x_j, r_k x_j⟩, so r_k x_j = 0 for every j. Since r_k = Σ_g (I ⊗ ⟨g|) P_k ρ P_k (I ⊗ |g⟩), this gives ⟨x_j ⊗ g, ρ (x_j ⊗ g)⟩ = 0 for every g, so ρ^{1/2}(x_j ⊗ g) = 0, so ρ ξ_k = 0 and ρ ξ = 0.

For the consequence, let M = Φ*(Q_r) ≥ 0. Tr(M E(ρ)) = 0 forces M^{1/2} E(ρ)^{1/2} = 0, so ran M ⊆ ker E(ρ) ⊆ ker ρ, and Tr(Mρ) = 0. ∎

The converse fails: in example W the unobserved receiver is perfect and the observed one is blind. Partial reversals occur: in example P the observed receiver gets 3/10 and the unobserved one 0. For a non-faithful E (the P2 owner section) the kernel inclusion fails: a unit mass on a removed atom u is sent to its owner (`chk3.py`). Theorem 3 is not claimed there.

## 5. Theorem 4: access. When does the observation's record survive later motion?

After an observation the retained state is E(ρ). Its central record is w_k = Tr(P_k E ρ) = Tr(P_k ρ).
- By record_access Theorem 2.1 (inherited), this record is readable without disturbing any retained state.
- By ledger Lemma 12.1 (inherited), it persists, refined, under every later nested pinching.

The question here is persistence under later motion.

**Theorem 4.** Let E be faithful and U a later motion followed by inspection.
(a) w_k(E C_U E ρ) = w_k(E ρ) for every ρ and every k ⟺ E*(U† P_k U) = P_k for every k ⟺ [U, P_k] = 0 for every k.
(b) If U A U† = A with sector permutation π (Corollary 1.3), the record is relabeled, w ↦ w ∘ π^{-1}. Every permutation-invariant quantity of the record is preserved, including the ledger's C between two preparations. The value at each named sector survives iff π = id.
(c) Closure and record persistence are logically independent:
  - A sector-permuting normalizer is closed and violates (a). An example is the v15.17 synthetic `swap` control; in `chk1.py`, X on S maps the record (0, 1, 0, 0) to (0, 0, 0, 1).
  - A unitary in Z(A)′ that does not normalize A satisfies (a) and is not closed. [D2] Such unitaries exist iff some block has BOTH n_k ≥ 2 and m_k ≥ 2 (GPT correction 1, with proof and the constructive witness U = I ⊗ (I − π) + V ⊗ π in the frozen extension, section 5). Draft 1 said "iff some m_k ≥ 2", which is false: A = C I_2 (n = 1, m = 2) is normalized by every unitary. The `chk3.py` witness is not relied on for the existence claim.
  - For full-block A (all v15.16 algebras), Z(A)′ = A, so (a) ⟺ U ∈ U(A). Then U is an inner automorphism of A, and closed.
(d) **Continuous paths (inherited v15.17).** A continuous path U_t with U_0 = I that normalizes A at every t has π_t = id, so it satisfies (a).
  - *Scope remark on the inherited text.* The README's "equivalently [H, P_s] = 0" is exact for full-block A, which covers every v15.16/v15.17 algebra. For A with multiplicity, [H, P_k] = 0 implies (a) but not normalization.
  - The atlas review (Part 3) and my 21:51 plan said "every later normalizing step fixes Z(A)". That wording is wrong as stated: normalizing fixes Z(A) as a set but may permute its sectors. Statement (a) is the correct pointwise condition.
(e) [D2] **Nonfaithful E and general channels.** For a possibly nonfaithful conditional expectation and any channel with Kraus operators L_j, every receiver weight survives E Φ E for all inputs iff (I − Q_r) L_j K_r = 0, where K_r is the support observation actually occupies in sector Q_r. This is GPT's accepted extension (observation_preservation_review, section 3), and it removes the faithfulness hypothesis of (a). In P2 it reads P T I = id.

*Proof.*
- (a), first ⟺: w_k(E C_U E ρ) = Tr(U† P_k U E ρ) = Tr(E*(U† P_k U) ρ), and w_k(Eρ) = Tr(P_k ρ). These agree for every ρ iff E*(U† P_k U) = P_k.
- (a), second ⟺: let Q = U† P_k U, a projection with Tr Q = Tr P_k. Restricted to block k, E*(Q) = P_k says (id ⊗ φ_k)(P_k Q P_k) = I_{n_k}. So (id ⊗ φ_k)(P_k − P_k Q P_k) = 0 with P_k − P_k Q P_k ≥ 0, and faithfulness gives P_k Q P_k = P_k. Hence Q ≥ P_k, and equal trace gives Q = P_k, that is [U, P_k] = 0. The converse is immediate.
- (b) follows from Corollary 1.3.
- (c): Z(A)′ = ⊕_k M_{n_k m_k}, which equals A iff all m_k = 1.
- (d): π_t is continuous into a finite set and π_0 = id.
- (e): proved in the cited frozen extension (necessity by the test state Q_r/Tr Q_r, sufficiency by support and trace preservation); not re-proved here. ∎

**On the inherited motions** (`chk2.py`): all 17 closed cases fix the record sectors, and no frozen motion is a sector permutation. This confirms v15.17's count. The B1, B2|0 and B2|1 motions commute with receiver A's projectors to within 3.6e-15. So, for every observed state, they keep receiver A's record and show no observation effect on it, even on masks where they are nonclosed on the full algebra. The pretime, A1 and A2 motions do not commute with them: the largest commutator norm with the A1A2 projectors is 0.79, 0.90 and 0.67 respectively.

## 6. Explicit examples (exact rationals; `chk1.py`)

Common frame for W and P:
- H = C²_S ⊗ C²_R, with S the source and R the receiver register.
- A = D₂ ⊗ D₂, both record bits pinched as in a v15.16 mask, so Z(A) = A. E is the dephasing: tracial and faithful.
- The receiver record is Q_r = I_S ⊗ |r⟩⟨r|_R. It is declared before anything else and is the same in both histories.
- The receiver starts blank: R = |0⟩, so both preparations have receiver record (1, 0) and C₀ = 0.
- W_c = CNOT_{S→R} is the v15.15-type write. It is a permutation matrix, so it is closed.

### 6.1 Which-path W: coherent source distinction (the inherited v15.17 collision witness with an explicit receiver)

- Preparations: ρ_b = |χ_b⟩⟨χ_b| ⊗ |0⟩⟨0|, with χ₀ = |+⟩ and χ₁ = |−⟩. Then E ρ₀ = E ρ₁ = (I/2) ⊗ |0⟩⟨0|, and G₀ = 1.
- Motion: U = W_c (H ⊗ I), which is nonclosed.

| History | Global retained distinguishability | Final receiver records (source 0 / source 1) | Receiver trace distance | Mutual information (balanced prior) |
| --- | --- | --- | --- | --- |
| Observed O = E C_U E | 1 → 0 → 0 | (1/2, 1/2) / (1/2, 1/2) | 0 | 0 bits |
| Unobserved N = E C_U | 1 → 1 → 1 | (1, 0) / (0, 1) | 1 | 1 bit |

- Effect on a single preparation: TV(p(Nρ_b), p(Oρ_b)) = 1/2 = ½ ‖ρ_b − Eρ_b‖₁, so Theorem 2(d) is saturated.
- Criterion: U† Q_r U = |+⟩⟨+| ⊗ Q_r + |−⟩⟨−| ⊗ Q_{1−r} ∉ A, so (R) fails.
- *Where the effect sits* (Corollary 1.4): inserting E between H and W_c changes nothing, because W_c is closed. Inserting E before H removes the receiver's bit. The effect sits at the nonclosed interference step, not at the write.

This is the inherited v15.17 control (`mix` at mask `1000`, phase pair (b_0000 ± b_1000)/√2). Reproduced: retained inputs 1.66e-15 apart, unobserved outputs 1.0 apart, observed outputs 8.5e-16 apart. Here it is restated with a declared receiver register.

### 6.2 Protection P: observation keeps a population distinction that coherent motion erases

- Motion: U = W_c (R_y ⊗ I), with R_y = (1/√5)[[2, −1], [1, 2]] (cos φ = 3/5, sin φ = 4/5).
- Preparations: ρ₀ = |0⟩⟨0| ⊗ |0⟩⟨0| and ρ₁ = ½(I − ¾X) ⊗ |0⟩⟨0|. Then G₀ = 5/8.

| History | Global retained distinguishability | Final receiver records (source 0 / source 1) | Receiver trace distance | Mutual information |
| --- | --- | --- | --- | --- |
| Observed | 5/8 → 1/2 → 3/10 | (4/5, 1/5) / (1/2, 1/2) | 3/10 | h(13/20) − (h(4/5) + 1)/2 ≈ 0.0731 bit |
| Unobserved | 5/8 → 5/8 → 0 | (4/5, 1/5) / (4/5, 1/5) | 0 | 0 |

In the unobserved history the motion makes the source's population and coherence contributions cancel at the receiver, so the final inspection retains nothing. The observation removes the coherence first, and that protects 3/10. By Theorem 3, no choice of U or preparations can make the observed receiver perfect while the unobserved one stays imperfect.

### 6.3 The 96 inherited v15.17 cases, refined (`chk2.py`; imports the v15.17 source read-only, baseline blob `0a01d2ee` verified)

The "central record" is the mask's P_s. "Receiver A" is the coarse projectors of the pinched A bits. Their identification with A's own register is record_access Theorem 3.1 at encoding time only; after a motion on system space it is a label, which is the I* caveat.

| Class | Count |
| --- | --- |
| (F) closed: also (C) and (R) | 17 |
| not (F), but (C) | 0 |
| not (C), but (R) at receiver A | 43 (16 of them have no pinched A bit, so receiver A has a trivial record) |
| not (R): receiver A sees the observation | 36 (12 each from pretime, A1, A2; 0 from B1, B2\|0, B2\|1) |

- Every nonclosed inherited case changes the central record for some state. The largest single-state effect, sup_ρ TV between the observed and unobserved central records, ranges over 0.0357–0.4902 across the 79 cases.
- For receiver A it ranges over 0.0553–0.3325 across the 36 cases.
- Strictness of (F) ⇒ (C) is therefore shown only by the synthetic example in Theorem 2, not by inherited motions.

## 7. Ledger reading: the observation effect is redistribution, never creation

Let h be any history: a composition of observations E and motions C_U. For two preparations, the global distinguishability D_k after k steps is nonincreasing (data processing), and the receiver's C_k ≤ D_k ≤ D₀. So every receiver gain in sections 6.1–6.2 (unobserved W: 0 → 1; observed P: 0 → 3/10) redistributes distinguishability that the source already had. This is ledger Theorem 12.2(1–3) carried from a decreasing restriction chain to histories with motion.

The observed history factors through E, so whatever sits in the loss layer (I − E)ρ when the observation happens never reaches any later receiver. This is the history analogue of ledger Theorem 12.2(6).

The unobserved history adds the counterfactual the ledger lacked. The same loss-layer content does reach the receiver, through Λ_U, if the motion comes first. So the ledger's loss is an effect of where the pruning step sits in the order, and Theorem 2(c) says exactly when that position matters.

## 8. Pre-time vs time-constituting wording

Per Aaron's 21:46/21:47 rules:
- The motion U in the unobserved history is pre-time reversible relational change (v15.12). It changes the state without establishing an order.
- The observation E in the observed history is an actual ordered recoverability update. Irreversible pruning does not happen "before" time; its ordered occurrence is time. Pre and post are logical stages, not clock periods.
- O and N differ by exactly one time-constituting step. Corollary 1.4 and Theorem 2 say that this step has an effect on later retained records iff the subsequent motion is nonclosed, and an effect on the receiver iff (R) fails.

**Proposition 8.1 (what counts as another step).** E E = E. If E is tracial and W normalizes A, then E C_W E = C_W E = E C_W.
- So observations separated only by closed motion collapse into one. An inserted observation counts as a distinct step, distinguishable by any later retained record, only when it is followed by nonclosed motion.
- This formalizes "recomputing the same sum is not another step" at the level of nonselective maps.
- [D2] *Scope* (GPT correction 3). E E = E is a nonselective map identity. It does not test whether, or how many times, an actual selective measurement event occurred: for the qubit projective instrument on I/2 the conditional states are |0⟩⟨0| and |1⟩⟨1| while the average stays I/2. The "step count" reading above is restricted to what later nonselective retained records can distinguish.
- *Proof.* C_W maps A to A, so C_W E ρ ∈ A is fixed by E. Then apply Theorem 1. ∎

The inherited Zeno-type cadence gap of 0.5 is therefore the effect of one additional time-constituting step inserted before nonclosed motion. The cause of that step is not modeled. Its occurrence is the declared input.

## 9. Status: earned vs assumed, and the relation to known results

| Ingredient | Status |
| --- | --- |
| Occurrence of the observation (that E happens, and where) | **Declared input** ("an observation occurred"), per Aaron; not derived |
| Which E (algebra A; tracial vs owner-section conditional expectation) | Supplied: v15.16 masks; P2 E_m. The criterion depends only on A; observed outputs depend on E (Corollary 1.2) |
| Motions U | Supplied: v15.17 reuses frozen v15.12–v15.15 operations; H, R_y, CNOT are supplied in section 6 |
| Preparations, and their reachability | Supplied; preparability **G** remains an explicit premise |
| Receiver identification Q ↔ the receiver's own subsystem | **Premise I*** (record_access §7) / GPT's actual-record-to-owned-part identification; not earned |
| Actual (selective) outcome, outcome instrument | Not derived. E is nonselective; actual records remain v15.11 RCR, supplied |
| Theorems 1–4, Corollaries 1.1–1.4, Proposition 8.1, the redistribution bounds | **Mathematically forced** given the above |

**Known results this rests on or reproduces.**
- *Standard*:
  - conditional expectations (Umegaki 1954; Tomiyama 1957; Takesaki 1972 for existence);
  - Lüders (1951) and pinching;
  - nondisturbance (Heinosaari and Wolf 2010);
  - the quantum Zeno effect (Misra and Sudarshan 1977; the cadence corollary is its one-insertion form);
  - which-path complementarity (Englert 1996; example W is the Mach–Zehnder case);
  - no-signalling in time / Leggett–Garg (Kofler and Brukner 2013; criterion (R));
  - decoherence and einselection (Zurek 2003), where central sectors are pointer sectors;
  - quantum Darwinism (Zurek 2009), not addressed here: one receiver, no redundancy;
  - data processing;
  - Landauer (1961), not used: no thermodynamics;
  - strong lumpability (Kemeny and Snell 1960);
  - operator QEC of observables (Bény, Kempf and Kribs 2007, cited by v15.17).
- *New here, within UQCF only*:
  1. the v15.17 criterion extended to every conditional expectation and every channel, so that it covers the ledger's non-tracial P2 owner section, with the remark that observed outputs depend on the choice of conditional expectation;
  2. the receiver-relative hierarchy (F) ⇒ (C) ⇒ (R) stated with the retained algebra, the ledger loss layer and a declared receiver, and evaluated on the 96 inherited cases (17 / 0 / 43 / 36; B-motions never visible to receiver A);
  3. Theorem 3 in this setting (observation cannot make a receiver perfect; faithfulness needed; fails for the P2 owner section);
  4. the separation of algebra closure from record persistence (Theorem 4(c)), correcting my own plan and the atlas wording;
  5. the identification of the observation effect as ordered redistribution of the ledger's loss layer (section 7).

  None of these is new mathematics.

## 10. Scratch checks (exploratory, not preregistered; disclosed; not committed)

- `/tmp/obs/chk1.py` (sympy 1.14, exact): examples W, P, the hierarchy witness, the cadence 1/2, the sector-swap relabeling, the classical owner-section vs tracial example. **0 violations.** All numbers in section 6 come from this script.
- `/tmp/obs/chk2.py` (NumPy 2.5.4 in a local venv; v15.17 pins 2.3.5): imports the v15.17 source extracted from `ac75b4fe` read-only. The run reproduces the inherited counts 17 / 0 / 79, min collision separation 0.07138, transport error 7.2e-15, cadence 0.5 and witness 1.66e-15 / 1.0 / 8.5e-16, and computes the section 6.3 table. **0 violations** of (F) ⇒ (C) ⇒ (R) or of sector fixing.
- `/tmp/obs/chk3.py` (random; seed 20261017):
  - Theorem 1, with tracial, faithful non-tracial and non-faithful conditional expectations, and with normalizer, Kraus-in-A and Haar channels: 720 cases.
  - Corollary 1.3: 100 cases.
  - Theorem 3 support inclusion: 300 cases, plus the non-faithful counterexample.
  - Theorem 4(a): 200 cases, plus the Z(A)′ non-normalizer and the non-faithful exception.
  - Theorem 2(a, b, d): 500 cases.
  - Corollary 1.4: 120 cases.

- `/tmp/obs/chk4.py` (draft 2, section 12; sympy exact for W and P, NumPy seed 20261018 otherwise): W record ½ = κ; P record 0 and 3/10 ≤ 3/8; classical prefix gives 0 under 200 Haar motions; 500 faithful cases of TV_G ≤ κ < 1 and κ ≤ 1 − 2^{−D_max}; 300 Ky Fan cases (attained value, 6000 random motions never exceeding it, the saturation condition); 400 block pinchings with κ ≤ 1 − 1/M and ρ ≤ M·Eρ; owner-section TV = 1. **0 violations.**

  **0 violations** in the final run. Two bugs in my own scratch code were found and fixed before that run: a transposed σ in the predual, and a witness algebra without multiplicity.

## 11. Open obligations

1. **Cause and occurrence of E.** Out of scope by Aaron's 21:50 reading. Here it is a declared input. Which E occurs (A and the conditional expectation) is also supplied.
2. **G.** Preparability of the two source preparations from one Genesis-pinned history remains an explicit premise.
3. **I\*** / receiver identification. The receiver record Q is declared, not shown to be the receiver's own subsystem with provenance independent of the separating formula. An available outcome instrument is also not derived (handoff, points 1–2). This is the native frontier GPT's measurement-first receipt names. This draft does not advance it.
4. **Native motion.** Every U is supplied. No inherited rule selects nonclosed motion.
5. **Non-faithful E.** For the P2 owner section, Theorem 3 fails (section 12.3 gives the perfect-record consequence). [D2] Theorem 4(a) is replaced by GPT's occupied-support criterion, Theorem 4(e). The descent criterion (Theorem 1) still holds.

## 12. The occurrence record: when a receiver can read THAT an observation occurred (new in draft 2)

This section is the construction-mode step of the ~23:00 ET loop. Per Aaron's 22:21 ET rule, "an observation occurred" is an empirical input: nothing here explains why or by what it occurred. The question is purely about effect. Given one prefix, can a later retained receiver record tell the history in which the observation occurred from the history in which it did not?

**Setting.** Fix one prefix state ρ: whatever Genesis-pinned history produced it, one state, not two. At this point the declared input b is either "occurred" (apply E) or "did not occur" (apply nothing). Then the same supplied motion Φ follows, and the same final inspection E. So the two histories are O = E Φ E and N = E Φ of section 3. They differ by exactly one inserted time-constituting step (section 8). Write Δ = ρ − Eρ = (I − E)ρ for the loss-layer content the step removes, and κ_E(ρ) = ½‖Δ‖₁ for the size of the change the step makes. The receiver record is the declared central family Q = {Q_r} of section 1 (premise I* unchanged), and q_r = rank Q_r.

### 12.1 The construction-mode ingredients come out of the setting

**Proposition 12.1 (one prefix, a native distinction, a blank receiver).**
(a) *Separation of preparations without G.* The two preparations compared, ρ and Eρ, come from one prefix and differ only by the declared event. No second preparation, preparer choice or reachability premise is involved. They are globally distinct iff Δ ≠ 0.
(b) *Native source distinction.* The distinction b is the occurrence of an ordered recoverability update itself, not a supplied source register.
(c) *Initially uninformed receiver, forced.* At the moment of the event, Tr(Y Eρ) = Tr(Y ρ) for every Y ∈ A, because E*(Y) = Y. So every retained observable, and in particular every receiver weight p_r, is identical in the two branches. No retained receiver can see an observation at the moment it occurs.

*Proof.* (a) and (b) restate the setting. (c) is the bimodule property E*|_A = id. ∎

(a) discharges G **only for the occurrence distinction**. It does not discharge G for arbitrary source distinctions, such as the coherent pair ρ_0, ρ_1 of example W. The prefix ρ itself must still be reachable, and it must carry loss-layer content (Δ ≠ 0). For the v15.16 masks that means coherence across the pinched sectors, which in the inherited stack comes from the supplied v15.12 reversible motions.

### 12.2 Exact receiver consequence and the redistribution bound

**Theorem 12.2 (occurrence record).** Let Φ be any channel. Then:
(a) **Exact form.** δ_r := p_r(N ρ) − p_r(O ρ) = Tr[Φ*(Q_r) Δ] = Tr[(I − E*)(Φ*(Q_r)) ρ]. The receiver's occurrence record is TV_R = ½ Σ_r |δ_r| = max_S |Σ_{r∈S} δ_r|.
(b) **No creation.** TV_R ≤ TV_G := ½‖E Φ(Δ)‖₁ ≤ κ_E(ρ). A receiver can read that an event occurred only out of what the event itself pruned.
(c) **Classical prefixes leave no record.** If ρ = Eρ, then δ_r = 0 for every channel, every receiver and every later history.
(d) **Closed motion leaves no record.** If Φ*(A) ⊆ A, then δ_r = 0 for every ρ (Theorem 1). If only Φ*(Q_r) ∈ A holds for every r, the receiver's record vanishes while the global one may not (Theorem 2(c), (R)).

*Proof.* (a): Q_r ∈ A, so the final E does not change p_r; then p_r(EΦρ) − p_r(EΦEρ) = Tr(Q_r Φ(Δ)) = Tr(Φ*(Q_r) Δ). The second form uses Tr(X(I − E)ρ) = Tr((I − E*)(X) ρ). The max-over-subsets form is the standard expression for total variation. (b): the receiver distribution is a coarse-graining of E Φ(·), and E, Φ are trace-norm contractive on Hermitian operators (data processing). (c) and (d) follow from (a) and Theorem 1. ∎

**Theorem 12.3 (what a supplied motion can extract, exactly).** Let λ_1 ≥ … ≥ λ_d be the eigenvalues of Δ (Hermitian, trace zero), with n_+ positive and n_− negative. For 0 < q < d put F(q) = max(λ_1 + … + λ_q, λ_1 + … + λ_{d−q}). Then over all unitary motions U,

    max_U TV_R = max over outcome subsets S, with q_S = Σ_{r∈S} q_r ∉ {0, d}, of F(q_S),

and this equals κ_E(ρ) iff some q_S or d − q_S lies in [n_+, d − n_−]. If Δ ≠ 0 and the receiver has at least two outcomes, the maximum is strictly positive.

*Proof.* By Theorem 12.2(a), TV_R = max_S |Tr(U† Q_S U Δ)|, with Q_S = Σ_{r∈S} Q_r. As U ranges over the unitaries, U† Q_S U ranges over every rank-q_S projection. By Ky Fan's maximum principle, max_P Tr(PΔ) over rank-q projections is λ_1 + … + λ_q. Since Tr Δ = 0, the minimum is −(λ_1 + … + λ_{d−q}). So max |Tr(PΔ)| = F(q). The positive part of Δ sums to κ_E(ρ), and a top-q sum equals it iff the top q eigenvalues include every positive one and no negative one, i.e. n_+ ≤ q ≤ d − n_−. For positivity: if Δ ≠ 0 and 0 < q < d, the top-q sum of a nonzero traceless spectrum is strictly positive, since otherwise the top q and the bottom d − q would both average 0, forcing every eigenvalue to be 0. ∎

The optimizing motion is supplied. No inherited rule selects it, and Theorem 12.3 is a capacity statement, not a native dynamics.

Exact instances (`chk4.py`, sympy):
- **W** (section 6.1, prefix ρ = |+⟩⟨+| ⊗ |0⟩⟨0|): Δ = ½ X_S ⊗ |0⟩⟨0| has spectrum (½, 0, 0, −½), so κ = ½. Here q_0 = 2 ∈ [1, 3], so the bound is attainable, and the inherited motion W_c(H ⊗ I) attains it: TV_R = TV_G = ½.
- **P** (section 6.2): for ρ_0 = |0⟩⟨0| ⊗ |0⟩⟨0|, ρ_0 ∈ A and the record is 0 (Theorem 12.2(c)). For ρ_1, κ = 3/8 and TV_R = TV_G = 3/10. The receiver reads the occurrence partially.

### 12.3 Faithful observations never leave a perfect occurrence record; owner-section absorptions can

**Proposition 12.4.**
(a) **Faithful E.** supp ρ ⊆ supp Eρ (Theorem 3), so ρ ≤ c Eρ with c = 2^{D_max(ρ‖Eρ)} < ∞, and

    TV_R ≤ κ_E(ρ) ≤ 1 − 2^{−D_max(ρ‖Eρ)} < 1.

For a pinching onto M nonzero central sectors (every v15.16 E_S, with M the number of sectors), the pinching inequality ρ ≤ M · Eρ gives κ_E(ρ) ≤ 1 − 1/M for every state ρ, pure or mixed. So no receiver, under any motion, reads with certainty in one trial that a faithful observation occurred.
(b) **Nonfaithful P2 owner section.** A perfect occurrence record is possible. With atoms (a, u | b), u in a's fiber, E = E_m, prefix x = δ_u and the supplied motion T swapping u and b, the fiber totals are (0, 1) unobserved and (1, 0) observed, so TV_R = 1 (`chk4.py`).

*Proof.* (a): for any projection P, Tr(PΔ) = Tr(Pρ) − Tr(P Eρ) ≤ Tr(Pρ)(1 − 1/c) ≤ 1 − 1/c. The pinching inequality (Hayashi 2002) gives c ≤ M. (b) is direct computation. ∎

*Reading of (b).* The owner-section absorption is a move (record_access Theorem 5.1): it relocates the unit mass from u to its owner a. So ρ and Eρ are orthogonal (κ = 1), and a non-lumpable motion (one failing GPT's P T I = id) carries them into different fibers. A dephasing can only remove coherence, which by (a) is never orthogonal to what remains. This is the occurrence-record form of record_access Corollary 5.3 (copy vs move). It is a structural difference between the two inherited kinds of pruning, the v15.16 pinching and the P2 aggregation. All exact checks: `chk4.py`, 0 violations (section 10).

### 12.4 Ledger and time reading

- **Redistribution, not creation.** By Theorem 12.2(b), what a receiver learns about the occurrence is bounded by κ_E(ρ), the change the event made. The carrier is the loss layer Δ: in the unobserved branch the motion carries Δ to the receiver (the leakage Λ_U of Theorem 2(a)); in the observed branch Δ is gone. The event is recorded by what it erased. This is the ledger point of addendum (b): the receiver gains information (0 → TV_R) while global distinguishability does not increase (TV_R ≤ TV_G ≤ κ).
- **Time.** Under Aaron's 21:47 ET framing, time is the ordered history of compatible records of events. Theorem 12.2 gives the exact condition for one event to leave a receiver-readable record of its own occurrence: some δ_r ≠ 0. A step after which every δ_r vanishes, for example a classical prefix or a closed later motion, is not distinguishable as a step by that receiver. This is consistent with the nonselective scope of Proposition 8.1 (GPT correction 3), and it does not count selective events.
- **Construction-mode checklist** (STANDING_DIRECTIVE addendum (b)):
  1. Source distinction: the occurrence b, which is native. The receiver is initially uninformed, and this is forced (Proposition 12.1(c)).
  2. Joint retained structure: E, the loss layer Δ and the supplied motion, all of them inherited or supplied as in section 9.
  3. Receiver consequence: the exact δ_r (Theorem 12.2(a)), attainable up to κ (Theorem 12.3).
  4. Redistribution bound: Theorem 12.2(b).

  Earned here: G for this pair, receiver blankness, the exact consequence and the bound. Still assumed: occurrence (a declared input, by rule), the motion, and I* (Q_r is declared, not shown to be the receiver's own part). Persistence of the written occurrence record under further motion is Theorem 4(a)/(e).

**Relation to known results.** TV_R for one receiver outcome is the *quantum witness* W = |P_b − Σ_a P(a, b)| of Li, Lambert, Chen, Chen and Nori (Sci. Rep. 2, 885, 2012), a no-signalling-in-time test (Kofler and Brukner 2013). Its relation to the trace distance and its maximum 1 − 1/M are due to Schild and Emary (Phys. Rev. A 92, 032101, 2015, [DOI](https://doi.org/10.1103/PhysRevA.92.032101)). Proposition 12.4(a) is consistent with that bound and is derived here from the pinching inequality. **New within UQCF only:** (i) the reading of the witness pair as a G-free, one-prefix separation with a forced blank receiver; (ii) the exact Ky Fan formula for the attainable record at a declared receiver rank (Theorem 12.3; I have not located it in the literature, but it is an elementary consequence of Ky Fan and no priority is claimed); (iii) the contrast that the nonfaithful P2 owner section admits a perfect occurrence record (TV = 1 exceeds the faithful 1 − 1/M bound), tied to absorption-as-move. None of this is new mathematics.

## 13. Next

1. Freeze sections 0–12 of draft 2. Preregister: Theorems 1–4, 12.2 and 12.3, Corollaries 1.1–1.4, Propositions 8.1, 12.1 and 12.4, examples W and P (exact rationals) and the owner-section example. The 96-case table stays exploratory unless it is reproduced independently.
2. Independent producer and checker. The producer uses exact sympy for W, P, the owner section and the Ky Fan formula. The checker uses a different algorithm: the full superoperator E C_U (I − E) and semidefinite or brute-force optimisation over motions for Theorem 12.3.
3. Rejecting controls: closed motion substituted, classical prefix (record must be 0), wrong receiver rank (the saturation condition must fail), a faithful E claimed perfect, and a draft-1 Theorem 4(c) multiplicity-only witness (A = C I_2).
4. Gemini (gemini-3.1-pro-preview) via Actions on the exact frozen text, with explicit reconstruction, counterexamples, inserted mechanisms and a verdict; then readback and a receipt.

Draft 1's step list follows for the record.


1. Freeze sections 0–9. Preregister as a declared finite universe: Theorems 1–4, Corollaries 1.1–1.4, Proposition 8.1, examples W and P (exact rationals), and the 96-case refinement table.
2. Write independent producer and checker code:
   - the producer uses exact rationals or sympy for W and P, and the Heisenberg test U† X U ∈ A for the hierarchy;
   - the checker uses a different algorithm, the full superoperator block E C_U (I−E) and its restriction to Z(A) and Q.

   Both must reconstruct the full 96-case universe with exact identity equality.
3. Add rejecting controls: substituted motion (closed for nonclosed), wrong mask, non-faithful E for Theorem 3, a sector-permuting normalizer for Theorem 4, and false receiver labels.
4. Submit the exact frozen text to Gemini (gemini-3.1-pro-preview) via Actions, inspect the logs, read back, and publish a receipt.
