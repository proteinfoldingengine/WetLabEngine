# Q147 RESULT (2026-11-11T13:35:44-07:00): C4 is proved. The bare P1 chain yields R_inc^- exactly when owner-decorated sibling types are forced by plain types
Science, local, supporting math. Not posted. NOT_DERIVED; Not claimed; scientific_breakthrough false. notify_aaron: no.
Heads unchanged: research 8c4f6594; thread 8a86d82d. PR111: no comments after 6799790426. No lock.

## Objects
D is the leveled dendrogram: nodes (B,l), B ∈ π_l, l = 0..m, plus a virtual root over π_m. Children of (B,l) are the blocks of π_{l−1} inside B.
G = Aut(D) acting on X_0, which equals the chain automorphisms of Q146. The owner decoration marks, at each node (B,l) with l ≥ 1, the child that contains B's owner t
(namely F_{l−1}(t)). dc is the owner-decorated canonical form. Exception pair: the marked child is a singleton and there is exactly one unmarked child, also a singleton.
C4 has two parts:
(i) no marked child is plain-isomorphic to an unmarked sibling, except an exception pair;
(ii) plain-isomorphic siblings (at every node, root included) have equal dc.

## Lemma 147.1 (𝒮 is the decorated dendrogram, modulo exception pairs)
𝒮_j = for each level-j node w, follow the marked chain down to the leaf t (the owner), and take {t} together with, for every node on the chain, the union of its unmarked children
(the shell A_l(t); unary nodes give nothing). So 𝒮 is a G-equivariant function of the decoration. Swapping the marking at an exception pair leaves every 𝒮_j unchanged
({t},{s} are both blocks either way, and no shell below is affected because the chains below are unary).
Conversely, 𝒮_l together with plain D recovers the marking up to exception pairs. In 𝒮_l, the unmarked children of (B,l) union to one block A_l(t), while the marked child
F_{l−1}(t) is cut into {t} and t's earlier nonempty shells. It is one block iff it is a singleton. The marked child can therefore be confused with an unmarked one only if there is exactly one unmarked child
and both are single 𝒮_l blocks, i.e. both singletons (an exception pair). Plain non-isomorphic children cannot be confused by an automorphism anyway.

## Theorem 147.2. 𝒮_j is G-invariant for all j ⟺ C4. (So, with Lemma 146.1, an Aut-invariant σ with closure R_inc^- exists ⟺ C4.)
(⇐) Let g ∈ G. Show dc(gv) = dc(v) for all nodes by top-down induction. Root children: g permutes the π_m blocks, preserving plain type, so (ii) gives equal dc.
Step: suppose dc(gv) = dc(v), with marked child c*. g(c*) is a child of gv of the same plain type as marked(gv), since dc(gv) = dc(v) forces the marked children's dc
and hence their plain types to agree. So by (i), g(c*) = marked(gv) unless it is an exception pair. In the non-exception case, dc(g c*) = dc(marked(gv)) = dc(c*). In the exception case all singletons share dc.
Unmarked children go to unmarked children. Within each plain type T, the dc's of v's unmarked children are all equal (ii), as are gv's, and the multisets of dc's agree.
dc determines plain type, so the two common values coincide: dc(gc) = dc(c). Hence g preserves the marking except at exception pairs, and by Lemma 147.1 it fixes every 𝒮_j.
(⇒) A violation of (i) gives a sibling swap of the marked child with an isomorphic unmarked one. If the marked child is a non-singleton, ≥2 blocks of 𝒮_l land inside the single block A_l(t).
If both are singletons with ≥2 unmarked, then {t},{s1,s2,...} becomes {s1},{t,s2,...}. A violation of (ii) gives a sibling swap g with dc(ga) ≠ dc(a).
If g fixed 𝒮, Lemma 147.1's converse (bottom-up induction) would give dc(ga) = dc(a), a contradiction. ∎
Proof sentences were checked against simultaneous multi-node removals: shells are unions of unmarked children, which may be several merged nodes, and nothing assumes one removal per step (T-414 lesson).
Confirmation (not proof): 1220 random n=7 cases (seed 147, unchanged Q146 logic), 0 mismatches. Q146 exhaustive n≤6: 0 mismatches.

## Reading and tags
This closes Q144–Q147 exactly. The (E1) stable-address label is information beyond the restriction chain precisely when some automorphism of the fiber dendrogram moves an owner
outside an exception pair. Equivalently, the chain sees where pruned material went but not, in general, which merged constituent was the receiver. The survivor reading R_inc^- is
chain-intrinsic iff C4 holds; otherwise it needs (E1) (ledger §13.2's "σ pinned by (E1)" is exact in that case and redundant otherwise). The fixed state cannot replace (E1) (Q145).
Tags: P1 chain, (E1),(E2), Thm 11.1/13.3 INHERITED. Lemma 147.1 and Thm 147.2 DERIVED (elementary; Aut of a rooted tree acts by isomorphic-sibling permutations, standard).
Novelty: elementary. A possible one-sentence scope precision for ledger §13.2, not a new physical claim. Local only. Hashes (PREREG/check/stdout): 4dd6aa55/69c64817/430fb4c1.

## NEXT
Q148: switch line. A Target B question (joint-event compatibility / naturality): do two commuting native pinchings E_S, E_T and a P1 pruning step commute as restriction maps
on the product frame, or does the order of a merge and a pinch change the survivor closure? Dedup first vs ledger §13.3 witness D ("either order"), Q119 (pruning order), and Q127/Q134 (native prunings commute).
If it is implied, drop it at the gate and pick a Target D invariant-observable question.
