# v16.25 — Type ledger and proof obligations (pre-adjudication)

| ID | Object | Type/provenance | Status |
|---|---|---|---|
| R1 | X | finite rooted common-Genesis prefix tree; v16.24 C1 | inherited |
| R2 | Y_i | actual root-containing prefix-closed retained view of X | inherited |
| R3 | Z_i subseteq Y_i | actual retained subview, literal inclusion; ancestral retraction r_YZ maps each node to longest retained ancestor | inherited operation |
| R4 | P_YZ | Q^Y -> Q^Z, finite sum over r_YZ fibers | inherited v16.21/v16.23 |
| R5 | V=(Y_i), Z=(Z_i) | indexed covers with the same union U for comparison in this campaign | declared admissible comparison |
| R6 | A_i^V(v)=Ch_U(v) intersect Y_i | finite child-incidence set | derived |
| R7 | tau_v(V) | minimum number of A_i^V(v) covering Ch_U(v), zero at leaves | v16.24 C7 |
| R8 | h(V)=max(1,max_v tau_v(V)) | least positive worst-case consistency order | v16.24 H0–H3 |
| R9 | compatible c | subtree coordinates on fixed U | inherited v16.23 O3/v16.24 H1 |

## P1 — refinement monotonicity

For every i and v, Z_i subseteq Y_i gives A_i^Z(v) subseteq A_i^V(v). If indices S cover all children using Z, the same indices cover them using Y. Thus the minimum cover cardinality satisfies tau_v(Z)>=tau_v(V). Taking maxima and the positive-order convention gives h(Z)>=h(V).

This proof uses the same U. It makes no claim when pruning changes the union.

## P2 — exactness and equality

v16.24 H2–H3 applies to every actual refined cover Z. Hence h(Z) is exactly max(1,max tau_v(Z)), not merely an upper bound. Equality of h values is therefore exactly equality of these maxima after the same order-one convention. Individual tau values may increase without changing h; no stronger equality criterion is assumed.

## P3 — composition of actual pruning

For W subseteq Z subseteq Y prefix-closed, let r_YZ and r_ZW be longest-retained-ancestor maps. For y in Y, r_YZ(y) lies on y's ancestor chain. The W ancestors of y and of r_YZ(y) have the same longest member because W subseteq Z. Therefore r_YW(y)=r_ZW(r_YZ(y)).

For x in Q^Y and w in W,
(P_ZW P_YZ x)(w)
= sum_{z:r_ZW(z)=w} sum_{y:r_YZ(y)=z} x(y)
= sum_{y:r_YW(y)=w} x(y)
= (P_YW x)(w).
This is a fiber partition argument, not a matrix assumption.

By induction, any finite factorization of nested retained subviews has the same final retraction and pushforward. Child incidence, tau and h depend only on the actual final views, so they are factorization-independent.

## P4 — fixed-union feasibility versus audit order

For fixed compatible subtree coordinates c on U, the unique signed source is x_U(v)=c_v-sum_{w in Ch_U(v)}c_w. This depends on U and c, not on which cover presents c. Therefore its global nonnegative feasibility is unchanged under same-union refinement. What can increase is h: fewer child incidences per view can require more views jointly to expose the same full node inequality.

## P5 — sharpness after refinement

Apply v16.24 H3 to the actual refined cover. At a vertex attaining t=h(Z)>1, assign c=d-1 to that vertex and its ancestors, one to each immediate child, zero elsewhere. Every subfamily with fewer than t refined views omits a child and is feasible; a minimum t-view child cover exposes -1. Local marginals must be computed using the actual refined fibers. Thus sharpness is inherited as a theorem schema, not by copying old arrays.

These arguments are written before the new adjudication implementation. The executable campaign must be able to reject violations of them.

**Time is pruning / ordered recoverability update.**
