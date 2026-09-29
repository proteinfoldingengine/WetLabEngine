# v16.26 — Proof ledger

## P1 locality
Removing a leaf c from one view changes only membership of c. Since c is a child of v and has no retained descendants in that view, only A_i(v)=Ch_U(v) intersect Y_i changes. All other child-incidence families are identical.

## P2 atomic bound
Let t=tau_v(before). v16.25 monotonicity gives tau_v(after)>=t. If any t-view cover survives, equality holds. Otherwise choose an old t-view cover S. The deleted c was essential to S. Same-union admissibility supplies another final view j containing c. Then S union {j} covers all children after deletion, so tau_v(after)<=t+1. Thus tau_v(after) is t or t+1.

## P3 exact trigger
By definition tau remains t iff at least one old minimum t-cover remains a cover after deletion. Therefore it rises iff every old minimum cover is destroyed.

## P4 global increment
Only tau_v can change and it changes by at most one. Since h=max(1,max tau), delta h is 0 or 1. It equals one exactly when the changed local value exceeds the previous global maximum.

## P5 atomic factorization
For a same-union endpoint refinement Z_i subset Y_i, repeatedly remove a leaf of Y_i\Z_i. Prefix closure is preserved. Every removed node belongs to the common final union, so some Z_j contains it and hence it remains in that view throughout. Thus each atomic step preserves the union. Finite repetition reaches Z.

## P6 path independence of total
For any atomic factorization V_0 -> ... -> V_m, sum_k (h(V_k)-h(V_{k-1})) = h(V_m)-h(V_0) by telescoping. P4 makes each summand 0 or 1. The locations of ones need not be canonical; the total is.

No fundamental time, response operator, or geometry enters.
