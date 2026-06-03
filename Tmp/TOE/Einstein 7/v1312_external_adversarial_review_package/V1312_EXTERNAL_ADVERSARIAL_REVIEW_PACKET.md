# V1312 — External Adversarial Review Package

## Review Target

This package asks you to review the V1300–V1311 synthetic transport branch.

## Frozen Claim Under Review

```text
Inside the tested synthetic transport simulations,
identity + closure is a scaled, adversarially tested minimal sufficient stack
for rejecting identity-matched counterfeits while preserving B-like closure
and ADM_M-like propagation.
```

## Do Not Review As

Do not review this as a claim of:

```text
physical GR
Einstein equations
full ADM derivation
physical spacetime curvature
universal law beyond tested simulations
```

Those are explicitly not claimed.

---

# Evidence Trail

## V1300 — ADM_M-first native momentum primitive

Initial continuity/momentum primitive showed slight ADM_M-like improvement but failed valid-path selection.

## V1302 — Momentum degeneracy audit

The earlier failure was diagnosed as a normalization/setup issue.

Corrected result:

```text
best momentum path = legitimate transport in 36/36 cases
best identity path = legitimate transport in 36/36 cases
```

## V1303 — Momentum propagation

Corrected momentum propagation worked.

Best regime:

```text
identity + momentum
valid_winner_rate ≈ 1.000
valid_weight      ≈ 1.000
ADM_M residual    ≈ 0.011
flow coherence    ≈ 0.9998
```

## V1304 — Bridge unification test

Suggested retained path identity as common ancestor:

```text
identity_only
≈ identity + closure
≈ identity + momentum
≈ identity + closure + momentum
```

But that was before identity-matched counterfeits.

## V1306 — Identity-matched counterfeit test

Identity-only failed:

```text
valid_weight                ≈ 0.507
identity_counterfeit_weight ≈ 0.493
```

Full stack rejected counterfeits:

```text
identity + closure + momentum
valid_weight                ≈ 1.000
identity_counterfeit_weight ≈ 0.000
ADM_M residual              ≈ 0.0009
```

## V1308 — Minimal sufficiency test

Minimal passing stacks:

```text
identity + closure
identity + closure + momentum
```

Failing stacks:

```text
identity only
identity + momentum
closure + momentum
momentum only
closure only
```

## V1310 — Scaling + unseen adversary test

Identity + closure survived scaling and new identity-matched adversaries:

```text
valid_winner_rate              = 1.000
valid_weight                   ≈ 0.998
identity_counterfeit_weight    ≈ 0.002
counterfeit rejection          = 1.000
ADM_M pass rate                = 1.000
closure pass rate              = 1.000
all_pass_rate                  = 1.000
```

---

# Reviewer Questions

## 1. Identity leakage

Does the identity metric encode the legitimate answer too directly?

```text
PASS / WEAK PASS / FAIL:
Notes:
```

## 2. Closure tautology

Does the closure metric merely restate the selection objective?

```text
PASS / WEAK PASS / FAIL:
Notes:
```

## 3. Counterfeit diversity

Are the identity-matched counterfeits strong and diverse enough?

```text
PASS / WEAK PASS / FAIL:
Notes:
```

## 4. ADM_M dependence

Is ADM_M-like propagation independently meaningful, or does it follow by construction?

```text
PASS / WEAK PASS / FAIL:
Notes:
```

## 5. Scaling

Does the tested scaling range support the claim as written?

```text
PASS / WEAK PASS / FAIL:
Notes:
```

## 6. Minimality

Is identity + closure fairly described as minimal among the tested stacks?

```text
PASS / WEAK PASS / FAIL:
Notes:
```

---

# Required Final Reviewer Verdict

Choose one:

```text
PASS
WEAK PASS
FAIL
```

## PASS means

The claim is supported as written, with its boundaries.

## WEAK PASS means

The core result appears real, but the claim should be narrowed.

## FAIL means

The result is not supported even inside the tested synthetic transport setting.

---

# Recommended Reviewer Output Format

```text
Verdict:

Supported findings:

Unsupported or overclaimed findings:

Main methodological concern:

Recommended next test:

Revised claim statement:

Notes on GR/ADM boundary:
```
