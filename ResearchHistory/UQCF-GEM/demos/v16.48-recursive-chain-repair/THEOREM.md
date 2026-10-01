# Compact-palette induction for all internal chains

Status: analytical proof reviewed independently; prospective implementation validation and stage closure pending.

## Statement and simultaneous induction
A finite no-unary rooted tree has an internal chain when each internal vertex except the deepest has exactly one internal child. Let its internal degrees be d0,...,dn-1 >=2. For a fixed attained internal hitting profile q0,...,qn-1, define

    m_last = q_last
    m_i = max(q_i,m_next)             if q_i < d_i
    m_i = d_i-1+m_next               if q_i = d_i.

For every suffix and every ordered NONEMPTY root palette P, simultaneously prove:
1. Attainment implies |P|>=m_i.
2. There is a canonical admitted state depending only on the suffix, profile and ordered P. Its root support is P and the union of all descendant supports is exactly the first m_i labels of P.
3. Every state of that profile normalizes to this canonical state through admitted one-incidence moves, with root support P FIXED and total suffix L1 profile deviation at most1.

All nonroot supports are nonempty subsets of their parent's. Leaves have q=0. The root support never changes; only a recursive child-root support may change during its parent's phases. Every q_i>=1. The strengthened statement includes |P|=1: all descendant supports are that singleton, all q_i=1, m_i=1, and the path is constant.

## Base and canonical pattern
At the deepest internal vertex the tree is a star. Necessarily |P|>=q. Its canonical leaves are the first q distinct labels, followed by the first label for every remaining leaf. The reviewed v16.43 star construction preserves q exactly except the fully packed case where its excursion is down by1. Root support stays P. A singleton palette is already canonical. Descendant union has cardinality q=m.

For a nonterminal node of degree d with l=d-1 side leaves and suffix requirement m_next, define its canonical pattern recursively:
- If r=q_i<d: its internal child's support is the first m_next labels of P. Side leaves are first r distinct labels and then the first label. Recursively fill the child with its canonical pattern on that chosen palette.
- If r=d: side leaves are first l distinct labels of P. The internal child's support is the next m_next labels, disjoint from those side labels. Recursively fill the child on that ordered palette.

Assuming |P|>=m_i, these patterns are admitted and attain the prescribed profile. In the nonsaturated case the child contains the first side label, so it does not increase the side hitting number r; descendant union uses exactly max(r,m_next) labels. In the saturated case all root children are disjoint, so root hitting is d and their union uses exactly l+m_next labels. Nesting means union of all descendants equals union of immediate child supports.

## Necessity of the palette bound
Let S be the current internal-child support. The inductive lower bound gives |S|>=m_next; also |P|>=r. These give |P|>=max(r,m_next) in the nonsaturated case. In the saturated case, any overlap between two child supports would allow one label to hit both, yielding a cover of at most d-1 labels. Thus all child supports are pairwise disjoint. The l side leaves each require at least one distinct label outside S, so |P|>=l+m_next. This proves necessity independently of the proposed normalization.

## Nonsaturated normalization
Freeze the entire internal-child subtree, whose root support is S. Let h be the hitting number of the l side leaves. Adding child S changes hitting by at most1, so h<=r<=h+1. Normalize those side leaves using the star construction on P, target h. If l=1, add the first label and then delete all other labels in that leaf; its hitting stays1. For l>=2 the star construction is exact in h except l=|P|=h. In that exception r=h=|P| (r cannot exceed |P|), and side hitting only drops to h-1; root hitting is between h-1 and h. In every case only the current root may deviate, by at most1.

Expand S to P parent-before-descendant (only this root's internal-child support changes, not any descendants). Root hitting stays h or h+1, and at full P it is exactly h. All lower profile coordinates are unchanged because they depend on child supports, not this expanded root support. If h=r-1, then r>=2 and r<=l: the side leaf at index r-1 currently repeats the first label. Recolor it to the r-th label of P, add before delete; the first singleton anchor remains. The side hitting rises from h to r, and root hitting equals it while S=P. If h=r, no change is required. The root is now exact and its side leaves are canonical.

Recursively normalize the internal-child subtree with root palette P fixed. The parent stays exact because its child support remains P and the side scaffold is fixed. By induction total deviation within the child subtree is at most1. At the endpoint all child-root descendants use exactly the first m_next labels of P. Delete all other labels from that child-root support. These deletions are admitted because no descendant uses them. They do not change any inner profile. The first label remains in the child, so the r singleton side colors still cover every root child and remain necessary; root hitting remains r. This reaches the recursive compact canonical endpoint. Parent and descendant excursions occur in separate phases.

## Saturated normalization and arbitrary-depth transport
Pairwise disjoint root children imply r=d and side hitting l. Normalize the internal-child subtree recursively on its own ordered fixed palette S. All root children remain disjoint, so the parent stays exactly d, while the child subtree has total deviation<=1. At its canonical endpoint remove labels of S beyond its first m_next from the child-root support. Shrink each side leaf to its least label. The whole profile is exact throughout these contractions.

There are now l singleton side roles and m_next nested roles, each nested role carrying one label's complete canonical incidence pattern throughout the internal-child subtree. All assigned role labels are distinct. Replace nested label x by label y absent from that subtree by adding y wherever x occurs, in parent-before-child order, then deleting x in child-before-parent order. Admission and nonemptiness are preserved. At every internal vertex, during addition the child-incidence set of y is contained in x's, and during deletion remaining x-incidences are contained in y's. Replacing a redundant hitting label by its superset proves that EVERY inner hitting number remains exactly unchanged, regardless of depth.

Use the v16.47 exchanges, now applied to the entire suffix:
1. Replace a role by a globally unused label: exact throughout.
2. Exchange a nested role x with outer singleton y: replace x by y in the subtree, then y by x in that leaf. Only this leaf and the internal child may overlap. Other children remain disjoint, so parent hitting is d or d-1; inner hitting is exact.
3. Swap two outer singleton roles by four add/delete moves: only those two children overlap; parent hitting is d or d-1.
4. Swap two nested roles via any outer pivot P by the three fixed-role swaps (A,P),(B,P),(A,P). This restores the pivot and swaps A,B. Each constituent exchange ends exact, so deviations do not accumulate. A pivot exists because d>=2.

Order the roles with the side leaves first, then the nested canonical pattern roles. Assign successive labels of P using an unused-label replacement or a role exchange. Earlier roles remain fixed after each complete exchange; a temporary pivot is restored. The final nested labels are in the same ordered roles as their original canonical pattern, so the recursive compact canonical endpoint is obtained even when the suffix contains further saturated nodes. During this transport only the parent deviates. This completes the simultaneous induction.

## Barrier conclusion and scope
For any two states in one attained profile, concatenate one normalization with the reverse of the other. Total L1 excursion is at most1, so each independent scalar barrier B1, Binf, Bs is at most1. Distinct exact components exclude a zero-cost path for each objective; integrality yields B1=Binf=Bs=1. Within a single exact component all are0. The common unit path also gives the separately defined LEX=(1,1,1) between distinct components.

The result covers arbitrary finite lengths, arbitrary degrees>=2, and arbitrary finite nonempty palettes for INTERNAL CHAINS. It does not prove unit barriers for internal branching (two or more internal children), arbitrary retained trees, or physical energy, metric, gravity, or fundamental time. Finite exhaustive and directed checks validate the implementation only; the general quantifiers follow from the induction above.
