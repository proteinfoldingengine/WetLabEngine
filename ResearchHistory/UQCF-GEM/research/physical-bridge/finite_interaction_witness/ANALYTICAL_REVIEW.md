# Independent analytical review of the finite interaction witness

Date: 2026-10-12. Reviewer: separate Codex analytical reviewer.

**Decision: ACCEPT as an analytical clarification of an inherited conditional mechanism.** No substantive mathematical or scope defect was found in the reviewed assessment or index addition. This is not numbered-stage certification, historical execution recertification, a new theorem milestone, a publication audit, or approval to adopt a physical law.

## Exact material reviewed

The declared repository is `proteinfoldingengine/WetLabEngine`, branch `research/uqcf-overlapping-guard-exchange`, at parent `0948e728d9542d601f166ebbd9bc169f14417af5`. The reviewer received the fetched source packet rather than independently querying the remote repository.

| Local reviewed file | SHA-256 |
|---|---|
| ASSESSMENT.md | `14523b46321df5e380c4a286f8836756546629264d174b074c9f2d7180daa169` |
| INDEX_APPEND.md | `e4758a624190ea4aecfa2537264e0562cedae5b2228a4bf08d87e3960312fa8a` |
| SOURCE_READBACKS.json | `e4857bd048544e8a8fd2e77661d2f0e09ef78649f8928f2909d955b57521e14e` |
| source_packet.json | `3fb1fe7279252a7494078d6dd594550a8f04e125fd842fe7fdd9be24173fbb2a` |

All thirteen packet source contents were mechanically checked against the manifest's byte lengths, SHA-256 hashes, and recomputed Git blob SHA-1 identifiers; all matched. Both packet and manifest name the parent above. This establishes internal byte identity of the supplied evidence, not independent proof of remote tree membership or historical run validity. No scientific code, test suite, numerical matrix calculation, simulation, historical workflow, or campaign was executed. The mathematics below was independently reconstructed analytically. Mechanical work consisted of reading, hashing, and writing this review.

## Independent mathematical reconstruction

Use the assessment's tensor order A,B,C and standard Pauli convention XY=iZ, YX=-iZ. Write H=X⊗Y⊗Z, P=X⊗X⊗I, Q=I⊗Z⊗Z.

1. **Signs and normalization.** PH=I⊗(XY)⊗Z=iQ, HP=I⊗(YX)⊗Z=-iQ, and PHP=-H. H is Hermitian, H²=I₈ and Tr H=0. Its +1 and -1 eigenspaces each have dimension four. Consequently (I₈±εH)/8 has trace one and eigenvalues (1±ε)/8, each fourfold. For 0<ε<1 both preparations are strictly positive.

2. **Initial proper marginals.** Every factor of H is traceless. Tracing out any nonempty subset therefore annihilates its contribution. An m-site proper marginal is I_(2^m)/2^m for both preparations. Thus equality applies to every proper marginal, not merely the displayed BC output.

3. **Exact finite action.** Set c=cos(s/2), t=sin(s/2). Then

       (cI-itP)H(cI+itP)
       = c²H + ict(HP-PH) + t²PHP
       = (c²-t²)H + 2ctQ
       = cos(s)H + sin(s)Q.

   This verifies both the finite result and the positive sign of the Q term. P²=I makes U(s) exactly unitary. The transformed operator remains a Hermitian involution by conjugation, so positivity, trace and full-state eigenvalues are preserved for every real s. No small-s approximation is used.

4. **Output reductions and locality.** Tr_A H=0 and Tr_A Q=2Z⊗Z, giving BC density (I₄±ε sin(s)Z⊗Z)/4. Tr_C annihilates both H and Q, so AB remains I₄/4. Tr_B annihilates both, so AC remains I₄/4. A further trace gives I₂/2 at every site. In particular an operation supported on AB has not changed C alone. BC changes only as a joint correlation. The qualification sin(s)≠0 is necessary and stated.

5. **Distinguishability.** Put a=ε sin(s). Since Tr[(Z⊗Z)²]=4, its expectation is ±a. The BC difference is a(Z⊗Z)/2. The four singular values are |a|/2, yielding half-trace-norm distance |a|=ε|sin(s)|. The original full-state difference is εH/4 and has trace distance ε; unitary conjugation preserves that distance. Thus the retained distance never exceeds the pre-existing global distance. The update redistributes distinguishability; it does not create a new global preparation distinction.

6. **Conditional parity law.** The parity-r projector on BC is Π_r=(I₄+rZ⊗Z)/2 with rank two. Taking its trace against the output density gives (1±ra)/2 exactly. Because |a|≤ε<1, both parity outcomes have positive probability. This is a valid conditional statistical distinction, not a deterministic single-event preparation decoder. Joint readout may be implemented by local Z outcomes and parity association, but supplying those operations and the associated record remains an additional interface premise. The assessment correctly makes it conditional.

7. **Controls.** At ε=0 the preparations coincide; at sin(s)=0 their retained pair marginals coincide. For a product V_A⊗V_B⊗V_C, each reduced pair transforms by its corresponding local product conjugation. Its initially maximally mixed state is fixed, proving the stated one-body-unitary control. The assessment does not generalize this into a no-go for all native couplings. The C-only null is also exact.

