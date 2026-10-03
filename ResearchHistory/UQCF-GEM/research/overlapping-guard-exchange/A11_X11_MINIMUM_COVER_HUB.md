# A11.X11 — minimum-cover completion creates economical exact hubs

Scope commit: a2fc08e6f1d5a4efbc7fee546acec34318cdfe72.
Supplemental scope commit: 353060178e818a9cb7196d2a90620033558d5783.
Parent analytical publication: 6b7e810915f443d2e50b6f63e9f7ae3883223e67.
Certified integrated baseline: 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Analytical candidate frozen for fresh independent whole-argument review. No execution.

## 1. Statements and native scope

Fix a finite ordered palette P, |P|=k, r labelled root slots and uniform ORIGINAL floor h>=2. A root is any subset of P of size at least h. A primitive toggles one incidence in one root, preserving that floor. Intermediate supports may be larger than h, and repeated toggles/temporary incidences are allowed. Exact endpoints have transversal q>=3. Set t=q-1 and B=binomial(h+t-1,h).

**Lemma X11H (minimum-cover completion).** Suppose an explicitly specified family G of m floor-safe supports has transversal EXACTLY t. Let D be its family of ALL minimum t-label covers, c=|D|. If k-t>=h, then G together with the c supports P minus H, H in D, has transversal exactly q=t+1. It is an exact hub using m+c existing slots when that many slots are available. Duplicate any guard support to fill further existing slots; exactness and the m-root guard persist.

**Theorem X11 (guard-to-hub completion).** Under the construction hypotheses, if

r>=m+c and r>=m+min(floor(r*(k-h)/k),B-1)-1,

then EVERY exact-q endpoint pair on that carrier has a finite native primitive path with tau in {q-1,q}, restoring every original labelled destination support. In particular r>=max(m+c,m+B-2) suffices.

The two inequalities are distinct: enough slots to REALIZE an exact hub, and enough slots to HAND OVER actual endpoint protection. A convenient hub alone proves no accessibility.

**Lemma X11P (grouped-cover completion).** For a specified t-guard G, a specified (t+1)-cover X of G and b existing reserve slots, an exact-(t+1) extension retaining G and covered by X exists exactly when ALL minimum t-covers can be partitioned among b groups whose allowed pools each have at least h labels and meet X. Section 4a proves the statement and its construction.

Theorem X11's access proof applies to such a grouped hub with r>=m+b replacing r>=m+c; its actual m-root guard and the same handover budget are unchanged.

**Theorem X11U.** Uniform original floor three, target four: all exact endpoint pairs are connected with 3<=tau<=4 on EVERY feasible finite palette when r>=14. This improves X10's sixteen by a general grouped-cover completion/economical-guard hub mechanism. The ungrouped fifteen-slot consequence remains valid but is superseded for this specialization.

**Corollary X11Seven.** The same full repair holds at k=7,r=14. This closes the previously remaining seven-label carrier using incidence-derived actual endpoint guards, not enumeration. The stronger X11U theorem also closes r=14 on all larger feasible palettes; this corollary records closure of the formerly remaining seven-label carrier.

Neither input endpoint needs a core, the seven-triple pattern, an X5-qualified triple or a common symmetry type. Uniform floors are required for full exact-endpoint guard placement. Original destination-directed scheduling and unrestricted nested universality remain open.

## 2. General completion lemma: cover obligations supply the added supports

Because tau(G)=t, D is nonempty and consists of all its minimum covers, each of size t. Every complement Z_H=P minus H meets the ORIGINAL floor h by k-t>=h. All supports use the original palette.

A set K of size at most t-1 fails to hit G and thus cannot hit the completed family. If |K|=t and K hits G, then K belongs to D and misses its actual added complement support Z_K. Hence no set of at most t labels hits the completed family.

For the upper bound choose any H_0 in D and any label x in P minus H_0, which exists because k-t>=h>=2. The (t+1)-set H_0 union {x} hits G. It also hits EVERY complement Z_H: a set of t+1 distinct labels cannot be contained in the t-set H, so one of those labels belongs to P minus H. Thus the completed family has hitting number exactly t+1.

This identifies ALL forbidden covers, supplies a concrete minimum q-cover and proves floor/palette legality. It does not rely on numerical reconstruction, a chosen subset of minimum covers, or approximate hitting numbers. Duplicate guard roots add no new cover obligation, so padding to r slots preserves exactness and the original m-root t-guard.

