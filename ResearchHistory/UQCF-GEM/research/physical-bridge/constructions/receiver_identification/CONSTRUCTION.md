# Construction: receiver identification. The inherited event names its own receiver

Author: proteinfolding-grokbot (UQCF Science Agent).
Draft 3, 2026-10-18 America/New_York (~04:00 ET loop): adds section 11 (premise G) and changes nothing in sections 0 to 9. Draft 2 (`f366da8b`, sha256 `833c011b…`) is frozen verbatim in `receiver_identification_d2_review/RESULT.md` (preregistration `7103099e`, code `33916d4e`); its review outcome is recorded in that directory, not here. Draft 1 was `512a863d`, frozen in `receiver_identification_review/RESULT.md`; draft 2 corrects an error in draft 1's Proposition 4 that draft 1's review missed (see the revision note).
Mode: CONSTRUCTION MODE (STANDING_DIRECTIVE addendum (b)). Target: the open premise I* of [record_access](../record_access/CONSTRUCTION.md) section 7 ("a P1 carrier address is a receiver subsystem whose state is its own grade coordinate").
Status: **unreviewed construction draft.** No milestone, native-access closure, CLOSED/CERTIFIED status, geometry, fundamental clock, dark-matter primitive or heuristic fitting is claimed. Time = pruning / ordered recoverability update. Per Aaron's standing rule (2026-10-17 22:21 ET), the occurrence of the event is an accepted empirical input; nothing here explains its cause or an observer. Scratch checks only (section 9); independent producer/checker and Gemini come at freeze.

## Revision note (draft 2)

[D2] adopts proteinfolding-gpt's [GPT_DRAFT1_FOLLOWUP.md](GPT_DRAFT1_FOLLOWUP.md) (`2d3ec376`, unreviewed author assessment, obtained analytically before the draft 1 freeze), checked here by scratch code (section 9):
- **Error in draft 1 Proposition 4(b).** The owner law is not p_a * p_u when other removed atoms share the fiber of a. It is nu_a * p_u, where nu_a is the law of everything else in the owner's fiber (the prior owner grade plus every other absorbed atom). Draft 1's equality clause "equality if p_a is a point mass" is false: root a = 0 with removed children u, v; u = 0 under p and 1 under q; v fair on {0,1} under both. The owner prior is deterministic, but the receiver TV is 1/2 while the source TV is 1. The corrected equality condition is that nu_a is a point mass (sufficient, not necessary). The frozen P4 grid had no second atom in the fiber, so its passing did not test this; the Gemini review also missed it.
- **Receiver scope.** By Theorem 2(b), every retained composite subsystem that contains r(u) is also informed. The uniqueness claim is about the unique **minimal (one-address) holder**, not the unique informed subsystem.
- **Positive addition (GPT).** For nonnegative integer grades, convolution by a fixed nuisance law is injective, so the receiver's law changes whenever p_u != q_u; there is no uniform positive lower bound (delta_0 vs delta_1 against nuisance uniform on {0..M} gives TV 1/(M+1)).
New in draft 2 (mine): Proposition 4.2, a sharp lower bound for the deterministic source pair: the receiver's TV is at least the largest atom of nu_a.

## Revision note (draft 3)

[D3] New section 11 (mine): G for this construction. Append-only extension forbids the same-carrier pair of Theorem 2 inside the pinned prefix, so its native form is a difference at an appended entry. The one-location occurrence pair (prefix P against P plus one append) needs only one legitimate append location, which is weaker than both the location-free premise N of preparability_branch_split and GPT's two-location premise, and Theorem 3 then names its single holder at every step for every history. The two-location pair has equal totals and two named holders of opposite sign until their lineages merge. This recovers the branch-split arrival criterion (its Theorem 2.2(2)) as a present-state statement. Sections 0 to 9 are unchanged from draft 2.

## Credit: what this builds on

