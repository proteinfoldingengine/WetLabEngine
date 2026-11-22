# An event-defined receiver and a source-amplitude grade contrast

On the fixed nine-site example, an exact completion criterion determines B's retained carrier without using palette rank. Under a frozen donor carrier, retention of B's old nonroot junction and minimum total incidence, the same B root grade is

    R_B(g) = g0 + (q0 - 1) g8,       q0 in {1,2}.

Thus the high-minus-low response is the original source amount g8. This is a conditional mathematical result about an existing source representation. **The completion criterion is not an inherited physical selection law.** There is no new common-field response or derived B-owned measurement.

## 1. Event roles without a palette order

Use the already-published fixed-donor source, P=(-1,0,1,2,3,3,2,1,0), source leaf s=v8 and other root child j=v1. The typed event is the original v16.26 atomic deletion with its before family, after family and actor index D:

| Arm | Before -D(v8) | After |
|---|---|---|
| high, AD | [257,63,199,319] | [257,63,199,63] |
| low, CD | [1,63,455,319] | [1,63,455,63] |

For a typed event e, define T(e) as the indices other than its actor whose BEFORE carrier equals the actor's AFTER carrier. In both arms T(e)={B}. The entire initial B and D views and grades agree between the arms for a fixed ambient g. The source loss is g8(delta8-delta0) in each event.

T(e) is a mathematical relation on fields the existing atomic certificate already contains. Under any permutation of view labels or rooted-vertex isomorphism, set equality and the actor exclusion transform with those labels, so T(e) transforms covariantly. No ordering choice or source-grade read is needed to name this candidate. All 24 view permutations in both arms are checked. In the unmarked AFTER state, B and D are identical, and swapping them is an automorphism; the marked event distinguishes the actor from its untouched twin.

This is addressability, not an instruction to send anything to T(e). The inspected v16.48 normalize accepts state, degrees, k and q; it does not consume that event identity. v16.27's attribution and v16.28's deletion-precedence routines likewise do not route to this twin. Naming it does not by itself remove the delivery gap.

## 2. The exact completion contract

Let S_v be the set of indices whose views contain vertex v. A state is a four-view prefix-closed cover of all nine sites, with all four indices at the root. Let tau_v be the minimum number of views covering the children of v. The native hitting calculation at the source AFTER state gives the internal profile

    q_high=(2,1,2,1),   q_low=(1,1,2,1)

at vertices 0,1,2,3; all other entries are zero.

Consider all completions subject to:

1. The donor's post-event carrier stays exactly D=63.
2. The event-defined candidate B retains j=v1.
3. The rooted union and the appropriate entire profile remain unchanged.
4. The endpoint has the least possible total incidence N=sum_v |S_v| among states satisfying 1–3.

For the displayed paths, conditions 1–3 hold at EVERY step. A and C are unrestricted within the native grammar. Condition 4 is an endpoint objective, not a requirement of monotone deletion or shortest execution. No canonical positional order is imposed.

These are **SUPPLIED completion conditions** when interpreted dynamically. The compact-palette theorem and software are inherited mathematics and prove normalization to an ordered canonical endpoint, with a profile-excursion bound. They do not mandate a physical minimum-incidence endpoint, frozen donor or retained B junction. Existence of those older compact constructions is not evidence that this new completion contract is automatically enacted.

## 3. Equality in a native counting bound forces the receiver

Every admitted state has four root incidences and at least one at each of eight nonroot sites, giving N>=12. The profile entry tau_2=2 means the supports of children v3 and v6 are disjoint and nonempty. Therefore |S2|>=2; prefix closure implies |S1|>=2 as well. Both exceed their already counted minimum by one, so

    N >= 4 + 8 + 1 + 1 = 14.                       (1)

At equality, all nonroot sites other than v1,v2 have exactly one holder, and S1,S2 each have exactly two. Since D=63 and B(v1) is retained,

    S1 = S2 = {B,D}.
    S3 = S4 = S5 = {D}.
    S6 = S7 = {B}.                                (2)

Indeed D holds v3,v4,v5 already. It does not hold v6,v7, so nesting, singleton support and (2) force their holder to be B. The root condition then determines the source leaf:

- For q0=1, S1 and S8 must intersect. Since D does not hold v8, its unique holder is B.
- For q0=2, S1 and S8 are disjoint. The unique v8 holder is A or C, never B.

Hence EVERY minimum completion has B=455 in the low arm and B=199 in the high arm. The exact complete minimum sets are

    high: [257,199,1,63] and [1,199,257,63];
    low:  [1,455,1,63].

They all have N=14, proving attainability and sharpness of (1). This is an exhaustive algebraic equality characterization for the declared nine-site domain, not a conjecture extrapolated from counts. B is determined even though the high endpoint's source-holder choice need not be unique. The conclusion is invariant under renaming the marked event roles.

If B is forbidden to acquire v7, its existing junction, D, and the distinct v7 holder all occur at v1. Thus |S1|>=3, which raises (1) to N>=15. The original four-deletion path below attains 15. The additional incidence is the exact cost of this kind of B blindness under the other stated constraints. This refers to support storage, not physical energy.

## 4. Constructive paths and the unchanged native deletion alternative

Write +/-i(v) for one native incidence edit. Starting at the high AFTER state, use

    -B(v5), -B(v4), -B(v3),
    +B(v6), -C(v6), +B(v7), -C(v7),
    -C(v2), -C(v1).

