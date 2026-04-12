# UQCF-GEM publication closeout plan
## Canonical claim
A frozen UQCF-GEM bridge implementation (`v9`) produces a reproducible, measurable **pre-classical structural-ordering effect** in protein folding trajectories across small real-protein targets. The effect improves backbone organization and pooled RMSD/angle metrics, but does **not yet** robustly solve productive long-range contact closure or final basin realization.

---

## Paper type
**Bounded bridge paper**, not "solved folding" and not "full ToE proof."

Working scope:
- bridge-layer hypothesis
- operational observables
- frozen v9 implementation
- 1UAO + 1L2Y results
- pooled confirmation
- trajectory-level artifact packet
- negative branch-family narrowing

---

## Immediate lock decisions
### Freeze
- `v9` only
- no more changes to the mainline
- all paper numbers must come from frozen baseline vs frozen v9

### Do not include as mainline evidence
- v10–v18 as candidate improvements
- speculative branch variants as if they were positive results

### Do include
- v10–v18 only as **negative narrowing / failed replacement families**

---

## Final experimental packet
## A. Canonical mainline packet
Use these as the core result set:
- `uqcf_bridge_patch_v9_1uao_results.csv`
- `uqcf_bridge_patch_v9_1uao_traces.csv`
- `uqcf_bridge_patch_v9_1uao_summary.csv`
- `uqcf_bridge_patch_v9_1uao_stats.csv`
- `uqcf_bridge_patch_v9_1l2y_confirm_results.csv`
- `uqcf_bridge_patch_v9_1l2y_confirm_traces.csv`
- `uqcf_bridge_patch_v9_1l2y_confirm_summary.csv`
- `uqcf_bridge_patch_v9_1l2y_confirm_stats.csv`
- `uqcf_bridge_v9_pooled_summary.csv`
- `uqcf_bridge_v9_pooled_stats.csv`
- `uqcf_bridge_v9_pooled_results.csv`

## B. Mechanism / artifact packet
Use these for operator-trace support:
- `uqcf_bridge_v9_trajectory_packet.md`
- `uqcf_bridge_v9_1uao_rmsd_trace_compare.png`
- `uqcf_bridge_v9_1l2y_rmsd_trace_compare.png`
- `uqcf_bridge_v9_1l2y_sigma_trace.png`
- `uqcf_bridge_v9_1l2y_closure_trace.png`

## C. Negative-family packet
Use as bounded failure analysis:
- `uqcf_branch_family_stop_memo_v13_v16.md`
- `uqcf_bridge_patch_v13_1uao_summary.csv`
- `uqcf_bridge_patch_v14_1uao_summary.csv`
- `uqcf_bridge_patch_v15_1uao_summary.csv`
- `uqcf_bridge_patch_v16_1uao_summary.csv`
- `uqcf_bridge_patch_v17_1uao_summary.csv`
- `uqcf_bridge_patch_v18_1uao_summary.csv`

---

## One last experiment to run before submission
## Bridge-to-classical handoff test
This is the single highest-value remaining experiment.

### Design
For matched seeds and same starting conditions:
1. **Classical-only** relaxation
2. **Bridge preconditioning (`v9`) -> same classical relaxer**

### Measure
- final RMSD
- angle RMS
- dihedral RMS
- contact recovery

### Why it matters
This is the cleanest test of the paper's central interpretation:
> the bridge is upstream of full classical realization and creates a better starting manifold for classical folding.

### Output filenames to create
- `uqcf_bridge_to_classical_handoff_results.csv`
- `uqcf_bridge_to_classical_handoff_summary.csv`
- `uqcf_bridge_to_classical_handoff_stats.csv`
- `uqcf_bridge_to_classical_handoff_traces.csv`
- `uqcf_bridge_to_classical_handoff_plot.png`

If time or scope prevents this, the paper can still go out as a **partial bridge result**. But this experiment is the best upgrade.

---

## Figure list
## Figure 1 — Conceptual architecture
**Filename:** `fig1_bridge_architecture.png`

Show:
- microscopic possibility / local return structure
- bridge layer / multiscale selection
- classical realization / chemistry and mechanics

Caption idea:
> Schematic of the proposed UQCF-GEM bridge layer between microscopic structure and classical fold realization.

## Figure 2 — v9 mechanism diagram
**Filename:** `fig2_v9_operator_diagram.png`

Show:
- observables: `R_micro`, `C_meso`, `loop_compat`
- compression into `sigma_bridge`
- readiness into `closure`
- injection into energy terms

