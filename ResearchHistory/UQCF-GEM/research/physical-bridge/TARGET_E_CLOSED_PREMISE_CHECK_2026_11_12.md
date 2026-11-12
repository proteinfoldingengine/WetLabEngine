# Target E: pointwise delivery, a uniform margin, and closed-premise minimality

Date: 2026-11-12 America/Phoenix. Author: GPT Work.
Research snapshot: `266f9dec2388f2550004ecbd606ca7e550be47da`; thread through T-425.
Authority for scope: the 04:34 MST Engineering ruling recorded in ACTIVE_RESEARCH_QUESTION.md at `42c95e3354eb77cc79046a24e5bd311d2f8bb844` releases a formal minimal-premise analysis of the actual W_R/W_E benchmark and closes Q155–Q184.

Status: **AUTHOR ANALYTICAL CHECK; unreviewed; no native premise earned.** This is a bounded mathematical check for the released Target E, not an admitted native producing operation, a numbered certification stage, or an adopted physical postulate. No scientific program was executed.

## 1. Deduplication and the exact question

The unrestricted realization-predicate version of Target E is already answered by [receiver_delivery_boundary/RESULT.md](receiver_delivery_boundary/RESULT.md), RD-6 (Git blob `a04f23b6f667cf61c32149b1f3bb6e0316e60377`). For the stipulated proper complementary receiver R, let

    d_R(W) = D(tau_u, tau_0)/5,
    tau_j = Tr_E |e_j><e_j|,
    B_R = {W : d_R(W)=0}.

Here D is trace distance and W ranges over the fixed benchmark isometries implementing C. A predicate forces pointwise delivery exactly when it excludes B_R. Calling that predicate the weakest delivery premise restates the target. The exact contrast formula also appears in [p1_receiver_location_resolution/RESULT.md](p1_receiver_location_resolution/RESULT.md), section 5 (blob `4182ba347f8c11bad63315ffa6395c496ddfa498`).

T-416 and the owner-action directive distinguish this proper-R problem from the retained-source p-effect. T-417 adds no operation removing that distinction. The owner-supported finite-effect/common-kernel result is a different, already analyzed premise class; it is not repeated here.

The additional question here is narrowly defined: if one restricts the premise language to **closed sets of admissible benchmark realizations**, does a weakest sufficient premise emerge? “Closed” refers to ordinary finite-dimensional matrix topology in this supplied Hilbert benchmark. It is a SUPPLIED analytical restriction on premise language, not an inferred native topology, continuity law, or physical robustness principle.

## 2. Exact control: positive in every realization does not imply a positive uniform margin

Use the existing carrier X=(o,p,u,v), retained Y=(o,p,v), pair z+=(1,1,2,1)/5 and z-=(1,1,1,2)/5, and complement K=E tensor R with basis |e r>. Fix e_0=|00>. For 0<t<=1 set

    e_u(t) = [(1-t^2)|10> + 2t|01>] / (1+t^2),
    W_t|j> = |j>|00>  for j in Y,
    W_t|u> = |p>|e_u(t)>.

Normalization follows from (1-t^2)^2+4t^2=(1+t^2)^2, and e_u(t) is orthogonal to e_0. Thus RD-0 applies: every W_t is an isometry implementing exactly the same reduced source channel C. No source pair, owner designation, factorization, or interface changes with t. W_1 is W_R, and the limit at t=0 is W_E.

Taking the E marginal gives

    tau_0 = |0><0|,
    tau_u(t) = [(1-t^2)^2 |0><0| + 4t^2 |1><1|]/(1+t^2)^2.

Consequently,

    d_R(W_t) = 4t^2 / [5(1+t^2)^2] > 0.

One fixed effect F=I_S tensor I_E tensor |1><1| attains this signed contrast for every t>0. Its pre-event expectation is zero in both preparations. This is therefore not an artifact of optimizing a different measurement for each realization.

Yet inf_{0<t<=1} d_R(W_t)=0. An entirely rational sequence suffices: at t=1/n,

    d_R(W_(1/n)) = 4n^2 / [5(n^2+1)^2] <= 4/(5n^2) -> 0.

The set {W_t:0<t<=1} excludes EVERY R-blind realization, including W_E, but has no positive uniform delivery margin. This does not contradict RD-6: pointwise nonzero delivery is precisely its predicate-language result. A claimed uniform positive margin needs an additional condition. No detectable-size threshold is imposed on Aaron's one-effect target by this observation.

## 3. Closed sufficient classes have a margin, but no weakest such class exists

Let Wcal be the full benchmark implementation class and G=Wcal minus B_R. Wcal is compact: RD-0 identifies it with the continuous image of the compact unitary group U(K), equivalently the finite-dimensional orthonormal-pair space. The function d_R is continuous.

If S is a nonempty closed subset of Wcal and S is contained in G, compactness gives

    min_{W in S} d_R(W) > 0.

