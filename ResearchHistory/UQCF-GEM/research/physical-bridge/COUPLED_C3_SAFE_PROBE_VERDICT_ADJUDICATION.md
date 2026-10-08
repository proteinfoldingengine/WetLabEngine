# C3 safe-probe review adjudication — unsupported REVISE label

Date: 2026-10-08.
Status: AUTHOR-SIDE ADVERSARIAL ADJUDICATION; NOT SCIENTIFIC CLOSEOUT.

Evidence: GitHub Actions run 37849493460; bounded-controls PASS; Gemini review job PASS as execution; evidence audit REVIEW_RECORDED with Gemini verdict REVISE, 8 findings, 0 missing assumptions, 0 counterexamples. Research input commit 77ac20020170607596262980c61aed8240adda7e, workflow commit 16ef7254f7437b55d0532e3a6d81aec60d8221d9. Gemini response SHA256 c41d7d33169215693dcdc2aec8bdcd74a5ef015ccc2991e5e2a96607a1964ccf.

## Whole-argument adjudication

The bounded theorem assumes finite spectator palette T, two initial worlds Z_A=empty and Z_B={u}, fixed prepared roots E(Z)=({a,b},{b,c},{a,c},{d,e} union Z), and the exact core-only retained channel O_core. The clarification explicitly freezes labelled residual R={r4}, so for every H subseteq {a,b,c,d,e}:
 M_core(H;Z) = 1[({d,e} union Z) intersect H = empty] = 1[{d,e} intersect H = empty].
The first three roots have hitting number 2, fourth root is disjoint and nonempty, so tau=3 for all Z; all floors2 hold.

A uniformly safe controller selects only labelled spectator toggles valid in every hidden world consistent with its observed transcript. Every selected edit commits exactly once, with no state-dependent feedback or hidden autonomous updates. If observed transcripts match at step n, the policy chooses the same edit in both worlds; it is valid in both; both receive identical constant success records; O_core is invariant. Induction proves identical transcripts at n+1. Equal signed changes preserve q_B-q_A=1. Therefore no transcript-only estimator can recover the initial bit b0 correctly for both worlds. A randomized policy with coupled randomness has identical output distributions, so it cannot have certainty in both worlds.

The review itself affirms these steps and finds no missing assumptions or counterexamples. Its limitations (restricted observation channel, strong uniform-safety and closed-world hypotheses, unspecified computational cost) are already explicit premises/boundaries, not logical objections within the frozen domain. A REVISE verdict with no actionable mathematical issue is not a certification failure, but neither does this author-side adjudication confer acceptance.

## Mandatory adversarial challenge

A fresh review must either:
(A) identify an exact false mathematical claim, an omitted hypothesis REQUIRED within the declared domain, or a concrete counterexample with full native states and edits, and explain why it defeats the theorem; or
(B) accept the theorem only within its stated scope while preserving all limitations.

No new geometry, fundamental time, observer access, force or physical mechanism is inferred. No automatic certification from finite tests or Gemini verdict.
