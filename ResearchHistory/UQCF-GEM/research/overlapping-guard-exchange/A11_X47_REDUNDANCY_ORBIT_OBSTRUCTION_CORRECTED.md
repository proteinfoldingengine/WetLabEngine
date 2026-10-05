# A11.X47 — corrected authoritative rendering

Status: source-integrity correction of the accepted X47 theorem.
Mathematical parent and accepted result: 6414a606bba86712faa89222ef5f7d5203085acd.
Erratum scope: 541b1894e5462d20ebee59ab12aebee48d21b10d.

This file is the authoritative readable rendering of X47. It changes no mathematical claim. The historical file A11_X47_REDUNDANCY_ORBIT_OBSTRUCTION.md remains immutable evidence of a Markdown serialization failure and is superseded for reading by this file.

No numerical execution, implementation, benchmark or numbered certification.

## 1. Native carrier and notation

Fix a finite ordered palette P, labelled original roots and their SAME ORIGINAL positive floors a_i. One primitive toggles ONE incidence in ONE root. Larger temporary supports remain native. No label or root is added, no floor is weakened, and no simultaneous move, compactness, geometry or fundamental time is imposed.

Use the restored mask setting of X45-X46. Nonempty role groups partition P. The same nonempty actual masks Q_i are used at both restored endpoints, and each restored root is the union of the role groups indexed by its mask. Let H4 be the family of all four-role covers.

For a directed simple ownership cycle

    C = (c_0, ..., c_(ell-1)),

define cyclic four-windows

    W_t = {c_t, c_(t+1), c_(t+2), c_(t+3)}.

For each actual root i define

    B_i(C) = {t : W_t is disjoint from Q_i}.

Then define

    B(C) = union over i of B_i(C),
    beta(C) = |B(C)|,
    Gamma(C) = sum over i of |B_i(C)|.

All cycle indices are taken modulo ell.

## 2. Typed statements

**X47B — duplicate-insensitive bad-window theorem.**

B(C) is exactly the set of bad cyclic four-window starts. Therefore beta is the exact number of bad starts and

    beta(C) <= Gamma(C).

If

    beta(C) < ceil(ell/2),

then two cyclically consecutive windows cover every actual root. Thus X45's same-representative criterion holds for the cycle.

This is the sharp universal threshold using beta alone. For every even ell at least eight, equality beta = ell/2 can have alternating good and bad starts and no adjacent good pair. The exact adjacency test is stronger than the scalar bound. The bound is sufficient, not necessary.

**X47O — redundancy/orbit orthogonality family.**

For every even m at least eight and every integer d at least one, there is a saturated exact-four template on m singleton roles and a destination whose ownership graph is one directed m-cycle such that:

1. the only four-covers are the m/2 even-start cyclic four-windows;
2. the X45 same-representative intersection is empty for the prescribed and only ownership cycle;
3. beta = m/2 and Gamma = d m/2;
4. the exact minimum pair-witness redundancy is

       rho = d [C(m-2,2) - 2];

5. rho can grow without bound while the cover family, beta, ownership cycle and X45 obstruction remain unchanged;
6. accepted X40L nevertheless supplies a complete lower-protected endpoint path, and accepted maximum-layer Theorem A converts that complete path to a path with tau in {3,4} between the exact endpoints.

Therefore exact-four consistency and arbitrarily large raw pair redundancy do not force X46's strict gap condition or X45 representative compatibility. This is not native disconnection, not failure of every direct upper construction and not failure of a band path.

## 3. Exact bad-window quotient

A start t is bad exactly when at least one actual mask misses W_t. Equivalently,

    t belongs to union over i of B_i(C).

Thus beta is exact. The inequality beta <= Gamma is only the union bound. Duplicating a labelled root repeats one summand in Gamma but does not change the union B(C).

If beta < ceil(ell/2), the number of good starts is at least

    ell - ceil(ell/2) + 1 = floor(ell/2) + 1.

A subset of a cyclic ell-set with no adjacent positions has size at most floor(ell/2). Therefore two good starts t and t+1 exist.

