# A11.X15 — slack buffers, degree leveling and universal floor-three target-four repair

Scope:bdc8be5e3bcd633de8265c93f44b4b8d5733ab62.
Parent analytical publication:826b0f961a76d0f77871ca65d5c581212a5dcd6a.
Certified integrated baseline:466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Candidate for fresh independent WHOLE-ARGUMENT review, including the consolidated argument. Analytical only.

## 1. Exact new results

**Lemma X15S (arbitrary-capacity incidence repair with strict slack).** Fix labelled rows, original positive floors a_i, a finite ordered palette of k labels, and an integer D>=1. Two compact tuples with row sizes a_i, all label degrees at most D, and total incidence S=sum a_i<Dk connect by one-incidence primitives retaining row floors and label degree at most D throughout. Each completed transfer or cycle returns all rows to size a_i. It reaches the EXACT compact labelled destination and does not require the source and destination column degree vectors to agree.

The reusable buffer may occupy a cycle row, or a supplied row OUTSIDE the cycle. In either case its incidence is restored. This removes the inherited capacity-two limitation and the assumption that a spare column must miss a cycle row.

**Lemma X15L (protected degree leveling).** Suppose a compact tuple has tau>=q-1, q>=3, max label degree at most M, D<=M, S<=Dk, and

r >= D+(q-3)M+1.

There is a finite primitive LOWER path to a tuple of the same compact row sizes and max degree at most D. Each primitive retains tau>=q-1 and original floors. It supplies an eligible move whenever any degree exceeds D, and its completed-transfer excess-degree potential strictly decreases. It need NOT arrive at exact q.

**Theorem X15N (complete repair through a common degree class).** Exact-q original endpoints with arbitrary positive original floors admit complete native {q-1,q} repair if they admit legal exact compactions of max degree at most M, and there is D<=M with S<=Dk and r>=D+(q-3)M+1, provided additionally, in the saturated case S=Dk,

r >= (q-2)D+2.

For S<Dk no additional inequality is needed. Degree leveling, renewed incidence repair and reversed destination leveling furnish a complete LOWER path between original exact endpoints; only THEN apply upper removal. Every original labelled/noncompact destination support is restored.

**Theorem X15U (universal original-floor-three target-four ROOT repair).** For EVERY finite ordered palette and fixed labelled root carrier with uniform ORIGINAL floor three, EVERY pair of exact-four endpoints is connected by a finite native primitive path maintaining

3<=tau<=4.

The original palette, slots and floors are unchanged, and the exact original labelled destination is restored. No X5-qualified entry, spare buffer count, hub shape or destination monotonicity is assumed in the endpoints.

This is a universal root-level upper bound of one unit, not a claim that every pair necessarily needs a positive defect. It is not universal original A11 destination-directed scheduling, arbitrary mixed-floor/higher-target connectivity, unconditional nested universality, physical interpretation or implementation certification.

## 2. Exact compaction and starting protection

Choose a minimum q-label cover H of each original endpoint. In each root retain an a_i-subset meeting H, delete other incidences individually, and save the reverse. Deletion cannot lower tau while H stays a cover, so each deletion is exact q. An excess incidence supplies the next edit; total excess strictly decreases. The original rows are never permuted.

X15N assumes compactions with the stated maximum-degree bound M. The proof does not infer arbitrary compactions are degree bounded. In the floor-three application below, EVERY original endpoint satisfies the actual degree bound, so every cover-retaining compaction preserves it.

At exact four, all roots avoiding a label x form an ACTUAL three-guard: a two-cover of them together with x would cover the full tuple. Those supports use only P minus {x}. Three roots requiring three labels must be pairwise disjoint and at floor three need nine labels. Consequently at k=9 an avoiding guard has at least FOUR actual roots, and every exact endpoint label degree is at most r-4. This statement is used only at exact endpoints.

## 3. Pending incidences and greedy progress for X15S

At every completed macro boundary, pair each row's present non-destination labels with its absent destination labels, making pending edges x->y coloured by that row. Equal row sizes give equal surplus and deficit counts in each row. Pairings can be chosen once using the palette order.

For every label v, the ACTUAL pending graph satisfies

out(v)-in(v)=degree_current(v)-degree_destination(v).

