# A11.X51 analytical scope - multi-cover exception chains

Parent: c94851834d298aec31700bed14c537a3fc022299.
Objective: replace X50's two-cover relay by a block-stable chain of any finite number of physical covers, and give a joint structural ordering certificate with actual lower pair witnesses.

Already-known reasoning disclosed before source freeze: for cover K_j let U_j be source exceptions and V_j destination exceptions. A cover works throughout active block p iff maxpos(U_j)<p<minpos(V_j). If K_0 covers the source, K_h covers the destination, and every U_(j+1) type precedes every V_j type, a first-index interval argument appears to cover every block, without requiring nested exception sets. Combining these upper precedence edges with selected new-witness-before-old-witness edges appears sufficient when the actual type graph is acyclic.

Planned structural control: disjoint physical four-sets K_0,...,K_h on k=4(h+1) labels, fixed complementary roots for all four-sets other than these, plus source/destination exceptional roots. A prescribed interleaved order should have exact-four boundary states with UNIQUE successive covers K_j, forcing h+1 distinct cover witnesses along that schedule. This is an upper-certificate necessity for a declared schedule, NOT absence of another two-cover order or native disconnection. Fixed background will be a permanent lower guard, openly distinct from interdependent lower renewal.

Native labels/slots/individual original positive floors and single-incidence primitives remain fixed. Positive original copies are allowed; no ingredients are added during repair. Prove exact endpoint hitting number, all pair witnesses, old/new coexistence, floors, eligible next moves, DAG ordering/termination, full labelled restoration, per-leg minimum, repeated-leg conditions and method limits.

Freeze exact candidate for fresh whole-argument review and separate reporting review before branch publication. Analytical only; no numerical execution, implementation, benchmark, integration merge, numbered stage or physical claim. Preserve all X49 failures, historical proofs and v16.55/v16.54. Efficiency work remains separately scoped and unstarted.
