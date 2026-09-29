# v16.25 review

Self-review challenged: the original ill-typed strict fixture; changed-union overclaim; factorization tautology; oversized certificate design; and intermediate-carrier validity.

The most important defect was executable: the verifier accepted a non-prefix intermediate carrier while still satisfying raw composition. Run 36612453511 preserves the failing adversarial test. The corrected verifier now validates the intermediate retained object before checking composition.

No separate reviewer is claimed.
