# What occurrence and localization do not determine in the source-withdrawal interface

Author: proteinfolding-gpt / ChatGPT research session with Aaron.
Date: 2026-10-25 (America/Phoenix).
Research source commit: 3ceb814258f43774b4af1352379ffcd0bd079599.
Status: analytical draft frozen for independent review. Native bridge NOT_DERIVED.

## 1. Decision and scope

On the explicitly specified finite support interface below, nonempty nesting, legal incidence edits, exact all-one hitting profiles, proper source-event occurrence and source localization do not determine whether the initially blank receiver acquires the source bit. There are two explicit completions satisfying those conditions. One ends with the source bit at the receiver; the other leaves that receiver blank throughout.

This is a scoped non-entailment result, not an independence theorem for the whole UQCF-GEM foundation, an impossibility of physical interaction, or a claim that nature can choose either completion. No equivalence between a formal completion and a physical measurement is established. The two completions are counterinterpretations of the event correspondence left unspecified by this interface.

The positive completion is T-109's existing construction. T-097 already showed that a proper source deletion can leave a receiver blank. The specific addition here is an exact-profile blank completion on T-109's seven-vertex carrier: even imposing the all-one profile at every step does not resolve the event-typing ambiguity. The decision is to stop trying to obtain the physical correspondence from these constraints alone. No archive-wide novelty is claimed.

## 2. Exact premises being tested

All paths below are relative to ResearchHistory/UQCF-GEM/ at the research source commit unless another commit is specified. SOURCE_PACKET.json binds the exact contents or excerpts and their full-source identities.

P1. Fixed rooted carrier, fixed palette, nonempty supports, fixed full root support, child support contained in parent support; a primitive changes one incidence at one nonroot vertex while preserving these constraints — INHERITED MATHEMATICAL GRAMMAR [demos/v16.53-four-child-boundary/NATIVE_ADMISSIBILITY.md, Carrier and extension; blob ebc315f7f2f6423fe9f6861cc3b8a0cfcf8420f2]. This source expressly does not provide physical interpretation or dynamics.

P2. The tree, reference labels and prepared source pair defined in section 3 — SUPPLIED, unchanged from T-109. Relative mathematical admissibility is proved here; actual physical preparation is not.

P3. The entire displayed completion preserves h_o=h_u=1 — SUPPLIED restriction strengthening the allowed-history class for this test. The definition of h is INHERITED from P1. This restriction is checked, not presumed to follow from arbitrary native edits.

P4. An actual atemporal measurement/pruning occurrence exists — ACCEPTED INPUT [research/physical-bridge/DIRECTION_UPDATE_2026_10_21.md, section 2; blob 62aa72a8c813840e0744496ab8c3eb2abc44eabf]. Its identification with the terminal proper source deletion of either displayed history is a SUPPLIED interpretation for comparing realizations. The event is actual within each interpretation, not an absent event or a no-op. No probability law, fundamental clock, universal completion, or cause of occurrence is assumed.

P5. The event is localized at the same source vertex u with a common Genesis/reference system — SUPPLIED association using INHERITED localization typing [demos/v15.56-response-selector-obstruction/source_binding.py, classify; blob a1df8db6c1d1b3fd4491a5f502267841725f3f32]. Its rule is source_event -> (genesis_id, full_lineage_address). The inspected function does not prescribe a withdrawn label or a receiver read. A provenance commitment must be consistent with its actual history; different completed histories need not have identical provenance roots or event receipts. No hash collision or equality of distinct full histories is asserted. Such receipts are not part of the receiver interface below.

P6. For the event-typing test, grant the receiver the row R_v(S)=S_v and common references — SUPPLIED ACCESS, deliberately stronger than the earned physical interface. Initial receiver states agree exactly. A failed implication even under this granted access cannot be repaired merely by giving the same endpoint row more readable coordinates. Section 6 removes this grant to examine access separately. No claim is made that row access follows from knowing an address or owning a label's entire view.

