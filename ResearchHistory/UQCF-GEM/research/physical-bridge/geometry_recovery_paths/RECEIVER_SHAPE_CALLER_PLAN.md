# Receiver shape at a nonroot fork: prospective test

Parent 13a498316c2bb6b07614865813843dec3dfab5b7, draft PR 156. Historical implementation e61d5b0e827f7b412824ad46021e2ad6cc6f7875. This responds to PR 111 comments 7147250309 and 7149694094.

## Preparation and intervention

Use a root, its child p, and three tip children a, b, c of p. Every chart starts with root and p. Source S also holds a,b,c, helper H holds a, and receiver R holds b. The fine extensive grades in that order are (5,3,2,2,1). The only intervention is whether S deletes a or b. Derive the local cover profile from each resulting state. Give both arms the same target: S holds c, H holds a,b, R holds no tips; all keep root and p. Invoke archived v16.39 build with those arguments, with no requested receiver turn or observation prefix. The target and invocation are supplied. R is characterized before intervention by its unique support of b alongside S. Include every permutation of the three chart indices and three sibling indices, and a zero-tip-grade rerun with the same geometry. Compute the two original source moves' v16.26 legality, every constructed move's coverage/profile and endpoint. Test the source-only alternative in which S removes both duplicated tips in opposite orders.

## Predictions to challenge

At p each post-source cover should have size two. The inclusion-minimal size-two cover should be unique, with one participating holder per tip. Its first singleton assignment should leave b with S after cutting a and with R after cutting b. In both cases the first archived recolor should read that same tip b and transfer it to H, using the actual list returned by shrinking the initial state. Record its old owner and verify that the materialized route contains the corresponding edits. Verify that the different receiver states disappear at the common endpoint. A trace that only scores the final certificate, a hard-coded receiver actor, or an address mismatch between arms fails this test.

Independently check the fixed fine test counting the grade below b: exact recovery for all grades from R's pushed P1 vector iff the test is constant on retraction fibers. Check its accessibility at the endogenous first recolor alongside the fork atom and a common-address subtree sum. Zero grades at both a and b should preserve the shape read, while erasing the fork-atom contrast. Audit whether any archived caller actually receives that numerical P1 vector.

## Replay and limits

Publish the positive or negative outcome and trace, with an independent set-based implementation and the exact archived execution. Keep archived file hashes, permutation controls, source-only continuation, foundational suite and provider disposition. Record failures. A successful trace would establish code-level use of receiver-related coverage conditional on this three-chart preparation and historical caller. Whether the source event itself requires the caller, the receiver can access that computation locally, or it gives a physical gravity signal remains open.
