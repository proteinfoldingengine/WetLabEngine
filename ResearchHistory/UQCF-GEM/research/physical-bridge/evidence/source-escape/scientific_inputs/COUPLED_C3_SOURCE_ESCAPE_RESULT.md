# Source escape under upper-four protection — analytical candidate

Status: OPEN, hand-derived before any new enumeration; independently accepted analytical theorem, prospective freeze and scientific verification pending. Integrated parent bc23cf44110e4d794ada59ae2b647599b5a19d42 (scoped cover-static closeout). No full reachability theorem or native acquisition mechanism is claimed.

## Domain and exact question

Use the closed cover-static domain: finite simple H with no isolated vertices, roots E(H), star M_v at each type v, all positive integer original multiplicities a_v, original palette A=sum a_v, source vertex-cover number3or4. Saturation G is a subgraph of H. Original floors are a_u+a_v on G-edges and1 otherwise. Every current label footprint is contained in some original star; current core hitting number is at most FOUR. Native edits toggle one label/root incidence and retain all these conditions; hidden incidences remain unchanged. Original domination supplies lower-three protection for every original protected hidden completion. No observation, access, outcome or commitment primitive is added.

For each original actual label x, write v(x) for its original type. A source escape event is the FIRST occurrence of either (V) an empty original label, or (X) an incidence on x at a root outside its original star M_v(x). Before this event every label is nonempty and a subset of its own original star. X is a footprint change relative to the ORIGINAL label type, not merely a deletion. Source escape is a necessary event on any first-vacancy route, not a sufficient condition for such a route.

Let B_v mean that H has a vertex cover of size<=4 excluding v. Covers may be nonminimum. Let T_v be the incident G-edge set at v.

## Exact first-escape gate

A first source escape is reachable iff at least one of these explicit certificates exists:

V(v): T_v is empty, and either a_v>=2 or B_v.

X(v,w,z): v,w,z are distinct, vw and wz are H-edges, T_v is contained in {vw}, and either a_v>=2 or B_v.

The certificate applies to ANY actual original label of type v. V deletes that label's whole star. X first deletes every root of that label except vw, then adds wz. Choose any deletion order; the first escape occurs at the final edit. X never empties its edited label. No other original label changes. The achieved costs are deg_H(v) for V and deg_H(v) for X (deg_H(v)-1 deletions plus one addition). These are construction counts, not a claimed globally optimal reserve cost.

## Necessity: normalize the first event, not the whole path

Take any safe finite path with a first escape. All earlier footprints lie within their own original stars and remain nonempty. Consequently no original saturated root can lose any original supporting label before the event: it initially has exactly its required a_u+a_v supporters, and no label originally outside those types has acquired that root. Original saturated traces are therefore intact.

For a V event on original type v, its label is emptied by deletion. Its saturated trace must be empty, so T_v is empty. Restore all other labels to their original stars in the state just after V. This only adds original incidences, preserves domination, increases support counts while preserving the fixed original floors and cannot increase the hitting number. Thus the single-label deletion state is safe. If a_v>=2 the remaining original copy supplies its type. If a_v=1, all active labels have types other than v; a cover of at most four labels is equivalent to B_v.

For an X event on original type v, consider its nonempty footprint F just BEFORE the new incidence r is added. F is contained in M_v, while F union {r} is contained in some original M_w and r is outside M_v. Distinct stars of a simple graph intersect in at most the single root vw. Hence F={vw}, and r=wz with z distinct from v,w. The intact saturated trace gives T_v subset {vw}. Restore all OTHER labels to their original stars at the pre-event state; the state with x={vw} stays safe by monotonicity.

If a_v>=2, a full original v-star remains and upper-four is automatic. If a_v=1, any at-most-four-label cover in this normalized state either excludes x, yielding B_v, or includes x together with at most three other original star types excluding v. Those types cover H minus vw. Adjoin w to them: this yields an H cover excluding v of size at most four, hence B_v. (The apparent alternative using a three-cover of H minus vw is therefore redundant.) This proves necessity without asserting that arbitrary later paths normalize similarly.

## Sufficiency and every protected hidden completion

For V, the stated condition makes the single-label empty endpoint satisfy upper-four. No saturated incidence is removed. Every nonsaturated root still has its other endpoint's positive original multiplicity, so floor1 holds. Every intermediate deletion state contains this safe endpoint incidence-wise, so floors and upper-four hold; each edited footprint remains a subset of its original star. The final deletion is the first empty label and no outside-star incidence appears.

