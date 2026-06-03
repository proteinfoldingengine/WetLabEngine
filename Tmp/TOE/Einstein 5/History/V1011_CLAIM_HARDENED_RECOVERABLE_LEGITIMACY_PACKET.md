# V1011 Claim-Hardened Recoverable Legitimacy Packet

**Status:** correction / claim-hardening pass  
**Purpose:** Incorporate peer review and correct the V1010 local-minimality overclaim.

## Peer Review Verdict

The peer review is accepted.

The core bridge result remains intact:

```text
visible state + Ω-like geometry is not enough
independent provenance is required
```

The correction is specific:

```text
Do not claim full local minimality of Genesis Pin from the full-stack run.
```

## What Remains Approved

```text
V1003 independent counterfeit stress: approved
V1006 finite formal history-space test: approved
V1007 generalized finite-family sweep: approved
V1008 map-class theorem draft: approved as theorem-candidate
V1009 necessity-vs-specificity boundary: approved
Core theorem-candidate: approved
```

## Corrected V1005 Interpretation

The full-stack ablation result was:

| Component Removed | Invalid Slips | Correct Claim |
|---|---:|---|
| `registry_matches` | 0 | not independently proven necessary by generated attack family |
| `root_matches` | 45 | locally necessary in generated attack family |
| `quorum_valid` | 42 | locally necessary in generated attack family |
| `append_valid` | 43 | locally necessary in generated attack family |
| `non_circular` | 0 | not independently proven necessary by generated attack family |

Therefore:

```text
Root, quorum, and append-only chain were locally necessary
against the generated attack family.

Registry and non-circular were not independently proven necessary
by that generated family.
```

## Corrected Claim Hierarchy

### Level 1 — Strongly Supported

```text
Independent provenance is necessary under the tested map-class conditions.
```

### Level 2 — Supported

```text
Genesis Pin is sufficient in the tested stack.
```

### Level 3 — Partially Supported

```text
Root, quorum, and append-only chain are locally necessary
against the generated attack family.
```

### Level 4 — Not Yet Proven

```text
Registry and non-circular components are independently necessary
in the generated attack family.
```

### Level 5 — Not Proven

```text
Genesis Pin is globally minimal or unique.
```

## Corrected Final Conclusion

```text
V1010 supports the theorem-candidate that visible-state and Omega-like geometry equivalence cannot certify recoverable legitimacy when provenance varies independently. Independent provenance is necessary under the tested map-class conditions. Genesis Pin is sufficient in the tested stack, but complete local minimality and uniqueness are not yet proven.
```

## Why This Strengthens the Work

This correction makes the paper harder to dismiss because it lets the executable proof govern the claim language.

The theorem-candidate does not require proving that every Genesis Pin component is uniquely indispensable.

It requires only the map-class separation:

```text
H = E × R
S(H), Ω(H) depend only on E
P(H) depends on provenance R
```

Under those conditions:

```text
S+Ω cannot certify legitimacy over independently varying provenance.
```

## Next Scientific Step

There are two valid paths:

```text
Option A — Stop and report out using V1011 as the corrected final packet.

Option B — Run V1012 targeted minimality expansion:
construct attacks specifically isolating registry and non-circular failures
to test whether they become locally necessary under expanded adversarial coverage.
```

The correct publication-safe route is Option A unless the paper needs a stronger Genesis Pin minimality claim.
