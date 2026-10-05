# A11.X48 - mixed-prefix four-cover relay

Exact analytical candidate.
Scope commit: d110a59831940ee14cec994ca08a284cf8241ea7.
Accepted analytical parent: 9b1f9d761e4ae5e6fbaa5bd7dc17b4eac4b452e2.

No numerical execution, implementation, benchmark or numbered certification.

## 1. Native setting

Fix a finite ordered palette P, labelled original roots and their SAME ORIGINAL positive floors a_i. One primitive toggles ONE incidence in ONE root. Larger intermediate supports are native. No label or root is added, no floor is weakened, and no simultaneous move, compactness, geometry or fundamental time is imposed.

Let A = (A_i) and C = (C_i) be exact-four endpoints on the same carrier. A whole-root order is a permutation

    sigma = (sigma_1, ..., sigma_r)

of the labelled root slots.

For 0 <= p <= r define the mixed endpoint tuple M_p by

    (M_p)_i = C_i  if i is among sigma_1, ..., sigma_p,
    (M_p)_i = A_i  otherwise.

An endpoint-containing edit of root sigma_(p+1) first adds all incidences in C_i minus A_i, one at a time, and then deletes all incidences in A_i minus C_i, one at a time. During additions its support contains A_i. During deletions its support contains C_i. All other roots equal their supports in M_p or M_(p+1).

## 2. Typed statements

**X48P - mixed-prefix upper relay.**

Suppose a whole-root order sigma is already proved to give a complete lower-protected endpoint-containing path: tau is at least three at every primitive, every same original floor is respected, every next primitive exists, the path terminates and the exact labelled destination C is restored.

If every mixed tuple M_p has a hitting set K_p of size at most four, then the SAME primitive path satisfies

    3 <= tau <= 4

throughout. The sets K_p may differ arbitrarily. No primitive is needed to change an existential hitting-set witness.

A useful two-cover sufficient condition is the following. Let K_minus hit every A_i and every C_i except possibly roots in V. Let K_plus hit every C_i and every A_i except possibly roots in U. If

    every root in U precedes every root in V under sigma,

then all mixed prefixes have four-covers. K_minus protects prefixes before the first V root completes; K_plus protects prefixes after the last U root completes.

The condition is renewable: any finite sequence of restored handovers may concatenate when each handover supplies a lower-safe order and a mixed-prefix cover certificate.

**X48F - forced relay in the alternating-window family.**

For every even m at least eight, take the d = 1 alternating-window template of corrected X47 and the destination one-step rotation. Accepted X40L supplies a lower-safe root order. Every such total root order forces an even start t for which

    Q_(W_(t-1)) precedes Q_(W_(t+1)).

Physical labels from W_t and W_(t-1) form a two-cover relay on that same order. Therefore the X40L preliminary path itself is a direct path with tau in {3,4}, has the endpoint-toggle minimum and reaches the full exact labelled and noncompact destination.

This family still has

    beta = Gamma = m/2,
    H_alt intersect pi^(-1)(H_alt) = empty.

Thus X45's same-representative lift fails and X46's strict scalar bound fails at equality, while a changing mixed-prefix four-cover succeeds. No maximum-layer conversion is used.

## 3. Proof of the mixed-prefix lemma

Fix p and write i = sigma_(p+1).

During every addition to root i, the active support contains A_i. All already completed roots equal C_j and all not-yet-active roots equal A_j. Therefore a hitting set K_p for M_p hits every inactive root and hits the active root through A_i. Hence K_p hits every primitive state in the addition phase.

After all additions, the active root is A_i union C_i. Both K_p and K_(p+1) hit it: K_p through A_i and K_(p+1) through C_i. A hitting-set witness is existential, so changing which four-set is cited at this same state is not a primitive and changes no incidence.

During every deletion from root i, the active support contains C_i. The completed roots, including i for purposes of the witness, equal or contain their M_(p+1) supports; the remaining roots equal A_j. Therefore K_(p+1) hits every primitive state in the deletion phase.

This proves tau <= 4 on every primitive of the supplied path. The assumed lower theorem proves tau >= 3, floors, actual edits, continuation, termination and restoration on the SAME path. X48 adds no move and changes no root order.

