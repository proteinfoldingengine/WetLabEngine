# Native information boundary: positive extension evidence and the action/access gap

Date: 2026-10-12. Exact inspected parent: `1dbf2e165a0b543214e6e6597fd8cca3bce46450`; tree `6a92b87a743664a0fdd98897082c3d6ed2b1027c`.
Status: scoped conditional analytical result ACCEPTED by separate ChatGPT mathematical/source review; see `native_information_boundary/ANALYTICAL_REVIEW_RAW.md` and `native_information_boundary/RECONCILIATION.md`. No numerical campaign or physical interaction is claimed.

## 1. Approved question and result type

The user approved: "Given only information already justified as available to a native event, what action—if any—follows, and what retained distinction can actually be accessed?"

We first audited what the inspected implementations actually receive, then studied the information boundary exposed by the preceding view-local theorem. The audit finds conditional record/address/update interfaces, but no inspected derivation of an event-accessible complete view together with current common-carrier evidence and an action/access coupling. This is a bounded source assessment, not proof that no native event or mechanism exists anywhere in the framework.

There is a mathematical advance: full common-carrier knowledge is stronger than necessary for some safe independent pruning. Given a complete individual view, positive evidence of retained extensions has an exact, weaker safety classification. That classification is proved below. The extra evidence is not silently declared physically available. Its least-retained member is not adopted as an event law.

All deductions and controls in this note are analytic and known before review or any future numerical campaign. The old no-carrier identity theorem, the old full-carrier classification and the observation-fiber issue are not counted as new discoveries.

## 2. What the inspected sources actually justify

The eighteen exact files are bound in `native_information_boundary/source_readbacks.json`. Relative paths below are under `ResearchHistory/UQCF-GEM/`. A field present in a mathematical state or a verifier is not automatically accessible to an event or observer.

| Input or operation | Source and inspected behavior | Earned consequence | Remaining premise |
|---|---|---|---|
| Actual retained views and subviews | `demos/v16.25-pruning-refinement-closure/TYPE_AND_PROOF.md`, R1–R5 | Literal prefix-closed views and subview contraction are typed; same-union comparison is explicit | These are state/comparison inputs, not a derivation of a native event reading a full view |
| Atomic view-leaf deletion | `demos/v16.26-consistency-increment-law/TYPE_AND_PROOF.md`, P1–P5 | Conditional same-union deletion has the stated increment bound and factorization | Another surviving view must cover the removed node; no actuator or observer access is derived |
| Full structural address | `demos/v15.56-response-selector-obstruction/retained_incidence.py` | Prefix ancestry is intrinsic once the address and retention condition are supplied | The file does not determine the current indexed cover, its view memberships or event access |
| Source/address binding | Same directory, `source_binding.py`, `product_identity.py` | A certified record explicitly binding the source to the full address types source localization | Record binding/certification remains a premise; no current incidence action or readout is produced |
| Provenance hash | Same directory, `ledger_address_equivalence.py` | A full ledger can certify ordered history | A hash alone is not a decodable branch address; historical provenance alone is not current carrier membership |
| Parent/order/depth fields | Same directory, `lineage_schema.py` | These fields do not separate siblings without a descendant-separating address datum | They cannot replace the full address required for an extension witness |
| Existing retained algebra and actual record | `v15/v15.11/ontology_continuity_audit.py`, `pinch`, `select_record`, `run_audit` | Conditional reduction and a supplied positive-weight actual record have defined outputs | RAS and RCR are explicitly existing supplied primitives; no preferred instrument/outcome or incidence-carrier binding is derived |
| Event carrier and generators | `demos/v15.13-independent-events/event_model.py`, `initial_state`, `event_unitary`, `run` | A supplied event model computes conditional states along compatible schedules | The carrier, generator coefficients, dependencies and record string are inputs |
| Already realized record reads | `demos/v15.14-record-dependencies/adaptive.py`, `READS`, `instrument`, `advance` | Readiness and conditional feed-forward follow from the declared read graph and actual earlier bits | The read wiring, controlled operation, state and outcome remain supplied; no current lineage-membership certificate or incidence update is generated |

This audit preserves the positive conditional roles of RAS/RCR and source localization. It neither removes existing premises nor replaces them with an empty-input model. It follows the inherited target-blind response gate and physical-frontier distinction between an input-dependent interaction and an outcome selector. Nondeterministic interaction is eligible if its action and accessible output are derived.

The prior native-record dependency ledger and candidate C1/C3 inspections already locate many of these supplied interfaces. Rechecking them is provenance and scope work, not another obstruction theorem. The rejected native-selection argument also matters: existing order, addresses and references must not be dropped to create an artificial symmetry obstruction.

## 3. Exact question with positive current-carrier evidence

Use finite rooted prefix trees with the same concrete address convention and root o. All supplied order, Genesis and index identities are retained. Fix an indexed palette P with at least two members. A possible current common carrier T is covered by root-containing prefix-closed views (Y_i).