Construction assigns these mathematical supports to the given labelled r slots. It introduces no new slot. It is NOT a simultaneous native edit of an arbitrary input endpoint into the hub. Access is the complete path theorem below; until that theorem's budget is satisfied no access is inferred.

## 3. An explicit seven-triple guard and all its minimum covers

Choose seven distinct EXISTING palette labels 1,...,7. Set S={1,...,7} and let G consist of the actual supports

123, 145, 167, 246, 257, 347, 356,

where 123 denotes {1,2,3}, and so on. These are subsets of the fixed palette with original floor three.

Every label belongs to three displayed triples. Each pair of distinct labels lies in exactly one displayed triple. These elementary incidence identities are completely specified by this list: for each first label, its three triples pair the other six labels as follows.

| Label | Other-label pairs in its three triples |
| --- | --- |
| 1 | 23, 45, 67 |
| 2 | 13, 46, 57 |
| 3 | 12, 47, 56 |
| 4 | 15, 26, 37 |
| 5 | 14, 27, 36 |
| 6 | 17, 24, 35 |
| 7 | 16, 25, 34 |

Each row partitions the other six labels, proving pair uniqueness and degree three directly. No external design property or classification is assumed. This finite incidence specification is a mathematical construction, not a new geometry axiom or a scientific enumeration run.

A single core label meets three triples. Two distinct core labels meet 3+3-1=5 triples. Labels outside S meet none. Hence no set of at most two palette labels covers G.

For three distinct labels a,b,c in S, count the triples they meet by inclusion-exclusion. Each label meets three triples, each pair shares exactly one, and all three share a triple exactly when {a,b,c} is one of the displayed supports. Thus their union of incident triples has cardinality

3+3+3-1-1-1+epsilon = 6+epsilon,

where epsilon is one for a displayed triple and zero otherwise. A displayed triple therefore hits all seven supports; any other three-set hits only six. A three-set using an outside-S label contains at most two core labels and hits at most five supports, so cannot cover G.

Consequently tau(G)=3 and its COMPLETE family of minimum three-covers is exactly the seven displayed triples. This proves the hypotheses of X11H without relying on a supplied cover count or unverified background design.

## 4. The economical exact-four hub on the same carrier

For k>=7, put the seven guard supports of Section 3 in seven slots and their seven FULL-PALETTE complements P minus H in seven more slots. These complement supports have size k-3>=4 and therefore satisfy the ORIGINAL floor three. Temporary and endpoint supports above the floor are native admissible; restricting them to triples would lose the stated construction.

Lemma X11H makes this fourteen-root tuple exact four. For example the four-cover {1,2,3,4} hits the guard and every complement support. Every pair misses a guard support, and every guard-covering triple H misses its particular complement root. Other triples already miss a guard root. Thus every forbidden pair AND triple has an actual root witness.

For r>=14 fill remaining existing labelled slots with copies of 123. This keeps tau=4 and the actual seven-root guard. Labels outside S can occur in complement supports. They are never added to the palette; all r slots already belong to the carrier. At k=7 the guard/complement support sizes are three/four. At larger k the complement roots remain legal and the identical argument proves exactness.

This exact hub has a smaller ACTUAL guard than X10's core hub: seven rather than eight. It is not obtained by asserting that every endpoint itself has a seven-root guard. Arbitrary endpoint guard availability still comes from accepted X9 or incidence counting.

## 4a. Grouped covers: exact hub creation from actual safe pools

Fix a family G with tau(G)=t and floor-safe supports, its COMPLETE minimum t-cover family D, and a supplied set X of exactly t+1 labels hitting G. Let b>=1 reserve slots have uniform original floor h. Partition D among groups D_1,...,D_b; empty groups are permitted. Write

U_j=union of H in D_j, W_j=P minus U_j.

**Lemma X11P.** An exact-(t+1) extension of G by b original-floor-h supports, with X hitting the completed tuple, exists IF AND ONLY IF some such partition satisfies

|W_j|>=h and X intersect W_j nonempty for every j.

