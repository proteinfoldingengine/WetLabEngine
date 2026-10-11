# Converted nested record — implementation and closure plan

> Implement inline under executing-plans and test-driven-development. Review delegation only; no implementation delegation.

Goal: independently verify RESULT.md's conditional source-erasing record conversion, preserve its precise protocol boundary, and complete the existing scientific publication loop.

Spec: COUPLED_C3_RECORD_CONVERSION_SCOPE.md and COUPLED_C3_RECORD_CONVERSION_RESULT.md at the prospective freeze. Existing scientific parent 0427e18aeae1625b7bd685e511038f769eef0c01. All analytical findings in those files are already known before computation. No native-access, actual-selection, guaranteed-write, shortest-path or physical closure claim.

## Frozen serialization and interfaces

Tree vertex order (o,u,r,w,B,C), with parents [null,0,1,1,0,0]. Labels a,b,c,d,x are integers 0,1,2,3,4. Extra labels start at 5. Five-way profile digits are 0=root only, 1=A only, 2=A and W, 3=B0, 4=C0. All supports are serialized as integer bit masks in vertex order. Initial source bit sigma and five-bit execution mask use integers; mask bit j selects command j+1.

Commands are [[2,4,1],[2,0,-1],[2,1,1],[2,4,-1],[1,4,-1]]. Executed positions are 1-based. Every requested history has identity [n,profile_digits,sigma,mask], canonically sorted by n, profile digits, sigma, mask. There are exactly 1984 identities.

A row contains id, status (VALID or REJECTED), states (initial plus each processed skip/legal-edit slice), profiles (h_o,h_u at each saved slice), executed (positions), failure (null or first illegal executed position), end (last legal support tuple), record_at_stop (a absent), source_erased_at_stop (u equals baseline A), and peak (largest |h_o-3|+|h_u-1|). On an illegal selected command stop immediately BEFORE appending its candidate state. Rejected histories are not realized complete executions; their fields describe the legal prefix only.

Top-level fields: schema='nested-record-conversion-v1'; source_parent; scope_sha256; commands; rows; forgery; claims. Claims are protocol_sound=true, native_access=false, guaranteed_write=false, optimality=false. Forgery contains the base sigma0 source, the native path +b(r),-a(r), profiles, native_valid=true, protocol_valid=false, record=1, source_erased=true, peak=0. Its states use the same encoding.

producer.produce() returns this entire object. producer CLI writes deterministic sorted compact JSON plus newline. independent.expected() separately reconstructs the complete object, independently enumerating subset partitions and full endpoint admissibility/hitting sets. It must also check signed source membership and exactly one named incidence change; endpoint admission alone cannot turn an absent deletion or present addition into a native edge. independent.verify(doc) compares canonical JSON exactly, rejecting bool/int substitutions as well as wrong or missing data; returns a compact summary only after equality. No producer imports or shared enumeration/math helpers in independent.py. Fixed scientific constants are duplicated deliberately.

## Tasks

- [ ] Freeze reviewed proof, scope, plan and source identities in Git before new scientific execution. Preserve raw analytical review and any author reconciliation.
- [ ] Write test_conversion.py first, using unittest. Every accepting test calls a readiness assertion so absent producer/checker produces genuine assertion RED, not a fabricated exception. Preserve red.log before implementing.
- [ ] Implement producer.py (bitset/local admission) and independent.py (set partitions/full admission/exhaustive hitting) from frozen schema. Compare all canonical records, not just counts. Run complete new tests and retain output.
- [ ] Tests must verify the full 1984 universe, complete positive five-edit routes, no false-positive valid sigma0 history, one-sided (not guaranteed) writes, source-erased positive record {b}, peak-one slices and exact completed endpoints; reject missing/duplicate/substituted rows, modified source bit/state/record/peak/protocol/binding/claims, malformed types and a forgery misclassified as native-illegal or protocol-valid. Verify the out-of-protocol native counterhistory positively.
- [ ] Check every saved slice with the existing v16.53 verifier.profile_check using pinned source bytes, in addition to the independent checker. This is a cross-check, not independence for the new checker.
- [ ] Fresh code review before scientific publication. Resolve critical/important issues and preserve failed executions.
- [ ] Run GitHub verification, the full 504-test integrated Path-A contract stack from the latest escape-obstruction workflow, new tests, full canonical reconstruction and native profile comparison. Record per-suite logs and actual counts; expected prior counts do not replace inspection. Workflow and scientific SHA must coincide.
- [ ] Fresh job regenerates byte-identical certificate and independently reconstructs it. Mathematical Gemini review then separate publication review, retaining exact manifests/raw responses, source hashes and actual verdicts. No unsupported closure after mere workflow success.
- [ ] Download original job archives and full logs. Audit members, sizes/digests, per-suite counts, source/response/provenance bindings and reproduction. Preserve failed controls. Publish scoped closeout, raw evidence, continuation entries and verified readback through leased commits; inspect current head before each ref update.

## Review focus and stops

Rejecting controls target dangerous false positives, not only missing files: arbitrary-history forgery accepted as a true source certificate; illegal source erasure with descendant x; omitted inexact slice; wrong order (+b before -a); claimed guaranteed write despite all-skip; native access inferred from record definition. A failed proof or checker requires correction and fresh gates, not narrowing the declared universe after seeing results.

No random search, heuristic branch pruning or extra source family. Total primary universe 1984; counterhistory separately declared. No implementation delegation or new external integration. Use the existing GitHub-secret Gemini review runner. Scientific runs remain open until original evidence and independent publication audit are verified.

Integration before freeze: current branch parent a8ca2289d4a4c7a5643cb028f17c06cd150ad771 adds the inherited coherent-register realization screen and an origin-index entry. The compare from 0427e18 shows no scientific implementation or used theorem changes. That screen is retained; this candidate does not claim its missing quantum/incidence representation or native enforcement/access bridge. Analytical source snapshot remains 0427e18; freeze is based on the current integrated parent.