For the forward cycle rotation pi(c_s) = c_(s+1),

    pi(W_t) = W_(t+1).

Both windows lie in H4. Hence W_t belongs to

    H4 intersect pi^(-1)(H4),

which is exactly X45's representative criterion.

The converse is false. At the boundary, bad starts may alternate and block adjacency; other arrangements at or above the boundary may still contain adjacent good starts. Therefore the strict beta inequality is the best guarantee obtainable from the scalar count alone, not an if-and-only-if condition.

## 4. Alternating-window construction and exact target

Let G be the cyclic group of m role positions, with m even and at least eight. Put

    W_t = {t, t+1, t+2, t+3}

and define H_alt to be the m/2 windows whose start t is even.

For every four-set J not in H_alt, declare d distinct labelled original roots with the same actual mask

    Q_(J,s) = G minus J,    1 <= s <= d.

There are no other roots. Every mask has width m-4. Give every labelled copy the saturated original floor m-4.

For any four-set I,

    I is disjoint from Q_(J,s)
    iff I is a subset of J
    iff I = J.

Thus I hits every declared root exactly when its complementary root was omitted, exactly when I belongs to H_alt. The complete four-cover family is H4 = H_alt.

It remains to exclude a smaller cover. Every three-set T has m-3, hence at least five, four-set extensions. A three-set is contained in at most two cyclic four-windows: if it fits in such a window, the possible starts are at most the two extensions of a consecutive triple; all other arrangements allow no more. Therefore at most two extensions of T lie in H_alt. Choose another extension J. Its declared complementary root Q_(J,s) misses T. Any smaller set extends to a three-set and is missed as well.

Hence the template transversal is exactly four.

The exact cover density is

    |H_alt| / C(m,4)
      = (m/2) / C(m,4)
      = 12 / [(m-1)(m-2)(m-3)],

which is below one half for every m at least eight and tends to zero.

## 5. Unique ownership cycle and empty upper intersection

Give every role one actual label x_t. At the destination send x_t from role t to role t+1. The incorrect-owner graph is exactly one directed simple m-cycle and has no alternative nontrivial simple cycle.

Let pi(t) = t+1. Pi maps every even-start window to an odd-start window. Odd-start windows do not belong to H_alt. Therefore

    H_alt intersect pi^(-1)(H_alt) = empty.

By X45C, no four same representatives from the declared one-per-role pool cover both restored endpoints for this prescribed cycle. Since the ownership graph has only this cycle, selecting another ownership cycle cannot repair the failure.

This is exactly a limitation of X45's representative lift. It does not exclude another four-label strategy, another direct upper construction or a native path.

The good starts are even and the bad starts are odd, so beta = m/2. A bad window W_t is missed by Q_(J,s) only if W_t is a subset of J, and because both have size four this requires J = W_t. Exactly its d labelled complementary roots miss it. No root misses a good window. Therefore

    Gamma = d m/2.

For d = 1, Gamma = beta = m/2. The strict X46/X47 bound fails at equality and no adjacent good starts exist. This proves sharpness. Increasing d leaves beta and the exact obstruction unchanged while making Gamma arbitrarily larger.

## 6. Exact pair redundancy

A root Q_(J,s) avoids a role pair K exactly when K is a subset of J. There are C(m-2,2) four-sets containing K. The omitted such sets are exactly the members of H_alt that contain K.

A pair lies in at most two even-start cyclic four-windows. Among all length-four windows containing a fixed pair, the possible starts form at most three consecutive cyclic positions, of which at most two are even. An adjacent pair in the appropriate parity position attains two. Therefore the minimum actual pair redundancy is exactly

    rho = d [C(m-2,2) - 2].

For d = 1,

    C(m-2,2) - 2 - (m-2)
      = (m-1)(m-6)/2
      >= 0.

Thus rho >= m-2. Central-binomial monotonicity and middle-term maximality give

    C(2 rho, rho)
      >= C(2m-4, m-2)
      >= C(2m-4, 2)
      > m(m-3)/2.

The final strict margin is

    [3m^2 - 15m + 20]/2 > 0