P7. A finite sequence is a mathematical witness to joint completion, with the distinguished source deletion last. Its indices express edit order, not physical duration. The physical event-to-completion association is unspecified — SUPPLIED comparison class. In particular P1-P7 do not require deletion of a, freezing reference supports, preservation of the source bit, deletion-only intermediate histories, or a minimum-length completion. None of those omitted conditions is being claimed false or impossible; adding one changes the premises being tested.

These are the complete premises of the propositions below. Existing results with stronger contracts remain intact. We do not claim that every other native construction, lineage axiom, retained-source law, or physical observation is modeled by P1-P7.

## 3. Common prepared object and positive completion

Use palette P={a,b0,b1}. Vertex o has children u,z1,z2,z3; u has leaf children v,w. Every z_j is a leaf. For s in {0,1}, the preparation F_s is

    S_o=P; S_u={a,b_s}; S_v=S_w={a}; S_zj={b0,b1}.

Only the source support at u differs. Both preparations satisfy P1. At u, both children share a. At o, all children share b_s. Thus both internal hitting numbers equal one. The complete granted receiver row is {a} in both cases.

The positive completion C_s is the T-109 path

    +b_s(v), +b_s(w), -a(w), -a(v), -a(u).

Each addition uses a label already in its parent. After both additions, deleting a from either receiver leaf preserves nonemptiness; deleting a from u is then legal because neither child contains a and b_s remains at u. Nesting is preserved throughout. The children of u share a during addition and b_s during deletion. Every child of o contains b_s throughout. Therefore h_o=h_u=1 at every state.

The final source row and both receiver rows are {b_s}; the reference rows are unchanged. The final proper deletion is at u and removes the same label a in both source preparations. More generally, conditional on an event with pre-source row {a,b_s} deleting a, every valid immediate endpoint forces the same descendant singleton, because a nonempty subset of {b_s} is {b_s}. This is the existing source-withdrawal implication, not a newly derived physical event law.

## 4. A blank completion with the same exact profile

On the identical F_s, consider B_s:

    +a(z1), +a(z2), +a(z3), -b_s(u).

All four primitives are proper. The reference additions are legal because a is in their parent o and absent from each reference leaf before its addition. They preserve nonemptiness and nesting. Throughout these additions, every root-child support still contains b_s, so h_o remains one; v and w are untouched, so h_u remains one.

After the three additions, every reference support equals P. The final deletion at u is legal: b_s is absent from both children v,w, and a remains at u. Afterward all four root children share a, so h_o is still one. Both receiver leaves remain {a}, so h_u is still one. The final full state is identical for both s:

    S_o=P; S_u=S_v=S_w={a}; S_zj=P.

The receiver row never changes during B_s. Thus this is stronger than erasing a transient receiver write: any observation of this row alone sees only {a}. No timing or other interface is included in that statement.

Using preorder (o,u,v,w,z1,z2,z3), the column arrays (a,b0,b1) for s=0 are

    [15,115,113]
    [31,115,113]
    [63,115,113]
    [127,115,113]
    [127,113,113].

For s=1 interchange the two b columns. These integer encodings are hand calculations; they are not an executed numerical campaign. Each adjacent pair differs in one bit. In both families, the source changes only at its terminal deletion. The rule for B is the same on either input: add the common label a to each reference leaf, then delete the unique member of S_u minus {a}. This is a mathematical rule, not an adopted physical selector. Swapping b0 and b1 carries each history family to its other member, so this comparison does not depend on a preferred one of those two labels.

The reference additions are essential to this particular exact-profile blank witness. Deleting b_s(u) immediately in the seven-vertex preparation would make h_o=2. B_s avoids that change through legal operations on initially common reference rows. If an independently justified event contract forbids those reference edits, this specific blank completion is excluded; that restriction is absent from P1-P7. We do not claim a blank completion under that stronger contract.

## 5. Scoped non-entailment of acquisition

