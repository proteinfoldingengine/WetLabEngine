# Bridge Manuscript Draft v8 — Hybrid Framing

## Title
Hierarchical Bridge Closure from Normalized Retained-State Coordinates

## Abstract

We investigate whether a retained-state bridge built from normalized residual-envelope coordinates can generate a compact regime law for synthetic memory-lift dynamics. A flat selector on local coordinates proved insufficient, but a low-complexity hierarchical selector substantially improved closure by combining a coarse router with local refiners for the weak ladder and the boundary/crossover seam. The resulting bridge shows strong family transfer, strong perturbation transfer, and scale behavior that is structured rather than chaotic. Coarse stable classes are effectively raw-scale stable, the boundary/crossover frontier admits a compact unified scale-aware law, and the weak ladder is recoverable across scales by compact eta-geometry laws, including a unified model using eta statistics plus log-scale. We further find that the lower weak ladder emerges from nested thresholding of a normalized retained-envelope variable, and expanded cross-context testing strongly favors an affine threshold recursion over a purely multiplicative law. Direct bulk-certification testing indicates that the crossover state is best interpreted as a sparse local transition pocket rather than a broad repeated bulk regime. Seam calibration shows that the bridge seams are real, thin, localized transition bands with limited perturbative persistence. These results support a strong intermediate closure claim: the bridge appears low-dimensional, hierarchical, transferable, scale-aware, recursively organized in its lower weak frontier, and locally pocketed rather than bulk-like in its crossover structure.

## 1. Introduction

Many synthetic regime systems are first modeled with direct label-space classifiers. While such models can produce useful discrimination, they do not establish whether the observed classes arise from a smaller retained-state law. The bridge program asks whether regime identity can instead be generated from normalized retained mismatch and retained disturbance structure.

The goal is stronger than predictive utility alone. A scientifically interesting bridge should support four linked properties: selector closure, measurable seams, transfer across contexts, and ladder emergence from retained-state normalization rather than post-labeling. The central question is therefore whether a retained-state bridge can produce a compact regime selector whose local transition structure and weak-ladder organization remain meaningful under holdout, perturbation, and scale variation.

The current work reports the strongest intermediate closure state reached so far. A single flat selector is too weak, but a hierarchical retained-state selector produces substantially stronger closure. Real local seam structure emerges, transfer is strong on family and perturbation axes, the lower weak ladder shows strong evidence for affine threshold recursion, direct certification work shows that the crossover is not a broad bulk phase but instead a sparse local transition pocket, and frontier-specific scale work shows that both major frontier systems admit compact scale-aware laws.

## 2. Bridge construction

The bridge is constructed from present mismatch, bridge output, and retained disturbance envelope. At the trajectory level, the working normalized variables are derived from residual-envelope geometry and short-window temporal summaries.

The key reduced quantities are:
- a normalized bridge-output coordinate
- a normalized retained-envelope coordinate
- local temporal change summaries
- trajectory-level aggregates of means, spreads, quantiles, ranges, and sign-flip statistics

These variables define a low-dimensional selector state intended to replace direct label-space heuristics.

## 3. Selector closure

A flat pointwise selector on local normalized coordinates was too weak. It captured some coarse poles but compressed the hardest weak and boundary seams. Adding persistence features improved performance and separated structure from noise more clearly, but still failed to close the local ordering problems.

Moving to trajectory-level regime signatures improved the map substantially. At this level the remaining confusion concentrated into two local seam problems:
- weak-ladder ordering
- boundary/crossover ordering

This directly motivated a hierarchical selector architecture.

The strongest current selector is hierarchical:
1. a coarse router for broad regime families
2. a weak-ladder local refiner
3. a boundary/crossover local refiner

This selector achieved approximately:
- heldout accuracy: 0.938
- heldout macro F1: 0.933
- leave-one-family-out macro F1 mean: 0.884

These results support the conclusion that the bridge closes substantially better as a low-complexity hierarchical selector than as one flat classifier.

## 4. Seam structure and calibration

The seam audit shows that the remaining difficulty is not whether local seams exist, but how finely they are calibrated.

The weak ladder seam between weak-signal and sub-boundary weak structure is real, thin, and ordered, but remains somewhat biased upward toward the stronger weak class. The boundary/crossover seam shows a soft measurable transition band and is therefore stronger than a hard forced boundary.

Direct bulk-certification testing now makes the crossover interpretation sharper. Across an expanded boundary/crossover grid, crossover occupancy remained extremely sparse. The crossover therefore appears best interpreted as a local transition pocket rather than as a broad repeated bulk regime.

