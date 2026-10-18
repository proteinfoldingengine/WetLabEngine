# Construction: record access. Where an inherited event meets a receiver-owned, readable record

Author: proteinfolding-grokbot (UQCF Science Agent).
Draft 1, 2026-10-17 America/New_York (~21:00 ET loop). Baseline research head `89dab026b5312408cde3a98fd2f9ea416d3027ad`.
Mode: CONSTRUCTION MODE (STANDING_DIRECTIVE addendum (b)); Aaron's 20:00/20:01 ET reconciliation directive (trace one event to a receiver-readable record; separate (i) occurrence, (ii) state change, (iii) access; name the smallest missing implication once).
Status: **unreviewed construction draft.** No milestone, native-access closure, CLOSED/CERTIFIED status, geometry, fundamental clock, dark-matter primitive or heuristic fitting is claimed. Time = pruning / ordered recoverability update. Scratch checks only (disclosed in section 9); independent producer/checker and Gemini come at freeze.

## Credit: what this builds on

Everything load-bearing below is inherited. The new content is the way the pieces are put side by side, and three short results (Theorem 2.1, Proposition 4.1, Theorem 5.1 with Proposition 5.2).

- **v15.13 independent events** (README blob `0d65ef13`): two local record chains A1 -> A2, B1 -> B2 on a supplied carrier, branch operators K_A = k_A (x) I_B, K_B = I_A (x) k_B. This is where the A|B tensor split (receiver locality) comes from. It is supplied there ("illustrative inputs").
- **v15.15 coherent records** (README blob `a6b80640`, `coherent_records.py` blob `fdf5367b`, `copy_gate` line 63, `encoding` line 78, `pinch_records` line 117): each event "coherently writes its computational label into a fresh register using controlled-NOT"; V = sum_r |r>_R (x) K_r.
- **v15.16 partial pruning** (README blob `982e54d0`, `recoverability.py` blob `0a01d2ee`: `encoding` line 58, `basis` line 65, `projectors` line 86, `reduce_input` line 94, `pinch_joint` line 100): K_r = |r><b_r|, Q_s V = V P_s, E_S E_T = E_{S union T}, A_S = direct_sum_s P_s M_16 P_s.
- **FCV P1/P2** (pushforward along r_XY, cumulative E_j, loss D_j), and my frozen **recoverable_pruning_ledger** (Gemini ACCEPTED, run 39070100916): Lemma 12.1 (pinching chain is record-compatible), Theorem 12.2 (G nonincreasing, central C nondecreasing, acquisition = promotion), Witness A, Witness C.
- **proteinfolding-gpt**: [inherited event-to-record reconciliation](../../inherited_event_record_reconciliation/RECONCILIATION.md) (source trace of V997, V1172, V1472, P1/P2, v15.16; continuation contract), the [two-location extension](../preparability_branch_split/TWO_LOCATION_EXTENSION.md) witness, and the accepted [own-view completion](../../own_view_completion_review/REVIEW_ACCEPTANCE.md). I do not repeat GPT's trace of V997/V1172/V1472; I take its findings as given (none of those programs identifies a software output with a receiver-owned record) and work on the one place in the inherited stack where a receiver-local register actually exists: v15.13 to v15.16.

## 0. Result first

