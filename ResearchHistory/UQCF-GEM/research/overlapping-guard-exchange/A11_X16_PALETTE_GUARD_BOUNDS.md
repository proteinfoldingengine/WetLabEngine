# A11.X16 — palette-aware actual guard requirements and mixed-floor repair budgets

Scope:29e5479f683209b92776ab86824d2e974a29ad7b.
Parent publication:a7cd10fe8b471d246ec23be4898f732e8798e9b9.
Certified baseline:466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Frozen candidate for fresh independent WHOLE-ARGUMENT review. Analytical only.

## 1. New structural bound and complete-repair criterion

A fixed finite ordered palette has k labels and r existing labelled slots, with original floors a_i>=h>=1, a_i<=k. Endpoints have EXACT transversal four. All primitive edits change ONE incidence in ONE root, preserving its original floor; temporary larger supports and repeated edits remain native.

For integers0<=t<=b<=v define

L(v,b,0)=1,
L(v,b,t)=ceil((v/b)*L(v-1,b-1,t-1)) for t>=1.

**Lemma X16C (actual complementary-cover requirement).** A family of ACTUAL blocks, each of size at most b, covering every t-subset of a v-label palette has at least L(v,b,t) blocks, counted by their actual labelled slots. Duplicated blocks do not invalidate this necessary bound. If b<t<=v, such a cover is impossible.

Consequently an exact-four endpoint with all floors>=h requires k>=h+3 and

r>=L(k,k-h,3).

**Lemma X16G (palette-aware minimum actual guard size).** At an exact-four endpoint, every label-avoiding family is an actual three-guard on k-1 labels with all floors>=h. Therefore it has at least

g_C=L(k-1,k-1-h,2)

actual roots. Any proved stronger lower bound can be used in its place. In particular combine g_C with X14's structural bounds:
- if k-1<3h, use at least4 roots;
- if k-1<ceil(5h/2), use at least5 roots.

Let g be the maximum of these furnished bounds. Every exact endpoint label degree is at most M=r-g. This is a MINIMUM guard cardinality/maximum degree bound; it is not X9's maximum selected-guard size or a free buffer certificate.

**Theorem X16R (complete repair from actual guard requirements).** Let S=sum_i a_i and g be ANY rigorously supplied lower bound on the number of roots in every label-avoiding three-guard for this carrier. Every exact-four endpoint pair has complete native repair with tau in {3,4} and exact original labelled/noncompact destination restoration in any of these cases:

(A) r<=2g-2;
(B) r=2g-1 and S<(g-1)k;
(C) r>=2g and S<=(g-1)k.

Exact endpoint feasibility guarantees r-g>=1. Cases lacking feasible endpoints are vacuous and are not called disconnection. The original floors may be unequal; no slot permutation is used in this theorem.

The new general covering-density proof derives actual input protection unavailable from a palette-free bound alone. X16R is a transparent consequence of those bounds and accepted X14/X15 renewal, not a newly claimed independent handover mechanism.

## 2. Actual cover counting proof

Prove X16C by induction on t. For t=0, the empty set must be contained in an actual block, so at least one block is required.

For t>=1 fix a label x. All ACTUAL blocks containing x, after deleting x, cover every (t-1)-subset of the other v-1 labels: each such subset together with x is one of the t-sets that the original family covers. These shortened blocks have size at most b-1. The induction hypothesis therefore requires at least L(v-1,b-1,t-1) blocks containing EACH label x.

Sum those actual incidences over all v labels. The actual number n of blocks contributes at most nb incidences, while the requirement is at least v*L(v-1,b-1,t-1). Hence

n>=ceil((v/b)*L(v-1,b-1,t-1)).

The proof uses the SAME labelled blocks across overlapping label obligations. No independent capacities are assigned to those obligations. The incidence sum counts sharing rigorously rather than treating witnesses as distinct invented roots.

For b<t a block cannot contain any t-set; since t<=v a t-set exists, so coverage is impossible. Recurrence is used only for0<=t<=b<=v. This is an elementary necessary covering-density bound, not an originality claim or an external covering-design classification. It does NOT prove a cover attaining L exists.

For roots A_i, complement B_i=P minus A_i has size at most k-h. Tau>=4 means EVERY three-set lies in at least one ACTUAL B_i. If k-h<3, tau<=k-h+1<=3; exact four is impossible. Otherwise X16C applies at(v,b,t)=(k,k-h,3), proving the endpoint count.

## 3. Palette-aware actual avoiding family

At exact four, fix x and select ALL actual roots missing x. A cover of them with at most two labels, together with x, would hit the entire tuple with at most three labels. Thus their transversal is at least three. Their supports lie in P minus {x} and retain their original floors>=h.

