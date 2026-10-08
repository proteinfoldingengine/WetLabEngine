# C3 retained-interface source audit: full miss-count can recover capacity bit, core quotient cannot

Date: 2026-10-07.
Status: AUTHOR-SIDE ANALYTICAL SOURCE AUDIT CANDIDATE / NOT INDEPENDENTLY ACCEPTED.
Frozen scope COUPLED_C3_NATIVE_INTERFACE_SCOPE.md at 9e762fc7cf0354c3f5bf48e2a4cf4c79fe5d1e0e.

## 1. What was actually inspected

The existing research-branch publications were read directly:
- POST_A12_DYNAMIC_RESIDUAL_RESULT.md, immutable source d1aeaeba5ddb6a6748a5a80cb69d5ab76fdf8db7.
- POST_A12_RICHER_FACTORIZATION_RESULT.md, immutable source eee9eba17ec2f272949051dcd7533e4424ab33f3.
- JOINT_RETAINED_RESULT.md, immutable source 6454074a95b526bf2125272f76bfad392e2f468f.
- PRECEDENCE_INTERFACE_RESULT.md, immutable source 00a58b1b3d9d6b1c0c190995a18c5d5e5d19cd40.
- COUPLED_C3_CAPACITY_OBSERVABILITY_RESULT.md, immutable source 7b567d4b22dbc968f60ddcaa7a04fced941ba490.

The GitHub default-branch search does not cover this research branch. The statements here derive from direct branch-file retrieval, not from an exhaustive repository-wide absence search.

## 2. The core-only quotient cannot recover b

In the C3 family, E(Z)=({a,b},{b,c},{a,c},{d,e} union Z), with hidden Z subset T disjoint from core {a,b,c,d,e} and fresh w. Floors all2.

The retained core projection R from the closed hidden-optimality theorem is identical for every Z. A core-only miss-count M_core(H), H subseteq {a,b,c,d,e}, also cannot distinguish Z: every spectator is disjoint from every core H, so for each root and H the miss indicator depends only on the core support.

A labelled core mismatch record Q or address record D likewise does not encode Z if defined only on the unchanged core endpoints. The original floor vector is (2,2,2,2) for every Z. Therefore the combined core-only record (R,M_core,Q,D,f) is identical at Z=empty and Z={z}, but b=1[Z nonempty] differs.

This is a concrete indistinguishability result for the specified core-only fields, not a claim about every possible native retained field.

## 3. A PREVIOUSLY PUBLISHED full-palette miss-count field CAN recover b

The dynamic residual theorem defines for a declared residual family Rset and every nonempty H subseteq full palette P, |H|<=4:
    M_Rset(H)=#{r in Rset: S_r intersect H=empty}.

Instantiate its residual family as the SINGLE named fourth root r4 (the first three are explicitly controlled), so N_Rset=1. For every spectator label z in the declared finite spectator palette T:
    M_Rset({z})=1 if z notin Z,
    M_Rset({z})=0 if z in Z.

Therefore
    b=1[Z nonempty]
      =1[exists z in T: M_Rset({z})=0]
      =1[sum_{z in T}(1-M_Rset({z}))>=1].

This is an exact derivation of b from the previously defined full-palette miss-count field, IF that field is actually retained for r4 and its spectator singleton coordinates.

An equivalent formula if ALL FOUR roots are placed in the residual family (and the first three never contain spectator labels) is:
    M_all({z})=4-1[z in Z],
    b=1[exists z in T: M_all({z})=3].

For T empty, the OR is false and b=0.

Thus the answer to 'does any already published mathematical retained certificate determine the bit?' is YES: full-palette singleton miss counts suffice. It is false to claim all prior retained mathematical interfaces are incapable of determining b.

## 4. Why this does NOT establish native observer access

The original dynamic-residual theorem explicitly says M_R is DERIVED information; it does not prove efficient initialization or observer accessibility. Its update law for a named residual edit assumes the active root's old/current support is supplied or retained.

Our extraction formula assumes:
- the full finite spectator palette T is declared and enumerable;
- singleton miss counts M_R({z}) are initialized and retained, not merely definable from hidden incidence data;
- the residual partition is fixed and known;
- if edits touch spectators or move the residual family, appropriate update information is available.

If an observer only has the core quotient R, it cannot conjure M_R({z}) from R. Computing these singleton coordinates from full hidden supports would itself be a forbidden undeclared full-state read unless an earlier native derivation supplies them.

In the exact hidden-Z family, spectator incidences remain invariant. Once initialized, their singleton miss counts are constant along the repair, so no repeated spectator read is required. This does NOT resolve the origin of their initial values.

The core-only joint-retained theorem and richer factorization deliberately hide Z and obtain LEGAL repair structurally. They do not claim optimal repair under the C3 floor2 criterion, so no contradiction arises.

## 5. Named active-root access and hypothetical legality

If r4's current support S4 and floor2 are supplied, the slack |S4|-2=|Z| is directly available at source. But that is explicit active-root support access, not a hidden-fiber quotient result.

A nondestructive hypothetical legality bit for -d(r4) also equals b in this family, as proved in the conditional capacity theorem, but the inspected retained-quotient interface does not establish a free legality oracle. The dynamic-residual theorem computes legality for DECLARED edits only when its required active-support information is supplied. It is not a mechanism for discovering a hidden root's unretained support.

## 6. Interface comparison

- Core R, core-only M_core, Q/D on core, original floors2: b NOT determined.
- Full-palette M_R singleton spectator coordinates with declared r4 residual: b exactly determined, conditional on initialization/retention.
- Explicit named r4 support/cardinality: b exactly determined, but exposes active-root information.
- Nondestructive hypothetical-edit legality query: b exactly determined, conditional on independently justified availability.
- Native observer-accessible derivation of any of those extra inputs from ordered events alone: NOT established by the inspected sources.

## 7. Precise next mathematical/physical bridge question

Can the full-palette singleton miss-count coordinates, or at least the aggregate OR bit b, be derived and initialized from already available ordered-event/retained-accessibility observables without inspecting hidden spectator supports?

If not, the result is an INITIALIZATION/OBSERVABILITY OBSTRUCTION, not a failure of the retained controller's legality.

Do not introduce a new observer bit or oracle to evade that gate. No physical force, geometry, energy, continuum, GR/ADM or fundamental time is inferred.

This is an author-side source audit, not a whole-repository negative theorem or independently certified result.
