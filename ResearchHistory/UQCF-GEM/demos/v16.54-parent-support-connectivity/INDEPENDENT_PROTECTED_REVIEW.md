# Independent review — protected positive-slack exchange

Reviewer: /root/v1654_protected_review. Verdict: ACCEPT within the stated analytical scope.
Artifact: PROTECTED_EXCHANGE.md at 4825b8d5544ace5185b10ca9af7f856c1840c276.
SHA256 verified by reviewer: a76dffd9e6f9db7e590ebb89e62c4a195c27af826e84cc5c3a60005329279ee0.
Executor separately verified exact immutable GitHub file readback.

Critical: none. Important: none. Minor: none.

## Review reasoning

The unsafe-addition criterion is valid, including extension to exactly q-2 labels: any extension meeting the old root would contradict the existing lower guard.

Witness relocation preserves floors because a_j<=a_i. Old and new disjoint witnesses establish the lower bound during the respective contraction and expansion phases. One label from each witness supplies the upper bound.

Partition operations preserve floors and the transversal band: q-2 untouched parts remain disjoint from the affected pair, which needs one or two hitting labels. Size transfers strictly reduce size discrepancy; swaps strictly increase correctly placed labels without moving already correct labels; witness replacement also has a strictly increasing bounded progress measure.

Theorem K is necessary and sufficient in the inherited feasible carrier. Its negative conclusion excludes protected states everywhere in that carrier without asserting disconnection. The disjoint-triangle family has transversal 2m, slack 3m(m-1)>0 and smallest-floor sum 4m>3m. It establishes the stated method limitation and, through exactness, satisfies the earlier endpoint inequalities.

Only source/skill reading, hash verification and manual mathematics were performed. No numerical scripts, tests, enumeration, file/Git mutations or further delegation.

## Declined-to-judge items and executor rulings

- Implementation correctness: outside analytical scope. Ruling: unclaimed; risk is mistaking existence proof for validated code.
- Executed algorithm behavior: no execution performed. Ruling: requires later prospective protocol; no behavior claimed.
- Numerical/exhaustive certification: no campaign authorized. Ruling: not certified; risk is false closure.
- Efficiency bounds: not proved. Ruling: finite termination only.
- Universal positive-slack connectivity: remains open. Ruling: protected endpoints only; risk is unjustified universal extrapolation.
- Accessibility from unprotected endpoints when K holds: not proved. Ruling: explicitly open even though a protected class exists.
- Root disconnection or native barriers: not established. Ruling: triangle family obstructs only this method; native barrier would need additional exclusions.
- Independent certification of inherited child interface/native lifting: prior documents are contextual references, not newly certified. Ruling: retain conditional hypotheses; no re-certification.
- Physical interpretation: outside scope. Ruling: none claimed.
- Git/PR provenance beyond the supplied hash: not reviewed. Ruling: executor checks exact file readback and Git ancestry/change scope separately.
- Merge readiness: outside analytical review. Ruling: keep draft; implementation and complete certification chain remain pending.
