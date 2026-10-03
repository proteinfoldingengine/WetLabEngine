# UQCF-GEM execution baseline

Status: **UNCERTIFIED ENGINEERING BASELINE**. Read-only analysis of completed v16.54 runs; no scientific execution, tests, workflow changes or performance acceptance took place. Scientific integrated reference: `466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f`. This document does not change its bounded scientific certification or claim a universal theorem.

## Measurement and completeness

GitHub run metadata and per-attempt jobs were fetched for every attempt reported by each of the nine runs (all report attempt 1). Jobs endpoints were paginated with per_page=100; total_count was exhausted: primary 10 jobs, reproduction 11, actual merge 11, and one job in each aggregation/preservation run. Raw job creation/start/completion timestamps, every returned step, retrieval URLs, exact-SHA workflow source, requests and relevant source are in timing_baseline.json. Source ledger maps the cross-workflow chains.

| Campaign | Created → final job | Duration-weighted critical path | Sum of runner job spans | Critical path |
|---|---:|---:|---:|---|
| [37059520424](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/37059520424) | 34m43s (2083s) | 34m36s | 93m15s | development → domains (7) → inherited |
| [37069226242](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/37069226242) | 46m43s (2803s) | 46m33s | 98m58s | route → development → domains (7) → inherited |
| [37075311542](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/37075311542) | 48m42s (2922s) | 48m32s | 99m27s | route → development → domains (7) → inherited |

Wall time ends at max(job.completed_at). Run updated_at is retained separately, because it is not a dedicated immutable completion timestamp. Runner sums are allocated job spans, not CPU time or billing. Critical path weights declared dependencies with observed durations, excluding queue and interjob gaps. Every matrix job is included in runner totals.

The primary workflow graph is development → eight domains → inherited. Reproduction and actual merge add route → development. Workflow needs, rather than timestamp coincidence, establishes these edges. Domain readiness is development completion; inherited readiness is the latest completion among all eight domains. Job creation minus readiness is dependency-to-creation delay; start minus creation is observed queue. Neither is inferred from the overall wall time.

## Bottlenecks observed

Actual merge shard 7 started 23:04:34Z and completed 23:34:15Z on 2026-10-02: **1781s (29m41s)**. Other domains took 374–627s (6m14s–10m27s). Inherited began 23:34:18Z and ended 23:47:36Z: **798s (13m18s)**, following all domains by declared dependency. Shard 7 was also the slowest primary (1147s) and reproduction (1913s) shard. This demonstrates skew in allocated job spans, not its internal cause.

The combined shard execution step includes source binding, independent whole-universe reconstruction, SQLite storage, freeze, production, verification and writing. Internal phase times are unavailable and explicitly null. Source inspection confirms whole-universe matching is repeated per shard, but its cost is unmeasured. Compression, setup and artifact steps are reported only at the granularity GitHub exposes. No attribution to case counts, CPU architecture, cache, memory pressure or infrastructure is justified.

## Cross-workflow chain

| Chain | Aggregation / preservation | Campaign final job → aggregation created | Aggregate final job → preservation created | Campaign created → preservation final job |
|---|---|---:|---:|---:|
| primary | [37063427057](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/37063427057) / [37069220208](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/37069220208) | 1m57s | 52m24s | 95m39s |
| reproduction | [37073565129](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/37073565129) / [37074296257](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/37074296257) | 0m54s | 1m02s | 57m21s |
| actual_merge | [37084743074](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/37084743074) / [37085148218](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/37085148218) | 77m57s | 1m58s | 134m22s |

Actual merge aggregation was created at 2026-10-03T01:05:33Z: **4677s (77m57s)** after the campaign final job, or 4676s after run updated_at. This is a request/launch interval between workflows. Its cause is unavailable; it is not runner queue or a measured scientific phase. Aggregation job span was 248s and preservation 92s. First-run preservation delay similarly includes work outside the campaign DAG. The separate workflows are request-triggered in fetched YAML, so automatic bounded orchestration could remove the need to launch them separately; no measured saving is claimed.

## Permitted inference

A2 changes scheduling: after development, complete inherited work may overlap complete domains if all source/protocol/resource/coverage checks remain invariant. Reserving one of eight total slots requires domain max-parallel 7, so one domain waits and observed durations cannot establish net speedup. Longest-domain skew and request gaps motivate A2 evaluation. A3 prepared-universe chunking is deferred: it would change preparation/artifact interfaces and needs a separate freeze and independent verification. No scientific cases or controls may be omitted.

Provenance: [execution ledger](https://github.com/proteinfoldingengine/WetLabEngine/blob/466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f/ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/EXECUTION_LEDGER.md), [scientific requirements](https://github.com/proteinfoldingengine/WetLabEngine/blob/466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f/ResearchHistory/UQCF-GEM/AGENTS.md). Exact source contents and run API URLs accompany the timing JSON.

