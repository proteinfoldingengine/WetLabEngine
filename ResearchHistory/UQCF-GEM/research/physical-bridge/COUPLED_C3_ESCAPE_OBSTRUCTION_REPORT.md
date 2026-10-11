# Perfect-matching escape-without-vacancy obstruction — verification report

Status: VERIFIED at event commit `857803fb97e80a9d7b4f9338ebf9ef2de4d5f8e1`; bounded closeout pending immutable publication readback. This report closes only the prospectively frozen `K6-{45}` / perfect-matching campaign. Broad C3, C4–C6, and physical origin remain OPEN.

## Result

Let `H=K6-{45}` and let `G` be any perfect matching contained in `H`. For every positive profile `a in {1,2}^6`:

1. every source has an actual first `X` escape (already within the CLOSED source-escape theorem): a type 4 or 5 label can retain its unique saturated edge `vw` and add `wz` for a third neighbor `z` of `w`;
2. no nonempty `G`-independent set is deficient, because the matching partner map injects `I` into `N_G(I)`;
3. by the CLOSED cover-static theorem there is no static reserve endpoint;
4. therefore no admissible path reaches a first vacancy, despite the available source escape.

This is an endpoint obstruction. It is neither the known all-NOOP obstruction nor a hidden-fiber obstruction. It separates an admissible escape relation from actual endpoint existence and actual-record selection. It supplies no hidden-state oracle and no progress requirement.

The tempting bridge substitution is invalid: completing the crossing label to `M(w)` adds no net support at the already-supported saturated bridge `vw`; deleting a destination-type label then lowers support from the required `a_v+a_w` to one less.

## Frozen bounded universe

- 14 host edges;
- 12 perfect matchings;
- 64 multiplicity profiles;
- 768 sources;
- 96,768 ordered `V`/`X` candidate classifications, including rejections;
- 48,384 nonempty vertex-subset/neighborhood rows;
- 19,968 actual-source-label admitted `X` routes;
- 110,592 route slices;
- 39,936 distinct route states counted source-by-source;
- 648,680,448 exact protected one-hidden-mask/state checks.

The producer and independently written checker reconstructed all 769 canonical JSONL records and agreed byte-for-byte on stream SHA-256 `b6b53398b5ec82f9552284b93cdb2e10ef357bc277e27054eda3aee41af77610`. A fresh reproduction produced the same digest.

## Verification and controls

Actions run `38167992780` passed all four jobs at the exact event commit:

- verification: 504 tests (9 new plus 495 inherited Path-A tests);
- fresh production and independent byte-identical reproduction;
- Gemini `gemini-3.1-pro-preview` adversarial mathematical review: **ACCEPTED**, zero missing assumptions, zero counterexamples;
- separate publication/evidence audit: **ACCEPTED**, zero missing assumptions, zero counterexamples.

All frozen rejecting controls fired: forbidden edge `45`, incomplete matching, false `X`, missing third vertex, minimum-degree substitution, false deficiency, saturated-bridge substitution, canonical corruption, stream truncation, extra row, and noncanonical encoding.

## Preserved adverse and infrastructure evidence

- Commit `7aaccd8b83f9a001e2d8f138fa2dbb4397ffc28d`, run `38167334252`, job `114552511434`: intentional tests-first RED; `ModuleNotFoundError` for the absent independent checker. No implementation computation occurred.
- Commit `c6751bc676e8398854c287411ed077685de3ed3a`, run `38167717768`, job `114553649731`: the new tests, producer, and checker passed, but the inherited stack stopped on the misspelled star-carrier test filename. This was a workflow-only failure, preserved before the one-line correction.
- Commit `857803fb97e80a9d7b4f9338ebf9ef2de4d5f8e1`, run `38167992780`: unchanged frozen science passed after correcting `test_star_carrier.py` to the existing `test_star.py`.

The three original Actions ZIP artifacts and full logs for all six relevant jobs are preserved under `evidence/c3-escape-obstruction-2026-10-11/`.

## Limits

This result is limited to `H=K6-{45}`, its 12 perfect matchings, and profiles `{1,2}^6`. It does not classify sources with a static reserve, arbitrary saturation graphs, later transfers, actual successor selection, mandatory progress, or physical origin. It adds no geometry, force, fundamental time, dark-matter variable, observation channel, or numerical heuristic as proof. No v16/full-stack certification follows.
