# v16.27 — Proof and interpretation ledger

P1. For every legal atomic path from fixed V to fixed Z, sum(delta h)=h(Z)-h(V). This is v16.26 telescoping and is path-independent.

P2. A per-event attribution is canonical only if the delta attached to each fixed removed pair (view index,node identity) is equal across every legal factorization.

P3. The v16.26 trigger is explicitly state-dependent: it asks whether every minimum child-cover in the **current pre-deletion cover** is destroyed. Earlier deletions can change that family of minimum covers. Therefore v16.26 alone does not imply event attribution is canonical.

P4. One admissible pair of paths with the same endpoints and the same event set but differing delta for an event refutes universal event attribution. The witness must preserve prefix closure and common union at every intermediate state.

No stronger conclusion is allowed from finite absence.
