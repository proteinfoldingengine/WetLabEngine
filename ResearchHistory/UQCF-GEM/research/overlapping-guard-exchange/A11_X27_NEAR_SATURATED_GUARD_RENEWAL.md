# A11.X27 — near-saturated witness parity and forced guard renewal

Scope:41f64e0cb669eeeeacc6271f831300bef20640a7.
Parent:46b876e090f16c01102fdf6b36aa9a0865a3312b.
Certified baseline:466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Frozen candidate for fresh independent whole-argument review. Analytical only.

## 1. Statements and native domain

Fix seven ordered labels, labelled original slots with floors3/4, and ell original floor-three slots. Endpoints are exact-four hitting families. Each primitive changes ONE incidence in ONE slot; all original floors remain fixed. Temporary larger supports, repeated/background edits are allowed.

X27B: For actual complementary blocks of sizes4/3 covering every triple, write f for the number of size3 blocks and delta=4ell+f-35 for excess triple multiplicity. Then f>=7-delta; when0<delta<=6, f>=8-delta.

X27G: At original-floor exact compaction with ell7,f7 or8, the ACTUAL original low-slot family is a three-guard: every palette pair misses a low root. At f7 both original grades are three-guards.

X27R: Every seven-label original3/4 carrier with ell7 has exact-four endpoints iff r>=14; every exact-four pair has finite native{3,4} repair restoring the FULL original labelled/noncompact destination.

X27Q: There is a fourteen-token exact-four hub with EIGHT triple tokens, six four-support tokens, a supplied minimum four-cover and an actual five-triple three-guard.

X27E: Every seven-label original3/4 carrier with ell8 has exact-four endpoints iff r>=14 and complete native{3,4} repair. Combined with inherited X26, EVERY feasible seven-label original3/4 carrier with ell<=8 has complete repair. For ell<=7 feasibility is iff r>=35-3ell; for ell8 it is iff r>=14.

No universal mixed-floor, destination-directed, higher-target or unrestricted nested theorem is asserted. These are structural witness constraints, not numerical passing cases.

## 2. Exact preparation and shared multiplicity identities

Choose a minimum four-cover H of each original endpoint. In slot i retain an a_i-subset meeting H and delete excess incidences individually. Deletion cannot lower tau, retained H keeps tau<=4, and the original floor is retained. Every unfinished slot supplies an excess incidence; total excess decreases. Save the reverse for complete original restoration.

In this compact exact endpoint, low-root complements are actual size4 blocks; high-root complements are actual size3 blocks. Every triple is contained in at least one such complement, because no triple hits the full exact-four family. Blocks are indexed by ORIGINAL slots, counting multiplicities.

For any k-label palette with these complementary block sizes, define mu(K)=number of actual blocks containing the triple K minus1. Write p4(uv),p3(uv) for actual block counts containing pair uv, d4(u),d3(u) for block degrees, e_uv=sum_(K containing uv)mu(K), and m_u=sum_(K containing u)mu(K). Counting the SAME actual incidences gives

2p4(uv)+p3(uv)=k-2+e_uv,
3d4(u)+d3(u)=binomial(k-1,2)+m_u.

A four-block contributes two triples through a pair and three through a vertex; a three-block contributes one. Thus delta=sum_K mu(K), sum_pairs e_uv=3delta and sum_u m_u=3delta. No separate capacities are assigned to different pair obligations.

## 3. Seven-label strict parity bound

At k7,2p4+p3=5+e. Let O be the number of pairs with odd e. Every pair with even e has odd p3>=1. Hence3f=sum_pairs p3>=21-O>=21-3delta, giving f>=7-delta.

Suppose equality f=7-delta holds at0<delta<=6. Both inequalities must be equality. Thus O=3delta=sum e, every positive e equals1, and p3 equals0 on exceptional pairs and1 elsewhere. Excess triples have multiplicity1 and are pairwise pair-disjoint: any repeated excess or shared pair would give e>=2.

Each vertex belongs to m_u excess triples. Their other two vertices are distinct, so m_u<=3. Exactly2m_u incident pairs are exceptional. Consequently2d3(u)=6-2m_u and d3=3-m_u. The vertex identity3d4+d3=15+m_u implies m_u divisible by3. Therefore every used excess vertex has degree3 and every unused one degree0.

The sum of excess vertex degrees is3delta, so there are exactly delta used vertices. A used vertex's three pairwise linear excess triples require six DISTINCT other used vertices. Thus at least seven used vertices exist, contradicting delta<=6. Equality is impossible; f>=8-delta. This proves X27B as a necessary structural bound, not a feasibility assertion.

## 4. Forced low protection at zero or one excess witness

For ell7,f7,delta0. Every pair has odd p3>=1. Since sum p3=21, p3=1 for every pair; the pair identity gives p4=2. Every pair lies in a complement in EACH original grade, hence misses an actual root in each grade.

For ell7,f8,delta1. Exactly one triple K0 has excess multiplicity1; all other triples have zero excess. Suppose a pair uv has p4(uv)=0.