Let K be a fixed finite root-containing prefix-closed set of addresses certified to lie in that SAME CURRENT T. This is positive membership evidence: K is a subset of T, but it need not equal T or describe all its leaves. It may be obtained mathematically by prefix-closing a finite collection of such witnesses. That construction does not supply the certificates or their accessibility.

A deterministic rule F_i^K takes the COMPLETE own view Y, plus K and fixed index/palette data, and returns a root-containing prefix-closed subset of Y. It cannot read other views or an additional description of T. Its input may include an absence fact such as a node being terminal in Y because the complete Y is part of the contract. We do not claim positive address evidence alone supplies that absence information.

Require universal carrier preservation for every finite T containing K and every indexed cover of that T:

    union_i F_i^K(Y_i) = T.

There is no fixed hitting-profile, protected-band, source-family, extra witness-ownership or event-history promise in this quantifier. Finite T=K union Y is an allowed completion. Stronger justified promises would define a different class.

For each input Y form the finite prefix tree Q=K union Y and define

    B_K(Y) = {o} union Anc_Q(Y intersect L(Q)),

where L(Q) denotes its leaves and Anc includes the vertex itself. All these ancestors belong to Y. Equivalently, retain the ancestors of precisely those local leaves of Y that have NO strict descendant in K, together with o.

## 4. Universal safety classification

**Theorem.** The family (F_i^K) preserves the common carrier for every completion and cover specified above if and only if

    B_K(Y) subseteq F_i^K(Y) subseteq Y

for every i and every root-containing finite prefix-closed Y. The right inclusion and output type are assumptions of the class.

**Necessity.** Fix i,Y, put Q=K union Y, and choose a nonroot leaf l of Q belonging to Y. Take the possible carrier T=Q and every other input view equal to Q minus {l}. This is a valid indexed cover; removing a global leaf preserves prefix closure. K subseteq T holds even if l belongs to K. Only view i can retain l after contraction. Since i's rule has the same input (K,Y), universal carrier preservation forces l in its output. Prefix closure forces all its ancestors. The root is mandatory. Root-only cases follow directly. Thus B_K(Y) is necessary.

**Sufficiency.** Fix any actual T containing K and any cover. A global leaf l of T belongs to some Y_i. Because K union Y_i is a subset of T containing l, l is also a leaf of K union Y_i. Thus B_K(Y_i) retains l and its ancestors. Every vertex of a finite T lies above a global leaf, so the outputs cover T. QED.

This proves that B_K is the unique least retained output in the stated information class. The proof determines which contractions are universally safe; it does not determine which actual event occurs.

**Nondeterministic scope.** The same bounds hold if each local input has a nonempty set of possible output subviews and preservation is required for EVERY Cartesian combination of their choices: each possible output must contain B_K(Y). Necessity chooses any violating output and arbitrary outputs for other indices; sufficiency applies to every choice. This covers demonic independent choices, not a claimed probability law. Correlated joint outcomes, extra completion promises and interactions using other views fall outside this product contract. No theorem here forbids those architectures or demands deterministic physics.

**Information limits.** K={o} gives B_K(Y)=Y, recovering the preceding no-carrier identity result. If the complete T is provided as K, then on Y subseteq T this is H_T(Y), recovering the preceding full-carrier classification. For K_1 subseteq K_2, B_{K_2}(Y) subseteq B_{K_1}(Y): additional positive extension witnesses can only remove potentially terminal local leaves from the mandatory set. This is information ordering, not physical duration.

**Repeated action and nonselection.** B_K is idempotent. Every nonroot leaf of B_K(Y) was a retained leaf of K union Y and has no descendant in K; it remains mandatory at the second application. Prefix closure then retains the whole first output. Identity also satisfies the safety classification. Hence even with K supplied, safety does not select B_K or require nontrivial pruning.

## 5. The exact atomic certificate

Let v be a nonroot leaf of the complete own view Y. Then deleting only v is guaranteed to preserve union over all completions consistent with K,Y if and only if K contains a STRICT descendant d of v.

If such d exists, d is not in Y because v is a leaf there. Some other view covers d, and its prefix closure covers v. Thus removing v from this view cannot remove v from the union. For simultaneous independent updates, the theorem's full output bounds supply the collective guarantee; an atomic argument about an unmodified other view alone is not a scheduler.

Conversely, if K has no strict descendant of v, v is a leaf of K union Y. The adversarial completion in the theorem makes it exclusive to this view, so deleting it loses the carrier. K containing v itself is insufficient. This is a necessary-and-sufficient certificate within the declared positive-evidence information class, not a certificate-generation algorithm or a physical deletion command.

The witness need not identify which other view carries d. Coverage and prefix closure supply its existence. However, its address must refer to the same current carrier and address system; an unrelated or historical address cannot play that role.

This extension identifies a weaker requirement than full global-leaf knowledge. The preceding result did not prove full carrier access necessary; this note provides the exact intermediate case. No archive-wide originality or priority claim is made for these elementary arguments.

