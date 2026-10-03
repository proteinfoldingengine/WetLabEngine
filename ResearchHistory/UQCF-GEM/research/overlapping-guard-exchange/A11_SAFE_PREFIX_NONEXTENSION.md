# A11.X1: a safe monotone prefix can strand all remaining repairs

Status: frozen candidate for independent analytical review. Scope parent: ca6908bd04ef35bf9f297c42c8878f156d7c6263. A11 primary schedule existence remains OPEN. This checkpoint disproves universal SAFE-PREFIX EXTENSION, not existence of a destination-directed schedule. No enumeration, numerical campaign, implementation, tests or workflows.

## 1. Carrier and result

Use 15 labelled roots I={0,...,14}. The palette is

    P={(S,c): S subset I, |S|=8, c in {0,1}}.

There are k=2*binomial(15,8)=12870 distinct labels. The second coordinate distinguishes two labels with the same incidence pattern; they are existing palette labels, not new labels introduced along a path. Define

    B_i={(S,c): i in S},  D_i=P minus B_i.

Then |B_i|=2*binomial(14,7)=6864 and |D_i|=6006 for every i. Floors are a_0=a_1=1 and a_i=6006 for i=2,...,14. All supports, including noncompact ones, are allowed by these original floors.

We construct exact-four endpoints A,C and a destination-directed primitive prefix A -> D with tau>=3. At D, EVERY remaining destination-directed event is illegal for the lower guard or the floors. Nevertheless the SAME A,C admit another destination-directed lower path. D also has a native lower path to C, but every such path must first delete a destination incidence at one of the already completed slots 0 or 1.

The example is not the original uniform-floor-three diagnostic and does not challenge any accepted primitive connectivity class. Its question concerns schedule extension inside an incidence-monotone box.

## 2. Pair-private protection in D

Every pair of palette labels has root-code intersection nonempty: two eight-subsets of a fifteen-set intersect. If the labels share the same code this is also immediate. Hence every pair is missed by some D_i, and tau(D)>=3.

For tau(D)<=3, take three distinct labels with root codes

    U={0,...,7}, V={0,8,...,14}, W={1,...,8}.

Their three-way intersection is empty. A set of labels hits all D_i exactly when the intersection of their root codes is empty. These three labels therefore hit D, giving tau(D)=3.

More strongly, every potential addition x=(S,c) to ANY D_i is unsafe for tau>=3. Such an x has i in S. Let

    T=(I minus S) union {i},  y=(T,0).

T is an eight-subset, S intersect T={i}, and x,y are distinct. The pair H={x,y} misses exactly D_i and hits every other D_j. Adding x at i removes its LAST missed root, so H becomes a two-label transversal.

This is an explicit protection witness for every addition, not an enumerated empirical assertion. The witness count changes from one to zero at the proposed addition. Any deletion at roots 2,...,14 violates the floor because |D_i|=6006=a_i. Thus the only legal native first moves out of D are deletions at slots 0 or 1; these preserve the lower bound because shrinking a support cannot decrease tau.

## 3. Exact-four source and its legal stranded prefix

Choose an eight-subset R excluding indices 0 and 1, for example R={7,...,14}, and distinct palette labels

    z_0=(R,0), z_1=(R,1).

Set A_0={z_0}, A_1={z_1}, and A_i=D_i for i>=2.

Any transversal of at most three labels must contain BOTH z_0 and z_1 to hit the singleton roots. If a third label has code Q, then R intersect Q is nonempty, because both have size eight in I. Every index in that intersection belongs to R and hence is different from 0,1. At that remaining root, all three labels are absent from D_i. The same reasoning covers a two-label candidate. Thus tau(A)>=4.

Choose labels u,v whose codes are eight-subsets intersecting exactly at {0}: partition I minus {0} into two seven-subsets and adjoin 0 to each. Their pair hits every root with index >=2, while z_0,z_1 hit the two singleton roots. These four distinct labels form a transversal, so tau(A)=4.

Since R excludes 0,1, z_0 belongs to D_0 and z_1 belongs to D_1. Expand A_0 to D_0 and A_1 to D_1 by adding each missing incidence individually, in any fixed order, leaving all other roots unchanged. Every intermediate tuple is componentwise contained in D, so its transversal is at least tau(D)=3. It contains A componentwise, so its transversal is at most tau(A)=4. The original floors hold. The prefix consists of exactly 2*(6006-1)=12010 genuine additions and stays in {3,4}.

Section 4 sets C_0=D_0 and C_1=D_1. Therefore ALL these additions are destination-directed events for A -> C. This is a legal prefix in A11's exact schedule class, not a path using an extra palette or a temporary incidence.

## 4. Exact-four destination on the same carrier

Identify the 15 root indices with the nonzero vectors w_i in F_2^4, with w_0=e_1 and w_1=e_2; order the remaining vectors to label the other slots. Let V=F_2^4 minus {0}. Assign each palette label x a nonzero normal v(x) in V, with exactly 858 labels of each normal. Define the intermediate complementary blocks

    K_i={x: w_i dot v(x)=0}.

Each K_i contains 7*858=6006 labels. We now specify an assignment ensuring K_0 subset B_0 and K_1 subset B_1, without a search.

Split the palette by its original S membership at indices 0,1. Counts are

| Original category | Label count | Assigned normal category |
| --- | ---: | --- |
| S contains both 0,1 | 3432 | 2574 labels to normals 00** other than 0000; remaining 858 to normal 1111 |
| S contains 0 only | 3432 | four normals 01**, 858 each |
| S contains 1 only | 3432 | four normals 10**, 858 each |
| S contains neither | 2574 | normals 1100, 1101, 1110, 858 each |