8. **Gauge scope.** Simultaneously conjugating states, source and measurement preserves probabilities. Holding the source/readout frames fixed makes the ± comparison operationally meaningful under the supplied interface. A passive simultaneous relabeling cannot count as another physical signal. None of this initializes a native reference or identifies qubits with native events. The assessment states these boundaries correctly.

9. **Singular polar boundary.** Since the one-site means vanish, the BC connected correlation matrix has only the ZZ entry ±a; its rank is one for a≠0 and zero for a=0. AB and AC correlation matrices are zero. This fixture never enters the positive-definite regular-polar domain used by the archived rotation-rank argument. A unique regular polar frame and its asserted invertible Sylvester map cannot be imported here. The assessment explicitly withholds those claims. Nonzero retained correlation is established; regular-polar rotational geometry is not.

10. **Source-derivative match.** For T_s(ρ)=U(s)ρU(s)†, X(ρ)=-i[P,ρ]/2 and D X_ρ[h]=-i[P,h]/2. At h=H/8, [P,H]=2iQ gives D X_ρ[h]=Q/8 and Tr_A D X_ρ[h]=(Z⊗Z)/4. These are exactly the s=0 derivatives of the full and BC hidden-tangent expressions. For the preparations themselves the derivatives carry the stated additional ±ε factor. There is no missing factor of two or sign mismatch. Matching R_e D X_ρ[h] does not extend the downstream regular-polar assertions through a singular point.

## Match to the inherited sources

The supplied v15.73 derivation explicitly uses U_s=cos(s/2)I-i sin(s/2)P, weight-two/weight-three Pauli support cancellation, null response on the source-support pair and disjoint singleton, and one-body null controls. The present fixture is a concrete member of that inherited support mechanism. The archived results themselves identify standard quantum correlation redistribution and say that the interaction is specified rather than derived from Genesis/recoverability. The assessment's positive interpretation matches those statements without recertifying the archived numerical ranks or execution receipts.

The source-derivative classification supplies the retained map R_e D X_ρ[h] and separates retained leakage from geometric observability. Its polar factorization explicitly assumes a regular stratum. The assessment uses the former and declines the latter for this fixture, as required.

The v15.81 supplied derivation states R T_λ(u)h=e^(-u)sinh(λu) R C(h). Its components, component basis, λ and nonnegative ordered strength are supplied. The assessment accurately identifies that coefficient as a second conditional finite mechanism, not as a selected native law or a new result of this review.

The v15.07 report supplies the canonical neutral reference, relative-density operator and centered logarithm on a supplied quantum carrier. The v15.08 report separates that positive operator result from physical source identification, and v15.09 separates it from tensor-factor/carrier and cross-domain identification. The assessment preserves those distinctions. v15.39 explicitly adds source and response axioms; the v15.46 research decision and static trace leave native joint-state provenance unestablished. Neither is silently promoted into a missing native premise.

The C3 quantum screen is expressly source-scoped and is not a universal no-go. The physical-frontier decision explicitly permits a substantive native interaction with a probabilistic retained output, without requiring a unique outcome or complete C3 resolution first. The assessment preserves both facts. It does not infer impossibility from a missing C3 record protocol.

The broad statement about earlier prefix-tree source/response comparisons is contextual history, not newly established by this finite witness. This review's positive reconstruction concerns the supplied quantum sources and the precise mathematical example; it does not certify that broader historical body.

## Research and governance findings

The note genuinely preserves a positive interaction result: an explicit, state-independent two-body operation changes which retained correlations encode a pre-existing full-state distinction. This is stronger than merely defining a decoder after the desired answer is supplied. It remains conditional on the quantum carrier, factorization, frames, preparation, source/action and retained readout interface.

The parameter s is used only as dimensionless operation strength. No physical clock, energy, geometry, force, dark matter, empirical gravity fit or GR dynamics is deduced. The construction adopts no native axiom, reopens no closed Path B route, and does not claim a novel quantum theorem. The discussion of an explicitly acknowledged additional physical assumption is a boundary on a different possible reentry, not adoption of one in this note; under the current no-new-axiom program it is not an authorized next move.

The next native obligation remains a derivation from already justified relational inputs of an action and accessible retained distinction. A probabilistic law can satisfy a suitably scoped constructive claim. Full C3 still needs its own incidence/reference/update/record connection and any separately required error/progress contract. These obligations are neither erased nor inflated into a global requirement that must precede every interaction result.

The supplied AGENTS.md governs numbered retained-research stages and their full closure chain. This note expressly undertakes no numbered stage, new scientific execution or closure claim. Therefore this review does not imply that prospective preregistration, independent production/verification, complete foundational execution, external review, publication or post-merge gates have occurred. If later work claims such a stage, its required gates remain outstanding. The exposed fixture cannot later become an unseen holdout.

INDEX_APPEND.md accurately summarizes the reviewed assessment, including the single-site null, conditional nature, rank-deficient limitation and open native/C3/gravity boundaries. No requested correction is necessary for the analytical acceptance above. The author assessment was not edited and nothing was published by this reviewer.
