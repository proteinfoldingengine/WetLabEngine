# v16.34 — Intrinsic invariant of disconnected q-fiber components

Parent: fully verified v16.33 head `126bb0a7039902bccc3699db1839c4a5a0f817b2`.

## Question
v16.33 proves that some q=tau fibers are disconnected under legal one-incidence q-preserving moves. What already-earned retained information distinguishes those disconnected components without restoring the complete labeled incidence state?

## Candidate data, in increasing strength
For each retained vertex v let M_v(Y) be the exact family of minimum-cardinality indexed-view subsets whose union covers Ch(v).

Test:
A. minimum-cover-family signature M(Y)=(M_v)_v;
B. essential-incidence signature E(Y): labeled incidences appearing in every minimum cover at their parent;
C. minimum-cover participation counts per labeled view and parent.

These are derived from the existing child-to-view incidence and the already-defined minimum-cover problem. They are not new physical observables.

## Gates
G1. CONSTANCY: Is candidate signature constant on every connected component of every q-fiber under invisible one-incidence moves?
G2. SEPARATION: Do different connected components of the same q-fiber always have different candidate signatures?
G3. COMPLETENESS: If a candidate is constant and separating, prove that equality of the candidate implies a q-preserving move path; do not infer this from bounded enumeration alone.
G4. MINIMALITY: If several candidates work, determine logical implication relations. Do not call one minimal solely because its serialized representation is shorter.

Possible outcomes: COMPLETE_INVARIANT / PARTIAL_INVARIANT / COUNTEREXAMPLE / UNRESOLVED.

## Exact definitions
M_v(Y)={S subseteq indexed views: |S|=tau_v(Y), union_{i in S}(Ch(v) intersect Y_i)=Ch(v)}.
E records only labeled child incidences (i,c) such that view i belongs to every member of M_parent(c) and c is retained in i.
Participation records for each (v,i) how many minimum covers in M_v contain i.

## Bounded audit
Reuse the independently reconstructed v16.33 universe exactly: rooted unordered trees through four vertices, 1–3 indexed views, whole-tree union. Reconstruct every q-class and invisible-move connected component independently. Evaluate A–C on every member.

Publish:
- component counts;
- within-component candidate variation;
- between-component collisions;
- smallest positive/negative witnesses;
- relabeling/storage-order controls.

## Rejecting controls
Reject producer-supplied connectivity, fabricated minimum-cover families, omitted minimum covers, wrong essential incidence, candidate equality across states when raw recomputation differs, and any claim of completeness supported only by finite enumeration.

## Interpretation
A complete invariant would classify connected components of the mathematical q-fiber under elementary invisible moves. It is not a physical charge, topological sector, or gauge invariant absent a later physical argument.

Time is pruning / ordered recoverability update.
