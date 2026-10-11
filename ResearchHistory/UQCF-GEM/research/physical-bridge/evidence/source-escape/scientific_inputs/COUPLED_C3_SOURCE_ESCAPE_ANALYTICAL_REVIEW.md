# Independent analytical review — source escape

Verdict: **ACCEPTED**, within the stated first-source-escape scope. No substantive missing assumption, incorrect implication, or analytical counterexample was found.

This review reads `source_escape/RESULT.md` against `cover_static/RESULT.md` and `cover_static/CLOSEOUT.md`, with the declared scoped parent bc23cf44110e4d794ada59ae2b647599b5a19d42. It is a hand-derived mathematical review only. No enumeration, implementation, new computational experiment, GitHub write, or native acquisition is performed or certified. The only written artifact of this review is this report. The candidate remains subject to its prospective freeze and any separately declared verification obligations.

## 1. Exact first-event classification and normalization

The event definition is exhaustive for the first departure from the region in which every original label is nonempty and contained in its own original star. Initial nonemptiness follows from positive multiplicities and the exclusion of isolated vertices of H. A one-incidence deletion can first violate nonemptiness; a one-incidence addition can first violate original-star containment. These cannot be simultaneous in a single toggle.

Before either event, a saturated edge uv can only be supported by labels originally of types u and v. There are exactly a_u+a_v such labels, precisely its fixed original floor. Consequently all those incidences must still be present. This proves the intact-trace premise even for paths involving arbitrary earlier deletions and re-additions, with any positive integer multiplicities.

For V on type v, every incident saturated edge would lose a required supporter on the final deletion. Thus T_v is empty. Restoring the other labels to their original stars only enlarges their footprints and leaves the edited label empty. Floors remain satisfied and an existing upper cover remains a cover. If a_v is at least two, a full original v-copy remains. If a_v is one, the resulting collection consists exactly of original stars at types other than v, with multiplicities. An upper-four label cover exists exactly when a type cover of size at most four excluding v exists. Repeated types in a label cover can simply be discarded. This establishes the stated V necessity.

For X, let x have original type v and let F be its nonempty footprint immediately before the first outside addition r. At the new state domination gives F union {r} contained in M_w for some original type w. Since r is outside M_v, w differs from v. Simplicity of H gives M_v intersect M_w either empty or {vw}. Nonemptiness forces F={vw}, and the new edge is wz for a third distinct vertex z. The intact trace then gives T_v contained in {vw}.

Restoring all other labels at this pre-event state proves safety of the normalized singleton state. If the edited label is not selected by an upper-four cover, its other selected star types give B_v. If it is selected and a_v=1, the at most three other selected types exclude v and cover every edge other than vw, giving D_{v,vw}. This reasoning does not require the selected cover to be minimum. It also does not normalize any later path. Necessity is sound.

## 2. Sufficiency, cost, and original label identities

For V, its proposed empty endpoint satisfies upper-four by either the surviving v-copy or B_v. Every removed incidence is nonsaturated, and the positive original multiplicity at its other endpoint supplies its floor of one. Intermediate states contain the safe endpoint incidence-wise. Until the final deletion the edited label remains nonempty and inside M_v. There are exactly deg_H(v) toggles from the original source.

For X, the singleton endpoint before the addition satisfies upper-four by a remaining v-copy, B_v, or the three-star D cover plus x. The trace condition retains every saturated incidence of x. Each removed nonsaturated incidence retains its other endpoint's original supporters. Every intermediate deletion state contains that singleton state; therefore any order deleting the other deg_H(v)-1 roots is safe. Adding wz enlarges the footprint and gives {vw,wz} contained in M_w. It preserves floors and the upper cover, and it is exactly the first outside-original-star incidence. The total is deg_H(v) toggles. The construction also works when deg_H(v)=1, with no preliminary deletion.

Actual labels of the same original type are interchangeable in these core arguments, because all unedited labels retain their full original stars. Accordingly the stated certificate works for each actual choice of x, not merely for some label of its type. The costs are exact for the displayed constructions and are correctly not asserted to be globally minimal.

