# C3 partial-seed theorem: exact event-prefix bounds and optimality identifiability

Date: 2026-10-07.
Status: REVISED AUTHOR-SIDE CANDIDATE after independent REVISE; fresh review required.
Frozen scope COUPLED_C3_PARTIAL_SEED_SCOPE.md at 542782cd198b65e9bfd79dd88193251666e74637.

Review history: original proof e7a6c7286f08256efd188e3a5357f08cb7a1b961 received independent REVISE for missing self-contained optimality/fallback evidence and undeclared buffer-label availability. The exact seed interval theorem itself was accepted. This corrected proof retains that result and supplies the missing carrier-level derivations.

## 1. Carrier and observation model

Let T be a known finite spectator palette of size N>=0. The prepared four-root state is E(Z)=({a,b},{b,c},{a,c},{d,e} union Z), Z subseteq T, original floors2, protected band 3<=tau<=4.

A COMPLETE ordered spectator event-direction ledger eps_1,...,eps_n is observed on labelled r4. Each eps_j=+1 means a native addition of an ABSENT spectator, and eps_j=-1 means deletion of a PRESENT spectator. Labels are not observed. Core roots and core incidences remain unchanged. The initial spectator set and its cardinality q0 are unknown.

Set s_0=0 and s_j=sum_{i=1}^j eps_i. Let m=min_{0<=j<=n}s_j and M=max_{0<=j<=n}s_j.

## 2. Exact feasible initial counts

**Theorem S1.** There exists a valid labelled spectator history over T realizing the observed direction ledger from some initial set Z0 of size q0 if and only if q0 is an integer satisfying

    L=max(0,-m) <= q0 <= U=min(N,N-M).

Proof of necessity. Any valid event changes spectator cardinality by its sign, so at prefix j, q_j=q0+s_j. As the spectator set is a subset of T, 0<=q_j<=N for all j including j=0. Therefore q0>=-min_j s_j, q0>=0, q0<=N-max_j s_j and q0<=N, precisely L<=q0<=U.

Proof of sufficiency. Fix any integer q0 in [L,U], choose any initial subset Z0 of T with q0 elements. At every prefix q_j=q0+s_j lies in [0,N]. If eps_{j+1}=+1 then q_{j+1}=q_j+1<=N, so q_j<N and at least one absent spectator is available to add. If eps_{j+1}=-1 then q_{j+1}=q_j-1>=0, so q_j>0 and at least one present spectator is available to remove. Choose any such spectator and continue inductively. This constructs a syntactically valid labelled native history with the specified directions.

Every prepared state has tau=3 and floor2: the first three roots form a triangle with hitting number2 and r4 contains {d,e} plus spectators disjoint from triangle labels. Thus the constructed events are also protected.

If L>U, NO valid spectator history can generate the ledger with the declared N. This is an inconsistent input, not evidence that b=0.

## 3. Exact possible current counts and bit classification

For every feasible q0, the current count is q_n=q0+s_n. Therefore the exact set of possible current counts is the integer interval

    [A,B]=[L+s_n,U+s_n].

Because the ledger is valid for each feasible seed, 0<=A<=B<=N.

The current capacity bit b=1[q_n>0] is determined exactly as follows:

- If B=0, b=0 in every consistent hidden world.
- If A>=1, b=1 in every consistent hidden world.
- If A=0 and B>=1, both b=0 and b=1 occur in consistent hidden worlds, so b is not determined.

There is no fourth case for a nonempty feasible interval of nonnegative counts.

## 3A. Explicit fresh-buffer universe and inherited shortest-path proof

The permitted native incidence palette is {a,b,c,d,e,w} union T, where w is a distinct label OUTSIDE T and outside {a,b,c,d,e}. It is initially absent from every root. In particular w remains available even if Z=T or T is empty. Every native event toggles one root-label incidence subject to floor2 and 3<=tau<=4.

For every Z, the following eight events are legal:
  +w(r4), -d(r4), +d(r1), -a(r1), +d(r3), -a(r3), +a(r4), -w(r4).

The fourth-root supports in the successive stages are {d,e} union Z, {d,e,w} union Z, {e,w} union Z (through the two triangle conversions), {a,e,w} union Z, then {a,e} union Z. Thus its cardinality never falls below 2 even when Z=empty, and its spectators never change.

At every step the first three roots have transversal number exactly 2: they progress through
 ({a,b},{b,c},{a,c}),
 ({a,b,d},{b,c},{a,c}),
 ({b,d},{b,c},{a,c}),
 ({b,d},{b,c},{a,c,d}),
 ({b,d},{b,c},{c,d}).
For each intermediate triple, {b,c} is a transversal and no singleton intersects all three roots. At every step r4 is disjoint from the UNION of the current triangle-root labels: before d is removed, the triangle has only a,b,c; after d is removed and until a is restored to r4, r4 has only e,w and spectators; at restoration the triangle has only b,c,d. Consequently the total hitting number is exactly 3 in every state. Every root respects floor2. The path reaches the exact target and removes w, for ALL Z including Z=T and N=0.

