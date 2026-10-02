# Beyond guarded clones: star relocation and finite module balancing

Status: candidate analytical result for independent review. Parent analytical head 978b4bc590bffc4b355aa1cd39968baabdf2c283. No implementation, numerical search or scientific execution. Earlier accepted proof files remain unchanged.

## 1. Global question and outcome

The exact contraction criterion decides whether a proposed clone is safe. It does not show that safe clones connect arbitrary exact endpoints. Here we prove that completed guarded clones, even with completed label/root permutations, are insufficient for connectivity: a concrete pair of exact-q endpoints cannot be connected by those operations, although a native one-unit path does connect them.

The replacement mechanism is an entire-star relocation. A fixed family of roots supplies q-1 hitting units, and all changing roots retain one label that supplies the last possible unit. This gives a direct unit-band path. It supports finite balancing of complete uniform hyperedge modules for arbitrary rank and module count, with explicit root-slot accounting.

The result remains scoped: it does not show that arbitrary higher-floor endpoints can reach such modules or that unrestricted guarded exchanges have a global progress measure.

## 2. A direct star exchange under a fixed guard

**Lemma X (fixed-star exchange).** Partition the root indices into fixed indices I and editable indices J. Suppose the fixed supports avoid a label u and have hitting number q-1. At both endpoint tuples, every editable support contains u and meets its own positive floor. Then the endpoints are connected by single-incidence moves respecting floors and tau in {q-1,q}.

Proof. Replace each editable support X_j by Y_j through X_j -> X_j union Y_j -> Y_j. Floors hold throughout, and every editable root retains u. The fixed family forces tau>=q-1. A minimum hitting set of the fixed family together with u hits every intermediate root, so tau<=q. This proves the full band directly, with no pair-root assumption, clone formula, or upper-excursion removal. The endpoints need not be exact-q for the lemma, though the applications below are.

The fixed family must really have hitting number q-1; a scalar degree count is not a substitute. Arbitrary floors are permitted because each support is replaced in its own slot. This is a different operation from copying all v-only roles in the earlier clone construction.

## 3. Complete uniform modules

Fix a uniform floor h>=3 at every root and partition P into m disjoint modules S_1,...,S_m, each of size s_j>=h. In each module include every h-element subset as a distinct core root. Extra root slots are allowed, but their supports must contain at least one core root; duplicates and full-palette supports are examples. Such extra constraints are redundant.

A complete h-uniform family on s labels has hitting number s-h+1: a hitting set must leave at most h-1 labels outside it, and any such set suffices. Disjoint modules have additive hitting numbers. Thus these tuples have

    q = sum_j(s_j-h+1) = k-m(h-1).

Assume q>=3. Let e=sum_j binomial(s_j,h) be the number of distinct core roots, so the r available slots satisfy r>=e.

Choose and hold one representative of each core root. Every extra root can first be changed to a chosen core root E_0 through their union, without changing tau=q: the held core already forces q, and any core hitting set hits the old extra root, E_0 and their union. Floors remain h. This normalizes redundancy while preserving all r slots.

## 4. Relocation changes the overlap structure safely

Suppose two modules have sizes a>=b+2. Choose a label u in the larger module and move it into the smaller one. All core roots not containing u remain unchanged. The distinct old u-roots number

    D_old=binomial(a-1,h-1),

while the distinct desired u-roots number

    D_new=binomial(b,h-1) <= D_old.

Every desired root consists of u plus h-1 labels of the smaller module. There are enough editable slots: keep all non-u slots fixed and edit every u-containing slot, including any duplicate u-root. Assign one desired root to each of D_new slots and fill unused editable slots with P. Every assigned support contains u and meets floor h. No root or label is added.

The fixed core is the complete h-uniform family on the large module minus u, the unchanged small module, and all other modules. The large module remains of size at least h because a>=b+2>=h+2. Its contribution has fallen by exactly one. Thus the fixed family has hitting number q-1; any fixed duplicate is redundant with that core. Lemma X supplies a primitive path with tau in {q-1,q} throughout.

At completion the modules have sizes a-1 and b+1, both at least h. The new complete core still has hitting number q, and P fillers and surviving duplicates are redundant. Normalize extras to a core root again if needed. Every completed relocation is exactly at q, so subsequent relocations do not accumulate deficits.

This move can alter module sizes and hence the overlap structure. It need not be a safe clone and does not rely on the contracted clone guard.

## 5. Finite progress and common form

