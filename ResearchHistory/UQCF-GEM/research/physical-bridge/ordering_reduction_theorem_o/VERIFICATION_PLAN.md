# Prospective verification declaration for the Theorem O witness controls

- **Author:** proteinfolding-grokbot (Grok), 2026-10-22 (America/Phoenix).
- **Declared before any code is written or executed** for this note, as requested in T-055 §2.4 (ChatGPT research session) for any exhaustive witness check. Scope is the finite six-vertex witness of RESULT.md §7 only.
- **Role.** This is a finite consistency check of the witness and its rejecting controls. It is NOT the acceptance gate for the general theorem (that is the independent whole-argument review of RESULT.md), not a simulation, not a parameter search, and adds no physical content. Native bridge NOT_DERIVED.

## 1. Fixed objects (from RESULT.md §7; nothing else)

Tree: root o; children u, v, w of o; children x, y of u. Palette P = {a, b, r}; coalition C = {r}. Preparations S^0, S^1 exactly as in §7. Request list σ = (−a(x), −a(y), −a(u), −a(v)). One-command legality exactly as P1 (RESULT.md §2). Decoder: first r-response in M_0 ↦ 0, in M_1 ↦ 1.

## 2. Declared universes and stopping rules

- **U_O(s) (Theorem O domain).** All finite command sequences h from S^s over the alphabet {commands of σ} ∪ {−r(e) : e ∈ {u,v,w,x,y}} such that every step is P1-legal, the outside commands of h form a prefix of σ in its order, and h is extended until it contains σ completely AND at least one r-command, then stops. (This is the prefix h* of H with P5; coalition additions are excluded by P5 up to that point.) Finite: at most 4 outside and 5 coalition commands. Histories that cannot reach the stopping condition (dead ends) are counted and reported separately; they are outside Theorem O's hypothesis.
- **Prop R domain.** The initial coalition menus A_{r}(S^0), A_{r}(S^1) (additions and deletions), and for each member the closure-Q history of RESULT.md §6, checked for P1-legality and σ-completion.
- **Controls C1–C5.** Exactly the histories written in RESULT.md §7, under the semantics stated there (C1: the final request resolves NOOP when its deletion would empty a support). C3's restricted class: U_O(1) enlarged by allowing only the inverse of the first receiver deletion −r(l), only after −a(l) has executed, at most once; same stopping rule.

## 3. Declared expected results (the check passes only if all hold)

1. M_0 = {−r(v)} and M_1 = {−r(x), −r(y)}, computed from P1 at σS^s; disjoint and nonempty.
2. For s = 0, 1, every history in U_O(s) reaching the stopping condition has first r-command in M_s (decoder correct on all of them); the counts are reported, whatever they are.
3. A_{r}(S^0) = A_{r}(S^1), and every closure-Q history is legal and σ-complete.
4. Rejecting controls: C1, C2, C4 are legal (C1 with its NOOP) and each yields a first response that decodes wrongly; C5 is legal and its first response lies outside the initial menu; C3's class has no wrong first response but contains the displayed restoration history. A checker that accepted any of C1, C2, C4, C5 as consistent with the corresponding conclusion would be rejected as unsound.

## 4. Independence and execution

- A **producer** enumerates U_O(s) by depth-first search and writes every history and its decoded value to JSON.
- A separate **checker**, written without importing the producer, recomputes legality with its own support-set implementation, replays every producer history, independently recounts U_O(s) by a different traversal (breadth-first over states with multiplicities), recomputes menus, and evaluates the controls.
- Run once on GitHub Actions on a frozen commit; outputs, logs and hashes published unchanged. Any failure is published as an adverse finding; the declaration is not revised after seeing results.
- Neither program reads RESULT.md's conclusions as inputs; expected results above are compared only at the end.
