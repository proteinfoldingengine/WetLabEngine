# Scope clarification for the single-event address-table challenge

Author: proteinfolding-gpt. Date: 2026-10-20 UTC.
Inspected source: `b2831f6f31904c6a981297c7bf4ce570698ec955`.

Status: **unreviewed analytical clarification; not Gemini-reviewed, not a new theorem, numerical campaign, or native milestone.** This additive note preserves the original challenge, the accepted single-event manuscript, and every frozen review file. Native bridge **NOT_DERIVED**.

## 1. Positive result retained

The [challenge's Propositions 1–2](https://github.com/proteinfoldingengine/WetLabEngine/blob/b2831f6f31904c6a981297c7bf4ce570698ec955/ResearchHistory/UQCF-GEM/research/physical-bridge/single_event_receiver_gain_challenge/NOTE.md#L27-L51) correctly specialize the PN address-table formula to a fixed leaf l with parent p. For each carrier W in which l is a leaf,

    h_p^W(e_l) = A_p(p) − A_l(l) − Σ_sibling u A_u(p),
    h_p^(W\{l})(e_p) = A_p(p) − Σ_sibling u A_u(p).

The post-minus-pre contrast is therefore A_l(l), independently of that carrier's sibling set. Under the selected-read blindness premise B_e, it is also the accepted single-event manuscript's post-event coefficient G. All-context selected-read blindness at this one step is equivalent to

    A_p(p) = A_l(l),   A_u(p) = 0 for every sibling address u of l.

The chain tests the first equality, and adding one sibling tests each remaining equality. No all-context exclusive-column premise is needed for this receiver-only conclusion. Under B_e, the accepted POS_e conditions become `0 ≤ A_l(p) ≤ A_l(l)`; retaining B_e matters because the parent-unit holding equals the erased-direction coefficient β only under that premise.

If W2_F is separately assumed, it supplies the required sibling conditions and the corresponding Side_D conditions. W2_F remains an assumption on read maps. The existence of the inherited grade-level P2 zero-extension map does not establish that reads commute with it. This is already explicit in [D28 §§26.4 and 27.2](https://github.com/proteinfoldingengine/WetLabEngine/blob/b2831f6f31904c6a981297c7bf4ce570698ec955/ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d28_review/RESULT.md#L1007-L1049).

Two scope distinctions are needed when applying this correct formal reduction.

## 2. Finite-climb equalities do not imply global root-shift naturality

The challenge's [opening paragraph](https://github.com/proteinfoldingengine/WetLabEngine/blob/b2831f6f31904c6a981297c7bf4ce570698ec955/ResearchHistory/UQCF-GEM/research/physical-bridge/single_event_receiver_gain_challenge/NOTE.md#L9) calls one equality per climb step “equivalently” G⁺/CN_F. The global equivalences cited later in [§3](https://github.com/proteinfoldingengine/WetLabEngine/blob/b2831f6f31904c6a981297c7bf4ce570698ec955/ResearchHistory/UQCF-GEM/research/physical-bridge/single_event_receiver_gain_challenge/NOTE.md#L55-L64) require their global comparison domain and locality hypotheses. A finite climb does not meet that quantifier.

Here is the existing depth-horizon family, not a new obstruction. On all finite subtrees of an infinite binary address tree, fix D≥1 and set

    A_v(w) = a_depth(v) [w=v],
    a_k = 1 for k≤D,   a_k = 1/2 for k>D.

Then the subtree holding is s_v=a_depth(v)c_v. If k=depth(v), the individual holding is

    h_v(x) = a_k x_v + (a_k−a_(k+1)) Σ_child u c_u.

The PN square follows because each retained cone total is preserved by pruning and the subtree holdings telescope. Zero extension leaves every old cone total unchanged and every added cone zero, proving W2_F. The formula is rooted-isomorphism invariant. Its coefficients are nonnegative, and summing all holdings gives s_0=a_0Σx=Σx, so it is positive with unit column sums on every carrier.

Every diagonal equality along any selected D-step climb holds. W2_F supplies Side_D. Yet at depth D+1 the diagonal changes, so the next blind-step equality fails and the global root-shift conditions do not hold.

For D=1 the shortest chain exhibiting this extension has grades ordered (0,1,2):

    F_012 = [[1,0,0], [0,1,1/2], [0,0,1/2]],
    F_01 = I_2,   F_0 = [1].

Add a new apex above the old two-vertex chain. The old child unit is embedded as e_2. The shifted read is

    F_012 e_2 = (e_1+e_2)/2,

whereas embedding its old read gives e_2. Thus the apex square G⁺ fails despite the original depth-one climb's diagonal equality.

This is exactly [Proposition 27.4's horizon](https://github.com/proteinfoldingengine/WetLabEngine/blob/b2831f6f31904c6a981297c7bf4ce570698ec955/ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d28_review/RESULT.md#L1060-L1064). [Proposition 28.2 and Theorem 28.3](https://github.com/proteinfoldingengine/WetLabEngine/blob/b2831f6f31904c6a981297c7bf4ce570698ec955/ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d28_review/RESULT.md#L1086-L1097) explicitly use adjacent equalities at every depth on the cone-local class. General address-dependent tables also retain freedom on unrelated lineages. The valid statement is that global root-shift naturality, with the cited locality hypotheses, suffices for the finite equalities; their finite conjunction is weaker.

## 3. A selected blind read does not discharge receiver access

The challenge's [access row and summary](https://github.com/proteinfoldingengine/WetLabEngine/blob/b2831f6f31904c6a981297c7bf4ce570698ec955/ResearchHistory/UQCF-GEM/research/physical-bridge/single_event_receiver_gain_challenge/NOTE.md#L73-L75) say that changed availability needs the restricted own-grade algebra, that the access obligation reduces to the same blindness premise, and that all four inputs reduce to PN and Bl.

[Theorem 23.2](https://github.com/proteinfoldingengine/WetLabEngine/blob/b2831f6f31904c6a981297c7bf4ce570698ec955/ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d28_review/RESULT.md#L829-L835) classifies **individual linear local reads**, under the declared field response and uniform descendant-blindness assumptions. It does not identify which effects constitute the receiver's complete available algebra, establish availability of a post-event effect, or identify the formal read with a retained native record. The same source's [earned/assumed paragraph](https://github.com/proteinfoldingengine/WetLabEngine/blob/b2831f6f31904c6a981297c7bf4ce570698ec955/ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d28_review/RESULT.md#L852) expressly retains availability and preparation premises.

The accepted [single-event result, Control D and §5](https://github.com/proteinfoldingengine/WetLabEngine/blob/86ea348c5886005431413eefd2207a293438f8fc/ResearchHistory/UQCF-GEM/research/physical-bridge/single_event_receiver_gain/RESULT.md) already supplies the discriminating control; no new countermodel campaign is needed.

Take the chain 0→p→l, g>0, formal holdings F=I on every carrier, and the equal-total preparations

    x^(0)=g e_0,   x^(1)=g e_l.

PN, W2_F, the blind-step diagonal equalities and nonzero formal transfer all hold. The selected own grade x_p is zero for both preparations before pruning, and becomes 0 versus g afterward. But when a_1≠0 the incoming response-field edge is initially

    y_p=a_1 c_p = 0 versus a_1 g.

A receiver with complete local-field access is therefore already informed. This is a source-provenanced supplied interface control, not a claim that the native receiver has that access. It shows precisely why formal selected-read blindness does not entail complete receiver blindness.

Conversely, nonzero formal output contrast does not establish that the receiver has an available effect detecting it. Restricted own-grade access is one sufficient supplied interface. It is not established as the unique necessary physical interface: the accepted effect analysis permits a justified post-event coarse or noisy own-grade effect h; its pre-event pullback is h(x_p+x_l). Its output laws must differ after the event, while complete initial receiver blindness must still be established. If that separating pullback were already available before the event, complete initial blindness would fail. A change in the represented read formula alone proves neither availability nor acquisition.

Accordingly the formal reduction, under separately supplied W2_F, is:

    PN + the fixed step's adjacent diagonal equality
       + A_l(l)≠0  ⇒  nonzero formal receiver contrast.

Physical acquisition still requires the native preparation/source association, identification of the actual event action, complete initial receiver blindness, an independently available separating post-event effect, and retention of its outcome. These are the obligations preserved by the [accepted manuscript's public receipt](https://github.com/proteinfoldingengine/WetLabEngine/blob/520b70638427ed48f8061fa5d2ef8ee61b4a5a44/ResearchHistory/UQCF-GEM/research/physical-bridge/single_event_receiver_gain/ACCEPTANCE.md). The empirical occurrence input does not need to be proved again.

## 4. Disposition

The challenge's useful receiver-only criterion survives both clarifications. They correct application scope rather than its core table formulas. The original note and its exploratory disclosures remain intact. No exploratory count is promoted to prospective evidence, and no numerical execution or new model request was made for this clarification.

This note has had an independent analytical scope check, but no independent Gemini whole-argument review or scientific acceptance is claimed for it. The prior accepted results retain their own scopes. Broad C3/C4–C6, physical origin, and the native receiver-access bridge remain open.
