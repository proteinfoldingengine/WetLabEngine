# Unit excursion can require unbounded simultaneous endpoint departures

Status: candidate analytical theorem for independent review. Parent checkpoint: 78c289eb5a0495ed176f80bd96273a5618fa5521. This is a symbolic argument, not an enumeration campaign. Native palette, labelled slots, positive floors and one-incidence primitives are unchanged. No implementation or numerical execution is authorized by this document.

## 1. The exact-endpoint family

For any integer m>=6, let P be the m^2 ordered-pair labels (u,v), with 1<=u,v<=m. Define row supports R_i={(i,v):1<=v<=m} and column supports C_i={(u,i):1<=u<=m}. These names describe subsets of labels, not added native structure.

Use r=m+1 labelled roots, each with floor h=m. The exact endpoints are

    A=(R_1,...,R_m,R_1),
    C=(C_1,...,C_m,C_1).

Every support has size exactly m. The m disjoint row roots require m hitting labels, and one label per row suffices; the repeated R_1 adds no constraint. Thus tau(A)=m, and likewise tau(C)=m. Set q=m and t=m-1.

The carrier is compact at both endpoints and has

    k=m^2 < (m+1)m=sum_i a_i,
    delta=sum_i(k-a_i)-(q-1)k=m(m-1)>0.

It therefore has higher uniform floors, a palette smaller than the sum of floors, positive derived capacity slack, and all exact-endpoint redundancy conditions. Those facts do not supply the restricted buffer schedule below.

## 2. A counting bound for mixed row/column states

At any root tuple X on this palette, classify each labelled slot relative to its OWN endpoint supports:

- old if X_i=A_i;
- new if X_i=C_i;
- intermediate otherwise.

No slot is both old and new, because its row and column supports differ for m>=2. Let o,n,d be the respective numbers, so o+n+d=r. This definition does not count how many incidences differ, nor which root is currently edited.

**Lemma P1.** For any such tuple with nonempty roots,

    tau(X) <= max(o,n)+d.

Pair min(o,n) old roots with new roots. Every row intersects every column in a palette label; choosing that label hits both roots in the pair. Choose one label from each unpaired old/new root and from each intermediate root. This uses at most max(o,n)+d labels. Repeated row or column supports can only reduce the number needed. No floor condition beyond nonemptiness is used in this bound.

## 3. Unbounded participation is necessary on every lower-guard path

**Theorem P2.** Every finite one-incidence path from A to C with tau>=m-1 at every state contains a state with at least m-3 intermediate roots.

At the start n-o=-r; at the end n-o=r. One incidence change affects one slot. It cannot change that slot directly from its old support to its new support or vice versa: those distinct supports have the same cardinality m and cannot differ by a single toggle. Hence n-o changes by at most one at each primitive. The integer sequence must visit n-o=0.

At such a balanced state o=n, whence o=n=(r-d)/2. P1 and the required lower guard give

    m-1 <= tau(X) <= (r-d)/2+d = (m+1+d)/2.

Therefore d>=m-3. This applies to every admissible path, including nonmonotone paths, repeated root edits and arbitrary temporary supports. It uses only nonempty roots and the one-incidence move rule, so allowing smaller intermediate floors would not evade this counting argument.

The conclusion concerns many roots being away from both endpoint supports at the same STATE. It does not introduce simultaneous native moves. The number of roots edited by any one primitive remains one, and the total excursion need not exceed one. P2 is not a lower bound greater than one on the excursion.

## 4. A one-unit path nevertheless exists

The palette permutation (u,v)->(v,u) maps A to C, including the duplicated final slot. It is a product of the finitely many transpositions swapping (u,v) with (v,u) for u<v.

For completeness, each palette transposition has a primitive unit-band realization. Let Y be a current exact-m tuple, sigma swap labels x,y, and U_i=Y_i union sigma(Y_i). Any transversal H of U can be made into a transversal of Y by adding at most one label: if H uses exactly one of x,y, add the other; if it uses neither or both, no repair is needed. Thus tau(U)>=m-1. Both Y and sigma(Y) have transversal m and the same support sizes.

Expand Y to U one incidence at a time, then contract to sigma(Y). During expansion the tuple contains Y, so its transversal is at most m; during contraction it contains sigma(Y), with the same bound. Every intermediate tuple is contained in U, giving the lower bound m-1. Each support contains its starting or destination support, so all floors m hold. Completed transpositions restore exact m. Concatenation reaches C in a finite path with tau in {m-1,m}.

This is the already accepted label-transposition mechanism applied to the explicit family, with its argument repeated to make coexistence of the lower participation bound and one-unit repair transparent. It is not a new claim that symmetry exchange was previously unresolved.

## 5. The universal adaptive one-buffer conjecture is false

The adaptive method of ADAPTIVE_BUFFER_RENEWAL.md holds all nonbuffer roots at their old or new supports except for the single root currently undergoing its union replacement. At any state it has at most two intermediate roots: the buffer and that active nonbuffer root. At boundary buffer changes, it has at most one.

For m>=6, P2 requires at least m-3>=3 intermediate roots on every lower-guard path. Therefore NO choice of buffer slot and NO order of the remaining roots can satisfy the adaptive one-buffer criterion for this endpoint family. In particular, the universal existence statement left open in the prior checkpoint has a negative answer. The actual one-unit connectivity statement remains true for these same endpoints by Section 4.

More generally, any architecture allowing at most b arbitrary intermediate buffer roots and at most one additional active root, while all other roots remain at their own old or new supports, requires

    b+1 >= m-3,  hence b>=m-4.

This remains a necessary bound if buffer identities change or roots are revisited, as long as the stated per-state bound on intermediate roots is maintained. It is not sufficient. No fixed buffer count b can make this architecture universal over m. A method that leaves other completed roots at temporary supports must count those roots as intermediate too.

Thus adding one more fixed buffer repeatedly cannot resolve the general theorem. An unrestricted primitive repair must permit a growing number of roots to retain temporary supports, or use another structural representation that accounts for that participation honestly.

## 6. Scientific and native limits

The excursion bound controls the deviation of the hitting number; it does not bound how many root supports can participate in the ordered repair. Endpoint-relative participation d is neither a conserved invariant nor the excursion itself. This family separates those quantities with an unbounded necessary participation bound and an explicit unit-band path.

No new endpoint connectivity class, universal higher-floor theorem, sharp participation optimum, physical law, or implementation certification is claimed. The example lies in an already connected symmetry class, which is essential to distinguishing method failure from a native barrier. Originality relative to mathematical literature has not been established.

P2 is a root-level theorem. It also applies to a projected native path if its roots remain nonempty, each native move changes at most one root incidence, and the projected parent retains tau>=m-1. Interior-only moves leave the counting statistic unchanged. This conditional observation is not a full native construction or a barrier claim. Lifting the explicit upper path uses the previously accepted child-interface assumptions.
