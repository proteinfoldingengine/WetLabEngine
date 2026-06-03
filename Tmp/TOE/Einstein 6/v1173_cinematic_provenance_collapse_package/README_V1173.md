# V1173 — Cinematic Provenance Collapse Engine

This version makes the network pruning visible.

## Three synchronized panels

1. **Left:** 6D winner field projected into geometric surface.
2. **Center:** live provenance network. Histories compete; branches shrink as pruning selects retained flow.
3. **Right:** Genesis Pin ledger and pruning telemetry.

## Run

Fast metrics:

```bash
python v1173_cinematic_provenance_collapse_engine.py
```

Cinematic animation:

```bash
python v1173_cinematic_provenance_collapse_engine.py --animate
```

For quick Colab testing, set:

```python
N_HISTORIES = 512
```

For full GPU run:

```python
N_HISTORIES = 2048
RES = 8
```
