# Round 15 Replication Guide

## Purpose
This package explains how to replicate the **Round 15 hardened prototype checkpoint** using the same cluster workflow that was used in the conversation.

It is written to be practical first:
- what to lock,
- what to extract,
- what math to apply,
- what Python to run,
- and how to report the result.

This is a **prototype replication guide**, not a claim of production-grade external validation.

## Round 15 closeout state being replicated

### Tier 1: relaxed clusters
- **Abell 2261** → `positive_signal`
- **Abell 1689** → `neutral`

### Tier 2: merger-offset cluster
- **1E 0657-56 (Bullet Cluster)** → `positive_signal`

### Aggregate read
- 3 systems
- 2 positive
- 1 neutral
- 0 destructive failures
- 0 catastrophic failures

## Replication philosophy
Round 15 used a strict sequence:

1. **Lock sources first**
2. **Choose exact pages**
3. **Extract only from those pages**
4. **Score with frozen logic**
5. **Audit failure modes**
6. **Only then interpret**

The key discipline is that the scaffold is **not retuned per object**.

## File families used in the workflow

### Prior public framework references
These are continuity references, not substitutes for current Round 15 evidence.

- `WetLabEngine` GitHub repository
- `RecreateResults.py`
- `uqcf_gem_lensing_verifier.py`
- `stellar_profile_to_map.py`
- `phase3_bullet-lensing_M31.yml`

### Round 15 local artifact families
For each system, Round 15 used files of the form:
- source papers / PDFs
- manual extraction CSVs
- score JSONs
- scoreable profile CSVs
- checkpoint JSONs
- closeout memo Markdown

## Tier 1 workflow: relaxed clusters
Tier 1 compares two radial observables on a shared radius grid.

### Abell 2261
- X-ray / gas-side anchor: `abell2261_clash_mass_profile_2012.pdf`, page 14
- Lensing mass-side anchor: `abell2261_clash_mass_profile_2012.pdf`, page 12

### Abell 1689
- Gas / temperature-side anchor: `abell1689_projected_potential_xray_2015.pdf`, page 5
- Projected mass-side anchor: `abell1689_strong_weak_lensing_halkola_2006.pdf`, page 16

### Tier 1 scoring idea
For each shared radius \(R_i\):
1. extract gas-side or temperature proxy \(g_i\)
2. extract mass-side proxy \(m_i\)
3. normalize each by its own maximum
4. compute the absolute normalized gap

\[
	ilde g_i = rac{g_i}{\max_j g_j}, \qquad
	ilde m_i = rac{m_i}{\max_j m_j}
\]

\[
\Delta_i = |	ilde g_i - 	ilde m_i|
\]

Then compute the mean:

\[
ar\Delta = rac{1}{N}\sum_{i=1}^{N}\Delta_i
\]

### Tier 1 verdict rule used in Round 15
- `positive_signal` if mean gap < 0.10
- `neutral` if 0.10 <= mean gap < 0.25
- `destructive_failure` if mean gap >= 0.25

This is a **prototype scoring rule**, not a final astrophysical likelihood model.

## Tier 2 workflow: merger-offset systems
Tier 2 asks whether gas peaks and mass peaks are clearly offset in the expected merger geometry.

### Bullet Cluster anchors
- Gas/X-ray morphology: `bullet_cluster_chandra_2006.pdf`, page 2
- Mass map: `bullet_cluster_lensing_2006.pdf`, page 10
- Offset calibration support: `bullet_cluster_lensing_2006.pdf`, page 8

### Tier 2 scoring idea
For each component, extract gas and mass peak positions in a common local frame:

\[
(x_g, y_g), \qquad (x_m, y_m)
\]

Then compute the offset magnitude:

\[
D = \sqrt{(x_g - x_m)^2 + (y_g - y_m)^2}
\]

### Tier 2 prototype verdict rule used in Round 15
- `positive_signal` if both major components show clear nonzero bounded offsets
- `neutral` if only one component is convincing
- `destructive_failure` if offsets collapse or become unusable / nonsensical

For the tighter Bullet pass, page-8 table values were used as calibration support, making the result stronger than the first rough pass.

## Final Round 15 prototype results

### Abell 2261
- mean absolute normalized gap = **0.09067254826748498**
- verdict = `positive_signal`

### Abell 1689
- mean absolute normalized gap = **0.10646864686468643**
- verdict = `neutral`

### Bullet Cluster
- main offset = **306.0 kpc**
- subcluster offset = **182.3 kpc**
- evidence level = `page_locked_and_table_calibrated`
- verdict = `positive_signal`

## Why this was called a round win
Round 15 was classified as a **conditional hardened prototype win** because:
- the frozen scaffold produced positive/neutral signal in both target regimes,
- the Bullet result was hardened beyond a loose first-pass extraction,
- and there were zero catastrophic failures.

## What this does *not* mean
This replication package does **not** claim:
- full external production-grade validation,
- a finished automated pipeline,
- or universal finality across all merger analogs.

It documents how the checkpoint was reached and how to reproduce the same style of result.
