# A two-label coverage constraint gives a sphere of four-chart states

At the root of the original v16.53 four-leaf model, take two named labels, four named nonempty chart supports, exact hitting number two, and the original one-incidence primitive. A label cannot cover all four charts. Thus at least one chart holds only label A and at least one holds only B. Encode A alone by −1, both labels by 0, and B alone by +1. Elementary moves change a coordinate one step. We attach a square when edits at two different charts are admissible in both orders with the same endpoint. A face denotes those two executable alternatives. Its interior is a mathematical realization. The program has discrete states.

## From three charts to four

More generally, on n such supports the union of the resulting cubical cells consists exactly of points of the cube with minimum −1 and maximum +1. Indeed a product cell contains only admissible corners precisely when one coordinate is fixed at each extreme. If one extreme lacks a fixed witness, choose a non-witness endpoint in every varying coordinate to obtain an inadmissible corner. The generalization assumes the same two-label rule for n ≥ 2. This run uses the original implementations for four children.

To identify the topology, subtract the mean of the coordinates and normalize to Euclidean length one. This maps the realization into the unit sphere in the (n−1)-dimensional zero-sum subspace. The inverse sends a unit zero-sum vector y to the vector with coordinates 2(y_i−min y)/(max y−min y)−1. These continuous inverse maps identify the space with the sphere of dimension n−2. The norm supplies a convenient proof of topology. It does not specify an intrinsic physical metric.

For three charts this is the prior subdivided hexagon with 12 states. For four it is a two-dimensional sphere with 50 vertices, 96 edges and 48 quadrilateral faces. Euler characteristic is 2. Holding chart four at 0 gives precisely the former 12-cycle. The two closed halves indexed by the sign of chart four have 24 faces each, with the cycle as their common boundary. It is a simple polygonal circle on a sphere, so each half is a disk. The winding around the earlier cycle can unwind by allowed square deformations when the fourth chart may change. Projection orthogonal to the cube diagonal gives a subdivided rhombic dodecahedron. The classical cube projection is illustrated by [Fukuda](https://www.cs.mcgill.ca/~fukuda/download/mathematica/Polyhedra/unfold_cubeprojections.pdf).

## Where the combinatorial curvature is

Every vertex link is a single cycle. Eight vertices have three incident squares and 42 have four. The eight are exactly the all-singleton assignments split 3 to 1. For the square complex the combinatorial contribution at each vertex is 1−degree/4, hence 1/4 at those eight states and zero elsewhere. With the additional metric choice of Euclidean squares, these are angle deficits of π/2 and zero respectively, totaling 4π. The interpretation by angles depends on the metric. The sphere describes possible holdings and commuting edits on a prepared interface.

## Which participants can certify a remote change?

For an attainable snapshot of a named group, count how many of the two required singleton types have yet to appear among the visible charts. If any chart is hidden, the observation forces a specified hidden chart to be a singleton exactly when this count equals the number of hidden charts. Each missing type needs a different hidden chart. Conversely, when there is a spare slot, assign the missing types to other hidden charts and give the specified one both labels. From a known initially double support at that address, a forced current singleton proves that a withdrawal occurred there.

In the four-chart case a single current row never forces a specified remote singleton by this rule. Two observed double supports force the two remaining charts to be opposite singletons, without fixing which holds which label. With three observers the projected states form the boundary of the three-cube, with 26 possible triples. With two observers all nine pairs occur, including double/double. These are mathematical group observations; the experiment supplies no native reader joining them.

## Historical and numerical checks

The four-child producer and independent verifier agreed on the hitting number of all 81 configurations. Every square passed the historical verifier with exact profile on both two-step routes across each diagonal. Edge incidences, every vertex link, both equator boundaries and every compatible completion of every nonempty proper observer subset were checked exhaustively. Replaying the original R-family normalizer on the 50 exact starts used 28 distinct exact edges. Every one of the 50 complete paths also entered the permitted one-unit excursion. The surface describes the exact subspace; the wider four-leaf rule admits all 81 configurations, whose cubical realization fills the four-cube. No archived traversal of an entire surface is claimed. Latest bot work on actual dispatch from a refreshed occupancy condition concerns a separate software operation.

Use Python 3 with the [historical v16.53 directory](https://github.com/proteinfoldingengine/WetLabEngine/tree/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary) as the argument. Producer and verifier Git blobs are 0501a1b32c0a660646ff95ecbb8a37a8f2e04b80 and 54e23706c170d0bb82c1b78161290145b6b99af7. This is a deterministic finite check and an analytic argument, without an independent model review of this new report.

```bash
set -euo pipefail
python -B four_surface.py "$DEMOS/v16.53-four-child-boundary" | diff - results.txt
```
