# Which retained view shares the field component lost in pruning?

On the anchored five-vertex example, the two specified deletions isolate a source component with an exact direction and amplitude. Its projection into the unchanged view C is zero at the leaf step. At the parent step it is `m(δ_p−δ_o)`, with `m=3` for unit counting. The same component is present in exactly one other endpoint view. The two histories exchange that view's identity. Ordinary restriction leaves C's own total field unchanged throughout.

## Preparation and premises

Use the tree with edges `o–p, p–l, p–w, o–d` and the initial label sets `o:ABC, p:ABC, l:AB, w:C, d:A`. A view consists of the sites carrying its label. Supply this preparation and the occurrence of **two v16.26 deletion atoms**. The archive uniquely forces the next deletion to be `−x(p)` after `−x(l)` for x=A or B. All references to order below concern these two edits. No elapsed time is assigned.

| Stage | A view | B view | C view |
|---|---|---|---|
| Initial | o,p,l,d | o,p,l | o,p,w |
| After A leaf | o,p,d | o,p,l | o,p,w |
| After B leaf | o,p,l,d | o,p | o,p,w |
| After A parent | o,d | o,p,l | o,p,w |
| After B parent | o,p,l,d | o | o,p,w |

Use the original finite-tree maps. For coarse retained E inside M, write `P_ME` for the nearest-retained-ancestor pushforward of a source and `I_EM` for literal inclusion by zeros. The Green map `T_Y` takes balanced signed sources to unweighted potentials modulo constants. Use root-zero representatives and orient every potential drop as child minus parent. In this category `R_XY T_X = T_Y P_XY`, and a local drive has extension `T_X I_YX = H_YX T_Y`. Source data and response classes each have their own overlap condition. These are inherited mathematical operations. An actual episode, its grade interpretation, and physical use of a response remain empirical or model-identification inputs.

## 1. The deleted edge supplies the candidate mode

For a single deleted leaf h of the pre-event view M with retained parent g, the old source decomposes into its reconstructed coarse part and the lost part

    D x = (id_M − I_EM P_ME) x = x(h) (δ_h − δ_g).

Indeed P adds x(h) to g and fixes every other retained coefficient. The signed residual has sum zero, even when x itself has nonzero total. Subtracting a balancing charge at o leaves the residual unchanged. The sign above denotes the old component omitted by reconstruction. The reconstructed coarse source minus the old source has the opposite sign.

Embed this residual into the ambient tree X by literal inclusion from M, then project to each endpoint view. At the first deletion C sends both l and p to p, so C's projected residual is zero for every coefficient. At the second deletion p is a leaf of the selected middle view M. Its overlap with C is precisely {o,p}. Write the unchanged C source on (o,p,w) as (b,u,v). Compatibility of the two middle sources on this overlap gives `x_M(p)=u+v=m`. The calculation allows signed rational sources and uses neither majority nor positivity. For m=0 the parent residual vanishes. For m≠0 the direction is fixed and the sign follows the grade.

Thus the second embedded residual in ambient order (o,p,l,w,d) is (−m,m,0,0,0) in both histories. Its unweighted Green potential is (0,m,m,m,0). Applying the original comparison identity gives the following complete local restrictions of that **one lost component**.

| Parent deletion | A potential of component | B potential of component | C potential of component |
|---|---|---|---|
| A | (0,0) | (0,m,m) | (0,m,m) |
| B | (0,m,m,0) | (0) | (0,m,m) |

The addresses follow from the retained maps. An endpoint that loses p pushes its positive charge back to o and cancels the dipole. The other endpoint retains both charges. For the fixed ambient unit count the unchanged C grade is (2,2,1), the first coefficient is 1, and the parent coefficient is 3. More generally agreement on the middle overlap already fixes the parent coefficient from C even when signed completions differ between histories. The table follows linearly. A and B are indexed mathematical views. This alone supplies no physical read operation for an occupant.

## 2. Passive field and shared measurement

For the fixed-ambient preparation, take the response of the projected grade balanced by its total at o. On a unit tree the child-minus-parent potential on an edge equals the sum of the balanced sources in the child's subtree. This follows by summing the Laplacian over that subtree. Hence the root-zero C field is (0,m,m+v) in both histories. For counting this is (0,3,4) before, between and after the deletions. The contribution (0,m,m) occupies an edge difference already present at C. Adding it again as a new C excitation would require a separate update law. Reversing the sign of the residual leaves the same distinction between decomposition and physical change.

On the common A sites K={o,d}, the counting potential difference is also unchanged, equal to 1. For any nonnegative ambient grade with the same C marginal, its value is the ambient amount at d, ranging over [0,b] in either history. For a balanced drive of h units from o to d, a measurement using these same two sites reads `x(d)+h` in either history for matched x(d). This follows from the tree equation or P6. The earlier A-root counting grades of 4 and 1 therefore coexist with identical passive shared-site field readings. Other probes or dynamics would require their own analysis.

## 3. What a local change obliges other views to do

