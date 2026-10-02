# Positive-slack exchange through disjoint root witnesses

Status: candidate analytical theorem; independent review pending. Parent analytical head a1d56d47dd733ed389661f7bc987413cca94762e. No implementation, enumeration or numerical execution. Earlier accepted proof files remain unchanged.

## 1. Problem and result

Use the same width-floor carrier: r nonempty roots A_i subset P, |P|=k, |A_i|>=a_i>=1; primitive moves toggle one incidence. Fix q>=3 and exact-q endpoints, where tau is the minimum hitting-set size. Complements B_i=P\A_i have capacities b_i=k-a_i. Keeping tau>=q-1 is equivalent to covering every (q-2)-subset with these complementary blocks.

Call an endpoint protected if it has q pairwise-disjoint roots. The indices of these roots are its witnesses. Nonemptiness makes these roots require q distinct hitting labels. This is a structural condition on exact endpoints, not a consequence of exactness in general.

**Theorem J.** All protected exact-q endpoints on the same palette and floor vector belong to one component of the root graph with tau in {q-1,q}. Their witness indices need not agree. The construction works at arbitrary arity and arbitrary positive slack, and needs no additional label.

**Theorem K.** Protected exact-q endpoints exist if and only if the sum of the q smallest floors is at most k. In particular, when that sum exceeds k, no path can pass through a protected state anywhere in this width-floor carrier. This is an obstruction to this method, not to one-unit connectivity itself.

We prove both results constructively. We also give an exact-q family that violates K's existence condition despite positive slack and the full exact-endpoint redundancy hierarchy. Thus deficient-label counts and total capacity do not imply the witness condition.

## 2. Why degree slack alone is not the exchange guard

For any lower-guard tuple A and a permitted addition x to root A_i, the addition violates tau>=q-1 precisely when there is a set H of q-2 labels such that x is in H, H misses A_i, and H hits every other root. Proof: such H hits the modified tuple. Conversely, a hitting set of size at most q-2 for the modified tuple must fail on the old A_i alone and use x, since the old tuple obeys the lower guard. Extend it to q-2 labels if necessary; any such extension still misses the old A_i, since otherwise it would hit the old tuple in q-2 labels. Feasibility supplies k>=q.

This criterion depends on which roots a prospective hitting set misses, not just the degree of x. At an exact-q endpoint no such H exists, consistently with the one-block replacement lemma. After a first excursion it may exist. We do not assert that incidence deficit alone rules it out.

Protected roots supply a different, directly checkable guard: untouched disjoint roots require separate hitting labels. The following proof uses those roots instead of claiming that a deficient label is automatically a safe buffer.

## 3. Normalizing the nonwitness roots

Let W be q witness indices at an exact-q endpoint. Expand every root outside W to P, one incidence at a time, leaving the witness roots fixed. The witnesses force tau>=q. Expansion cannot increase tau from q. Thus all these moves stay exactly at q and preserve floors.

Thereafter the nonwitness roots are redundant: any hitting set for the q nonempty witness roots hits P. All q witness roots remain pairwise disjoint. They need not yet cover P or have their floor sizes.

## 4. Moving the witnesses to a common set of indices

Order the indices by (a_i,i), using the supplied child order to break ties. Let W_* be the first q indices. Suppose W differs from W_*. Choose j in W_*\W and i in W\W_*. Then a_j<=a_i. The root A_j currently equals P.

Contract A_j to the current A_i by deleting incidences outside A_i. This is floor-safe because |A_i|>=a_i>=a_j. During contraction the original witness set W remains disjoint and forces tau>=q. Choosing one label from each original witness hits every root: A_j continues to contain A_i and all other nonwitness roots equal P. Thus tau=q throughout.

Now regard (W\{i}) union {j} as the witnesses. Its roots have exactly the same disjoint supports as before. Expand A_i to P. The new witnesses force tau>=q, and expansion cannot raise tau. All nonwitness roots are once again P.

This replaces one witness outside W_* by one inside it; |W intersect W_*| strictly increases. After at most q replacements the witnesses are W_*. Equal floors cause no problem because the fixed ordering selects W_* and a_j<=a_i still holds. No simultaneous moves are used.

## 5. Finite partition exchanges on the common witnesses

