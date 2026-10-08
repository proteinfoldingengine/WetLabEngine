# C3 optimal-host theorem — reporting clarification

Date: 2026-10-07.
Status: reporting-only clarification after independent mathematical ACCEPTED verdict.

Frozen scope: 22d0f1cfa93406379e9e0950d12548c422495f28.
Frozen proof: b91a850caf5b9e56094698cdd475243b793c62db.
Independent accepted review: c714fe91b55eccd919d6f402ce2b3bbb4cfb788d.

There are six mandatory endpoint-differing incidence toggles in the exact source/target. Therefore an eight-edit path has room for exactly two off-endpoint toggles, which must be the addition and subsequent deletion of one and the same temporary incidence.

In particular, after +w on any root, adding w on a different root would create a second temporary incidence. Restoring both at the exact target would require at least four off-endpoint toggles, violating the eight-edit budget. This eliminates an implicit additional-w branch in the optimal-host proof.

The frozen theorem and its conclusions remain unchanged. The accepted result concerns ONLY the declared four-root carrier and optimal eight-edit paths; longer alternative-host paths and general retained host selection remain open.