On the v=k-1 remaining labels, their relative complementary blocks have size at most b=k-1-h and cover every PAIR. Since exact four requires k>=h+3, b>=2 and X16C applies. They number at least g_C, not independent counts for each pair. Therefore degree(x)<=r-g_C.

X14's minimum three/four-root guard palette bounds apply to the SAME actual family: three roots requiring three labels need3h labels; four such roots needceil(5h/2). Combining these proved lower requirements yields g and degree<=r-g. Larger supports and unequal floors only make their complementary capacities smaller; replacing their individual capacities by b is a valid relaxation for a lower bound.

Exact compaction to ORIGINAL floors retains a supplied minimum four-cover, by deleting excess incidences while saving the reverse. Deletion cannot lower tau and the cover remains, so all compaction primitives are exact four. It cannot increase any degree, so every compact endpoint has max degree at most M=r-g and row sizes a_i. Every original labelled slot keeps its own floor.

The endpoint degree statement is not reused as an exactness implication at arbitrary deficient prefixes. During repair, the explicit X14/X15 actual witness arguments supply the lower guard instead.

## 4. Proof of complete repair criterion

At a feasible exact endpoint some label occurs in a nonempty root, so r-g>=1. Put M=r-g.

**Case A:** choose D=M. Then

r>=2M+2 iff r<=2g-2.

Accepted X14C applies at q4 to the degree-bounded exact compactions, with arbitrary positive original floors. Its actual pending cycles retain at most one temporarily degree D+1 column. Every pair meets at most2D+1<r actual roots, giving a missed-root witness. Eligible greedy/cycle moves, repeated row colours, original floors and renewed cycles are proved in the inherited source. Maximum-layer conversion and reversed exact compaction restore the original labelled destination. No total slack condition is needed.

**Case B:** M=g-1, r=2M+1, and S<Mk. Use X15N with D=M. The leveling condition r>=D+M+1 is equality and no above-D degree exists initially. X15's strict-slack incidence schedule stays at degree<=D throughout. Every pair hits at most2D<r roots. Borrowed cycle-row or outside-row buffer incidences are restored; the balance identity supplies the next greedy move or cycle until the pending macro count reaches zero. Since this is strict slack, no extra saturated inequality is required.

**Case C:** set D=g-1. Then r>=2g implies M=r-g>=g>D. The assumed S<=Dk and

D+M+1=(g-1)+(r-g)+1=r

supply X15N's protected leveling hypotheses. In saturation its additional r>=2D+2 is exactly r>=2g. Thus X15N applies in both slack and saturation.

For completeness, leveling an above-D donor x uses a below-D recipient y supplied by S<=Dk. Their degree inequality gives an ACTUAL row containing x but missing y. Add y then delete x, keeping that original floor. Every pair containing y hits at mostD+M<r roots; other pairs retain old actual witnesses, and deletion cannot lower transversal. Excess-degree potential strictly decreases, providing finite access to the renewable class even if the arrival has tau3.

Once in that class, strict slack uses an existing spare label. If all cycle rows contain it, a full cycle column supplies an actual OUTSIDE row missing it; buffer that incidence, rotate the cycle, restore the buffer. Saturation uses one overfull column and a travelling hole. Every forbidden pair misses an actual root at every primitive, and completed macros restore the reusable balance/degree structure. Pending differences strictly decrease at completed repair macros; borrowed correct incidences are restored and not falsely counted as per-primitive progress.

The full original source-to-destination LOWER path includes saved exact compaction, protected source leveling, the degree-class connection, reversed actual destination leveling and reversed destination compaction. Internal entries need not be exact four. Only the COMPLETE lower path between original exact-four endpoints is passed to maximum-layer Theorem A, producing the native band{3,4} and the same full original labelled destination.

These arguments are inherited X14/X15 within explicitly supplied domains. Floors are never weakened or reassigned; arbitrary mixed-floor permutations are not used. Failure of cases A/B/C is failure of a sufficient criterion, not native disconnection or an absent repair path.

## 5. Concrete strengthening at floor four

These examples are consequences of general guard requirements and renewal, not separate numerical campaigns.

### Nine labels

For h4,k9:

g_C=L(8,4,2)=ceil((8/4)*ceil(7/3))=6.

This improves X14's palette-structure-only lower bound of five avoiding roots. Exact endpoint feasibility also requires

r>=L(9,5,3)=ceil((9/5)*6)=11.

At r11, M=5 and S=44 for uniform floor4. Since r=2g-1=11 and44<5*9=45, case B connects EVERY exact-four endpoint pair on that carrier with complete original destination restoration.

