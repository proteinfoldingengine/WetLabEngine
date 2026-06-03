# Next AI Takeover Instructions — V1025

## Current strongest result

V1025 established the primitive native continuity closure:

```text
C_native = Δsource + dt·div(J·source)
J = -∇ψ
```

Result:

```text
legitimate C_norm: 0.4107
control C_norm:    10.3649
gap:               9.9541

legitimate corr(Δsource, -dt·div(J·source)): 0.9012
control corr:                                0.0043
```

Interpretation:

```text
The primitive native continuity closure is strong.
The weak V1024/V1024.1 ADM-like closure was caused by lifting too early.
```

## Full stack that must stay in place

Do not run higher ADM/Bianchi/GR-adjacent tests unless this full stack remains active:

```text
1. Ω similarity
   geometry resemblance

2. Genesis Pin
   provenance legitimacy

3. source-flow closure
   ordered accessibility consistency

4. raw source-manifold residual
   nonfactorized leakage detection

5. source-event origin binding
   forged source rejection

6. native continuity closure
   C_native = Δsource + dt·div(J·source)
```

Each layer is non-redundant. Do not collapse them into one score.

## Key milestone chain

```text
V1011:
  Ω + Genesis allowed source_shuffled_null through.

V1011.1:
  Added B-like source-flow closure.
  Immediate bug fixed.

V1012:
  Generalization failed under harder counterfeits.

V1013:
  All surviving invalids were nonfactorized_leakage.

V1014:
  Exported summary metrics were insufficient.

V1015:
  Raw source-manifold residual fixed leakage.
  invalid certified = 0.

V1016–V1017:
  Leave-one-family-out and portable threshold normalization.
  invalid certified = 0 in all folds.

V1018:
  Leakage strength sweep passed.
  nonzero leakage certified = 0.

V1019:
  Forged source-manifold attack passed closure.
  Exposed need for source-origin predicate.

V1020:
  First source-origin predicate failed.

V1020.1:
  Source-event binding fixed forged-source attack.
  forged with source-origin binding certified = 0.

V1021:
  Certified-source ADM re-audit.
  Momentum-like branch was strong.
  Hamiltonian-like branch was weak.

V1022:
  Hamiltonian branch improved with flow-pressure terms.
  H_norm 0.6998 → 0.1231.
  But H was not discriminative.

V1023:
  Role separation:
  H branch = broad same-slice compatibility.
  M branch = certification-sensitive separator.

V1024:
  Bianchi-like ADM closure failed because slices were artificial.

V1024.1:
  Native ordered updates helped weakly.

V1025:
  Primitive native continuity closure gave strong signal.
```

## Claim boundaries

Allowed:

```text
model-native accessibility-flow closure
native continuity closure
source-flow conservation-like diagnostic
ADM-like same-slice diagnostic
Bianchi-like structural role inside the recoverability model
```

Not allowed:

```text
physical General Relativity
Einstein equations
actual Bianchi identity
actual ADM constraints
physical spacetime curvature
tensor covariance
quantum gravity
```

Correct framing:

```text
The recoverability/accessibility framework exhibits a model-native continuity closure
that may play the structural role required before any legitimate ADM/Bianchi-like
lift can be tested.
```

## Recommended next branch: V1026

Name:

```text
V1026 — Continuity-to-ADM Lift Rebuild
```

Do not reuse the weak V1024 closure directly. Build the ADM-like branches from the primitive continuity law.

Recommended construction:

```text
C_native = Δsource + dt·div(J·source)

H_lift = H_full_flow_pressure + α·C_native
M_lift = M_momentum_like + β·∇C_native
```

Test whether adding native continuity correction improves ordered-slice ADM-like closure.

## V1026 pass conditions

```text
1. C_native remains much lower for legitimate native histories than controls.
2. H_lift/M_lift closure improves over V1024.1.
3. Only full-stack-certified histories pass.
4. Forged, shuffled, leaked, and source-origin-invalid histories fail.
```

## Required controls

Include:

```text
source_shuffled_control
forged_static_control
nonfactorized_leakage
forged_source_manifold
source-event-origin-invalid forged source
```

## Required ablations

Run:

```text
A. Ω only
B. Ω + Genesis
C. Ω + source-flow closure
D. Ω + Genesis + source-flow closure
E. full stack with source-event origin binding
F. full stack + C_native correction
```

## Root thesis to preserve

Do not copy GR.

Test whether the accessibility-flow constraint system has an internal consistency identity that plays the same structural role as Bianchi:

```text
ordered recoverability updates
→ accessibility density A
→ ψ = log A
→ J = -∇ψ
→ native source continuity
→ certified source/provenance closure
→ ADM-like same-slice constraints
→ model-native Bianchi-like compatibility
```

The current result says the primitive continuity layer is real and strong.

The next task is to lift it correctly.
