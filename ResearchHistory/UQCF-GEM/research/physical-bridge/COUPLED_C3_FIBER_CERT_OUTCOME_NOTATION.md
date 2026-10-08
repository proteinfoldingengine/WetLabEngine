# C3 observation-fiber certification — outcome-record notation clarification

Date: 2026-10-08.
Disposition: NOTATION CLARIFICATION ONLY; frozen result and scope unchanged.

## Provenance

Frozen scope: COUPLED_C3_FIBER_CERT_SCOPE.md at 5703c02c79227a5bb6af549d767309ad532b2109.
Accepted underlying proof: COUPLED_C3_FIBER_CERT_RESULT.md at 721cd92c67682ac2fcd9ae88d883557f89d863a2.
Independent mathematical reviewer: Firecrawl spark-2 job 01a11cdc-ecba-75f5-a062-4980a3da6169, thread 01a11cdc-ecf3-77bb-a2da-47b9bf93b3a6, verdict ACCEPTED with notation-level qualification.

## Unambiguous model

Let X_adm denote the finite set of physically admissible incidence states. Fix the initial state x and attempted command a. Let Y(x,a) be a finite NONEMPTY SET OF OUTCOME RECORDS, not necessarily a subset of X_adm. There is a specified post-state map

  π : Y(x,a) → X_adm.

Each record includes sufficient abstract provenance to define a semantic commitment bit c:Y(x,a)→{0,1}. For example, one may choose records y=(s,c) in X_adm×{0,1} where s is the final state, with Y restricted to permitted operational outcomes, and π(s,c)=s. This is a mathematical outcome representation, not a physical acknowledgement channel.

The retained post-state observation is O_0:X_adm→R and the actual recorded observation on outcomes is

  O=O_0∘π : Y(x,a) → R.

Any capacity predicate that depends only on state factors as b=b_0∘π. Unlike b, the semantic commitment bit c need NOT factor through π when two distinct possible outcome records have the same post-state but different histories.

Then Theorem F1 is expressed exactly as before: c=g∘O for some g on observed values IF AND ONLY IF c is constant on all fibers of O. The corresponding statements for b and (c,b), minimal common refinement y~y' iff O(y)=O(y') and p(y)=p(y'), and supplementary alphabet lower bound max_r |p(O^{-1}(r))| are unchanged.

## Checks

In the C3 example, R=(E(empty),0) and C=(E({z}),1) are distinct outcome records with different post-states. O_0 includes only core projections, core-only miss counts, tau, and floor-validity; its values on these two post-states coincide. Hence c and capacity b differ in a single observation fiber, so neither can be inferred from that channel. A full-palette or cardinality observation would separate this particular pair if genuinely accessible.

For a model allowing two records y_1=(s,0), y_2=(s,1) with identical post-state s, all POST-STATE observations O_0 necessarily coincide; no state-only observable, even the complete state, resolves the execution provenance. This is not a claim that such a pair is permitted in the C3 native primitive model; its inclusion is conditional on a wider declared outcome relation.

The always-commit singleton model remains trivially certifiable even by constant observation. Rejection is a no-op, not a native incidence edit.

## Limits

This clarification does not add an observer, command acknowledgement, guaranteed commit, measurement, conserved physical quantity, geometry, energy, force, GR/ADM, continuum, or fundamental time. It resolves a domain/codomain ambiguity in a theorem that remains abstract.
