# V1010 Final Recoverable Legitimacy Theorem-Candidate Packet

**Status:** final report-out packet for the current iteration  
**Scope:** Recoverability / Genesis Pin / Ω-like geometry legitimacy bridge  
**Claim level:** theorem-candidate under specified map-class conditions

## Executive Summary

The current iteration has reached report-out.

The evidence chain now supports a disciplined theorem-candidate:

> For a history space H = E × R where terminal visible observables S(H) and geometry-like fields Ω(H) depend only on event/order structure E, visible-state equivalence and geometry-like equivalence are insufficient to certify recoverable legitimacy when multiple provenance variants R share the same E. Under these map-class conditions, an independent provenance predicate P(H) is necessary. Genesis Pin is one sufficient and locally minimal implementation in the tested stack, but uniqueness is not proven.

The practical compression is:

```text
State is not history.
Geometry-like form is not provenance.
Visible equivalence is not legitimacy.
Ω-like equivalence is not legitimacy.
Recoverable legitimacy requires independent provenance.
```

## Evidence Chain

| Version | Test | Result | Status |
|---|---|---|---|
| V1001 | Geometry–Legitimacy Split | High geometry similarity counterfeits rejected by provenance. | Supported |
| V1002 | Full Up-Chain Certification | Visible-only and geometry-only accepted broadly; full certification accepted only pinned provenance. | Supported |
| V1003 | Independent Counterfeit Stress | 250/250 counterfeits passed geometry-only; 0/250 passed full certification. | Report-out gate passed |
| V1005 | Genesis Pin Minimality Ablation | Removing any single component allowed invalid histories through. | Local minimality supported |
| V1006 | Formal Finite History Space | S+Ω classes were ambiguous; P(H) separated legitimacy exactly. | Finite formal model supported |
| V1007 | Generalized Non-Injectivity Lemma | 20 finite configs preserved S+Ω underdetermination; full P(H) eliminated invalid certification. | Constructive lemma supported |
| V1008 | Map-Class Theorem Draft | If H=E×R and S,Ω depend only on E, S+Ω cannot certify R-legitimacy. | Theorem draft |
| V1009 | Necessity vs Specificity | Independent provenance is necessary; Genesis Pin is sufficient but not proven unique. | Claim boundary hardened |

## Theorem-Candidate Statement

Let:

```text
H = E × R
```

where:

```text
E = event/order structure
R = provenance metadata
S(H) = terminal visible observable
Ω(H) = geometry-like response/accessibility field
P(H) = recoverable provenance predicate
```

If:

```text
S(H) and Ω(H) depend only on E,
and at least two provenance variants in R share the same E,
and P distinguishes one as legitimate and another as illegitimate,
```

then:

```text
No certifier depending only on S(H)+Ω(H) can certify recoverable legitimacy.
```

Therefore:

```text
An independent provenance predicate P(H) is necessary.
```

## Genesis Pin Status

The Genesis Pin predicate tested here includes:

```text
pinned registry
pinned root
witness quorum
append-only continuity
non-circular origin
```

Current status:

```text
sufficient in tested stack: yes
locally minimal against tested attacks: yes
globally unique: not proven
production cryptography: not claimed
```

## What Is Proven Inside the Tested Stack

- **Proven inside tested stack:** Visible terminal equivalence is insufficient for legitimacy.
- **Proven inside tested stack:** Geometry-like Ω equivalence is insufficient for legitimacy.
- **Proven inside tested stack:** Independent provenance predicate P(H) separates legitimate from illegitimate histories when S+Ω are underdetermined.

## What Is Supported but Not Universal

- **Supported, not universal:** Genesis Pin is locally minimal against the tested attack family.
- **Supported, not unique:** Genesis Pin is a sufficient provenance predicate in the tested stack.

## What Is Not Proven / Not Claimed

- **Not proven:** Genesis Pin is the only possible provenance predicate.
- **Not claimed:** Physical spacetime, GR, Einstein equations, ADM constraints, physical curvature, or production cryptographic security.

## Clean Public Claim

```text
State is not history. Geometry-like form is not provenance. In this tested recoverability stack, visible and Ω-like equivalence can be counterfeited; full legitimacy requires independent recoverable provenance.
```

## Scientific Meaning

The important result is not merely that counterfeits fail a checklist.

The deeper result is that when the observable geometry layer and the provenance layer are factorized, geometry-like agreement cannot carry source legitimacy by itself.

That makes the bridge sharper:

```text
form-equivalence ≠ source-equivalence
```

## Next Research Track

1. External replication of V1003–V1007.
2. Formal proof polishing for the map-class theorem.
3. Alternative provenance predicate comparison beyond Genesis Pin.
4. Adversarial search over non-factorized cases where S or Ω partially leak provenance.
5. Threshold sensitivity and robustness audits.

## Stop Point

This is the correct stopping/report-out point for the current chain.

The next work should be replication, formal polishing, and adversarial expansion — not more version-chasing without a new proof obligation.
