# Round 10 External Validation Milestone Writeup

## Title
Round 10 External Validation of the Frozen Bridge Workflow Using THINGS and SINGS/IRAC Public Data

## Executive Summary

This bundle documents the current state of the Round 10 external-validation effort. The original challenge was fair and explicit: the simplest explanation, by Occam's razor, was that Bridge might still be a SPARC-specific or overfitted mechanism until it passed frozen testing on genuinely external data.

The work documented here does **not** yet constitute a final blind adjudication across a large independent galaxy sample. However, it **does** establish a meaningful external-validation milestone:

1. A working external reconstruction path was built using public THINGS H I products and SINGS/IRAC stellar products.
2. That path was shown to work on multiple galaxies, not just one.
3. In the most mature pilot cases, the **frozen Bridge law remained positive relative to baryonic-only fits after major SPARC-side ingredients were replaced with external reconstructions or externally shaped proxies.**

This is scientifically meaningful pilot evidence. It is not yet decisive proof.

---

## Scientific Question

The central question for Round 10 is:

> Does the frozen Bridge workflow continue to show signal once key observables are reconstructed from external public datasets rather than inherited directly from SPARC?

This breaks into two separate technical questions:

1. **Geometry / reconstruction question**  
   Can a raw external 2D velocity field be converted into a believable 1D rotation curve?

2. **Model question**  
   Once that external observable is credible, does the frozen Bridge law still outperform baryonic-only fits?

Keeping those questions separate is important. A failed geometry solution is **not** a Bridge failure; it is a preprocessing failure.

---

## Data Sources Used

### External data
- **THINGS** public H I products:
  - moment-0 (integrated H I)
  - moment-1 (velocity field)
  - moment-2 (dispersion)
- **SINGS / IRSA IRAC1** public stellar images and weight maps (for stellar disk proxy work)

### Internal comparison / target references
- `rotation_curve_corpus_v7.json`
- SPARC entries
- THINGS entries embedded in the corpus

---

## Method Summary

### Stage 1: External rotation-curve reconstruction
For each galaxy:
- Download THINGS `mom0`, `mom1`, `mom2`
- Choose or refine:
  - center `(xc, yc)`
  - inclination
  - position angle
  - systemic velocity
- Deproject the line-of-sight velocity field using major-axis selection
- Build a 1D radial rotation curve
- Compare the reconstructed curve to THINGS-corpus and/or SPARC references

### Stage 2: External gas proxy
- Start from THINGS `mom0`
- Build cumulative H I radial profiles
- Compare cumulative gas proxy or gas-support proxy to SPARC `Vgas^2`
- Promote the best external gas-shape proxy into an external `Vgas(r)` proxy

### Stage 3: External disk proxy
- Start from SINGS / IRAC1 stellar image
- Build robust radial light profile
- Convert to a cumulative or support-style proxy
- Compare to SPARC `Vdisk^2`
- Promote best disk-support proxy into an external `Vdisk(r)` proxy

### Stage 4: Frozen Bridge test
Run the frozen Bridge workflow on:
- external `Vobs`
- externalized `Vgas`
- externalized `Vdisk`
- `Vbul = 0` when appropriate for bulgeless pilot cases

Compare Bridge RMSE to baryonic-only RMSE.

---

## Results by Galaxy

# 1. DDO154

## External rotation-curve reconstruction
The DDO154 THINGS reconstruction closely matched the SPARC DDO154 reference.

### Key comparison
- `n_compared = 12`
- `RMSE = 2.6029 km/s`
- `MAE = 2.2612 km/s`
- `Corr = 0.9864`

### Interpretation
This established that the external reconstruction path could work at high fidelity on a real non-SPARC public dataset.

## External gas proxy
The local `mom0(r)` profile was the wrong quantity to compare directly to `Vgas^2`, but the cumulative gas profile worked strongly.

### Gas-shape correlations
- correlation vs cumulative gas profile: `0.8897`
- correlation vs gas-support proxy: `0.8018`

### Interpretation
The THINGS H I map carried the right radial gas-shape information.

## External disk proxy
The first raw IRAC pass was noisy and not trustworthy. After robust centroiding, sky subtraction, and clipped annular summaries, the disk shape became usable.

### Robust disk-shape correlations
- clipped mean vs `Vdisk^2`: `0.6576`
- clipped median vs `Vdisk^2`: `0.6703`
- clipped weighted mean vs `Vdisk^2`: `0.7520`

### Interpretation
The stellar side was recoverable, though noisier than the gas side.

## Frozen Bridge tests on DDO154

### Hybrid external pilot (external `Vobs`, SPARC baryons)
- RMSE baryonic: `21.2076`
- RMSE Bridge: `18.8522`
- improvement: `2.3554 km/s`

### External gas proxy pilot
- RMSE baryonic: `22.4283`
- RMSE Bridge: `20.0473`
- improvement: `2.3810 km/s`

### External gas + external disk proxy pilot
- RMSE baryonic: `22.6650`
- RMSE Bridge: `20.8481`
- improvement: `1.8169 km/s`

### Smoothed external gas + external disk proxy pilot
- RMSE baryonic: `22.6464`
- RMSE Bridge: `19.9073`
- improvement: `2.7391 km/s`

### DDO154 conclusion
DDO154 became the first **nearly full external pilot success**. Bridge remained positive even after major SPARC-side ingredients were replaced with external proxies.

---

# 2. NGC 2403

## Initial status
A crude quick-pass reconstruction failed because the geometry basin was wrong.

## Geometry refinement
Using a tighter THINGS-like basin and then local refinement, the NGC 2403 reconstruction became credible.

### Best refined geometry
- `xc = 1020.0`
- `yc = 1021.0`
- `incl = 62.3 deg`
- `PA = 42.8 deg`
- `vsys = 107.0 km/s`