This statement is CONDITIONAL on exact endpoints existing. The covering lower bound does not establish existence at r11, and no feasibility classification or disconnection is claimed. Its actual strengthened degree cap supplies access to a renewal class where the previous five-root bound did not.

### Ten labels: complete feasible uniform-floor-four class

For h4,k10, the basic cover requirement is g_C=L(9,5,2)=ceil((9/5)*ceil(8/4))=4. However an actual avoiding family lives on nine labels, fewer thanceil(5*4/2)=10 needed by a four-root three-guard. X14G therefore gives g=5.

The compact uniform incidence inequality4r<=10(r-5) excludes every r<=8; r<4 is already impossible. At r9, M4 and S36<4*10=40, so case B supplies complete repair for every exact-four pair that exists.

At r10, S40=4*10, r=2g and case C gives complete saturated repair. An exact-four feasibility control DOES exist here: all five4-subsets of one five-label core and all five4-subsets of a disjoint five-label core. Each core has transversal2, their disjoint union has exact4, and two labels from each supply a minimum four-cover. Every support has its original floor4. Duplicate padding proves feasibility for every r>=10.

For r>=11, accepted X12D applies with h4,k10,r>=10 and ceil(4r/10)>=5. Its exact two-core hub has six-root three-guard; actual incidence supplies the required outside slots, and its full original labelled restoration is inherited.

Hence EVERY exact-four pair on EVERY feasible ten-label, uniform-original-floor-four carrier has complete native{3,4} repair. This is universal CONNECTIVITY within this declared palette/floor class. Feasibility at r9 is NOT decided; below9 it is excluded, and at every r>=10 it is constructed.

## 6. Explicit nonuniform-floor feasible class

For h3,k9, X16C gives g_C=L(8,5,2)=ceil((8/5)*ceil(7/4))=4, matching the previously used minimum-guard deduction. At r8, case C applies to EVERY original floor profile with all a_i>=3 and

S=sum a_i<=27.

This includes genuine nonuniform floors, for example(4,3,3,3,3,3,3,3), S25. This is an explicit derived COROLLARY of accepted X15 mechanism with actual input availability; it is not presented as a new independent renewal construction.

Feasibility is supplied: on labels1..9 put
2349,134,124,123,678,578,568,567
in the eight labelled slots, with the first slot floor4 and the others floor3. The first four roots require two labels: the last three share label1, but the first misses1, and{1,2} hits all four. The last four are all triples on{5,6,7,8} and require two labels. These palettes{1,2,3,4,9} and{5,6,7,8} are disjoint, so the full tuple has EXACT transversal4, with minimum cover{1,2,5,6}.

The theorem connects arbitrary exact-four endpoints on that SAME profile, not merely endpoints sharing the displayed core shape. No floor-four root is compacted below its original floor. For the whole S<=27 profile class, existence of every individual profile is not asserted; the theorem is for all exact endpoints that exist.

## 7. Scientific contribution, classification and boundaries

The new bound tracks actual overlapping cover obligations inside each avoiding-root family. It improves guard requirements through palette capacity, yielding smaller ACTUAL endpoint degree bounds, which in turn furnish native access to renewable degree classes. Necessary cover counts do not replace actual lower witnesses on the path: X14/X15 provide those witnesses, next moves, progress and exact restoration.

The covering-density argument is elementary and is not claimed original. No external design theorem or catalogue is used. The explicit corollaries transparently compose accepted renewal results; no passing count, implementation or new handover is invented.

X15's universal uniform-floor-three target-four ROOT theorem remains complete and unchanged. X16 extends derived protection and declares additional mixed-floor/higher-floor classes. Universal all-mixed-floor target-four connectivity, all-uniform-floor-four palettes, higher targets and unrestricted nested universality remain OPEN. Original A11 destination-directed universality also remains OPEN: buffers may displace correct incidences before restoration and upper conversion can change the schedule.

Root results lift only through the inherited exact-child interfaces/fixed-root clearance; no unconditional nested theorem or negative barrier follows. Unit repair is an upper bound, not a positive minimum defect for every pair. No physical metric/gravity/energy, fundamental time or originality claim.

Sources: X14G/X14C at826b0f961a76d0f77871ca65d5c581212a5dcd6a; X15S/L/N at parenta7cd10fe8b471d246ec23be4898f732e8798e9b9; X12D at1216c1007b0a91cf5e6c0a1c14d813a81dcc23b9; exact compaction/maximum-layer A at baseline466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f. Frozen sources are unchanged and domains checked, not recertified.

Analytical only. No numerical enumeration, scientific test/workflow/run ID, implementation, benchmark, numbered v16.55 certification or integration merge. Separate accepted efficiency design and certified v16.54 remain unchanged.