If uv subset K0, then p3(uv)=6. There are only five distinct triples through uv, so the actual high blocks must include all five, with K0 repeated. Each other pair of K0 occurs in at least two high blocks. The eighteen pairs outside K0 have odd p3>=1. Thus sum p3>=6+2+2+18=28>24=3f, contradiction.

If uv is not contained in K0, p3(uv)=5. No triple through uv can repeat, since only K0 repeats. Therefore five high blocks are exactly uvx for the five outside labels x. The other THREE high blocks cannot contain uv.

Put S=P minus{u,v}, and let a be the number of endpoints u,v outside K0; a is1 or2. For each such endpoint w the vertex identity gives3d4(w)+d3(w)=15. Its five displayed high blocks imply5<=d3(w)<=8, so d3(w)=6. At least one of the remaining three high blocks contains w. The blocks needed for the a endpoints are DISTINCT, since no remaining block contains both u,v.

Each such block contains at most one pair entirely in S; every other remaining block contains at most three. Thus the remaining high blocks cover at most9-2a DISTINCT S-pairs. The first five cover zero S-pairs. Every S-pair not contained in K0 has odd p3>=1 and must be covered. If a1, K0 meets S in two labels and NINE S-pairs require coverage, exceeding7. If a2, K0 meets S in three labels and SEVEN require coverage, exceeding5. Contradiction.

Thus every pair has p4>=1. Its actual original low root complement supplies a missed-root witness. This proves X27G for ALL pair types without treating overlapping high blocks as independent reserves. No high-grade guard is claimed forced at delta1.

## 5. Forced protection installs replacement protection and completes repair

Use inherited X26Q's explicit Q7:
low triples123,145,167,246,257,347,356;
high supports4567,2367,2345,1357,1346,1256,1247.
The displayed triples cover every pair exactly once; distinct triples intersect once, so the three-subsets in their complements partition the other twenty-eight triples. Accordingly every triple misses an actual Q7 root. H=1234 hits every root. Q7 is EXACT FOUR and its seven high roots form a three-guard (each pair lies in a displayed low triple and misses its high complement).

At ell7,r14/15 place the seven low tokens in the ORIGINAL low slots and the seven high tokens in seven ORIGINAL high slots, in fixed orders. At r15 put a duplicate4567 in the remaining high slot. This specifies the SAME FULL legal exact-four Q for both endpoint legs.

At arbitrary compact exact E*, its seven low roots are the actual guard from Section4. HOLD ALL THESE ROOTS FIXED while repairing each HIGH slot to its full Q support: add every missing destination incidence, then remove every old-only incidence. Every forbidden pair misses a fixed low root. Additions retain floors; deletions retain the full size4 destination.

All Q high roots are now installed and form an actual three-guard, disjoint in slot indices from the old low guard. HOLD this installed high guard fixed while repairing every low slot similarly to its size3 Q destination. Every pair now misses an installed high root. Protection is renewed BEFORE the last old protecting support is changed; there is no assumed spare incidence slot.

Each unfinished scheduled root supplies a missing incidence, or after additions an old-only incidence. Its symmetric difference decreases per edit. A finite slot/phase order gives finite termination at FULL exact Q. The preliminary path maintains tau>=3 but may exceed4. Apply accepted maximum-layer theorem A ONLY to this COMPLETE lower leg between exact-four E*,Q in the original union-closed positive-floor carrier. The converted path maintains3<=tau<=4; conversion need not preserve its schedule or length.

Prepend exact source compaction. Construct the same leg C->Q, reverse it and join at the IDENTICAL full labelled Q. Reverse destination compaction restores every original incidence and noncompact support in its ORIGINAL slot. The installed guards support repeated full endpoint legs; exact-four resetting after individual handovers is unnecessary. This is a guaranteed complete repair, not only a safe local edit.

For ell7 weighted triple capacity requires4ell+f>=35, hence f>=7 and r>=14. Q7 with high duplicates proves feasibility at every r>=14. The preceding construction handles r14/15; inherited X26R handles r>=16 because f>=9 and r>=35-3*7. This proves X27R without arbitrary mixed-floor slot permutations.

## 6. Eight-small-token fourteen-root exact hub

Inherit X25's ACTUAL five-triple guard G={123,145,246,257,367}, tau3, and its complete minimum three-cover classification:

123,126,127,156,147,167,
234,246,247,235,256,257,
345,347,356.

New disjoint assigned groups and actual reserve supports are:
(126,127,167)->345;
(234,247,347)->156;
(235,256,356)->147.

Their respective unions are1267,2347,2356, so the specified triple supports miss every assigned cover. The nine assigned covers are distinct. The SIX remaining covers are123,156,147,246,257,345. Give them respective four-support complements4567,2347,2356,1357,1346,1267.

