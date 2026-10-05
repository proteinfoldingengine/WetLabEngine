# A11.X61 - hybrid-boundary batch handover with competing covers

Date: 2026-10-05 UTC.
Analytical parent: d5f9cf86d32456b07d5c48a38557899c9bbfc8ee.
Scope freeze: 1a6dfe1f2937fcc7eb17504b3560ab2829c562c6.
Status: exact candidate for fresh independent whole-argument review.
Analytical only; no numerical execution.

## 1. Native theorem on actual labelled roots

Fix a finite palette P and ORIGINAL labelled root indices I. Root i has exact source A_i subset P, exact destination C_i subset P, and its SAME original positive floor f_i<=min(|A_i|,|C_i|). Both full endpoint tuples have transversal exactly four. A primitive adds or deletes ONE incidence in ONE original root; temporary larger supports are allowed.

Partition I into nonempty ordered batches
B_1,...,B_h.
For 0<=j<=h define the exact hybrid boundary tuple H_j by
H_j(i)=C_i if i lies in B_1 union ... union B_j,
H_j(i)=A_i if i lies in B_(j+1) union ... union B_h.

Assume:

(U) For every j there is an ACTUAL physical set K_j subset P, |K_j|<=4, hitting every support of H_j.

(L) For every physical pair D subset P, |D|=2, either:
- some actual root w has (A_w union C_w) intersect D empty; or
- there are actual roots v,u with C_v intersect D empty, A_u intersect D empty, and batch(v)<batch(u).

Then there is an explicit native path from A to C with 3<=tau<=4 after EVERY primitive, all original floors, exact full labelled restoration, and exactly
sum_i |A_i symmetric-difference C_i|
primitives. This is the unavoidable GLOBAL endpoint Hamming minimum.

Call this X61B, the hybrid-boundary batch theorem.

No unique endpoint cover, common fixed cover, colored representation, root type, equal floor, compactness or supplied safe primitive list is assumed. The finite ordered partition, boundary covers and actual witnesses are the declared sufficient certificate. Failure to supply them is only failure of this method.

## 2. Construction and upper safety

For j=1,...,h perform two finite phases on ALL roots in B_j, in fixed original index and palette order:

ADD phase: add every incidence in C_i minus A_i that is absent.
DELETE phase: after ALL batch additions finish, delete every incidence in A_i minus C_i that is present.

At the start of batch j the tuple is exactly H_(j-1). K_(j-1) hits it. During additions:
- every earlier-batch root stays at C_i;
- every later-batch root stays at A_i;
- every active batch root contains A_i.
Therefore every K_(j-1) intersection present at the boundary persists. K_(j-1) hits EVERY state through the last addition.

After all additions, every active batch root contains BOTH A_i and C_i. K_j hits H_j: it hits C_i for every active/earlier root and A_i for every later root. Hence K_j hits the all-added state. Switch the existential upper witness there; this is not an incidence edit.

During deletions every active support retains C_i. Earlier and later roots remain at their H_j endpoints. Thus K_j hits every deletion state and the exact boundary H_j.

This proves tau<=4 at every primitive, including partial additions, partial deletions and arbitrary coexistence of original roots in the same batch. A K_j of size below four remains a valid upper bound; it may be extended when a four-set identity is desired.

This differs from X51's strict block-stable interface. No one cover must hit BOTH endpoints of every active root before its additions. The witness changes only after the whole batch contains its destination endpoints.

## 3. Actual lower witnesses

Fix a physical pair D.

If w is a common union witness from(L), every intermediate support of root w is contained in A_w union C_w. Hence it avoids D even while w itself changes.

Otherwise choose v,u from(L), and put p=batch(v)<batch(u)=q. Until batch p begins, u is untouched at A_u and avoids D. Throughout every addition/deletion in batch p, u remains untouched because q>p. At the end of batch p, v is exactly C_v and avoids D. It remains completed during every later batch, including when u changes.

Thus an ACTUAL original root avoids D after every primitive. Shared roots may witness many pairs simultaneously; no independent capacity is allocated. Since every two-label set fails to hit the tuple, no smaller set hits it either. Therefore tau>=3 throughout.

The proof supplies all pair safety on the SAME batch schedule as the upper covers. It does not combine separately chosen lower and upper paths.

## 4. Floors, continuation, termination and exact minimum

Every listed addition is absent and every deletion present. During additions the root contains A_i; during deletions it contains C_i. Its size is therefore at least min(|A_i|,|C_i|)>=f_i, including unequal saturation. The palette, root identity and floor never change.

The finite ordered lists of batches, roots and endpoint-differing incidences give an actual next primitive whenever work remains. Empty lists are skipped without fictitious moves. The total pending scheduled incidence count decreases after every primitive and terminates at C_i in every original slot.

Common incidences never change. Every incidence in A_i symmetric-difference C_i changes exactly once. Any native path between the exact endpoints must toggle each such incidence at least once, so the count is the global outer endpoint Hamming lower bound and is attained.

For finite repeated endpoint legs, a fresh qualifying certificate at each exact restored boundary yields minimum per leg. The concatenation need not be globally shortest between outermost endpoints.

## 5. Infinite competing-cover family

Fix m>=9, roles G={0,...,m-1}, physical singleton palette P={x_s:s in G}, and cyclic physical-label permutation
pi(x_s)=x_(s-1)
with indices modulo m. On role-index subsets pi also subtracts one.

Put
K0={0,1,2,3},
M={0,2,5,7}.
For every four-set J subset G with J not in {K0,M}, declare n_J>=1 ORIGINAL labelled copies of root type Q_J=G minus J, with
A_J={x_s:s not in J},
C_J=pi(A_J)={x_s:s not in pi(J)}.
Each copy has any same original positive floor<=m-4, including arbitrary unequal saturation. The omitted masks are not roots or added resources.