For X, the singleton state x={vw} has upper-four from the remaining v-copy or B_v. No saturated root except vw can be incident to v, and vw stays. All nonsaturated losses leave the other type's original labels, so floors hold. Any deletion order reaches this singleton through supersets of it. Adding wz then preserves floors/upper-four and is dominated by M_w. It is the first outside-original-star incidence and no label has become empty. The same argument works for every original choice of x.

At every state, domination by original footprints prevents any new full-system cover of at most two labels: replace chosen current core labels by original containers, retaining hidden labels, to contradict the original protected lower-three condition. The current core cover supplies upper-four. This is uniform safety of the constructed path under original hidden completions, not a native means of selecting or committing that path.

## Cover-reinforced source-lock corollary

Call v cover-pinned when B_v is false: EVERY H vertex cover C of size<=4 contains v. Such a cover necessarily has at least two neighbors of v outside C. With zero such neighbors remove v; with exactly one, replace v by that neighbor. Either operation would give a cover excluding v of size<=4, a contradiction. Suppose every type v satisfies either deg_G(v)>=2, or a_v=1 and v is cover-pinned. Then no source escape and hence no first vacancy is reachable.

Proof. Strong saturated traces exclude both V and X. For a singleton cover-pinned v, B_v is false. The exact gate therefore excludes every escape. Equivalently, before any hypothetical first outside incidence the upper cover forces the unique original v-label to retain at least two private roots for whichever cover is selected; it cannot fit any other star. This corollary is sufficient for locking, not a necessary classification of all locked sources.

## Explicit static-but-unreachable case with an isolated saturation type

Let H=K6 minus edge45. Its only independent pair is45, so its unique cover of size<=4 is C=0123 and its source hitting number is4. Let G be the complete bipartite graph between {1,2} and {3,4,5}, with vertex0 isolated. Choose a=(1,1,1,2,1,1), so A=7.

Static reserve exists: I={3,4,5}, N_G(I)={1,2}, deficiency1. Its only member in C is type3, which has multiplicity2; hence it is eligible under the closed cover-static theorem. Counts n=(1,2,2,1,0,0) sum to6, preserve C, meet all original floors and admit a spare label.

Nevertheless no first vacancy is reachable. Every v!=0 has saturated degree at least2. Type0 is a singleton and cover-pinned: the unique C leaves both its neighbors4,5 outside C. The corollary applies. Thus static existence AND minDegree(G)<=1 is NOT sufficient on general pair-root carriers, even when minDegree(G)=0. The source may still admit safe deletions within original stars; no claim of a singleton native component is made.

If a_0 is increased to2, V(0) holds and deleting one original type0 label reaches a reserve while another remains. This sharp control distinguishes a genuinely usable weak type from one required for upper protection. The negative and positive examples are hand-derived; no campaign has run.

## Source-three and other controls

For H=K5-minus34, all singleton, G isolating0, B_0 holds through nonminimum cover1234; V(0) succeeds even though minimum cover012 cannot be kept. K5 with duplicated types and saturated K23 has all G-degrees>=2, so no first escape despite static reserves. H=K5 with a saturated star has degree-one donors and admits X certificates, illustrating that a source can escape via reassignment rather than immediate vacancy. X existence alone is not promoted to general reserve reachability.

## Retained limits

This exactly characterizes the first escape gate, not all components, subsequent transfers, first-vacancy reachability after X, exact repair/exchange/restoration, arbitrary carrier hypergraphs, missing source types, edit-cost optimality, termination or native acquisition. It gives a new sufficient lock and a strict counterexample to the five-type reachability generalization. Broad C3/general C4 remain OPEN. No next numerical results exist before prospective freeze.


## Degree-one carrier boundary

The requirement that w has a neighbor z distinct from v in an X certificate is substantive. On a two-vertex connected component of H, both endpoint stars equal the single root; no outside-original-star incidence can be added through that component. If its edge is saturated, none of its labels can be emptied either.

For a concrete separate hand-derived control, take H to be K23 with parts{0,1}/{2,3,4}, disjoint from edge56, take G=H and all seven source multiplicities2. Source hitting number is3. Static reserve exists via I={2,3,4}, N={0,1}, retaining original cover{0,1,5}; nevertheless no source escape is possible. Types0..4 have saturated degree>=2; types5,6 have degree1 but no third vertex z for X, while V is excluded by their saturated root. Thus merely checking for a replaceable weak type, without a possible new incidence, is also insufficient. This example explicitly includes equal source-star behavior without assigning a fresh label or adding a new root.