A pending edge ending at a label of degree less than D supplies a greedy transfer: add its destination in its coloured row, then delete its source. The destination incidence is absent and the source present; the row grows by one and returns to its floor. Degrees stay at most D. Remove that pending edge.

If edges remain and no greedy transfer exists, every pending destination label is full, of degree D. Since the destination tuple has degrees at most D, each full label with an incoming edge has an outgoing edge. Following edges supplies a directed cycle; extract a simple cycle with distinct labels. All cycle labels are full. A loop is impossible because a label cannot be both surplus and deficit in one row.

Strict total slack S<Dk supplies a label z of current degree less than D at EVERY completed boundary. It is outside the cycle because cycle labels are full. In this blocked situation it has no pending incoming edge. It is an EXISTING palette label, not an added one.

## 4. Two actual buffer cases and repeated restoration

Write a simple cycle as x_1->x_2,...,x_m->x_1, with m>=2, and let I be its set of row colours. Each row has its original floor size at this boundary.

**Case A: z is absent from a cycle-coloured row.** Choose a cycle edge x_1->x_2 of such a row i, rotating notation if needed. Transfer its source incidence from x_1 to z by add-before-delete. This fills at most one spare slot at z and opens a hole at x_1.

Process the preceding cycle edges in reverse order, x_m->x_1,...,x_2->x_3, each by add-before-delete into the current hole. This propagates the hole until x_2 is underfull. Finally transfer the buffered row-i incidence z->x_2. The cycle's destination incidences are installed; z returns exactly to its original incidence set and degree.

Repeated nonadjacent row colours are safe. Distinct cycle labels and disjoint row surplus/deficit sets keep all directed destination incidences absent and all directed source incidences present until their own transfer. A repeated row returns to its floor after each transfer. Adjacent edges cannot have the same colour. z is outside the cycle, and its temporary row-i incidence is untouched until final restoration.

**Case B: every cycle-coloured row contains z.** Since degree(z)<D, at most D-1 rows contain z, and they include I. Choose any full cycle label, say x_1. Its D actual incident rows cannot all be among those fewer-than-D rows. Thus an ACTUAL row j contains x_1 and misses z. Because I is contained in z's incident rows, j is OUTSIDE the cycle colours.

Transfer row j's x_1 incidence to z by add-before-delete, opening a hole at x_1. This buffer may temporarily displace a correctly placed incidence; it will be restored. Process ALL cycle edges in reverse cyclic order, x_m->x_1,...,x_1->x_2. Each fills the current hole and opens the preceding one; after all cycle edges the hole is again at x_1. Restore row j by z->x_1.

The buffer row is not edited by the cycle. It returns to its exact original support, regardless of whether its original x_1 incidence belongs to the destination. z returns to its exact original incidence set. All cycle rows install only their pending destination incidences and delete their pending non-destination incidences.

In BOTH cases every addition goes into a column with room and every deletion propagates the hole or closes the restored buffer. All label degrees remain at most D. Every primitive adds before removing within its actual row, retaining the original floor. No simultaneous primitive, extra row, new label, cloned capacity or unprotected root permutation is used.

The pending graph is used again only AFTER complete buffer restoration. At that boundary all rows have the prescribed sizes, degrees are at most D, the actual balance identity holds, and S<Dk still supplies a spare label. If differences remain, another greedy transfer or another cycle with one of the two eligible buffer cases exists.

For termination, count pending row surplus/deficit pairs at completed boundaries. A greedy macro resolves one, and a cycle macro resolves every selected cycle edge. A buffer incidence can increase symmetric difference during its temporary use, so no per-primitive monotonicity claim is made here. Each macro has an explicitly finite eligible sequence and strictly decreases the pending count. The process terminates at the EXACT compact destination with every buffer support restored. This proves X15S.

## 5. Protected degree-leveling proof

For X15L use potential

Phi=sum_x max(degree(x)-D,0)

at completed-transfer compact boundaries. If Phi>0, choose a label x of degree greater than D. Since S<=Dk, some label y has degree less than D; otherwise the above-D label would force S>Dk. Thus degree(x)>degree(y), supplying an actual row i containing x but missing y.

Add y in row i, then delete x. The row floor is retained by add-before-delete and its size returns to a_i. After addition degree(y)<=D, and all other degrees are still at most M. After deletion max degree remains at most M, and Phi decreases by one; no recipient excess is created.

