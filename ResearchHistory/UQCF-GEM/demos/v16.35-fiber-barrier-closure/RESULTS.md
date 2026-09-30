# v16.35 results

The disconnected q-fiber components found in v16.33 have positive exact combinatorial excursion barriers.

On the complete declared four-vertex/up-to-three-view cover universe, exact minimax graph search found **18 pairs of q-equivalent retained states** for which every legal one-incidence path must leave the endpoint q value. The independent verifier rebuilt the full cover graph for each published record and recomputed all 18 barriers exactly.

Barrier coordinates are integer summaries of q excursion:
- B1: minimum possible maximum L1 deviation from endpoint q;
- Binf: minimum possible maximum coordinate deviation;
- Bs: minimum possible maximum number of changed q coordinates.

These are not energies, actions, times or geometric distances.

Scientific GREEN: run **36656856899**, execution SHA `696d58fd0b9ba3780749a1c3ad7a7213c6edca95`. Inherited v16.32-v16.34 regressions passed.

The original exact implementation was computationally inefficient because it rebuilt the graph per endpoint pair. It was replaced without changing the universe or definitions by a graph-once exact minimax implementation.
