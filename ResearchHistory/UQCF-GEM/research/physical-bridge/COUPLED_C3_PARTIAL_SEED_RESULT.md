# C3 partial-seed theorem: exact event-prefix bounds and optimality identifiability

Date: 2026-10-07.
Status: AUTHOR-SIDE ANALYTICAL CANDIDATE; independent review pending.
Frozen scope COUPLED_C3_PARTIAL_SEED_SCOPE.md at 542782cd198b65e9bfd79dd88193251666e74637.

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
