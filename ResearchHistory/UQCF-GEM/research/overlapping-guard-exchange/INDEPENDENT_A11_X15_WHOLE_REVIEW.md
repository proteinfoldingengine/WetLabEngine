# Independent whole-argument review — A11.X15

Verdict: ACCEPT. No mathematical revisions requested.
Reviewer: independent agent /root/x15_whole_argument_review.
Repository:proteinfoldingengine/WetLabEngine.
Candidate:fdfcc64ae0f828d9dcedc2cc41d2bc2a63868e5d.

| Reviewed source | Git blob | SHA256 |
| --- | --- | --- |
| A11_X15_UNIVERSAL_FLOOR_THREE_REPAIR.md | 1a512e7193b082f3e50d8fc2d0d555489416f6be | 6907acf000829479ec99fefb43392a36ca7d396665f94e3655493bfd858a22f1 |
| A11_REPAIR_CONSOLIDATION.md | 645b7af716acb9b15c36aff77b1f24d61a88d263 | 2fd3615ef1d644a6779c9210595aaa1ea81fa85a93995ca2f68abfe2077fa542 |
| A11_X15_SCOPE.md | 0bae2316fa397ff1bdfba117d95b8c47bbc97a4d | Scope commit below |

Scope:bdc8be5e3bcd633de8265c93f44b4b8d5733ab62.

## Actual attributable review

The following preserves the independent reviewer's mathematical report and decision; identifier/math formatting is normalized and publication hashes are supplied above.

The scope openly discloses preliminary reasoning developed before analytical freezing and does not misrepresent this as prospective numerical preregistration.

I read the actual complete proof and consolidation, the X12/X13/X14 mathematical sources and their actual independent reviews, the explicit X11 thirteen-root constructor, actual O1 source, applicable AGENTS.md, and the relevant frozen baseline sources at466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f: maximum-layer removal and five-root repair, full endpoint permutations, palette-room connectivity, protected exchange, and conditional child interfaces.

### Strict-slack incidence repair

Lemma X15S is correct.

At a completed macro boundary, equal current and destination row sizes give actual surplus/deficit pairings. Their directed graph satisfies out(v)-in(v)=degree_current(v)-degree_destination(v). A pending edge ending at an underfull column supplies the stated add-before-delete transfer.

If no greedy move exists, every pending destination is full. The balance identity and destination degree bound guarantee an outgoing edge at every reached full label, hence an eligible directed cycle. Extracting a simple cycle ensures distinct label vertices. The strict inequality S<Dk supplies an underfull existing palette label outside that cycle at every completed boundary.

Both buffer cases are valid:

- Cycle-row buffer: when the spare label misses a cycle row, temporarily replacing that row's cycle-source incidence opens the hole needed for reverse cycle rotation. The final buffered transfer installs its pending destination and removes only the temporary incidence.
- Outside-row buffer: when every cycle row contains the spare label, the spare column has fewer than D incident rows, whereas a full cycle column has D. An actual row containing that cycle label but missing the spare label therefore exists. It is outside the cycle's row colours. Borrowing its incidence opens a hole, processing all cycle edges restores the hole to the original cycle label, and reversing the borrowed transfer restores the buffer row exactly.

Every addition uses available column capacity and every removal follows an addition in that same row. No original floor, label, slot, or capacity is changed. Repeated nonadjacent row colours are harmless because cycle labels are distinct and a row's original surplus and deficit sets are disjoint. Adjacent edges cannot have the same colour.

The outside buffer can temporarily displace a correctly placed incidence, so the proof correctly measures progress only at completed macros. Each macro restores all borrowed incidences and resolves its selected pending edges. The actual balance identity, row sizes and slack recur, guaranteeing another eligible transfer or cycle whenever differences remain. Finite pending-count decrease proves termination at the exact compact labelled destination.

### Protected degree leveling

Lemma X15L is correct.

When excess degree is positive and S<=Dk, an above-D donor forces a below-D recipient. Their degree inequality guarantees an actual row containing the donor and missing the recipient. Add-before-delete is consequently eligible and floor-safe.

After the addition, the recipient degree is at most D, while all other degrees remain at most M. For every forbidden set K of at most q-2 labels containing the recipient, number of roots hit by K<=D+(q-3)M<r. Thus an actual root misses it. Sets not containing the recipient retain their old actual missed-root witnesses through the addition. The subsequent deletion cannot lower transversal.

