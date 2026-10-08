# C3 observation-fiber certification theorem: exact factorization and minimal distinguishing refinement

Date: 2026-10-08.
Status: AUTHOR-SIDE ANALYTICAL CANDIDATE; independent review pending.
Frozen scope COUPLED_C3_FIBER_CERT_SCOPE.md at 5703c02c79227a5bb6af549d767309ad532b2109.

## 1. State, attempt, outcomes, and retained observation

Let X be a finite labelled-incidence state space, X_adm its native admissible states under declared floors and hitting-number band, x a known prepared initial state, and a a known attempted command. Let Y=Y(x,a) be a nonempty finite set of possible post-attempt outcomes, each in X_adm. If a may reject, x may be in Y as a NO-OP; rejection is not a native edit. A successful committed edit yields its actual valid successor.

Let O:Y->R be the retained post-attempt observation. The transcript includes x and a, which are fixed in this theorem. Let c:Y->{0,1} be the semantic-commit predicate, and b:Y->{0,1} any requested capacity predicate. We do not assume that c is inferable from state alone in all models; in the present formalism Y must distinguish outcome records with different c even if their final incidence supports happen to coincide. More precisely, where necessary Y consists of labelled OUTCOME RECORDS (post-state, commitment status), with O factoring through their post-state. This avoids silently identifying two outcomes that have identical supports but different commit provenance.

## 2. Exact factorization criterion

**Theorem F1.** A deterministic function g:R-> {0,1} satisfying g(O(y))=c(y) for every y in Y exists if and only if c is constant on every fiber O^{-1}(r) intersect Y.

Necessity: if O(y)=O(y'), then g(O(y))=g(O(y')); hence c(y)=c(y').

Sufficiency: on every attained r in O(Y), choose any y with O(y)=r and set g(r)=c(y). Fiber constancy makes this independent of the choice. Extend g arbitrarily to unattained r. Then g composed with O equals c on Y.

Exactly the same proof applies to b, and to the pair p=(c,b):Y->{0,1}^2. A joint deterministic certifier exists if and only if the PAIR is constant on every O-fiber.

This is an information-factorization theorem, not an implementation of a measurement or observer.

## 3. Coarsest additional observation sufficient for a requested predicate

Fix O and a finite target predicate p:Y->V. Define an equivalence relation
  y ~_{O,p} y' iff O(y)=O(y') AND p(y)=p(y').

This relation refines the O-fiber partition. Any augmented observation A:Y->W for which (O,A) determines p must distinguish every pair with equal O but unequal p; therefore the partition induced by (O,A) refines ~_{O,p}. Conversely the partition ~_{O,p} itself determines both O and p and is sufficient. Hence ~_{O,p} is the UNIQUE COARSEST PARTITION refining O that suffices to determine p. It is not necessarily a unique minimal sensor or a canonical numeric encoding.

For each attained r, at least |p(O^{-1}(r))| distinguishable observation classes are needed inside that fiber. The worst-case number of supplementary symbols is at least max_r |p(O^{-1}(r))|. If A may use symbols with O jointly, this bound is attainable by separately coding the predicate classes inside each fiber. For a Boolean p, a one-bit supplementary code always suffices mathematically (e.g. p itself), but this does NOT derive an accessible one-bit physical observation.

If p is the pair (c,b), up to four classes may be needed inside an O-fiber; fewer suffice if some pairs do not occur. These are exact combinatorial bounds for the declared outcome space.

## 4. C3 semantic-commit carrier

Let E(Z)=({a,b},{b,c},{a,c},{d,e} union Z), floor2 and tau=3. Start at x=E(empty), issue attempted +z(r4), and permit exactly two outcomes:
  R=(E(empty), c=0): rejected no-op;
  C=(E({z}), c=1): committed valid native insertion.

The declared core-only O consists of labelled core projections, all core-only miss counts, exact tau and floor-validity. Both outcomes have identical O, but c(R)=0 and c(C)=1, and b(R)=0, b(C)=1.

Thus c, b, and (c,b) each fail fiber constancy for this O. One extra binary distinction is NECESSARY AND SUFFICIENT as an abstract refinement of this two-outcome fiber.

A legitimately initialized full-palette singleton miss count M_{ {r4} }({z}) distinguishes R (value1) from C (value0); so does full r4 cardinality (2 versus3), floor slack (0 versus1), or an actual semantic-commit acknowledgement. These are conditional stronger observation channels, not proven natively available.

## 5. Deterministic commitment removes this specific obstruction

Consider a stronger declared operational model in which the attempted +z(r4) is syntactically valid and ALWAYS commits exactly once, and there are no other possible outcomes. Then Y={C}, every predicate is constant on every observation fiber, and even a constant O admits a certifier (g returns c=1). This is a theorem about a different outcome relation; it does NOT show that the native theory supplies an always-commit mechanism.

If a failed attempt and a successful edit could lead to the same final support through compensating hidden edits, post-state O alone could not distinguish their provenance; outcome records, not just incidence states, must be retained in Y. That observation further limits, rather than strengthens, physical claims.

## 6. What is and is not discovered

We now have a reusable criterion: a proposed retained-information field supports semantic commitment or capacity inference EXACTLY when its observational fibers do not mix target values. This identifies what any successful native observer bridge must separate, without choosing a new primitive or invoking an external alignment trick.

The criterion itself does NOT construct a native observable, show how miss counts are initialized, establish commitment semantics from ordered events, or derive force, geometry, energy, continuum, GR/ADM or fundamental time.

Broader C3 observer/accessibility and C4-C6 remain OPEN.
