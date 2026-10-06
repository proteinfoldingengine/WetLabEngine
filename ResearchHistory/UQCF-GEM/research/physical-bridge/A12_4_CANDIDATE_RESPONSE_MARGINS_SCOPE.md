# A12.4 scope — candidate-centered exact response margins

Date: 2026-10-06 UTC.
Status: prospective analytical physics-bridge scope. No numerical execution, implementation, geometry, force law, energy, continuum, or numbered certification.

Native basis only. A12.1-A12.3 are comparison candidates and are not assumed accepted.

## Objective

Determine how much of the global target-four certificate structure is actually needed to decide the legality of ONE candidate incidence move.

For protected E with 3<=tau<=4:

For candidate Add(i,x), x notin E_i, define its lower shadow
    Sh_-(i,x)={{x,y}: y notin E_i, y!=x}
and margin
    A_E(i,x)=min_{K in Sh_-} W_E(K),
with A=+infinity if the shadow is empty.

Conjectured exact criterion:
    Add(i,x) legal iff A_E(i,x)>=2.

For candidate Del(i,x), x in E_i, define surviving-cover count
    D_E(i,x)=#{H: |H|<=4, C_E(H)=1, (E_i minus {x}) intersect H != empty}.

Conjectured exact criterion:
    Del(i,x) legal iff |E_i|-1>=f_i and D_E(i,x)>=1.

## Required results

1. Prove both iff criteria exactly.
2. Show these are candidate-centered projections of the global W/C fields, not new primitives.
3. Express one-step response R(e->f) as threshold crossing of f's candidate margin:
   - addition f crosses A from >=2 to <=1 under suppressing additions, or from <=1 to >=2 under facilitating deletions;
   - deletion f crosses D from >=1 to0 under suppressing deletions, or0 to>=1 under facilitating additions, with floor threshold included for same-root effects.
4. Prove covariance under root/label relabeling.
5. Characterize cross-root response as a change in a candidate-centered margin caused by another root.
6. Do not call A or D a physical potential, field strength, energy or distance.
7. Determine whether the scalar global summaries mu_-=min_K W(K) and N4=sum_H C(H) are sufficient for individual move legality. If not, provide exact counterexamples; if a clean proof is not found, leave this open rather than asserting it.
8. State the observer boundary precisely: a candidate-centered sufficient statistic is not yet an internally accessible observable. Internal accessibility requires a model-derived readout protocol.

## Physics-facing target

If proved, this is the first exact compression from the full relational state to a move-specific response state. It identifies what information is sufficient to predict whether one local change remains admissible, while preserving relabeling covariance.

Next question: can these candidate-centered margins themselves be reconstructed from bounded/local retained information, or is global access unavoidable?

No fundamental time; only ordered relational updates.
