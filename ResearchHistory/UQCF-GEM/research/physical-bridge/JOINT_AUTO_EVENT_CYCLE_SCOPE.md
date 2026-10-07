# Joint automatic event-cycle scope

Date: 2026-10-06 (America/Phoenix).
Status: PROSPECTIVE ANALYTICAL SCOPE.

Parents:
- AUTO_COVER_HANDOFF_CLOSEOUT.md at e13f829e5bef68d8558d355300ec07b18f53d8b6.
- AUTO_LOWER_WITNESS_CLOSEOUT.md at 371f999d7dd0ef894f29b2bd104d6f4bc75969a5.

## Objective

Combine automatic lower-witness edges with floor/upper protection and determine whether the retained endpoint event graph can cycle even when both exact endpoints are protected.

Exhibit the smallest exact counterexample if possible, and distinguish selected endpoint-certificate failure from native connectivity.

## Carrier

Palette P={x,y,z,w}.

Three labelled roots, all original floors1:
    r1={x}
    r2={y}
    r3={z}

Exact target:
    r1*={y}
    r2*={x}
    r3*={z}

Source and target both have tau=3.

Endpoint-only events:
    A1=A(r1,y)
    D1=D(r1,x)
    A2=A(r2,x)
    D2=D(r2,y).

r3 is unchanged.

Use common upper cover H={x,y,z}; tau<=4 is structurally harmless, so no nontrivial upper handoff is required.

## Required automatic lower selections

For Kx={x,z}:
- old witness r2 at source;
- new witness r1 at target.
Derive
    D1 -> rho_x -> A2.

For Ky={y,z}:
- old witness r1 at source;
- new witness r2 at target.
Derive
    D2 -> rho_y -> A1.

Other pairs may use permanent witnesses or add edges, but must not remove this cycle.

## Floor edges

Because r1,r2 are floor-saturated singleton sources and singleton targets, endpoint-only floor safety requires
    A1 -> D1
    A2 -> D2.

Prove combined cycle:
    A1 -> D1 -> rho_x -> A2 -> D2 -> rho_y -> A1.

Therefore the selected automatic endpoint event certificate is cyclic and admits no topological execution.

## Native bypass

Prove the following native path using temporary label w stays at tau=3 and floors1:

1. Add w to r1.
2. Delete x from r1.
3. Add x to r2.
4. Delete y from r2.
5. Add y to r1.
6. Delete w from r1.

This reaches the exact target.

Thus the joint endpoint-only certificate cycle is not native disconnection; a temporary off-endpoint incidence changes the witness/capacity structure.

## Boundaries

Do not claim every endpoint-only path is impossible unless separately proved. The primary theorem is selected-certificate cyclicity. If endpoint-only impossibility follows directly for this carrier, prove it explicitly and scope it.

Do not infer physical meaning.

## Next frontier

Characterize what temporary incidence provides. Candidate interpretation: it supplies one unit of temporary floor capacity and a temporary witness identity, breaking the alternating floor/lower-witness cycle.

Seek a theorem for cycle-breaking auxiliary capacity without treating the temporary label as a physical primitive.
