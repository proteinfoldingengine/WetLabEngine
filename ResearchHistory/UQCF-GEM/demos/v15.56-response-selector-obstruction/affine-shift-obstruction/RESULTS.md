# v15.85 — affine-shift obstruction

The frozen gate returned **AFFINE_SHIFT_RESCUE_OBSTRUCTED** and **NONUNITAL_RECOVERY_OBSTRUCTION_CONFIRMED**, with `all_valid: true`. Three tests passed. No criterion, amplitude, or inherited scientific verdict was changed.

## Earned statement

For a qubit trace-preserving affine map with fixed real linear Bloch part T, complete positivity at any translation t implies complete positivity at zero translation. The exact identity

    J(T,-t) = (Y tensor Y) J(T,t)^T (Y tensor Y)^dagger

uses the full transpose. It preserves positivity; averaging the opposite translations gives J(T,0). The converse existence claim follows by choosing t=0. All 13 coefficient identities and unitarity were verified exactly with SymPy. This proves the all-translations statement; a finite shift search or a small numerical witness coefficient would not prove it.

Consequently, no affine translation rescues the fixed full linear maps L, L^2, or L^3 from v15.84. Their negative Choi witness expectations are respectively -0.5, -0.242709988126002647, and -0.025144043889588823. Both witness marginals agree with I/2 within 7.38e-81; translation coefficients have magnitude at most 6.91e-81. These numerical witnesses corroborate the exact theorem.

## Fourth-power controls and recovery

For T=L^4, shifts along its left null singular axis have the analytic admissibility interval |tau| <= 0.73389395662773758648. This is a one-dimensional section, not a classification of the full translation region.

| Frozen tau | Classification | Minimum unnormalized Choi eigenvalue |
|---|---|---|
| -1 | NON_CP | -0.104441821109626 |
| -0.5 | CPTP | 0.078277442971898 |
| 0 | CPTP | 0.160367971024049 |
| 0.5 | CPTP | 0.078277442971898 |
| 1 | NON_CP | -0.104441821109626 |

For each admissible row, the three antipodal right-singular-axis input pairs have input trace distance 1 and output distances 0.370763470600710436, 0.308500587351191228, and zero (numerically below 9e-82). The optimal equal-prior mean pure-target overlap fidelities are 0.685381735300355218, 0.654250293675595614, and 0.5. A separate binary measure-and-prepare recovery attains each pair's bound. This does not assert one recovery is simultaneously optimal for an arbitrary ensemble.

A common translation cancels from every state difference. Thus the distinguishability and per-pair recovery obstruction extend analytically to every admissible translation with this fixed T. Nonunitality does not restore the lost distinguishability.

Amplitude-damping Kraus and complex Pauli-Y replacement controls passed. Maximum affine identity error was 1.06e-81; maximum null-axis spectrum-formula error was 6.33e-81. The smallest tested state eigenvalue was -1.06e-81, within the frozen numerical tolerance, not a scientific positivity failure. Parent reconstruction error was 4.22e-80, within its frozen 1e-60 gate.

## Provenance and verification

- Certified parent: `b35525fd01bea949cacd6b2f65939c57a2911682`.
- Preregistration/tests: `f53d4f375b948076fd2f0d54eac3b07d80aa4f63`.
- Expected RED: [36353928893](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36353928893), job `108717768272`, artifact `10943346921`. Setup passed; the test reported the absent scientific implementation. ZIP SHA-256: `df07b80b51f6cd796426b0186c22efcb62d1878da7bcb63848dc428cc28d48db`.
- Tested implementation: `f0b7618a07389f901cd112d1b491e70c5e02c260`.
- GREEN: [36354287734](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36354287734), job `108718790460`, [artifact 10943337606](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36354287734/artifacts/10943337606).
- GREEN ZIP SHA-256: `28ed9ef425cfc90bbec48354657348eaa0859bf77f7e6884dba56e5c763a9efd`.
- Lossless [RESULT.json](RESULT.json) SHA-256: `a61ca58f52ca49e9a9f4186ded63a29b9cf84195f688ba00e77d05d15329370a`.

Both exact job logs and downloaded artifacts were inspected. ZIP hashes, execution heads, frozen source bytes, and GREEN SHA256SUMS entries were verified. The scientific verdicts above were read from the result JSON, not inferred from workflow status. SHA256SUMS retains the artifact filename `result.json`; its bytes are published here as `RESULT.json`. Documentation is a subsequent additive commit; the tested implementation SHA above identifies the scientific run.

## Boundaries and next question

This remains a conditional qubit Bloch-channel interpretation of the retained loop, not an identification with the original three-qubit source law. It selects no physical source law, introduces no fundamental time, and derives no gravity. Powers count composition. Historical NOs, including v15.81's finite-window failure, remain unchanged.

The full linear action T, including its zero action on the discarded direction, was held fixed. Changing that action while agreeing only on the surviving plane is a different completion problem and was not tested. The next mathematically distinct question is whether CPTP agreement on the surviving plane requires restoring an action on the discarded direction. Any such completion would not retroactively rescue the fixed maps tested here or establish continuous full polar transport across v15.82's boundary.

No merge to main.