There are exactly six mandatory endpoint-differing incidences: +d,-a on r1; +d,-a on r3; and +a,-d on r4. Thus every exact repair requires at least six toggles.

If Z is nonempty, the six-event path
  -d(r4), +d(r1), -a(r1), +d(r3), -a(r3), +a(r4)
is legal: after deleting d, r4={e} union Z has at least two elements; throughout, r4 is disjoint from the changing triangle-root union, and the triangle has hitting number2. Hence tau=3 and floors2 at each step. The path attains the six-event lower bound.

If Z is empty, every endpoint-differing deletion initially violates floor2. Every endpoint-differing addition is also forbidden by a two-cover: +d(r1) produces cover {c,d}; +d(r3) produces {b,d}; +a(r4) produces {a,b}. Thus no endpoint-only first event is legal. Any exact path must use an off-endpoint toggle, which must eventually be undone (each incidence differs from its exact target by parity), costing at least two extra edits beyond the six mandatory endpoint toggles. Therefore length>=8; the explicit buffer path attains eight.

Moreover for Z=empty, among the six mandatory endpoint events, none is initially legal. For Z nonempty, among those six only -d(r4) is initially legal; the others have the same floor failures or two-cover failures. Since a six-edit optimum can use ONLY the six mandatory endpoint events, its first event must be -d(r4). That event is illegal for Z empty. This establishes disjoint optimal first-event sets in ambiguous fibers without invoking a separate unique-host theorem. (The stronger unique optimal host +w(r4) for the empty case is established in the earlier closed C3 host theorem, but is not required for this incompatibility argument.)

## 4. Shortest-repair controller and impossibility

The independently closed C3 hidden-optimality theorem gives minimum eight protected edits when Z is empty and minimum six when Z is nonempty. The empty case's optimal first move is +w(r4); the nonempty case's six-edit optimum begins -d(r4).

Thus:
- If B=0, choose the known eight-edit buffer route; it is shortest for every consistent hidden state.
- If A>=1, choose the known six-edit endpoint-only route; it is shortest for every consistent hidden state.
- If A=0<B, NO deterministic controller that sees only N and the direction ledger can select a first native edit that begins a shortest protected repair in EVERY consistent hidden state. The two worlds share identical observed inputs but demand disjoint optimal first moves.

However the eight-edit buffer route is legal for every possible Z, so the same incomplete retained record still permits a safe, exact, fiber-uniform repair. This preserves the distinction between universal LEGAL control and universal OPTIMAL control.

## 5. Explicit rejecting and positive controls

A. Ambiguous ledger. N=2, eps=(+1,-1). Prefix sums (0,1,0) give m=0, M=1, L=0, U=1, s_n=0. Thus current q in {0,1}. One world begins empty and adds then removes one spectator. Another begins with one spectator, adds the other then removes one. Both yield the same observed signs but require different shortest repair classes.

B. Lower-bound information from a deletion. N=2, eps=(-1,+1). Prefix sums (0,-1,0) give L=1,U=2, current q in {1,2}. Despite unknown seed, b=1 is determined; a six-edit repair is uniformly shortest.

C. Full count reconstruction from event saturation. N=2, eps=(+1,+1,-1,-1). Prefix sums (0,1,2,1,0) give L=U=0. The only feasible initial count is zero, and final b=0. Native validity plus finite capacity has forced the seed, WITHOUT an externally supplied initial count.

D. Inconsistent ledger. N=1, eps=(+1,+1) gives L=0,U=-1; no valid history exists. It must be rejected rather than assigned a capacity bit.

E. Empty palette. N=0 permits only the empty ledger, with L=U=0 and b=0.

## 6. Relationship to the prior capacity count and miss-count certificate

If a complete event ledger with known q0 is available, the prior formula q_n=q0+s_n gives a single count. Here, unknown q0 instead produces an exact INTERVAL of counts. Event-validity constraints sometimes collapse that interval or determine just its positivity, so full seed reconstruction is not always needed to choose the shortest repair.

For residual family {r4}, previously defined full-palette singleton miss counts satisfy q=sum_{z in T}(1-M_R({z})). If those coordinates are initialized, they provide q directly. This theorem uses only finite palette size and event signs; it does not assert access to those initialized coordinates.

## 7. Boundary and next obligation

The theorem derives exact partial-seed information from the ASSUMED complete valid spectator event-direction ledger, known N and declared prepared carrier. It does not derive ledger completeness, root addressability, spectator typing, validity of an arbitrary unverified transcript, or the physical origin of finite palette T.

No observer-access theorem, universal information law, geometry, force, energy, GR/ADM, continuum or fundamental time follows.

The next genuine first-principles gate is to derive which event distinctions are natively accessible from ordered update structure, rather than postulating a complete labelled event channel.
