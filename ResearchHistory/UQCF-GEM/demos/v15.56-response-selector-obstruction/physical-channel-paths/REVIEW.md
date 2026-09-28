# Independent review

The independent reviewer checked the physical-path construction, exact normalization/positivity/CPTP argument, one-sided rank obstruction, implementation, protocol and tests before measurement. No blocking issues were found. The reviewer ran all five unit tests successfully without running the ensemble or editing files.

The review emphasized that normalization changes connected correlations nonlinearly, so normalized moments/ranks must be rebuilt rather than rescaled. It also clarified that the inherited zero-normal-block label concerns uncertified constant-rank stability, not physical-path existence. Both points are explicit in the implementation and derivation.