## 4. Proof of the two-cover relay

Define the exceptional sets exactly by

    U = {i : K_plus is disjoint from A_i},
    V = {i : K_minus is disjoint from C_i}.

Assume K_minus hits every A_i and every C_i for i outside V. Assume K_plus hits every C_i and every A_i for i outside U. Assume every U root occurs before every V root. Empty U or V has the evident vacuous interpretation.

Before the first V root completes, no completed destination root belongs to V. K_minus hits every completed C_i and every remaining A_i. Hence it covers each such mixed prefix.

At and after the first V root completes, every U root has already completed. K_plus hits every destination support, including completed U and V roots, and it hits every remaining source support because no remaining root belongs to U. Hence it covers every later mixed prefix.

Between the last U completion and the first V completion both covers may work, but overlap is not required. At the primitive that processes the first V root, K_minus protects additions and K_plus protects deletions by Section 3.

Thus every M_p has a four-cover and X48P applies.

## 5. The accepted alternating template

Let G be m cyclic roles, with m even and at least eight. Put

    W_t = {t, t+1, t+2, t+3}.

Let H_alt be the even-start windows. For every four-set J not in H_alt declare one labelled root

    Q_J = G minus J

with saturated floor m-4. Every role group is the singleton {x_t}. The destination sends x_t from role t to role t+1.

Corrected X47 proves:

1. the template transversal is exactly four;
2. the complete four-cover family is H_alt;
3. the ownership graph is one directed m-cycle;
4. H_alt intersect pi^(-1)(H_alt) is empty;
5. beta = Gamma = m/2;
6. the exact pair redundancy is rho = C(m-2,2) - 2;
7. rho satisfies X40L's strict central-binomial condition.

X48 does not recertify those frozen statements. It uses them as accepted inputs.

## 6. Every lower-safe order forces an upper relay

Restrict any total root order sigma to the odd-window roots. Put n = m/2 and write

    R_j = Q_(W_(2j+1)),    j modulo n.

Let pos(R_j) be the position of R_j in sigma. It is impossible that

    pos(R_(j-1)) > pos(R_j)

for every cyclic j. Chaining all n strict inequalities would return to the starting element and assert that its position is strictly greater than itself. Therefore some j satisfies

    pos(R_(j-1)) < pos(R_j).

Set t = 2j. Then t is even and

    R_(j-1) = Q_(W_(t-1)),
    R_j     = Q_(W_(t+1)).

Define the physical four-label sets

    K_minus = {x_s : s belongs to W_t},
    K_plus  = {x_s : s belongs to W_(t-1)}.

At the source, the owner-role set of K_minus is W_t, an even window in H_alt. Thus K_minus hits every source root.

At the destination, x_s has owner role s+1. The owner-role set of K_minus is W_(t+1), an odd window. In this complementary-root template, a four-role set I misses Q_J exactly when I = J. Therefore K_minus misses exactly the one destination root

    V = {Q_(W_(t+1))}.

At the source, the owner-role set of K_plus is the odd window W_(t-1). It misses exactly the one source root

    U = {Q_(W_(t-1))}.

At the destination, the owner-role set of K_plus is W_t, an even cover. Thus K_plus hits every destination root.

The forced cyclic ascent gives U before V in sigma. Section 4 supplies four-covers for every mixed prefix of that exact order.

## 7. Direct lower and upper completion on the same path

For d = 1, corrected X47 proves

    rho = C(m-2,2) - 2 >= m-2

and hence X40L's strict criterion. X40L deterministically supplies a complete lower-safe whole-root order and endpoint-containing add-before-delete primitive path. It proves:

- every palette pair retains an actual witness;
- tau is at least three at every primitive;
- saturated floors m-4 are respected;
- every primitive is literal and eligible;
- the handover terminates;
- every selected label reaches its final owner;
- every labelled root reaches its full noncompact destination;
- common incidences remain fixed and every endpoint-differing incidence toggles exactly once.

Apply Section 6 to that very order. It produces K_minus, K_plus, U and V after the lower order is known; no change to the order is required. X48P then gives tau <= 4 on every one of the same primitives.

