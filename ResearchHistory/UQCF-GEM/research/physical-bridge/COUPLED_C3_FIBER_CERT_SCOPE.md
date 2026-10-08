# C3 observation-fiber criterion for native commitment — frozen theorem-first scope

Date: 2026-10-08.
Status: PROSPECTIVE ANALYTICAL SCOPE; no independent acceptance.

Parent: COUPLED_C3_COMMIT_OBSERVABILITY_CLOSEOUT.md at 373baba85931899f2831f44d63f9dc6594ddc3c6.

Objective: move beyond one hand-picked rejected/committed pair. Derive a reusable NECESSARY-AND-SUFFICIENT mathematical criterion for whether any retained observation channel can certify a semantic commitment or recover a capacity bit, without introducing an acknowledgement oracle.

Declared general setting:
- Finite incidence state space X of labelled roots over a finite palette; admissible subset X_adm determined by original floors and protected hitting-number band.
- Attempted command a and a fixed known initial state x, with a nonempty set Y(x,a) of permitted post-attempt outcomes (which may include a rejected no-op x and committed native transition y). Rejection is not itself a native transition.
- Observation O(y) in a declared set R; known attempt a and initial x are part of the transcript.
- Predicate c(x,a,y) in {0,1} identifies actual semantic commitment. A separate predicate b(y) in {0,1} records desired capacity.
- No assumption that all commands may reject, that every edit commits, or that observation channels are physically accessible.

Required theorem:
1. Exact deterministic certification g(x,a,O(y))=c(x,a,y) exists on Y(x,a) if and only if c is constant on each O-fiber of Y(x,a).
2. The analogous iff criterion for b; and for simultaneous (c,b) certification, the pair must be constant on each fiber.
3. For finite Y, define the minimal additional observation partition needed to refine O to make the predicate recoverable; show it is the partition by predicate values INSIDE each original fiber, and state this is a mathematical distinguishability requirement, not a physical sensor.
4. Apply to C3 attempt +z(r4) from known E(empty), with permitted rejected no-op and committed insertion. Core-only O merges outcomes with c and b different; initialized full-palette singleton miss count for z, exact r4 size, or actual semantic acknowledgement splits them.
5. Show that if the outcome relation excludes rejection and has only one valid committed successor, the criterion is satisfied even by constant O. This demonstrates the obstruction depends on outcome nondeterminism, not on the mere existence of native signed syntax.
6. Avoid claims of general observer impossibility, observer-accessible initialization, forces, geometry, GR/ADM, or fundamental time.

No numerical campaign. Publish frozen proof and author audit; request independent adversarial review before any closeout.
