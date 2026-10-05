# Independent A11.X45 whole-argument review

Date: 2026-10-05 UTC  
Reviewer: independent Codex analytical reviewer (`/root/x45_whole_argument_review`)  
Repository: `proteinfoldingengine/WetLabEngine`

## Exact review binding

- Accepted analytical parent: `090f684531de77a3c319c7419cab41b7c56e3f87`
- Scope commit: `1fb37f8b170067ec494079ae8733b39c824aa54f`
- Exact candidate commit: `347a39dc177825d09e9c87d22b17eea532c421f6`
- Exact candidate tree: `dbf0b19b9e36bc3267146265dbd124ccc43b100e`
- Scope source: `A11_X45_SCOPE.md`
- Proof source: `A11_X45_ORBIT_COVER_TRANSPORT.md`

The candidate is two commits ahead of the accepted parent. The exact parent-to-candidate comparison adds only the X45 scope and proof files: 44 scope lines and 199 proof lines, with no inherited source modification or deletion.

## Verdict

**ACCEPTED.**

The bound candidate proves X45C, X45R and X45F in their stated domains. I found no orientation error, missing pair case, hidden unselected-label assumption, invented witness capacity, floor violation, renewal gap, event-count error or overbroad necessity claim requiring revision.

This acceptance is analytical. It does not certify a numerical campaign, implementation, benchmark, integration merge, numbered version, universal accessibility theorem or native disconnection result.

## 1. Exact representative criterion and orbit formulation

The representative equivalence is correct for the explicitly declared representative pool. At the restored source boundary, the physical representatives indexed by `I` have owner-role set `I`, so they cover exactly when `I in H4`. At the restored next boundary those same physical labels have owner-role set `pi(I)`, so they cover exactly when `pi(I) in H4`. Thus the necessary and sufficient condition for this lift is exactly

`H4 intersect pi^{-1}(H4) != empty`.

The orientation is consistent: `pi^{-1}(H4)` is used as `{I: pi(I) in H4}`, and the directed orbit edge is `I -> pi(I)`. Therefore an intersection member is precisely an adjacent occupied pair on an orbit, including the wraparound edge.

The qualifications are also correct. On a cycle of length `d`, an independent set has size at most `floor(d/2)`, so occupancy strictly above that bound forces adjacency. A nonempty `pi`-invariant subfamily supplies adjacency directly. These are openly sufficient corollaries; the proof claims necessity only for orbit adjacency in the declared one-representative-per-role lift. It does not say that global half-density is necessary, or that failed adjacency excludes another cover or another native path.

Exact template transversal four rules out a four-label endpoint cover with fewer than four distinct owner roles: repeated owner roles would yield a template cover of size at most three. No implicit representative multiplicity is used.

## 2. Same-label lift through primitives and division of duties

For a compatible `I`, the same four physical labels hit every old root and every next root. The lower schedule's endpoint-containing property is sufficient at every primitive:

- an active addition support contains its old endpoint;
- an active deletion support contains its next endpoint;
- every other root is old or completed next.

Hence the four labels hit every partial support and prove `tau <= 4`. This argument remains valid when all four representatives move.

The source correctly keeps the lower and upper obligations separate. X45 supplies no pair guard, floor legality, root ordering, next ownership cycle or descent. Those duties are explicitly inherited on the same physical path. Conversely, X45 adds no primitive, so the lower path's one-toggle endpoint-event count is retained. Renewal occurs only at restored mask/group boundaries, where the template and orbit test are again available; exact four is not falsely required after every primitive.

## 3. Exact block-family cover calculation

For `q >= 2`, `ell >= 6` and `m=q ell`, the construction declares one mask `Q_J=G\J` for every four-set `J` not equal to a cyclic four-interval in one block.

For any four-set `I`, `I` misses `Q_J` iff `I subset J`, which for equal cardinality is iff `I=J`. Consequently the four-covers are exactly the omitted interval family `H`, with `|H|=q ell=m`.

The no-three-cover argument is sound. A three-set meeting multiple blocks is in no interval. A three-set inside one cyclic block is contained in at most two length-four cyclic intervals; a consecutive triple attains the maximum by extension at either end. It has `m-3 >= 9` four-set extensions, so at least one extension is not in `H`; the corresponding declared root misses the three-set. Smaller sets inherit a missing root by extension to three roles. Thus the template transversal is exactly four.

The density computation

`m / binomial(m,4) = 24 / ((m-1)(m-2)(m-3))`

is exact, is already below one half for `m>=12`, and tends to zero. This is a symbolic infinite-family result, not finite no-counterexample evidence.

## 4. Pair redundancy and X40 lower composition

A role pair `K` is avoided by `Q_J` exactly when `K subset J`. There are `binomial(m-2,2)` such four-sets. Cross-block pairs lie in no omitted interval; a within-block pair lies in at most three, with adjacent pairs attaining three for `ell>=6`. Therefore