## 3. Hidden safety and multiplicities

The proof uses arbitrary positive a_v, not a binary-profile assumption. The only branching on multiplicity is the distinction between one copy and a surviving original copy. Positivity at the opposite endpoint supplies every nonsaturated floor after the single-label deletions. Saturated floors continue to use their original numerical values, without recomputation under changed footprints.

The hidden-completion argument is the inherited original-domination argument from the accepted static domain: a hypothetical full cover of at most two labels can replace selected current core labels by original containers, retaining any selected hidden labels. At most two labels still suffice in the original protected system, a contradiction. Repeated replacements can reduce cardinality and do not cause a problem. At each constructed state the core cover independently supplies upper-four. Thus the claim is uniform safety for every original protected hidden completion with unchanged hidden incidences. It supplies no observation, label-selection procedure, commitment, or acquisition mechanism.

## 4. Cover-pinning is a valid sufficient lock

If deg_G(v) is at least two, neither T_v empty nor T_v contained in a single edge can hold; both gates are excluded regardless of multiplicity.

For a singleton cover-pinned v, B_v fails by definition. Suppose D_{v,vw} held, with witness D of size at most three excluding v. Then D union {v} is an H cover of size at most four. For each neighbor t of v other than w, the edge vt remains in H minus vw and forces t into D. This cover therefore leaves at most the one neighbor w outside it, contrary to cover-pinning. Hence every D_{v,vw} fails and so do all V/X gates at v.

The alternative private-root explanation is also valid before first escape. The original types of any selected at-most-four-label cover form an H vertex cover C. Cover-pinning forces v into C and at least two neighbors outside C. Because v has only one original label and all current labels still stay in their own stars, that label must retain each of the corresponding two roots. Its footprint cannot fit the distinct star required by a first X event. This reinforces the sufficiency claim without asserting necessity of cover-pinning for locking.

## 5. Explicit static-but-unreachable instance

For H=K6 minus edge45, the only independent pair is {4,5}, no independent triple exists, and the unique H cover of size at most four is C={0,1,2,3}. Thus its source hitting number is four.

With saturated K_{2,3} between {1,2} and {3,4,5} and isolated 0, I={3,4,5} is G-independent with neighborhood {1,2} and deficiency one. Under a=(1,1,1,2,1,1), its only intersection with C is duplicated type3, so the static theorem applies. The proposed n=(1,2,2,1,0,0) has total six versus original total seven. All types in C survive. Each saturated edge to type3 has endpoint count sum 3, matching its floor 3; each saturated edge to type4 or type5 has count sum 2, matching its floor 2. The retained C covers every nonsaturated root. This is a valid static reserve.

Every type other than 0 has saturated degree at least two: types1,2 have degree three and types3,4,5 degree two. Type0 has a_0=1, lies in the unique upper-four cover, and has both neighbors4 and5 outside that cover. It is cover-pinned. The lock therefore excludes every first source escape, including a vacancy. Static existence together with minDegree(G)=0 genuinely fails to imply first-vacancy reachability.

The positive multiplicity control is correct: increasing a_0 to two leaves T_0 empty and a surviving type0 copy, making V(0) valid. Deleting one original type0 star costs five edits and gives a reachable vacancy. This comparison does not depend on any enumeration.

## 6. Other controls and scope

For K5 minus34, the four-cover {1,2,3,4} excludes0, and isolation of0 in G makes V(0) valid even with singleton multiplicities. This correctly uses an upper-four cover rather than only the minimum three-cover.

A saturated K_{2,3} on K5 has minimum saturated degree two, excluding all V/X gates even with duplicated types. Static deficiency is compatible with that exclusion. With a saturated star on K5, a leaf v, center w, and another leaf z give the stated X pattern: T_v={vw}, and the four other types provide B_v.

The theorem establishes first escape, and the sufficient lock excludes vacancy because any vacancy route has a first escape. It does not establish a general vacancy route following X, full component classification, optimal costs, exact restoration or exchange, or native acquisition. The retained limitations accurately preserve these distinctions. No claim about arbitrary hypergraph carriers follows from the simple-graph star-intersection step.

