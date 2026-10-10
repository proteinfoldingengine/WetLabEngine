# Exact static reserve capacity and an unbounded reachability gap

Status: analytical argument frozen before computation. Use the original-source universal safe-region theorem, not a narrowed or current-source hidden fiber.

## 1. Maximal-footprint integer characterization

Let R be a finite nonempty labelled root set, C_i nonempty, 3<=tau(C)<=4, original positive floors f_i<=|C_i|, and fixed finite core palette P. The hidden palette is disjoint and nonempty. For each core x its original footprint is I_x(C); M is the set of inclusion-maximal nonempty such footprints, with duplicates merged. Every root belongs to a member of M.

An allocation consists of nonnegative integers n_J for J in M. It is feasible iff each root i has sum_{J contains i}n_J>=f_i, AND some at-most-four distinct positively occupied J cover R. Define kappa(C,f) as the minimum sum_J n_J over feasible allocations. This minimum exists: expand each original active footprint to a containing maximal footprint. Original floors hold, and an original cover of at most four labels expands to a cover by at most four occupied maximal footprints. This uses at most |P| labels.

Claim: for any integer0<=N<=|P|, some core D using at most N active labels is uniformly admissible over ALL original protected hidden completions iff kappa<=N.

Necessity: the universal safe-region theorem gives core floors, tau(D)<=4 and, for each active x, I_x(D) subset I_y(C). Choose a maximal J containing I_y(C), and assign x to J. Expanding all assigned footprints cannot reduce root sizes, so allocation floor inequalities hold. A core hitting set of D of at most four active labels gives at most four assigned occupied J whose union covers R. Total allocation is exactly the number of active D labels, at most N.

Sufficiency: assign distinct actual labels from P to the sum n_J slots, each assigned footprint exactly J. Define D_i as labels whose assigned J contains i; other P labels are absent. Root sizes meet floors; a chosen at-most-four occupied J cover gives a core cover of at most four actual labels. Every current footprint equals an original maximal footprint, so it is dominated by an original core label. The exact universal criterion gives admissibility for every original Q. Palette names can be assigned arbitrarily; therefore a SPECIFIED r can be omitted iff kappa<=|P|-1. More generally any prescribed set of s labels can be omitted iff kappa<=|P|-s.

This is a finite integer feasibility characterization, not a numerical heuristic or a complexity/efficient algorithm claim. It characterizes static safe cores, not a route from C. The explicit upper-cover condition is retained independently of the floor multicover inequalities. Q empty makes core floors and upper protection necessary; arbitrary hidden lower protection follows original footprint domination.

## 2. Arbitrarily large spare capacity with no first safe edit

For n>=2 use roots L_i={a,c_i}, R_i={b,c_i}, i=1..n, and F={f}. Palette P={a,b,f,c_1,...,c_n}; floors2 on every L_i/R_i,1 on F; ALL are saturated and all n+3 labels active. The original core has tau3: a,b,f cover; F needs f, and no one label covers all L/R roots for n>=2.

Original maximal footprints are L={L_i}, R={R_i}, each pair J_i={L_i,R_i}, and {F}. They form an antichain: pair J_i crosses L/R, while each of L/R has at least two roots. Every original footprint is one of these maximal footprints; equal duplicate footprints do not occur. At a saturated source, deletions fail the admitted empty-Q floor. Any syntactically new addition enlarges an active footprint, which cannot be contained in a distinct original footprint in this antichain. The universal criterion supplies an admitted hidden witness, so no first changing toggle is uniformly safe. Arbitrary NOOPs cannot leave this isolated source. This invokes the inherited general first-progress theorem, not unsuccessful path search.

Capacity nevertheless equals5. The2n L/R roots demand4n incidences. Each occupied maximal footprint other than{F} supplies at most n of these incidences (n>=2), and{F} supplies none. Hence at least four non-F labels are needed, plus one F label: kappa>=5. Assign two labels to L, two labels to R, one to F: floors hold and these three occupied footprint types cover all roots, so kappa<=5.

An explicit five-label target D uses{a,c_1} at ALL L roots,{b,c_2} at ALL R roots,{f} at F. For n>=2 these are five distinct labels, D tau3, floors preserved. c_1 now maps to original a footprint, c_2 to original b, and a,b,f are fixed; thus all original protected Q remain admitted. The unused labels are c_3,...,c_n. For n>=3 static reserve count is n-2 and grows without bound, yet the original source cannot make ANY first safe changing edit. It cannot reach D or ANY absent-label state under the declared native alphabet. D is a different labelled endpoint even for n=2, where no label is absent. Hidden Q is unchanged; no observer information is recovered.

This falsifies 'enough static reserve capacity guarantees safe release' and 'safe destination implies connectivity', even with saturated source, core tau3, arbitrary original hidden fiber and an unbounded number of potentially unused labels. It does not prove impossibility with an initially unused supplied label, multi-incidence atomic moves, hidden-label edits, restricted fibers or modified floors.

## 3. Upper-control and interpretation

Upper-cover constraints must be checked for candidates separately. Ten roots T_i,X_i, i1..5: original labels A on all T, B on X1..3, C on X4..5, and p_i on{T_i,X_i}. Original core tau3 (A,B,C); floors1. All pair footprints are maximal. Candidate retaining only the five p_i pairs meets floors and original-footprint domination but has tau5 in the admitted empty-Q world. It is unsafe. This does not itself claim that omitting the cover condition changes the MINIMUM kappa for this example; it demonstrates failure of a floor-plus-domination candidate rule.

The new exact static characterization generalizes earlier particular capacity obstructions, while the family separates arbitrarily large capacity surplus from native motion. It does not repeat the antichain first-progress lemma as a new discovery. The prior saturated redundancy-transfer route remains valid on its nested-footprint family, and core-region admissibility remains distinct from connectivity. Next find positive path-existence conditions beyond a single common backbone, or identify the exact further connectivity obstruction when safe first progress exists. Native observer access and committed progress remain supplied, broad C3/general C4 OPEN. No force, fundamental time, dark-matter variable, inserted geometry or physical GR derivation follows.