Check EVERY forbidden palette set K of at most q-2 labels. If y is not in K, its hitting status is unchanged by adding y, so an old ACTUAL missed root remains. If y is in K, the number of roots it meets after addition is at most

D+(q-3)M < r.

Hence it still misses at least one ACTUAL root; choose the first missed root for a supplied witness. This also handles smaller sets containing y and q=3. Empty sets miss every nonempty root. The subsequent deletion cannot lower transversal. Thus every primitive retains tau>=q-1.

The argument uses the SAME actual column incidences, not independent capacities. It supplies the next donor, recipient and row whenever Phi>0. Phi is a finite nonnegative integer and strictly decreases at completed transfers, so the process reaches degree at most D. It may remain at tau=q-1 or rise above q; exact entry is NOT asserted. This proves X15L.

## 6. Complete composition and upper removal

For X15N, compact original exact-q endpoints A,C legally to their floor sizes and maximum degree at most M. Apply X15L separately to obtain lower-guard tuples A',C' of maximum degree at most D. These tuples need not be exact q. Save every actual leveling edit and its reverse.

If S<Dk, connect A',C' using X15S. Since M>=D,

r>=D+(q-3)M+1 >= (q-2)D+1.

Throughout that connection, every set of at most q-2 labels meets at most (q-2)D<r actual roots. Thus it retains the lower guard even though its endpoints can be inexact.

If S=Dk, all degree-bounded columns at A',C' have degree EXACTLY D. Use X14's actual cycle construction on their balanced pending graph: one column is temporarily degree D+1 and the hole travels backward until saturation is restored. Its primitive eligibility and renewed cycle existence use only compact row sizes/degree balance, not exact q. The additional inequality r>=(q-2)D+2 supplies every lower witness throughout. Do not invoke X14's exact-endpoint upper-conversion conclusion at the inexact A',C'; use ONLY its proved LOWER primitive cycle schedule.

Now concatenate original source exact compaction, source leveling, the degree-class connection, reversed destination leveling and reversed original destination exact compaction. Every piece has floors and tau>=q-1. Every join is its ACTUAL saved tuple. The FULL original endpoints, not the internal A',C', have exact q.

This is a finite native LOWER path. All roots stay nonempty, so its upper bound is finite, at most r. Apply accepted maximum-layer Theorem A to this full path between the ORIGINAL exact-q endpoints. It produces a path with tau in {q-1,q} and the same original labelled endpoints. No upper conversion is applied prematurely to a level-(q-1) entry.

The final path may contain temporary/repeated incidences and may change the preliminary schedule. Every original destination support is restored. Renewal is availability of the next macro after buffer restoration or degree reduction, not exact-q resetting after each macro. The supplied complete result can be reused for any finite chain of exact endpoints satisfying the hypotheses.

No original-floor permutation is used, so arbitrary positive floors are valid within X15N's explicit sufficient class; unrestricted mixed-floor connectivity is not inferred.

## 7. The nine-label completion follows from a general mechanism

For k9, uniform original floor3 and exact target4, Section 2 gives max label degree M=r-4 at each original endpoint and every exact compaction. Take D=3 and S=3r.

| Root count | M | S | Capacity Dk | Leveling requirement r>=D+M+1 | Degree-class handover |
| --- | --- | --- | --- | --- | --- |
| 7 | 3 | 21 | 27 | 7>=7 | Strict slack, X15S; every pair hits at most6<7 roots |
| 8 | 4 | 24 | 27 | 8>=8 | Level to3, then strict-slack X15S |
| 9 | 5 | 27 | 27 | 9>=9 | Level to3, then saturated X14 lower cycles; pair hits at most7<9 roots |

Every stated hypothesis is supplied. At r7 no degree-leveling edit is needed because M=D. At r8/r9 a donor degree>3 implies an actual recipient degree<3 even in the saturated case, and a root containing the donor but missing the recipient exists by their degree inequality.

The recipient's new degree is at most3. At r8, every pair containing it hits at most3+4=7<8 roots; at r9 it hits at most3+5=8<9. Other pairs retain their ACTUAL previous missed roots during the addition. Deletion cannot weaken protection. Once degrees are at most3, strict or saturated renewed incidence schedules supply completion as shown in the table.