- **FCV P1 transport** (pushforward mu_r(x)_t = sum over z with r(z) = t of x_z along a complete-fiber contraction r: X_s -> X_t of a prefix-closed carrier; address stability r(t) = t for retained t). Inherited; nothing here modifies it.
- **recoverable_pruning_ledger** (frozen, Gemini ACCEPTED, run 39070100916): Witness A, Theorem 11.5 (no global creation on the two-preparation contract), Proposition 11.6 (loss arrow).
- **record_access draft 1** (`352fac2d`): Theorem 2.1 (readability = centrality), Theorem 5.1 (P1 absorption factorizes into two-address moves), Proposition 5.2 (canonical reversible form = controlled-add, = v15.15 `copy_gate` for 0/1 grades and a blank owner), and the statement of I*.
- **observation_effect draft 3** (frozen, Gemini ACCEPTED, run 39099852840): Theorem 12.5 keep-or-reveal, whose conditional reading is that move-type (absorption) pruning carries intact occurrence records.
- **proteinfolding-gpt**: [record_consumer_trace](../../record_consumer_trace/TRACE.md) (v15.14 `READS`/`advance` is the supplied consumer interface; its section 3 asks for an inherited access relation without a READS table, tensor split, controller or encoder by hand), the [two-location extension](../preparability_branch_split/TWO_LOCATION_EXTENSION.md), and the [inherited reconciliation](../../inherited_event_record_reconciliation/RECONCILIATION.md). GPT's trace flags that P1's additive grade and v15.14's binary outcome have different types; section 5 below addresses this only for 0/1 grades.

## 0. Result first

1. **I* splits in two, and the first half is not a premise (Proposition 1).** Because an inherited grade is an address-indexed function, its configuration space is a Cartesian product over addresses. The observable algebra of that space is canonically the tensor product of one-address algebras, and its canonical reversible dilation is canonically the tensor product of one-address registers. So "an address is a subsystem whose state is its grade coordinate" (call it I*-a) is earned from the inherited data type. What remains (I*-b) is only "that subsystem counts as the receiver".
2. **The inherited event determines which subsystem receives the distinction (Theorem 2).** Take an initially uninformed receiver: two preparations that agree on every retained address. After a complete-fiber contraction r, the retained outcomes differ exactly on the owner set O = {a retained : the removed fiber sums of a differ}. For a single source difference at a removed atom u, O = {r(u)}: exactly one one-address subsystem becomes informed (every composite containing it is informed too, Theorem 2(b)), and it is the one the inherited fiber map names. No READS table, controller, or chosen readout is involved.
3. **The record follows the lineage and has exactly one holder (Theorem 3).** Along any finite history of complete-fiber contractions, a single source difference at u is held, at every step, by exactly one retained address, the lineage image L_k(u) = r_k o ... o r_1(u), and by no other. It is never copied and never lost while the holder is retained. This is the ancestry ledger read as a record trail.
4. **The gain is a redistribution, not a creation (Proposition 4, corrected in draft 2).** For random product preparations, the receiver goes from total-variation distinguishability 0 to TV(nu_a * p_u, nu_a * q_u), where nu_a is the law of the rest of the owner's fiber. This is at most TV(p_u, q_u), with equality when nu_a is a point mass, and it is strictly positive whenever p_u != q_u (injectivity, Corollary 4.1). For the deterministic source pair it is at least max nu_a (Proposition 4.2, sharp). The retained-plus-removed joint distinguishability never increases.
5. **The v15.13 tensor split is the dilation of the P1 address product (Proposition 5).** In the canonical reversible form, every native move acts on exactly the two registers {u, r(u)} and as the identity on all others. So the receiver locality that v15.13 supplied by hand is, under the dilation, the inherited address product.
6. **What remains (section 7).** I*-b is the only identification step left, and given Theorems 2 and 3 it can be stated as an operational definition rather than a hidden choice: the receiver of an event is the retained subsystem whose state carries the event's distinction. Occurrence stays a declared input; preparability G of the two preparations stays the premise of preparability_branch_split.

## 1. Setting

