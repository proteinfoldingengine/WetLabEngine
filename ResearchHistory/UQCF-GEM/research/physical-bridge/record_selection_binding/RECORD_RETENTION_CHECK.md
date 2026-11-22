# Source interpretation check: the joint operation and the original record

Author analysis, November 20, 2026 America/Phoenix.
Status: analytical follow-up, not independently reviewed. No native premise is upgraded.
Baseline: draft PR153 at 444f3426c326e3d79b09f7de6e45dbd69ba877e6; integrated research at e7e01bab68ba5171dacd91333f98d208d810dac3.

This checks an inference that must not be drawn from the newly reviewed joint-instrument theorem. Its mathematics is retained. Compatibility of a conditional branch with a total channel does not establish that the original outcome remains readable in the total channel's source output. This is an application of the existing complete-fiber criterion, not a new record-recovery theorem.

## Inspected premises

- INHERITED code semantics: v15/v15.11/ontology_continuity_audit.py, blob 8871e50f19322adbb62f34ea3837ba8e6cb16c8b, functions pinch, select_record, refines and history_control. The selected state lies in the explicitly supplied projector's corner. Record-history order uses projector inclusion.
- INHERITED conditional interpretation: v15/v15.11/REPORT.md, blob 255a62a329cc4ebb445122a8c5602df6e2dabc9c, sections 3-4. Compatible record refinement is a premise. Nested retained algebras alone do not ensure retention of an old central record.
- ACCEPTED-CONDITIONAL joint instrument: JOINT_INSTRUMENT.md, blob 6bafbf6414f71cf97f3bd5822b50cc90e7a0f34f, and review record at PR153 comment 7054502724 / run 44845772193. The inspected raw verdict, blob c983d4fa93893ba92a31f426e400caf63780ca35, accepts that theorem while retaining NOT_DERIVED. This follow-up is outside that review.
- Existing analytical compatibility criterion: measurement_first_review/RESULT.md equations (2)-(5), blob e8523368d50c366150221c5210ea6192534008d7. A state-independent event descends through P1 exactly when it is a union of complete fibers; retention of a finer record algebra requires separate justification.
- SUPPLIED as in the joint theorem: matrix encoding on (o,p,u,v), Q=I-pi_u, channel C(rho)=Q rho Q+rho_uu pi_p, two-outcome contract, canonical preparations, and any interpretation of these as a physical event/probability/readout.
- ACCEPTED INPUT: an actual atemporal occurrence. Occurrence does not select the matrix instrument or identify its output with an owner-held object.

## Direct checks and known analytical conclusions

1. The original pinch D retains its record effect: D*(pi_u)=pi_u. For the new total channel,
   C*(F)=Q F Q+F_pp pi_u.
   Every such pullback has equal p,p and u,u entries. Consequently no source-output effect F can obey C*(F)=pi_u, nor C*(F)=Q, on all inputs. Arbitrary coherences in F cannot change this contradiction. Equivalently C(pi_p)=C(pi_u)=pi_p, so those source inputs cannot have different outcome probabilities under any common source-output readout.

2. This is the existing complete-fiber obstruction for the fiber {p,u}. A positive control survives: C*(pi_p)=pi_p+pi_u. The post-event parent amount is retained; the pre-event p-versus-u origin label is not recoverable from that source output alone. Recovering that label is NOT required for the weaker target of one owner-available effect with a source-dependent response.

3. The unique joint instrument still exists. Its u branch sends pi_u to pi_p. In the unchanged source encoding, refines(pi_p,pi_u) and refines(pi_u,pi_p) are both false. Its Q and u branch outputs both lie inside Q. Thus the old Q/u projectors on the source output cannot be identified with its two surviving outcome labels, and u->p alone is not a strict inclusion step in the original history_control order. This does not rule out a separately justified record algebra, a different representation, or a different compatible history. It prevents importing that old history result without the missing correspondence.

4. The canonical pair exposes the conditioning scope without assuming physical preparability of pure basis states. In the mathematical model:

| Description | Plus parent probability | Minus parent probability | Difference |
|---|---:|---:|---:|
| Nonselective C output | 3/5 | 2/5 | 1/5 |
| Conditional Q branch | 1/3 | 1/4 | 1/12 |
| Conditional u branch | 1 | 1 | 0 |

   Both preparations have positive u weights, 2/5 and 1/5. The u-conditioned source states coincide exactly. This does not refute statistical distinguishability of the whole instrument, or the existing nonselective p-effect response. It shows that the nonselective contrast cannot be cited as the same conditional contrast for every accepted record. No universal per-outcome response or full record recovery is imposed as a new requirement.

## Frozen verification scope

The above results were derived before execution. The bounded check will import the original source unchanged after verifying its Git blob, call its pinch, select_record and refines functions, and compare with independent exact rational matrix calculations. It will check the dual map on all 16 matrix units, the two canonical preparations, the pure collision witness, and the positive full-fiber effect.

Rejecting controls will reject the claims that the original pi_u record is retained by C, that u->p is projector refinement, or that the u-conditioned canonical source states separate. The original D record and the parent full-fiber effect are positive controls. No sampling, new event construction, outcome law, environment, record register, decoder, or source-wide campaign is introduced.

This is a bounded interpretation check outside the prior Gemini acceptance, not a numbered certification stage. The admitted producer remains missing, so no new Gemini run is requested to re-certify the existing complete-fiber result.

## Research consequence

The current positive joint-instrument theorem survives intact. For future candidates, specify which consequence the claimed owner actually holds: the changed parent amount, the selected Q-branch state, or an outcome label in a justified record algebra. These are different objects. The known parent response is sufficient if its event binding and availability are earned. Adding an ungrounded outcome register would leave the existing ownership gap unchanged.

Next source obligation: identify one inherited actual operation and the same owner's available effect, with the claimed conditional or nonselective state semantics stated explicitly. No source inspected here supplies that obligation. Native event binding and owner access remain NOT_DERIVED; scientific_breakthrough=false.