There is no assumed feasibility classification, simulated state list or frozen-background reachability search. For every exact endpoint that exists, the general construction connects it to its original exact destination. This proves complete repair at ALL three remaining nine-label root counts without treating them as separate campaigns.

## 8. Whole-domain uniform-floor-three target-four conclusion

Here are all carrier branches, with inherited hypothesis domains explicit. A finite palette with floor three requires k>=3; exact four also requires r>=4.

- k<=5: any k-2 labels hit every root of size at least3, so tau<=k-2<=3. Exact four is infeasible.
- k6: for EVERY three-label set K, exact four supplies an ACTUAL root disjoint from it. The complement has size3, so that root equals P minus K. All twenty distinct triples occur, forcing r>=20. X12's actual-guard composition applies: the ten triples on any fixed five-label subset are an actual three-guard; source and destination each have such a guard, and r>=20 exceeds the one-overlap budget10+10-1. Uniform full exact endpoint permutation M, O1 and A plus reversed exact compaction restore every original destination. X12 checks this branch without a classical equality theorem.
- k7: X12 proves all feasible carriers. At r4 protected J applies because exact4 on four roots forces them pairwise disjoint; r5 inherited F applies for every positive floor profile. At r6..9, actual incidence guards have N=floor(4r/7)=3,4,4,5 and r>=2N-1, supplying full O1/M/A composition. At r>=10 accepted X12U applies. Feasibility of each tuple is not assumed.
- k8: accepted X14E proves every feasible carrier; exact4 is infeasible below r8, saturated renewal covers r8, and X12D covers r>=9.
- k9: r<4 is infeasible; r4 protected J and r5 F cover any feasible endpoints. At r6 X13 proves infeasibility. Section7 supplies every r7..9. At r>=10 X12U applies.
- k>=10: accepted X12W supplies all r>=6 with h3; r4 is protected J and r5 is F; r<4 is infeasible.

These branches exhaust EVERY finite ordered palette and root count with possible exact-four original-floor-three endpoints. Each positive branch yields the SAME original labelled destination and the native band {3,4}. Hence X15U is universal for this declared root problem.

Frozen dependencies at baseline466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f include GENERAL_PARENT_CONNECTIVITY A/F and exact compaction, PROTECTED_EXCHANGE J, OVERLAPPING_CLIQUE_EXCHANGE M and PALETTE_SLACK_CONNECTIVITY AE as used inside accepted X12. Actual O1 is in GUARD_HANDOVER.md. Accepted X12, X13 and X14 sources remain unchanged. The only saturated dependency used at inexact entries is X14's explicit LOWER cycle construction; exact endpoint conclusions are withheld there.

## 9. Discovery and precise remaining obligations

The complete renewal explanation now has both forms:
- spare capacity can be accessed even when the spare label occupies every cycle row, by an actual OUTSIDE row buffer that is restored;
- saturation is repaired by a single temporary overfull label and travelling hole;
- when endpoint degrees are too large for those certificates, ACTUAL low-degree recipients reduce excess while preserving all old and new forbidden-cover witnesses.

The first two restore a reusable structure; the third guarantees finite access to it. Their composition supplies complete exact repair, not merely a safe local move or a repeatable supplied sequence without availability.

X5's conditional triple-anchor assumptions are no longer needed for UNIVERSAL uniform-original-floor-three target-four native root repair. No universal X5 qualification/reachability is inferred; a replacement construction proves connectivity even where that entry class is empty.

Original A11 stricter destination-directed scheduling remains OPEN. Temporary buffers can displace correct compact incidences before restoring them, and maximum-layer conversion can alter the schedule. General mixed-floor target-four, higher original floors/targets outside the proved classes and unrestricted nested universality also remain OPEN. Conditional native child lifting uses the baseline six-clause interfaces and fixed-root clearance; a root theorem alone does not certify those interfaces for every possible subtree.

No physical energy/metric/gravity/fundamental time or originality claim. The result is ordered repair with retained recoverability and a root-level upper bound of one defect unit.

No numerical enumeration, scientific execution/test/workflow/run ID, implementation, benchmark, numbered v16.55 certification or integration merge. Certified v16.54 and separate accepted efficiency design remain unchanged; runner implementation and measured speedup remain unstarted. Any implementation certification remains subject to the scientific closure requirements.
