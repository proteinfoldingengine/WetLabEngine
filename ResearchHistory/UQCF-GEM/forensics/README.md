# UQCF-GEM Forensic Records

This directory contains provenance-first audits and historical reconstructions that support the active UQCF-GEM research program without promoting retrospective interpretation into experimental fact.

## Protein research records

- [Early Protein-Backbone Engine Forensic Reconstruction](backbone-lineage-2026-09-16/) — reconstructs the Phase-I observable-driven engine, Patch 630 full N-CA-C backbone physics, TPO / Goldilocks lineage, historical QIS combined probe, and later production-QIS divergence.
- [Protein P0 — Frozen v9 Native-Information / Source-Provenance Audit](v9-native-information-audit-2026-09-17/REPORT.md) — separates the unresolved provenance of the canonical April-v9 generator from a recovered executable handoff reproduction. Current result: `CANONICAL_V9_GENERATOR_PROVENANCE_UNRESOLVED`; recovered reproduction: `V9_REPRODUCTION_SOURCE_RECOVERED_AND_AUDITED`.
  - [Machine-readable P0 summary](v9-native-information-audit-2026-09-17/SUMMARY.json)
  - [P0 source manifest](v9-native-information-audit-2026-09-17/SOURCE_MANIFEST.json)
  - [Historical repository-recovery record](v9-native-information-audit-2026-09-17/RECOVERY_SEARCH.json) — exact v9 packet commit/tree plus bounded repository/Drive search; result `EXACT_V9_GENERATOR_NOT_RECOVERED_IN_AUDITED_REPOSITORY_SCOPE`.
  - [Recovered reproduction source audit](v9-native-information-audit-2026-09-17/REPRO_SOURCE_AUDIT.json) — hashed executable reproduction, static dependency audit, native-geometry substitution control, and RNG reproducibility finding.

## Claim discipline

Forensic records distinguish:

1. executed/raw evidence;
2. executable source and exact provenance;
3. contemporaneous narrative claims;
4. later synthesis and interpretation.

A recovered reproduction is not silently promoted to the original historical generator. Source-level claims are scoped to the executable object actually audited unless a provenance binding is independently established.
