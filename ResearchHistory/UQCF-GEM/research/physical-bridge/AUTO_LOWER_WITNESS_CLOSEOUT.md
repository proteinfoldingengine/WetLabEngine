# Automatic retained lower-witness handoff: scoped analytical closeout

Date: 2026-10-06 (America/Phoenix).
Disposition: ANALYTICALLY COMPLETE FOR ENDPOINT-ONLY LOWER PAIR-WITNESS HANDOFF.
Evidence: written mathematical proof with author-side audit and immutable readback.

## Immutable record

Scope:
- 5f9a109c68c9784b2a04c80e82a2ad3450a8c77a
- AUTO_LOWER_WITNESS_SCOPE.md

Result:
- ee25f0bc94ecef95b5e2c602258423be3e634b6a
- AUTO_LOWER_WITNESS_RESULT.md

Parent upper-cover closeout:
- e13f829e5bef68d8558d355300ec07b18f53d8b6

## Audit findings

1. Source/target tau>=3 guarantees at least one actual old/new witness for every physical pair K.
2. A selected new witness n_K has no target K-incidence, so every source K-incidence is source-only; deleting all of them before rho_K makes n_K actually miss K.
3. A selected old witness o_K has no source K-incidence, so every target K-incidence is destination-only; holding all such additions until after rho_K keeps o_K actual before handoff.
4. The new witness remains K-free after handoff because its exact target misses K.
5. Therefore every physical pair has an actual missed root after every event state and tau>=3.
6. Permanent endpoint-union witnesses need no marker.
7. The union over all K is acyclic by levels deletion -> pair marker -> addition.
8. This theorem deliberately does not certify floors or tau<=4; those channels can add opposite-direction edges.
9. Fiber-uniformity follows when the selected endpoint witness signatures are retained across the hidden fiber.
10. Symbolic controls cover permanent, one-deletion, two-deletion and multiple-destructive-addition cases.

No mathematical correction was required in this author-side audit.

## Advancement

The lower channel is now automatically derived and is the exact directional dual of the upper channel:

    upper: addition -> handoff -> deletion
    lower: deletion -> handoff -> addition.

The opposing directions make joint compatibility a real mathematical question rather than an assumed property.

## Next frontier

Combine lower, upper and floor edges in one event graph. A concrete saturated singleton-swap construction already indicates that a genuine joint event cycle is possible; that result must be frozen and proved separately.

No physical force, geometry, energy, observer field or fundamental time.