`rho = binomial(m-2,2)-3 = m(m-5)/2`

is the exact minimum, not merely a lower estimate.

The application of X40L is numerically and logically correct. With `n=m-3`, the proof establishes `rho>=n`, then

`binomial(2rho,rho) >= binomial(2n,n) >= binomial(2n,2) > m(m-3)/2`.

The final strict inequality is equivalent to `3n>5`, true because `n>=9`. This matches X40L's actual strict hypothesis. The family supplies a minimum role cover, equal positive corresponding group sizes and the same actual masks/floors, so all inherited inputs are present.

X40L may therefore supply actual pair witnesses, a simultaneous conditional root order, literal add-before-delete edits, `tau>=3`, same-slot floor legality, another eligible cycle, strict incorrect-owner descent, event uniqueness and full labelled restoration. X45's upper argument is applied to those same primitives; no independent per-pair capacities are invented.

## 5. Renewable long-cycle control and exact destination

With singleton role groups and one block rotation per block, the misplaced graph is exactly `q` disjoint simple cycles of length `ell`. There is no hidden shorter cycle and no unselected label in an active cycle.

For any selected block cycle, its induced permutation rotates that block and fixes all others. The full interval family `H` is invariant. Choosing an interval in the active block gives `I, pi(I) in H4`; all four corresponding labels are selected and change owners. Thus the upper protection is genuinely transported rather than furnished by unchanged cover labels.

Completing one cycle fixes exactly its `ell` labels and leaves the other disjoint cycles unchanged. The mask template, singleton sizes, X40 redundancy and orbit compatibility renew. The incorrect-owner count decreases by `ell`; exactly `q` finite handovers terminate at the full labelled destination. Common incidences remain fixed and every endpoint-differing incidence is toggled once, so the endpoint-event minimum is established on the direct `{3,4}` path.

At singleton sizes every root has size `m-4`, so all declared positive floors through the saturated value `m-4` are legal. No reserve is silently introduced.

## 6. Separations and controls

The stated sufficient-method separations are valid:

- X38 fails because every nontrivial ownership cycle has length `ell>=6`, outside its no-cycle-longer-than-three condition.
- X39 fails because every actual mask has width `m-4`, below its `m-3` premise.
- X40U fails because every role in every minimum four-cover is a singleton; X40L is used only for the lower path.
- X43 cannot choose a qualifying actual root: every actual mask has size `p=m-4` and complement size `n=4`, contradicting `n>=p+3` for `m>=12`.
- X44's strict global-majority premise fails because the exact density is below one half.

The incidence-profile proof correctly excludes X41's singleton-mask direct input in every partition-union representation of the same endpoint. For distinct roles `a,b`, more than four four-sets contain `a` but not `b`, while at most four omitted intervals contain `a`; hence a declared `J notin H` distinguishes them. Cells must be profile-homogeneous, so distinct roles cannot be merged, and every actual root contains `m-4>=8` profiles rather than one cell. The proof appropriately does not turn this input obstruction into native disconnection.

The saturated controls are also correct. Four disjoint floor-safe supports would require `4(m-4)>m` distinct labels. Two labels separated by two positions in a block have combined old/new footprint equal to a four-interval `I in H4`; since every declared complement is indexed by `J notin H`, `I` meets every `Q_J`. Those two labels therefore hit every rootwise whole endpoint union, showing that simultaneous whole-union preparation is unsafe. This is stated only as a method obstruction.

Finally, every root changes under the product of block rotations: invariance of `Q_J` would make its four-element complement a union of full permutation orbits, but each orbit is an `ell`-block with `ell>=6`.

## 7. Counterexample and overclaim checks

I specifically checked the smallest admitted cyclic length for wraparound anomalies. At `ell=6`, a three-set is still contained in at most two cyclic four-intervals, and an adjacent pair is contained in exactly three, so both extremal counts remain valid.

I also checked the possible orientation reversal in the ownership action, the use of outside-cycle representatives, the possibility of repeated owner roles, and the transition between completed block cycles. None creates a gap: invariance would survive either rotation orientation in the family, while the general criterion uses the stated `I -> pi(I)` convention consistently.

The limitations are materially complete. X45 does not claim arbitrary endpoints admit the representation, arbitrary lower paths satisfy the endpoint-containing schedule, arbitrary permutations preserve the sparse cover family, failure of the criterion proves no path, or the result extends to unequal corresponding sizes, mixed-floor permutation, higher targets, directed/nested universality or physical interpretation.

## Acceptance statement

The exact candidate `347a39dc177825d09e9c87d22b17eea532c421f6`, tree `dbf0b19b9e36bc3267146265dbd124ccc43b100e`, is accepted for reporting publication. Reporting must preserve this exact proof source and its limitations, identify X40L as the independent lower theorem, avoid upgrading sufficient-method separations into impossibility results, and retain the analytical/non-numbered status.