Call K2=pi(K0)={m-1,0,1,2} and L={0,1,4,5}.

### Exact competing endpoint covers

At the source, the physical four-covers are EXACTLY K0 and M. If a four-set H is declared, A_H misses it. If H is omitted, any declared A_J disjoint from H would require H subset J and hence H=J, impossible. Thus both omitted masks cover and no other four-set does.

No set T of at most three labels covers. Extend T to a four-set J outside {K0,M}; for |T|=3 there are m-3>=6 extensions and only two omissions, while smaller T has still more. Then A_J misses T. Therefore source tau is exactly four. Permutation gives destination tau four with exact four-cover family {pi(K0),pi(M)}. The endpoint covers genuinely compete; neither endpoint has a unique minimum cover.

The four sets K0,M,K2,pi(M) are distinct for m>=9.

### Pair footprints and the sole transfer obligation

For a physical pair D={x_s,x_t}, its full old/new owner footprint is
F(D)={s,t,s+1,t+1}.
A declared root Q_J has (A_J union C_J) intersect D empty exactly when F(D) subset J.

If |F(D)|<=3, extend it to a declared four-set outside the two omissions. If |F(D)|=4 and differs from both omissions, Q_(F(D)) is a common union witness.

M contains no cyclically adjacent role pair for m>=9. Every size-four footprint is the union of two cyclic adjacent pairs, so F(D) cannot equal M.

The only pair with F(D)=K0 is
D_star={x_0,x_2}.
Indeed starts outside {0,1,2} introduce an outside role, and among starts0,1,2 only0 and2 cover all four positions.

Hence D_star is the SOLE physical pair without a common union witness. Choose actual declared types
v=Q_{1,3,4,6},
u=Q_{0,2,4,6}.
Their masks differ from K0,M and from each other. Destination C_v avoids D_star because {1,3} lies in v's mask; source A_u avoids D_star because {0,2} lies in u's mask.

## 6. Three derived batches and covers

Define distinct declared types
a=Q_L=Q_{0,1,4,5},
b=Q_{1,2,3,4},
c=Q_{m-1,0,1,2},
d=Q_{1,2,5,6}.
For m>=9 these masks and those of u,v are declared and pairwise distinct. None equals K0 or M.

Put ALL original copies of a,b,v in B1; ALL copies of c,d in B2; every remaining original root copy, including all u copies, in B3.

Use boundary covers
K_0=K0,
K_1=L,
K_2=K2,
K_3=K2.

The cover calculation is exact. For any physical four-set K:
- its source exception is Q_K when K is declared, and empty when K is omitted;
- its destination exception is Q_(pi^-1(K)) when that mask is declared, and empty when it is omitted.

K0 has no source exception because it is omitted; its only destination exception is b. Since b lies in B1, K0 covers H0.

L's source exception is a, already in B1; its destination exception is d, still at source after B1. Thus L covers H1.

K2's source exception is c, completed in B2; it has no destination exception because pi^-1(K2)=K0 is omitted. Hence K2 covers H2 and the full destination H3, regardless of all remaining roots.

For lower condition(L), every pair except D_star has its declared common union witness. For D_star, v lies in B1 and u lies in B3, so batch(v)<batch(u). X61B applies.

Therefore every member of this infinite family has a direct native path with 3<=tau<=4, exact original floors, full labelled/noncompact destination restoration and global minimum
sum_{J notin {K0,M}} n_J |J symmetric-difference pi(J)|.
The construction is deterministic after fixed root/palette orders; no numerical search or averaging is used.

## 7. Structural controls and separation

Every root type changes. A nonempty proper four-set cannot be invariant under the transitive one-step m-cycle, so J!=pi(J).

The entire endpoint-union tuple has transversal EXACTLY TWO. D_star hits every union because it has no common union-avoiding root. No singleton hits all unions: its footprint {s,s+1} has a declared four-set extension, giving an actual union root that avoids it.

Thus there is no unchanged background root and no permanent union three-guard. Lower protection genuinely transfers from actual u to completed v.

The family lies outside X60's colored one-anchor/two-outside representation: its roots have size m-4 and its endpoint minimum covers are the competing pairs {K0,M} and {pi(K0),pi(M)}. The batch theorem itself is representation-free and accepts arbitrary source/destination sizes and individual floors.

This does not claim the displayed three covers are necessary; other valid partitions or two-cover paths may exist. It does not prove every arbitrary exact-four pair has an X61B certificate. The result is a reusable sufficient interface plus an infinite family beyond unique covers, not unrestricted native connectivity or universal minimum repair.

## 8. Dependency and remaining direction

X61B abstracts the actual first-new-before-last-old witness principle used by X34/X51 and combines it with X60's inside-batch cover switch. It weakens X51's demand that one cover hit both endpoints of every active root, while retaining explicit actual roots and copy states. The proof above is direct; no frozen theorem is rewritten.

X52 supplies the one-omission comparison and six mask choices. X61's second omission M creates competing endpoint covers. The proof rechecks all cover, footprint and witness properties after that change rather than assuming deletion of a root is harmless.

Remaining: derive existence of a qualifying partition/covers from weaker endpoint invariants, or extend the certificate when lower witness precedence and upper hybrid-cover reachability form cycles requiring partial-root interleaving across batches. A failed partition is method failure. Arbitrary accessibility, unrestricted mixed/directed/higher-target/nested universality and physical interpretation remain open.

No maximum-layer conversion, numerical execution, workflow, implementation, fixture, benchmark, integration merge or new numbered certification. Certified v16.54/v16.55, frozen sources and original evidence remain unchanged. Separate efficiency implementation remains unstarted.