## Nonblocking editorial precision

In the V necessity paragraph, restoring other labels “increases floors” should be read as “increases support counts while preserving the fixed original floors.” The floors themselves remain fixed throughout the model. This is a wording improvement only; the defined domain and all proof inequalities use the correct fixed floors.

Final analytical assessment: **ACCEPTED** for the exact first-source-escape theorem, its displayed construction costs, cover-reinforced sufficient lock, and the stated static-but-unreachable example. No numerical verification or broader scientific closeout is implied.

## Subsequent pre-freeze simplification — independently accepted

After the initial review above, the author proposed eliminating the redundant D alternative and identifying cover-pinning with failure of B_v. This supplement preserves the initial gate acceptance and independently verifies the stronger, simpler presentation. It uses no computation.

First, D_{v,vw} implies B_v. Given a cover D of H minus vw of size at most three excluding v, the set D union {w} still excludes v, has size at most four, and covers all of H: D already covers every edge other than vw, and w covers vw. This remains true whether or not w already belongs to D. Therefore the original expression a_v>=2 or B_v or D_{v,vw} is equivalent to a_v>=2 or B_v. The exact X gate can and should drop D. The original necessity argument that produces D remains sound, but one more sentence can convert it immediately to B_v. The original theorem was correct, with an unnecessary alternative rather than a missing case.

Second, cover-pinning is equivalent to not B_v. The forward direction is part of its definition. Conversely assume B_v fails. Every H cover C of size at most four then contains v. If such a C left no neighbor of v outside C, removing v would retain a cover, exclude v, and have size at most four, contradicting failure of B_v. If it left exactly one neighbor w outside C, replacing v by w would retain a cover of the same size excluding v: edges not incident to v retain their original covering endpoint, all other v-edges have their other endpoint in C, and vw is covered by w. This is the same contradiction. Each such C must therefore leave at least two neighbors of v outside C, exactly the remaining cover-pinning condition. Covers of size at most four exist by the source-domain hypothesis, so this description also avoids any issue of an empty family.

Consequently both gates can use the common condition a_v>=2 or B_v, and the sufficient-lock condition can equivalently describe its singleton alternative by not B_v. This equivalence does not turn the sufficient lock into a necessary lock classification: a weak saturated type may also have no geometric X extension wz, and the exact gate continues to govern that distinction. No change to the displayed costs, hidden-completion proof, explicit example, or retained scope follows.

Supplemental verdict: **ACCEPTED** for these pre-freeze simplifications. No implementation or enumeration has been performed.

## Final degree-one carrier boundary — independently accepted

The subsequently added example H=K_{2,3} on parts {0,1}/{2,3,4}, disjoint from edge56, with G=H and all seven a_v=2, is valid. Vertex-cover numbers add across these disjoint components, giving source cover number 2+1=3. The set I={2,3,4} has neighborhood {0,1} and deficiency one. The original cover C={0,1,5} is retained by the explicit static counts (3,3,1,1,1,2,2), whose total thirteen is one below the original palette fourteen. Every saturated bipartite edge has count sum four, as does edge56, matching the original floors. C supplies upper-four (indeed upper-three).

Types0,1 have saturated degree three and types2,3,4 degree two, excluding both gates. Types5,6 have a nonempty saturated trace, excluding V. Their only neighboring type has no neighbor other than themselves, excluding the distinct third vertex required for X. Since their equal stars are both {56}, containment in the other endpoint's star cannot permit a new root incidence. Thus no first escape occurs despite static reserve and duplicated weak types. The geometric extension condition is substantive, and the sufficient-lock corollary is not a necessary classification.

Only a minor wording refinement is suggested: this example exhibits equal original stars M5=M6, but no strictly nonmaximal original star. Accordingly “equal source-star behavior” is more precise than “nonmaximal/equal source-star behavior.” The boundary paragraph is otherwise **ACCEPTED**. The proposed correction from “increases floors” to increased support counts preserving fixed floors also resolves the earlier editorial note. This supplemental check is purely analytical; no prospective campaign counts or numerical outcomes are certified.