This checks every forbidden set using the same actual incidence columns, rather than fictitious independent capacities. The proof supplies a donor, recipient and editable row whenever the excess potential is positive, and each completed transfer decreases that finite potential by one. The resulting entry need not be exact q; the candidate correctly preserves that distinction.

### Complete composition and saturated internal entries

Theorem X15N follows with the stated hypotheses.

Cover-retaining endpoint compaction preserves exact q throughout and has saved reverses restoring all noncompact incidences. Leveling the two compact endpoints yields actual degree-D entries, with all intermediate lower protection retained.

In strict slack, X15S stays within degree D. The leveling inequality implies r>=(q-2)D+1, so every forbidden small set still misses an actual root.

At saturation, S=Dk forces all entry columns to have degree exactly D. X14's lower cycle construction applies to the actual pending graph without requiring exact-q internal entries. Its single temporarily overfull column yields at most(q-2)D+1 roots hit by any forbidden set; the additional saturated inequality makes this strictly less than r. Its cycle restoration, next-cycle availability and termination remain valid.

The candidate appropriately invokes only this lower construction at the potentially inexact internal entries. It applies maximum-layer Theorem A only after concatenating the entire finite lower path between the original exact-q endpoints. All joins are actual saved tuples. Reversed destination leveling and compaction restore the complete original labelled destination.

No row permutation occurs in this new sufficient theorem, so its stated mixed-floor class is valid. Universal mixed-floor connectivity is not inferred.

### Completion of the nine-label domain

The new endpoint degree bound is sound. Roots avoiding a label at exact four require at least three hitting labels and lie on only eight other labels. A three-root three-guard would require three pairwise disjoint floor-three supports and therefore nine labels. Each avoiding family must consequently have at least four actual roots, giving endpoint degree at most r-4. Cover-retaining compaction preserves this bound.

For nine labels, choosing D=3 and M=r-4 gives:

| Roots | M | Incidences | Capacity | Verified mechanism |
| --- | --- | --- | --- | --- |
| 7 | 3 | 21 | 27 | Strict-slack degree-three repair |
| 8 | 4 | 24 | 27 | Protected leveling, then strict-slack repair |
| 9 | 5 | 27 | 27 | Protected leveling, then saturated lower cycles |

The leveling inequality holds in every row of this table. At nine roots the additional saturated inequality also holds. Thus the three previously possible residual counts are resolved by one general constructive mechanism, without a feasibility assumption or numerical campaign.

### Universal carrier composition

The universal theorem exhausts the carrier domain correctly:

- Palettes below six labels cannot admit exact four under floor three.
- Six labels force all twenty complementary triples to occur as actual roots. The actual ten-triple guards on a fixed five-label subset satisfy the inherited one-overlap placement budget at every feasible root count.
- Seven-label carriers use X12's actual incidence-guard composition and explicit exact hub within their checked domains.
- Eight-label carriers are completely covered by X14's infeasibility/regularity argument and X12 access above eight roots.
- Nine-label carriers use inherited protected/five-root repair at small arity, X13's six-root exclusion, the new degree-leveling argument at seven through nine roots, and X12 above that range.
- Palettes of at least ten labels use X12 wide-palette access for six or more roots, protected exchange for four roots, and inherited five-root repair. Fewer than four roots cannot have transversal four.

The inherited hypotheses are supplied: uniform floors justify full exact endpoint token permutations where used; O1 uses actual guards with at most one shared slot; palette-room uses the original floor sum; protected exchange is confined to protected endpoints; five-root repair includes its saturated case. Exact joins and reverse preparations restore every original labelled support.

### Consolidation and closure classification

The consolidation accurately explains local safety, reusable protection and guaranteed completion as separate obligations. It distinguishes temporary lower-path schedules from their converted band paths, and internal level-three entries from exact-four endpoints.

The accepted conclusion is universal original-floor-three, target-four native root repair, with an upper defect bound of one. It does not assert that every endpoint pair requires a positive defect.

The source correctly leaves original A11 destination-directed universality, unrestricted mixed-floor/higher-target connectivity and unrestricted nested universality open. Conditional child lifting retains the baseline interfaces. It makes no physical, fundamental-time, efficiency, originality, numerical-certification, or v16.55 implementation-certification claim.

Accept both frozen mathematical sources at the stated candidate and blobs for analytical publication and closure of their declared theorem domains. No revision is required.

Review method: immutable-source reading and direct mathematical checking only. No enumeration, numerical diagnostic, scientific tests, workflows, branch mutation, implementation, benchmark, or inherited-source rewrite was performed.
