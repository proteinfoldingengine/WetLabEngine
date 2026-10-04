# Independent whole-argument analytical review — A11.X40

**Verdict: ACCEPTED — X40W, X40L, X40B, X40U and X40F at exact candidate `79701f3a9ea5826a79b2fa83525d99cf01d7f4d6`, within their declared sufficient domains. No required mathematical or interpretive revision.**

Reviewer: independent Codex agent `/root/x40_whole_argument_review`, specifically dispatched for this whole-argument review. Date: 2026-10-04 UTC. The reviewer did not author or edit the candidate and did not delegate. This is attributable analytical review, not human peer review, numerical verification, implementation certification or recertification of inherited sources.

## Exact sources and boundary

Repository: `proteinfoldingengine/WetLabEngine`. Sources were fetched read-only through the GitHub connector at immutable refs. No checkout, GitHub write, scientific execution, test, enumeration, benchmark, workflow, integration merge or numbered certification was performed. Source-directory/tree metadata retrieval was only file discovery, not scientific enumeration. This local review document is the sole deliverable write.

Candidate tree `66eeab1fd4e3fb705ae8dd60906737848f9de5a0` has direct parent scope `94b2d3b689a9dd5a717608ba0579518fab9542a0`, tree `0ee155c30ccdac2f126fbd06d137b16d6d4beb04`. Scope has direct parent `2aa4fd886229dfe175c61789abf0135fc687c748`. Commit metadata reports only the X40 proof added by the candidate and only the scope added by the scope commit. The scope blob matches at scope and candidate. This verifies retrieved provenance, not a whole-repository audit.

Paths in this table are relative to `ResearchHistory/UQCF-GEM/`.

| Source assessed | Immutable ref | Blob |
|---|---|---|
| `AGENTS.md` | X40 candidate | `e5407215a81b914fc02f5c107333a2f0261634ee` |
| `research/overlapping-guard-exchange/A11_X40_SCOPE.md` | scope and candidate | `9a141c408d821171368d490dfc0fccdd0d96ab51` |
| `research/overlapping-guard-exchange/A11_X40_SPARSE_WITNESS_RENEWAL.md` | X40 candidate | `c3de07704e3c3faa9b77ab72df1d8445bf41094c` |
| `research/overlapping-guard-exchange/A11_X34_COUPLED_WITNESS_HANDOVER.md` | analytical parent | `b9b4fde21b3b830f99e158ad909d2ac440d8e469` |
| `research/overlapping-guard-exchange/INDEPENDENT_A11_X34_WHOLE_REVIEW.md` | analytical parent | `6484102daf950dd3207412285339e8bc47d515bc` |
| `research/overlapping-guard-exchange/A11_X39_DENSE_MASK_CYCLE_RENEWAL.md` | analytical parent | `c822f57babdcd2782ed8259f740d839c864e6f2b` |
| `research/overlapping-guard-exchange/INDEPENDENT_A11_X39_WHOLE_REVIEW.md` | analytical parent | `5ea754aa34a60f4d752c787b20656b6ac7200fc7` |
| `research/overlapping-guard-exchange/A11_X38_TRIANGLE_CYCLE_RENEWAL.md` | analytical parent | `abb8304dd3c76356ada9ab5d92b2aae516bdc5a3` |
| `research/overlapping-guard-exchange/A11_X37_SHARED_ROLE_CYCLE_RENEWAL.md` | analytical parent | `f057022ba890a74a37c30b4983a1be9000f8914a` |
| `demos/v16.54-parent-support-connectivity/GENERAL_PARENT_CONNECTIVITY.md` | certified `466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f` | `922ae44713c6810c5a99716c52ecb37738a880a6` |
| `demos/v16.54-parent-support-connectivity/OVERLAPPING_CLIQUE_EXCHANGE.md` | same certified ref | `865f0797892a2e5e869ec2180d3c842026889445` |

