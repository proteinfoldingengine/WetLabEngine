# Public Reproducibility README

## What this is

A test framework for pruning-order recoverability traces.

It asks whether geometry-like closure appears only when an ordered recovery ledger preserves:

```text
source-origin
prior event dependency
provenance lineage
entropy arrow
repair/recovery closure
```

## What this is not

It is not proof of:

```text
physical geometry
spacetime
GR
physical curvature
Einstein equations
ADM closure
```

## Required input

A real independent trace, not a static graph.

```text
source → disruption/loss → repair/recovery → closure
```

## Run

```bash
python v1472_12_manifest_runner.py your_manifest.json
```

## Evidence candidate only if

```text
real trace passes preregistered threshold
all nulls fail
geometry is never computed on inadmissible slices
```