The resulting hub comprises FIVE guard triples, THREE reserve triples and SIX four-supports: fourteen roots, eight triple tokens. Each minimum guard three-cover misses its assigned ACTUAL reserve. Any other three-set fails to hit G and misses an actual guard root. Every three-set therefore misses a full hub root. H=1234 hits all five guard triples, all three triple reserves345,156,147, and every four-support since4+4>7. Thus the full hub is EXACT FOUR with supplied minimum H. This proves X27Q, using the inherited complete classification openly and checking every NEW group.

## 7. Feasibility forces graded access for eight low slots

For ell8 weighted capacity gives f>=3. If r<=13 then f<=5:
f3 gives delta0 and Section3 requires f>=7;
f4 gives delta1 and requires f>=7;
f5 gives delta2 and requires f>=6.
All contradict. Thus any exact-four endpoint requires f>=6,r>=14.

Conversely place Section6's eight small tokens in the eight ORIGINAL low slots and its six four-tokens in high slots. Any further high slots receive duplicate4567, which is hit by H. The base preserves the lower exact-four bound, so the FULL padded hub is exact4. This proves feasibility for every r>=14.

For complete access apply accepted X23A with h3,b4,n8,m5. The restricted compact-source incidence is exactly3ell=24. Some actual label has ORIGINAL low-slot degree at least ceil(24/7)=4=m-1. Its ALL-root avoiding family is an actual three-guard: a two-cover with the label appended would contradict exact4.

Four small destination guard tokens fit distinct original low slots OUTSIDE that source guard; the fifth fits a distinct remaining low slot, causing at most one overlap. The three other small tokens fit remaining low slots; every other FULL token is size4 and fits all remaining original floors. Hence the full assignment is legal, not an arbitrary mixed compact permutation.

Baseline M legally permutes full hub tokens with decreasing-floor swaps, saving the reverse. O1 installs the destination guard before repairing all remaining supports. At its possible single shared slot a pair either misses an exclusive support, or both guard inequalities force it to miss BOTH shared endpoint supports and hence their union. These are actual all-pair witnesses through the handover. One-incidence union edits retain floors; scheduled symmetric differences decrease and every unfinished root supplies a next edit. The installed guard renews protection. Apply A to the COMPLETE exact-ended lower leg, then the saved full hub return. Both endpoint legs join at the identical FULL labelled hub; saved destination compaction restores every original support. All inherited X23A hypotheses are supplied. This proves X27E.

X26E already closes ell<=6. X27R supplies ell7 and this section ell8. The consolidated ell<=8 statement follows. Feasibility conditions are proved separately from connectivity; impossible weighted/parity profiles are not disconnection claims.

## 8. Limits, dependencies and scientific distinction

This removes X26's independent outside-HIGH-slot degree condition at the tight ell7 carriers: exact shared witness constraints force an actual LOW guard instead. That guard installs a disjoint replacement high guard using existing relationships. The reusable two-phase construction then reaches a common exact labelled hub and restores arbitrary endpoints. For ell8, a new overlapping cover grouping removes X25's ninth-small-slot requirement at fourteen roots; a structural parity bound excludes all smaller counts.

No universal spare buffer, safe-prefix completion, canonical accessibility or independent pair-capacity assumption is made. Actual guards, eligible decreasing edits, renewal, termination, exact entry and full labelled restoration are supplied separately. No general impossibility of other mechanisms is claimed.

Inherited frozen sources remain unchanged: X23 graded FULL access and actual M/O1/A composition; X24 weighted capacity; X25 five-guard/minimum-cover classification; X26 specified Q7, high guard and ell<=6/r>=16 consequences, all at parent46b876e090f16c01102fdf6b36aa9a0865a3312b. Baseline OVERLAPPING_CLIQUE_EXCHANGE M and GENERAL_PARENT_CONNECTIVITY A at466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f apply to ORIGINAL positive floors. Root-only conclusions retain exact-child/fixed-root-clearance restrictions for conditional lifting.

Fresh whole-argument review must check strict parity equality consequences, both one-excess cases, every shared pair witness, original grade placement, disjoint renewal, eligible progress/termination, exact Q and H, new grouped cover partition, X23 mixed FULL permutation domain, maximum-layer conversion only at exact endpoints and full original restoration.

Remaining seven-label mixed profiles must exclude ALL inherited accepted classes and ell<=8, not be treated as separate campaigns. Stronger shared-multiplicity guard constraints or genuinely reusable multiple-overlap handovers remain the mathematical directions. Higher palettes/floors/targets, original destination-directed A11 and unrestricted nested/physical interpretation remain separate.

No scientific enumeration/tests/workflows/run IDs, implementation, benchmark or certified integration merge. Numbered v16.55 remains OPEN pending prospective execution scope, independent complete reconstruction, rejecting controls, inherited replay/logs, deterministic reproduction/durable evidence, exact merge review and post-merge audit. Certified v16.54 and accepted efficiency design are unchanged; runner execution and measured speedup remain unstarted. Ordered repair/retained recoverability, no fundamental time or inserted geometry.
