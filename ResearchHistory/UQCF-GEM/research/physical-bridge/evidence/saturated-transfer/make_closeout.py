import json,pathlib,re
base=pathlib.Path(__file__).parent
e=json.loads((base/'EVIDENCE.json').read_text())
math=json.loads(re.sub(r'^```(?:json)?\s*|\s*```$','',(base/'math/review.txt').read_text().strip()))
audit=json.loads(re.sub(r'^```(?:json)?\s*|\s*```$','',(base/'publication/saturated_transfer_publication/review.txt').read_text().strip()))
assert e['author_reconciliation'].startswith('PASS') and math['verdict']==audit['verdict']=='ACCEPTED'
text=f'''# Saturated redundancy transfer: bounded scientific closeout

Status: CLOSED within the declared mathematical/interface scope. Broad C3/general C4/native observer access and progress remain OPEN. Date: 2026-10-10 UTC.

## Scientific discovery

A fully saturated overlapping core can release an already used private label without relaxing an original floor, growing its palette or adding a root. In the declared family W roots have {{A,b_j}} on a partition into k nonempty private blocks, singleton roles B,C, and host{{D,E}}. For k>=2, a donor private label replaces a reserve private label on its block. The released label buffers an exact apex/host exchange, then returns to its original block before donor cleanup. Every private and hidden incidence is restored exactly at each macro endpoint. The same capacity is renewable along any finite prescribed sequence of distinct current-apex/host exchanges. No hidden state is learned.

The sharp family boundary is k=1: saturated deletion fails in the admitted empty-hidden world, and every new addition violates original footprint containment. This source is isolated under uniformly safe core-only toggles, regardless of optional NOOP. For k>=2 the constructive script has2m+4+4|V_r| committed edits. This is an achieved cost, not a globally optimal bound.

Original source footprint domination gives tau(original full state)<=tau(current full state). A separate B,C,E and A-or-D four-cover supplies the upper bound. Add-before-delete preserves all original saturated floors. These analytical facts cover arbitrary finite partitions and arbitrary disjoint hidden palettes over ALL protected original completions; finite enumeration does not replace the proof. Inherited spare-buffer choreography is not claimed new. The increment over the prior occupied-reserve theorem removes its FLOOR-SLACK premise as well as an initially absent label for this family.

## Frozen identities and executed evidence

| Record | Immutable identity |
|---|---|
| Prospective scope/proof | {e['scope_commit']} |
| Tests and absent-implementation RED | {e['tests_commit']} |
| Executed science and workflow | {e['scientific_commit']} |
| GitHub Actions | [run {e['run_id']}](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/{e['run_id']}) |
| Verification job | 114094265762 |
| Mathematical review job | 114094522855 |
| Separate publication audit job | 114094775587 |

All98 tests passed:22 new contracts,26 inherited label-release,22 inherited footprint,28 inherited fixed-family. The initial RED is a missing-producer import failure: one unittest loader placeholder fails, ZERO scientific test bodies run. It is not22 failed scientific claims.

The entire bounded domain contains76 donor/reserve cases from every canonical partition at m=2,3,4,7444 protected source completions and274096 forward/reverse slice checks. These completion counts include repetition across donor/reserve choices. Three one-block sources check108 possible first toggles with admitted rejecting witnesses. Four separate native controls reject premature release/cleanup by floors, mixed reserve reuse by full tau3->2, and premature apex splitting by core tau4->5 in a three-private-block source. The latter does not claim every two-block premature schedule fails.

Production uses bit toggles and subset hitting sets. Independent reconstruction uses sets, Cartesian partition generation and minimal representative unions, compares the COMPLETE typed record, and rejects omissions, duplication, altered values, extra members and bool-for-int changes. Certificate: {e['certificate']['bytes']} bytes, SHA256 {e['certificate']['sha256']}. Local/Actions/repeated/fresh-publication certificates agree byte for byte. [Evidence ledger](evidence/saturated-transfer/EVIDENCE.json) records source identities, archive/member/input/response hashes, counts and reproduction gate. The three original downloadable ZIP bytes and all three actual job logs are permanently preserved under that evidence directory.

## Independent assessment and author reconciliation

Gemini mathematical review ACCEPTED and separate publication-consistency audit ACCEPTED, each with zero listed missing assumptions or counterexamples. Both use gemini-3.1-pro-preview via v1beta and are independent API assessments, not formal proof-assistant certification. Raw responses and their manifests are retained; [mathematical assessment](COUPLED_C3_SATURATED_TRANSFER_ACCEPTED_REVIEW.md) and [publication audit](COUPLED_C3_SATURATED_TRANSFER_PUBLICATION_AUDIT.md) describe their limits.

Author examination independently checks original source domination, cover direction, explicit upper cover, saturated floor replacement, reserve departure before reuse, restoration against the original fiber, endpoint private-label identity and renewal. No substantive mathematical objection remained. The publication reviewer's statement about verified freeze identities refers to supplied records: the API reviewer did not independently fetch GitHub history. Author immutable readback separately verifies the scope/proof and test freezes against executed input bytes. Reviewer shorthand 'up to m=4' means the frozen domain m=2,3,4; arbitrary-m statements rest on proof. The RED demonstrates an absent implementation, not successful execution of the scientific suite. Per-macro current-core next-action recognition does not imply that an arbitrary multi-macro goal list or its current goal index originates physically.

## Remaining assumptions and continuation

Current core access, static labelled routing/partition, disjoint palette, supplied original floors and protected-source promise remain assumptions. Hidden Q is fixed. Each committed edit is an actual single incidence toggle; optional NOOP may stall indefinitely. Core-slice recognition applies to each supplied exchange template; no automatic global goal selection, observer genesis, scheduler, hidden sensor or physical force is derived. No primitive spacetime, fundamental time, dark matter, continuum or GR derivation is introduced.

The next mathematical obligation is general saturated reserve availability: separate existence of an absent-label state in the universal safe region from reachability by safe toggles. Investigate maximal-original-footprint capacity with the upper-four cover constraint, and demand a native obstruction if capacity is insufficient or a feasible state is disconnected. This family result does not justify general connectivity. The native observer-record origin obligation remains independently OPEN.
'''
(base/'closeout.md').write_text(text)
for phase,obj,title in [('math',math,'Independent mathematical review'),('audit',audit,'Separate independent publication-consistency audit')]:
    key='mathematical' if phase=='math' else 'publication';r=e['reviews'][key]
    source='mathematical-review-response.txt' if phase=='math' else 'publication-audit-response.txt'
    body=f'# {title}: saturated redundancy transfer\n\nVerdict: {obj["verdict"]}. Not formal certification or broad C3/C4 closure.\n\nScience/workflow commit: {e["scientific_commit"]}. Run: {e["run_id"]}. Model: {r["model"]}. Input files: {r["input_count"]}. Total tokens: {r["tokens"]}. Response SHA256: {r["response_sha256"]}.\n\n[Unmodified raw response](evidence/saturated-transfer/{source}) and exact manifest/archive hashes are preserved. Zero missing assumptions and counterexamples listed.\n\n'
    body+='\n'.join('- '+str(s) for s in obj['findings'])+'\n\nLimitations retained:\n\n'+'\n'.join('- '+str(s) for s in obj['limitations'])+'\n\nAuthor reconciliation: scope/proof frozen before computation; complete bounded domain m=2,3,4, not all smaller m; RED executes only loader failure, not scientific test bodies. Analytical arbitrary-partition/hidden-palette proof is distinct from finite enumeration. Ordinary subset containment suffices for safety. Script cost is not global optimality. Supplied per-macro goals/core access and NOOP progress remain assumptions. The API assessment reads supplied records; its freeze-identity assertion is reconciled by author immutable GitHub readback, not an independent reviewer fetch of history. See closeout for exact boundary and evidence.\n'
    (base/('review.md' if phase=='math' else 'audit.md')).write_text(body)
print('Closeout and two reconciled review records generated; no broad closure claimed.')
