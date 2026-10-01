# v16.52 prospective recursive ternary composition protocol

Status: PREREGISTERED / NOT EXECUTED / NOT CERTIFIED.

Verified integrated parent: 76f373c8940433efc463762e675daf3e231f8cb5.
Parent tree: 3829d2f4be44c3c19c72f990afcf6e45b4559817.
Parent independent closeout: 41d9b7bc8bf8b73cc01cefcbcd8fdc9ee8a1b4cf.
The v16.51 amendment remains disclosed in inherited evidence.

## Prior knowledge and target
v16.50 established finite binary composition. v16.51 established one ternary root over binary children, including attached compact contraction and ordered-role transport. It did not certify recursive ternary composition.
Before this registration, source inspection suggested an arity-independent complete-role replacement argument: during duplication the new label's child-incidence pattern is dominated by the old one, and during deletion the reverse domination holds. This is a disclosed proof lead, not a new preregistered discovery.
No new numerical campaign, new implementation, or recursive proof acceptance precedes this registration.

Primary question: do fixed-root normalization, compact canonical endpoints, exact-interior complete-role transport, attached contraction and transported-order equivariance form an interface closed under binary AND ternary joining?
Scope: finite rooted ordered trees with every internal arity in {2,3}; nonempty nested supports; frozen primitive one nonroot incidence move; global root fixed.
Target profiles have integers 1 through local arity. Primary B1, Binf, Bs remain independent scalar minima. LEX is diagnostic only.

## Proof obligations
R1 define a typed interface with all quantifiers, arbitrary ordered root palettes and exact endpoints.
R2 prove complete-role replacement preserves every interior hitting number at every primitive, for arbitrary descendant arity; explicitly account for proper-parent nesting, nonempty supports, and subtree-absent destination.
R3 prove binary joining preserves the SAME interface when children are not assumed binary.
R4 prove ternary joining preserves it for targets 1,2,3, including a width-k child, child-local holes, ordered roles, and exact phase boundaries.
R5 prove prefix compactness, attached contraction, arbitrary ordered palettes, transported-order equivariance and well-founded finite induction.
R6 derive scoped independent barrier consequences from integer lower bounds; do not infer disconnectedness or positive barriers for endpoints in the same exact component.

Candidate width recurrence: leaf1; binary target1 max, target2 sum; ternary target1 max, target2 max(max child width,ceil(sum/2)), target3 sum. This is a target to prove and independently validate, not a verifier axiom.

## Frozen directed cases
Let L=(), B=(L,L), T=(L,L,L), A=(T,L,L).
Shapes: A; F=(T,T,L); G=(T,T,T); H=(A,T,B); J=((T,L),(L,T),T).
Each shape includes EVERY target profile q with q_v in 1..arity(v), in preorder. Profile counts respectively9,27,81,162,324:603 total.
For each profile use candidate minimum M and M+1; label permutations identity, reversal and cyclic; starts compact and exact-preserving inflated. Total7236 directed identities.
Compact starts are recursively canonical under the permuted labels.
Inflated starts scan every nonroot vertex in preorder, labels in increasing order, adding an absent label iff it is in the parent and the resulting entire target profile remains exact. No path findings influence this procedure.
Expected identity is (shape,complete q,k,permutation,start mode); independent verifier reconstructs all identities and requires exact equality. Count-only checking is insufficient.
These are directed specification cases, not exhaustive enumeration of all admissible states. Generality rests on proof.
Every primitive is independently checked for admission, fixed root, one incidence, total SUM of absolute profile deviations <=1, and exact common endpoint.
Independent verifier uses support sets and exhaustive hitting-set minimization, not producer bitwise/profile/width functions. Independently derive child-interface minimal palettes via incidence-region feasibility for 2/3 children. Cache only identical immutable feasibility questions.

## Outcomes and stopping
RECURSIVE_INTERFACE_VALIDATED: all R1-R6 accepted independently and all frozen cases and controls verified.
INTERFACE_NOT_PRESERVED: a specific construction/interface obligation fails, retaining full case and partial path; NOT a nonunit witness.
INCOMPLETE: coverage, resources, infrastructure, provenance or unresolved proof obligation. Retain all evidence; no dropped cases, silent domain reduction or post hoc relabeling.
NONUNIT_CERTIFIED is a separate optional claim requiring an admitted endpoint pair and independent exhaustive threshold disconnection or rigorous lower bound ruling out ALL unit paths. No such search is required by this campaign and no failed construction implies it.
Higher arity and physical interpretation remain outside scope.

## Execution and controls
Numerical science/tests on GitHub only. Local source inspection and byte/log/hash audits allowed.
Python3.11, sympy1.13.3, mpmath1.3.0, ubuntu24.04. 45-minute job ceiling; stop INCOMPLETE on timeout.
Before producer implementation: commit and execute genuine expected-failure tests for absent recursive interface and a full independent-verifier omitted-corpus rejection defect. The verifier may be implemented first to make the latter meaningful using a separately constructed frozen canonical zero-path control corpus. Missing/duplicate/substituted/wrong-profile cases must be rejected by the actual verifier entrypoint. Preserve logs and exact RED manifest. No helper-only substitute.
Then implement minimal construction and green controls covering nested total-excursion stacking, root changes, invalid moves, wrong endpoints, minimum palette, width-k order, child-local hole, role-order mismatch, failure retention and classification; provenance and archive corruption controls.
Freeze exact new test manifest before definitive science. Inherited1071 checks unchanged and all39 v16.51 scientific files freshly reproduced.
Full closure: independent proof/source review; primary artifact-bound science; separate fresh reproduction; source/log/certificate/manifests and original archives durably published; exact-head review/ready/merge; actual-merge full replay; independently reviewed durable receipt decision. No external-auditor dependency. No CLOSED/CERTIFIED until all gates pass.
