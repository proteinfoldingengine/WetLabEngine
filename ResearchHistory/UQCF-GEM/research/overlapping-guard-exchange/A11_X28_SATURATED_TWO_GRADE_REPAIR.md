# A11.X28 — saturated witness balance forces two-grade protection and direct repair

Scope:4dd6dc93ccddafcbebed66cfee517ba2a5cb7d1b.
Parent analytical publication:ae080ab1799cc093b2bfc9c67363f57511cf04b9.
Certified baseline:466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Frozen candidate for fresh independent WHOLE-ARGUMENT review. Analytical only.

## 1. Exact theorem and native setting

Let k>=7 be ODD. Fix an ordered k-label palette and labelled ORIGINAL slots with two original floors:
low k-4 at ell slots; high k-3 at f slots.
Assume integer counts satisfy

4ell+f=binomial(k,3), 3f=binomial(k,2).

Equivalently f=k(k-1)/6 and ell=k(k-1)(k-3)/24; the theorem applies only when these are integers.

**X28G — forced two-grade actual protection.** At EVERY exact-four endpoint, each original grade family is an actual three-guard. More precisely every pair is missed by exactly ONE high root and exactly(k-3)/2 low roots. Every support is forced to equal its original floor.

**X28R — complete direct repair.** EVERY pair of exact-four endpoints on this carrier admits finite native one-incidence repair maintaining3<=tau<=4 and restoring the FULL original labelled destination. No hub, slot permutation, external reserve, independent outside-slot degree or universal guard-availability assumption is needed.

The counts are conditional carrier hypotheses, NOT an assertion that exact-four endpoints exist for every qualifying k. k7 overlaps the accepted X27 ell7/f7 case.

**X28F — nonvacuous mixed control.** On k9 there is a self-contained specified exact-four carrier with ell18 floor-five slots and f12 floor-six slots (r30). Thus X28R closes EVERY exact endpoint pair on this original mixed carrier, in any ordering of the floors. The symbolic construction and supplied minimum four-cover are proved below without external classification or scientific enumeration.

Native rules remain fixed: one incidence in one labelled slot per primitive, fixed palette/original positive floors; temporary larger supports, background changes and repeated incidences are permitted. No geometry or fundamental time is introduced.

## 2. Saturation forces compact supports and unique triple witnesses

At exact four, EVERY triple K fails to hit the whole root family, so K is contained in an actual complement B_i=P minus E_i.

A low-slot complement has size at most4 and contains at most FOUR triples. A high complement has size at most3 and contains at most ONE. Thus the sum of all actual triple-witness capacities is at most4ell+f=binomial(k,3). Covering every triple requires at least that many incidences. Consequently equality holds:
- every triple is contained in EXACTLY ONE actual complementary block;
- every low complement has size4 and every high complement size3.

Indeed a smaller low block loses at least three triple incidences, and a smaller high block loses its one incidence, incompatible with equality. Hence every ORIGINAL support is already compact. No deletion or native simplification was used to infer this. The statement also rules out originally noncompact exact endpoints IN THIS class; the broader repair method below still states how cover-retaining compaction would work if needed.

For a pair uv let p4(uv),p3(uv) count the ORIGINAL low/high complementary blocks containing it. Count the k-2 triples containing uv in the SAME unique-witness partition. A four-block containing uv contributes two triples, a three-block one. Therefore

2p4(uv)+p3(uv)=k-2.

Since k is odd, p3 is odd and at least1 for EVERY pair. Sum over all pairs:
sum p3=3f=binomial(k,2).
There are exactly binomial(k,2) pairs, each contributing at least1. Thus p3=1 for EVERY pair, and p4=(k-3)/2>=2.

A block containing a pair means its ACTUAL root misses that pair. The high family and low family therefore EACH protect EVERY forbidden two-label hitting set. Every smaller set can be padded to a pair, so each is an actual three-guard. These witnesses use the SAME existing supports; there are no independent capacities for overlapping pair obligations. This proves X28G and generalizes X27's zero-excess argument.

## 3. Actual direct endpoint handover, renewal and finite progress

Let A,C be arbitrary permitted exact-four endpoints. Their original grade indices L,F are fixed by the ORIGINAL floor vector, not selected by an input-dependent permutation. Section2 supplies both guards at both endpoints.

First HOLD ALL source high supports A_i,i in F unchanged. Repair every low slot to its ACTUAL destination C_i: add all missing destination labels in palette order, then remove every old-only label. Each intermediate forbidden pair misses a fixed actual source-high root.

After all low slots equal C, the ACTUAL destination low family is installed and is a three-guard. Now HOLD ALL those low supports fixed while repairing every high slot similarly to its actual C_i. Each forbidden pair misses an installed actual destination-low root.

Source-high and destination-low guards occupy DISJOINT original indices, although their label supports may overlap extensively. Shared labels create no spare-capacity assumption: only existing incidences are added, with temporary larger supports allowed. The replacement guard is installed BEFORE the old high protection changes. No simultaneous move occurs.

