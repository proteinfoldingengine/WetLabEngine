# A11.X56 scope — colored graph guards without the anchor-edge product

Status: frozen analytical scope. Parent 2fd7531f3c86df2d9e289b0bc299c0a532ffeee2 on research/uqcf-overlapping-guard-exchange. No numerical execution or numbered implementation campaign.

## Objective and disclosed reasoning

Remove X55's requirement that every outside graph edge appear with every anchor. Let each anchor a in A={0,1,2,3} have its own ACTUAL simple outside graph Gamma_a. Only root types {a} union e with e in E(Gamma_a) exist; no missing anchor-edge type may be cloned or added.

The candidate guard condition is
vc(union_(a in J) Gamma_a) > |J| for every nonempty J subset A.
The union here is the graph with the union of ACTUAL edge sets. This appears equivalent to: A is the only role hitting set of size at most four, and every role footprint of size at most four other than A is avoided by an actual type. Given a footprint F, put J=A minus F and X=F intersect R; then |X|<=|J|, so an edge from some Gamma_a, a in J, misses X. Conversely a violating vertex cover gives a second role cover of size at most four.

Retain four ACTUAL relay types, obtained from disjoint outside edges e_u,e_v: e_u belongs to Gamma_1 and Gamma_3; e_v belongs to Gamma_0 and Gamma_2. A compatible labeling is fixed BEFORE defining endpoint groups and successor exchange, with e_u={4,6}, e_v={5,7} and m-1 outside e_u. This explicit compatibility is not claimed to follow from the colored guard inequalities.

The X55 five-stage order seems to use only those four relay types plus the footprint lemma, so it should restrict to this incomplete anchor-edge family. Lower and upper protection must still use the same physical schedule and original copies.

A disclosed extremal candidate has six disjoint outside edges e_u,e_v,f0,f1,f2,f3 and graphs
Gamma_0={e_v,f0}, Gamma_2={e_v,f2}, Gamma_1={e_u,f1}, Gamma_3={e_u,f3}.
For singleton J the union matching has2edges; for pairs it has3 or4; for triples5; for all anchors6. Thus the proposed inequalities hold using only8distinct root types. Since every Gamma_a needs vertex-cover number at least2, at least8types are necessary within this colored condition. Compatible nonconsecutive labeling should give exact one-copy primitive count46t for every m>=16.

These are already-known candidate deductions disclosed before the proof, not prospective numerical discoveries.

## Required deliverable and checks

Prove the colored guard equivalence; exact-four endpoints; all physical pair witnesses including the sole per-column exceptional pair; shared five-stage upper/lower coexistence; arbitrary original positive copy floors including unequal saturation; every legal primitive, eligible continuation, reusable parallel columns, finite progress and exact labelled destination restoration. Derive the global incidence minimum and verify the8type/46t control symbolically.

Restrict any necessity claim to the declared footprint condition or specified singleton schedule. Native connectivity was already known. Do not claim arbitrary colored families, automatically compatible relays, every preassigned cyclic order, multiple exceptional pairs, universal mixed/directed/higher-target/nested repair, or a new physical result.

Freeze the exact candidate before fresh whole-argument review. Preserve earlier failed constructions and source history. Update the four reports only after attributable acceptance, obtain separate publication review and verify immutable bytes, full repository diff and live branch. Certified v16.54/v16.55, integration and original evidence remain unchanged. Separate efficiency runner/fixture/benchmark work remains unstarted; no numerical job, simulation or benchmark is authorized.
