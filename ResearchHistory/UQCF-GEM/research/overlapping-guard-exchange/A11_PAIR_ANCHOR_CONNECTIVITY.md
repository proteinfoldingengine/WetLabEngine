# A11.X4: one floor-two root suffices for target-four repair

Status: frozen candidate analytical proof for independent review. Scope parent: f74b5afe9a81d2dbf328a515da506a87f401b6f3. Fixed original palette, labelled slots, positive floors and single-incidence moves. No enumeration, numerical campaign, implementation, tests or workflows.

## 1. Theorem and accepted dependencies

Let A,C be permitted exact-four endpoints on a finite ordered palette P, |P|=k, with the same labelled slots and positive original floors a_i. Suppose one selected slot s has ORIGINAL floor a_s=2.

**Theorem X4.** A and C have a finite primitive path with tau in {3,4}, regardless of all other positive floors. The proof constructs the band directly.

Together with independently accepted X3 (a floor-one slot suffices), every exact-four carrier containing ANY original floor at most two has native one-unit connectivity. This is stronger than the accepted all-floors-two/mixed-floors-one-two classes, and does not require the other floors to be small.

Inherited dependencies at integrated baseline 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f:

- OVERLAPPING_CLIQUE_EXCHANGE.md Lemma L: primitive realization of a palette transposition with one-unit band at any exact completed hitting level.
- GENERAL_PARENT_CONNECTIVITY.md Lemma C: capacity-bounded element covers connect through coverage-preserving, capacity-preserving individual block moves when total capacity exceeds palette size.
- X3's common-residual preparation argument is used only for the separate higher-target corollary; accepted Theorem A supplies that corollary's final upper-excursion removal.

These are inherited analytical dependencies, not new implementation certification or independently recertified proofs. Section 6 explicitly checks an additional upper-band property of Lemma C's construction. Main X4 does NOT require upper-excursion removal.

Temporary incidences and repeated toggles are allowed. No universal A11 destination-directed schedule, minimum-floor necessity, all-floors-at-least-three closure or unrestricted nested universality is claimed.

## 2. Make and align an exact pair root

At either endpoint choose a minimum four-label transversal H. In the selected root retain one label of H and one other distinct label, deleting all its other incidences individually. The root has at least two labels and retains its original floor two. Deletion cannot lower tau, and H continues to hit every root, so tau remains EXACTLY FOUR.

Map the retained pair to the same canonical pair T={u,v}, the first two labels of P, using a whole-palette permutation implemented by inherited Lemma L. Every completed transposition is exact four and every intermediate primitive has tau in {3,4}. Root identities, cardinalities and floors are preserved. Track the permuted minimum transversal H, still of size four. At the completed tuple X, X_s=T and tau(X)=4.

Set R=P minus T and n=|R|=k-2>=2. Perform this normalization separately at A and C; reversing the second normalization later restores all original labels and supports.

## 3. Actual roots avoiding BOTH pair labels provide protection

At a normalized endpoint let

    M={i!=s: X_i intersect T is empty},
    Q_i=R minus X_i for i in M.

For each x in R, the three-label set {u,v,x} is NOT a transversal since tau(X)=4. Root s meets it, so some nonanchor root misses all three labels. That root belongs to M and its Q_i contains x. Consequently the Q_i COVER ALL R.

Equivalently the positive-floor supports (X_i) in M have residual transversal g>=2. They lie in R. The tracked four-label cover H must use at least one anchor label to hit T, and at most two labels are in T; therefore H_R=H intersect R has size two or three. It hits every M support, so g<=3. Thus g is either TWO or THREE.

The fixed pair root T together with this ACTUAL M family has transversal exactly 1+g>=3. In particular it excludes every possible two-label transversal of the entire tuple:

- a pair inside R misses T;
- {u,v} misses every M root;
- {u,x} or {v,x}, x in R, misses an M root whose Q_i contains x.

No root guard is inferred merely from restored counts. The source family itself protects every relevant pair while other roots are prepared.

## 4. Exact-four endpoints force STRICT residual capacity

Use a floor-defined partition of the nonanchor slots, the same at both endpoints:

    F={i!=s: a_i<=n},   Z={i!=s: a_i>n}.
    c_i=n-a_i for i in F.

Every M index belongs to F. Let B_i=P minus X_i and b_i=k-a_i. For i in F, b_i=c_i+2. Each Q_i in M has |Q_i|<=c_i. For i in Z, b_i<=1.

**Lemma X4S (derived slack).** Sum_{i in F} c_i >= n+1.

Proof. Coverage of R by the M blocks gives

    n <= sum_{i in M}|Q_i|
      <= sum_{i in M}c_i
      <= sum_{i in F}c_i.