Assign any label outside the union of the W_* roots to one selected witness root, one incidence at a time. Disjointness is preserved and eventually the witness roots partition P. All such states have tau=q. Write these q indices in their supplied order as w_1,...,w_q. Choose common target part sizes

    c_{w_j}=a_{w_j} for j>=2,
    c_{w_1}=k-sum_{j>=2} a_{w_j}.

They meet the floors because existence of the original disjoint witnesses implies sum_{i in W_*} a_i<=k.

If a current part has size above c_i and another below c_j, transfer one label x from the former to the latter: first add x to the receiving root, then delete it from the donor. Before deletion the donor has size strictly above c_i>=a_i. Both moves respect floors. The q-2 other parts are disjoint from the affected pair and each other; the affected pair requires one or two hitting labels. Thus the intermediate transversal is q-1 or q, and the completed transfer restores a partition with tau=q. Each transfer reduces sum_i ||A_i|-c_i| by two. This reaches the fixed target sizes in finitely many transfers.

Choose a canonical partition of the ordered palette with those sizes, for example consecutive intervals. To fix a misplaced label x currently in part i and destined for part j, choose y in j that is not destined for j. Such y exists because j has its target size and lacks x. Perform

    add y to A_i; add x to A_j; delete x from A_i; delete y from A_j.

The same q-2 untouched parts and nonempty affected pair keep tau in {q-1,q}; floors hold throughout. At completion x is correct and no previously correct label moved. Finitely many swaps reach the canonical partition. Every nonwitness root remains P.

Each protected exact endpoint has therefore been connected to the same canonical tuple. Reverse the path for the second endpoint and concatenate. This proves J, including distinct witness sets. Paths need not have q disjoint roots at their inexact intermediate states; their guard is proved directly.

## 6. Existence and a precise limitation

Necessity in K: any q disjoint roots have total size at least the sum of their floors and at most k. Their floor sum is at least the sum of the q smallest floors.

Sufficiency: if those q smallest floors sum to at most k, choose disjoint nonempty subsets of P meeting those floors, use them as roots W_*, and set all other roots to P. The resulting tuple has transversal exactly q. This proves K. Theorem J connects all protected endpoints; K does not assert that all exact endpoints are protected or can reach this class.

**Analytical obstruction family for this method.** For any integer m>=2 take m disjoint three-label palettes. On each palette {u,v,w}, use the three roots {u,v}, {v,w}, {u,w}. All 3m floors equal 2. Then

    r=3m, k=3m, q=2m,
    d=r-q+1=m+1,
    delta=dk-sum_i a_i=3m(m-1)>0.

Each triangle requires exactly two hitting labels, and the palettes are disjoint, so tau=2m=q. The sum of the q smallest floors is 4m>3m=k. Hence no protected state exists anywhere with these floors and palette, although these are valid exact-q endpoints. Their complements consequently satisfy every exact-endpoint covering and local-capacity inequality in EXACT_ENDPOINT_CAPACITY.md. Every label has degree 2<d and is deficient; this does not create the missing witness class.

This is a symbolic family proved directly, not a finite search or numerical campaign. Already m=2 concerns the pair-cover lower guard, and higher m gives higher-subset guards. We claim neither that these states are disconnected nor that their native one-unit repair fails. The family rules out making the witness condition a universal consequence of positive slack, even when all exact-endpoint conditions are retained.

## 7. Remaining obligation and native boundary

Theorem J resolves the protected endpoint class uniformly over arity, target and slack. The saturated normal form from Theorem H lies in this class; the new proof also allows slack, changing witness indices, unused labels and variable part sizes.

To establish a universal theorem, one must handle exact endpoints without disjoint witnesses. When K's inequality fails, no route through this normal form is possible in the stated carrier. The next structural exchange mechanism must preserve overlapping witnesses or directly protect complementary subset covers. When K's inequality holds, accessibility of the protected class from every unprotected exact endpoint is still unproved.

The earlier conditional native lifting applies to the constructed root paths when children supply the accepted interface. Failure of this method, including nonexistence of a protected root state, is not a native barrier proof. A native unit path can have additional freedoms outside the fixed minimum-exact-width carrier.

Independent review must check the exact unsafe-addition criterion, witness relocation, all intermediate guards/floors, both termination arguments, K's equivalence and the obstruction family's limited meaning. No implementation, efficiency bound, numerical certification, universal positive-slack theorem or physical interpretation is claimed.
