# Independent whole-argument review — A11.X44

**Final verdict: ACCEPTED at exact revised candidate `9c8083bbc12d84fab5ca36361a39466e24d0a425`, tree `232423e8bef65e4015a541ec417be6c8721134cf`. No further whole-argument revision is required.**

Reviewer: independent Codex agent `/root/x44_whole_argument_review`. Date: 2026-10-05 UTC. This is the final fresh whole-argument review after a required theorem-domain correction. It is not the separate reporting/publication review, numerical verification, scientific execution, numbered certification, inherited-proof recertification or literature-originality assessment. I did not author or modify the GitHub candidate, mutate GitHub, run science/tests/enumerations/workflows/code/benchmarks, or delegate.

## Exact revision history and identity

Repository `proteinfoldingengine/WetLabEngine`; paths below are relative to `ResearchHistory/UQCF-GEM/research/overlapping-guard-exchange/`.

| Object | Commit | Tree | Sole parent |
|---|---|---|---|
| accepted analytical parent | `fee852f07ca8db8296197c41ab418b89a6437335` | — | — |
| X44 scope | `f1bd8022142fa751948599cadf474fac28b71a0b` | `6336703f124456e93becba79d2ba053b127031ee` | `fee852f07ca8db8296197c41ab418b89a6437335` |
| initial proof | `17b81dcc388e78e93546590a1dcb9474f1b9d29b` | `042c74195c17c5708c8b49971e33584e058c88e2` | `f1bd8022142fa751948599cadf474fac28b71a0b` |
| clarified but rejected candidate | `5306bc21c770a8195e1298a7c72326c5bdff88ff` | `7438dbf2049fa4fe341e6d508e48b747621f0978` | `17b81dcc388e78e93546590a1dcb9474f1b9d29b` |
| accepted revision | `9c8083bbc12d84fab5ca36361a39466e24d0a425` | `232423e8bef65e4015a541ec417be6c8721134cf` | `5306bc21c770a8195e1298a7c72326c5bdff88ff` |

I fetched the revised manuscript afresh at `9c8083…`; this verdict does not infer its text from the prior local review. The exact Git comparison is one commit ahead and modifies only `A11_X44_MAJORITY_COVER_TRANSPORT.md`, from blob `3f08517aaeb57ea8736628e9655a5de74b66caed` to `624cc9bd2414e220f57199932440b3f265e28689`, with six additions and two deletions. Scope and inherited sources are unchanged.

The first whole review gave **REVISION REQUIRED** at `5306bc…`. Its precise objection was that abstract X44R said only that a lower “cycle theorem” supplied an add-before-delete handover, without formally requiring the one-label simple-cycle exchange, representative role permutation and endpoint-containing root schedule used for the SAME-label lift. X44M and concrete X44F otherwise passed. That rejected object remains immutable in ancestry and is not relabelled accepted.

## The X44R defect is fixed

Revised X44R is now “direct renewable simple-cycle repair” and requires at every unfinished restored boundary:

- one actual selected label on each role of a simple ownership cycle, moving to the next cycle role;
- fixed representatives outside the cycle, inducing the role permutation `pi`;
- a root schedule where every active partial root contains its old endpoint during destination additions or its next endpoint during old-only deletions, while every other root is old or completed next;
- `tau>=3`, all SAME original floors, and restoration of the SAME mask template and positive group sizes; and
- strict decrease of the incorrect-owner count until the specified FULL destination.

Together with Section 3, the outside representative is chosen for every noncycle role from its nonempty unchanged group; selected labels represent cycle roles. These representatives are distinct because the groups partition the palette. This is exactly the physical permutation system missing before. The root-processing clause is also exactly what ensures endpoint covers hit every primitive support.

The progress quantity is now the nonnegative integer number of incorrectly owned labels, and the terminal state is explicitly the FULL destination. Hence strict decrease plus finite handovers gives well-founded termination, not an unspecified decreasing measure.

Section 8 narrows the retained input to the same one-label simple-cycle/endpoint-containing form. New Section 9 accurately records the initial rejection, the portions that passed and the exact correction. It does not claim that the rejected overbroad statement was accepted and adds no arbitrary-handover theorem. The requested defect is fixed.

## X44M and SAME-label physical lifting

Let `Omega` be all four-role subsets. For every permutation `pi`, the induced action on `Omega` is bijective, so `|pi^{-1}(H4)|=|H4|>|Omega|/2`. Therefore

`|H4 intersect pi^{-1}(H4)| >= 2|H4|-|Omega| > 0`.

Choosing the lexicographically least member is a deterministic eligible rule. Both `I` and `pi(I)` hit every actual mask; exact transversal four makes them minimum covers. This is a strict finite intersection theorem, not random choice, enumeration or independently chosen endpoint covers. The proof correctly claims sufficiency only: equality can fail for the bare intersection argument, but no converse or mask-family realization is asserted.

For a typed handover, let `z_j` be the selected actual cycle label at a cycle role and a fixed actual label at every noncycle role. At the old boundary its owner is `j`; at the next it is `pi(j)`. Thus `K={z_j:j in I}` is FOUR SAME actual labels hitting every old and every next labelled root. During additions an active root contains its old support; during deletions it contains its next support; all other roots are old or completed next. The SAME `K` therefore hits every physical support after every primitive.

This proves only `tau<=4`. Revised X44R correctly leaves actual pair witnesses, `tau>=3`, literal next moves and same-slot floor legality to the lower theorem on the SAME path. At restored boundaries masks and positive groups renew, so majority renews and a fresh four-label set may be chosen. No cover representative is consumed.

## X42 composition, renewal and minimum events

