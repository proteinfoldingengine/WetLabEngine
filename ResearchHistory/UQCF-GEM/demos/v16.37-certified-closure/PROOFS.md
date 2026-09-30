# v16.37 proof and argument ledger

## P1 — Legal graph connectivity
Every indexed covering prefix-view state can be expanded to the state in which all views contain the whole tree. Add missing vertices ancestor-first in each view. Each move changes one incidence, preserves prefix closure and cannot destroy the whole union. Reverse such expansions to connect arbitrary states. Repeated indexed views are admitted. Thus all primary finite minimax problems have attaining paths.

## P2 — Scalar minimax and quotient ultrametric
Fix a graph and q0. For any one of the three primary scalar nonnegative costs c with c=0 exactly on q=q0, define d(a,b)=min_path max c. Minima exist on the finite graph (cycles may be removed without raising cost). Concatenating minimizing a-b and b-c paths proves d(a,c)<=max(d(a,b),d(b,c)). Reversal proves symmetry; a constant path gives d(a,a)=0. Zero distance means a zero-cost path, exactly connectivity inside the q0 fiber. Appending zero-cost paths proves representative independence; quotienting zero-cost components yields an ultrametric. This proof only compares endpoints in the same fixed fiber, not across different q0 values.

## P3 — Exact scalar threshold certificates
For integer t, d(a,b)<=t iff b is reachable from a in the induced set {c<=t}. An attaining path of maximum B and a complete reachable set at threshold B-1 excluding b establish d=B. For B=0 the lower set is empty. Primary costs are nonnegative integers. Producer emits three paths and three lower reachable sets; verifier independently recomputes both graph and lower sets.

## P4 — Independent minima and lexicographic objective
The primary Bj optimize separately on the unrestricted graph; their minimizers may be different paths. Their tuple does not in general have a jointly attaining path. For LEX_BARRIER first minimize c1 threshold, restrict to that sublevel, minimize cinf, then restrict and minimize cs. This is exactly lexicographic optimization by nested feasible sets. The independent verifier instead enumerates all attained-cost threshold boxes in lexicographic order and chooses the first connected box. This agrees because each coordinate of a path maximum is attained at a vertex.

The abstract two-route control has path triples(4,2,2) and(3,3,1): independent minima(3,2,1), lex optimum(3,3,1). It proves objective distinction on an abstract graph only. The historical abstract control demonstrates that componentwise maximum does not preserve lex order, making one lex-best label insufficient generally. Neither abstract graph is claimed to be an admitted retained construction.

## P5 — Complete shape/state/pair coverage
Ancestor-first parent arrays contain a labeling of every finite rooted tree by topological ordering; rooted bracket codes identify rooted unordered shapes. The producer chooses the first (lexicographically least) ancestor-array representative. Every labeled tree with n>=2 has a Prüfer sequence; checking every root and every root-fixed relabeling includes all ancestor-first representations. The independent verifier takes the least representative per rooted code; n=1 is explicit.

Prefix views can be generated either by testing all root-containing subsets for parent closure or recursively choosing an included rooted prefix or the empty set at every child. Both constructions enumerate exactly the same admitted views. Indexed products preserving whole union enumerate exactly the states. Direct one-bit toggles and all-pairs incidence difference1 enumerate the same legal graph.

For each q, connected components partition every state with that q. Every unordered component pair is explicitly certified. Representative independence from P2 allows these records to cover all cross-component endpoint pairs; their complete identities are defined by the stored state lists and component memberships, not by a count. The verifier rebuilds the exact graph and pair sets. The <=4 endpoint identities are then compared with the historical corpus; the latter does not define enumeration.

## P6 — Outcome scope and witness minimality
A nonunit primary value on an admitted equal-q disconnected pair refutes unit universality. Exact complete enumeration before it in the frozen ordering supports bounded minimality only. If all finite tested values are unit, the result is BOUNDED_UNIT_ONLY and does not prove a universal unit theorem. No universal unit proof is supplied here; the actual enumeration verdict is recorded in SUMMARY.json and REPORT.md.

## P7 — Predictor interpretation
The exploratory C uses the already computed barrier to define its allowed set. This dependency prevents treating C as a predictor computed without the target barrier; it does not by itself refute mathematical factorization. A corpus whose target is constant cannot discriminate competing signatures by no-collision. The new campaign separately checks whether the larger frozen domain has target variation.

## P8 — Evidence and physical boundary
The proofs are written mathematical arguments with a fresh reviewer, not proof-assistant formalization. Numerical verification is independently implemented, not independent empirical measurement. No result derives energy, action, physical metric, gravity or fundamental time. Time is pruning / ordered recoverability update.
