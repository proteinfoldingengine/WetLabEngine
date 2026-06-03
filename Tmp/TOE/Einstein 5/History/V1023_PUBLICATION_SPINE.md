# V1023 Publication Spine  
## Recoverable Legitimacy Under Observable Compression

**Status:** publication-spine draft  
**Purpose:** Provide the clean spine for a manuscript, report, or external AI handoff.

## One-Sentence Claim

```text
When observable form compresses away provenance, legitimacy cannot be recovered from form alone.
```

## Formal Spine

```text
Let H=E×R and F(H)=(S(H),Ω(H)). If H(P|F)>0, then no F-only certifier can certify recoverable legitimacy; a provenance-bearing information channel is required.
```

## Core Equations

```text
H = E × R
F(H) = (S(H), Ω(H))
H(P | F) > 0  ⇒  F-only certification is underdetermined
I_missing = log2(|R_equivalence_class|)
```

## Adaptive Corollary

```text
Adaptive optimization of F-similarity cannot recover legitimacy information not encoded in F.
```

## Genesis Pin Status

```text
Genesis Pin is sufficient in the tested stack; targeted local minimality is supported; global minimality and uniqueness remain unproven.
```

## Publication Structure

| Section | Title | Content |
|---|---|---|
| 1 | Problem | Visible state and Ω-like geometry can match while recoverable provenance differs. |
| 2 | Map-Class Setup | H = E × R; F(H)=(S(H),Ω(H)); P(H) is provenance legitimacy. |
| 3 | Core Theorem Candidate | If H(P|F)>0, no F-only certifier can determine recoverable legitimacy. |
| 4 | Information Equation | I_missing = log2(|R_equivalence_class|). |
| 5 | Adaptive Corollary | Optimizing F-similarity cannot create provenance information absent from F. |
| 6 | Genesis Pin Role | Sufficient tested provenance implementation; targeted local minimality supported; uniqueness unproven. |
| 7 | Falsification Boundary | If F fully encodes provenance, H(P|F)=0 and theorem condition is not met. |
| 8 | Claim Boundary | No GR, spacetime, cryptographic-production, global-minimality, or uniqueness claim. |

## Reviewer-Safe Abstract

```text
This work studies recoverable legitimacy in systems where terminal observables
and geometry-like response fields compress ordered histories. We model histories
as H = E × R, where E is event/order structure and R is provenance metadata.
When the observable map F(H)=(S(H),Ω(H)) does not injectively encode provenance,
legitimacy can vary inside an F-equivalence class. In that case H(P|F)>0, and
no certifier using F alone can distinguish legitimate from illegitimate histories.
Computational stress tests, finite history-space constructions, entropy audits,
and adaptive adversary tests support the same conclusion: form-equivalence is
not source-equivalence. A provenance-bearing information channel is required.
Genesis Pin is one sufficient tested implementation in this stack, with targeted
local minimality supported, while global minimality and uniqueness remain open.
```

## Do-Not-Overclaim Boundary

Do not claim:

```text
physical spacetime
General Relativity
Einstein equations
actual ADM physics
physical curvature
quantum gravity
production cryptography
Genesis Pin uniqueness
global minimality
```

## Final Public-Friendly Line

```text
State is not history. Geometry-like form is not provenance. If the information
needed to prove origin is not in the observable, no amount of matching the
observable can recover it.
```