The counts follow from 2*binomial(13,6)=3432, 2*binomial(13,7)=3432 and 2*binomial(13,8)=2574. Within each row, assign in any declared lexicographic order to the displayed normal classes. This defines a finite bijection with the required class counts; no enumeration or primary-source design property is needed.

A label whose normal has first coordinate zero comes from an original code containing 0, and similarly for coordinate 1. Thus K_0 subset B_0 and K_1 subset B_1. Set destination complementary blocks and supports as

    E_0=B_0, E_1=B_1, E_i=K_i for i>=2;
    C_i=P minus E_i.

Therefore C_0=D_0 and C_1=D_1. For i>=2, |C_i|=12870-6006=6864>=6006, so all original floors hold.

Every triple of distinct palette labels lies in some K_i: three homogeneous linear equations w dot v(x)=0 in four variables have a nonzero solution w. Repeated normal classes cause no difficulty. Replacing K_0,K_1 by the larger B_0,B_1 retains triple coverage, so every triple is missed by some C_i. Consequently tau(C)>=4.

For the upper bound select four palette labels with normals 1100,1000,0010,0001. These vectors are linearly independent. The label with normal 1100 comes from the original category containing neither 0 nor 1, by the assignment table. No nonzero w is orthogonal to all four normals, so their four-label set is contained in no K_i. It is contained in neither B_0 nor B_1 because of that first label. Thus it is contained in no E_i, equivalently it hits every C_i. The labels are distinct because their normals differ. This proves tau(C)=4 independently of mere pair redundancy.

## 5. No directed completion after the prefix

At D, slots 0 and 1 already equal C, so A11 permits no remaining events there. At every other slot, every support addition is forbidden by its explicit unique missed-pair witness from Section 2. Every support deletion is forbidden by the original floor. D differs from C since tau(D)=3 and tau(C)=4, so the remaining event set is nonempty.

Therefore NO first remaining destination-directed event is legal. No ordering or interleaving of the remaining symmetric-difference events can complete this prefix. This excludes every directed continuation of THIS prefix, not every A -> C schedule.

In the unrestricted native graph the same first-move argument has another consequence: every lower path D -> C must initially delete an incidence at root 0 or 1. Those roots already equal their destination, so this is a compulsory temporary deletion of a destination incidence. Roots are not forbidden to be revisited in the native carrier. Returning D -> A by reversing the 12010 additions is legal, stays in {3,4}, and enables the alternative below. This is an obstruction to insisting that completed roots remain completed after reaching D, not a primitive disconnection.

## 6. Another complete destination-directed schedule exists

Keep A_0={z_0} and A_1={z_1} unchanged while repairing all other roots to C. With these singleton roots fixed, the ONLY possible two-label transversal is H_0={z_0,z_1}. Thus the lower guard is exactly the existence of at least one other root missing H_0.

At the source, every root indexed by R misses H_0, giving eight choices. At C, the two normal vectors v(z_0),v(z_1) both begin 11. Their homogeneous common orthogonal subspace has dimension at least two, hence at least three nonzero vectors. None is w_0=e_1 or w_1=e_2, since both normals have first two coordinates equal to one. Hence at least three roots with index >=2 have C_i disjoint from H_0.

Choose an old protecting index i in R and a destination protecting index j>=2 with j!=i. First repair root j through A_j -> A_j union C_j -> C_j, adding missing destination incidences individually and then deleting source-only incidences. The unchanged root i protects H_0 throughout. Then keep the completed C_j fixed while repairing ALL other roots with index >=2 in the same add-then-delete fashion, including root i. C_j protects H_0 throughout. Each replacement respects its original floor by expansion from a permitted source and contraction to a permitted destination.

After these 13 roots equal C, expand the two singleton roots to C_0 and C_1 by their original destination additions. Every state in this last stage is componentwise contained in C, so tau>=tau(C)=4; floors remain valid.

Every endpoint symmetric-difference incidence has now been toggled exactly once, common incidences stayed fixed, and the labelled destination is reached after exactly |E+|+|E-| events. This is a complete A11 destination-directed path with tau>=3. Protection is explicitly transferred from an old H_0-missing root to a completed new one BEFORE releasing the singleton constraints. The construction is finite and supplies its next legal root and incidence at every stage.

This alternative can have upward excursions; no unproved exact-four restoration claim is made at its intermediate completed roots. Accepted maximum-layer removal converts this finite lower path between exact-four endpoints to a native path in {3,4}, possibly outside the destination-directed class. It is an inherited theorem, not independently recertified here.

## 7. Scientific conclusion and unchanged primary gate

**Safe-prefix extension is FALSE.** Native legality of all past events, exact endpoint redundancy, and decreasing remaining-event count do not guarantee a legal next destination event. Two prematurely expanded singleton constraints can strand thirteen compact roots, each protected against every addition by a private pair. At D, renewal necessarily starts by revisiting one completed root.

**A11 universal schedule existence remains OPEN.** This example has an explicit complete destination-directed schedule, so it is not a class obstruction and does not satisfy the negative alternative of A11's primary completion gate. It identifies why arbitrary safe choices are insufficient and why protecting constraints must sometimes be held until the new constraints are established.

The carrier has 15 roots, 12870 labels, two floors one and thirteen floors 6006; it is not the q=4/uniform-floor-three unresolved diagnostic. All moves use its fixed original palette, slots and native support sizes. The elementary F_2^4 argument is a finite incidence construction for this analytical example, not an inserted physical geometry or external alignment rule. General q>=4 primitive/nested connectivity remains OPEN or conditional as before; native lifting retains accepted child-interface conditions. No implementation certification, efficiency, originality or physical claim is made.

