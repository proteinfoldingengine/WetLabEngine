# Footprint review defect — author adjudication and fresh-review obligation

Status: initial mathematical and publication verdicts ACCEPTED, but author reconciliation identifies incorrect mathematical paraphrases. Closure is withheld pending fresh corrected independent assessment. Proof and scientific implementations remain unchanged.

Initial execution:9a68f2b25fccc9638366467b6ce2df9eab5e538b; run38005748370. Both responses are preserved unmodified under evidence/footprint/initial, with original archives, hashes and logs.

Both reviewers state that mapping current core hits back to original core hits guarantees the hitting number cannot increase beyond the original. That direction is WRONG. If H covers the current completed state, replacement produces a source cover H' with |H'|<=|H|. Thus tau(source)<=tau(current). In particular it forbids a current two-cover when the source has tau>=3. The separate condition tau(D)<=4 supplies the upper bound. This is exactly how the unchanged frozen proof argues.

A direct counterexample to the review paraphrase is C=({a},{a},{b},{c}), D=({a},{w},{b},{c}), empty Q, palette{a,b,c,w}. All floors1 hold; each D footprint is contained in an original footprint and tau(D)=4, but tau(C)=3. This local author control was checked with the existing exact hitting routine after review; it is not part of the prospectively frozen census or its counts. Its mathematics is immediately checked by four distinct singleton roots versus three distinct original labels.

Both reviewers also summarize all first-edit failures as footprint violations. Correct split: every deletion fails the floor in the admitted empty-Q world; every syntactically valid addition of an active label violates footprint containment. The frozen proof already makes this split. Also C4 is a project obligation label, not a hitting-number band; no identification of general C4 with broader bands is intended.

Fresh review must independently assess these points, the unchanged theorem and all other claims, not simply retain ACCEPTED. If any proof or code defect is found, identify it explicitly. Initial reviews and controls must remain accessible. A fresh run reproduces the same certificate and executes both mathematical and separate publication review with this adjudication included. This is an evidentiary correction, not a changed theorem, new finite campaign, or reason to change correct mathematics to obtain acceptance.