Each addition retains the current original floor. Each deletion leaves the entire destination C_i, whose size meets that same ORIGINAL floor. Palette legality holds because additions are labels from C_i subset P. An unfinished root supplies its next missing incidence; after these additions, any remaining difference supplies an old-only deletion. Every scheduled primitive decreases that root's symmetric difference with C_i by one. Finite phase and slot lists terminate at the FULL original labelled tuple C. Previously completed supports remain correct.

Thus a complete finite LOWER path A->C with tau>=3 exists. It may rise above4 after some deletions, so no direct upper-band claim is made for its schedule. Apply accepted maximum-layer theorem A ONLY to the completed path between the ACTUAL exact-four original endpoints, in the union-closed original positive-floor carrier. It yields a finite path with tau in{3,4}, preserving both endpoints and all floors. It need not preserve length or scheduling properties. This proves X28R.

For any finite sequence of exact endpoints, the same theorem applies to each consecutive pair. The end of every leg again has guards in BOTH original grades by X28G. Renewal during the preliminary leg occurs when the destination-low family is installed; exact-four resetting after each handover is not required.

For clarity about noncompact restoration: general exact preparation retains a minimum four-cover label in each chosen original-floor subset and deletes excess incidences individually, preserving exactness and saving the reverse. Applying the lower construction to the compact endpoints and reversing the actual saved destination preparation restores every noncompact support. In the present saturated class Section2 proves those preparations have ZERO moves; no unsupported noncompact endpoint is claimed to exist. Converted repair still restores the precise labelled original C.

## 4. Self-contained nine-label support construction

Let F be the nine-element field F3[t]/(t^2-2). The polynomial is irreducible because the only squares in F3 are0 and1, so2 is not a square. Elements are a+bt for a,b in F3, with t^2=2. Order these nine symbols lexicographically by(a,b). These are the NINE native palette labels.

For defining a finite list of subsets only, use the AUXILIARY indexing set X=F union{infinity}, of size10. Infinity is never a native palette label, never an incidence, and never an additional root. The resulting native complements below are all subsets of F.

Invertible2x2 matrices over F, identified up to a nonzero scalar, act on X by fractional-linear bijections

z -> (az+b)/(cz+d),

with the usual explicitly defined conventions: a denominator zero maps to infinity; infinity maps to a/c when c!=0 and to infinity when c=0. A nonzero determinant makes this action invertible.

There are(9^2-1)(9^2-9)=80*72 invertible matrices: choose a nonzero first column and a second outside its nine-element span. Dividing by the eight possible nonzero scalars gives720 distinct fractional-linear maps. Distinct scalar classes give distinct maps: a map fixing infinity,0,1 is necessarily identity (fixing infinity makes c0, fixing0 makes b0, fixing1 makes a=d).

This group acts SHARPLY transitively on ordered triples of distinct X symbols. Existence follows by sending any triple(u,v,w) to(infinity,0,1). For finite distinct u,v,w an explicit map is

z -> ((w-u)/(w-v))*((z-v)/(z-u)).

When one entry is infinity, take the corresponding simplified affine/reciprocal formula; for example u=infinity gives(z-v)/(w-v), v=infinity gives(w-u)/(z-u), w=infinity gives(z-v)/(z-u). These formulas supply all cases and have nonzero determinant. Uniqueness follows because a map fixing infinity,0,1 is identity.

Let B0={infinity,0,1,2}, the four symbols of F3 union{infinity}, and let B be its orbit as UNORDERED four-subsets under these720 maps.

Its setwise stabilizer has exactly24 maps. The fractional-linear subgroup with coefficients in F3 has(3^2-1)(3^2-3)/(3-1)=24 scalar classes; all preserve B0 and induce distinct permutations of its four symbols. Conversely any stabilizer element is determined by its images of three B0 symbols, so there are at most4*3*2=24. Therefore the orbit has720/24=THIRTY distinct four-blocks.

Every unordered triple of X lies in the same number lambda of orbit blocks, since the group is transitive on triples and preserves the orbit. The thirty blocks supply30*binomial(4,3)=120 triple incidences; X has binomial(10,3)=120 triples. Thus lambda=1: EVERY triple is contained in EXACTLY ONE four-block. This is an algebraic orbit/count proof, not an executed enumeration or an externally assumed design theorem.

Exactly TWELVE blocks contain infinity: each covers three pairs among the other nine labels, and every such pair lies in a unique block containing infinity. Hence3 times this block count equals binomial(9,2)=36. The other EIGHTEEN blocks avoid infinity.

Define the native complementary blocks:
- for each of the eighteen orbit blocks avoiding infinity, retain that actual size4 subset of F as a LOW complement;
- for each of the twelve orbit blocks containing infinity, remove infinity and retain the resulting size3 subset of F as a HIGH complement.

Every triple of F is covered EXACTLY ONCE: its unique orbit block either avoids infinity and is retained, or contains infinity and reduces to that very triple. All thirty complementary blocks are distinct within each original grade. Their ROOT supports in F have sizes5 and6, respectively. Assign these tokens to eighteen original floor-five and twelve original floor-six slots in any fixed ordering. This is a definition of a legal endpoint, not a simultaneous native edit or a claim that field labels constrain later moves.

