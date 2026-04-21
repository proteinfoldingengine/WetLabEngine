# Transfer Status Note

## Purpose

This note consolidates the current transfer-audit results for the hierarchical retained-state bridge and separates which transfer claims are now strong from which still require careful qualification.

The transfer audit was run after hierarchical selector closure and seam-status consolidation.

The three transfer axes considered were:

1. cross-family transfer
2. cross-perturbation transfer
3. cross-scale transfer

---

## 1. Why this note is needed

A selector can look strong on its native construction set and still fail as science if it does not transfer.

The transfer audit therefore asks whether the retained-state bridge law survives:

- family holdout
- perturbation of noise and bridge gain
- scale change

This note records the current answer.

---

## 2. Certified transfer behavior

### A. Cross-family transfer is strong
The hierarchical selector shows strong leave-one-family-out behavior.

Current result:
- LOFO macro F1 mean ≈ **0.884**

This means the selector is not merely memorizing the families used to discover the map.

That is a major positive result.

### B. Cross-perturbation transfer is strong
Across the tested perturbation cells (noise scaling and lambda shifts), performance remained strong.

Current result:
- mean perturbation macro F1 ≈ **0.876**

Several perturbation cells performed near-perfectly.

This supports the claim that the bridge law is robust to moderate perturbations in:
- noise level
- local bridge gain

That is also a major positive result.

---

## 3. Qualified transfer behavior

### Cross-scale transfer is not fully raw-invariant
Without any scale correction, performance across trajectory lengths dropped at the shorter and longer tested scales.

Raw macro F1:
- T = 60 → ≈ **0.662**
- T = 100 → ≈ **0.863**
- T = 140 → ≈ **0.506**

So raw scale transfer is not yet closed.

This means it would be premature to claim full scale invariance in the current raw feature coordinates.

---

## 4. Strong renormalization result

Although raw scale transfer is not fully stable, the scale-renormalization audit showed that a **small affine renormalization** of the trajectory-signature space recovers much of the lost performance.

After affine renormalization:

- T = 60
  - macro F1 improved from ≈ **0.662** to ≈ **0.906**

- T = 140
  - macro F1 improved from ≈ **0.506** to ≈ **0.667**

This is scientifically important.

It means the scale failure is not chaotic or regime-destroying.
It is at least partly **renormalizable**.

So the correct current statement is not:

- “scale transfer fails”

but rather:

> raw scale transfer is incomplete, but the regime map appears approximately stable after affine renormalization.

That is a much stronger and more precise result.

---

## 5. Current best transfer reading

The strongest current transfer reading is:

- **family transfer**: strong
- **perturbation transfer**: strong
- **scale transfer**: incomplete in raw coordinates, but substantially improved by affine renormalization

That is the correct current state of the evidence.

---

## 6. Strongest current admissible claim

The strongest current admissible claim is:

> the hierarchical retained-state bridge transfers strongly across families and moderate perturbations, and its scale dependence appears structured enough to be substantially corrected by a small affine renormalization of the trajectory-signature space.

That is the current claim level supported by the audit.

---

## 7. Strongest inadmissible overclaim

It is not yet justified to claim:

- exact scale invariance in raw coordinates
- fully closed scale transfer without renormalization
- or universal scale closure across all future synthetic families

Those remain open.

---

## 8. Best current publication posture

For publication or public progress reporting, transfer should now be described as:

- family transfer: **supported**
- perturbation transfer: **supported**
- scale transfer: **partially supported via renormalization**
- full raw scale invariance: **not yet established**

That is both strong and honest.

---

## 9. Best next step

The strongest next move is:

> proceed to the **ladder derivation audit**, while carrying forward the transfer result exactly as:
- strong on family and perturbation
- renormalizable but not yet raw-closed on scale

That is the correct next closure stage.
