# v16.35 — q-fiber barrier closure

Parent: fully verified v16.34 head `0b4e0fae619f44b951b0f1529c960237b3083d31`.

## Question
When two states have the same q=tau but lie in disconnected q-preserving move-components, what is the minimum unavoidable q excursion along any legal one-incidence path between them?

Use only existing legal covers, one-incidence moves and q. Do not add a physical energy or metric.

For a path Y0...Ym between q-equivalent endpoints with q0, define the excursion set of each intermediate q(Yk). Candidate scalar controls are preregistered only as mathematical summaries:
- L1 barrier B1 = min_path max_k ||q(Yk)-q0||_1
- Linf barrier Binf = min_path max_k ||q(Yk)-q0||_inf
- support barrier Bs = min_path max_k #{v:q_v(Yk)!=q0_v}.

## Gates
A. EXISTENCE: every pair of states in the same whole-union cover space is connected by legal one-incidence additions/deletions if intermediate q may change.
B. POSITIVITY: disconnected same-q components have strictly positive barriers.
C. COMPONENT LEVEL: determine whether barrier from one q-component to another is independent of chosen representatives; if not, report a range rather than force a component distance.
D. TRIANGLE/ULTRAMETRIC: test but do not assume metric properties on component-level minima.
E. LOCALIZATION: identify which parent coordinates must change on minimum-barrier paths; determine whether this is fixed or path-dependent.

## Verification
Independently reconstruct full move graph on the v16.33 bounded universe. Use exact integer q vectors and exact graph search; no floating thresholds. Require explicit shortest/minimax path certificates for each disconnected fiber pair.

Reject false barrier zero, omitted lower-barrier path, illegal move, changed union, and producer-supplied graph trust.

## Interpretation
Barrier is combinatorial excursion in consistency quotient, not energy/action/time/curvature.

Time is pruning / ordered recoverability update.