## External rotation-curve reconstruction

### Refined vs THINGS
- `n = 286`
- `RMSE = 12.2814`
- `MAE = 9.6506`
- `Corr = 0.9033`

### Refined vs SPARC
- `n = 69`
- `RMSE = 12.6581`
- `MAE = 10.0244`
- `Corr = 0.9330`

### Interpretation
This showed that the external workflow generalized to a second galaxy once the correct geometry basin was found.

## External gas proxy
The cumulative THINGS gas profile matched the SPARC gas-support shape extremely well.

### Overlap-only gas correlations
- `n valid cumulative = 68`
- correlation vs cumulative gas profile: `0.9903`
- correlation vs gas-support proxy: `0.7012`

### Interpretation
NGC 2403 gas reconstruction was very strong.

## External gas Bridge pilot
- RMSE baryonic: `38.5880`
- RMSE Bridge: `36.0456`
- improvement: `2.5424 km/s`

## External disk proxy
The raw IRAC brightness profile was again the wrong quantity to compare directly to `Vdisk^2`.

### Direct profile correlations
- clipped mean vs `Vdisk^2`: `-0.2328`
- clipped median vs `Vdisk^2`: `-0.2381`
- clipped weighted mean vs `Vdisk^2`: `-0.1711`

This looked bad until the physically correct disk-support proxy was constructed.

### Cumulative/support proxy correlations
- correlation vs cumulative stellar profile: `-0.2213`
- correlation vs disk-support proxy: `0.8903`

### Interpretation
The stellar information was there, but it had to be translated into a disk-support-style quantity.

## Nearly full external Bridge pilot on NGC 2403
With external `Vobs`, external gas proxy, and external disk proxy:

- RMSE baryonic: `39.0149`
- RMSE Bridge: `36.3410`
- improvement: `2.6739 km/s`

### NGC 2403 conclusion
NGC 2403 became the second **nearly full external pilot success**.

---

# 3. NGC 3198

## Initial status
A quick pass landed in the wrong basin and failed badly.

### Quick-pass comparison
- vs THINGS:
  - RMSE `109.8116`
  - MAE `105.6934`
  - Corr `0.4332`
- vs SPARC:
  - RMSE `102.2775`
  - MAE `96.8701`
  - Corr `0.3236`

### Interpretation
This was a reconstruction failure, not a Bridge failure.

## Basin relocation
A broader relocation search found a much better geometry neighborhood.

### New best basin
- `xc = 535`
- `yc = 536`
- `incl = 50 deg`
- `PA = 15 deg`
- `vsys = 600 km/s`
- RMSE `23.43`
- MAE `18.76`
- Corr `0.770`

## Local refinement
A tighter refinement improved the solution further.

### Best refined geometry
- `xc = 541.0`
- `yc = 542.0`
- `incl = 50.0 deg`
- `PA = 15.0 deg`
- `vsys = 595.0 km/s`

## Refined reconstruction

### Refined vs THINGS
- `n = 63`
- `RMSE = 16.6063`
- `MAE = 13.6945`
- `Corr = 0.8446`

### Refined vs SPARC
- `n = 33`
- `RMSE = 20.5236`
- `MAE = 17.0870`
- `Corr = 0.8490`

### Interpretation
NGC 3198 is now a **real third-galaxy external reconstruction success**, though rougher than DDO154 and NGC 2403.

### NGC 3198 conclusion
This is best labeled as:
- **third-galaxy reconstruction success**
not yet
- third nearly full external pilot

The external component path for NGC 3198 has not been carried as far as DDO154 / NGC 2403.

---

## Overall Scientific Interpretation

### What is scientifically meaningful already
Yes, the results are scientifically meaningful **in a bounded pilot sense**.

The following claims are now defensible:

1. A working external reconstruction path exists using public THINGS and SINGS/IRAC data.
2. That path is not limited to one simple galaxy.
3. The frozen Bridge workflow remains positive after substantial externalization of the baryonic inputs in the most mature pilot cases.
4. The externalization path behaves honestly:
   - some galaxies work quickly,
   - some require geometry refinement,
   - and a failed quick pass does not automatically imply model failure.

### What cannot be claimed yet
Not yet defensible:
- that overfitting has been ruled out decisively
- that Bridge has passed a large blind external adjudication
- that all external baryonic decompositions are fully first-principles and final
- that the observed signal is universal across a large new sample

---

## Best Current Status Label

Recommended status label:

**Meaningful pilot external-validation evidence**

or

**A real external validation milestone, but not yet decisive adjudication**

---

## Most Important Result

The single most important scientific pattern is:

> As major SPARC-side ingredients were replaced by external reconstructions or externalized proxies, the frozen Bridge law remained positive relative to baryonic-only fits in the two most mature pilot galaxies.

That is the strongest current answer to the overfitting criticism.

---

## Recommended Next Steps

### Immediate next step
Package the three-galaxy milestone cleanly:
- DDO154
- NGC 2403
- NGC 3198

### Two sensible follow-on directions

#### Option A: strengthen method
Build a reusable external reconstruction pipeline notebook/script so future galaxies can be processed more systematically.

#### Option B: strengthen evidence
Push to a fourth galaxy and/or convert NGC 3198 into a full external component pilot.

### Harder next threshold
The next threshold that would shift this from “meaningful” to “hard to dismiss” would be:
- a small frozen multi-galaxy external set run with no ad hoc retuning beyond documented geometry calibration, and/or
- a larger public external catalog workflow

---

## Bottom Line

Round 10 has progressed from:
- external data incompatibility

to:
- one strong external pilot (DDO154)

to:
- a second nearly full external pilot (NGC 2403)

to:
- a third successful external reconstruction (NGC 3198)

That is a real scientific milestone.