Caption idea:
> Frozen v9 bridge operator: observables, compressed bridge state, and injected energy modulation.

## Figure 3 — 1UAO result summary
**Filename:** `fig3_1uao_summary.png`

Show:
- baseline vs v9 on:
  - best RMSD
  - angle RMS
  - dihedral RMS
  - contact recovery

## Figure 4 — 1L2Y result summary
**Filename:** `fig4_1l2y_summary.png`

Same structure as Figure 3.

## Figure 5 — Pooled packet
**Filename:** `fig5_pooled_v9.png`

Show:
- pooled paired deltas
- p-values for:
  - best RMSD
  - angle RMS
  - dihedral RMS
  - contact recovery

## Figure 6 — Trajectory-level artifact check
**Filename:** `fig6_v9_trajectories.png`

Show:
- 1UAO RMSD over step
- 1L2Y RMSD over step
- optional inset: `sigma_bridge` and `closure_ready`

## Figure 7 — Negative branch-family map
**Filename:** `fig7_branch_family_map.png`

Show:
- v13–v18
- which metric each moved
- why none replaced v9

Caption idea:
> Negative branch-family exploration narrowed the bridge interpretation by showing that routing/closure variants altered tradeoffs without improving the frozen mainline.

---

## Section headers for the paper
## 1. Introduction
- Why a real ToE should generate new organizing principles
- Why protein folding is a meaningful test domain
- Hypothesis: an intermediate bridge layer between microscopic structure and classical realization

## 2. Bridge hypothesis and operationalization
- micro / meso / bridge observables
- `sigma_bridge`
- `closure`
- how the bridge enters the dynamics
- what remains classical

## 3. Experimental design
- proteins: 1UAO and 1L2Y
- baseline vs frozen v9
- matched-seed protocol
- metrics
- branch loop and why v9 was frozen

## 4. Results: frozen v9
- 1UAO
- 1L2Y
- pooled cross-target packet

## 5. Trajectory-level operator trace
- RMSD trajectories
- `sigma_bridge`
- `closure_ready`
- artifact check framing

## 6. Negative branch-family narrowing
- v13–v18
- why routing and finishability families did not replace the mainline
- what this says about the bridge being stronger for ordering than closure

## 7. Interpretation
- bridge effect is real but partial
- pre-classical organization vs downstream classical realization
- why this supports a bounded ToE-style bridge claim

## 8. Limitations
- no solved long-range closure
- no full folding solution
- no claim of full ToE proof
- small-protein regime only
- no TSP trajectory packet included in this paper unless added later

## 9. Future work
- bridge-to-classical handoff
- larger topology classes (e.g. villin / 1VII)
- more complete closure physics

---

## Abstract template
We test whether a UQCF-GEM-inspired multiscale bridge layer can produce a measurable structural effect in protein folding trajectories beyond ordinary classical baseline dynamics. We implement a frozen bridge operator (`v9`) that compresses local and mesoscopic observables into a conformation-dependent bridge state and readiness variable, which then modulate the folding energy prior to full classical realization. Across two small real-protein targets (1UAO and 1L2Y), the frozen bridge implementation improves backbone-ordering metrics and pooled RMSD/angle performance relative to baseline. Trajectory-level traces indicate that the effect is not only endpoint-based, but appears as a distinct pre-classical organization signal during evolution. Negative branch-family tests show that later routing and finishability variants can alter tradeoffs but do not replace the frozen mainline, suggesting that the bridge is stronger as an ordering mechanism than as a complete long-range closure solver. These results support the existence of a bounded, testable bridge-layer effect while leaving productive long-range contact realization as an open downstream problem.

---

## Claim language to keep
Use:
- reproducible bridge-layer effect
- pre-classical structural ordering
- multiscale selection layer
- upstream of full classical realization
- bounded, testable consequence of the framework

Avoid:
- solved folding
- proved the full ToE
- unique explanation of biology
- quantum mechanics directly folds proteins
- complete basin solution

---

## Submission package checklist
- [ ] freeze v9 and record commit hash / code snapshot
- [ ] rerun canonical packet once cleanly if needed
- [ ] run bridge-to-classical handoff test
- [ ] finalize figures 1–7
- [ ] finalize mechanism note
- [ ] finalize negative-family summary
- [ ] draft manuscript
- [ ] prepare public repo / audit folder with canonical files only

---

## One-sentence publication message
> We identified a reproducible, measurable bridge-layer effect that improves pre-classical protein backbone organization across real small-protein targets, supporting a bounded UQCF-GEM-style multiscale selection mechanism upstream of full classical realization.