Consequently the preliminary path is directly in the band

    3 <= tau <= 4.

Because X48 adds no primitive, the path retains X40L's exact count

    sum over i of |A_i symmetric-difference C_i|,

which is the mathematical endpoint-toggle minimum. Maximum-layer Theorem A is not invoked.

## 8. Renewal and repeated use

Completing the full m-cycle restores the singleton group sizes, the same actual masks, the same saturated floors, exact target four and the exact labelled destination for that leg.

For any finite supplied chain of exact singleton partitions on the same alternating template, with each next leg a one-step cyclic rotation in some declared cyclic role order, apply X40L separately to the leg. Every resulting total root order again has a cyclic ascent among its odd-window roots, so the two-cover relay is reconstructed rather than consumed.

Concatenating the finite legs gives a direct band path and exact labelled restoration at every declared leg endpoint. The endpoint-toggle minimum is retained per leg. A concatenated chain that revisits incidences is not claimed globally minimum between its outermost endpoints.

This is reusable renewal at restored boundaries. It is not a claim that every arbitrary unfinished state or every arbitrary safe prefix can continue.

## 9. Exact advance beyond X45 and X46

X45 asks for one physical four-set whose source owner roles and destination owner roles are both covers. The alternating family has no such set in the declared one-representative-per-role pool. X48 does not change that fact.

Instead X48 uses K_minus before the exceptional destination root and K_plus after the exceptional source root. The hitting-set witness changes at a mixed prefix, while the physical root edits remain exactly the lower-safe X40 edits.

X46's strict scalar condition also remains false:

    beta = Gamma = m/2
    is not less than ceil(m/2) = m/2.

The new resource is neither more redundancy nor fewer bad windows. It is the orientation of two exact exceptional roots inside the actual lower-safe root order. A total cyclic order forces at least one usable orientation. This is a joint lower-order and upper-cover statement.

For d greater than one, a two-cover relay would require all copies of one exceptional root type before every copy of the other. The single cyclic-ascent argument does not force that block precedence. X48 makes no duplicated-family claim.

## 10. Prior-method separations and controls

The family remains outside the direct sufficient inputs recorded by corrected X47:

- X38: the only nontrivial ownership cycle has length m at least eight.
- X39: every mask has width m-4, less than m-3.
- X40U: every role group is singleton.
- X41: all role incidence profiles are distinct and every root contains at least four profiles.
- X43: its size premise would require 4 >= m-1.
- X44: the cover density is below one half.
- X45: the exact same-representative intersection is empty.
- X46: the strict gap bound fails at equality.

Four disjoint saturated supports cannot fit because 4(m-4) > m. Two labels whose old/new footprints form an even window hit every whole endpoint-union root, so global union preparation is unsafe. Every root changes under the full rotation.

These facts control earlier methods. They do not prove native disconnection. The new result instead constructs a direct band path for the d = 1 family.

## 11. Limits and next obligation

X48 proves a general mixed-prefix upper interface and an infinite saturated family in which the actual lower-safe order forces a usable two-cover relay. It separates common endpoint protection from renewable prefix protection: protection can change identity without adding an incidence or returning to exact four between roots.

The inputs remain substantial. The general theorem requires a complete lower-safe whole-root order plus four-covers for all mixed prefixes, or the stated two-cover exception order. The family uses the supplied alternating template, equal singleton role sizes, d = 1 and a full cyclic rotation.

X48 does not prove arbitrary endpoints admit a relay order, that X40's conditional choice can enforce arbitrary block precedence, or that duplicated alternating families work. Unequal corresponding group sizes, below-X40 lower repair, arbitrary accessibility and unrestricted mixed-floor, directed, higher-target and nested universality remain open.

The next mathematical question is whether several covers can relay through multiple overlapping exception sets under the same conditional root-order potential. That would replace the one-switch certificate with a genuinely multi-stage cover handover.

No numerical execution, enumeration, workflow, implementation, benchmark, integration merge, numbered certification, literature-originality or physical claim. v16.55/v16.54, their frozen sources and all evidence remain unchanged. Separate efficiency implementation, fixtures and benchmarks remain unstarted.