A prefix-closed carrier is a finite rooted forest X_s (every retained node's parent is retained). A complete-fiber contraction keeps an ancestor-closed subset X_t containing the roots, and sends each removed atom u to its nearest retained ancestor r(u); r(t) = t on X_t (address stability). A grade is x: X_s -> Z_{>=0} (or R_{>=0}); its configuration space is Omega_s = prod over z in X_s of Omega_z with Omega_z = Z_{>=0}. When a finite range is needed, Omega_z = {0, ..., N_z} with N_z at least the largest reachable owner total (a capacity for the dilation only; the commutative statements need no truncation).

A **preparation pair** is two grades x, x' on X_s. The receiver side is **uninformed** if x and x' agree on every retained address of the contraction about to happen: x|_{X_t} = x'|_{X_t}. In the random version, preparations are product distributions p, q on Omega_s with equal marginals on every retained address.

## 2. Proposition 1 (I*-a: address subsystems are canonical)

**Proposition 1.** For finite ranges, let B_z be the algebra of functions on Omega_s that depend only on x_z. Then:
(a) the B_z commute, are independent (a product of minimal projections, one from each B_z, is a nonzero minimal projection of C(Omega_s)), and together generate C(Omega_s); the map f_1 (x) ... (x) f_n -> f_1 ... f_n is a canonical isomorphism from the tensor product of the C(Omega_z) to C(Omega_s);
(b) l^2(Omega_s) = tensor product over z of l^2(Omega_z) canonically, by |x> -> tensor product of |x_z>;
(c) each B_z is central in C(Omega_s) (commutative), so by record_access Theorem 2.1 every B_z-record is freely readable and persists under every later retained operation that fixes B_z.

*Proof.* (a) Minimal projections of C(Omega_s) are point indicators 1_{x}, and 1_{x} = product over z of 1_{x_z}(x_z); the 1_{x_z} span B_z and products of spanning sets span. (b) Same map on basis vectors. (c) Commutativity. QED.

So in the commutative stack the subsystem structure that I* asks for is a consequence of the inherited data type (grade = address-indexed function), not an additional premise. This is the classical, trivial case of the observation that subsystems are induced by the algebra of operationally relevant observables (Zanardi 2001; Zanardi, Lidar and Lloyd 2004); Theorem 2 adds that here the inherited events themselves are 2-local in exactly this factorization.

## 3. Theorem 2 (the event names its receiver)

**Theorem 2.** Let r: X_s -> X_t be a complete-fiber contraction and x, x' a preparation pair, uninformed on X_t. Write Delta_a = sum over removed u with r(u) = a of (x_u - x'_u). Then:
(a) mu_r(x)_a - mu_r(x')_a = Delta_a for every retained a, so the retained outcomes differ exactly on O = {a in X_t : Delta_a != 0};
(b) for any set W of retained addresses, the W-marginals of mu_r(x) and mu_r(x') differ iff W meets O; in particular the informed subsystems are exactly the members of O, each informed through its own coordinate only;
(c) if x and x' differ at a single removed atom u, then O = {r(u)};
(d) if x and x' differ only at retained addresses, the pair is not uninformed; if they differ only at removed atoms whose differences cancel within each fiber, O is empty and the event erases the distinction (inherited loss arrow, ledger Proposition 11.6).

*Proof.* (a) mu_r(x)_a = x_a + sum over removed u in r^{-1}(a) of x_u, and x_a = x'_a. (b) Coordinatewise from (a). (c) Delta_{r(u)} = x_u - x'_u != 0 and Delta_a = 0 otherwise. (d) Direct. QED.

What is new here is the reading, not the algebra: the inherited fiber relation r fixes not only *how* the outcome changes (record_access Theorem 5.1) but *which* subsystem receives the distinction. In GPT's terms (record_consumer_trace section 3), the removed-address-to-owner relation r(u) = a is the source-backed correspondence between the native event and the receiver; together with Proposition 1 it supplies items 1 and 2 of that list (the receiver's own state structure, and an existing record within it tied to the event) without a declared READS key.

## 4. Theorem 3 (the record follows the lineage)

Let r_1, ..., r_K be successive complete-fiber contractions X_0 -> X_1 -> ... -> X_K, and L_k = r_k o ... o r_1 the lineage (ancestry-ledger) map, with L_k(t) = t for t retained through step k.

**Theorem 3.** Let x, x' on X_0 differ at exactly one address u. Then for every k, mu_{L_k}(x) and mu_{L_k}(x') differ at exactly one retained address, L_k(u), by exactly x_u - x'_u.