The endpoint is [257,199,1,63]. For the low state, insert +B(v8),-C(v8) before the final two deletions, reaching [1,455,1,63]. These are respectively nine and eleven legal edits. At every state the entire profile is exact, D=63, and B(v1) remains. They are explicit constructed paths in the inherited move relation, not outputs of an existing caller implementing the contract.

The complete state enumeration below finds shortest distances 9 and 11 to a minimum. The paths attain the coordinate Hamming lower bounds: seven deletions/two additions in the high path, eight deletions/three additions in the low path. The second high minimum is at distance 11. Reaching a minimum requires additions; a deletion-only path cannot deliver either missing source leaf or remote leaf to B.

There is also an already implemented blind alternative. Original v16.26 factor, given the endpoint with B=3, deletes B(v5), B(v4), B(v3), B(v2). It leaves A,C,D fixed, keeps B's junction, and stays exactly at q in BOTH arms. Endpoints are [257,3,199,63] and [1,3,455,63], both of incidence 15. B's source root remains g0+g8. This path carries neither the old remote split delta7-delta1 nor the new source split delta8-delta0 into B. It is ordinary P1 contraction, not a proposed averaging or alternative grade law.

The two retention conditions are substantive:
- Dropping B-junction retention permits one more B(v1) deletion, giving high [257,1,199,63] at N=14 with no B acquisition.
- Dropping donor freezing permits those five deletions on D instead, giving high [257,63,199,1] at N=14 while B is unchanged.

Each is an exact-profile native path retaining the other condition. These are controls on the new implication. They do not refute the earlier ordered normalizer or show that the source event cannot be associated with a physical process.

## 5. The original source amount, not an inserted gain

Use the already-reviewed conservative compatible grade continuation: unedited grades stay fixed, each changed grade preserves its coarse marginal, and the source family remains compatible. It stays the P1 marginals of a single common ambient g. These are supplied associations to live support edits; the existing support routine does not store or pass a grade.

B=199 retains v1 but not v8. Its root fiber is {v0,v8}, so b0=g0+g8. B=455 retains both root children, so its root fiber is {v0}, giving b0=g0. This proves

    R_high(g) - R_low(g) = g8                      (3)

for every formal rational source g. The coefficient is fixed by native P1, not fitted. The same initial B=63 has root grade g0+g8 in both arms. With unit grade, this fixed existing root reads 2 high and 1 low. A zero source amount gives zero scalar contrast; a negative source amount reverses its sign.

For an initially hidden source distinction take strictly positive grades

    g^(0)=2*1,   g^(1)=2*1+delta8-delta0.

Their complete initial B grades coincide because v8 retracts to v0. After the D event, D=63 is likewise blind. At every low minimum B alone retains v8, so its root grades are 2 and 1 and its v8 grades are 2 and 3. All other views become blind to that dipole. At either high minimum, B's root grades are 4 and 4, and A or C retains the dipole. This is a conditional source-to-receiver transfer of a preexisting distinction on the same native source representation.

The older v1 contrast -g7 disappears under this completion contract: both minimum B carriers contain v7 and have the same v1 source grade g1. The proposed structural condition changes the prediction rather than preserving a preferred earlier readout.

Equation (3) is a **source-grade read at the existing root**, not the root potential. In the usual grounded gauge the root potential is zero in every chart. Each fixed g has the same ambient source and common potential throughout its support edits, and both arms agree in their common field at that fixed g. Across g^(0) and g^(1), an ambient v8 potential difference already exists before acquisition; the low completion exposes it in B's expanded carrier. There is no generated common-field increment, mass calibration, physical force or gravity claim. Projecting both final B grades onto their literal common carrier also removes the newly exposed source split.

## 6. Complete verification and scope

The finite domain contains all admitted states with D=63, B(v1) retained, fixed full union and each stated profile. Per-view bitmask enumeration and independent per-vertex nested-support reconstruction give exactly the same identities:

| Domain | States | Minimum endpoints | All states reachable from the source AFTER state? |
|---|---:|---:|---|
| high | 77 | 2 | yes |
| low | 6377 | 1 | yes |

The unchanged v16.48 verifier independently checks every state's profile and the constructed paths. The producer and checker enumerate the complete domain, including the larger states and blind completions; the minimum endpoints are not preselected samples. Raw state identities, their digests, distances, exact paths, and grade outputs are preserved. All nine source basis vectors check the endpoint formula and all displayed positive/blind path-state source families against independent ancestral reconstruction. The 48 marked-event relabeling checks keep the same event-defined B; they are not executions of a new event router. Missing, duplicate, substituted and false-provenance records are rejected.

The current packet is mathematical support for the existing native acquisition candidate. It exchanges palette-dependent endpoint choice for explicit structural completion premises. It does not claim that the total physical assumption burden has decreased, that the complete atom selects a fresh versus internal controller call, or that the grade is B's accessible physical record. The earlier identical-internal-event countercontrol remains applicable.

Another bot is handling the unchanged-view-coverage premise reduction at PR153 comment7067193458. This result does not incorporate or certify it: the previous full-path conservative grade hypotheses are retained here.

The next native obligation is concrete: an existing event operation would need to preserve the donor and receiver anchor and select this minimum completion, or derive an equally strong receiver-forcing condition. A compatible grade update and a readable B-owned root would still need operational identification. The finite proof shows exactly what that completion would predict; it is not authorization to insert its selection law as a physical axiom without marking it.
