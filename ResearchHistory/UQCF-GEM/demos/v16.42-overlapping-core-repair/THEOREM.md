# Unit repair for an overlapping core with arbitrary binary depth

Use the admitted supports, primitive incidence moves, internal hitting numbers and independent B1, Binf, Bs of v16.41. Let T(d,m) be an m-leaf star wrapped in d binary parents, each with a side leaf, where d>=0 and m>=3. Set k=d+2, root support K, q0=2 at every internal vertex and zero at leaves.

**Theorem.** The exact-profile graph has k!/2 components, each with 3^m-2*2^m+1 states. Between distinct components B1=Binf=Bs=1; the separate LEX optimum is (1,1,1). Within a component all barriers are zero. This is a compositional overlapping family, not a universal or indecomposability theorem.

## Saturation and exact components
For two child supports, hitting number2 means disjointness. Each binary side branch therefore uses labels disjoint from all lower branches. The bottom core needs at least two labels because its hitting number is2. Its d side leaves each need at least one label. These disjoint requirements exhaust k=d+2 labels: each side leaf is a singleton, the core palette has exactly two labels, and each spine support is exactly the union of the palettes below it. Slack internal incidences are impossible by disjointness and exhaustion.

Write the two core labels as a,b. Each core leaf support is A={a}, B={b}, or C={a,b}. Hitting number2 is equivalent to the occurrence of at least one A and at least one B. Inclusion-exclusion gives 3^m-2*2^m+1 such configurations. There are k!/2 assignments of ordered side labels with an unordered remaining core pair. A primitive exact move cannot change a side singleton without leaving the saturated characterization. It remains to prove each fixed assignment is connected.

## Zero-cost core normalization
Normalize to leaf0=A, leaf1=B, all remaining leaves C. If leaf0 is the unique B, retain an A at some other leaf i and choose a third leaf t (m>=3). Make t into B, passing through C if necessary, while i retains A and leaf0 retains B. Then change leaf0 to A through C. In every other case, make leaf0=A directly, passing through C if needed; another B remains whenever leaf0 initially was B. Next make leaf1=B through C if necessary, with leaf0 retaining A and the prior B witness retained until the new B exists. Expand all remaining singletons to C. Both singleton witnesses remain at every step, so q is unchanged. All changes occur in leaves, preserve admission, and do not affect any ancestor's q. Reversing normalization connects any two states with the same side assignment.

For m=2 the two configurations (A,B) and (B,A) are isolated in the exact fiber. The third-leaf assumption is essential; the numerical boundary control must observe this.

## Fresh-label substitution lemma
In any admitted rooted subtree, suppose a occurs and b is absent throughout it. Its outside parent, if any, must already contain b when its root changes. Add b at every vertex containing a in top-down order, then remove a from those vertices in bottom-up order. Prefix inclusion remains legal: additions find b already at the parent; removals wait until children no longer need a. No support becomes empty because its replacement b is present.

Every internal hitting number is unchanged. During the addition phase, the set of children hit by b is contained in the set hit by a; replacing b by a in any hitting set never worsens coverage. Other labels are unchanged, so the optimum is unchanged. After all additions, b has the original a coverage everywhere. During removal the current a coverage is contained in b coverage; b replaces a in a minimum cover, again preserving the optimum. This proof requires b to be fresh in the whole subtree, not merely absent at one leaf.

## Exchanges between terminal palette blocks
Terminal blocks are the side leaves and the bottom core. Their palettes are disjoint. Select a in one block and b in another, with lowest common ancestor v. Let Va be all vertices containing a in the selected child subtree of v; define Vb similarly. Add a on Vb top-down, then b on Va top-down; remove a on Va bottom-up, then b on Vb bottom-up. Do not change v or any ancestor.

Below v, each operation is a fresh-label clone or its completed replacement as in the lemma, so all internal hitting numbers stay fixed. At v (a binary vertex), the originally disjoint child supports intersect during the exchange, giving q_v=1, and return to disjointness at the end, giving q_v=2. No other coordinate changes. Admission follows from the same ordering and nonemptiness argument. Both labels already lie in S_v, so the initial child additions are legal. Thus every exchange has all three state costs <=1.

For any endpoint pair, visit side leaves in fixed order. If the current side label differs from its target, exchange it with the target label in another terminal block. Previously fixed sides cannot contain this target label because endpoint side labels are distinct. Each exchange therefore fixes one further side without disturbing earlier ones. Once all side labels agree, the core palette agrees; join the two core states through the zero-cost normal form. This gives a finite admitted path between every pair. Distinct exact components have lower bound1 for each scalar objective; the construction supplies matching upper bounds. The same path gives the separately defined LEX triple. For d=0 the exact fiber is connected and there are no distinct component pairs.

## Scope of evidence
The proof is for every d>=0,m>=3. Finite validation covers only the six preregistered parameter pairs. It independently verifies every admitted state and edge, target component and endpoint pair, every target-state normalization, and the exchange path certificates. Passing this campaign does not settle unit barriers for arbitrary overlapping profiles. The two-label core and saturated disjoint outer palettes are substantive assumptions.
