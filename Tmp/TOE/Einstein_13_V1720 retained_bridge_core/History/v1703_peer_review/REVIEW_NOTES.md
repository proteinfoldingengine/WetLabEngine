# V1703 L3 Arc — Work Product for AI Peer Review

This package contains the executable scripts and captured outputs from a session
that (a) closed Pillar 3 (ADM/H–H) negative, and (b) opened a forward arc on L3
(third-order retained structure). It includes my own critique, because the most
important findings here are about *which results are load-bearing and which are
near-tautological*. A reviewer should attack those classifications.

## Reproduction

All scripts are deterministic (seeded numpy, no external data). Run:
```
python3 v1703_L3_real.py
python3 v1703_1_L3_transport.py
python3 v1703_2_assoc_faith.py
```
Captured outputs are in the matching `*_OUTPUT.txt` files. Earlier-stage scripts
(v1701_*, v1702_*) are included for chain-of-custody but are not the focus.

## The algebra (shared primitives)

- `roll_kernel(x,y) = roll(x,1)*y - x*roll(y,1)` — non-associative kernel.
- `op_global(x,y,g) = x + y + g*roll_kernel(x,y)` — retained product (gamma=0.17).
- `associator3(a,b,c,g) = op(op(a,b),c) - op(a,op(b,c))` — genuine associator.
- Branches: columns of QR of a random matrix (orthonormal), dim=12, 4 branches.
- Atlas (from V1698): 7 random orthonormal chart frames, sparse edge graph,
  transitions T_ij = frames[j]^T frames[i].

## Findings, ranked by how load-bearing they are

### FINDING 1 (LOAD-BEARING, can fail, did not): L3 is irreducible. [v1703_L3_real.py]
The third-order associator field is NOT reducible to branch + pairwise structure.
- Capture by lower-order span: mean 0.736 (< 0.90 closure threshold).
- Rank lift: rank(lower)=10, rank(lower+O3)=12, **lift = +2 (exact integer)**.
The rank lift is basis-independent and is the strongest evidence: there are
provably 2 dimensions in the associator span orthogonal to all lower-order
structure. This is a real algebraic property of the non-associative product.

SELF-CRITIQUE to attack: the random control returns capture=1.0000 (a random
target is fully captured by a random same-size span because dim=12 < span size).
So "capture < 0.90" is partly a statement that the associators are *structured*
(sub-random), not purely that they are irreducible. The rank lift is the clean
evidence; the capture fraction is corroborating but weaker than it looks.
Reviewer should check: does the +2 lift persist at other dim / n_branch / gamma?

### FINDING 2 (EXPECTED, mildly informative): product is globally well-defined. [v1703_2]
Associators computed with each chart's LOCAL pullback product transport faithfully
(residual 2.6e-15); a genuine gamma change at the destination breaks it (null
7.4e-3, ~13 orders separation). The gamma-null failing shows global consistency is
gamma-specific, not automatic.

SELF-CRITIQUE (important): this is close to a construction identity. local_op is a
pullback of the SAME global op through frames; transporting it telescopes
(frames[j]^T frames[i] · frames[i]^T = frames[j]^T). Both sides reduce to the same
global associator in frame j, so agreement is largely forced. What is genuinely
shown: the product is globally single-valued and gamma-sensitive. What is NOT
shown: anything L3-specific — any fixed function of the global product transports
identically.

### FINDING 3 (NEAR-TAUTOLOGICAL — flagged, not relied upon): L3 "transports". [v1703_1]
Fixed L3 subspace vectors transport at 1e-15, scramble-null fails at ~1.8.
This is a pure linear-algebra identity for ANY fixed subspace. Included for
completeness and as a cautionary example. It does NOT establish that L3 is
"global" in any special sense. DO NOT cite Finding 3 as evidence of L3 structure.

## Structural caveat the reviewer should weigh

The atlas-transport test family (Findings 2 and 3) is, by its construction,
**incapable of failing for a fixed global object**, because the atlas is built from
consistent orthonormal frames and every global object pulls back consistently. The
only perturbations that break these tests change the global object itself
(scrambled transitions, changed gamma). Therefore "transports faithfully across the
atlas" should be treated as a consistency check, NOT as discovery of global
structure. The one result that survives this critique is Finding 1 (irreducibility,
via rank lift).

## What is NOT claimed

- No connection to ADM/Dirac H–H closure. That was tested separately (v1701_18,
  v1701_19, v1702_2) and is NEGATIVE: the scalar-scalar commutator has <1–2%
  per-operator overlap with any pre-registered momentum family.
- No physics. This is finite-dimensional non-associative algebra over R^12.
- No continuum limit, no time, no claim about nature.

## The only remaining test that can fail on L3 specifically

A holonomy-of-associator test: define third-order structure by a procedure that
accumulates around atlas loops where chart-local operation ORDER matters, so
non-associativity can produce genuine path-dependence. If path-dependent → real
cohomological L3 obstruction. If it closes → L3 is trivializable. This is NOT yet
run. Every atlas-transport test run so far cannot fail for a fixed object; this one
could. Recommended as the next step if the arc continues.

## Requested review focus

1. Is the +2 rank lift (Finding 1) robust to dim, n_branch, gamma? (the real claim)
2. Is my classification of Findings 2–3 as expected/tautological correct, or am I
   underselling them?
3. Is the proposed holonomy-of-associator test actually capable of failing, or does
   it also hide a construction identity?
