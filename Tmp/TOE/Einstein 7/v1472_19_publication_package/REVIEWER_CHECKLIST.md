# Reviewer Checklist

## Must pass

- [ ] Input is a pruning-order trace, not a static graph.
- [ ] `prior_dependency` references prior `event_id`.
- [ ] `provenance_id` does not satisfy `prior_dependency`.
- [ ] Entropy-arrow definition is external and declared.
- [ ] Damaged/repaired proxy is external and declared.
- [ ] Threshold is declared before scoring.
- [ ] Geometry-like closure is never computed on inadmissible slices.
- [ ] All required nulls are run.
- [ ] All required nulls fail.
- [ ] Continuous M_total is reported.
- [ ] Threshold sweep is reported.
- [ ] Claim boundaries are preserved.

## Automatic failure

- [ ] Static-only input.
- [ ] Provenance shuffle passes.
- [ ] Event order shuffle passes.
- [ ] Closure-only static null passes.
- [ ] Threshold adjusted after seeing score.
- [ ] Geometry computed on inadmissible slice.
