# A11.X50 - block-stable cover relay and renewable copied handovers

Analytical parent: 24e610138407c402bc706bc52e61cc759e2f6e20.
Scope: be06bc3d9912e3469d0ff188e958658cc783222a.
Exact analytical candidate; no numerical execution or numbered certification.

## 1. Native domain and theorem

Fix a finite ordered palette P, labelled original root slots, and their SAME original positive floors. A primitive toggles ONE incidence in ONE slot. Larger intermediate supports are allowed. No labels, roots, floor amendments, simultaneous moves or compactness constraints are introduced.

Supply finitely many types t. A type specifies an ORDERED support pair (A_t,C_t); it is not defined only by its source. There are n_t>=1 original labelled copies of each type. Copy s has its own original floor a_(t,s)<=min(|A_t|,|C_t|). The actual source and destination are exact four.

Supply a type order sigma whose one-representative-per-type add-before-delete path is lower-safe at every primitive. Supply physical label sets K_minus,K_plus of size at most four with:
- K_minus hits every A_t;
- K_plus hits every C_t;
- U={t: K_plus misses A_t};
- V={t: K_minus misses C_t};
- every U type strictly precedes every V type in sigma.

**X50R (block-stable relay).** Process types in sigma order, copies within each type in their fixed labelled order, each copy by adding C_t minus A_t and then deleting A_t minus C_t in palette order. This complete ACTUAL path has 3<=tau<=4 at every primitive, respects every original floor, reaches the full labelled noncompact destination, and uses exactly the endpoint-toggle minimum. No upper joint mean, multiplicity bound, spare support or maximum-layer conversion is needed.

The essential additional conclusion beyond X48's single-root relay is a cover that hits BOTH A_t and C_t throughout every active type block. Thus it also covers simultaneously present old copies, new copies and the active enlarged support.

**X50F (derived infinite family).** For EVERY even m>=8, the alternating-window template of corrected X47 with arbitrary positive original labelled multiplicities n_J admits such a block-stable relay for the one-step cyclic rotation of singleton role labels. Original floors may be individually unequal positive values at most m-4, including complete saturation. The direct path reaches the exact labelled destination with the mathematical incidence minimum. Finite chains of rotations in the SAME or explicitly template-preserving cyclic order renew the mechanism at each restored endpoint. Counts are minimum per leg, not globally minimum for an arbitrary chain.

## 2. Coexistence cover derived from the strict relay

If V is empty, K_minus hits every source and destination support. Use it throughout. If U is empty, K_plus hits every source and destination support. Use it throughout. This also covers the case both are empty.

Otherwise let v0 be the first V type in sigma. For any block t strictly before v0 use K_minus:
- no previously completed type is in V, so its destination support is hit;
- every later source support is hit;
- the active type t is not in V, so BOTH A_t and C_t are hit.

For block v0 and every later block use K_plus:
- every U type strictly precedes v0 and has fully completed;
- every completed destination support is hit;
- neither the active type nor a later type is in U, so the active A_t and all later source supports are hit;
- every C_t is hit, including the active one.

These facts prove a physical four-cover of the full tuple with BOTH active endpoint constraints at every type block. No independent copy capacity is allocated: the same set hits any positive number of identical old/new supports simultaneously. At every primitive the active copy contains A_t during additions and C_t during deletions. All other active-type copies equal one of these supports. The cited set therefore hits every actual root. The switch between covers occurs after an entire earlier block and requires no incidence primitive.

Strict precedence is important. If U and V overlap, this certificate is impossible. Mere coverage of the adjacent type prefixes was insufficient in X49; here neither cover is asked to ignore an old or new active copy.

## 3. Actual lower witnesses, floors and next edits

At any primitive inside a type block, take the active copy as the representative of that type and one actual copy of each other type. Previously completed types use C_t; later types use A_t. This representative tuple is exactly the corresponding state on the supplied lower-safe type path. Every physical pair is missed by an actual representative support. That support is one of the original labelled roots, so additional copies cannot erase it. This is a witness argument for tau>=3, not an upper monotonicity claim.

A completed copy may be chosen instead when a block has just finished. At a block boundary every active-type copy is at its same endpoint. Thus every state, including phase and block boundaries, has an actual avoiding witness for every pair. With palette size at least four, excluding all two-label hitting sets excludes smaller hitting sets as well.

For each active copy the absent C_t minus A_t additions and present A_t minus C_t deletions are literal eligible primitives. Common incidences remain fixed. During additions size is at least |A_t|; during deletions at least |C_t|. Hence each individual floor a_(t,s) is retained, including saturation. The chosen next copy and type exist until the finite lists end; no arbitrary-safe-prefix extension is asserted.

Termination uses the finite lexicographic schedule of type index, copy index and edit-list index, equivalently the decreasing total count of pending scheduled edits. Zero-edit copies require no primitive and are simply advanced. Completion restores every original destination support with its own label. The total is
    sum_t n_t |A_t symmetric-difference C_t|,
the unavoidable number of endpoint-differing incidences. Thus it is minimum. The upper argument adds no primitive and changes no type order.

## 4. Alternating family and the lower-safe TYPE order

