# Which other views retain a single pruning loss?

In the project's finite rooted trees, the set of views that retain a nonzero loss component can be read directly from the original incidence relation. Each of those views already fixes its amplitude from its own pre-event source. This extends the calculation in [COMMON_FIELD.md](COMMON_FIELD.md) to arbitrary finite size and arbitrary numbers of holders.

## Premises

1. **INHERITED.** All views contain the same root and are ancestor-closed subsets of one finite rooted tree X. Source pushforward P sends a vertex charge to the nearest retained ancestor. Inclusion I extends charges by zeros. Use the one-edge, unit-conductance Green inverse on balanced sources with potentials modulo constants. These are the operations of FCV P2/P4/P6, v16.22 T1 and v16.23 O1–O4.
2. **INHERITED for a v16.26 atom; SUPPLIED for its actual occurrence.** In one indexed view M delete a single nonroot leaf h of that view, with parent g, obtaining E. All other indexed views persist and their union with E equals the old union U. The vertex h may have descendants elsewhere in X. The argument also applies to a proper retained union U inside X.
3. **SUPPLIED when identifying the coefficient from another view.** The pre-event source on M and a persisting holder V are compatible on their literal intersection. Signed rational grades are sufficient. For the global invariance statement below, begin with a jointly realizable source or response family on U and perform just the specified passive comparison on M. Actual physical readout and any active state update are open.

## The loss and its complete set of holders

Let q=x_M(h) and orient source loss as old minus reconstructed coarse source. Write

    D x_M = (id_M − I_EM P_ME) x_M,
    d = I_MX D x_M = q (δ_h − δ_g).

For any post-event view V, including E, its projection and its Green potential in the root-zero gauge obey

    P_XV d = q (δ_h − δ_g)    when h belongs to V,
    P_XV d = 0                otherwise.
    (T_V P_XV d)(z) = q · 1[h is an ancestor of z],  z in V,

where h counts as its own ancestor. In the first line the two deltas on the right live in V. This is a statement about the component of the old source discarded by M. If q=0 every projected source and response is zero. For q≠0 the set of nonzero holders is exactly {V : h∈V}. Membership is determined by the cover, with no selection of a receiving index. Union preservation guarantees at least one holder distinct from the edited index. Uniqueness requires that precisely one other index retains h. With several holders, all retain the same oriented component.

**Proof.** Deleting h moves its full grade to g in the old description, yielding the displayed difference after zero extension. If V contains h, ancestor closure includes g. Their two separate charges survive. If V lacks h, h and its parent have the same nearest retained ancestor, so their charges cancel. For the Green formula take the function equal to q throughout the retained subtree at h and zero elsewhere. On a unit tree its only nonzero edge difference is q across g–h. Applying the Laplacian gives +q at h and −q at g. If h is absent, ancestor closure also excludes all its descendants and the potential is zero. Root-zero normalization and invertibility finish the proof.

## The amplitude was available in every holder's old source

Fix another V containing h, and J=M∩V. It contains both g and h. Since h is a leaf of M, h is a leaf of J. Consequently

    q = (P_MJ x_M)(h) = (P_VJ x_V)(h)
      = sum of x_V(z) over z in V descended from h.

The first equality uses that the fiber of h in M is the singleton {h}; the middle one uses the stated overlap compatibility. The last fiber is the entire retained subtree of V at h, including h itself. No transfer from M into V is needed to determine this number from the mathematical data. Whether a physical system can read its own subtree total is a separate question. If the nonroot edge is driven by another law, incidence alone does not establish that law. With signed grades the total can be zero even when the site h is present, or negative in the stated orientation.

## What a passive update preserves

Suppose an old source x_U realizes the whole cover. Push x_M to E and leave the other sources as they were. Functoriality makes the old x_U a valid realization of the new data. Since the union is U in both cases, v16.23 O2/O3 uniqueness gives the very same reconstructed source on U. The analogous assertion for an initially compatible family of **response classes** follows by restricting M's old response to E, leaving the others fixed, and applying O4. If response classes come from grades by subtracting the total at the common root, use the original balanced-source naturality. Independent arithmetic-mean recentering of raw marginals need not commute with pushforward. The unique glued object is on U. Outside a proper U, extension to all of X can have additional freedom.

Thus this native passive operation has an exact answer to two different questions. Other views containing h retain the complete lost edge mode. Their pre-event data already determine it and their unchanged local states do not record that M deleted h. A physical, newly accessible consequence would require an actual update or a local readout that distinguishes whether the deletion occurred.

## Prior result and present extension

The project had already proved signed source gluing, the restriction of subtree totals and unchanged-union invariance in v16.23 O2/O3. O4 proves gluing of response classes. FCV already supplies the loss projector and original Green comparison. This note applies those results to identify exactly which other indices see a single atom's discarded mode, its complete unit-tree potential, and the coefficient that was already present at each holder. No general novelty or experimental detection claim is made.

The exact check in [check_loss_support.py](check_loss_support.py) exhausts 17 unlabelled rooted tree shapes through five vertices, 1,518 selections of pre-event view, deleted leaf and comparison view, and 5,297 independent source-basis columns. Of these selections, 752 retain h and 766 lose it in the comparison view. All 752 subtree-total compatibility rows reproduce the asserted coefficient. The code also tests a proper union with two distinct extensions, an unchanged signed glued field, and a mean-centering counterexample. On the chain o–h–w with raw grade (1,1,1), mean-centering on the whole tree gives zero, while pushing first to (o,h) yields raw grade (1,2) and local mean-centering gives an edge drop of 1/2. For a fixed view only adding a constant to the potential is a gauge change. A unit balanced source dipole on one edge changes its drop by one. The finite replay checks the implementation; the argument above gives the general result.