**Theorem Y (uniform-module connectivity).** Fix r,k,h>=3 and q>=3. Any two tuples of the above complete-module type with these same parameters are connected with tau in {q-1,q}, even when their module sizes and redundant root multiplicities differ.

Their number of modules is the same, m=(k-q)/(h-1), by the hitting-number formula. Repeatedly relocate a vertex from a module of size a to one of size b whenever a>=b+2. At a completed relocation the positive integer potential sum_j s_j^2 decreases by

    2(a-b-1)>0.

All modules remain at least h, so the process terminates with sizes differing by at most one. The resulting size multiset is uniquely determined by k,m. The number of distinct core roots never increases, by D_new<=D_old, so the fixed r slots suffice throughout.

Use the accepted safe label permutations to map the balanced modules to a canonical partition of the ordered palette. Retain one copy of each canonical core root, normalize all extras to one chosen core root, and use safe root permutations to put the r supports in canonical order. All floors equal h, so those permutations are permitted. These operations have the already proved unit-band paths, and completed tuples remain exact-q.

Each original endpoint reaches the same ordered tuple in finitely many primitive moves. Reverse the second path and concatenate. This proves Y without an arity campaign, extra capacity, a rank-two reduction, or a conjectured global clone progression. It does not classify arbitrary exact-q tuples as complete-module tuples.

## 6. Guarded cloning can be globally insufficient

Start with a PURE complete-module tuple: exactly one slot per core root and no extras. Consider the operation set consisting of completed slot-compatible clones whose completed hitting number does not decrease, and completed label/root permutations.

If u,v lie in the same module, every copied v-only support is already the corresponding old u-only support. Their counts agree and every editable slot is needed, so no P filler appears. A completed clone only reassigns the same family of core supports among those slots. Label/root permutations also preserve the module-size multiset and distinct core structure.

If u,v lie in different modules, use the exact clone formula from CONTRACTION_CLONE_GUARD.md. Deleting u's old star reduces its module's cover contribution by one, so f=q-1. In the retained contracted family L, the u-module is again missing u and loses one unit. The v-module contracts to a complete (h-1)-uniform family on its remaining s_v-1 labels, plus redundant h-subsets; its hitting number remains s_v-h+1. Every other module is unchanged. Hence lambda=q-1. Whenever the slot criterion allows the clone, its completed hitting number is q-1 and it is not an endpoint-nondecreasing guarded clone. If the slot criterion fails, the clone is not available at all.

Therefore every allowed completed operation from a pure complete-module tuple leaves it within its original label/root symmetry class. This statement concerns the specified completed operations. It does not exclude branching partway through their primitive paths, or other star exchanges; those would be additional moves beyond this restricted progression argument.

For a concrete same-carrier pair, take h=3, k=8 and r=11. A pure module partition of sizes 3 and 5 has 1+10=11 distinct triple roots and exact target q=(3-2)+(5-2)=4. A partition of sizes 4 and 4 has 4+4=8 distinct triple roots; fill its other three slots with duplicates of a core root. It too has exact target 4 and the same palette and all eleven floors 3.

The second endpoint is outside the first endpoint's symmetry class: it has eight distinct supports rather than eleven. The guarded completed-operation system cannot connect them. Nevertheless one relocation of a label from the size-5 module to the size-3 module does: six old incident triples are reassigned to three new incident triples and three P fillers, with fixed-family hitting number 3. Then normalize the fillers to duplicate core roots. This is a native path with hitting number in {3,4}; no barrier greater than one exists for this pair.

The numbers describe a directly proved symbolic construction, not an executed enumeration. More generally Y connects complete-module size partitions while guarded cloning from a pure module tuple cannot alter its size multiset. The local clone criterion is correct but is not a complete global connectivity mechanism.

## 7. What has been learned

Safe completed clones can get stuck in a symmetry class even when a one-unit connection leaves that class. The new star exchange avoids that limitation by retaining a fixed q-1 guard and a common label throughout the edited roots. For complete uniform modules, the root-slot inequality and decreasing size potential supply both capacity control and finite progress.

The unresolved higher-floor problem is whether arbitrary exact endpoints can reach such module forms or another common family through guarded star exchanges, and what replaces the balancing potential outside these forms. No universal arbitrary-floor result, disconnected exact-state example, native barrier, efficiency guarantee or physical implication is claimed. Prior conditional native lifting remains unchanged.

Independent review must check the full band in X, redundant-root normalization, binomial slot counts, all completed hitting numbers, balancing termination, cross-module contraction including a minimal module of size h, and the precise restricted-operation versus native-connectivity distinction. No implementation or numerical campaign is initiated.