Let G have m even cyclic roles, m>=8, each with singleton label x_t. Put W_t={t,t+1,t+2,t+3}, indices modulo m. Let H_alt consist of the even-start windows. For each four-set J not in H_alt declare n_J>=1 original labelled roots of type Q_J=G minus J. At the source the physical support is {x_t:t in Q_J}. At destination x_t has role t+1. All roots have size m-4.

Positive multiplicities do not change hitting sets at either endpoint. Corrected X47 proves exact four for the one-copy template, the exact cover family H_alt, and minimum TYPE pair redundancy
    rho_type=C(m-2,2)-2>=m-2.
The quotient is an analytical witness selection from existing slots, not deletion or addition of physical roots.

X40L's strict bound holds on the one-copy template:
    C(2 rho_type,rho_type)>=C(2m-4,m-2)
        >=C(2m-4,2)>m(m-3)/2.
The last difference is (3m^2-15m+20)/2>0. X40L supplies a deterministic lower-safe TYPE order and its one-cycle add-before-delete path. Its domain matches: same template, singleton equal corresponding groups, original positive floors at most m-4, exact four, fixed carrier and one-label primitives. Use floor m-4 in this analytical type certificate; every actual copy floor is at most it.

The incorrect-owner graph is one full directed m-cycle. The type path makes exactly this handover. No arbitrary original-copy order is claimed lower-safe or block-compatible.

## 5. Forced block relay on that SAME lower-safe order

Restrict the supplied total TYPE order to odd-window complementary types
    R_j=Q_(W_(2j+1)), j modulo m/2.
There is a cyclic ascent: for some j, R_(j-1) precedes R_j. Otherwise all cyclic successive inequalities would be strictly descending, impossible in a finite total order.

Set t=2j and use the actual physical four-sets
    K_minus={x_s:s in W_t},
    K_plus={x_s:s in W_(t-1)}.
As proved in X48:
- K_minus covers all source types and misses exactly destination type Q_(W_(t+1));
- K_plus covers all destination types and misses exactly source type Q_(W_(t-1)).
The equality test is that a four-role set I misses G minus J exactly when I=J. Destination roles shift by one.

Thus U={R_(j-1)}, V={R_j}, with U strictly before V on the SAME X40L order. X50R now supplies the previously missing coexistence covers. Completing each entire copy block enforces all original U copies before every original V copy by construction. No cyclic ascent is asserted for an arbitrary original-copy order, and no assumption that X40L can satisfy arbitrary imposed precedences is used.

This proves X50F for arbitrary positive n_J, not only equal d. The lower theorem is applied BEFORE copying; its actual representatives lift at every primitive. The stronger upper certificate is independently derived rather than inferred from type-prefix covers.

## 6. Renewal and scientific meaning

After one full rotation the singleton role partition, masks, root sizes and original floors are restored. The same template has the same type redundancy and alternating cover structure. For every finite next leg in the same declared cyclic order, reconstruct the X40L type order and its forced cyclic ascent, then process its original copy blocks. Template-preserving automorphic orders work by carrying the same masks/windows/exception identities through the automorphism. Arbitrary reorderings that fail to preserve this structure are not included.

Each finite leg completes and leaves its inputs renewed. Protection may sit at level three inside a leg; no exact-four reset after each copy is necessary. Exact four is restored at every supplied leg endpoint. A finite chain therefore terminates and restores its exact labelled final destination. Per-leg minima do not imply an outer-endpoint global minimum.

The advance removes the n_J=1 restriction of X48F and DISCHARGES X49Q's additional coexistence-cover hypothesis for this structural family. It does not reinstate X49's withdrawn unconditional lift: generic type-prefix covers still need not protect simultaneous A_t and C_t copies. A strict ordered two-cover relay does.

The family remains at beta=m/2, with empty X45 same-representative intersection and singleton groups. Uniform d copies have Gamma=d*m/2. Arbitrary copies alter Gamma but not beta or the cover family. The original saturated case has no support-floor reserve. Native symmetry connectivity was already supplied by L and complete lower-path conversion by X40L plus A; the new result is direct band repair with a block schedule and the incidence minimum, not new connectivity or disconnection.

## 7. Limits, dependencies and remaining obligation

Frozen dependencies at analytical parent:
- A11_X40_SPARSE_WITNESS_RENEWAL.md: X40L, conditional eligible type choices, actual pairs, floors and full cycle completion;
- A11_X47_REDUNDANCY_ORBIT_OBSTRUCTION_CORRECTED.md: exact alternating covers, type redundancy, singleton cycle and prior method limits;
- A11_X48_MIXED_PREFIX_COVER_RELAY.md: exception identities and forced TYPE ascent;
- A11_X49_JOINT_RELAY_POTENTIAL.md: lower copy lift and correctly rejected generic upper lift.

No source is rewritten or recertified. Maximum-layer A is NOT invoked on this direct path. No new independent averaging principle, efficiency bound or executed benchmark is asserted.

Remaining: a block-stable multi-cover relay with more than two witness stages, or economical joint structural conditions when no such ordered exception separation is available. Arbitrary unequal role counts/accessibility, below-X40 lower protection, unrestricted mixed-floor/directed/higher-target/nested claims remain open. Failed relay conditions are method failures, not no-path certificates.

No numerical execution, implementation, workflow, integration merge, numbered certification, literature-originality or physical claim. Preserve v16.55/v16.54 and original evidence. Separate efficiency runner/fixtures/benchmarks remains unstarted and independently scoped.