This is a conditional consequence of CLOSEDNESS plus pointwise delivery. The open family in section 2 explains why closedness cannot simply be omitted.

Now declare the premise class precisely:

    C_closed = {S closed in Wcal : W_R belongs to S and S intersect B_R is empty}.

This class is nonempty: S={W_R} belongs to it and has contrast 1/5. A larger admitted set is a weaker premise. There is no inclusion-maximal member of C_closed, and hence no weakest sufficient premise in this language.

Proof: G is not closed, because W_t belongs to G for t>0 but converges to W_E in B_R. Therefore a closed S contained in G cannot equal G. Choose W' in G minus S. Then S union {W'} is closed, still contains W_R, still avoids B_R, and strictly enlarges S. It is a strictly weaker sufficient premise in the same declared language. This works for every S in C_closed.

The result does not exclude a weakest condition inside a smaller, independently specified structural language. Nor does it say every useful physical premise is closed. It says that “all predicates” and “all closed predicates” do not by themselves select a noncircular weakest physical law: the first has the target-equivalent answer G (RD-6), while the second has no weakest answer.

## 4. Consequence for the released task

Before executing another Target E block, fix the permitted premise language and the conclusion quantifiers:

- Pointwise: every admitted realization has a nonzero contrast.
- Uniform: one positive lower bound works for the entire admitted class.
- Fixed effect or realization-dependent effect: specify which; section 2 already uses one fixed effect.

Do not label the RD-6 exclusion condition a new postulate derivation, and do not promote pointwise exclusion to a uniform margin. If a new structural class is selected, state its independently meaningful state/action/access clauses before examining which models they exclude. Derive necessity/sufficiency only within that class. A class engineered by defining “allowed” to mean “delivers” earns nothing.

This check does not authorize resuming the closed guard/section classification, a new source census, or the parked v16.54 work. It adds no native event-to-owner operation.

The retained-source p-effect remains a separate accepted conditional target: its contrast is 1/5 for EVERY W in Wcal, including this entire family and W_E. No proper-complement selection premise is necessary for that mathematical consequence. Its native event correspondence and operational ownership/access remain unresolved.

## 5. Premise and verification ledger

- Existing benchmark input: C, the diagonal pair, E tensor R factorization, blank R, and the proper-R interface are SUPPLIED benchmark data.
- Existing mathematical infrastructure used: RD-0 and RD-6; no new source interpretation.
- Additional analytical restriction: closed admitted realization sets, expressly SUPPLIED.
- Derived in this note: the exact rational counterfamily and the closed-class minimality consequence, by the displayed algebra and compactness argument.
- Native premises moved from SUPPLIED to DERIVED: none.
- Available physical receiver effect forced by native structure: none.
- Scientific importance: a bounded guard against a duplicate or ill-posed minimal-premise claim; not delivery discovery.
- Verification: source comparison and author hand proof only. No finite campaign, numerical experiment, Gemini request, independent acceptance, merge, or claim-status change. Independent challenge remains welcome.
- Novelty: the contrast formula and unrestricted blind-set criterion are credited to the existing results. The additional statements are elementary consequences in the explicit premise language, with no literature-wide or repository-wide novelty claim.

Native bridge NOT_DERIVED. Physical result not claimed. scientific_breakthrough=false.

## 6. Peer check and fixed-effect control — 2026-11-12

Dot independently checked the displayed isometries, all input matrix-unit cases for C, the receiver marginal, and the closed-set argument in [PR111 comment 6823073688](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6823073688). This is peer analytical checking, not a Gemini verdict or scientific certification. Dot requested no repair and supplied the following additional control, which I checked algebraically.

Define S_rot = {(I_S tensor I_E tensor U_R) W_R : U_R in U(2)}. This compact closed class contains W_R and has d_R=1/5 everywhere, since its two proper-R marker states are orthogonal. It therefore belongs to the section 3 premise class.

Nevertheless, no ONE FIXED binary effect F_R distinguishes every member. Let a,b be an orthonormal eigenbasis of F_R. Choose U_R|0>=(a+b)/sqrt(2) and U_R|1>=(a-b)/sqrt(2). Both expectations of F_R equal Tr(F_R)/2, so its contrast is zero for that member. Scalar effects are covered as well. This is a permitted change of the joint implementation; the source preparation and initial blank receiver remain fixed.

This control separates a uniform trace-distance guarantee (for each realization an effect exists) from a common fixed-effect guarantee. Section 3 asserts only the former. Section 2's t-family does have the explicitly displayed common effect, and is unaffected. The control is limited to one binary effect: it does not exclude a fixed informationally complete measurement with multiple outcomes or an available effect family. It also does not impose a generic reference-frame requirement.

The retained-source p-effect remains 1/5 throughout S_rot. Its ownership/access question is unchanged. Dot's exact response is frozen with the review inputs; a fresh whole-argument review will assess this note including this addendum, with no prior peer verdict treated as authority.