The governing UQCF-GEM AGENTS was read. Root and intermediate/deeper AGENTS fetches returned not found. Its numbered-stage scientific closure requirements do not turn this explicitly analytical checkpoint into an execution or certification. The scope honestly discloses already-known reasoning before freezing. v16.55/v16.54 evidence and implementations are neither changed nor recertified here.

## X40W: exact consistency and actual witnesses

With nonempty partition groups, any actual label cover induces an owner-index cover of the masks. Conversely representatives of a minimum template cover give a label cover. Thus template transversal four is equivalent to exact-four at every restored partition, and the supplied H genuinely yields four distinct actual representatives.

For a two-index set S, no avoiding root would make S itself a template cover. Exactly one avoiding original slot i would allow one index from its nonempty Q_i to be added to S, forming a cover of size at most three. Both contradict exact four. Hence rho is at least two. Duplicate masks count as separate actual original labelled slots, as required by the ordering theorem; no roots are introduced by repair.

Every footprint of at most three indices is avoided by an actual mask, or would itself cover the template. This statement needs neither a mask equal to the footprint complement nor a lower width premise. The candidate correctly distinguishes actual avoidance from X39's stronger dense co-triple rigidity.

## X40L: exhaustive cycle accounting and compatible conditional order

At each structural boundary, equal current and destination group sizes imply equal incoming/outgoing misplaced-label multiplicities after cancelling correct labels. A nonempty finite balanced loop-free directed graph supplies a simple cycle: after entering a vertex one cannot stop, and repetition yields a cycle. Fixed finite orders make the cycle and arc-label choices deterministic. No short-cycle decomposition is assumed.

The permutation orientation is correct. For x_t initially in i_t and destined for i_(t+1), sigma(x_t)=x_(t-1) gives sigma-inverse(x_t)=x_(t+1), initially in i_(t+1). Therefore the next partition places every selected label at its final owner, exchanges one label in and out of each involved group and restores every b_j and N_i.

An ordinary label has one fixed owner; a selected label has expanded union footprint {i_t,i_(t+1)}. Two ordinary labels, ordinary/selected pairs and adjacent selected-edge pairs use at most three indices. The consistency argument supplies an actual root whose entire old/new union misses each such pair. This includes ordinary labels outside the cycle and all partial supports in changing roots.

Only selected labels on disjoint cycle edges can lack a common witness. For l at least four, exactly l unordered edge pairs are adjacent, leaving binomial(l,2)-l=l(l-3)/2 possible conflicts. Some sparse masks can still supply common witnesses, so the claim is an upper bound, correctly unlike X39's exact noncommon count. Length two and three have no conflict pairs. Each noncommon pair has two distinct old owners and two distinct new owners; its endpoint witness sets each contain at least rho actual roots. If there is no common witness these sets are disjoint, exactly as required by X34.

Coordinate monotonicity of binomial(u+v,u) for u,v at least rho bounds each bad-order fraction by 1/binomial(2rho,rho). The conflict bound is at most m(m-3)/2, so the strict hypothesis yields Psi_cycle less than one. This is a mean number of actual bad events. Linearity uses no independence; all pairs use the same original labelled root identities, so shared resources are handled jointly.

The inherited conditional formula is appropriate and exact. With no new witness completed, the remaining u' old and v new witnesses contribute 1/binomial(u'+v,u'). Once a new witness completes, the bad event is impossible if an old witness remains or occurred after the first new witness; otherwise it is certain. Common-witness pairs contribute zero. Full extensions split into equally sized classes according to their next root. Their average is Psi(D), so a least next index with nonincreasing conditional count exists whenever roots remain. The count stays below one; at a full order it is an integer and hence zero. Availability is derived, not inferred merely from safe moves or an assumed decreasing potential.