Accepted X42L supplies exactly the typed lower path for X44F. Equal current/destination role sizes make the incorrect-label ownership multigraph balanced; if nonempty it contains a simple directed cycle. X42 selects one actual label per cycle role and sends it directly to the next role/final owner.

It derives one shared conditional order on the SAME original labelled roots. Each scheduled root receives all absent next incidences before any old-only deletion. During addition it contains its old endpoint; during deletion it contains its next endpoint, each of size `N_i`, so every SAME original floor `a_i<=N_i` remains legal even at saturation. Actual witnesses preserve `tau>=3`.

Completing a cycle restores all `b_j,N_i`, masks, witness inputs and majority. It removes balanced arcs and strictly decreases incorrect owners. If unfinished, another cycle exists; finite orders and finite literal incidence lists make each leg finite. Integer descent reaches every `D_j` and FULL original labelled/noncompact `C_i`.

Each label moves only in its resolving cycle and directly to its final owner. Common endpoint incidences remain fixed and every differing incidence toggles once, giving exactly `sum_i |A_i symmetric_difference C_i|` primitives, the unavoidable endpoint-toggle minimum. X44M supplements that SAME path, so the count survives. No A conversion or runtime claim is used.

## X44F exact family and lower inequality

For `m=3h`, `h>=3`, with disjoint `S,T,U` of size `h`, masks are all `Q_J=G\J` for three-sets `J`, plus one actual `S` and one actual `T`.

Every three-set `J` misses `Q_J`, excluding covers of size at most three. Every four-set meets every co-triple complement. It covers the two small roots exactly when it meets both `S` and `T`, and such sets exist. Thus the transversal is exactly four and

`|H4|=C(3h,4)-2C(2h,4)+C(h,4)`.

Twice its excess over half the universe is

`C(3h,4)-4C(2h,4)+2C(h,4)=h(h-1)(19h^2+37h-18)/24>0`

for every `h>=3`. The exact count and factorization are correct.

For any role pair `K`, `Q_J` avoids it exactly when `K subset J`; there are exactly `m-2` choices of the third member of `J`. Hence actual `S` localization has `p=h` and `alpha,rho>=m-2`. Coordinate monotonicity gives

`C(alpha+rho,alpha)>=C(2m-4,m-2)>=C(2m-4,2)`,

and

`C(2m-4,2)-2h(m-3)=12h^2-21h+10>0`

for `h>=3`. Therefore X42's strict `C(alpha+rho,alpha)>2p(m-3)` condition holds using actual shared root identities, with no invented per-pair capacity.

## X39, X43 and singleton separation

X39 fails because actual `S,T` have width `h<m-3=3h-3`.

Every possible actual original root is exhausted for X43. Choosing `S` fails because one `S` role plus three `U` roles misses actual `T`; choosing `T` fails symmetrically. Choosing a co-triple `Q_J` gives block size `m-3` and complement size `3`, contradicting X43's `n'>=p'+3`. Thus no actual root supplies X43's typed input.

For any distinct roles `a,b`, a three-set `J` containing `a` but not `b` makes `Q_J` omit `a` and contain `b`; all role incidence profiles are distinct. Any cell in any partition-union representation of the SAME endpoint must be profile-homogeneous and cannot merge roles. Every root contains at least `h>=3` profiles, so no original root is one cell. This excludes X41 direct singleton input only, not access to another state or native connectivity. The proof correctly admits X40's strong lower applicability; X44's advance is upper transport.

## Saturated singleton control and method limits

With every `b_j=1`, the block-ordered full `m`-cycle selects and moves every palette label, leaving no unselected label. Saturated floors are `h` on `S,T` and `m-3` on co-triples, two distinct grades at least three. Every mask is a nonempty proper subset of the connected cyclic permutation, so every root changes. Unique one-label role profiles prevent SAME-state regrouping into a size-two group or creation of an unselected representative.

Only two low-floor slots exist. Four distinct floor-safe supports would require at least

`2h+2(m-3)=8h-6>3h=m`

incidences, so four disjoint/private supports cannot fit. This is only a preparation obstruction.

The corrected whole-union pair witness is valid. Labels on the last-`S` to first-`T` and last-`T` to first-`U` edges have four distinct combined roles, meet `S,T`, and meet every co-triple mask. The **pair** hits every rootwise original endpoint union, giving union transversal at most two and making simultaneous whole-union preparation unsafe. The proof does not say either label works alone, every root order fails or the endpoints are disconnected.

## Connectivity, limits and acceptance boundary

Accepted Lemma L already connects the endpoints: equal corresponding sizes permit a palette permutation carrying each `B_j` to `D_j`, hence every same-mask `A_i` to `C_i`, and L implements it at the same floors. X44 claims no new connectivity classification.

The retained domain is explicit: SAME exact-four masks, strict majority, positive equal corresponding sizes and a renewable lower mechanism of the typed simple-cycle/endpoint-containing form. Failure at/below half is not a no-path theorem; X43 can work below half. Arbitrary representation access, unequal sizes, below-bound/unlocalized repair and unrestricted mixed-floor/directed/higher-target/nested universality remain open. Disjoint and whole-union controls are method limits only. No science, implementation, benchmark, numerical, certification, originality or physical claim is introduced.

X44M, revised X44R and X44F now match exactly. The sole defect identified at `5306bc…` is fixed without a new overclaim, and Section 9 preserves the rejection history honestly. **The exact revised whole argument at `9c8083bbc12d84fab5ca36361a39466e24d0a425` is ACCEPTED.** This permits only the next separately requested reporting/publication review; it does not pre-approve a reporting object or replace later immutable readbacks.