1. **Readability is exactly centrality (Theorem 2.1).** Inside a retained algebra, a record can be read without disturbing any retained state, and stays readable under every later inherited pinching, if and only if its projections are central. This derives the "readable, jointly measurable, invariant" half of access premise A from inherited structure. It is a known fact about nondisturbing measurements, applied here.
2. **In the executed v15.16 code, the pruning event and the receiver's own read are the same map (Theorem 3.1).** Pinching record bits S is identical, as a channel, to the Lüders read of the receiver's own register projectors Q_s. After it, the read is repeatable. No readout channel is added. But the receiver's local register state is the same before and after every pinching.
3. **So the ledger's noncommutative "acquisition" is a change of status, not a write (Corollary 3.2).** In Witness C, receiver A's own register already separates the two preparations perfectly before any pinching. The write happened at the v15.15 controlled-NOT, which is a supplied copying interaction.
4. **No receiver-local event can inform a blank receiver (Proposition 4.1).** A transfer needs a joint event acting on source and receiver together. Every inherited pinching and every v15.13 local operator is receiver-local or source-local; the only joint event in the quantum stack is the supplied v15.15 write.
5. **P1 absorption is a native joint event, and its reversible form is the v15.15 write (Theorem 5.1, Proposition 5.2).** On the address-wise configuration space, the inherited pushforward of one complete-fiber contraction factorizes into pairwise moves (x_u, x_a) -> (0, x_a + x_u) from each removed atom u to its owner a. Each move changes the owner's coordinate iff x_u != 0, is not a copy, conserves total grade, and resets u. Its canonical reversible dilation is a controlled-add from u into a followed by discarding the removed address u. For a blank owner and 0/1 grades this is exactly v15.15's `copy_gate` followed by pruning of the control.
6. **The smallest missing implication, named once (section 7):** I* = "a P1 carrier address is a receiver subsystem whose state is its own grade coordinate". Under I*, an admissible complete-fiber contraction necessarily changes an accessible receiver record (obligations (ii) and (iii)), with occurrence (i) still open. Without I*, the commutative stack has the native joint event but no subsystem, and the quantum stack has the subsystem but only a supplied write.

## 1. Setting and obligations

Following Aaron's 20:01 ET directive, three obligations are kept separate throughout:
- (i) **occurrence**: a native event (append, contraction, pinching) happens;
- (ii) **state change**: given the event, the receiver's own record must change, in a way that separates two preparations from the same initial record;
- (iii) **access**: that record is readable by the receiver, with no added readout channel, and is the receiver's own.

Access is split further into (iii-a) readability without disturbance, (iii-b) persistence under later retained operations, (iii-c) ownership (the record is the state of the receiver, not a description of it).

## 2. Readability is exactly centrality

Let A be a finite-dimensional C*-algebra (a retained algebra) and {e_i} a family of projections in A with sum 1. Its Lüders read is L(a) = sum_i e_i a e_i.

**Theorem 2.1.** The following are equivalent:
(a) L fixes A pointwise;
(b) phi o L = phi for every state phi on A (the read disturbs no retained state);
(c) every e_i is central in A.
If moreover A = A_j belongs to a record-compatible decreasing chain (Z(A_j) contained in A_{j+1}, in particular any nested v15.16 pinching chain by ledger Lemma 12.1), then each central e_i stays central in every later A_k, is fixed by every later conditional expectation E_k, and keeps its weight omega(e_i).

*Proof.* (a) <=> (b): L(a) lies in A because e_i lies in A, and states separate points of A. (c) => (a): sum_i e_i a e_i = sum_i e_i a = a. (a) => (c): multiply sum_i e_i a e_i = a on the left by e_j to get e_j a e_j = e_j a, and on the right to get e_j a e_j = a e_j; so e_j a = a e_j for all a in A. Persistence: Z(A_j) is contained in Z(A_k) for k >= j by record compatibility (ledger Lemma 12.1 and v15.11 section 4); elements of A_k are fixed by E_k; weights are restrictions of the same state. QED.

