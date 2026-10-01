# Binary-fork unit barriers
Status: proposed general proof, subject to independent review and preregistered validation.

## Objects and claim
Let a no-unary rooted tree have exactly two root children u,v, each the center of a star, with respectively m,n>=2 leaf children. The root support is the full indexed-label palette K of size k>=2. Every nonroot support is a nonempty subset of its parent's. A primitive move adds or removes one label incidence while preserving admission. The profile q(w) is the minimum label-set cardinality hitting all child supports, with zero at leaves.

For every attained profile (r,s,t) at root,u,v, every state connects to a common canonical state within total L1 profile deviation at most1. Thus B1, Binf and Bs are each0 within an exact-profile component and each1 between distinct exact components. The separately optimized nested LEX triple is also(1,1,1) between distinct components. No equivalence of independent and lexicographic objectives is asserted in general.

## Facts and canonical target
The root has two nonempty child supports A,B, so its hitting number is1 when they intersect and2 when disjoint. It is always in {1,2}. Also |A|>=s and |B|>=t. If r=2, disjointness implies k>=s+t, so in particular s<k and t<k.

Choose ordered canonical palettes A*={0,...,s-1}. For r=1 choose B*={0,...,t-1}; for r=2 choose B*={s,...,s+t-1}. They have the correct nonzero cardinalities and the required intersection/disjointness. The canonical inner leaf coloring uses the palette's first s or t labels on distinct ordered anchors and its first label on remaining leaves. For finite canonical trees, order the larger child star first (lexicographically sorted bracket codes); the proof permits either fixed child order.

## Sequential normalization
Process u and then v, leaving the other child's support and leaves fixed during each operation. For the current child w with target h and desired palette D:

1. Expand its support to K, adding missing labels one at a time. Child leaves are unchanged, so q(w)=h throughout. The other child value is unchanged. Root hitting remains1 or2, hence differs from its target r by at most1.
2. Apply the reviewed v16.43 star normalization to the leaves of w, in a label order listing D first and K\\D second, both internally increasing. Its endpoint is the desired singleton coloring. If k>h, the spare-label condition excludes the fully packed exception and the path keeps q(w)=h exactly. If k=h, the only possible inner deviation is at most1 (fully packed m=k=h); crucially w's support is K throughout this step, so the root is exactly1. Moreover the original target r must be1, since initially |support(w)|>=h=k already forced that support to be K. Thus the inner excursion never coexists with a root deviation. The other child stays at its target. This includes h=1; with k>=2 it is in the exact spare-label regime.
3. Remove labels outside D from support(w), one incidence at a time. No child leaf uses those labels after normalization, so removal is admitted. D is nonempty, and all leaf supports stay contained in it. q(w)=h remains exact, the other child value remains exact, and only root hitting can differ from r by at most1. If k=h, there are no removals.

Every local star step remaps to one global leaf-incidence move; support expansion and contraction are also primitive and admitted. Repeating for the second child reaches the same canonical state determined only by the target profile and fixed vertex/label ordering. Its root profile is exact by the intersection/disjointness of A*,B*.

At every step either both inner values are exact and only root deviation (<=1) is possible, or one inner value deviates by at most1 while the root and the other inner value are exact. Leaves remain zero. Hence total L1 deviation is at most1. Reverse one canonical path and concatenate to connect any two exact-profile states. Distinct exact components exclude a zero-cost path for all three scalar objectives; integrality gives lower bound1. The common upper-bound path also gives LEX=(1,1,1) between distinct components.

## Scope and evidence
This proves a family with three internal vertices: a binary root with two star children, for arbitrary leaf degrees and indexed-label count. It does not cover three-internal chains, forks with additional root children, arbitrary retained constructions, intrinsic indecomposability or physical interpretations. Complete bounded graph and path verification tests the implementation; it does not by itself establish the general quantifiers.
