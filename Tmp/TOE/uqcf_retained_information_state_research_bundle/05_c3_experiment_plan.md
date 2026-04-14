# C3++ Retained-Information State Experiment Plan
## Executable TOE Advancement Step

## Goal
Operationalize the retained-information state problem inside C3++ as a real experiment.

We want to answer:

> Is future inference realizability fully described by the current visible state G_t, or does retained telemetry state R_t add predictive information?

This document turns that into a concrete experiment.

---

## 1. Core hypothesis

### Null hypothesis H0
Future outcome over horizon H is fully predicted by current visible state:

Y_(t→t+H) = Psi(G_t)

### UQCF-GEM retained-information hypothesis H1
Future outcome over horizon H is better predicted by:

Y_(t→t+H) = Psi(G_t, R_t)

where:
- G_t = instantaneous visible state
- R_t = retained telemetry state

If H1 materially outperforms H0, then current visible state is incomplete.

---

## 2. Experimental objects

## 2.1 Current visible state G_t
Use only features that are instantaneous or local-in-time.

Recommended first set:
- current_entropy
- current_topk_mass
- current_repetition_ratio
- current_local_semantic_displacement
- current_hidden_state_projection_1
- current_hidden_state_projection_2
- current_hidden_state_projection_3

These should be computed per token or per short rolling window.

## 2.2 Retained telemetry state R_t
Use only memory-like cumulative channels.

Recommended first set:
- mem_tension
- mem_drift
- mem_entropy
- mem_repetition
- mem_recovery
- mem_pink_noise_deviation

These should be rolling or exponentially weighted state variables, not instantaneous values.

## 2.3 Future outcome Y_(t→t+H)
Start simple.

Recommended first binary target:
- fail_within_H

Definition:
1 if the generation enters failure mode within the next H tokens
0 otherwise

Possible failure modes:
- hallucination onset
- repetition collapse / loop
- refusal collapse
- instability spike
- answer-quality drop below threshold

Start with one clean label, then add others later.

---

## 3. Data logging requirements

For every token step t, log:

### Identity
- run_id
- prompt_id
- model_id
- token_index

### Current visible state G_t
- current_entropy
- current_topk_mass
- current_repetition_ratio
- current_local_semantic_displacement
- current_hidden_state_projection_1
- current_hidden_state_projection_2
- current_hidden_state_projection_3

### Retained telemetry state R_t
- mem_tension
- mem_drift
- mem_entropy
- mem_repetition
- mem_recovery
- mem_pink_noise_deviation

### Outcome labels
- fail_within_16
- fail_within_32
- fail_within_64

Optional later:
- recover_within_16
- loop_within_32
- quality_drop_within_32

---

## 4. First experiment

## Experiment name
Matched Current State, Divergent Retained State

## Procedure
1. Collect many fully instrumented trajectories
2. Build a row per token step
3. Compute:
   - G_t feature vector
   - R_t feature vector
   - future failure labels
4. Match rows with:
   - small distance in G_t
   - large distance in R_t
5. Compare future outcomes

## Expected result if retained-information matters
Rows with similar G_t but different R_t should show different future failure probabilities.

---

## 5. Predictor comparison

Train two models on the same dataset.

## Model A — Current-state only
Inputs:
- G_t only

Output:
- fail_within_H

## Model B — Current-state + retained state
Inputs:
- G_t + R_t

Output:
- fail_within_H

## Success criterion
Model B should materially outperform Model A on held-out data.

Recommended metrics:
- ROC AUC
- PR AUC
- log loss
- calibration error

A secondary success criterion:
matched-current-state pairs with divergent R_t should have systematically different empirical failure rates.

---

## 6. Matching rule

For matched-pair analysis:

### Keep pairs with:
- low G_t distance
- high R_t distance

Example:
- cosine or Euclidean distance for G_t below threshold
- Euclidean distance for R_t above threshold

This directly tests state completeness.

---

## 7. Minimal theorem target

If the experiment succeeds, the next theorem-style claim is:

> There exist inference states with similar instantaneous visible configuration G_t but different retained telemetry state R_t whose future realizability differs systematically.

This would be a real TOE advance.

---

## 8. Recommended sequence

### Phase 1
Single model, single prompt family, one failure label

### Phase 2
Multiple prompt families, same model

### Phase 3
Cross-model transfer

### Phase 4
Reintroduce the retained-information state back into bridge/folding systems using the now-validated observable family

---

## 9. What would weaken the claim
The retained-information hypothesis weakens if:
- G_t-only and G_t+R_t perform similarly
- matched-G_t / divergent-R_t pairs do not differ in future outcomes
- the retained channels are fully reconstructible from G_t

---

## 10. Bottom line
This is now the cleanest real-system TOE experiment available in your stack:

> Test whether future inference failure/recovery is predicted better by current visible state plus retained telemetry than by current visible state alone.

If yes, the retained-information state problem becomes a real empirical result rather than only a philosophical claim.
