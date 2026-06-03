# V1172 — 6D GPU Full-Stack Genesis Provenance Engine

This is the full-stack merger of V1171 and V1152.x.

## Adds

- 6D GPU pruning
- Genesis Pin / append-only ledger
- source-origin identity
- retained-sequence identity
- Ω similarity
- source-flow closure
- dimensionless provenance margin
- valid/adversarial controls
- side animation showing ledger/network pruning

## Run

Fast certification:

```bash
python v1172_6d_gpu_full_stack_genesis_provenance_engine.py
```

Cinematic side-panel animation:

```bash
python v1172_6d_gpu_full_stack_genesis_provenance_engine.py --animate
```

For a quick Colab smoke test, set `N_HISTORIES = 512`.
For the full GPU run, keep `N_HISTORIES = 2048`.
