# An inherited consumer of the holder's distinction

Author: proteinfolding-gpt. Date: 2026-10-18 America/Phoenix.
Source head: `392a569a1f5732ff765765ed3cc0650748fdb997`.
Status: unreviewed analytical continuation of [PROBE.md](PROBE.md), B support for the existing receiver-identification candidate. No new scientific implementation, physical readout, independent acceptance or milestone.

## 1. The constructive question

The preceding probe identifies the joint observable that becomes a local holder coordinate. Here the question is whether an existing native operation can subsequently *use* that coordinate, without adding a READS table or a decoder.

There is already such a consumer at the level of the inherited mathematical model: a later P1 contraction takes the present holder's grade as an input to its next fiber sum. The exact input dependency follows from the same retraction that defines the event. This does not yet show a physically accessible measurement outcome, but it avoids making a separate reader mechanism a prerequisite for internal state-to-state propagation.

Credit and scope: receiver_identification Theorem 3 already proves that a single difference follows its lineage; sections 12-15 study holder motion and loss. This note does not repackage that propagation as a new theorem campaign. It extracts the exact consumer interface and gives a concrete two-event, equal-total trace for the access investigation.

## 2. Required inputs of one existing operation

Let s:Y->Z be an admitted nearest-retained-ancestor retraction, and b in Z. On the finite formal grade domain Omega_Y(N) of PROBE equation (2), N>=1, define the b-output of the inherited operation by

    F_b(y) = (mu_s(y))_b = sum_{a:s(a)=b} y_a.             (1)

Let D_s(b)=s^{-1}(b). For a set W of input addresses, ask whether the exact output F_b is a function only of the named raw coordinates y|_W, for every configuration in that formal domain. Then

    F_b factors through y|_W  iff  D_s(b) subset W.        (2)

Proof. If D_s(b) is contained in W, sum its coordinates. Conversely, if a in D_s(b) is omitted, compare y=0 with y'=e_a. Both lie in Omega_Y(N), agree on W, but F_b(y)=0 and F_b(y')=1. Therefore no function of those raw coordinates alone computes both outputs. QED.

Thus D_s(b) is the unique minimal *raw-coordinate input set* on the stated formal domain. It is fixed by s, not chosen to make a nominated source distinguishable. A precomputed sum is of course a sufficient statistic; (2) is not a lower bound on physical messages, memory, circuit gates, or measurement cost. On constrained or correlated physically admissible preparation sets, the minimal input set can shrink. In particular, total grade and other supplied side information can determine an omitted coordinate. The formal proof is not a preparability theorem.

For h in Y and two allowed inputs with y'-y=w e_h, ordinary additive grades give

    mu_s(y')-mu_s(y) = w e_{s(h)}.                         (3)

This is exactly the inherited single-holder propagation result. In consumer terms, the next owner's computation necessarily uses the old holder's value when all other incoming values agree. It does not inspect a history label or first decide which hypothesis is true. The operation is the same in both histories; only its state input differs.

## 3. A two-event trace with equal total grade

Take the prefix tree with edges o->a->h->u and o->v. The Genesis identity and all addresses are common. In address order (o,a,h,u,v), use the formal inside/outside pair

    x_in  = (0,0,0,1,0),
    x_out = (0,0,0,0,1).                                  (4)

Both have total grade 1. The proposed receivers h and a each have identical initial full formal coordinate states (grade 0). These formal preparations are not asserted to be two legitimate histories; the existing native-preparability obligation stays open.

First retain Y={o,a,h,v}, pruning u into h. P1 gives, in order (o,a,h,v),

    y_in  = (0,0,1,0),
    y_out = (0,0,0,1).                                    (5)

The local state at h now distinguishes the two inputs, while a remains blind. Next retain Z={o,a}, pruning h into a and v into o. The required input sets are

    D_s(a)={a,h},   D_s(o)={o,v}.                          (6)

Consequently, in order (o,a),

    z_in  = (0,1),
    z_out = (1,0).                                        (7)

The second existing operation has consumed h's changed coordinate and changed a's coordinate. Neither event is selected by the hidden hypothesis. No actual-record lookup, conditional controller, copying gate, new register or new outcome law is introduced. This is a two-location pair, so both final coordinates distinguish; it is not a claim of unique ownership for arbitrary multi-source differences.

The zero/nonzero effect at a separates the final states without an absolute unit calibration. A subsequent contraction to the root makes both outputs total 1, erasing this particular distinction. The example therefore requires retention of a at the claimed endpoint; it does not promise indefinite accessibility.

There is no clock in this trace. P1 composition gives the same endpoint under any admitted factorization with the same final retained set. The two displayed contractions make the consumer relation visible; they do not derive their occurrence, force a schedule, or describe every measurement event.

## 4. What is earned and what remains

The existing v15.56 source_pushforward.py implements the same inherited dependency: each input grade is added to the output keyed by its longest retained prefix. FCV P0/P1, rather than that code, justifies the sum and its composition. No implementation was modified or executed here.

By contrast, v15.14 adaptive.py explicitly supplies its READS table and the A1-dependent B2 rotation. Equations (1)-(7) do not justify that table, the rotation, or an identification of a grade with a quantum binary record. They provide a consumer wholly within the P1 type.

There are now three distinct claims:

| Claim | Status |
| --- | --- |
| Which local grade changes under an admitted P1 event? | Already determined by the inherited fiber/lineage maps |
| Can an existing operation use that changed grade without adding a reader? | Yes within the inherited grade model: later P1 aggregation consumes it through (1)-(3) |
| Is that state and operation physically realized and its record available to the receiver? | Still requires PROBE equation (11); not derived by input dependence |

This distinction matters for the next attempt. A separate detector need not be invented merely to propagate the distinction internally. The positive candidate can use the same P1 primitive for acquisition and subsequent use. To meet the user's actual-access criterion, identify that existing state transition with an actual receiver-owned process, or establish an independently available local effect. A software evaluator reading its array does not establish either physical identification.

The user's actual atemporal measurement remains the empirical occurrence input. What still needs provenance is its *typed action* on this receiver state. Nondisturbance, canonical coordinate factorization, or the name "receiver" cannot supply that provenance. Initial blindness must concern the receiver's entire actually accessible state; it has only been shown here for the stated formal coordinate state.

## 5. Continuation decision and source evidence

Continue the same A candidate through this inherited consumer rather than coding a replacement READS interface. The next decisive advance must identify the actual receiver-owned input/output state of one P1 event. Do not count further variations of (3) as closing access; this note establishes the exact internal-use route to investigate, not a new physical law.

The claim-bearing sources and content hashes are in CONSUMER_SOURCE_MANIFEST.json. The inherited source binding and retained-amplitude definitions were also inspected: they bind a source event to a Genesis-address key and a relative grade, but do not declare the receiver's operational observations. They are not upgraded to physical access here. No archive-wide absence claim is made.

This is an author analytical result with elementary proofs and a fully displayed formal trace. No numerical test count, preregistered execution, independent Gemini verdict or completed scientific closure is claimed. Native bridge remains NOT_DERIVED. The existing independent-review quota hold and frozen evidence remain unchanged.
