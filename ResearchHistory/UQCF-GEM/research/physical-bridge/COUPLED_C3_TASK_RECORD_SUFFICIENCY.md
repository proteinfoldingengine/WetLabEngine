# C3 task-specific record sufficiency

Date: 2026-10-11. Source parent: c0084919eba5683c99d9be2bfb04b061f1c287ee.
Status: explanatory analytical note; standard factorization arguments, no novelty or new numbered campaign claimed. Native record production/access and broad C3/C4-C6 remain OPEN.

## Purpose and assumptions

The prior full-source condition ker(P) intersect ker(B)={0} is stronger than deciding one admission predicate. This note states the weaker requirement and checks it against the existing C3 two-sided readout. It does not construct a channel, prescribe a hidden-state-dependent outcome, or assume every legal request commits.

Let X be the explicitly declared source domain and f:X->Y the task answer. Fix a protocol and an accessible record interface independently of the answers. For each source x let O(x) be the set of records possible at the specified decision point under that protocol, including every permitted resolution. A record includes only justified accessible data; an analyst's state, pruning output, or hidden outcome is not automatically accessible. For adaptive protocols it must contain the available history needed by the decoder, rather than only a final snapshot if the decoder uses history.

## Exact task decoding

A decoder d on the union of possible records, correct for every source and every permitted record, exists exactly when

    f(x) != f(x') implies O(x) intersect O(x') is empty.

Necessity: a shared record would require d to give two different answers. Sufficiency: assign a record the common answer of the sources capable of producing it; disjointness makes that answer unique. Values outside the union are irrelevant. Empty O(x) gives no completion claim. Universal finite completion must be established separately, including executions which never reach a decision point.

For a deterministic available record o(x), this reduces to constancy of f on every fiber of o, equivalently f=d composed with o on X. The coarsest abstract partition sufficient for this single answer is the partition into f-fibers. Defining that quotient does not derive a native process which produces its class identifier.

## Sound partial decoding

Allow an undecided output ?. A record r can soundly produce y precisely when all sources compatible with r have answer y. Records compatible with different answers must remain undecided. This is the maximal sound decision rule at the level of abstract available records, not a claim that a native observer can enumerate its compatibility class.

The source domain and target are load-bearing. An initial-state certificate need not decide a later current-state predicate after an unreported update. Known source promises can refine compatibility classes, but cannot be inserted solely to eliminate a counterexample.

## Application to the existing C3 readout

In COUPLED_C3_CORE_READOUT_RESULT.md, distinguish the root4 bridge switch beta from the core label b. The source predicate is f(x,y)=xy. The existing admissibility inequalities are d1<=x, d2<=y, beta<=1-xy. Therefore visible d1=d2=1 soundly certifies f=1, while visible beta=1 soundly certifies f=0. The baseline d1=d2=beta=0 is compatible with both answers. Existing accessible core histories permit the conditional protocol to keep these certificates after exact core restoration; the final restored core snapshot alone would lose that distinction.

This is precisely sound partial decoding, already proved in the inherited checkpoint. Its possible nontermination is not a defect in certificate soundness. The inherited all-NOOP history prevents a guaranteed finite total decision, but is not a new obstruction discovered by this note. Most importantly, the predicates and inequalities do not manufacture accessible core snapshots or physical enforcement.

## Linear specialization: memory needed for a task, not the full source

For the explicitly conditional finite-dimensional vector-space diagnostic, let P:V->W be the pruning map, T:V->Y a linear task, and B:V->R a linear record. Assume BOTH Px and Bx are available. Then a linear decoder of Tx from (Px,Bx) exists exactly when

    ker(P) intersect ker(B) is contained in ker(T).

Proof: the kernel of the joint map x->(Px,Bx) must lie in ker(T). If it does, define the decoder on the image of the joint map by (Px,Bx)->Tx; this is well defined and linear, and can be extended to the whole finite-dimensional output space. This proof concerns the full declared vector space; a restricted physically realizable domain can have a weaker requirement.

For K=ker(P), the least possible record dimension over unrestricted linear B is rank(T restricted to K). Indeed ker(B restricted to K) subset ker(T restricted to K), so rank(B restricted to K)>=rank(T restricted to K). Conversely, if the existing retained inclusion I obeys PI=id, take the record codomain T(K) and

    Bx=T(x-IPx).

Then Tx=T(IPx)+Bx, giving the matching dimension. Without a supplied section one can choose a linear complement mathematically, but that would not establish a canonical or native record. Even when I is supplied, the displayed B is only an algebraic sufficient statistic: no device, interaction, accessibility or actual recording law has been derived. With T=id this reduces to the full-recovery dimension dim ker(P). The nonlinear Boolean C3 predicate is governed by the fiber criterion above, not this rank formula.

## Decision and scientific status

Use task-specific distinguishability when evaluating a concrete native candidate, rather than demanding full-state reconstruction unnecessarily. Retain sound conditional certificates even if guaranteed completion is unavailable. Require the candidate's record to come from an independently justified interaction and access interface; do not define it to equal f or Bx and call that a derivation.

No new source-to-record interaction has been found here. No scientific tests, Gemini request, numerical campaign, or closure claim is added. This note makes the existing response gate more precise and preserves the current positive and negative results.

## Immutable sources

All links use source parent c0084919eba5683c99d9be2bfb04b061f1c287ee. Historical candidate headers do not supersede later closeouts.

- [Retained-source decomposition, P2](https://github.com/proteinfoldingengine/WetLabEngine/blob/c0084919eba5683c99d9be2bfb04b061f1c287ee/ResearchHistory/UQCF-GEM/foundational-closure-verification/PROOFS.md): existing section I and decomposition x=IPx+(x-IPx).
- [Core readout](https://github.com/proteinfoldingengine/WetLabEngine/blob/c0084919eba5683c99d9be2bfb04b061f1c287ee/ResearchHistory/UQCF-GEM/research/physical-bridge/COUPLED_C3_CORE_READOUT_RESULT.md): complementary visible certificates, retained-history restoration and possible stalling.
- [Internal-record attempt](https://github.com/proteinfoldingengine/WetLabEngine/blob/c0084919eba5683c99d9be2bfb04b061f1c287ee/ResearchHistory/UQCF-GEM/research/physical-bridge/COUPLED_C3_INTERNAL_RECORD_ATTEMPT.md): why deterministic copying is not derived by committing every legal request.
- [Target-blind response gate](https://github.com/proteinfoldingengine/WetLabEngine/blob/c0084919eba5683c99d9be2bfb04b061f1c287ee/ResearchHistory/UQCF-GEM/research/physical-bridge/COUPLED_C3_TARGET_BLIND_RESPONSE_GATE.md): input, carrier, action, accessible output, discrimination and completion obligations.
