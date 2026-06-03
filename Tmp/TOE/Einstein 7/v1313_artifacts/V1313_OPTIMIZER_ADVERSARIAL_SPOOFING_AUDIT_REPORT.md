# V1313 — Optimizer Adversarial Spoofing Audit

## Status

Completed.

## Frozen Stack

```text
identity + closure
```

## Summary

```json
{
  "document_id": "V1313_OPTIMIZER_ADVERSARIAL_SPOOFING_AUDIT",
  "status": "completed",
  "frozen_stack": "identity + closure",
  "attack_cases": 5,
  "attacks_per_case": 20,
  "total_optimizer_attacks": 100,
  "spoof_success_count": 11,
  "spoof_success_rate": 0.11,
  "valid_winner_rate": 1.0,
  "mean_valid_weight": 0.7244904953063447,
  "mean_optimizer_counterfeit_weight": 0.27550950469293073,
  "max_optimizer_counterfeit_weight": 0.46385334074649837,
  "summary_by_attack": [
    {
      "attack_type": "direct",
      "spoof_success_rate": 0.0,
      "min_identity": 1.3219055479870197e-14,
      "min_B_like": 0.3206548876519974,
      "max_invalidity": 0.9999999999986156,
      "mean_B_like": 0.49081545010252264,
      "mean_identity": 4.881828112528019e-05
    },
    {
      "attack_type": "joint",
      "spoof_success_rate": 0.0,
      "min_identity": 0.0026445160472263972,
      "min_B_like": 0.17884915656017064,
      "max_invalidity": 0.9999999999977336,
      "mean_B_like": 0.2549883094912381,
      "mean_identity": 0.006155041581139462
    },
    {
      "attack_type": "localized",
      "spoof_success_rate": 0.4,
      "min_identity": 1.3219055479870197e-14,
      "min_B_like": 0.10543194513142788,
      "max_invalidity": 0.9999999999959703,
      "mean_B_like": 0.21745679398441436,
      "mean_identity": 3.708713281433192e-05
    },
    {
      "attack_type": "spectral",
      "spoof_success_rate": 0.04,
      "min_identity": 3.536117324879721e-11,
      "min_B_like": 0.2314155035426097,
      "max_invalidity": 0.9999999999979958,
      "mean_B_like": 0.3654310787968612,
      "mean_identity": 6.240212464068761e-05
    }
  ],
  "verdict": "FAIL_OR_WEAK_PASS",
  "boundary": "Synthetic derivative-free optimizer audit; not physical GR or full ADM."
}
```

## Summary by Attack Type

| attack_type   |   spoof_success_rate |   min_identity |   min_B_like |   max_invalidity |   mean_B_like |   mean_identity |
|:--------------|---------------------:|---------------:|-------------:|-----------------:|--------------:|----------------:|
| direct        |                 0    |    1.32191e-14 |     0.320655 |                1 |      0.490815 |     4.88183e-05 |
| joint         |                 0    |    0.00264452  |     0.178849 |                1 |      0.254988 |     0.00615504  |
| localized     |                 0.4  |    1.32191e-14 |     0.105432 |                1 |      0.217457 |     3.70871e-05 |
| spectral      |                 0.04 |    3.53612e-11 |     0.231416 |                1 |      0.365431 |     6.24021e-05 |

## Case Selection Results

|   case | winner               | valid_winner   |   valid_weight |   optimizer_counterfeit_weight |   best_optimizer_weight |   optimizer_spoof_success_count |
|-------:|:---------------------|:---------------|---------------:|-------------------------------:|------------------------:|--------------------------------:|
|      0 | legitimate_transport | True           |       0.730111 |                      0.269889  |               0.213464  |                               3 |
|      1 | legitimate_transport | True           |       0.923139 |                      0.0768613 |               0.0753535 |                               2 |
|      2 | legitimate_transport | True           |       0.547439 |                      0.452561  |               0.232096  |                               3 |
|      3 | legitimate_transport | True           |       0.885617 |                      0.114383  |               0.113435  |                               1 |
|      4 | legitimate_transport | True           |       0.536147 |                      0.463853  |               0.359177  |                               2 |

## Interpretation

A strong pass requires:

```text
spoof_success_count = 0
valid_winner_rate = 1.0
mean_valid_weight > 0.95
optimizer_counterfeit_weight < 0.05
```

## Boundary

This remains a synthetic optimizer audit. It does not claim physical GR, Einstein equations, physical spacetime curvature, or full ADM derivation.