Suppose the last sum were at most n. All inequalities would be equalities. Then the Q_i form a disjoint partition of R, each |Q_i|=c_i, and every F index outside M has c_i=0 and hence b_i=2.

For distinct x,y in R, the triple {u,x,y} must be missed by some root because tau(X)=4. Root s meets it. No Z block can contain this triple, since b_i<=1. No F block outside M can contain it, since b_i=2. Therefore some M block must contain x and y in its Q_i.

But the M partition has at least two nonempty parts: every part has size at most c_i=n-a_i<=n-1, because the ORIGINAL floors are positive. Choose x,y in different parts. No M block contains both, a contradiction. Thus total residual capacity strictly exceeds n, proving the integer bound n+1.

This slack is DERIVED from exact endpoint triple protection and original positive floors. It is not assumed, supplied as a new resource, or a claim that the palette has enough labels to separate every incidence. Zero capacities c_i=0 are allowed.

## 5. Prepare the SAME labelled residual carrier inside the band

Hold root s=T and all source M supports fixed. For each inactive flexible slot h in F minus M, replace its support X_h by the WHOLE R through

    X_h -> X_h union R -> R,

performing individual additions followed by individual deletions. R fits its original floor a_h<=n, and all intermediate supports meet that floor. Expand each Z root to P by individual additions.

The fixed pair root and M family give tau>=1+g>=3 throughout. For the upper bound, the tracked four-label transversal H continues to hit EVERY state: the addition segment contains the old support, already hit by H; the contraction segment contains R, hit by the nonempty H_R. Previously converted flexible roots equal R and are hit by H_R; M supports are unchanged; expanded high roots retain their old supports. Hence tau<=4 throughout all preparation moves.

At completion the pair root is T, every F support is in R at its ORIGINAL floor, and every Z support is P. The newly inserted R roots impose no extra requirement on the nonempty M residual cover, so the residual transversal remains g in {2,3}. More generally for ANY subsequent tuple Y on this carrier,

    tau(full lifted Y)=1+tau_R(Y),

because hitting T requires one label of T while the F supports require a residual cover inside disjoint R; full-palette Z roots are redundant.

This supplies a SAME palette R, SAME labelled index set F and SAME positive original floor vector at both endpoints, even though M differed between them. |F|>=2 because its residual positive-floor supports have transversal at least two. Their complementary blocks Q_i=R minus Y_i have capacities c_i<=n-1 and cover R.

Prepared completed stages may have full transversal THREE. This is allowed one-unit defect, not a claim that exact four has been renewed at each stage.

## 6. Element-cover renewal has a direct residual {2,3} band

**Lemma X4B.** For a palette R of size n>=2, capacities 0<=c_i<=n-1 with sum c_i>=n+1, and covering block tuples whose complementary supports have transversal in {2,3}, inherited Lemma C's construction can be carried out with complementary transversal in {2,3} at EVERY primitive.

Here is the required additional band check, rather than assuming it from the lower-cover theorem:

1. Select one current owner of every residual label and remove its other block copies individually. Element coverage and capacities persist. Removing a block incidence ADDS a support incidence, so transversal cannot increase from its starting value at most three. Coverage excludes all singleton transversals, giving the lower bound two.

2. At the resulting owner partition, transversal is EXACTLY TWO. All singleton labels are contained in an owner block, so no singleton hits the complementary supports. At least two owner blocks are nonempty, since each capacity is at most n-1. Two labels owned in different blocks are contained together in no block, so their pair hits every complementary support.

3. Use Lemma C's owner transfers, including its existing spare bin when a target bin is full. Each transfer consists of adding the label to its new block before deleting its old copy. It starts and ends at an owner partition of exact level two. The intermediate block addition is a single support deletion preserving positive floors; it can increase transversal by at most one. Therefore the intermediate level is at most three. Coverage persists, so it is at least two. When buffering is needed, the two transfers are performed sequentially, returning to a partition between them. The spare bin is an EXISTING slot guaranteed by the derived total-capacity bound, not an added root.

4. At the target owner partition, add the target duplicate block incidences individually. Every intermediate block is contained in its target block, so every complementary support contains its target support. Transversal is therefore at most the target value, at most three. Element coverage gives the lower bound two.

This proves X4B. Complementary roots meet their original floors because block capacities are preserved. For the single-deletion bound in step 3, reverse the standard one-addition argument: a hitting set for the old tuple can be repaired by appending one label from the remaining nonempty support. The inherited capacity constraint guarantees that remaining support is nonempty.

Finite termination and next legal owner choices are inherited from Lemma C: a misplaced label is fixed, a misplaced occupant can be moved into an existing spare bin if needed, and previously fixed owners are not displaced. All bin moves are individual incidences. Protection renews by establishing the new owner BEFORE deleting the old one, while the spare-capacity certificate remains valid at every completed partition.

## 7. Connect and restore the exact labelled endpoints

