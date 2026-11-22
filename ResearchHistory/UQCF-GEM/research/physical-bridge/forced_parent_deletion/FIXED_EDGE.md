# Fixed-port test of the archived source-leaf handoff

**Result.** The three v16.48 traces contain a conditional relay of the original grade from C to A. In the model's unit-conductance tree response, the newly held edge has potential difference g9. The chart that already held the edge has exactly the same potential difference before and after C acquires it. Adding or removing this pendant edge produces zero change in the linear coupling among all previously shared sites. The original repair uses the holder's address to release a leaf. Its computation takes only support data. Physical readout, gravitational units and a spacetime correspondence remain open.

## Which field is being tested

Use the v16.22 common-ancestor Green matrix in root gauge, equivalently the inverse grounded unit-tree Laplacian. For an oriented edge from parent p(v) to child v, summing the vertex equations over its subtree gives

    F_v = φ(v) − φ(p(v)) = Σ_{u in subtree(v)} g_u.

The grounded root balances the nonroot loads. Adding a constant to all potentials leaves every F unchanged. P1 projects omitted mass to its nearest retained ancestor. On any edge present in a prefix-closed chart, summing the projected source over its retained subtree recovers the same full-tree subtree sum. At leaf 9 this gives F9 = g9 whenever the chart carries the original leaf amount. F is a model potential difference. Its physical scale and coupling are unspecified.

The inputs are the actual v16.48 archived directed cases 178, 184 and 190, whose common −D9,+C9 prefix was previously independently reviewed. W1 fixes the grades on unedited charts and W2 requires compatible chart marginals at each state. They allow the underlying complete source to vary between states where the unedited views cannot distinguish it. The coherent initial source is supplied. These assumptions associate a grade to a support-only program.

## Positive local response and the existing-edge control

B retains leaf 9 across C's gain. W1/W2 and the earlier D-to-B overlap fix B's grade there to its initial amount g9. After the gain, C and B agree there. Take the two strictly positive inputs g=2 everywhere and g'=g+(δ9−δ0)/2. The model potential differences across B's edge are 2 and 5/2 both immediately before and immediately after C gains it. C can represent these same two numbers on its expanded carrier. Its prior carrier has no such edge. The difference between the preparations is 1/2 on this edge. The event-induced change in that contrast, measured at B, is zero. For the root-to-leaf balanced drive, every old-port potential difference on pre-gain C has zero response under the fixed-ambient projection. The new edge has normalized Dirichlet term F9²/2, giving 2 and 25/8. Zero and signed controls give (drop, term) of (0,0) and (−1,1/2). No chart visibility assumption makes the potential or these quadratic quantities physically observable.

## Geometry at the previously retained sites

Write L for the *full*, ungrounded Laplacian of the smaller chart and e for the coordinate vector of the attachment vertex. In old-site order followed by the new leaf, the larger unit-tree Laplacian is

    Lplus = [[L + eeᵀ, −e], [−eᵀ, 1]].

Eliminating the leaf from the field equations gives L as the old-site operator, exactly. The corresponding source on the old vertices is x_old + e x_leaf, the P1 pushforward. On a floating network one uses a balanced injected load or takes the grounded root as reference. Thus all effective resistances between old sites and the entire response matrix to probes on them are identical. Loads that change freely need not give identical realized potentials. Susceptibility is compared at the same probe.

Any extension between finite connected prefix-closed charts of one fixed unit tree consists of such pendant additions in ancestor order. Repeated elimination proves the fixed-port result on their common retained chart, also when different branches are gained and lost. This argument permits no inference to changing underlying weights, additional independent links, or a new law for the kernel. A candidate gravity mechanism expressed as a change in static coupling between existing sites must supply some operation outside this restriction of a fixed tree. A change in source strengths is a distinct mechanism and must have a source-dependent generating rule.

For the three actual windows, native grounded Green matrices and independently assembled Laplacians agreed in exact arithmetic. All 66 unordered old-port pair comparisons passed, counting each donor and recipient chart in each execution. The per-case totals are 24, 24 and 18. Projecting a basis of balanced loads also reproduced the source term after elimination.

## Which field changes are forced when grades may drift

Let U be the union of the unchanged chart carriers at C's gain. A P1 marginal on a rooted chart of fixed shape is equivalently specified by the total mass and the subtree sums at every retained nonroot site. The inverse subtracts child subtree sums from a vertex's subtree sum, using the total at the root. W1 therefore fixes the total and every F_v with v in U. Conversely, total and all full-tree subtree sums determine a unique rational full source. Varying any omitted F_v independently yields another compatible family satisfying W1/W2 on this edit. Positivity can restrict the magnitude near the boundary. The rank statement concerns formal rational variations, with small variations also possible at strictly positive sources.

The exact unrestricted increment ranks at C's gain were 3, 4 and 2. The free edges, by child vertex, were {4,6,7}, {3,4,5,6} and {4,6}, respectively. Edge 9 belongs to U in every case. The checker independently builds W1 constraint matrices by applying the native P1 operation to each source basis vector, obtains the exact rational nullspaces, and maps them to edge gradients.

For an explicit test, start with all source entries 2. One continuation keeps the full ambient source fixed. A second changes it at the C gain by −(δ4−δ3)−(δ6−δ2), and then holds it fixed. Every unedited chart at the switch has identical grades in the two histories. Both sources are strictly positive. Only the drops at 4 and 6 change, each by −1. The total ambient quadratic energy changes by 0 or −3. C's total quadratic energy changes by +2 or −1 in the same support event, although C gains exactly g9=2 in both. The model permits opposite signs for the total energy change. Counting the energy term at the newly available edge alone cannot establish a unique total field-energy impulse.

## What the original repair actually reads next

The original outer-star recoloring calls support and obtains C as holder at state 8. It writes +A9 and then −C9. The same support read subsequently gives A. The pinned producer's structural return matches the archived path with this instrumentation. No grade, potential, or energy is passed to the recoloring. C and A overlap at leaf 9 for one state, so W1/W2 force A(9)=g9 through the C release. C's root grade returns to g0+g10+g9. This is a relay beyond the previously reviewed C gain.

At the next edit, +A1, A is the only chart holding 9. All unchanged charts then send δ9−δ0 to zero under P1. Two compatible histories with the same original all-2 source can have A(9)=2 or 5/2 at state 11; both yield exactly the same structural actions. The checker verifies these positive histories through the rest of each actual trace and computes the W1/W2 nullspace on the prefix. This identifies the first loss of amplitude protection after the A gain. Support-address use by the controller leaves the grade magnitude unconsumed in the inspected caller.

## Reproduction and limits

The [protocol](FIXED_EDGE_PROTOCOL.md) disclosed the already known exploratory observations. The [fixed-port addendum](FIXED_EDGE_PROTOCOL_ADDENDUM.md) recorded the analytical Schur prediction before its numerical verification. The three matching runs share one branch of the repair algorithm. This is a test of their proposed field signature and a general fixed-tree identity, without an experimental measurement. See [geometry outputs](evidence/fixed_edge/geometry.json), [relay outputs](evidence/fixed_edge/relay.json), [field checker](check_fixed_edge.py) and [relay checker](check_grade_relay.py).
