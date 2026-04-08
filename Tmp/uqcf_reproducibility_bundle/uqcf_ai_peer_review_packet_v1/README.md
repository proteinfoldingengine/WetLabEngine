# UQCF AI Peer Review Packet v1

This packet is designed for AI peer review, not human journal submission.

## Purpose
Provide a compact, auditable package that answers four questions:

1. What are the explicit equations?
2. What is assumed vs derived vs numerically certified?
3. What is the first quantitative data-facing result?
4. How should the framework be positioned relative to adjacent idea classes?

## Packet structure

### 01_math_spine
The explicit equation layer:
- equations.md
- notation_table.md
- derivation_status_table.md

Use this first. It is the core mathematical audit trail.

### 02_quantitative_proxy
The first quantitative proxy confrontation:
- proxy table
- summary JSON
- note
- residual-mode audit showing whether a trivial wrapper fix rescues the mismatch

Key current result:
- proxy chi2 ≈ 6.83 over 6 anisotropic BAO points
- reduced chi2 ≈ 1.14
- RMS residual ≈ 2.61%
- one extra low-complexity wrapper mode improves chi2 only weakly (Δchi2 ≈ 0.68)

### 03_context
Compact positioning note:
- adjacent classes
- overlap
- difference
- novelty claim level
- what not to overclaim

### 04_observable_lock
The locked DESI-facing falsification grid:
- strictly positive F_AP-style proxy shifts on z = {0.51, 0.71, 0.93, 1.32, 1.48, 2.10, 2.33}
- roughly +0.26% to +0.91%

### 05_scope
Hard falsification and domain-of-validity note

## Recommended review order

1. 01_math_spine/equations.md
2. 01_math_spine/derivation_status_table.md
3. 02_quantitative_proxy/sprintF_proxy_confrontation_summary.json
4. 02_quantitative_proxy/sprintF_residual_mode_audit_summary.json
5. 03_context/context_novelty_note.md
6. 05_scope/sprintD_hard_falsification_note.md

## Current disciplined claim level

The framework currently supports:
- explicit equation visibility
- explicit status labels for assumptions vs derived vs numerically certified relations
- one first quantitative proxy confrontation
- one context/novelty positioning note
- one locked falsification layer

It does not yet support:
- a full likelihood cosmology claim
- a symbolic global proof
- or a final human-journal-ready theory manuscript