Apply X4B to the two prepared residual endpoints. They have levels two or three, cover R in complements, share F/c_i, and the strict capacity bound was derived in Section 4. Every residual block incidence toggles the corresponding support incidence at its ORIGINAL root index, using only existing labels of R.

Keep T and every Z root P fixed. Exact additivity lifts the residual {2,3} path to full {3,4}. Concatenate the normalization/preparation from A, this middle path, and the reverse of the normalization/preparation from C. All portions have already been shown to stay in {3,4}, preserve floors and use individual incidence moves.

The concatenation is finite: selected-root compaction deletes finitely many incidences; global symmetry is a finite transposition word; each flexible/high root has a finite preparation word; owner normalization/transfers/target duplication are finite; and the reverse destination word is finite. Every original labelled support is restored exactly at C.

This proves X4 DIRECTLY in the one-unit band. No upper-excursion removal is needed for this main theorem; no completed-stage exact-four restoration is inferred from owner counts.

## 8. A restricted higher-target profile corollary

**Corollary X4H.** For q>=4, q-4 original floor-one slots PLUS a DISTINCT original floor-two slot suffice for native one-unit connectivity of exact-q endpoints, with arbitrary other floors.

For q=4 this is X4. For q>=5 choose m=q-4 floor-one anchors, excluding the distinguished floor-two slot. Apply the accepted X3 normalization/common-residual preparation with this m, retaining the original floors. The normalized full level is at least q, so the active residual level is at least FOUR. The residual palette has n=k-m>=4, so the distinguished floor-two slot belongs to the common flexible index set and keeps its original floor two even if initially inactive.

As in X3, additions to the whole residual palette descend from a level at least four to exact four before dropping below it, using the one-incidence bound and eventual level one. The residual endpoints now satisfy X4, INCLUDING its floor-two hypothesis. Its direct {3,4} path lifts by m to {q-1,q}. Reverse the destination construction and apply inherited Theorem A once to the full lower path if normalization/symmetry produced upward excursions.

This uses a SPECIFIC preserved residual floor profile, not a premise of universal target-four connectivity for all floor vectors. No such universal premise is assumed. Additional original floor-one slots are harmless. The corollary is sufficient, not a minimality claim.

## 9. Why a floor-three root does not follow from this preparation

Consider the ORIGINAL palette of six labels and all twenty three-element root supports, every floor three. Its transversal is exactly four: every three-label candidate misses its complementary three-root, and every four-label set hits every three-root.

Fix one root T of size three and let R=P minus T. The ONLY other root disjoint from all of T is R itself. Its residual transversal is ONE, and its residual complement is empty. Thus the family avoiding all three anchor choices does not provide the element-cover protection used for a pair root.

Replacing all other supports by R would end at the tuple consisting of T and copies of R, of transversal TWO. No ordering of that preparation can stay above the required lower bound three, because its destination violates it. This is a rigorous failure of that one-family normalization, not an exact-four endpoint pair or a primitive disconnection.

This illustrative carrier is ALREADY covered by the accepted uniform-slot theorem: h=3,q=4 gives N=binomial(h+q-2,h)=10, and r=20=2N meets baseline GUARD_BUFFER_CONNECTIVITY.md Theorem AC. It is not a new unresolved diagnostic or numerical campaign.

For a fixed triple root T, lower tau>=3 instead requires EVERY label pair H meeting T to be missed by some other root; pairs disjoint from T already miss that root. At an exact-four endpoint, for each two-element subset {a,b} of T and each x outside T, the triple {a,b,x} is missed by another root. Equivalently the roots avoiding each chosen pair {a,b} supply an element-cover family of the outside labels in their complements. These are THREE overlapping pair-indexed protection systems, not a single family avoiding all of T.

Transferring their owners simultaneously with shared root capacities remains a separate unresolved mechanism. The present proof does not assert that its one-family slack or preparation extends to those coupled systems.

## 10. Scientific boundary

Native exact-four connectivity is now closed for EVERY carrier with at least one original floor equal to one or two. Any hypothetical remaining native exact-four counterexample must therefore have ALL original floors at least three; no counterexample is claimed.

Many all-floors-at-least-three carriers are already covered by palette-room, slot-bound, guard, protected, symmetry, module or cyclic theorems. Exclude those before identifying an unresolved finite domain. The original minimum-three/target-four frontier remains OPEN outside applicable accepted classes.

A11's universal destination-directed question remains OPEN. Compaction, global label permutations, preparation to R/P and owner transfers can use temporary incidences or repeated toggles, so this native theorem does not certify incidence-monotone schedules. General unrestricted root/nested universality is unchanged, with accepted child-interface conditions still required for native lifting.

No external design property, primitive time, physical geometry, alignment rule, numerical evidence, implementation certification, measured efficiency or originality claim is made.