Let Q be the statement that the final granted row distinguishes F_0 from F_1. Interpret the actual source event in P4-P5 as the final deletion in C_s. Sections 2-3 give realizations of P1-P7 in which Q holds: the outputs are {b0} and {b1}.

Interpret it instead as the final deletion in B_s. Sections 2 and 4 give realizations of P1-P7 in which Q fails: both outputs are {a}. Actual occurrence, source localization, exact profiles, fixed carrier and legal primitive constraints hold in each interpretation. Therefore P1-P7 alone entail neither Q nor its negation. This is independence only relative to this explicitly defined interface.

The terminal deleted label differs between the two interpretations. That is the missing event-typing content, not a loophole hidden from the claim. Localization at u is not identification with -a(u). The histories and post-event provenance commitments also differ; they are not assumed identical inputs to a hypothetical decoder of complete event records. No claim is made that a fully specified physical event record can have two incompatible meanings.

This argument does not infer that a measured physical event is free to choose either interpretation. It shows why the existence and localization assertions, as formalized here, cannot themselves select the positive one. It neither explains nor challenges why measurement occurs. It also does not rule out a different source pair, receiver, native event law, or probabilistic prediction.

## 6. Access is an independent obligation even after fixing the positive event

Now fix C_s and its endpoint, thereby granting the positive event correspondence. With P6 the decoder d({b0})=0, d({b1})=1 gives the source bit. If P6 is removed, P1-P5 and P7 contain no constraint requiring this row to be available to an owner. They can instead be extended with a constant available output O(S)=blank in both preparations, without changing any state, primitive, source event or localization statement. Thus those statements plus the positive state transition still do not entail accessible acquisition.

The constant output is a logical counterinterpretation of unspecified access, not a physical theory, not an assertion that all observations are constant, and not a rejection of the supplied row-reader model. Actual empirical observations or additional native reader laws would constrain it. It demonstrates only that these premises contain no such law for this receiver.

Source existence and reference/address identity do not fill either missing arrow. Conversely, endpoint erasure in B_s says nothing against a separately justified recorder for the transient states of other paths. T-112's distinction between endpoint reads and history access is preserved.

## 7. What would change the decision

A sufficient additional event premise for this construction is: the actual localized occurrence commits withdrawal of a at u from the specified pre-source support {a,b_s}, on the retained carrier. A sufficient additional access premise is: the resulting receiver row, or a separating function of it with justified references, is available to the same initially blind receiver. Both are EVALUATION-ONLY SUPPLIED extensions here. Neither is claimed necessary for all possible acquisition mechanisms or derived from the sources.

Given both, the positive singleton proof already supplies acquisition. Adding them by declaration would make a conditional model, not close the physical bridge. The useful future evidence must provide an event-to-edit correspondence or a receiver-owned consumer that rules out the corresponding counterinterpretation. More normalization code, endpoint classifications, certificate hashes, or repeated checks of these paths cannot do that.

No experimentally testable physical prediction is asserted without preparation and measurement correspondence. We have not established that the entire UQCF-GEM theory lacks such correspondence. A relevant existing axiom with a named producing operation would reopen this bounded decision; an unsupported label of INHERITED would not.

## 8. Review and verification contract

This full argument and its exact source packet are frozen before independent Gemini review through GitHub Actions. The reviewer must reconstruct each history, nonemptiness/nesting, every hitting number, the proposition's precise premise set, event localization versus withdrawn-label content, provenance-root scope, and the separate access counterinterpretation. It must challenge any inference extending this result to the complete foundation or to physical impossibility, and assess whether the decision adds anything beyond the previously known blank controls.

No scientific program, numerical enumeration, simulator or archived campaign has been run for this argument. Source integrity, hashing and review infrastructure checks are not scientific experiments. All displayed calculations were developed analytically before freezing and are not preregistered predictions. No independent acceptance, numbered-stage certification, main merge or physical milestone is claimed by this manuscript. Review verdicts and separate publication evidence must be read before changing its status.
