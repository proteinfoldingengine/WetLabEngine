# Exact C3 ↔ nested-support star correspondence — analytical candidate

Date: 2026-10-11 UTC. Prospective scope frozen at `365d55c497d65f6003b5e7f8691438280e62c3fe`.
Status: **ANALYTICAL CANDIDATE / NOT INDEPENDENTLY VERIFIED OR CLOSED**. No new numerical campaign, Gemini mathematical acceptance or publication audit is claimed.

## Sources and typing

The v16.53 `NATIVE_ADMISSIBILITY.md` defines a finite ordered palette P, fixed root support P, nonempty nested child supports, parent hitting number h_v for immediate child supports, and one-label nonroot incidence toggles. It declares the four-child boundary (with earlier binary/ternary interfaces inherited) and allows intermediate native h to vary. The C3 `COUPLED_C3_SOURCE_ESCAPE_CLOSEOUT.md` defines indexed pair-root supports, original positive floors and the band 3<=tau<=4. `COUPLED_C3_EVENT_GRAMMAR_C4.md` already reconciles single-incidence event notation with A11; this result is more precise about the **nested tree carrier and its local hitting invariant**, but is not a physical origin claim.

## Proposition (scoped)

Fix m in {3,4}, ordered palette P and positive floors f_i. Let G_C3 be the directed graph with vertices all tuples S=(S_1,...,S_m) of subsets of P satisfying |S_i|>=f_i and 3<=tau(S)<=4, and an edge S->S' exactly when one incidence (i,x) is toggled and S' is also admitted.

Let G_star be the directed induced graph of depth-one ordered native stars with root support P, m indexed children with nonempty supports T_i subseteq P, restricted to |T_i|>=f_i and 3<=h_root(T)<=4. Its edges are native single-child incidence toggles with admitted endpoints.

Then F(S)=(P;S_1,...,S_m) is an exact labelled directed-graph isomorphism G_C3 -> G_star.

**Proof.** Every C3 vertex maps to a star because S_i subseteq P and positive f_i implies S_i is nonempty. Conversely any restricted star has a unique ordered child tuple S_i=T_i satisfying the same floors. By the two definitions, h_root(F(S)) is the minimum cardinality of a subset K of P meeting every child S_i, which is exactly tau(S). Hence the band predicates coincide and F is bijective on vertices.

A C3 edge changes one Boolean incidence (i,x) while fixing all others. Under F it changes exactly the label x in nonroot child i, preserves the fixed root P, and retains nesting because all child supports stay subsets of P. The target has the same positive floors and band by the preceding identity, so the star edge is legal. Conversely a native star edge in the induced restricted graph changes exactly one child incidence; applying F^{-1} yields the same C3 toggle and admitted target. F and F^{-1} preserve direction, index, label, sign and every intermediate state. QED.

If a *particular* hidden completion Q is fixed, apply the same map to its full root supports, with P the declared full palette. If only core edits are allowed, restrict both edge sets to that edit alphabet. If safety must hold for **every** originally protected Q, form the intersection of these fixed-Q relations under the common core projection, and preserve the original-footprint restriction on both sides. The bare v16.53 native admissibility relation does not automatically enforce either condition. In particular no graph-isomorphism assertion is made between the universally protected C3 graph and the **unrestricted** nested-star graph.

## Explicit controls and interpretation

1. **Band is an added restriction.** Three child supports all containing a common label have h_root=1 and are legal in unrestricted nested support but not in the C3 band. Thus an unrestricted v16.53 unit-excursion theorem cannot be imported as a C3 3-to-4-band theorem.
2. **Floor is an added restriction.** The native star's nonemptiness only requires size>=1, whereas C3 may demand f_i=2 or larger. Deleting a label from a size-two child to size one is natively nonempty but violates a C3 floor-two constraint.
3. **Indexed support is not reconstructed by h.** With four children `({a,b},{b,c},{a,c},{d,e,u})` and `({a,b},{b,c},{a,c},{d,e,v})`, both have h_root=3, but their labelled support states differ. The inherited swapped-*two*-residual-root discriminator would require three triangle children plus two residual children (m=5), so it is **outside this frozen four-child star theorem**. It remains an external native-reference gate, not evidence that this restricted star embedding solves the broader C3 record problem. v16.32 independently warns that minimum-cover values can forget redundant labelled incidence; its different category should not be conflated with this star.
4. **Arity boundary.** A star with five or more children is outside the accepted v16.53 four-child root scope. Replacing it with a binary/ternary grouping changes which immediate-child supports define h_root; it is not a free generalization.
5. **Actuality.** C3 NOOP is a possible resolution of a request and is not a native incidence edge. A path of allowed toggles is not a selected realized history; neither v16.53 nor this correspondence derives enforcement, retention or progress.

## What was and was not advanced

The result identifies an exact *mathematical* shared carrier for 3- and 4-root C3 instances, including the local hitting invariant and restricted move graph. This is stronger than merely sharing the notation A(i,x),D(i,x). It could allow already proven structural lemmas to be translated **only after** their additional hypotheses and path constraints are checked.

It does not produce a certified physical root reference, source-event-to-incidence binding, observer record, GR correspondence, new force or native success selector. Root/child indices are part of the supplied mathematical object. Simultaneous relabelling must transport the reference; a fixed-reference response needs an independently grounded reference identity.

## Verification gate

The finite universe, independent checker and rejecting controls are prospectively specified in `COUPLED_C3_STAR_CARRIER_SCOPE.md`. No implementation or numerical result is claimed here. Independent proof review and, if pursued as a certified checkpoint, complete numerical verification, separate publication audit, artifact preservation and immutable readback remain pending. **Do not mark CLOSED.**

Broad C3/C4-C6, native record origin, enforcement, actual selection and progress remain OPEN. Path A active, Path B closed; no fundamental time, geometry or dark matter introduced.