Sufficiency: choose an h-subset Z_j of W_j retaining one label of X intersect W_j. This is possible by BOTH inequalities and respects the original floor. Every H in D_j misses Z_j. A set smaller than t already misses G; a t-cover of G belongs to D and therefore misses an actual reserve. Thus the full tuple has tau>=t+1. X hits G and each chosen reserve, giving tau<=t+1 and exactness. These are mathematical supports in the stated existing slots, not simultaneous edits of an input state.

Necessity: suppose reserve roots Z_1,...,Z_b complete G to exact t+1 and X hits everything. Every H in D must miss at least one reserve, or it would cover the full endpoint with t labels. Assign it to one missed reserve. Then Z_j is contained in W_j, so |W_j|>=|Z_j|>=h; since X hits Z_j, X intersects W_j. This gives the partition with both inequalities. No distinctness among supports is needed, only distinct labelled reserve slots.

This equivalence characterizes extension of THIS specified G with THIS supplied q-cover X and b reserve slots. It does not characterize native connectivity or assert that arbitrary guards admit a cheap extension. Checking only total group capacity is insufficient: the supplied exact upper cover must also meet every allowed pool.

The pool algebra is inherited in spirit from CYCLE_BUFFER and ADAPTIVE_BUFFER_RENEWAL; it is explicitly proved here rather than claimed a new general capacity law. Their pools protect exposed (q-2)-covers during a lower handover. Here the roles are ALL minimum (q-1)-covers of a specified guard, and the additional supplied q-cover controls exactness of a manufactured hub. The application and exact construction/slot count are different.

## 4b. Six-root protection and a thirteen-root exact hub

Remove support123 from the seven-triple family of Section 3. The retained ACTUAL guard is

G'=(145,167,246,257,347,356).