**Corollary 2.2.** In ledger Theorem 12.2, item 5, the projections P_{s'} that become central at step j lay in A_{j-1} but were not central there, so by Theorem 2.1 every read of them disturbed some retained state. "Promotion" is exactly the passage from disturbing-readable to freely readable. This sharpens the ledger's wording: what the pinching changes is readability status.

Prior art: this is the finite-dimensional case of the standard result that a measurement is nondisturbing on an algebra iff its effects commute with it (Heinosaari and Wolf, "Nondisturbing quantum measurements", 2010), and it is the operational content of superselection sectors and of einselected pointer observables (Zurek). Nothing here is claimed as new mathematics. What it earns for UQCF is that (iii-a) and (iii-b) are not separate premises once a record is central in a record-compatible chain.

## 3. The executed register: the pruning event is the receiver's own read

v15.15 and v15.16 execute V = sum_r |r>_R (x) K_r with K_r = |r><b_r| (`basis` line 65 certifies this rank-one form; it fails closed otherwise). The register R is four qubits A1, A2, B1, B2. Receiver A owns the factor R_A = R_{A1} (x) R_{A2}; that ownership is the v15.13 locality split, inherited but supplied there. For S contained in {A1, A2} and a label s on S, Q_s = |s><s|_{R_S} (x) I is a projector on R_A's factor.

**Theorem 3.1 (register realization).** For every input rho and every S contained in {A1, A2}:
(a) Q_s V = V P_s (inherited intertwining, v15.16 README), so the minimal central projections of A_S are realized by projectors local to the receiver's own factor.
(b) The joint pinching `pinch_joint`(., S) equals the Lüders read X -> sum_s Q_s X Q_s. The ordered recoverability update and the receiver's read of its own register are the same channel.
(c) After the pinching, the read is repeatable: sum_s Q_s N_S(rho) Q_s = N_S(rho), and N_S(rho) = direct_sum_s Q_s V rho V^dagger Q_s, whose s-block is V P_s rho P_s V^dagger. The rest of the joint state is conditioned on the record value.
(d) Receiver A's local state is diagonal and unchanged by every pinching: Tr_{not R_A} N_S(rho) = sum_a Tr(P^A_a rho) |a><a|, summed over the four labels a on A1A2 with P^A_a the corresponding v15.16 projector, for every S contained in {A1, A2}, including S empty (N_S is the joint pinched state D_S(V rho V^dagger)).

*Proof.* (a) is the inherited identity. (b): `pinch_joint` keeps the matrix entries whose register labels agree on the bits of S (line 100), which is sum_s Q_s X Q_s. (c) follows because Q_s Q_{s'} = delta Q_s. (d): Tr_sys(V rho V^dagger) = sum_{r,r'} |r><r'| Tr(K_r rho K_{r'}^dagger) = sum_{r,r'} |r><r'| delta_{r r'} <b_r|rho|b_r>, because K_r rho K_{r'}^dagger = <b_r|rho|b_{r'}> |r><r'| has trace delta_{r r'} <b_r|rho|b_r>. The register is already diagonal. Pinching on R_S is a local channel on R_S, so it commutes with tracing out everything else and fixes diagonal matrices. QED.

**Corollary 3.2 (Witness C reread).** For psi_0 = (b_0000 + b_1000)/sqrt2 and psi_1 = (b_0100 + b_1100)/sqrt2, receiver A's register state is diag(1/2, 0, 1/2, 0) versus diag(0, 1/2, 0, 1/2) on A1A2 = 00, 01, 10, 11, at mask 0000, 1000 and 1100 alike (scratch check, section 9). Receiver A's register separates the preparations perfectly before any pinching. The ledger's central-record jump C: 0 -> 2 at step 2 is real as a statement about the center of the recoverable input algebra, but it is not a change in any receiver-local physical state. The register was written at the v15.15 controlled-NOT.

So, for the executed quantum stack: (iii-a), (iii-b) are earned (Theorem 2.1 and 3.1(c)), (iii-c) is inherited from v15.13 locality (supplied there), and the event that changes the receiver's record, (ii), is the v15.15 write. That write is a copying interaction, which addendum 2026-10-17 grades D when supplied. The pinching (the ordered recoverability update) never changes the receiver's local record; what it removes are the receiver-rest coherences (ledger Theorem 12.2, item 6).

## 4. Why a receiver-local event can never inform a blank receiver

**Proposition 4.1.** Let H = H_R (x) H_rest with the receiver's factor H_R, and let Lambda = Phi (x) Psi be any product of channels (either factor may be the identity). If two joint states have the same receiver marginal, so do their images. In particular no pinching with receiver-local projectors, no v15.13 local operator k_A (x) I_B, and no source-local operation can make a blank receiver informed.

*Proof.* Tr_rest (Phi (x) Psi)(X) = Phi(Tr_rest X), since Psi is trace preserving. QED.

This is the no-signalling form of data processing; it is standard. Its use here is to say exactly what kind of event (ii) needs: a *joint* event, acting on the source part and the receiver's factor at once. Inside the inherited quantum stack, the only joint events are the v15.15 controlled writes (system label -> fresh register, and the A1-controlled B2 block), both supplied.

## 5. The commutative stack has the native joint event: P1 absorption as a move

Work on one complete-fiber contraction r: X_s -> X_t of a prefix-closed carrier, with retained owners t in X_t and removed atoms u in X_s \ X_t, each sent to r(u) in X_t. Grade vectors x in R_{>=0}^{X_s} are points of the address-wise configuration space Omega_s = prod_{z in X_s} R_{>=0}. This Cartesian product over addresses is the coordinate structure of a grade function; it is not an added geometry. The inherited P1 pushforward is mu_r(x)_t = sum_{z : r(z) = t} x_z.

**Theorem 5.1 (absorption factorizes into moves).** For a removed atom u with owner a = r(u), let m_{u->a}(x) set x_a to x_a + x_u and x_u to 0, leaving all other coordinates fixed. Then:
(a) mu_r = drop_{X_s \ X_t} o prod_u m_{u->r(u)}, and the moves commute with each other in any order, so no schedule is needed inside one contraction.
(b) Each move acts on exactly the two coordinates {u, a}: it is a joint event in the sense of Proposition 4.1, and it is not a copy (x_u is reset, nothing is duplicated).
(c) The owner's coordinate changes iff x_u != 0. For two preparations that agree everywhere except x_u = g versus x_u = h != g, a blank-or-common owner coordinate becomes x_a + g versus x_a + h. This is ledger Witness A, and with the inside/outside placement it is GPT's two-location witness (A + w, c) versus (A, c) or (A, c + w).
(d) Total grade is conserved by each move. The pair map (x_u, x_a) -> x_a + x_u is noninjective on its full domain (this is the inherited loss arrow, ledger Prop 11.6), but on the two-preparation contract with a common known x_a it is injective, so no global distinction is created (ledger Theorem 11.5).
(e) The owner's coordinate function is an element of a commutative algebra, hence central; by Theorem 2.1 it is freely readable and persists until a itself is removed.

*Proof.* (a): addition is commutative and associative, and distinct removed atoms have disjoint source coordinates; dropping the zeroed coordinates leaves mu_r(x). (b)-(e) are direct. QED.

**Proposition 5.2 (canonical reversible form is the v15.15 write).** Give each address a finite register |x_z> (capacity at least the largest reachable owner total plus one). The unitary C_{u->a}: |x_u>|x_a> -> |x_u>|x_a + x_u> (controlled-add, no wraparound below capacity), followed by discarding the register of the removed address u, implements m_{u->a} on every classical input: the owner's reduced state is the pushforward distribution of x_a + x_u. For a blank owner (x_a = 0) and grades in {0, 1}, C_{u->a} is the controlled-NOT, and the owner's reduced state equals the v15.15 register marginal diag(|<0|v>|^2, |<1|v>|^2) for any control state v.

*Proof.* C_{u->a} permutes basis states, because (x_u, x_a + x_u) determines (x_u, x_a). Tracing out u leaves sum over x_u of p(x_u) times the owner's shifted distribution, which is the pushforward. For 0/1 grades and a blank owner, x_a + x_u = x_u and C is CNOT; tracing out the control dephases the target in the computational basis. QED.

**Corollary 5.3 (event-to-record correspondence).** "v15.15 write, then prune the written-from address" equals "P1 absorption into a blank owner", at the level of the owner's record, for 0/1 grades. The difference between the two stacks is exactly what happens to the source address: v15.15 keeps it (a copy, which leaves a joint record and receiver-rest coherences for pinching to remove), P1 removes it (a move, which leaves only the owner's record). Under I* below, the supplied v15.15 write becomes the reversible form of an inherited pruning step instead of an added copying channel. Landauer's principle applies to the discarded register in the usual way; no thermodynamic claim is made.

## 6. Obligations ledger after draft 1

| Obligation | Quantum register stack (v15.13 to v15.16) | Commutative P1 stack (with Theorem 5.1) |
| --- | --- | --- |
| (i) occurrence | supplied (masks are alternative reductions, v15.16 README) | open; supplied in Witness A; pruning_occurrence gives conditional forcing only |
| (ii) state change at the event | only at the supplied v15.15 write; pinching never changes the receiver's local record (Thm 3.1(d)) | **forced given the event**: owner coordinate changes iff x_u != 0 (Thm 5.1(c)) |
| (iii-a) readability | earned (Thm 2.1, Thm 3.1(b,c)) | earned (Thm 5.1(e), commutative) |
| (iii-b) persistence | earned (ledger Lemma 12.1, Thm 2.1) | earned while the owner is retained |
| (iii-c) ownership as a subsystem | inherited from v15.13 tensor split (supplied there) | **missing: premise I*** |
| separation | yes, from the write | yes (Thm 5.1(c)) |
| global creation | none (Thm 12.2) | none (Thm 5.1(d)) |

Neither stack alone has all rows. The quantum stack has a receiver subsystem with a supplied write; the commutative stack has a native joint write with no subsystem.

## 7. The smallest missing implication

**I*.** Each retained address of a P1 carrier is a receiver subsystem, and its own grade coordinate is that subsystem's state (equivalently: the address-wise configuration space of section 5 is realized as a tensor product of address registers, and a complete-fiber contraction acts on it as the moves of Theorem 5.1).

**Conditional result.** Under I*, an admissible complete-fiber contraction that removes an atom u with x_u != 0 into a retained owner a necessarily changes a's own record, separates preparations that differ in x_u from the same initial record of a, makes that record freely readable and persistent (Theorem 2.1), adds no readout channel, and creates no global distinction. That is obligations (ii) and (iii) together, conditional on I* and with (i) open: the "admissible event necessarily changes an accessible receiver record" result Aaron asked for, in conditional form.

Why I* is smaller than premise A of the frozen ledger: A asked for readability, persistence and locality together. Theorem 2.1 discharges readability and persistence for any central record, and Theorem 5.1 shows the inherited event is already local to the pair {u, r(u)}. What remains is only the identification of an address coordinate with a subsystem. I* is not derived here. It is not contradicted by anything inherited, and v15.13's A|B split is an instance of it on the quantum side, but there it is supplied.

Two honest limits. First, I* is a representation statement; it does not say why a contraction occurs (i). Second, Proposition 5.2 dilates the classical move only on classical (diagonal) inputs; coherent superpositions of grade values are outside the P1 domain and nothing is claimed for them.

## 8. Novelty, stated plainly

- Theorem 2.1: known (nondisturbing measurement iff commuting; superselection; pointer observables). New only in what it discharges for UQCF.
- Theorem 3.1: the identity "dephasing equals Lüders measurement" is textbook (deferred measurement, decoherence). New: applying it to the executed v15.16 code to show that the ledger's noncommutative acquisition is a status change and that the register record was written by the supplied v15.15 copy.
- Proposition 4.1: no-signalling; standard.
- Theorem 5.1 and Proposition 5.2: the factorization of a pushforward into moves and its Stinespring-style reversible form are elementary. New for UQCF: the explicit correspondence between the inherited P1 absorption and the supplied v15.15 write (Corollary 5.3), which locates the copy-versus-move difference as the exact point where the two stacks part, and reduces the access premise to I*.
- Compared with quantum Darwinism: there, redundancy of copies across environment fragments makes a record objective. Here the P1 event is a move, not a copy, so the receiver's record is single-owner by construction; objectivity across many receivers is not addressed.

## 9. Scratch checks (exploratory, not preregistered; disclosed)

- `/tmp/acc/chk10.py` imports the committed v15.16 `recoverability.py` (blob `0a01d2ee`) read-only. V isometry error 1.2e-14; receiver-A register marginals for psi_0, psi_1 at masks 0000, 1000, 1100 as in Corollary 3.2, off-diagonal exactly 0; Lüders read of A1A2 equals `pinch_joint(., '1100')` with error 0 on 50 random inputs; repeatability error 0; intertwining Q_s V = V P_s error 6.6e-15.
- `/tmp/acc/chk11.py`: 2000 random classical inputs with random register sizes, owner marginal of controlled-add then discard equals the pushforward; 200 random control states, blank-owner CNOT marginal equals the dephased control; 200 random pairs with equal receiver marginal stay equal under a receiver-local dephasing. 0 violations.

Neither script is committed. Independent producer and checker code come at freeze.

## 10. Next

1. Look for I* in inherited material before positing it: the V997 Genesis Pin carrier and FCV TYPE_LEDGER for any statement that an address carries its own state; v15.13 for how its A|B split was introduced.
2. Test whether I* is compatible with GPT's own-view result (its record Y_r is also a coordinate, the r-column of the incidence array), so that both witnesses reduce to the same interface.
3. Then freeze sections 0 to 8, preregister, independent producer and checker (Theorems 2.1, 3.1, 5.1, Proposition 5.2), and send the exact frozen text to Gemini (gemini-3.1-pro-preview) via Actions.
