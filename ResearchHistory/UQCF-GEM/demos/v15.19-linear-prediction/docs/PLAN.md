# v15.19 — Linear prediction module versus invariant algebra

Continue the frozen four-qubit simulator. The question is the smallest real
Hermitian linear operator space containing the entire original retained algebra
and invariant under the SAME six supplied finite motions (separately and jointly),
including inverse motions. Do not require multiplication closure and do not call
its orthogonal projection a physical quantum channel without a separate proof.

The seven families and sixteen masks are the same 112 cases as v15.18. No new
carrier, motion, source, retained-algebra selector, entropy, time or RCR is added.
The historical exchange-specific v12.48 GOSM result is distinct and not reopened.

1. Generic tests first, verify absent implementation RED.
2. Real Hermitian-coordinate block-Krylov closure with rank ambiguity stop.
   Fix numerical constants before measurements: null singular value <=1e-11,
   retained >=1e-8; any gap value stops. Closure tolerance 1e-9.
3. Independently count single-unitary cyclic dimensions by adjoint eigenphase
   sectors. Compare whole subspaces when feasible. No tuning from results.
4. All 112 cases, explicit all-input invariant-subspace residuals, direct versus
   coordinate-prediction trajectories and negative controls for incomplete seeds.
5. Distinguish linear closure from associative closure and a physical CPTP map;
   show an explicit non-CP linear-projection control. Keep inherited source bytes.
6. Render a numerical comparison, offline HTML and MP4 with playback distinct from
   physical time. Run new tests and available prior tests in separate processes.
7. GitHub publication is blocked on the v15.18 renderer/template upload; do not
   bypass the write block or claim a new branch, PR or CI run. Deliver local work.
