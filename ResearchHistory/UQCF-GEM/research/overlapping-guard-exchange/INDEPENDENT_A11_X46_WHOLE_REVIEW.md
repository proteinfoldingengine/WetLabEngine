# Independent A11.X46 whole-argument review

Date: 2026-10-05 UTC  
Reviewer: OpenAI Codex, fresh independent whole-argument review agent

## Exact reviewed object

- Repository: `proteinfoldingengine/WetLabEngine`
- Accepted analytical parent: `02add6acaa56284cd21308990dce23a84a469d75`
- Frozen X46 scope commit: `70aa5ecdb03e4d2d74429a66a8877b602823aed9`
- Exact candidate commit: `6d375e887cfbcd8541a0d4ec7450cd7c086fe9f6`
- Exact candidate tree: `adbd68abed3ba9d71cd0549efdafaa8876df594a`
- Scope source: `A11_X46_SCOPE.md`, blob `7f976e1caabecaff7838eb317cc39452fac6f829`
- Proof source: `A11_X46_CYCLE_GAP_TRANSPORT.md`, blob `8016ac69c74ad83cb30c4b67befbf6ded2a7f3c2`

I read `ResearchHistory/UQCF-GEM/AGENTS.md`, the frozen scope and exact proof, and the relevant accepted X38--X45 sources, with particular attention to X40 lower renewal, X43 scarce-cover transport, X44 majority transport and X45's exact orbit criterion. I did not edit GitHub or treat any numerical execution as evidence.

## Verdict

**ACCEPTED.** X46G, X46R and X46F form a correct conditional analytical advance in their stated domain. I found no counterexample, hidden numerical enumeration, missing primitive obligation, or claim that requires mathematical correction.

## 1. X46G: cycle-gap theorem

For a cyclic start `a`, `W_a` is bad exactly when at least one actual mask misses it. Thus the bad-start set is precisely the union of the rootwise bad sets and

`|B| <= Gamma(C)`

is an ordinary union bound; no independence or separately allocated root capacity is used. Because `Gamma` is integral, `Gamma < ceil(ell/2)` gives at least `floor(ell/2)+1` good positions. The maximum independent-set size of a cycle of length `ell` is `floor(ell/2)`, including odd cycles and the wraparound edge, so two cyclically consecutive good starts exist.

The orientation is correct: the declared ownership rotation has `pi(c_t)=c_(t+1)`, hence `pi(W_a)=W_(a+1)`. Consequently a good adjacent pair supplies exactly an element of `H4 intersect pi^{-1}(H4)`, with the same convention used by X45.

The rootwise formula is also exact. When a mask meets the cycle, its cyclic complement splits into maximal linear gaps, and a gap of length `d` contains exactly `max(0,d-3)` starts of four-consecutive windows. Starts belonging to distinct gaps are disjoint. When the mask avoids the whole cycle, the cyclic wraparound changes the count from the linear expression to `ell`; the proof states this case separately. The source correctly calls `Gamma` a sufficient overcount, not a necessary condition.

## 2. X46R: same-label primitive lift

The adjacent windows provide four selected physical labels whose old owner roles are `W_a` and whose next owner roles are `W_(a+1)`. Both are actual covers. In the required endpoint-containing schedule, an active root contains its old endpoint through additions and its next endpoint through deletions; every other root is old or completed next. The same four labels therefore hit every primitive support, proving only `tau <= 4`.

The division of duties is explicit and correct. X46 does not infer pair witnesses, `tau >= 3`, floor legality, a processible next cycle, eligible primitives, descent or restoration from the gap budget. Those remain hypotheses and outputs of the lower theorem on the same physical path. At a restored boundary the mask template and group sizes return, so the gap test is renewable and consumes no root or representative. Since X46 adds no edit, an event-minimum statement proved below is preserved.

## 3. X46F: exact family

For `q>=2`, `h>=2`, `H=qh` and `m=4H`, the masks are all co-triples `G\T` plus the disjoint residue roots `D_0,D_2`, each of width `H`. Every set of at most three roles is missed by a suitable co-triple, while every four-set hits every co-triple. Hence the four-covers are exactly the four-sets meeting both `D_0` and `D_2`, and the four-windows establish exact transversal four.

Inclusion-exclusion gives

