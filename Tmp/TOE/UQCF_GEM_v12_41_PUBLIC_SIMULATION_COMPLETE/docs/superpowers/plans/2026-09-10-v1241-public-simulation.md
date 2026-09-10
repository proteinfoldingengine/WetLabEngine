# v12.41 Public Simulation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and execute a standalone simulation of exact quantum moment-map closure with a broken control.

**Architecture:** A single Python module contains the quantum model, ordered sweep, diagnostics, CSV export, static plot, and animation rendering. A focused unittest file validates exact closure, broken-control separation, density-matrix validity, and output schema before rendering.

**Tech Stack:** Python 3, NumPy, pandas, matplotlib, imageio/ffmpeg when available.

**Spec:** `docs/superpowers/specs/2026-09-10-v1241-public-simulation-design.md`

## Global Constraints
- No fundamental-time interpretation.
- Exact branch must pass numerical closure assertions before rendering.
- Broken control must exhibit a materially nonzero closure residual.
- No inserted ADM or gravitational equations.

### Task 1: Numerical core
- [ ] Write failing tests for state validity, exact closure, and broken residual.
- [ ] Run tests and verify RED.
- [ ] Implement minimal numerical core.
- [ ] Run tests and verify GREEN.

### Task 2: Public artifacts
- [ ] Add failing tests for sweep schema and output creation helpers.
- [ ] Run tests and verify RED.
- [ ] Implement CSV, PNG, MP4/GIF rendering.
- [ ] Run complete test suite.
- [ ] Execute simulation and verify outputs.
