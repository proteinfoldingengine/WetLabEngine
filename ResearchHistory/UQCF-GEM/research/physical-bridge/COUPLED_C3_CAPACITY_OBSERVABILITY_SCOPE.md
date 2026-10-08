# C3 capacity-bit observability — prospective theorem-first scope

Date: 2026-10-07.
Status: FROZEN PROSPECTIVE SCOPE; not certified.

Parent bounded hidden-capacity closeout: COUPLED_C3_HIDDEN_OPTIMALITY_CLOSEOUT.md at 4c134d9b904eac92653c564b6e0299accab5b702.

## Goal

Determine exactly whether b=1[Z nonempty], required for shortest protected repair in the hidden-spectator family, can be derived from existing native quantities rather than posited as a new physical primitive.

## Frozen family

E(Z)=({a,b},{b,c},{a,c},{d,e} union Z)
C(Z)=({b,d},{b,c},{c,d},{a,e} union Z),
all original floors2, protected 3<=tau<=4, Z disjoint from a,b,c,d,e,w and invariant under repair. R is the restricted retained core projection from the parent result and omits full root sizes and spectator counts.

## Distinguish three information interfaces

I0: only R; no full root sizes, hidden spectator reads, or query oracle.
I1: R plus an EXISTING native floor slack value sigma4=|E4|-f4, if that value is independently justified as retained.
I2: R plus a nondestructive native legality query L(E,-d(r4)) evaluating whether this hypothetical primitive would respect floor and band. Do not assume such a query exists or is accessible unless explicitly declared.

## Required analytical theorem

1. Show sigma4=|Z| and b=1[sigma4>=1].
2. Show exact native legality of -d(r4) at source is equivalent to b=1, including the hitting-number check.
3. Prove R alone cannot compute b (indistinguishable empty and nonempty Z), and therefore cannot select shortest repair uniformly.
4. Prove I1 or I2 suffices to select shortest path if, and ONLY if, that observable is genuinely provided. State explicitly that computing it from full hidden incidence data is not observer-independent.
5. Distinguish checking a hypothetical edit from executing it. The latter is not a harmless query and is illegal for empty Z.
6. Establish a one-bit information lower bound only within this two-policy family; do not claim a general observer-access theorem, Shannon law, physical force, geometry, or fundamental time.
7. Supply countercontrols: same R but opposite b, legality query cannot be replaced by checking tau alone, and a hypothetical oracle cannot be silently smuggled into I0.

## Scientific stop condition

If the current native framework has no previously derived access to sigma4 or a nondestructive legality query, report a precise observability obstruction, not a new primitive or claimed derivation.

No numerical campaign is authorized. Publish immutable proof, audit, and request independent mathematical criticism before any scoped closeout.