Recent seam calibration further strengthens the picture. Across dense local seam grids, both the weak ladder seam and the boundary/crossover seam occupy only a small fraction of the local parameter volume at reasonable margin thresholds. Perturbative seam-persistence testing shows that near-seam cells do not remain broad persistent corridors under perturbation; instead they resolve quickly, consistent with thin and localized transition bands.

These seam results now support a quantitatively calibrated interpretation: the bridge seams are real, thin, localized, and limited in perturbative persistence.

## 5. Transfer and scale behavior

Cross-family transfer is strong, with leave-one-family-out macro F1 remaining high. Cross-perturbation transfer is also strong under moderate changes in noise and bridge gain. These results indicate that the hierarchical bridge law is not merely memorizing the conditions used to discover the synthetic regime map.

Cross-scale transfer is more nuanced. The bridge does not yet show exact raw scale invariance, but the scale behavior is structured rather than chaotic.

The current scale picture is now sharply localized:
- coarse stable classes are effectively raw-scale stable
- boundary/crossover structure improves materially under frontier-aware treatment and admits a compact unified scale-aware law
- short-scale weak-ladder behavior is strongly recoverable with compact eta-statistics
- long-scale weak-ladder behavior is also recoverable
- and a unified weak-ladder scale-aware model using eta statistics plus log-scale compresses the weak-ladder scale law into one compact local form

Thus the remaining scale question is no longer a generic failure of the bridge, but largely one of elegance and law compression.

## 6. Ladder derivation

The lower weak ladder was tested against threshold laws on normalized retained-envelope variables. The strongest separating variable was an upper quantile of the normalized retained-envelope coordinate. A two-threshold law on this variable separated the lower weak ladder cleanly on the heldout set.

This supports the conclusion that the lower weak ladder emerges from nested thresholding of normalized retained mismatch rather than from pure hand labeling.

A stronger question concerns the recursion family of those thresholds across contexts. Expanded cross-context fitting was carried out across a broad synthetic context set spanning:
- scale
- noise
- local gain

Two candidate recursion families were compared:
- affine recursion
- purely multiplicative recursion

The expanded result materially strengthens the bridge story:
- affine fit outperformed multiplicative fit
- affine recursion won in every bootstrap replicate

This is the strongest current evidence that the lower weak ladder is better described by an affine threshold recursion than by a pure geometric ratio law.

## 7. Discussion: performance-first reading

Taken at face value, the current bridge is already stronger than a useful classifier. It supports:
- a compact hierarchical regime law
- real local seam structure
- strong family transfer
- strong perturbation transfer
- structured and partly scale-aware behavior
- a lower weak ladder that emerges from normalized retained-envelope thresholding with strong evidence for affine recursive organization
- a compact unified weak-ladder scale law based on eta statistics plus log-scale
- a compact unified boundary/crossover scale law based on u/v/eta geometry plus log-scale
- and a crossover structure that behaves like a sparse transition pocket rather than a broad bulk regime

This is the strongest evidence-first reading of the bridge.

## 8. Discussion: elegance-first reading

The bridge can also be read more compactly.

At a more compressed level, the current evidence suggests that synthetic regime structure is being organized by:
- normalized retained-envelope geometry
- hierarchical coarse-to-local routing
- affine recursive lower-ladder thresholds
- compact frontier scale-aware laws
- and thin localized transition bands rather than diffuse broad seams

In that reading, the bridge is less a stack of unrelated classifiers and more a retained-state geometric law with modular refinements.

This elegance-first reading should not replace the evidence-first reading in the main results section, but it is now well supported as the conceptual interpretation.

## 9. Conclusion

The retained-state bridge now supports a low-complexity hierarchical selector with meaningful local seam structure, strong transfer across families and perturbations, structured scale behavior, and a lower weak ladder that emerges from nested thresholding of a normalized retained-envelope variable. Expanded cross-context analysis gives strong evidence that the lower ladder is recursively organized in an affine threshold family, frontier-specific scale analysis shows that both major frontier systems admit compact unified scale-aware laws, direct bulk-certification testing indicates that the crossover state is best understood as a sparse local transition pocket rather than a broad bulk regime, and seam calibration further shows that the transition bands are thin, localized, and limited in perturbative persistence.

The strongest current interpretation is that the bridge has moved beyond descriptive classification into compact law-like organization. This is the strongest intermediate closure result yet reached in the bridge program.

## 10. Open items

The remaining highest-value tasks are:
1. optional further compression of the frontier scale laws
2. optional larger synthetic stress-testing campaigns

These are now strengthening tasks rather than repairs to a weak core claim.