## 6. Rejecting controls and remaining constraints

**Mere ancestor membership.** Let Y={o,v}. With K={o,v}, completion T=Y and every other view {o} forces v to survive. Knowing v exists does not certify its redundancy.

**One positive extension.** With the same Y and K={o,v,d}, where d is a child of v, B_K(Y)={o}. This is a proof witness for permissible deletion, not a prepared physical interaction or an observer gaining knowledge. The input includes d in the current union and its absence from Y.

**One uncovered local tip blocks a larger deletion.** If Y has two terminal descendants x,y below v and K extends only x, then y remains a leaf of K union Y. Its ancestor v is mandatory even though the x branch may become removable. Evidence for one terminal branch cannot justify deleting an entire cone containing another unprotected tip.

**Stale or foreign witness.** Reusing the extension address d after the actual carrier has become T'={o,v}, or taking d from another Genesis/address system, violates K subseteq T. With Y={o,v} and other views {o}, deleting v loses the carrier. No certificate-validity conclusion follows merely from the record still storing d. If independently justified same-union evolution is maintained, membership of K persists in the union; changing the carrier requires renewed justification.

**Hitting-band safety is separate.** Set K=T in the ternary counterexample of the preceding view-local result. B_K=H_T there, and the root hitting number rises from 1 to 3. Thus partial-information classification does not produce a universal unit-band guarantee or enforce C3 floors. Single-incidence deletion has the inherited atomic bound where its same-union premises hold; repeated updates need the separate endpoint/path constraints already stated in the prior results. We insert no full-state band checker into F_i^K.

**Choice remains open.** B_K and identity can differ on the positive-extension input while both preserve union. Permitting the smaller output is not an event forcing it, nor does a nonempty set of outputs define physical probabilities or retained accessibility.

## 7. What the latest record example actually transfers

The prior five-vertex example has common root o, child u with leaves r,w, and another leaf C. In source zero, Y_a={o,u,r}; in source one, Y_a={o,u}. The memory support at u is initially identical, but the COMPLETE input view to the a-rule is already different. Under the same H_T operation, the output record R=1[a absent at u] equals 1[r absent from the initial Y_a] on those two preparations.

Therefore the operation moves a distinction already present in its full input into the declared memory coordinate. It does not acquire a previously absent distinction for an observer already given that complete input. A receiver restricted initially to the memory coordinate could gain a distinction through a derived coupling—but that receiver access and physical coupling remain precisely the missing obligations. Dependence on a system-side input is not prohibited merely because the receiver lacks it.

This is input accounting for the existing example, not a new observation-fiber impossibility theorem and not a rejection of deterministic information transfer. No claim is made that the two preparations are indistinguishable on their complete system inputs. A fixed stochastic kernel with identical complete channel inputs cannot produce source-dependent output laws merely by naming its outcomes; a native interaction with the source would change that input/action premise and must be justified separately. We do not introduce such a law here.

## 8. Answer to the approved native-event question

The source-address modules justify intrinsic prefix comparison conditional on a properly bound full address. They do not supply the needed assertion that an address belongs to the present common carrier, a complete current own view (or equivalent terminal certificate), access to those facts by the relevant event, or an actual action-to-accessible-record coupling. The adaptive event modules do contain explicit computations on already realized bits, but their event instruments/read wiring remain declared inputs. Identifying one of those bits or instruments with current view membership would insert an unearned connection.

Thus no new native action or physically accessible distinction follows from this inspected packet. The new theorem narrows what a potentially useful input could certify: a current same-carrier strict descendant plus a truthful local-terminal fact can justify the safety of a particular deletion without a global map. It does not establish that such inputs are available or that safety causes execution.

For the positive-extension independent-view route, the next eligible continuation is to identify an inherited construction that gives BOTH (i) current same-carrier membership of a strict descendant and (ii) the complete own-view/local-terminal fact to an event with a justified update relation. If that route is found, specify how a distinct receiver retains and accesses its output. A historical hash, supplied tuple, arbitrary event-bit encoding, legal-move enumerator or another successful prepared record is not that construction. It remains permissible that a derived joint or correlated architecture falls outside the independent-view class.

Reviewed disposition: **POSITIVE_EXTENSION_SAFETY_CLASSIFIED; NATIVE_INPUT_ACTION_ACCESS_UNRESOLVED**. This is a conditional information-boundary theorem and bounded input audit. Native origin/access, physical source correspondence and broad C3/C4–C6 remain OPEN. No numerical enumeration, GitHub Actions execution, historical 527-test replay, Gemini/external review, main merge or numbered-stage CLOSED/CERTIFIED claim is made. Any future numerical campaign must be prospectively frozen under AGENTS.md; these already-known deductions cannot be relabelled as unknown preregistered findings. No maximal-deletion law, fundamental clock, geometry or dark-matter variable is adopted. Path A remains active; time is pruning / ordered recoverability update.
