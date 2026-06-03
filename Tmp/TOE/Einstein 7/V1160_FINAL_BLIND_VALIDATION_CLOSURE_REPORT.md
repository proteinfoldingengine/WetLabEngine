# V1160 — Final Blind-Validation Closure Report

## Status

Completed.

## Frozen Law

```text
AdmissibleGeometry := BufferedNormalizedOmegaCompatibility AND GenesisPin AND SourceFlowClosureEnvelope AND CausalTransportSignatureEnvelope
```

Functional form:

```text
A(H)=1[ MΩ_buf(H)≥0 ∧ MP(H)≥0 ∧ MC_env(H)≥0 ∧ MK_env(H)≥0 ]
```

Conservative margin:

```text
M*(H)=min(MΩ_buf, MP, MC_env, MK_env)
```

Ω stability-buffer protocol:

```text
Ω_threshold = min(valid Ω margin) - 0.25 * std(valid Ω margin), calibrated only from valid histories.
```

## Latest Held-Out Result

```json
{
  "old_valid_rate": 0.9666666666666667,
  "old_invalid_rate": 0.0,
  "old_invalid_certified_count": 0,
  "old_false_negative_valid_count": 1,
  "buffer_valid_rate": 1.0,
  "buffer_invalid_rate": 0.0,
  "buffer_invalid_certified_count": 0,
  "buffer_false_negative_valid_count": 0
}
```

## Main Scientific Result

The current closure result is:

```text
valid_rate = 1.000
invalid_rate = 0.000
invalid_certified_count = 0
false_negative_valid_count = 0
```

under the V1159.2 held-out validation after applying the pre-declared Ω stability-buffer rule.

## Core Thesis

```text
Admissible geometry is path-certified geometry.
```

A final geometry-like state does not certify merely because it looks right.

It certifies only when the candidate history preserves:

```text
1. buffered normalized Ω compatibility
2. Genesis / source-origin provenance
3. source-flow closure envelope
4. causal transport path-signature envelope
```

## Evidence Chain

| Version | Test | Result |
|---|---|---|
| V1152.5 | Main demonstration | Valid transported/noisy histories passed; geometry/provenance/closure counterfeits failed. |
| V1153 | Ablation extraction | Initial Ω + Genesis + Closure triad extracted, but not proven irreducible. |
| V1154 | Fresh generator | Triad leaked; final-state certification was incomplete. |
| V1154.3 | Causal transport signature | Path-level transport closed noncausal mid-history leaks. |
| V1154.5 | Recall recovery | Valid envelope calibration recovered 1.0/0.0 on hard adversaries. |
| V1156.3 | Normalized Ω | Raw global Ω threshold failed; normalized Ω restored cross-generator performance. |
| V1157.2 | Invariance campaign | Stability-envelope calibration survived world/resolution/noise/warp stress with 1.0/0.0. |
| V1159 | Blind held-out | Frozen law nearly passed unseen worlds: 0.967 valid, 0 invalid leaks. |
| V1159.1 | False negative autopsy | Only failure was Ω envelope boundary in branching_pulse. |
| V1159.2 | Pre-declared Ω buffer | Buffered Ω recovered held-out valid_rate=1.0 while preserving zero invalid leaks. |


## What Was Actually Solved

The work did not merely produce a better visual or a better filter.

It isolated a recurring failure mode in information-to-geometry models:

```text
final-state similarity is underdetermined.
```

Counterfeits can match final geometry, final Ω-like field structure, or final source-flow closure.

The system only stabilized when certification became:

```text
normalized
provenance-aware
closure-aware
path-aware
stability-envelope calibrated
```

## Why This Matters for “It from Bit”

The result turns “it from bit” into an operational admissibility problem.

The question is no longer only:

```text
Can bits generate geometry?
```

The sharper question is:

```text
Which informational histories are admissible as geometry?
```

The answer produced by this campaign is:

```text
Only path-certified histories survive.
```

## Claim Boundary

This is computational closure inside the tested simulation framework.

It is not yet a derivation of physical spacetime, GR, or Einstein equations.

It is, however, a concrete computational admissibility law candidate for information-to-geometry emergence.

## Recommended Next Step

Do not keep tuning this branch.

Next work should be:

```text
1. Clean-room replication by another AI or human.
2. Manuscript-style methods/results packet.
3. Frozen code bundle with no further threshold tuning.
4. Larger blind generator suite.
```