for m at least eight. Therefore accepted X40L applies.

## 7. Correct lower and upper conclusions

X40L supplies a complete path between the labelled exact endpoints with:

- actual pair witnesses at every primitive;
- tau at least three;
- literal add-before-delete edits;
- legality at the same original floors;
- eligible continuation and renewal;
- strict finite progress;
- full exact labelled and noncompact destination restoration.

This use of redundancy is substantive. X47 does not say redundancy is useless.

The empty X45 intersection means this argument does not provide the X40 event-minimum direct upper lift through the declared representative pool. Only after the complete lower-protected endpoint-to-endpoint path exists may accepted maximum-layer Theorem A be applied. It then supplies a path with

    3 <= tau <= 4

between the exact endpoints. The converted path need not preserve the preliminary schedule, event minimum or an unfinished waypoint. Failure of the representative lift and existence of a converted band path are distinct conclusions.

Certified theorem L also supplies connectivity for these symmetry endpoints.

## 8. Saturation and prior-method separations

All root sizes and floors equal m-4. The endpoints are completely saturated and have no root-floor reserve. Source and destination groups are singleton and have equal positive corresponding size.

- X38 does not apply because the unique nontrivial ownership cycle has length m at least eight.
- X39 does not apply because every mask has width m-4, less than m-3.
- X40U does not apply because all role groups are singleton. X40L is used only for the lower proof.
- X43 does not apply because its size premise would require 4 >= m-1.
- X44 does not apply because the exact cover density is below one half.
- X45 fails for the prescribed pool and only cycle because its exact intersection is empty.
- X46 fails because Gamma = d m/2 is not less than ceil(m/2) = m/2.

X41's singleton-root input is unavailable in every partition-union representation of the same endpoint. All role incidence profiles are distinct. For a not equal to b, among the C(m-2,3) four-sets containing a and not b, at most two lie in H_alt. Choose another J. Then Q_J omits a and contains b. Any representation cell must be profile-homogeneous, so distinct roles cannot merge. Every actual mask contains m-4, at least four, distinct profiles and cannot be one cell.

These are separations from sufficient methods, not no-path theorems.

## 9. Saturated controls

Four pairwise disjoint saturated supports would require

    4(m-4) > m

distinct palette incidences for m at least eight. Therefore four private floor-safe roots cannot fit.

The whole endpoint union is two-covered. Choose even t and labels x_t and x_(t+2). Their source/destination role footprints are

    {t,t+1} and {t+2,t+3}.

Together these footprints form W_t in H_alt, so the pair hits every root's source/destination union. Simultaneous whole-union preparation is unsafe.

Every root changes. If Q_J were invariant under the full rotation, its four-set complement J would be invariant. A nonempty invariant subset of a transitive m-cycle is all of G, impossible because |J| = 4 < m.

Again, these are controls on earlier constructions, not native disconnection.

## 10. Scientific conclusion and next obligation

Lower witness abundance and upper-cover organization are orthogonal. Pair redundancy counts actual roots missing each forbidden pair and can force complete reusable lower repair. Orbit-compatible upper transport asks how minimum four-covers are organized under the ownership permutation. Exact-four consistency does not couple these structures, and labelled duplication can amplify the former without changing the latter.

The duplicate-insensitive union beta is the correct exact scalar behind X46's union-bound step. The full adjacency pattern of good windows remains the exact X45 condition for this representative lift.

A stronger theorem must impose or derive a joint condition linking actual lower witnesses to transitions among actual four-covers, such as an overlap-corrected bad-window structure or cover-aware cycle selection. More raw witness count alone cannot close the gap.

No claim is made for arbitrary endpoint accessibility, unequal corresponding group sizes, below-X40 lower repair, failure of every possible direct upper strategy, native disconnection, unrestricted mixed-floor, directed, higher-target or nested universality, literature originality or physical interpretation.

No numerical execution, workflow, implementation, benchmark, integration merge or numbered certification is authorized. v16.55, v16.54, their frozen sources and all original evidence remain unchanged. The separately promised efficiency implementation, fixtures and benchmarks remain unstarted.