For each scheduled root, exactly the absent destination-only incidences are added before exactly the present source-only incidences are deleted. Expansion contains the old endpoint and contraction contains the next endpoint, each of cardinality N_i. Every intermediate support therefore respects the SAME original positive floor a_i, even at saturation. A nominal replacement already present via another included role is correctly omitted; contraction still contains the entire destination support.

For common witnesses the whole union misses the pair. For disjoint witnesses the derived first(V)<last(U) order leaves an untouched old witness through the first new witness's active edits, then a completed new witness afterward. This covers every individual primitive. Equal roots need no no-op; finite incidence lists and finite remaining-root count supply next-edit existence and termination. The continuation theorem concerns these certified generated prefixes, not arbitrary safe histories.

## Renewal, strict progress and complete event minimum

Every completed cycle restores the same partition sizes, actual root cardinalities, masks, exact transversal, H and rho. No protecting reserve is consumed. Removing one incoming and outgoing arc at each involved index preserves balance. Any nonempty residual graph again has a simple cycle of length at most m, and the same strict count bounds every such next cycle.

Selected labels become correct, no correct label is moved, and the nonnegative incorrect-owner count decreases by l. Each handover is finite, so repetition terminates at the exact D_j and every FULL original labelled C_i. Physically silent group changes can be omitted as native moves while bookkeeping still decreases this measure.

A label remains at its original owner until its one resolving cycle, then moves directly to its final owner. Masks containing both owners retain its common incidence, masks containing neither remain absent, and masks containing exactly one toggle precisely its original differing incidence once. Other cycles do not touch it. Thus the preliminary lower path has exactly sum_i |A_i symmetric_difference C_i| edits, the unavoidable endpoint toggle minimum. For a finite chain this count is per leg; it is not global event uniqueness across a chain returning to previous states.

## X40B and X40U: separate upper mechanisms

X40B correctly first obtains the COMPLETE finite lower path with original exact-four endpoints. Certified theorem A then applies with q=4 and lower level three in the same fixed palette/slots and positive-floor carrier, whose arbitrary allowed additions and unions match its hypotheses. It guarantees exact outer endpoints and tau in {3,4}. It does not guarantee the preliminary schedule, count, event uniqueness or internal waypoint preservation. The candidate explicitly withdraws all those guarantees after conversion, including for a full concatenation.

X40U is separately direct. A simple cycle selects at most one label from each group. For each j in the supplied four-index minimum cover H, b_j at least two guarantees an unselected current label. Four such labels are distinct, unchanged and have owner set H at both endpoints. They hit every old and next root. Active expansions contain the old root; contractions contain the next root; other roots are old or completed new. The SAME four actual labels therefore hit every partial tuple. Combined with the lower pair witnesses this proves 3<=tau<=4 directly, retaining the preliminary minimum count.

Restored group sizes renew this representative choice before every next cycle. These are existing labels serving an upper cover, not new palette ingredients, spare root-floor support or independent lower capacities. Every actual root can remain saturated. The cover-size condition is sufficient, not necessary, and the candidate does not incorrectly impose it on X40L/B or on X39's different cover construction.

## X40F: automatic small-role class and sparse infinite control

For m=4 and 5, rho>=2 gives binomial(2rho,rho)>=6 while m(m-3)/2 is two and five respectively. The criterion is automatically strict for EVERY supplied actual transversal-four template on those roles. X40L/B follow without density or root reserve. X40U additionally needs its stated multiplicities in H. This is a structural result, not a finite numerical campaign.

For the sparse constructor, the singleton {1} forces role one into every cover. Among the remaining m-1 roles, all complements of pairs have transversal three: each two-set is missed by its matching complement, while every three-set intersects each high mask. The total template therefore has exact transversal four with H={1,2,3,4}. All high masks are nonempty for m>=5, and all original duplicate slots are declared before repair.

