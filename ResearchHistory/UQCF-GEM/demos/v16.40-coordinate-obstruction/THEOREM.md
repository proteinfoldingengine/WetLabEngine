# Unit barriers can require arbitrarily many deviation locations

## Objects and scope
A state on a finite rooted tree with three indexed views assigns each vertex a nonempty support S_v subset of K={a,b,c}; S_root=K and S_child subset of S_parent. Equivalently each indexed view is a root-containing prefix subtree and the views cover every vertex. A primitive move changes one view incidence at one nonroot vertex, preserving admission. At a nonleaf v, q_v is the minimum number of view labels meeting every child support; leaves have q_v=0. Costs relative to a fixed endpoint profile q0 are L1=sum|q-q0|, Linf=max|q-q0| and support size=#(q!=q0). Each primary B is its own scalar minimax over paths; LEX is a separate nested minimax diagnostic.

The theorem concerns this combinatorial category only. It neither supplies physical energy nor proves the universal unit-barrier conjecture. It disproves a universal fixed-coordinate repair claim by a decomposable family. No smallest witness claim is made.

## Two rigid branches
A star B has root b and three leaf children. Requiring q_b=3 forces the three child supports to be three different singleton labels. Indeed if no pair of labels hits all children, for each omitted label some nonempty child support must be contained in that singleton. There are precisely three children, so these are exactly the three singleton supports. Prefix closure then forces S_b=K. There are six such states. A one-incidence change cannot move between them: any different permutation changes at least two incidences. Thus the exact-profile branch state cannot change along any admitted path on which its profile stays fixed.

The branch A has root a, children w and l, and w has two leaf children x,y. Require q_a=q_w=2. The equality q_w=2 means S_x and S_y are disjoint nonempty sets, whence |S_w|>=2. The equality q_a=2 means S_w and S_l are disjoint nonempty sets. As |K|=3, S_w has exactly two labels, S_l the remaining singleton, and S_x,S_y are the two different singleton labels in S_w. Also S_a=K. Again exactly six states result, and each is isolated in the exact branch profile: changing the leaf permutation or the choice of the omitted label requires multiple incidences; the other supports are forced by those choices.

These statements remain true when a branch is attached below a larger root. Project any global primitive path to its branch coordinates, deleting repeated projected states. This yields legal one-incidence branch moves, including changes at the branch root; but while its whole q profile is fixed, that root and all other supports are forced to the six states above. Therefore no such projected move can change the branch state. This argument does not assume the global root profile is fixed.

## Family and lower bound
For any integer r>=1, attach one copy of A and r disjoint copies of B below a new global root. There are 6+4r vertices. In both endpoints, all branch roots and the global root have support K. Choose one rigid branch state in every branch, and define the other endpoint by interchanging a and b at the two designated leaves in each branch, leaving c in the remaining position. In A these are leaves x,y, with S_l={c}. In each B they are its a- and b-labeled leaves.

Both endpoints have q_global=1, q_a=q_w=2 and q_b=3 in each star, with leaf coordinates zero. Every branch changes its state. By branch rigidity, every connecting global path must have at least one q deviation within EACH branch at some time. The branches have disjoint vertex sets, so the union over the path of deviating coordinates has size at least r+1. In particular no one-coordinate path connects the endpoints when r>=1, regardless of how large a deviation that coordinate is allowed.

## Constructive matching upper bound
Swap two singleton leaves initially {a},{b} by these four legal incidence moves:
1. Add a to the b leaf.
2. Add b to the a leaf.
3. Remove a from the original a leaf.
4. Remove b from the original b leaf.
The two supports evolve ({a},{b}), ({a},{a,b}), ({a,b},{a,b}), ({b},{a,b}), ({b},{a}). Their union is always {a,b} and all ancestors remain unchanged.
In A this changes q_w from 2 to 1 during the swap and back to 2; q_a remains 2 because S_w={a,b} and S_l={c}. In B the third leaf {c} is unchanged, so q_b falls from 3 to 2 and returns to 3. No other coordinate changes. Execute the swaps in the r+1 branches serially. Every intermediate state is admitted, q_global remains 1, and at most one coordinate deviates, by exactly one. The path uses exactly r+1 distinct deviation coordinates and 4(r+1) primitive moves.
Every primary scalar barrier and LEX therefore has upper bound 1. A zero-cost path would preserve all branch profiles and contradict rigidity; hence every scalar lower bound is 1. The primary triple and separate LEX are all (1,1,1). The endpoint incidence-Hamming distance is 4(r+1), so the displayed path is also globally shortest in primitive moves. This shortest-move property is separate from its barrier optimality.

## Remaining obstruction class
Using the v16.39 definitions, the ancestor closure H of active vertices contains a->w. Its parent has q_a=2<k, and the subtree at w contains no saturated q=k vertex. Thus SC fails for every member of this family. At the endpoints S_w={a,b} is a proper subset of K, so endpoint-full fails too. Other saturated stars do not lie below w and do not repair this failed edge.
The example is deliberately reducible into independently changing branches. Whether every admitted pair has unit barriers remains unresolved, as does fixed-coordinate sufficiency under suitable conditions excluding this independent-branch decomposition. The theorem proves that any sufficient condition for global fixed-coordinate repair must exclude such simultaneous branch changes, or permit multiple repair locations.

## Finite certificate
The preregistered numerical test is ONLY r=1 on the specified ten-vertex representative, with every admitted state independently enumerated, all exact-target-fiber component pairs classified, all unit edges and static partitions checked. The general-r theorem above is a mathematical argument, not an extrapolation from those finite counts. Predicted counts and the named path remain hypotheses until execution and verification succeed.