`|H4| = C(4H,4)-2C(3H,4)+C(2H,4)`.

The displayed twice-excess polynomial expands correctly to

`H(-3H^3+14H^2-11H+2)/2`.

For `H>=4`, `f(H)=3H^3-14H^2+11H-2` has `f(4)=10`, positive derivative at four, and increasing derivative thereafter, so the excess is strictly negative. Thus the family genuinely lies below X44's strict-half hypothesis.

Every block four-window contains all four residue classes and cannot fit inside a three-set. It therefore meets every actual mask, making every rootwise gap count and `Gamma` exactly zero. The `q` singleton block rotations are disjoint simple cycles of length `4h>=8`. Completing one fixes exactly its selected labels, leaves the other cycles unchanged, restores the template, and decreases the incorrect-owner count by `4h`; exactly `q` renewable handovers reach the full labelled destination.

## 4. Lower protection, floors and minimum events

A role pair is avoided by exactly `m-2` co-triple roots containing that pair in their omitted triple. A pair with one role in `D_0` and one in `D_2` is avoided by neither sparse root, proving the minimum `rho=m-2`, not merely a lower bound.

The X40 margin is valid:

`C(2m-4,m-2) >= C(2m-4,2) = (m-2)(2m-5)`,

and subtracting `m(m-3)/2` yields `(3m^2-15m+20)/2>0`; the declared family has `m>=16`. X40L therefore supplies the actual conditional root order, all pair witnesses, lower guard, primitive legality and renewal on these same cycles.

The unequal saturated floors are exactly `m-3` for co-triples and `H` for the two sparse roots. Add-before-delete endpoint containment preserves each same original floor without residual capacity. Every label is resolved once, directly from its source owner to its destination owner, so common incidences remain fixed and each endpoint-differing incidence toggles once. X46 adds no primitives; the resulting direct `{3,4}` path has the endpoint-toggle minimum and restores every labelled root support.

## 5. Separation and controls

The sufficient-class separations are correctly limited and exhaustive for the declared actual roots:

- X38 fails because every nontrivial ownership cycle has length `4h>=8`.
- X39 fails because `D_0,D_2` have width `m/4<m-3`.
- X40U fails because all role groups are singletons, while X40L is used only for the lower bound.
- X43 fails for either sparse root by an explicit one-sparse/three-outside set missing the other sparse root; a co-triple root has complement size three and violates its size premise.
- X44 fails by the exact below-half calculation.
- X41's singleton direct input cannot be recovered by same-endpoint regrouping: co-triples distinguish every pair of role profiles, so cells must be singleton profiles, while every actual root contains at least four such profiles.

With only two low-floor slots, any four disjoint floor-safe supports need at least `2H+2(m-3)=5m/2-6>m` incidences. This is correctly classified only as a private-support method obstruction. Two labels separated by two positions in one block have a combined source/destination footprint equal to a covering four-window, so they hit every rootwise endpoint union; the whole-union tuple is at most two-hit and simultaneous whole-union preparation is unsafe. This too is not promoted to native disconnection.

Finally, every root changes: the sparse roots change residue class, and invariance of a co-triple would require its three-role complement to be a union of full `4h`-role block orbits, which is impossible.

## 6. Scope and remaining hypotheses

The proof does not claim necessity of the gap bound, arbitrary accessibility, universal existence of a gap-admissible cycle, or a new lower repair theorem. It preserves the explicit inputs of a supplied exact-four mask template, equal positive corresponding group sizes, a typed endpoint-containing lower handover and renewed admissible-cycle availability. Unequal corresponding sizes, below-X40 lower repair and unrestricted mixed-floor, directed, higher-target or nested universality remain open. X45 remains the exact inherited orbit criterion; X46 derives one sufficient incidence-level route to it.

The analytical status is therefore appropriate: this is a reusable structural upper-interface theorem plus a nonempty infinite family, not a numerical campaign, new connectivity classification, implementation certification or physical interpretation.

## Final disposition

The exact candidate `6d375e887cfbcd8541a0d4ec7450cd7c086fe9f6` at tree `adbd68abed3ba9d71cd0549efdafaa8876df594a` is **ACCEPTED without requested revision** for reporting and immutable analytical publication, subject to the separately required exact reporting review and publication readback.
