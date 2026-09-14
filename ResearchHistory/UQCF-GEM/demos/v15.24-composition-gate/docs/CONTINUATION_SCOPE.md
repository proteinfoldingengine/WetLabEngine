# Continuation and evidence boundary

The earlier continuation stopped with a staged tree, not a published v15.24 branch.
This continuation preserves its model, tests, renderer, template and baseline bytes.
It adds executable verification/publication and corrects the report's evidence
wording. Previously stated local numerical results are provisional historical
values until independently reproduced by the new run.

The tests-first Git parent bca53f756507f0d33ac7eae353fe0b1391144e02 is retained.
The workflow replays a missing-model control from that parent and a missing-view
control from an isolated copy. These runs demonstrate failure sensitivity now;
they are NOT the original local RED logs, which were not recovered in this turn.
It then runs all 436 selected tests (30 v15.24 plus 406 preserved checks).

All report/HTML/video/data/evidence delivery is through GitHub. The archive
records fresh source identity, environment, CI logs and byte digests. A successful
movie decode does not prove visual quality or browser correctness; those checks
must be executed and reported separately. No independent peer review or formal
proof checker is claimed. None of this closes older original-byte archival gaps.

Publication stays on an additive research branch and draft PR. No existing
research file, fixed scientific tolerance, accepted physical assumption, main
branch or repository visibility is changed. No new research version beyond
v15.24 is opened before this gate and its publication are finished.
