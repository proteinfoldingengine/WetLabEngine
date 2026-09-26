# Matched completion -> polar connection: bounded verification plan

Pinned baseline: 8cf281ab1eb9cba2e2912abb5c12b043f215328d.
Retain all historical code and the corrected graph baseline unchanged.

Question: does the already archived ETL -> connected Pauli correlation -> raw
polar transport -> loop conjugacy observable chain expose hidden completion
information with initial one/two-body data held fixed?

The preceding diagonal parity fixture has C_ij=0 initially. It is NOT a
full-rank connection fixture and will not be regularized. Test that null first.
The v13.09 report supplies a cyclic chiral three-body operator and collective
Z source, but its directory contains report/summary checking rather than a
pinned generative seed. Build a separately labelled rational witness family,
NOT a numerical reproduction of its quoted results.

Freeze before evaluation: oriented cycle (0,1),(1,2),(2,0), c=1/20,
cos(theta)=3/5, sin(theta)=4/5, h in {-1/100,0,1/100}.
rho=(I + sum_edges c[(3/5)(XX+YY)+(4/5)(XY-YX)+ZZ]
        + h sum_cyclic (XY-YX)Z_spectator)/8.
Source P=Z0+Z1+Z2 is the archived source ray with explicit unit convention.
Observable Tr(O01 O12 O20), reference susceptibility d<(Z0+Z1+Z2)/3>.
Use raw polar factors, never a determinant flip, graph-weight change, or fit.

Proofs/checks: exact Pauli algebra, trace and PSD lower certificate; all initial
proper marginals equal; source commutation; exact derivative and polar jet;
independent numerical dense-state exponential and SVD finite differences;
independent local-frame rotations; same-state, identity-source, hidden-zero,
flat-loop trace-blind, source scale and singular-transport nulls. Change c,h,
and rational rotation in declared controls; no exclusion based on outcome.

Record a test-first failure, then exact and independent numeric tests. Publish
implementation, behavioural tests, results, report, CI step in one atomic
fast-forward commit on the existing research branch after checking its head.
Report local scope separately from full GitHub historical suite. No main merge.
No claim of provenance selecting a source or hidden state, history creating
h, scalar-lineage coupling, physical curvature, gravity, or novelty.
