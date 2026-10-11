# Independent publication audit — reserve activation

Verdict: **ACCEPTED** for the concrete, qualified publication packet reviewed below. Blocking findings: **none**. Final immutable publication, leased head binding, and final text/binary readback remain **PENDING and unattested**. This acceptance does not itself make the campaign CLOSED.

## Scope and evidence actually examined

This is a fresh separate publication review of the local concrete packet, not a new scientific reconstruction or a remote-fetch attestation. I read CLOSEOUT.md, RECONCILIATION.md, REPORT.md, REVIEW.md, RESULT.md, VERIFICATION_SCOPE.md, the binding and author audit records, raw mathematical/publication responses and manifests, audit implementation and controls, original metadata and archive/log bindings, binary entries, retained original-audit failure traces, and the log-transport diagnostic.

Scientific event: b1caebd3d57dcb74c85f969543d577931e04ed5b. Workflow run: 38142825347. Prospective scope freeze: bf40d757b903256f66f9f809b767db7d9ab0826f. The historical analytical/prospective and pre-remote status sentences in RESULT.md, VERIFICATION_SCOPE.md, REPORT.md and REVIEW.md are stage-specific retained material; CLOSEOUT.md and RECONCILIATION.md provide the current reconciled state. Their old pending statements must not be represented as the current outcome or silently rewritten within the already reviewed scientific input set.

## Executed verification

I ran audit_originals.py and test_original_audit.py in an isolated temporary copy, without changing implementation or original evidence. Both exited 0. Their regenerated author_reconciliation.json and author_audit_controls.json were structurally identical to the retained records.

The audit checks all four successful jobs against run and scientific identity; original archive digest, byte size and exact member sets; 46 mathematical and 49 publication inputs against the retained scientific documents and original artifact bytes; exact raw response hashes and ACCEPTED verdicts; first-attempt response records; per-suite test counts totaling 485 (30 new plus 455 inherited); identical verification/fresh scientific outputs; complete decoded job-log digest, size, job/run binding, upload identity and start/end markers. The two raw reviews have no reported missing assumptions or counterexamples. Reviewer acceptance does not imply inspection of every binary row: the raw publication review explicitly uses digest/size/count summaries for binary or oversized inputs.

The intact audit accepted and all nine adversarial controls rejected at the specified gates: missing whole archive, corrupt whole archive, missing review input, truncated complete log, wrong run identity, compensating per-suite test counts, omitted archive member, omitted canonical identity archive, and wrong job binding. These controls do not add scientific tests.

I separately recomputed all four Git blob identities from the actual original ZIP bytes and matched binary_entries.json. ZIP byte sizes are 2,448,389; 3,625; 4,441; and 2,447,948, all below 8 MB. They are whole archives; segment reassembly is not applicable. I byte-compared extracted raw reviews/manifests/gate with publication_evidence. All matched. These checks support the concrete local payload and prospective binary entries; they do not attest to a future immutable repository readback.

The certificate SHA256 is 7ad7b7ffee26ce7dade9ed18402606fdd2a1b7284b45c53bc6af65bff4dc2c30; the canonical companion SHA256 is d266da0cfb59738320d0479f7450eee264e35af6dc4f973e5a934f53cd7f667c. Recorded campaign counts agree with the archived certificate: 5,054 abstract sources, 47,151 abstract states, 173,230 candidates, 46,947 edges, 21,685 first-vacancy terminal identities; 8,192 native sources, 7,488 positive and 704 negative, 16,422 macros, 67,134 forward actual edits, and 75,326 forward slice occurrences/source-local distinct states.

## Required qualifications are present

- Exactness is for the specified fixed-anchor monotone saturated-neighbor full-star transfer template. This is sufficient for native reachability, not a classification of all native paths or arbitrary partial-star interactions. Native enumeration uses the declared canonical routes and all1/all2 K4,3 source profiles.
- The K4,3 chain achieves 18 actual incidence edits. The raw review's “requiring 18” wording is expressly qualified; no minimum-cost or shortest-path result is established.
- Order independence applies to exhaustive activation closure and its existence verdict. Early-stopping routes may have different lengths and intermediate surplus.
- Exact reversal restores the original labelled source only when there are no intervening changes. Arbitrary reserve use, exchange, repair and restoration remain unproved.
- The 303,865,084 protected one-hidden/state pairs are the recoverable logical Cartesian coverage count checked through exact factorization; this is not a claim of separately rerunning a predicate 303,865,084 times. Arbitrary finite hidden-completion safety is analytical. Reverse routes revisit already counted states.
- K2 zero-edit container reassignment is bookkeeping, not a committed incidence edit or source escape. Raw “physical edits” means model incidence toggles, not measured physical events.
- Native acquisition, retained record origin, enforcement, successor selection and progress, general native reachability, and broad C3/C4–C6 remain OPEN. No force, mass, energy, duration, fundamental time, geometry or dark-matter derivation is established. The closed source-escape result need not be reopened.

## Retained adverse evidence

The original-audit and first controls failure traces reject a local fresh-reproduction log at its existing size/digest check. I verified that the retained 18,002-byte truncated file has SHA256 3552cf5986035fb9d485024b4e527d05439d8d28ae829e34dd71db8e80c1adc9 and is an exact prefix of the current 23,959-byte original log. The restored file matches the retained complete provenance SHA256 a19bdc3b923f26fb6f94830828cae6b30198a4bfec50a920e70d0125eca7cf8d. The retained account says fresh retrieval matched the pre-existing complete digest without relaxation; the available files support exact recovery, but this review did not independently observe the retrieval chronology or establish the truncation mechanism. The closeout appropriately leaves the cause unknown.

The packet also preserves the genuine missing-producer RED, native closure-field RED, initial inherited-launcher path failure and corrected profile-omission control finding. None is counted as a passing scientific test. No substantive scientific or publication blocker remains in the reviewed claims.

## Reviewed document identity

The following SHA256 values bind this review to the concrete author-facing documents examined before any subsequent publication-stage status update.

| File | SHA256 |
| --- | --- |
| CLOSEOUT.md | e7fb2058bcb375ab7e3ba2c64dcee220259d55cc186edfd750f65f9ccde8afbb |
| RECONCILIATION.md | 4441dbbc0e7a0976b6e1acc7fb07250f39d5f2d9c14fde7faacf95930a84859d |
| REPORT.md | f2bff588ae268f094464d1c4f014b7177762ef3603796e1d59394dcb09fe2d54 |
| REVIEW.md | 697198ec7e3b8dfa07a0330181e142dd2b2159144cd017f54f22a3c5c8bb0191 |
| RESULT.md | 99f8687efb9333ed24103286a92eee3faaddcbca7ead0fec5112e77e786269a0 |
| VERIFICATION_SCOPE.md | 4a94c04528c7d53dc29065e636ac7844324e9a4e57052228a68f27f9262a2b09 |
| binding.json | b0d2f20a42213cfcbbefdfa3a710ae002ed8e53cf01d318b85ff33d9e8b4bd0c |
| author_reconciliation.json | 9ab4edd95da9c34a8d653e9f2b04ce1bb4da473bf27e510d6254a36ebed5b37e |
| author_audit_controls.json | 832c0cde5b7ffb44d081fbf4d370ccb7c2bfda100b9bb080882803d501170dfa |
| binary_entries.json | f7d6d941d8e8e57854147c566c8e5854891472136b36ab35ca8f0296f7e8e52c |
| log_transport_failure.json | b998695a1f2c0119a4f8ecc8847f95ee6304364d8718ad8cadc8b17c0347f4e4 |
