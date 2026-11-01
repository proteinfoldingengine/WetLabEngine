# T-240 receiver-delivery boundary for the accepted P1 blind/informative pair

Status: `STAGE_1_SCOPED_THEOREM_PACKAGE_PENDING_INDEPENDENT_REVIEW`. The native bridge stays `NOT_DERIVED`. No claimStatus changes. No physical-law claim is made.

Exact parent: research/uqcf-overlapping-guard-exchange at `dbe016b6f15298280650a50025fe7f20f123b2da`. The preregistration was committed as `b20ae69f2e648dd39aec391367254d53b3720dad` (2026-11-01 06:47 MST), before any script existed.

Execution disclosure: after the preregistration, the producer, verifier and controls were run once locally on the box at 06:49 MST (Python 3.13.5, sympy 1.13.3). All ten preregistered gates were GREEN and all ten controls were rejected. No prediction, definition or control was changed afterwards. The binding evidence is the GitHub Actions run recorded in `EVIDENCE.md`.

Coordination disclosure (slip): T-239-dot-a, T-239-dot-b and T-239-work-a (PR #111 comments 6558724079, 6558758034 and 6558770810, posted 06:39-06:43 MST) and the research-branch documentation commit `8ca3d886` (06:43 MST) appeared before the 06:47 preregistration. I did not inspect them until after the local run. They change no preregistered object, prediction or control. RD-6 and the credits in section 7 were added afterwards to answer them, are analytical only, and are labeled as post-preregistration.

Scope: this is Aaron's receiver-delivery direction (2026-11-01). It asks whether inherited UQCF structure forces the update produced by an actual event to arrive in a receiver-owned retained output, rather than in a complementary subsystem. The accepted counterexample pair W_R/W_E is the standing test.

## 1. The accepted challenge, reconstructed

Sources:
- `p1_receiver_location_resolution/RESULT.md`: freeze `812daac0`, run 40933321991, merged by PR #124 as `71694b92`.
- `P1_CANONICAL_RECEIVER_ACQUISITION.md`.

Setup:
- Carrier: H_S = span{|o>,|p>,|u>,|v>}, with retained Y = {o,p,v}.
- Pruning: u is pruned and r(u) = p.
- Channel: Q = |o><o|+|p><p|+|v><v| and C(ρ) = QρQ + <u|ρ|u> |p><p|.
- Pair: z+ = (1,1,2,1)/5 and z- = (1,1,1,2)/5, with ρ_z = Σ z_j |j><j|.
- Environment: K = E ⊗ R = C² ⊗ C², with basis |e r> at index 2e+r, starting blank.
- Realizations:
  - W_E|j> = W_R|j> = |j>|00> for j in Y.
  - W_E|u> = |p>|10> and W_R|u> = |p>|01>.
  - W_R = (1⊗SWAP)W_E.
- Accepted finding: R is blind for W_E and informative for W_R.

All W in 𝒲(C,K) = {isometries W: H_S → H_S⊗K with Tr_K(W·W†) = C} have the same reduced channel. Therefore no premise phrased through C alone can choose between them.

Notation:
- An interface 𝒜 is a unital *-subalgebra of B(H_S⊗K).
- Its contrast is Δ_𝒜(W) = max{ Tr F (Wρ_+W† - Wρ_-W†) : F ∈ 𝒜, 0 ≤ F ≤ 1 }.
- Its pre-event contrast is Δ⁰_𝒜 = Δ_𝒜 evaluated on ρ_±⊗|00><00|.
- A product interface is 𝒜 = 𝒜_S ⊗ B(K_A) ⊗ 1_{K_B}, with K = K_A ⊗ K_B and 𝒜_S ⊆ B(H_S).

## 2. The frozen missing implication

Premises, each tagged:

| id | premise | tag | source |
|---|---|---|---|
| E1 | an actual measurement/pruning event occurs | ACCEPTED INPUT | `DIRECTION_UPDATE_2026_10_21.md` L19 |
| E2 | the event is a native same-Genesis pruning (g,X)→(g,Y) with retraction r | INHERITED type (L3, L4); event→L3 typing SUPPLIED | foundational `TYPE_LEDGER.md` L21-22; `P1_EVENT_BINDING_FRONTIER.md` |
| E3 | P1 grade update y = P_XY x (fiber pushforward) | DERIVED from E2 | `TYPE_LEDGER.md` L25; `P1_NATIVE_PRUNING_TYPING.md` |
| E4 | physical carrier H_S, encodings Π_X/Π_Y, channel C, diagonal pair | SUPPLIED benchmark | receiver-location RESULT L39, L53 |
| E5 | the joint event is some W ∈ 𝒲(C,K) with blank K | SUPPLIED class | receiver-location RESULT |
| E6 | a designated receiver R with interface 𝒜_R that is initially blind (Δ⁰_{𝒜_R} = 0) | SUPPLIED | receiver-location RESULT L53 |
| E7 | the P1 owner of the removed source is B_{r(u)} = B_p | DERIVED (P1 Theorem 1) | `P1_CANONICAL_RECEIVER_ACQUISITION.md` L41-45, L62-74 |
| K_inh | every inherited constraint on the realization, as inspected (section 4) | INHERITED | section 4 table |

Candidate conclusions:
- A (owner identity): 𝒜_R contains the retained-output owner effect Π_Y(B_{r(u)}), i.e. the effect π_p⊗1_K.
- B (delivery): Δ_{𝒜_R}(W) > 0 for the actual W.
- C (realization independence): Δ_{𝒜_R}(W) takes one value on all of 𝒲_K := {W ∈ 𝒲(C,K) : K_inh(W)}, and that value is positive.

Frozen answer, proved in section 3:
- E1-E7 ∧ K_inh entail none of A, B or C for a general initially blind R.
- They entail B for every admitted W, and also C, exactly when the interface premise OA* ∨ OC holds (Theorem RD-4).
- A is the special case of OA* in which R owns B_{r(u)}.

## 3. Theorems (typed, exact; scoped to the supplied benchmark class)

**RD-0 (characterization and orbit).** W ∈ 𝒲(C,K) iff there are orthonormal e_0, e_u ∈ K such that W|j> = |j>|e_0> for j in Y and W|u> = |p>|e_u>. 𝒲(C,K) is a single orbit of the group {1⊗U : U ∈ U(K)}.

*Proof.*
1. (⇒) For j in Y, C(|j><j|) = |j><j| is pure. A bipartite unit vector whose S-marginal is pure is a product, so W|j> = |j>|e_j>. In the same way, C(|u><u|) = |p><p| gives W|u> = |p>|e_u>.
2. For j ≠ k in Y, C(|j><k|) = |j><k|. Also Tr_K(|j><k|⊗|e_j><e_k|) = <e_k|e_j> |j><k|. So <e_k|e_j> = 1, and Cauchy-Schwarz equality gives e_j = e_k =: e_0.
3. W is an isometry, so 0 = <p|u> = <Wp|Wu> = <e_0|e_u>.
4. (⇐) The columns are orthonormal, so W is an isometry. Checking Tr_K on the 16 matrix units:
   - Y-Y units are preserved.
   - |u><u| maps to |p><p|.
   - |j><u| maps to <e_u|e_0>|j><p| = 0, which equals Q|j><u|Q = C(|j><u|).
5. Orbit: given two orthonormal pairs (e_0,e_u) and (e_0',e_u'), extend both to orthonormal bases. The unitary U carrying one basis to the other satisfies (1⊗U)W = W'. Conversely, Tr_K is invariant under 1⊗U, so the orbit stays inside 𝒲(C,K). ∎

**RD-0′ (rigidity).** If a predicate Φ on isometries satisfies Φ((1⊗U)W) = Φ(W) for all U ∈ U(K), then Φ is constant on 𝒲(C,K). So Φ either admits every implementing realization or none. In particular, the realization set left after imposing every inherited constraint is either 𝒲(C,K) or empty. *Proof.* Immediate from RD-0. ∎

**RD-1 (inherited constraints are U(K)-invariant).** Every inherited structure K listed in section 4 is typed on one or more of the following:
- the native lineage/address/grade data (g, X, Y, r, P, I, R, H);
- the retained source output, through the supplied Π_Y;
- the reduced channel Tr_K(W·W†).

None of these depends on a choice of basis, vector or tensor factor inside the blank complement K. Each therefore defines a U(K)-invariant predicate. By RD-0′ each one admits W_R if and only if it admits W_E. The accepted result already shows that W_R satisfies the inherited contracts, so each one admits both.

*Proof obligation.* This is a per-source claim, discharged row by row in section 4. It is a typing statement about the inherited definitions as written. It is not a theorem about every conceivable future definition. ∎

**RD-2 (minimum over realizations).** Let 𝒜 = 𝒜_S ⊗ B(K_A) ⊗ 1_{K_B} be a product interface with dim K_B ≥ 2. Then min_{W ∈ 𝒲(C,K)} Δ_𝒜(W) = Δ_{𝒜_S}(C) := max{ Tr F (C(ρ_+) - C(ρ_-)) : F ∈ 𝒜_S, 0 ≤ F ≤ 1 }.

*Proof.*
1. (≥) For any F ∈ 𝒜_S with 0 ≤ F ≤ 1, the element F⊗1_K lies in 𝒜. Also Tr (F⊗1)WρW† = Tr F C(ρ). So Δ_𝒜(W) ≥ Δ_{𝒜_S}(C) for every W.
2. (attained) Pick a unit vector a ∈ K_A and orthonormal b_0, b_1 ∈ K_B. Set e_0 = a⊗b_0 and e_u = a⊗b_1; by RD-0 this defines a realization W_0 ∈ 𝒲(C,K).
3. Write σ = Tr_{K_B}(W_0 ρ W_0†). For diagonal ρ, this is Σ_{j∈Y} z_j |j><j|⊗|a><a| + z_u |p><p|⊗|a><a| = C(ρ)⊗|a><a|. (The cross terms vanish because b_0 ⊥ b_1.)
4. For G ∈ 𝒜_S⊗B(K_A) with 0 ≤ G ≤ 1, Tr G (C(Δρ)⊗|a><a|) = Tr <a|G|a> C(Δρ). The compression <a|G|a> := (1⊗<a|)G(1⊗|a>) lies in 𝒜_S, and 0 ≤ <a|G|a> ≤ 1. Hence Δ_𝒜(W_0) ≤ Δ_{𝒜_S}(C). ∎

**RD-3 (complete complement).** If K_B is trivial, so that 𝒜 = 𝒜_S⊗B(K), then Δ_𝒜 is constant on 𝒲(C,K). *Proof.* Conjugation by 1⊗U maps {F ∈ 𝒜 : 0 ≤ F ≤ 1} onto itself, and RD-0 gives the orbit. ∎

For the trivial S-interface with the complete K, the value is (1/2)(|Σ_Y Δz| + |Δz_u|) = |Δz_u|. For the canonical pair this is 1/5.

**RD-4 (minimal premise: necessary and sufficient).** Let R have a product interface 𝒜_R. Let 𝒲_K be the realizations admitted by K_inh, which by RD-1 and RD-0′ is all of 𝒲(C,K). Then delivery holds for every admitted realization, i.e. min_{W∈𝒲_K} Δ_{𝒜_R}(W) > 0, iff

- **OA\*** Δ_{𝒜_{R,S}}(C) > 0: R owns an effect on the retained source output that separates C(ρ_+) from C(ρ_-); or
- **OC** K_B is trivial (R holds the complete complement) and Δ_{𝒜_R}(W_E) > 0.

*Proof.* If dim K_B ≥ 2, RD-2 gives min = Δ_{𝒜_{R,S}}(C). If dim K_B = 1, RD-3 makes Δ constant, so the minimum is the value at W_E. These two cases are exhaustive. ∎

Further consequences:
- Initial blindness (E6) is an extra requirement that both OA\* and OC must satisfy. P5 enumerates the commutative S-interfaces with the trivial K-part: exactly three are initially blind and satisfy OA\*.
- In the one-source extensive setting of P1 Theorem 1, the one-address persisting factors are B_b for b in Y. Theorem 1(c) says exactly one of them, B_{r(u)}, is pre-blind and post-informed. Restricted to one-address interfaces, OA\* is therefore "R owns B_{r(u)}", which is conclusion A.
- Conclusion C requires the contrast to be realization-independent. That holds when 𝒜_R acts only on S or holds all of K. It fails for a proper complementary factor (P4: TR and TE vary with W).

**Necessity of the extra premise (no inherited route).** The conjunction of the inherited constraints is U(K)-invariant (RD-1). By RD-0′ it cannot shrink 𝒲(C,K) to a subset on which a proper complementary factor is always informed: by RD-2 that factor's minimum is attained at W_0, and W_0 is admitted.

So any premise that makes a proper complementary factor such as R deliver must be one of:
- **(NF) factor-naming:** a non-U(K)-invariant constraint on W that names a factor or vector of the blank complement. Example: "the record of the removed summand is written into R", which as a predicate is k_R(W) := Tr_E|e_u><e_u| ≠ Tr_E|e_0><e_0|. P7 confirms that k_R is true for W_R, W_M and W_N and false for W_E.
- **an interface premise** (OA\* or OC) about what R owns.

No inspected source supplies NF, and NF is not a consequence of OA\* or OC.

**RD-6 (exact surviving blind set for the designated R; collapse of realization-language minimality; added post-preregistration).** Let R be the designated receiver, with interface 1_S⊗1_E⊗B(R). For W ∈ 𝒲(C,K), write τ_x := Tr_E|e_x><e_x| for x ∈ {0,u}.

1. For diagonal input, R's state after W is (1-z_u)τ_0 + z_u τ_u. So Δ_R(W) = |Δz_u| D(τ_u, τ_0), where D is the trace distance. For the canonical pair this is D(τ_u, τ_0)/5.
2. Hence the blind set is B_R = {W ∈ 𝒲(C,K) : τ_u = τ_0}. It is nonempty, containing W_E and every e_0 = a⊗b_0, e_u = a'⊗b_0 with a ⊥ a'. It is not a single point: it contains the whole family (U_E⊗1_R)W_E, and more.
3. A realization constraint K forces delivery to R exactly when its admitted set avoids B_R, i.e. when K ⇒ (τ_u ≠ τ_0) on 𝒲(C,K). The pointwise condition τ_u ≠ τ_0 is itself the weakest such constraint. It is exactly the accepted location criterion of p1_receiver_location_resolution/RESULT.md §5.
4. So in the language of constraints on realizations, Target E collapses to restating the goal (this agrees with T-239-dot-b and T-239-work-a). Any non-tautological K that forces delivery must at least break every unitary of K that carries an admitted realization into B_R. In particular K cannot be U(K)-invariant (RD-1), and it must separate R from E.
5. For the designated R, 𝒜_{R,S} = C·1. So OA\* fails (Δ_{C1}(C) = 0) and OC fails (E is nontrivial). RD-4 therefore confirms that delivery to R is not guaranteed under any U(K)-invariant constraint set.

Consequently, a non-tautological minimal new premise can live only in identification language, not in realization language:
- OA\*: identify the designated R's available output with a separating retained-output effect, as in I* or B_a→Access.
- OC: identify R with the complete complement.

Both are NEW premises. Adopting either by definition would be the redefinition that T-239-dot-a and T-239-work-a warn against. This result states each premise as the boundary and does not adopt it.

*Proof.* Item 1: for diagonal ρ, Tr_S(WρW†) = Σ_{j∈Y} z_j|e_0><e_0| + z_u|e_u><e_u|. Then trace E, and the pre-event R state is |0><0| for both preparations. Items 2-5 follow from item 1, RD-0, RD-1 and RD-4. ∎

**RD-5 (what W_R actually delivers).** For every W and diagonal input:
- the complete complement holds (1-z_u)|e_0><e_0| + z_u|e_u><e_u|, a function of z_u only;
- the retained source output holds Π_Y(y) with y = P_XY z, i.e. y_p = z_p + z_u.

In W_R, R's state is (1-z_u)|0><0| + z_u|1><1|.

Now take the removed-summand pair z'_+ = (1,2,1,1)/5 and z'_- = (1,1,2,1)/5. It has equal y, so every S-interface is blind both before and after (P6). Yet R under W_R is informed with contrast 1/5. So what W_R hands to R is the fine-grained split inside the fiber (the ker P_XY direction e_u - e_p), not the P1 owner coordinate y_{r(u)}. The P1 owner B_{r(u)} lives on the retained source output (through the supplied Π_Y), and every realization delivers to it (RD-2 with K_A trivial). The W_R/W_E freedom concerns only where the discarded fine-grained record goes.

## 4. Adversarial test of every inherited structure K

Every row evaluates the K as defined in its source. "Admits both" means K is U(K)-invariant (RD-1), so it holds for W_R exactly when it holds for W_E.

| # | inherited K | source (parent dbe016b6) | domain it is typed on | W_R | W_E | separates? |
|---|---|---|---|---|---|---|
| 1 | lineage/ancestry ownership (L1, retraction r L4) | foundational `TYPE_LEDGER.md` L19, L22; `PROOFS.md` L13-19 | words of X, Y; r: X→Y | admits | admits | no |
| 2 | retained-source identity (L6/L7; source binding) | `TYPE_LEDGER.md` L24-25; v15.56 `source_binding.py` (genesis_id, provenance_root, source_event, full_lineage_address) | grades on X, Y; source fields have no output-factor slot | admits | admits | no |
| 3 | P1 owner correspondence | `P1_CANONICAL_RECEIVER_ACQUISITION.md` L41-45 (B_a, eq. 3), L62-74 (Thm 1) | factors indexed by a ∈ Y; owner state is the p-population of C(ρ) | admits | admits | no |
| 4 | retained algebra / record compatibility | `complementary_record_screen/RESULT.md` L74-80 (Prop 1: complement information fixed only up to environment isometry); `measurement_first_review/RESULT.md` L17 (v15.11 RAS/RCR) | retained algebra on S; complement only up to isometry, i.e. explicitly U(K)-invariant | admits | admits | no |
| 5 | native subsystem ownership | P1 eq. (3) L45 | ⊗_{a∈Y} B_a; K carries no address | admits | admits | no |
| 6 | actual-record primitives (RCR) | `measurement_first_review/RESULT.md` L17 | conditional state of an already specified record in the retained algebra | admits | admits | no |
| 7 | provenance binding | v15.29 README L5 (`PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED`); `source_binding.py` | provenance_root over lineage; no complement factor | admits | admits | no |
| 8 | preservation/retention | `ancestry_retention_review/RESULT.md` L42 (contract R); isometry of W | grade totals on fibers; both W isometric | admits | admits | no |
| 9 | composition/compatibility on source and receiver | `PROOFS.md` L13-19 (P_YZ P_XY = P_XZ); `TYPE_LEDGER.md` L39 (naturality under retained relabelings); T-235 PN/SX (SUPPLIED reads) | maps on X, Y and on reduced channels; composites of dilations are again orbit-related | admits | admits | no |
| 9a | operational identification I\* (retained address is an actual receiver subsystem) | `constructions/record_access/CONSTRUCTION.md` §7 (explicitly SUPPLIED) | identification premise, not a realization constraint | n/a | n/a | not inherited; it is the OA\* route |
| 9b | actual-record selection select_record | v15.11 `ontology_continuity_audit.py` L58-73; T-239-dot-b | supplied projectors on S; conjugation-covariant, select(VωV†, VP_bV†, b) = V select(ω,P_b,b) V† | admits | admits | no |
| 10 | owner-vs-environment distinguishing rule | none found: receiver-location RESULT L53 (factorization/access are explicit conditional premises); `partial_complement_capacity/RESULT.md` L15; T-233 N2; `TYPE_LEDGER.md` L45 (quantum/CPTP leg supplied) | (not defined) | n/a | n/a | no K exists |

Admission gate for each candidate premise (the 5 questions from the direction):

| question | OA\* | OC | NF |
|---|---|---|---|
| 1. inherited or new? | NEW interface premise (special case "R owns B_{r(u)}" = A) | NEW interface premise | NEW dynamics premise |
| 2. stated without named factor, inserted geometry, clock, or fitting? | yes: an effect on the retained output | yes: "all of K" is basis-free | no: names a factor/vector of K |
| 3. rejects W_E as a delivery to a proper factor R? | not applicable; it relocates R to the owner, where both W deliver | not applicable; both W deliver to all of K | yes |
| 4. necessary for guaranteed delivery? | yes, jointly with OC (RD-4) | yes, jointly with OA\* | not for delivery as such; needed only if R must be a proper complementary factor |
| 5. derivable from the inspected sources? | no: B_a→Access remains open (T-156; `P1_EVENT_BINDING_FRONTIER.md` AB) | no | no |

Counterexamples showing that weaker premises fail (all reproduced by the certificate):
- (w1) "R is some initially blind complementary factor" (TR): W_E gives 0 on the trivial partition.
- (w2) "R is a proper factor of K and the reduced channel is C" (TE): W_R gives 0.
- (w3) "R owns a retained effect" without separation, e.g. π_o: the contrast is 0.
- (w4) "R separates after the event" without initial blindness, e.g. π_v: Δ⁰ = 1/5 ≠ 0.
- (w5) "R owns a cone total {o}{p,u,v}": contrast 0. This is consistent with T-225 and T-235 Prop O (cone totals are invariant and cannot record the update).
- (w6) OC is sufficient without OA\*. So OA\* alone is not necessary, and the minimal premise is the disjunction.

## 5. Separation of claims

- Mathematical (proved here, scoped to the supplied benchmark class): RD-0 through RD-5, and RD-1 as a per-source typing table.
- Physical: none. Whether some physical receiver is the retained-output owner (OA\*), or holds the complete complement (OC), is an identification/access question. It is not derived.
- Derived from native premises: E3 and E7 only (the P1 pushforward and owner).
- Supplied: E4, E5 and E6, the Hilbert encoding Π_Y, and the factorization K = E⊗R.
- Does this constrain delivery? Yes, negatively and sharply: no inherited K can force delivery to a proper complementary factor (RD-1 + RD-2). Positively: delivery to the owner on the retained output is realization-independent (RD-2 with K_A trivial). This depends on the supplied Π_Y.
- Observable distinction: W_R and W_E are distinguishable only through effects that name the E/R factorization. Every effect in 𝒜_S⊗1_K, and every effect on all of K, gives the same statistics for both (RD-3). No native observable is identified that tells them apart.

## 6. What is not derived

- B_a → Access (that a physical receiver can read the owner factor): open, as in T-156 and `P1_EVENT_BINDING_FRONTIER.md`.
- Event→L3 typing and the Hilbert/CPTP encoding Π_X, Π_Y, C: supplied.
- Any NF-type law that selects where the fine-grained removed-summand record goes: absent, and by RD-0′ not obtainable from U(K)-invariant inherited structure.
- Generality beyond this benchmark class (one removed address, diagonal pair, blank finite K, product interfaces). Non-product interfaces are covered only by RD-3 and RD-0′, not by RD-2.

## 7. Relation to concurrent and earlier entries; novelty limits

- T-239-dot-b already proved the SWAP case of RD-1: constraints that factor through n, Π_X, Π_Y, P/I and C agree on W_R and W_E. It also proved conjugation-covariance of select_record. RD-0/RD-0′ extend this from SWAP to the full U(K) orbit. RD-2 and RD-6 answer its open question ("other blind realizations may survive") with the exact surviving blind set and the realization minimum for every product interface.
- T-224 and T-239-work-a already noted that the retained-source p-effect is realization-independent, and gave the z_u versus y_p type check. RD-5 and the K_A-trivial case of RD-2 restate those points as consequences of the general theorem. They are not new.
- T-239-dot-b and T-239-work-a warned that realization-language minimality is tautological. RD-6 proves that collapse exactly and locates the only non-tautological premise class (identification: OA\* or OC).



RD-0 is the standard Stinespring uniqueness-up-to-partial-isometry theorem, specialized here. RD-2 is a scoped observation about compressions. The contribution is the typed application to the UQCF P1 owner question: the reframing that the owner lies on the retained output, the per-source invariance table, and the minimal-premise boundary OA\* ∨ OC versus NF. It is not a new physical result. scientific_breakthrough: false.