Every pair hits at most five of the original seven supports. Removing just one therefore still leaves at least one of these six missed. The displayed triples are three-covers, so tau(G')=3.

Its COMPLETE family of minimum three-covers is:
- the original seven triples123,145,167,246,257,347,356;
- the four triples456,457,467,567 contained in Q={4,5,6,7}.

Proof of completeness. By Section 3 any core three-set that is not a displayed triple hits six of the original seven and misses exactly one support. It covers all retained six iff that missed support is123, equivalently iff it is disjoint from123, hence is a three-subset of Q. The four displayed Q-triples are indeed nonline triples by inspection of the original list. Sets with outside-core labels have at most two core labels and hit at most five supports; removing one support cannot make five hit supports cover six. Smaller sets have already been excluded. Thus exactly these eleven covers occur, without a numerical enumeration.

Use seven reserve supports as follows. Their assigned groups partition all eleven minimum covers, and each reserve misses every cover in its own group.

| Reserve support | Assigned minimum three-covers | Group union | Allowed pool within S |
| --- | --- | --- | --- |
| 456 | 123 | 123 | 4567 |
| 236 | 145,457 | 1457 | 236 |
| 234 | 167,567 | 1567 | 234 |
| 135 | 246,467 | 2467 | 135 |
| 134 | 257 | 257 | 1346 |
| 126 | 347 | 347 | 1256 |
| 127 | 356,456 | 3456 | 127 |

Here strings denote sets of labels, as before. Every group has an allowed pool of at least three labels, and each specified reserve is a triple in that pool. Choose the supplied four-cover X={1,2,3,4}. It hits all six guard supports because the original line123 hits every original line. It hits reserve456 at4, and each other reserve contains two labels from123. Thus every selected reserve is met by X, certifying BOTH conditions of X11P directly.

The six guard roots and these seven reserves give an exact-four THIRTEEN-slot hub with an actual six-root three-guard. Every palette pair misses a guard root. Every guard-covering triple is one of the eleven listed and misses its assigned reserve; any other triple misses a guard root. The supplied X proves the upper bound. This accounts for ALL forbidden small covers using actual supports.

All thirteen roots have exactly three labels and original floor three. For k>7 use the identical thirteen supports on seven existing labels; leave other palette labels unused. Such labels cannot help hit any root or create an unaccounted minimum cover. The full allowed pool in a group includes these extra labels; the chosen original triples still fit it and meet X. No label or slot is added to the carrier.

Duplicate any guard support to fill further existing slots. In particular one duplicate realizes a fourteen-slot exact hub. The full restoration/access proof below applies with m=6,b=7, so construction requires thirteen slots and guard handover requires only6+9-1=14 with arbitrary X9 endpoint guards. No universal six-root bound for arbitrary input endpoints is claimed.

At k=7 this thirteen-slot realization is optimal for extending this particular six-root guard to exact four: its seven original-line minimum covers must each be missed by a reserve, and a floor-three support cannot miss two different original lines. Any two such lines intersect in exactly one label, so their union has five labels and its palette complement has only two, below the floor. None of the six guard roots misses a minimum cover of itself. Hence seven additional reserve slots are necessary. This is a precise construction bound on THIS retained guard at k=7, not a native barrier or an optimal hub theorem on all carriers.

## 5. Exact endpoint preparation and actual guard availability

Let A,C be arbitrary original exact-q endpoints under Theorem X11's general hypotheses. At each choose a supplied minimum q-cover H. In each root choose an h-subset retaining a label of H and delete the other incidences individually.

Every deletion retains the original floor, and shrinking cannot decrease tau. The retained H keeps tau<=q; hence every preparation state is EXACT q. If excess remains, an incidence outside the chosen retained subset supplies the next eligible deletion. Total excess strictly decreases, so compaction is finite. Its saved reverse restores all original supports.

Accepted X9G supplies an ACTUAL t-guard of size at most B-1 at each compact exact endpoint for uniform h>=2,q>=3. Its classical uniform set-pairs inequality/equality dependency remains explicitly inherited; no new classification is introduced here.

The incidence guard is also available: the compact tuple has hr incidences, so some label has degree at least ceil(hr/k). Its actual avoiding roots number at most N=r-ceil(hr/k)=floor(r*(k-h)/k). If at most q-2 labels covered those roots, adding the omitted label would cover the full tuple with at most q-1 labels, contradicting exact q. Thus those actual roots form a t-guard. Select the smaller available bound

G_A<=min(N,B-1).

The hub is compacted with its own minimum q-cover if necessary. Its m original guard supports may be above the floor in the general theorem. Shrinking them during cover-retaining compaction cannot decrease their transversal; they remain an actual t-guard on the same m slots. In both seven- and six-triple specializations they already have exactly the floor size and remain unchanged. The complementary supports compact legally while retaining the supplied four-cover.

Both compact endpoints are EXACT q before inherited endpoint permutation or maximum-layer conversion. No exact-endpoint redundancy lemma is invoked on a mere level-t intermediate.

## 6. Complete one-sided access: full placement, primitive renewal and progress

We spell out the complete access argument rather than infer it from hub existence. Connect an arbitrary compact exact endpoint E* to the compact exact hub Q*. Let I be its selected actual guard of size a<=min(N,B-1), and let J_0 be the hub's guard of size m. Under r>=a+m-1 at least m-1 existing slots lie outside I.

Assign the hub guard tokens to those outside slots, using at most one slot in I, and extend the assignment to a permutation of ALL r support tokens of Q*. Equal supports may be distinct tokens. Uniform original floor h makes the completed permuted hub Q** admissible and exact q. Save the reverse of accepted Lemma M's finite {q-1,q} path Q*->Q**.

This is a full exact-endpoint permutation, not an edit primitive and not a permutation of an unprotected bare t-guard. M's swap construction adds incidences to the union of the two supports then contracts to swapped destinations, one incidence at a time. At uniform floors each desired token fits both swapped slots. The next desired token lies in an unfixed slot, and each completed swap fixes a destination without moving already fixed slots. Thus an eligible next swap exists and fixed-slot count increases to termination. No arbitrary mixed-floor placement follows.

Write J for the placed hub guard, with |I intersect J|<=1. Its comparison family D on I union J uses the source root at source-exclusive indices, hub root at hub-exclusive indices, and the union of source/hub supports at the possible shared index s.

For a set K with |K|<=t-1, if it hits every exclusive support and there is one shared index, the two actual guard inequalities force K to miss BOTH source_s and hub_s, hence their union. If the guards are disjoint, D contains the unchanged source guard. Thus tau(D)>=t. This is accepted O1 with its full actual witness hypotheses supplied. At target four it handles every pair, with no independence assumption for overlapping protection systems.

Construct a preliminary finite LOWER path:
1. Keep I fixed and replace each hub-exclusive root by its hub destination: add all missing destination labels, then delete all old-only labels.
2. At the shared slot, if present, add to the union and contract to the hub support. All roots on I union J are componentwise subsets of D throughout. A small set missed by a D support remains missed by its current subset.
3. The complete hub guard J is installed. Keep it fixed and repair every remaining root to Q** by its own union path.

Every addition retains the old floor-safe support, and every deletion retains the now-complete destination support. All labels remain in P, all slots are existing, and every primitive toggles one incidence.

The sum of symmetric differences from Q** decreases by one per scheduled primitive. Whenever an unfinished root lacks a destination incidence, that addition is eligible. Once all destination incidences are present, any old-only incidence is an eligible deletion. The phase's persistent guard proves lower protection for each supplied move. Finite phases and finitely many incidence differences prove termination at the full exact Q**.

Renewal is the installed unchanged hub guard before the old guard's remaining slots are repaired. It need not return tau to q at every handover; level t is permitted. This reuses O1's proved mechanism, not a newly claimed necessary multiple-overlap rule.

## 7. Upper conversion, complete labelled restoration and two-leg composition

The preliminary access path keeps tau>=t and may exceed q. Uniform floor h gives finite bound tau<=k-h+1. Accepted maximum-layer Theorem A applies to this ACTUAL finite lower path between exact-q endpoints on the original nonempty union-closed floor carrier. It produces a finite primitive path with tau in {q-1,q}. Its finite layer-removal progress is inherited; no efficiency or schedule preservation is asserted.

Concatenate exact source compaction, converted access, reversed full hub permutation and reversed hub compaction. Each join is exact q. This ends at the ORIGINAL full labelled hub Q, including its larger complement supports and every duplicate token's destination incidence. A lower-level guard tuple or an arbitrary symmetry copy is not the join.

Do this separately for A->Q and C->Q. Reverse the second COMPLETE path and concatenate at the exact labelled Q. The primitive graph is undirected: reversing a legal incidence edit retains legality and the same band. The join is exact q, so deficits do not accumulate. The endpoint is exactly ORIGINAL C in all labelled supports, including initially noncompact incidences. This proves Theorem X11 and its grouped-construction version using m+b realization slots.

Same-slot X5 qualification is unnecessary because X5 is not invoked. The hub contains no assumed copy of an input guard: full exact-endpoint uniform permutation supplies actual compatible placement on each leg. Conditional nested lifting retains baseline Section 7's exact-child and fixed-root-clearance interfaces. No root result is promoted to unrestricted nested connectivity.

## 8. Universal floor-three target-four consequences

For h=3,q=4, t=3,B=10. The original seven-guard/un-grouped construction has m=7,c=7, so r>=max(14,15)=15 suffices. That correctly reviewed initial result remains a corollary.

The grouped construction of Section 4b has m=6,b=7. It needs m+b=13 actual hub slots and

r>=m+(B-1)-1=6+9-1=14

for arbitrary endpoint access. On EVERY palette k>=7 the identical thirteen triples, plus duplicate padding to r, form a full exact-four hub on that carrier. Every arbitrary compact endpoint has an actual guard of at most nine by X9, and the hub has one of at most six. Their sum is at most fifteen<=r+1 at r>=14. The full exact-hub theorem therefore connects EVERY original endpoint pair for k>=7,r>=14.

For k<=5, every k-2 labels hit every root of size at least three, so tau<=k-2<=3 whenever roots exist; exact four is infeasible. For k=6, exact four forces an actual root complementary to EVERY three-label set K: K is not a cover, and a root missing K must equal its three-label complement because of the floor. Different K require the twenty distinct triples and at least twenty slots. Thus r=14,...,19 at k=6 is infeasible. For k=6,r>=20 accepted X9 already guarantees repair (its all-palette threshold is seventeen). Palettes too small to meet the floor have no endpoints. This proves X11U across every feasible palette, without enumeration or execution.

At k=7,r=14, the source incidence bound N=floor(14*4/7)=8 improves nine to eight and either the original seven-guard/fourteen-root hub or the strengthened six-guard/thirteen-root hub supplies access. This proves X11Seven and closes the previously remaining seven-label fourteen-slot obligation. At k=7,r=13, the strengthened hub itself fits, N=floor(13*4/7)=7, and6+7-1=12<=13 supplies access; that carrier was already accepted under X8. Existing accepted results and the new fourteen-slot closure leave no prior seven-label residual carrier obligation.

For larger palettes at r=13, the strengthened hub exists but an arbitrary endpoint's bound can be nine, requiring fourteen slots for the supplied O1 placement. Hub existence alone does NOT settle those carriers. Universal r=13 for every palette remains OPEN; actual smaller guards or other accepted classes may still apply.

## 9. Consolidated meaning, inherited method boundaries and open obligation

X10 established that exactness can replace a group of core selections with one actual root, and that a suitably protected exact hub permits complete access. X11 supplies a general way to manufacture an EXACT hub from a specified guard by completing ALL its minimum-cover obligations, either separately or grouped into actual floor-safe reserves met by a supplied exact upper cover. The six-triple instance reduces the hub guard size, hence the all-palette access budget. It does not assert a universal seven-root bound for arbitrary exact endpoints.

The constructor uses only native supports on existing labels/slots. It explains how the protection mechanism can be reached and reset to a full exact hub; it is not a proposal to install all supports at once or to assume an arbitrary safe prefix can finish. Exact access on each leg plus original hub restoration makes the mechanism reusable for any finite chain of exact endpoints on the proved carrier.

Inherited solved classes are not erased: floor-one/two anchor results have different original floors; target three is already accepted; palette-room, protected disjoint roots, saturation, modules/cyclic classes and symmetries remain sufficient in their stated domains. The new all-palette fourteen-slot theorem does not assume their special input structure. At k=8,r=14, X9's N=floor(14*5/8)=8 and B-1=9 give a universal criterion requiring r>=15, which fails at fourteen; X10's universal criterion requires sixteen. X11 proves ALL endpoints there and on every larger feasible palette by the same thirteen-root hub with duplicate padding, not just a selected example. Some individual pairs may already satisfy conditional accepted methods.

Minimum-cover completion is analytical finite construction, not an efficient algorithm: c can be large and computing all covers may be costly. The seven- and six-triple specializations explicitly characterize their COMPLETE seven/eleven covers and supplied grouping, needing no broad search. No new external design/equality assumption is introduced; X9's classical equality input is inherited only for the arbitrary endpoint guard bound. The displayed incidence system is checked locally without an imposed geometry or an originality claim.

Next research remains stronger derived actual guards, a sharper access budget to economical hubs, or genuinely reusable handovers when multiple overlaps are necessary. Residual uniform-floor-three target-four carrier bounds can now use r<=13 and k>=8 before all other accepted exclusions; k=6 is excluded there by the twenty-root argument, and the former seven-label residual is closed. These are method-derived bounds, not a checklist of campaigns. No bound failure, deficient chosen bridge or inability to find a smaller guard proves native disconnection.

Original directed A11 scheduling, mixed-floor placement, general higher-target universality, universal floor-three target-four repair below fourteen and unrestricted native/nested repair remain open. The scientific statement is ordered repair and retained recoverability; no fundamental time, physical energy or geometry is introduced.

## 10. Fresh whole-argument gate and execution boundary

Independent review must check: ungrouped and grouped ALL-cover completion, pool capacity PLUS supplied exact upper-cover incidence, constructive sufficiency and fixed-class necessity; explicit degree/pair identities and every minimum-cover case including outside labels; construction slot count versus access count; actual full-palette complement supports above floors AND compact thirteen-slot grouped hub including the local construction-optimality boundary; exact compaction preserving guard lower protection; X9/X7 availability domains; full exact-endpoint uniform permutation; O1 shared witnesses, primitives and renewed next-move existence; termination and finite upper conversion; complete original hub restoration, reversal and exact two-leg join; small-palette exclusions, universalr14 and k7/r14 arithmetic and residual claims; inherited conditional child interfaces.

Immutable dependency sources: X9 reviewed candidate31566452722b73d833250f1132a154883a73d60f/publicationfe8085d006e8e8b6c24a5b70613eaf573bf518ed; analytical parent6b7e810915f443d2e50b6f63e9f7ae3883223e67 GUARD_HANDOVER O1 and X10; baseline466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f GENERAL_PARENT_CONNECTIVITY A/childinterfaces and OVERLAPPING_CLIQUE_EXCHANGE M. Frozen proofs/certificates remain unchanged.

No scientific enumeration, numerical diagnostic, tests, workflow, benchmark, new implementation version or certified integration merge. The separately promised read-only efficiency baseline/design remains complete; runner implementation/execution remains unstarted.
