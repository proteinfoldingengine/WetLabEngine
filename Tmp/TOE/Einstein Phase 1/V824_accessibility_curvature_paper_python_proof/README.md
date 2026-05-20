# Accessibility Curvature Law — Paper + Python Proof

This package contains:

```text
ACCESSIBILITY_CURVATURE_LAW_PAPER.md
accessibility_curvature_proof.py
README.md
MANIFEST.json
run_stdout.txt
run_stderr.txt
proof_results/
```

## Core law

```text
G_proxy = 2α Δ log(A + ε)
A = exp(C - μ + η repair)
```

## Run

```bash
python accessibility_curvature_proof.py
```

## Claim boundary

Supported:

```text
The synthetic ordered-update model supports an accessibility-curvature scalar/conformal law.
```

Not supported:

```text
Full tensor Einstein closure.
ADM momentum closure.
Physical spacetime GR.
```