For S={1,u}, exactly d(m-2) high copies avoid it. For S={u,v} outside one, the singleton and d matching high copies give d+1 avoiding slots. Since d(m-2)>=d+1 for m>=5,d>=1, actual rho is exactly d+1. Taking d=m-3 gives rho=m-2. The central-binomial induction inherited from X39 is valid: for n=m-2>=2, B_2=6>2=R_2, B_(n+1)/B_n>3, and 3R_n-R_(n+1)=n^2-3>0. Hence the strict criterion holds for all m>=5. At m=5,d=1 the automatic small-role argument already suffices.

Every excluded triple J outside role one has complement containing one and at least one other role. No actual mask equals that complement: only the singleton contains one. Thus ALL such complementary-triple masks are genuinely absent. The singleton nevertheless avoids every such J. Its width one is smaller than m-3; X39's dense-width premise is genuinely violated, while the actual redundancy and shared witness argument replace it.

The diagonal and forward-cycle t-label cells are disjoint existing labels. Rows and columns both have group size 2t and palette size 2mt. The singleton floor is 2t; each high floor is 2t(m-3), both saturated and unequal. H's group multiplicities are at least two, so X40U applies directly.

There is only one low-floor slot. Any four distinct slots have total floors at least 2t+3*2t(m-3)=2t(3m-8)>2tm for m>4. Thus four pairwise-disjoint floor-safe supports cannot fit ANYWHERE on this carrier. This is a private-root mechanism obstruction, not native disconnection.

The misplaced graph is t parallel copies of a directed m-cycle and has no shorter simple ownership cycle. Every actual mask is nonempty and proper, hence has an entering and leaving edge in that connected cycle. Every original root changes, and multigroup saturated roots lack X37's required original reserve. X38's stated short-cycle graph condition is unavailable; no failure of all alternative schedules follows.

Selected labels on 1->2 and 3->4 two-cover the full cycle union: the former hits the low root via role one; the two labels together expose rest roles two, three and four, and a high complement can exclude only two of those. The same pair hits the full original endpoint union. Therefore whole-union preparation is unsafe. A three-guard formed from subfamilies of those actual full unions is excluded; contracted auxiliary guards and every possible whole-original-root order are not excluded. The candidate correctly makes only the limited claim.

At t>=2 after the first completed cycle, every proper mask has lost a selected source-only crossing label and gained a selected destination-only crossing label, so differs from A_i. An unselected copy remains on each crossing edge; a remaining source-only incidence still present is absent from C_i, so each root also differs from C_i. ALL original roots are therefore unfinished relative to BOTH original endpoints while every group/root size and rho are restored. Residual ownership is exactly t-1 parallel copies of the same long cycle. Renewed handovers complete exactly t cycles and restore exact labelled C. This is a symbolic unbounded constructor, not sampled evidence.

## Advance, limits and publication obligation

Equal corresponding group sizes permit a palette bijection B_j->D_j; certified L already supplies native symmetry connectivity at the same original floors. X40 therefore proves a new sufficient renewable event-unique scheduling interface beyond X39's dense pattern, not a new connectivity classification. X34's exact bad-event counting and conditional averaging and X39's cycle-local accounting/induction are openly inherited. A is used only for X40B after lower completion; X40U is proved independently.

The supplied actual template, equal nonempty corresponding cardinalities, original positive floors, strict redundancy margin, and X40U's cover multiplicities remain explicit inputs. A failed count or failed multiplicity condition is not a no-path certificate. Arbitrary template accessibility, unequal group sizes, arbitrary safe-prefix extension, below-bound sparse templates, scarce upper representatives and unrestricted mixed/directed/higher-target/nested universality remain unresolved. No literature-originality, runtime/efficiency, physical energy/metric/gravity or fundamental-time conclusion follows. Earlier X37/X38/X39 domains remain intact.

This acceptance attaches only to the exact candidate and scoped analytical claims. The reconciled reporting packet must receive a separate exact publication review, followed by immutable readback. Those publication obligations are not completed by this whole-argument review.

**Final whole-argument verdict: ACCEPTED in the declared domains; no required changes.**
