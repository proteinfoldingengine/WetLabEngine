# C3 core-probe follow-on — bounded refutation replay scope

Date: 2026-10-08.
Integrated parent: b883c526cd4f19c4a7dcd69fec9cf01ab6f94a5d.
Status: REVIEW PREPARATION ONLY. Not an independent mathematical review or a change to the theorem's frozen hypotheses.

## Exact source under examination

Scope 4e0cb8c68c807265fb48652b1f990a18d4a43a2c, blob 8891b150d4374a4f7fac6945fed2035f03648590.
Proof e7dc592d0f98121c7c232f33018a0a199c30ba8e, blob d619932c44d051f2a0c698365709d6f42e02f078.
Author audit 8ca82d010d21ccfe7c34d4507240e77e863b5c08, blob 1b2189c41a665a5bb91f97e44edd213aac0263a2.
Continuation index b883c526cd4f19c4a7dcd69fec9cf01ab6f94a5d, blob 399a3e762f030e8329b41823d1ca859392439241.

The target of review is the exact history-completion formula, not just a proposed probe: F(H)={Z subseteq T: |Z|>=D(H)} with D(H)=max_j max(0,2-|P4_j|). Proof sources and earlier acceptances remain unchanged.

## Work-unit limits

Keep the process repository-contained. Do not launch external-AI review or polling. Same-assistant checking and a separately specified executable oracle must not be represented as an independent reviewer verdict. No CLOSED/CERTIFIED status change or follow-on physical claim is authorized by this replay.

Re-run the earlier audit's published Python hand checks and preserve the fresh actual output. A new execution does not establish provenance of an earlier execution. Inspect the whole proof analytically, separately from bounded tests.

Add a small, deterministic replay covering the concrete probe carrier: roots 1-3 stay {a,b},{b,c},{a,c}; root 4 can receive attempted insertion/deletion of any of the five core labels; spectators are immutable, confined to root 4, and drawn from a one-label or two-label palette. All valid-command rejections remain possible. Initial core support is {d,e}. This is a strict slice of the full theorem, which allows edits to all four roots. No random sampling, broad numerical campaign, or inherited-stack certification is requested.

## Oracle and coverage requirements

Generate actual successor supports from commands; determine floors and the exact hitting number by directly enumerating full-palette hitting sets. Do not generate hidden completions from D. Propagate all explicit hidden subsets compatible with each observed outcome, including distinct subsets of the same cardinality. Explore the finite reachable belief-state graph to a fixed point, retaining the observed history deficit separately.

Compare the explicit completion SET against the theorem's predicted set at each reachable state and transition. A fixed-point graph can cover arbitrary history length inside this finite slice; it does not prove the all-root or arbitrary-palette theorem.

Record canonical state and command/outcome-edge sets so that deleting an otherwise valid state or outcome is rejected by fresh reconstruction. Test deliberately wrong estimators that credit a rejected attempt, forget the certificate on restoration, conflate spectator identities, or replace D by the Boolean D>0 when exact completion families are requested. Include a direct empty-core projection check.

## Analytical review obligations and publication gate

Check the nonempty-core replacement lemma, empty-core formula, necessity and constructive sufficiency of the complete history fiber, adaptive-command induction, rejection semantics, invariant-spectator requirement, exact restoration versus guaranteed progress, and the no-finite-two-sided-decision theorem. Report issues explicitly; do not silently repair an already published statement.

Publish source, actual deterministic output, exact provenance and the same-assistant review disposition. Update the continuation index additively. A separate independent mathematical acceptance and subsequent separate publication audit are still unfulfilled gates unless an actual new verdict is obtained. Immutable readback verifies publication, not scientific acceptance. Broader C3 and C4-C6 remain OPEN.
