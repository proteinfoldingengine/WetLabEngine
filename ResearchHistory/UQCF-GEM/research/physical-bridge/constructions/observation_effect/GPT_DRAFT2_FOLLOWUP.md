# Draft-2 continuation: retain the positive occurrence construction and separate its two tests

Current review status: this unchanged argument, frozen as occurrence_contrast_review/RESULT.md, was independently ACCEPTED in run 39095260396. See the [acceptance receipt](../../occurrence_contrast_review/REVIEW_ACCEPTANCE.md). The original author text below is retained; its pending-review language describes the pre-review state. Acceptance does not cover the entire Grok draft or derive native receiver access.

Author: proteinfolding-gpt. Date: 2026-10-17 America/Phoenix.
Inspected branch: 35593a4faeed800bf9fff4d59fbd01a18b66b23a.
Status: author analytical follow-up, not independent acceptance of draft 2. No new mechanism, simulation or numerical campaign.

## Positive construction already available

Draft 2 compares one prefix x with its observed version E x. That avoids choosing two unrelated initial states. Its initially blank retained record follows from P E = P in the P2 setting. Preserve this improvement.

The accepted nonfaithful control in observation_preservation_review/RESULT.md section 3 already gives a stronger illustration than the three-atom example: a later operation can preserve every already observed receiver record and nevertheless make occurrence versus nonoccurrence perfectly distinguishable. We need not invent another operation or launch a campaign to see this; it is the same four-dimensional control, read in atom notation below.

This is an effect-level illustration with supplied motion. It does not resolve native receiver access.

## Two different questions, two different equations

Let P push forward onto the retained owners, I be the inherited owner section, PI = id, E = IP, and T be the supplied column-stochastic map on the fixed fine carrier.

Preserving an already observed record for every input means

    P T I = id.                                             (1)

An observation having no effect on any later fiber record means

    P T (Id - I P) = 0, equivalently P T = P T I P.          (2)

For a particular prefix x the occurrence contrast is

    delta(x) = P T (Id - I P) x.                            (3)

These are different contracts. Equation (2), not (1), is strong lumpability: P T = S P for a coarse stochastic map S. If such S exists, multiplying by I gives S = P T I; conversely (2) supplies that S. A lumpable T may change or permute the coarse record through S. Equation (1) fixes that coarse motion to the identity on observed inputs but says nothing about T on directions removed by E.

Thus draft 2 section 12.3 should not describe non-lumpability as failing PTI=id. Its specific three-atom swap has both properties, but those properties are not equivalent.

## Reuse the accepted four-dimensional control

Use atom order (a,u,b,v), fibers {a,u} and {b,v}, owners a,b:

    P x = (x_a+x_u, x_b+x_v),
    I y = (y_a,0,y_b,0).
    
Take the already accepted control T that fixes a,b and exchanges u,v. In the quantum notation of the accepted source it fixes basis 0,2 and swaps 1,3. Because T fixes the occupied owner directions,

    T I = I, hence P T I = id.                              (4)

For the single prefix x = delta_u:

    P x = P E x = (1,0),                                    (5)
    P T x = (0,1),
    P T E x = (1,0).                                        (6)

The receiver weights are initially identical. The two final declared record distributions have total variation one. Existing observed record weights are nevertheless preserved for every input by (4). There is no need to sacrifice record persistence to obtain this occurrence contrast in the supplied model.

This is direct substitution into the previously reviewed control, not a new native channel, new physical preparation, or fresh independent acceptance of the occurrence interpretation.

For comparison, exchanging whole fibers, a with b and u with v, gives P T = S P with S the two-owner swap. It is lumpable and leaves no occurrence contrast, although PTI = S is not id. This is an explanatory algebraic control only.

## Actual event and preparation scope

The user's actual atemporal measurement remains the declared event input; no prior external clock is required. The useful gain from one prefix is reduced preparation bookkeeping. It does not itself prove that an empirical event realizes the stipulated E, that the no-event counterfactual is operationally available, or that Q is an available receiver record. A mathematical counterfactual does not require laboratory intervention; an experimental discrimination claim would require an appropriate preparation/record contract.

Likewise the initial-blankness equality concerns the nonselective retained state. It should not be read as denying the supplied selective RCR outcome or asserting that no actual measurement was experienced. Keep the inherited selective/nonselective distinction.

## Native continuation stays at the source-backed interface

The live source check confirms:
- FCV TYPE_LEDGER L1-L8 identifies addresses, retained inclusions, grades and pushforward; it does not identify an address coordinate as a physically accessible subsystem.
- v15.56 source_binding.py localizes a certified source event at a Genesis/address pair and expressly earns no amplitude.
- record_access section 7 explicitly leaves the subsystem identification I* open.
- Draft 2 explicitly leaves motion and I* supplied. Optimizing T or U cannot settle either.

The previously published INTERFACE_HANDOFF already records this source resolution; this note does not count re-reading it as new science. The next native construction must instantiate that interface: an independently justified receiver state/observation structure, together with an inherited event acting on it. An operational receiver algebra can suffice; a tensor-product implementation is not mandatory. The event-to-state correspondence must be established before invoking (3) as physical evidence.

Do not turn this correction into another free-motion search or native milestone. Incorporate equations (1)-(3) in draft 2's planned whole-argument review, retain its supplied-motion scope, and keep the separate ownership/access investigation as the primary native task. The new draft and this follow-up remain unreviewed; the prior preservation acceptance is unchanged.

## Exact source anchors

All live sources below were read at the inspected branch SHA:
- constructions/observation_effect/CONSTRUCTION.md: Git blob 3972d74f23f18df09834986e3b68cf8e1676bedd (draft 2).
- constructions/record_access/CONSTRUCTION.md: I* remains explicit in section 7.
- ../../foundational-closure-verification/TYPE_LEDGER.md: Git blob aa2d66adbfd552188dd3dec9270824fd605981d8.
- ../../demos/v15.56-response-selector-obstruction/source_binding.py: Git blob a1df8db6c1d1b3fd4491a5f502267841725f3f32.

The four-dimensional control is frozen in observation_preservation_review/RESULT.md, blob ec8277d35207655eebe492fba0d98e344188e158, freeze 53d164b07e32576f04bdedc31f1c2d3757e9637e, accepted in run 39091716370. That review did not review draft 2 or this follow-up. Paths above describe provenance, not physical realization. No scientific module was executed and no full-draft certification is claimed.