## 5. Supplied exact-four cover for the control

The preceding actual triple witnesses prove the native tuple has tau>=4. We must supply a four-cover; triple witnessing alone would not exclude tau>4.

Take H={0,1,t,2+t}. Its four elements are distinct. A size3 complement cannot contain H. We prove H is not one of the size4 complements.

The unique orbit block through{0,1,t} has fourth symbol1+t. Here is an explicit derivation rather than a classification assertion. The map

g(z)=t(z-1)/((t-1)z)

sends(0,1,t) to(infinity,0,1). All denominators and conventions are legal because t!=0,1. The unique orbit block containing infinity,0,1 is B0 itself; therefore the fourth symbol d in the block through0,1,t satisfies g(d)=2. Rearranging gives

t(d-1)=2(t-1)d,
(2-t)d=t,
d=t/(2-t)=1+t,

using t^2=2 and arithmetic modulo3. No solution at infinity occurs, since g(infinity)=t/(t-1)!=2; equality would give t2. The denominator2-t is nonzero.

Thus H, whose fourth element is2+t rather than1+t, is not an orbit block. It is not contained in ANY native complement: those have size3 or4, and containment in a size4 complement would force equality with H. Therefore H meets EVERY actual root. This gives tau<=4 and proves exact FOUR.

The actual low/high counts are ell18,f12, with4ell+f=84=binomial(9,3) and3f=36=binomial(9,2). X28G/R apply. This proves X28F and shows the extension is nonvacuous beyond seven labels. No existence for other odd palettes follows from this one symbolic constructor.

## 6. Inherited domains and genuine method distinction

The new mechanism depends on the native complement identity, X27's disclosed shared multiplicity counting principle and baseline maximum-layer A. Neither full token permutation M nor a canonical accessibility theorem is needed for X28R. Actual ORIGINAL grade protection is forced directly, allowing full destination repair between arbitrary endpoints.

For the nine-label control S=18*5+12*6=162. Every exact compact endpoint has maximum degree M>=ceil(162/9)=18. X14C would require r>=2D+2 with D>=18, hence r>=38>30. X15N would require r>=D+M+1, implying D<=11; its other requirement S<=Dk would give162<=99, impossible. Therefore neither whole-carrier cap/degree theorem applies for ANY admissible parameter choice.

The control has genuine original floors5/6, not uniform3/4. It has no floor1/2 and no cover-automatic floor>=k-2=7; X17's stated automatic lift therefore does not apply. Palette-room AE's k>=S fails. X21W requires k>=3b+1=19; X21H requires k>=7ceil(b/4)+b=20, both failing at k9. X23F's block module requires k>=8ceil(b/4)=16, failing. X23's broader graded theorem would still require a supplied compatible exact base and capable-slot degree, not inferred from general mixed admissibility. No blanket failure of every conditional older guard bridge is claimed; some actual pairs may already have such certificates.

The point is a STRUCTURAL family of carriers whose actual two-grade guards are forced by exact feasibility and saturation. The theorem is not another finite passing campaign. It removes independently supplied outside-slot room and canonical-hub access in this class, although its exact saturation and balance hypotheses remain explicit.

## 7. Review, limits and remaining obligations

Review must check parity uses ODD k, unique triple witness equality forces original compaction, both ACTUAL grade guards cover EVERY pair, fixed original grade indices/disjoint renewal, floor-safe individual edits, eligible next move and finite progress, upper conversion only after complete exact-ended path, full labelled endpoint restoration/repeated reuse, integer feasibility limits, self-contained field/orbit/stabilizer/triple arguments, auxiliary infinity never becoming a native resource, supplied H and unique fourth completion, and inherited method domains.

Frozen inherited sources at parentae080ab1799cc093b2bfc9c67363f57511cf04b9 remain unchanged: X27 shared witness identities; X14/X15 cap/degree domains; X17 automatic lift; X21/X23 floor/palette module domains. Baseline GENERAL_PARENT_CONNECTIVITY A/AE references apply only under their actual native positive-floor hypotheses; AE is used here only as a method comparison.

Remaining mathematical direction: relax exact saturation/balance using rigorous shared multiplicity constraints, or construct genuinely reusable multiple-overlap handovers when forced disjoint-grade guards are unavailable. No equivalence between failed route and native disconnection, no universal safe-prefix completion and no cloning/path shortcut. All previous accepted results and failed-method classifications remain preserved.

Original A11 destination-directed scheduling, unrestricted mixed/higher-target/nested and physical interpretation remain OPEN. Conditional lifting retains exact-child/fixed-root-clearance hypotheses. Field coordinates merely specify finite sets and add no geometry to native admissibility. Ordered repair/retained recoverability, no fundamental time or physical metric/energy/gravity claim.

No scientific numerical enumeration/tests/workflows/run IDs, implementation/benchmark or certified integration merge. Numbered v16.55 remains OPEN pending prospective execution scope, independent complete reconstruction, rejecting controls, inherited replay/logs, deterministic reproduction/durable evidence, exact merge review/post-merge audit. Certified v16.54 and separately accepted efficiency design stay unchanged; runner execution and measured speedup remain unstarted.
