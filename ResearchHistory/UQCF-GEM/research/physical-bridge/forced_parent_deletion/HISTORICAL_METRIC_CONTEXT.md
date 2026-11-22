# Fixed-edge metric and active-context controls

## One edge with two calculated weights

V498's original graph code calculates a vertex conductance proxy from the min–max normalized degree of its own input graph. In the normalizer's A-removal history, B keeps the complete mask 63 and the common edge (o,v1). In the C-removal history B gains v7 on its first edit. It still holds the old edge. B's degree at v1 rises from 2 to 3. Its minimum and maximum graph degrees remain 1 and 3 and its root degree remains 1.

To expose just the topological term, supply the same fixed fields to the original V498 function on each chart. Use L=R=1, Lambda=Pi=0 and T/(C_surplus+epsilon)=1. The local average of this constant source ratio is still one. The V498 node loading becomes

    w(v) = 5/4 + (1/4) / (c(v) + 1/20),

where c is the original 1/5 plus 4/5 times the degree's min–max normalization on that chart. The historical code sets the edge weight to the mean of the endpoint loads. For B, c(o)=1/5 in both cases, and c(v1)=3/5 and 1, respectively. The original routine stores weights matching the independent exact calculation.

| Input to the historical V498 formula | Weight of the same edge o–v1 |
|---|---:|
| B after A releases v8 | 101/52 |
| B after C releases v8 | 157/84 |
| C at that same C-removal endpoint | 101/52 |
| Full fixed nine-vertex union, either history | 1705/1092 |

The difference between B's two calculations is 20/273 in the V498 model's weight. It starts on B's first addition and persists to the endpoint. In the high endpoint B and C both contain the identical edge. For the same supplied background fields the formula assigns different weights there, so both chart outputs cannot be restrictions of one metric. Evaluating the same code once on the full retained union yields a single weight and zero branch contrast. This tests the original formula on an explicitly supplied calibration, not an inherited route assigning the V498 fields to the support history. The project has not identified these dimensionless graph weights with a physical conductance or gravitational observable.

For any weighted-tree field with positive common edge conductance k_e, summing the balance equation over the descendants on one side of edge e cancels every internal term. The drop on the oriented edge is J_e/k_e, where J_e is the net load inside that subtree. The formal source dipole at v8 has zero subtree load on o–v1. Thus a physical signal at this edge still needs a newly derived subtree load, or, under nonzero background load, a change to the shared response parameter. The two incompatible chart weights supply neither.

## Three recorded futures after the same source transition

The original nine-tree certificate entry 1 includes all 41 historically selected normalization paths. Three of them record the actual incidence transition [257,63,455] to [257,63,199], which is the same C removal at v8. The fourth listed row uses that after-state as the start of its own original invocation.

| Archived row, zero based | Context at that state | Retained root target | Remaining moves | First B(v7)=1 among those moves |
|---|---|---:|---:|---:|
| 2 | Already running | 1 | 8 | never |
| 29 | Already running | 2 | 32 | 26 |
| 31 | Already running | 2 | 32 | 26 |
| 33 | Fresh caller | 2 | 10 | 1 |

The two 32-move suffixes are literally equal. With row 33 they also share the complete target profile, while their next writes differ. Thus the stored target separates the original pair but cannot account for all these exact continuations without execution context. Any deterministic implementation that represents these three distinct futures from the same post-state must distinguish at least three control contexts. This is a finite statement about the archived paths and their remaining edits. For just the eventual receiver bit on these four rows, the two old high-target continuations give the same answer as the fresh one. Move counts do not give physical durations.

[Exact V498 and chronology replay](evidence/routed_grade/metric.json) · [Job and source readback](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/44926899349) · [Original V498 function](https://github.com/proteinfoldingengine/WetLabEngine/blob/1433a1c54b1696d57e6291c59148e878cd825afa/Tmp/TOE/v498_retained_geometry_formal_report_package/v498_retained_geometry_proof.py#L294)
