# Implementation review before v16.04 measurement

Preregistration commit: 1273637d90bfc71b90f22f377c877f08ec8b96dc. Expected RED run 36479322504, controls job 109120785455, inspected from the exact job log: six absent-implementation assertion failures; measurement job skipped.

Independent review checked the commutator sign, global index lift, connected differential, source contribution sign, parent provenance/structure, and domain/rank/precision controls. It identified missing explicit covariance and precision checks for prepared commutator directions, and missing precision checks on connected directions. These were added before measurement, with the original tolerances retained. Follow-up review approved the corrected implementation with no remaining critical or important findings.

Six new regression tests and nine parent regression/reporting tests pass locally. Local Python is 3.12; the workflow pins Python 3.11, numpy 2.3.5, sympy 1.13.3 and mpmath 1.3.0. No candidate or ensemble measurement was executed before this review. Measurement must still establish actual numerical validity; review is not a scientific result.
