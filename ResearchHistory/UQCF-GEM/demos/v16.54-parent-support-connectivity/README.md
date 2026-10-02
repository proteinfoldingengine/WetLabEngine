# v16.54 — structural conditions for one-unit repair

Current status: the complete primary campaign, fresh reproduction, independent aggregation, durable publication and evidence review passed. All 77 scientific files reproduce exactly. Actual-merge replay remains pending; the implementation is not yet CLOSED/CERTIFIED.

## Mathematical result

The parent-support problem reduces to connectivity of capacity-bounded complementary blocks that cover every `(q-2)`-subset. Once such a lower-guard connection exists, maximum-layer replacement removes upper excursions and gives a root path with transversal number in `{q-1,q}`. This criterion is independent of branching number.

Exact-q endpoints have additional structure: their complements cover every `(q-1)`-subset, leave at least one q-subset uncovered, and obey `sum_i(k-a_i) >= (q-1)k`. These are derived endpoint restrictions. They are not assumed to prove general pair- or higher-subset exchange connectivity.

The accepted floor-two theorem connects every feasible exact-q endpoint pair with all root floors equal to two, for arbitrary arity (q>=3; the elementary cases handle q=1,2). The accepted analytical work also supplies constructive regimes and explicit limits: element-cover buffering, degree-two cycle exchanges, saturated configurations, guarded clone/contraction and relocation steps, palette slack, finite-support reduction, and native lifting. A failure of a particular module construction is recorded as such; it is not promoted to impossibility of every native one-unit path.

The universal higher-floor connectivity question remains **OPEN**.

## Implementation evidence

The approved [prospective validation plan](PROSPECTIVE_VALIDATION_PLAN.md) freezes nine mechanism families M1–M9. The producer constructs paths; a separate verifier reconstructs the entire prescribed universe and checks primitive steps, width floors, guards and the shared excursion budget.

- First complete campaign: GitHub run `37059520424`, scientific/workflow SHA `0ba1284ade581267997882de2d4c723f2b9ee3a4`. All eight complete-domain shards and the inherited v16.53 stack passed.
- Independent aggregation: run `37063427057`. Complete identity coverage, prescribed mechanism diagnostics, original artifact hashes and full inherited-package verification passed.
- Fresh reproduction: run `37069226242` at `0a0037bc74399e04609e156d3bfd00736486bcbc`; all eight domains, 83 development controls and the full inherited stack passed. Aggregation `37073565129` passed.
- Durable publication: run `37074296257`, evidence commit `aca507ff7a22f7ee6050c2c6eb6e8da0e93653dc`. All 77 scientific files are byte-identical to the first campaign; all nine original archives were reconstructed and verified by the executor and independent reviewer.
- See [independent premerge review](INDEPENDENT_PREMERGE_REVIEW.md) and [reproduction interpretation](INDEPENDENT_REPRODUCTION_DESIGN_REVIEW.md). Final certification still requires replay and accepted evidence at the actual merge SHA.

Use [EXECUTION_LEDGER.md](EXECUTION_LEDGER.md) and [INDEPENDENT_IMPLEMENTATION_REVIEW.md](INDEPENDENT_IMPLEMENTATION_REVIEW.md) for the execution and review record. Frozen analytical documents and `protocol.json` retain their original historical status text; this page reports the subsequent implementation phase without changing those preregistered bytes.

## Proof entry points

- [General parent connectivity](GENERAL_PARENT_CONNECTIVITY.md): maximum-layer replacement, complementary-block criterion and arbitrary-arity target-three connectivity.
- [Exact endpoint capacity](EXACT_ENDPOINT_CAPACITY.md): the stronger endpoint conditions.
- [Module capacity obstruction](MODULE_CAPACITY_OBSTRUCTION.md): a characterized limit of the module method.
- [Finite-support reduction](FINITE_SUPPORT_REDUCTION.md): reusable finite support for a prescribed finite path.
- [Native admissibility](NATIVE_ADMISSIBILITY.md): the fixed carrier and move rules.

This work extends v16.54. It does not open v16.55.
