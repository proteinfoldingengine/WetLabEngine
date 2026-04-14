# Fresh retained-state confirmation pack

This pack rebuilds the retained-information result from scratch.

## What it does
- simulates a fresh bounded nonlinear retained-state system
- compares G-only vs G+R prediction
- runs matched-pair close-R vs far-R contrast
- runs repeated-split validation
- runs reconstructibility and channel ablation
- writes plots and a short report

## Run
```bash
python fresh_retained_state_confirmation.py --outdir fresh_retained_state_confirmation
```

## Why it matters
This is a fresh independent reconstruction of the retained-state theorem shape, using new dynamics and new analysis from scratch.