*Proof.* Pushforwards compose: mu_{r_k} o ... o mu_{r_1} = mu_{L_k}, since fibers of a composite are unions of fibers. The difference vector is (x_u - x'_u) e_u, and mu_{L_k} sends e_u to e_{L_k(u)}. QED.

So a single source distinction has a unique holder at every step, the holder is the lineage image of the source, the distinction is never duplicated (single-owner record, unlike the redundant fragments of quantum Darwinism; Zurek 2009), and it is never weakened in the deterministic case. Address stability r(t) = t is what makes "the same holder across steps" well defined. Under multiple differences the holder set at step k is {a : sum over z with L_k(z) = a of (x_z - x'_z) != 0}, and merging can cancel distinctions; this is the inherited loss arrow, now located at the step where two differing lineages first share an owner.

## 5. Proposition 4 (redistribution, random preparations; corrected in draft 2)

Let p, q be product distributions on Omega_s that agree on every address except a single removed atom u (marginals p_u, q_u), and let a = r(u). Let N_a = sum of x_z over z in r^{-1}(a) with z != u (the prior owner grade and every other atom absorbed into a), with law nu_a. By the product hypothesis nu_a is the same under p and q and independent of x_u.

**Proposition 4.** (a) Before the event, every retained marginal is the same under p and q: the receiver side is blank, TV = 0.
(b) After the event, the owner's laws are nu_a * p_u and nu_a * q_u, and TV(nu_a * p_u, nu_a * q_u) <= TV(p_u, q_u), with equality if nu_a is a point mass (sufficient, not necessary).
(c) The retained joint TV after the event equals the owner's TV in (b), and is at most the joint TV of all addresses before the event, which is TV(p_u, q_u). No distinguishability is created; the receiver's gain is at most what the dropped source held.

*Proof.* (a) by construction. (b) Owner = N_a + x_u with independent summands, so its law is the convolution; convolution with nu_a is a channel (data processing); a point mass is a shift, a bijection. (c) Disjoint fibers of a product input give independent output coordinates; every non-owner output has the same law under p and q, so the joint TV equals the owner's TV; the pushforward is a channel on the full joint, so data processing gives the bound. QED.

[D2] Draft 1 wrote p_a (the owner's own prior) in place of nu_a; that is correct only when no other removed atom is absorbed into a. Counterexample to draft 1's equality clause: see the revision note.

**Corollary 4.1 (injectivity; GPT, D2).** For grades in Z_{>=0} with ordinary (non-wrapping) addition, p_u != q_u implies nu_a * p_u != nu_a * q_u. *Proof.* Let d = p_u - q_u, m the least index with d(m) != 0, n the least index with nu_a(n) > 0. The coefficient of nu_a * d at m + n is d(m) nu_a(n) != 0, since every other term with i + j = m + n has i < m or j < n. QED. There is no uniform lower bound: delta_0 against delta_1 with nu_a uniform on {0, ..., M} gives TV = 1/(M+1).

**Proposition 4.2 (sharp lower bound for the deterministic source pair; new in draft 2).** Let p_u = delta_s and q_u = delta_t with k = |t - s| >= 1 (the Witness A form: the source distinction is definite). Then for every nuisance law nu_a on Z_{>=0} with finite support,
max_n nu_a(n) <= TV(nu_a * delta_s, nu_a * delta_t) <= 1,
and the lower bound is attained by nu_a uniform on {0, ..., M} with k = 1.
*Proof.* TV = (1/2) sum_j |nu(j) - nu(j - k)| (shift invariance of TV). Fix n* with nu(n*) = max nu and restrict the sum to the residue class j = n* (mod k). Along that class the sequence nu(n* + i k), i in Z, is 0 for |i| large and takes the value max nu at i = 0, so its total variation is at least 2 max nu. Hence TV >= max nu. For uniform nu on {0..M} and k = 1 the sum is 2/(M+1). QED.

Reading. Whatever else the owner's fiber absorbs, a definite source distinction leaves the receiver with at least the weight of the most likely nuisance value; the receiver's discrimination degrades only by spreading of the nuisance law, never to zero. This is the ledger point of addendum (b) in exact form: the receiver gains information without global creation, by a move from the removed source into the owner, and the gain is bounded below by a property of the inherited fiber alone.

## 6. Proposition 5 (the tensor split of v15.13 is the dilated address product)

On l^2(Omega_s) = tensor product of l^2(Omega_z) (Proposition 1(b)), let C_{u->a} be the controlled-add permutation |x_u>|x_a> -> |x_u>|x_a + x_u> (below capacity), tensored with the identity on every other register.

**Proposition 5.** (a) C_{u->a} commutes with every operator supported on registers other than u and a. (b) Applying C_{u->r(u)} for all removed u (they commute) and then discarding the removed registers gives, on every classical input, the pushforward mu_r on the retained registers. (c) For 0/1 grades and a blank owner, C_{u->a} is the controlled-NOT of v15.15 and the owner's reduced state is the dephased control.

*Proof.* (a) by construction; (b) record_access Proposition 5.2 applied atom by atom, with the moves acting on disjoint source registers; (c) record_access Proposition 5.2. QED.

Consequence: in the v15.13 to v15.16 quantum stack, the receiver factor R_A was supplied by a declared A|B split (record_access section 3, obligation (iii-c)). Under the canonical dilation of the P1 stack, the corresponding split is the inherited address product, and the event is 2-local in it. This does not derive v15.13's specific A1, A2, B1, B2 labelling, and it does not extend the P1 domain to coherent superpositions of grade values (still outside the P1 domain, as record_access section 7 states).

## 7. What is earned, what is still assumed

| Ingredient | Status after draft 1 |
| --- | --- |
| native source distinction | inherited: x_u != x'_u at a removed atom (Witness A form) |
| initially uninformed receiver | by contract: x and x' agree on X_t (Proposition 4(a) in the random form) |
| update rule | inherited P1 pushforward (record_access Theorem 5.1 moves) |
| retained consequence | forced: exactly the owner set O changes (Theorem 2), with a unique lineage holder (Theorem 3) |
| receiver subsystem (I*-a) | **earned**: canonical address product (Proposition 1) |
| receiver identity (which subsystem) | **earned**: named by r (Theorem 2(c)), carried by L_k (Theorem 3) |
| readability, persistence | earned (Proposition 1(c), record_access Theorem 2.1) |
| "that subsystem is the receiver" (I*-b) | **operational definition**, see below |
| no global creation | earned (Proposition 4(c), ledger Theorem 11.5) |
| strictly positive receiver gain in law | earned for Z_{>=0} grades and product preparations (Corollary 4.1); lower bound max nu_a for a definite source pair (Proposition 4.2) |
| occurrence of the contraction | declared empirical input (Aaron, 2026-10-17 22:21 ET) |
| preparability G of x, x' | open; premise of preparability_branch_split (GPT packet ACCEPTED in corrected scope, run 39076009238). [D3] Reduced in section 11 to one typed premise: a single legitimate append at one location |

**I*-b as a definition.** After Theorems 2 and 3, there is exactly one minimal candidate for "the receiver of this event": the unique one-address retained subsystem whose own state carries the event's distinction (composites containing it carry it too, Theorem 2(b)), and that subsystem is named by the inherited fiber map, not chosen. Taking that as the definition of the receiver is not a free choice among alternatives; it is the only identification consistent with (i) receivers being retained subsystems (Proposition 1), (ii) a receiver holding the distinction in its own state, and (iii) Aaron's rule that observation is an empirical input whose actor is not to be explained. [D2, GPT] The factorization shows B_a is a canonical state factor; it does not by itself show that B_a is the receiver's independently available observation algebra, so operational availability stays part of I*-b and is not discharged here. What the definition does not supply is any claim that this subsystem is an agent, or that it "uses" the record; v15.14's consumer step (GPT's trace) is a further supplied interface and is not addressed.

Two honest limits. First, all of this is in the commutative P1 stack; the quantum stack enters only through the canonical dilation (Proposition 5), on classical inputs. Second, Theorem 2 needs the two preparations to differ at removed atoms and agree on retained ones; whether such pairs are natively preparable is G.

## 8. Novelty, stated plainly

- Proposition 1: the canonical tensor factorization of functions on a product space is elementary; observable-induced subsystems are known (Zanardi, PRL 87, 077901, 2001; Zanardi, Lidar, Lloyd, PRL 92, 060402, 2004). New for UQCF: it discharges I*-a, which record_access had listed as missing.
- Theorems 2 and 3: elementary linear algebra of pushforwards. New for UQCF: the inherited fiber and lineage maps identify the receiver of a distinction uniquely and track it as a single-owner record trail. Compared with quantum Darwinism, the record here is single-owner (a move, not a copy), so objectivity across many receivers is not addressed and is not claimed.
- Proposition 4: data processing; standard. New only in placing the ledger's "gain without creation" in exact form for random preparations. Corollary 4.1 is the elementary injectivity of convolution on the nonnegative integers (leading-term argument). Proposition 4.2 is an elementary total-variation bound for a shifted law; I know no specific citation and claim no mathematical novelty, only its use here as a fiber-only lower bound on the receiver's gain.
- Proposition 5: Stinespring-style dilation of a classical move; elementary. New for UQCF: the v15.13 receiver split becomes the inherited address product under that dilation.

## 9. Scratch checks (exploratory, not preregistered; disclosed)

`/tmp/rid/chk1.py` (seed 20261018; not committed): random rooted trees with 2 to 9 nodes, random ancestor-closed retained sets.
- Theorem 2(a): owner set O equals the set of differing retained coordinates, 3000 cases, 0 violations; uninformed-before, 3000 cases, 0 violations.
- Theorem 3: single difference held exactly at L_k(u) along random histories of up to 4 contractions, 5996 step checks, 0 violations.
- Proposition 4: owner TV <= source TV (2000 exact-rational cases), equality for point-mass owner prior (2000), data processing on the joint (2000): 0 violations.
- Proposition 5: controlled-add permutation commutes with random operators on a third register (200), blank-owner reduced state equals the pushforward (200): 0 violations.

Draft 2 additions (exploratory, not preregistered): `/tmp/rid/chk2.py` reproduces GPT's counterexample (receiver TV 1/2 vs source TV 1 with deterministic owner prior), checks the corrected law nu_a * p_u against a brute-force joint pushforward with 1 to 3 other fiber members (1500 random exact-rational cases, 0 violations, 0 injectivity failures) and the 1/(M+1) example. `/tmp/rid/chk3.py` checks Proposition 4.2 on 5000 random exact nuisance laws and shifts (0 violations; bound attained in 1394 cases; uniform M = 5 gives 1/6).

The draft 1 freeze campaign (`receiver_identification_review/`, run 39106192684) remains the record for draft 1; its passing P4 grid had no second fiber atom and so did not test the corrected statement.

## 10. Next

1. (Done for draft 1, run 39106192684.) Draft 2: freeze sections 0 to 8 anew, with a P4 universe that includes several removed atoms in one fiber and a Proposition 4.2 universe, preregister, independent producer (exact enumeration over all ancestor-closed retained sets of all rooted trees up to a declared size and grade range) and checker (different algorithm, e.g. matrix form of mu_r and lineage composition), rejecting controls (wrong owner, copy instead of move, non-ancestor-closed retention, swapped lineage), then Gemini (gemini-3.1-pro-preview) via Actions on the exact frozen text.
2. (Draft 3, section 11.) G reduced to a single legitimate append. Next: freeze section 11 with a preregistered union-carrier universe (all rooted prefixes up to a declared size, every append location or location pair, every history of up to 3 contractions written on prefix addresses), and test whether the inherited V997/v15.56 sources supply the typed event-to-tree action that premise N_1(l) needs, without re-doing GPT's two-location source audit.

## 11. G: the native form of the pair, and what it needs (new in draft 3)

Theorem 2 compares two grades on one carrier that differ at a removed atom. This section asks when such a pair is natively preparable, using only the inherited append-only structure (preparability_branch_split section 1: E-pin, E-addr, E-ret, E-anc) and keeping every legitimacy statement as a typed premise.

**Proposition 11.1 (where a native difference can sit).** Let two histories both be append-only extensions of one pinned prefix tree P with grades x_P. Then they agree on every entry of P (E-addr: append-only extension changes no existing address or grade). So a native preparation pair can differ only at appended entries. In particular the same-carrier pair of Theorem 2 cannot be realized by changing the grade of an existing atom of P; its native form puts the difference at an entry appended after P.
*Proof.* E-addr, as stated in preparability_branch_split Lemma 2.1. QED.

**Lemma 11.2 (zero padding).** Let T = P plus one leaf e under l in P, and let U = P plus leaves e under l and e' under l' (l' in P). Write the history as contractions written in addresses of P, as in preparability_branch_split's common operation: at step k a set X_k of P is retained (ancestor-closed, containing the roots), and an appended leaf is retained exactly when its parent is (it goes with its parent's subtree). Extend a grade on T to U by x_{e'} = 0. Then at every step the retained outcome on U, restricted to the retained addresses of T, equals the retained outcome on T, and the extra retained address e' (if retained) has value 0.
*Proof.* T is ancestor-closed in U, so the nearest retained ancestor of a node of T is the same in T and in U; e' contributes 0 to whichever owner receives it. QED.
Scope: the padded leaf is a bookkeeping device for comparing two different trees on one carrier. It does not assert that a zero-grade entry exists natively, which is the zero-grade scope that preparability_branch_split leaves open.

**Theorem 11.3 (one-location occurrence pair).** Compare the prefix history P (nothing appended) with T = P plus one leaf e of grade w > 0 under l. Pad both to T (x_e = w against x_e = 0). Along every history of contractions written on P-addresses, with lineage maps L_k on T:
(a) at every step the two retained outcomes differ at exactly one address, the holder L_k(e), by exactly w (Theorem 3 applied to the single difference w at e);
(b) the holder starts at e itself (L_k(e) = e while l is retained), and when l's subtree is first retracted it moves to the nearest retained ancestor of l; from then on it follows the lineage of l;
(c) a receiver a in P is informed at step k exactly when L_k(e) = a, that is, from the arrival step s_a(l) of preparability_branch_split until a itself is retracted, after which the holder is a's lineage image. Before arrival a is blank (Lemma 2.1 there);
(d) the distinction is never erased and never copied: a single difference cannot cancel at a merge (Theorem 3).
*Proof.* (a) and (d) are Theorem 3 on T with the single difference at e, together with Lemma 11.2 for the padding of P to T. (b) The appended leaf is retained exactly when its parent is, and a removed node's owner is its nearest retained ancestor. (c) Restates (a) and (b) with s_a(l) = min{k : e in F_k(a)}. QED.

**What this asks of G.** Theorem 11.3 needs exactly two legitimate histories: the pinned prefix P itself (legitimate by N1, the inherited definition) and one append at one location. Call the premise
- **N_1(l):** appending an entry of grade w > 0 under l in P is a legitimate carrier history.
This is strictly weaker than preparability_branch_split's location-free N2 and than GPT's two-location premise (both appends legitimate). It is the carrier form of N3 at one specified location. GPT's source audit (TWO_LOCATION_EXTENSION section 1) shows that the V997 certificate-extension lemma earns syntactic continuity for a supplied event and does not supply the event-to-tree action (parent location, grade). So N_1(l) is still a premise, now in its smallest form: one supplied event, interpreted as one append at one location. Nothing about where or whether the event occurs is explained; the occurrence is the declared empirical input, and the theorem says only that if both histories are legitimate, the receiver named by the lineage records which one happened.

**Theorem 11.4 (two-location pair).** Let l != l' in P, T = P plus e under l, T' = P plus e' under l', both of grade w > 0, padded to U (Lemma 11.2). Along every history of contractions written on P-addresses, with lineage maps L_k on U:
(a) the retained difference at step k is w(delta_{L_k(e)} - delta_{L_k(e')}); so either exactly two retained addresses differ, L_k(e) by +w and L_k(e') by -w, or none, and none happens exactly when L_k(e) = L_k(e');
(b) once L_k(e) = L_k(e'), the distinction is erased at every later step (the lineage maps compose: L_{k+1} = r_{k+1} o L_k);
(c) the total retained grade is the same in both histories at every step: the gain at one holder is matched by the loss at the other, so this is pure redistribution;
(d) a receiver a in P is informed at step k exactly when exactly one of e, e' is in its fiber, which is preparability_branch_split Theorem 2.2(2) restated as a present-state fact about named holders.
*Proof.* (a) Linearity of the pushforward and mu_{L_k} e_z = e_{L_k(z)}, as in Theorem 3. (b) Equal images stay equal under composition. (c) Pushforwards preserve the total. (d) e is in F_k(a) iff L_k(e) = a; if both are, L_k(e) = L_k(e') = a and (a) gives no difference. QED.
Needs: both appends legitimate (GPT's two-location premise). Gains over Theorem 11.3: equal totals, so the source distinction is not visible in the global grade sum, and the receivers are a named pair with opposite records. Cost: a second legitimacy premise and a merge step that erases the distinction (the inherited loss arrow, located at the first common lineage image of l and l').

**Corollary 11.5 (random nuisance).** If the grades on P are drawn from a product law that is the same in both histories, then at step k each informed holder h in Theorem 11.3 or 11.4 sees nu_h * delta_w against nu_h (nu_h = law of everything else in h's fiber), so by Proposition 4.2 its TV is at least max nu_h, and the receiver is never left with nothing while it holds the record.
*Proof.* Proposition 4.2 with the source pair delta_w, delta_0 (k = w), applied to each holder separately; independence of the fiber sum from the appended grade is the product hypothesis. QED.

**Status of section 11.** Earned: Proposition 11.1 (where a native difference can sit), Lemma 11.2, Theorems 11.3 and 11.4, Corollary 11.5, all from E-addr, E-ret, E-anc and sections 3 to 5. Assumed: N_1(l) for Theorem 11.3, or both appends for Theorem 11.4; the occurrence of each contraction; the contractions being written on P-addresses (source-independent, as ledger Theorem 11.5 requires). Not claimed: any native emission law for the append (the P_emit of preparability_branch_split), any derivation of N_1(l) from the V997 sources, or any order selection. Novelty: elementary linear algebra; new for UQCF only in reducing G for this construction to a single typed append premise and in naming the holder of an occurrence record at every step.

Scratch check (exploratory, not preregistered, disclosed): `/tmp/rid2/chk_g.py` (seed 20261018, not committed), random prefixes with 2 to 7 nodes, random append locations, random histories of 1 to 4 contractions on P-addresses: 50,080 step checks of Theorem 11.3(a) and Lemma 11.2, Theorem 11.4(a) and (c) on every distinct-location case (9,825 merged steps), 0 violations.
