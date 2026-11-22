# One common grade can generate square views, but the work gate requires a restricted catalog

November 21, 2026 (America/Phoenix). Parent `38a2cab02955fe4e637a2e8929186310434319ea`. This is a scoped Path-A derivation and exact archive replay. The native source-to-receiver bridge is open.

## Common-grade work

**INHERITED.** Fix a finite Genesis-pinned prefix tree $X$. A view $A$ contains the root and every ancestor of each address it retains. FCV `lineage.py` implements $P_{XA}$, which aggregates each atom at its longest retained ancestor. Use the literal zero extension $I_{AX}$ of v16.23 O1 to write $E_A=I_{AX}P_{XA}$. Let $c_v(g)$ be the subtotal of the common extensive grade $g$ in the subtree of $v$. By v16.23 O3, a retained subtree keeps its subtotal. An absent prefix has no descendants in the view. Thus $c_v(E_Ag)=1_{v\in A}c_v(g)$, with the same total at the root for every view. This is on the same ambient carrier $X$, including for comparison of views of different sizes. O1 gives $E_AE_B=E_{A\cap B}=E_BE_A$.

**ACCEPTED-CONDITIONAL.** The v16.22 anchored tree inverse and v15.40 work pairing give exact work equal to the sum over edges of squared differences in subtree subtotals. [Prior exact check](P1_GRADE_WORK_RESULT.md)

The work between the embedded grades of two views is

$$
D(A,B)=\sum_{v\in A\triangle B}c_v(g)^2.
$$

Intersection therefore gives products of two retained-address indicators with grades coming from a single $g$. The comparison rule takes a supplied list of labels with source and response vectors. O1 and O3 give composition and compatibility of views. The archived caller still requires its eligible input list.

## A necessary restriction on the available views

Take a finite catalog of at least two distinct projected sources. Discard coordinates with zero weight $w_v=c_v(g)^2$, then consider the corresponding masks on the remaining coordinates. Intersection and union commute with discarding these coordinates. With distinct masks the minimum off-diagonal work $m$ is positive. If two labels have the same effective mask, separation already fails in the v15.40 metric test.

**Claim.** If the effective masks are pairwise intersection-closed, the original v15.42 operational complex cannot be identified from the global-minimum work graph. The same holds for union-closed effective masks.

For intersection closure, any nearest pair is comparable by inclusion. Otherwise its intersection belongs to the catalog and lies at strictly positive distance less than $m$ from both endpoints. Take a minimum edge $A\subsetneq B$. The degree gate already rejects unless every vertex has exactly four neighbors. At $A$, let $C$ be any of the other three neighbors. If $C\subsetneq A$, the additions $B\setminus A$ and removals $A\setminus C$ are disjoint and each has weight $m$. Thus $D(B,C)=2m$. If $C\supsetneq A$, consider $B\cap C$. An overlap of positive weight between $B\setminus A$ and $C\setminus A$ would have weight strictly between 0 and $m$ because these sets are distinct and have equal weight $m$. Closure would then supply $B\cap C$ at distance strictly between 0 and $m$ from $A$. So the additions are disjoint and again $D(B,C)=2m$.

The work is a positively weighted sum of absolute differences of indicators, so the triangle inequality bounds every pair of neighbors at $A$ by $2m$. The three pairs containing $B$ all maximize. The original `construct_operational_complex` requires exactly two disjoint maximizing pairs after its degree and face gates. Closure under unions has the same proof by complementing masks on the fixed effective ground set, which preserves all work and turns union into intersection.

In particular, if a successful catalog has an incomparable nearest pair, both its intersection and union are absent from the effective catalog, since either would introduce positive distances strictly smaller than $m$. The theorem concerns availability to the same work evaluator. A source preparation may exist elsewhere in the algebra of views. The claim leaves open other grades, geometries, and inherited rules for what an owner can actually compare.

## Frozen exact comparison

**SUPPLIED.** Use the previous periodic five-by-five address association on a star with 25 leaves, and take unit grade at every leaf and at the root. For each $(x,y)\in(\mathbb Z/5)^2$, form the vertical strip $\{x,x+1\}\times\mathbb Z/5$ and horizontal strip $\mathbb Z/5\times\{y,y+1\}$. Execute FCV pruning from the same $X$ to one strip and then to their intersection, and extend the result back to $X$. Their intersection is the four-corner support used per source in the previous test. Validate the two orders and direct pruning against each other. Preparations share total grade 26. The strips, label assignment, common star and unit grade are declared inputs. Each square label indexes an entire retained view. [Previous connection replay](P1_WORK_CONNECTION_RESULT.md)

Replay exactly four catalogs using the original work calculation and the raw v15.42 `construct_operational_complex` gate. The analytic expectations below precede numerical execution.

| Work input | Expected views | Expected minimum | Expected number of minimum edges | Expected gate outcome |
| --- | ---: | ---: | ---: | --- |
| The 25 square intersections | 25 | 4 | 50 | Identifiable, 25 faces, tangent rank 2 |
| Squares and the ten generating strips | 35 | 4 | 50 | `degree_not_four`, ten isolated strips |
| Squares and the side shared by the squares at $(0,0)$ and $(1,0)$ | 26 | 2 | 2 | `degree_not_four`, 23 isolated squares |
| Full intersection closure of the square catalog | 101 | 1 | 125 | `degree_not_four`, all 25 squares isolated |

On the 25 square inputs, two axis-neighbor masks share two leaves. Diagonal neighbors of the square centers share one. A nonneighbor along an axis at cyclic distance 2 has disjoint mask. At each center the four perpendicular neighbor pairs give work 6 and the two opposite pairs give work 8. The original periodic fixture supplies an independent expected edge set. All ten strips are farther than 4 from any other view in the second case. Adding the specified side yields exactly two distance-2 inclusions. Each of the 50 original square-neighbor pairs likewise has an available-in-principle distinct shared-side mask whose admission would lower the minimum.

Every nonempty intersection of the squares is a product of cyclic coordinate blocks of size one or two. Hence the full closure has the original 25 squares, 50 sides, 25 singleton views and the root-only view. The 125 minimum edges are the 25 root-to-singleton and 100 singleton-to-side edges. The independent checker derives these supports and edges from the original periodic fixture and compares the entire sets. The archived work and exact cut formula are compared for every pair. The raw geometry gate applies to all four catalogs before the v15.43 application restrictions on a square label count could intervene.

The positive comparison requires supplying the square views as the available list. The inherited operation now produces the grades once the two input strips are given. Adding the actual intermediate strip views or their smaller intersections to that list breaks the archived gate. For native square geometry, the missing step is an inherited reason why the owner comparison can use the joint outputs with the required exclusions. No physical owner, event scheduler, time coordinate or gravity claim follows from the comparison.
