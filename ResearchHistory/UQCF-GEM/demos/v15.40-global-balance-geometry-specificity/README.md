# UQCF-GEM v15.40 — Global-Balance Geometry Specificity

## Result

`CANONICAL_INCIDENCE_GEOMETRY_SPECIFICITY_SURVIVES`

The preregistered finite exact gate found that the canonical global-balance response recovers the independently constructed `B2` face-neighbor relation at `L=5,7,9,11`. None of the four frozen controls passes the same all-size metric-and-correspondence rule.

This is scientifically important evidence of finite internal specificity, conditional on the inherited source and response axioms. It is not a physical metric, spacetime, gravity, a continuum result, Einstein dynamics, or a scientific breakthrough. Pillar 3 remains `OPEN`.

## Exact construction and result

For each face the audit uses `s_f=e_f-(1/L^2)1`, exact rational arithmetic, the canonical `(4I-A_ax)u_f=s_f`, and four frozen controls. The response constructor sees only labels, sources, and responses; the target constructor sees only signed `B2` support.

| Family | Metric at every size | `N_R=N_B2` at every size | Gate |
|---|---:|---:|---:|
| Global balance | yes | yes | pass |
| Direct inheritance | yes | no | fail |
| One-incidence transport | no | yes | fail |
| Matched diagonal balance | yes | no | fail |
| Matched step-2 balance | yes | no | fail |

The verdict is unchanged at scales `1` and `7/3` and after the frozen relabeling. Every source, unordered pair, and ordered triple was evaluated. Exact work and neighbor sets are stored with lossless, verified torus-displacement encodings in `docs/RESULTS.json`.

## Boundary and next object

This is an exhaustive finite computation, not a general-size theorem or continuum result. It supports only a finite internal Level-1 correspondence candidate conditional on inherited axioms. The next permitted object is `PREREGISTER_FORMAL_CONNECTION_CURVATURE_AND_SOURCE_CORRESPONDENCE_GATE`. Pillar 3 remains `OPEN`.

## Reproduce

```bash
python -m unittest -v test_gate.py
python geometry_specificity_gate.py --check docs/RESULTS.json > /tmp/v1540-results.json
cmp docs/RESULTS.json /tmp/v1540-results.json
python -m compileall -q response_generation.py response_geometry.py incidence_target.py geometry_specificity_gate.py test_gate.py
```
