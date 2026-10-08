# C3 core-visible two-sided readout — prospective scope
Status: NEW ANALYTICAL CANDIDATE; verification/review/audit not yet run.
Parent: a33943ee29bc23202b608e16bdeccff250cb83cd; native record-origin gate remains OPEN.

## Exact model and incremental question
Use the existing four disjoint core pairs ab,cd,ef,gh and spectator w on roots1/2, hidden bits x,y. Original floors2, band 3<=tau<=4. The observer receives labelled core projections after each attempt; it receives NO tau, hidden cardinality, spectator read, rejection reason or success acknowledgement. Core accessibility itself is inherited and not physically derived.

During a readout episode x,y are invariant. Allowed core commands are +/-a(root1), +/-c(root2), +/-e(root4), each executed once as either the syntactically valid toggle with an admissible successor, or a NOOP. Every invalid request MUST be a NOOP; legal requests may also reject. No other writers, delayed or compensating changes. This is the already declared admissible-toggle-or-NOOP transition model, not a supplied legality-query output. It assumes actual inadmissible edits never commit.

CRITICAL SCOPE CHANGE: commands need not be known admissible in every currently compatible state. This gate is NOT the uniformly-safe-command safe-probe model. If admissibility enforcement is not supplied by the native relation, the protocol is unlicensed. Do not call that enforcement physically derived or a controller algorithm.

Let d1,d2 indicate removal of a,c and b indicate added e on root4. State ID is x y d1 d2 b. Baseline core has d1=d2=b=0. Hand deductions, known before enumeration:
tau=4-xy-b; floors iff d1<=x,d2<=y; admissibility adds b<=1-xy.
Expected primary universe:14 admissible states, six core commands,84 rejection self-outcomes and26 committed outcomes, total110.
Baseline anchored service subgraph: x=1, d1=d2=b=0, commands +/-w(root2), two states and six outcomes.

## Proposed result
A visible -a(root1) certifies x=1, and -c(root2) certifies y=1 through original floors. Observing both removed certifies xy=1. A visible +e(root4) certifies xy=0 through the protected lower bound. These are actual core changes, not hypothetical legality reads. For each hidden pair there is a reachable finite core transcript certifying its conjunction, but all-NOOP paths exclude guaranteed acquisition.

Core restoration by reinserting a,c and deleting added e is admissible and preserves x,y; complete restoration is observable and reachable, never guaranteed. Stored certificate persists only while hidden bits are unchanged.

On the core-certified x=1 sector, either visible -c or visible +e certifies y=1 or0. Restore core, attempt exactly one payload +/-w(root2), then acquire a fresh readout certificate. Comparing pre/post certified y distinguishes actual toggle vsNOOP. This is delayed, certificate-conditioned detection, NOT instantaneous readout after every attempt. Repeat only after observed restoration. No initial hidden-bit recovery after destructive payload edits is claimed.

## Verification/review contract
Freeze proof before execution. Producer: exhaustive label-subset hitting oracle over 32 candidate configurations. Independent verifier: minimal unions of one representative per root, independent integer-state relation. Compare full state, edge, observation-fiber, service and restoration-path identities; exact types and provenance. Test missing/duplicate/substituted states/edges, wrong tau, invalid floor/band moves, false NOOP inference, omitted core observation, silent hidden writers, uniform-safety overclaim and guaranteed-progress/physical-access claims.

Resources: standard-library Python; finite exact enumeration only, producer timeout30s and Actions15min cap. Stop on any exact mismatch or accepted corrupted control. Inherited compatibility checks are diagnostic, not full v16 certification. Require fresh adversarial review, author reconciliation, separate whole-evidence publication audit, durable raw artifacts and immutable readback before scoped closure.
