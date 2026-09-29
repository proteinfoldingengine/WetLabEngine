# Independent review

Before measurement, reviewer review1607 independently passed the five synthetic tests and checked orientations, gradients, moving frames, counts, attribution and provenance. One important finding: the initial numerical bound used the unprojected reference norm, a valid but weaker control than the preregistered projected-reference bound. Added test_projected_reference_bound; observed RED, then implemented the exact projected control. Six tests now required. No protocol or measured inputs changed; no ensemble was run before this correction.

The verdict tracks a nonzero normal contribution separately from total response. Final reporting must retain possible cancellation by other contributions. The 16.15 protocol was reviewed with no further blockers.
