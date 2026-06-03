# V1019 Formal Proof Note

**Title:** Recoverable Legitimacy Under Observable Compression  
**Status:** formal theorem-candidate note

## Definitions

Let:

```text
H = E × R
```

where:

```text
E = event/order component of history
R = provenance component of history
```

Let:

```text
F(H) = (S(H), Ω(H))
```

be the observable/geometry map.

Let:

```text
P: H → {0,1}
```

be a recoverable-legitimacy predicate.

Let:

```text
C_F: image(F) → {0,1}
```

be a certifier that uses only the observable value `F`.

## Proposition

```text
If H=E×R, F(e,r)=F(e,r') for at least one e and distinct provenance variants r,r', and P(e,r)≠P(e,r'), then no certifier C_F depending only on F can both accept the legitimate history and reject the illegitimate history.
```

## Proof

1. Let h1=(e,r) and h2=(e,r') with P(h1)=1 and P(h2)=0.
2. By the observable-compression assumption, F(h1)=F(h2).
3. Any certifier C_F using only F must assign C_F(F(h1))=C_F(F(h2)).
4. If C_F accepts h1, then it also accepts h2.
5. If C_F rejects h2, then it also rejects h1.
6. Therefore C_F cannot separate legitimacy over h1,h2.
7. Thus F-only certification is insufficient whenever legitimacy varies inside an F-equivalence class.

## Entropy Corollary

```text
If H(P|F)>0, then at least one F-equivalence class contains both legitimate and illegitimate histories; therefore F-only certification is underdetermined.
```

Equivalently:

```text
H(P | F) > 0  ⇒  F-only certification is underdetermined.
```

## Missing-Information Form

```text
I_missing = log2(|R_equivalence_class|)
```

If `I_missing > 0`, then the observable class contains unresolved provenance alternatives.

## Falsification / Boundary Condition

```text
The theorem does not apply if F injectively encodes all provenance information relevant to P, so that H(P|F)=0.
```

So the theorem is not:

```text
observables can never certify legitimacy
```

It is:

```text
compressed observables cannot certify legitimacy when they lose provenance-relevant information
```

## Genesis Pin Role

```text
Genesis Pin is a sufficient provenance-bearing predicate in the tested stack. V1012 supports targeted local minimality against the expanded adversarial family. Global uniqueness is not proven.
```

## Final Reviewer-Safe Claim

```text
Under observable compression, when provenance legitimacy varies inside an F=(S,Ω)
equivalence class, no F-only certifier can recover legitimacy. A provenance-bearing
information channel is required.
```