Original v16.23 O4 permits a joint potential exactly when the local classes agree on their intersection. Consider a fixed C increment expressed by its edge differences (s,t) on op and pw. Its root-zero class is (0,s,s+t), and the balanced C source for it is (−s,s−t,t). If A's class is held fixed, O4 permits this increment exactly when it restricts to zero on J=A∩C. Equivalently the source pushes to zero on J, by naturality and invertibility of T_J. The dimension is |C|−|J| because restriction onto the potential classes of J is surjective.

| Stage | A∩C | Dimension with A fixed | Other views obliged to match any nonzero op change under full joint compatibility |
|---|---|---:|---|
| Initial or either leaf step | o,p | 1 | A and B |
| After A parent deletion | o | 2 | B |
| After B parent deletion | o,p | 1 | A |

For the same C unit drive `δ_p−δ_o`, O4 requires any other view retaining p to take exactly the same +1 on its op edge. A view that loses p can remain unchanged. Private-edge variations of a freely adjusting view are generally underdetermined by O4. Literal injection of that one drive from C into X fixes a particular extension with ambient potential (0,1,1,1,0), which gives the first table with m=1. The computed pruning residual has exactly this direction whenever m≠0. No externally chosen pulse is needed to identify the component. Realizing a new pulse or reading its availability would need an operation of its own.

With **both** A and B held fixed, the unit op drive fails in every stage. With both free, its fixed ambient extension succeeds in every stage. The pw control `δ_w−δ_p` produces (0,0,1) on C and passes with A fixed everywhere. C's unchanged grade stays nonnegative under the unit op trial, changing from (2,2,1) to (1,3,1) if that trial is supplied. With A held fixed an exact local decision on this fixture requires distinguishing whether A retains p. One bit with that meaning is sufficient for every (s,t). An implementation seeing identical C state and identical request, with no source-dependent input, cannot return the two correct deterministic answers for s=1. O4 is a compatibility relation. In the inspected implementation the successful tuple or error goes to the caller. A locally accessible result is a separate requirement.

## Original-code replay and event-selection challenge

`check_common_field.py` calls the historical v16.26 atom and verifier, v16.22 root Laplacian and inverse, and v16.23 source, overlap and response operators. It also checks the algebra at zero baseline, independent gauge offsets, both controls, all three pairwise orders of gluing the full cover, nine signed grid drives per stage, the nine integer lifts of C=(2,2,1), and signed/fractional examples with m=2,0,−2,5/6. The matched common A-port sweep checks 90 responses. The two-view admissible grid counts are 9/9 after A parent, 3/9 after B parent and 3/9 before either parent. Allowing A to adjust admits all nine at every stage. The proof above gives the full rational-space result.

To test Grok's specific candidate for making the second event happen, `check_attached_contraction.py` invokes the original v16.52 and v16.53 normalizers. With profile [1,2] and the same default order ABC, both expand d first, both delete C at p, and both source branches reach the same endpoint. Source-dependent orders can select the matching deletion as the third edit after two expansions of d. All eight paths pass the original v16.52 path verifier with zero excursion, and all four standalone fixed-root controls stop. This genuine attached-child contraction does not select the required second deletion following the source edit on this fixture.

## Scope and source lineage

- **INHERITED in the finite category.** Ancestor pushforward, literal inclusion, the loss projector, Green comparison and O4 appear in the foundational closure proofs P2/P4/P6/P7, v16.22 T1 and v16.23 O4. The v16.26 engine and verifier supply the conditional two-deletion address rule. Unit ambient counting is an identified v16.24 representation.
- **DERIVED on this fixture.** The first residual is invisible in C's source projection. The second has coefficient m fixed by C and a unique other p-retaining endpoint. A fixed A clamp yields the stated C response subspaces. The full-cover test identifies which sharing obligation changes. Original procedures reproduce the displayed values.
- **SUPPLIED.** The preparation, actual occurrence and typing of both deletions, and compatible middle grade when a nonzero numerical residual is claimed. The unit counting preparation supplies the example value of three. Fixed ambient source is the declared passive comparison. Holding A fixed or trying a C pulse is specific to the intervention comparison.
- **OPEN.** Does an inherited event enact the two deletions, then expose or enact the lost component as a changed record owned by a distinct retained system? Does the realized dynamics turn this finite response into a measurable gravitational field? No clock, spacetime metric, dimensionful force or Einstein equation is derived here.

The v16.23 engine's `glue_response` (lines 82–86) accepts two already supplied fields and returns a union or raises an incompatibility error. Its `case` (lines 153–163) constructs matrices for certification. `test_gate.py` (lines 60–64) tests gauge independence of the returned tuple. The earlier `receiver_move_interface/RESULT.md` distinguishes global legality from readable local rejection. These inspected callers supply no physical clamp or receiver-owned response. The native-delivery status remains open.

The foundational producer `produce_certificates.py` constructs lost generators and the original aggregate (lines 12–22), computes projector differences and their Green images (43–48), and returns certificate fields (57–64). `lineage.py` returns the coarse aggregate (44–52). The verifier reconstructs the decomposition (202–223). These concrete callers identify where the lost mode is already computed and where the result goes. In this source path it is stored in a certificate. A write into a second view's next local state would require another operation.
