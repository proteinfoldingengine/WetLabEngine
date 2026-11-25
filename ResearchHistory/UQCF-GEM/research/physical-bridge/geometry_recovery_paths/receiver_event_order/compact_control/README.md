# Same receiver inputs, different joint receipt

This is a supplied five-chart unit-star rejecting control for proposed receiver access, separate from the archived 25-chart proof in draft PR #158. The calculation was exploratory. The case here does not reproduce the archived degree-four geometry gate, propose an event scheduler, or establish a native record. No independent whole-argument verdict is claimed by this evidence packet.

## Premises and consequence

**Inherited:** v16.26 union-preserving single-incidence deletion and its separately implemented verifier at commit e61d5b0e827f7b412824ad46021e2ad6cc6f7875; P1 pushes the unit grade of a removed tip to its nearest retained ancestor; pair work on this star counts tips held by exactly one member of a pair. **Supplied:** the ordered five charts and seven tip supports in FIXTURE.json. All charts contain the root. Source A drops tips (1,2) or (3,4); receiver B is asked to drop tip 5 in both cases.

All source cuts avoid B's sites. B's own ordered view, exact P1 grade, own-site holder columns, ordinary legal deletion menu and incident row of pair works match at corresponding steps. The two source endpoints also have identical complete work tables: each chart outside A occurs equally often among the two edited tips in each arm. As the probe incidence at tip 5 is the same, those complete work tables remain equal after the probe.

Before the probe the minimum cover families are {BEX, AFX} and {BEX}. The first ordinary minimum in the specified chart order is BEX in both arms. F is the alternative holder of tip 5. The probe keeps AFX available in the first arm but destroys the only minimum BEX in the second, returning (0,false) and (1,true) respectively. The full own record of B remains identical between the two post-probe states; this distinguishes joint-caller output from local retained state. In PR #158's *archived* fixture, chart 12 has shared versus private tip 718, so its ordinary legal menu does not match; the supplied control here does not change that fact.

On all 32 subsets of the five edits, the minimum is 3 plus the indicator that both (A,3) and (B,5) have occurred. The cover increment is attributed to the later of those two events. All 80 directed edges are legal and all 120 complete orders yield the stated attribution; the B probe has one-unit increment in 60 orders. These counts are not a time ordering law or probabilities.

**Open:** The resulting certificate is returned to the joint caller. No inherited action in this packet supplies, writes, exposes or retains its value at B. An owner-aware mechanism must pass the identical-local-restriction control without assuming the very receipt access it is intended to establish.

## Reproduction and frozen checking contract

From this directory, point replay.py at the unmodified historical v16.26-consistency-increment-law directory. Both source Git blob identities are checked before evaluation.

    python3 -B replay.py /path/to/v16.26-consistency-increment-law > actual.json
    cmp EVIDENCE.json actual.json
    python3 -B check.py actual.json

The evidence contains all 80 historical certificates, not just the selected outputs. The checker imports neither the producer nor the historical code. It reconstructs each state and cover from the frozen incidence columns, checks the complete matched restrictions and pair work, counts the 120 orders and rejects a falsified trigger. The historical verifier rejects a false trigger independently. A fresh reviewer should challenge both the proof and the distinction between calculated joint attribution and B-owned access.
