# A9: exact renewal conditions at a one-unit-defective boundary

Status: frozen bounded analytical candidate for independent review. Parent scope: 27a18a94e499f3657b33d07b164e406533287a7a. A9_SCOPE.md defines the deliverable. This checkpoint does not close the general sequence-existence question.

## 1. Baseline and typed exchange

The accepted v16.54 GENERAL_PARENT_CONNECTIVITY.md Theorem D already proves arbitrary-arity target-three primitive connectivity through bounded element covers. This is not a new result of A9. Targets q>=4 are the active scope here.

Fix the original finite palette P, labelled roots and positive floors. Put L=q-1. Choose two distinct labels u,v and fix every background D_i subset P minus {u,v}. Fix which slots are active. Inactive roots are D_i; active roots are D_i union S_i with nonempty S_i subset {u,v}. All native floors apply. This is exactly A6's two-label fiber, now permitting macro endpoints at level L.

Let F be the inactive-root family, g=tau(F), and lambda_0=tau({D_i: all i}), computed on the background palette. An empty family has transversal zero; an auxiliary family containing an empty background has transversal infinity. Native inactive roots remain nonempty by their floors.

For an admissible tuple X put

    lambda_u(X)=tau({D_i: u is absent from X_i}),
    lambda_v(X)=tau({D_i: v is absent from X_i}).

The A6 formula, obtained by partitioning hitting sets according to their intersection with {u,v}, is

    tau(X)=min(lambda_0,1+lambda_u(X),1+lambda_v(X),2+g).

This accepted formula is repeated as a dependency with its precise conventions, not claimed anew. It is valid at defective as well as exact-target tuples.

## 2. Exact no-second-unit criterion for the saturation route

Assume the fiber contains an admissible X with tau(X)>=L. Then lambda_0>=L and g>=L-2=q-3, by the formula. Let S be the common role-saturated tuple: all active roots receive both u and v. This adds incidences only, so floors hold. For S,

    tau(S)=min(lambda_0,1+g).

Given any two admissible fiber tuples X,Y with tau>=L, expand X to S one incidence at a time, then contract S to Y. Each expansion state contains X; each contraction state contains Y. Every intermediate tuple is contained in S. Floors hold by containment of the corresponding endpoint at its labelled slot.

**Theorem R1.** This prescribed saturation route preserves tau>=q-1 if and only if

    g>=q-2.

Sufficiency follows from lambda_0>=L and 1+g>=L, and inclusion gives the same bound to every intermediate tuple. Necessity follows because the route visits S. In particular, if g=q-3, then tau(S)=q-2 EXACTLY: saturation spends a second unit relative to q. The assumption of an admissible lower endpoint rules out g<q-3.

This is necessity for the saturation route, not for all paths in the fiber. Section 5 gives an explicit legal fiber path when this condition fails.

When R1 holds, each path has tau at most max(tau(X),tau(Y)) as well, by endpoint containment in the respective half. It has finitely many incidence moves. Positive floors, repeated backgrounds and unequal floors do not change the argument.

## 3. Renewal rule and the missing global obligation

For a fiber with lambda_0>=L and g>=q-2, an admissible completed destination Y retains the lower guard exactly when

    lambda_u(Y)>=q-2 AND lambda_v(Y)>=q-2.

This follows from the four-term formula; its two constant terms are already at least L. A finite sequence of such fiber exchanges may use different pairs, backgrounds and active-slot unions at each boundary, provided each step recomputes its actual inactive family and checks R1 plus its actual destination residual conditions. The stages may remain at tau=q-1; restoration to exact q is not required at every macro boundary.

If the sequence starts and ends at exact q, concatenating the finite incidence realizations gives a tau>=q-1 primitive path. The accepted maximum-layer-removal theorem converts it into tau in {q-1,q} if any upward excursions occur. Its finite palette, labelled slots, positive floors and exact endpoint hypotheses are preserved. The dependency is invoked, not independently recertified here.

This is a defect-carrying renewal interface. It proves safety and finite completion of each supplied exchange and of a supplied finite chain. It does NOT prove that an eligible next exchange always exists, that a sequence can reach an arbitrary destination, or that choosing exchanges has a well-founded global progress measure. Those are still required for universal closure.

There is a sharp additional restriction in the critical case g=q-3: every state in that fiber has tau<=2+g=q-1. Thus exact q cannot be restored anywhere inside that fiber, even by a path different from saturation. Any exact-target renewal must change the fiber or use a different mechanism.

## 4. A reachable defective state with a genuinely disconnected fiber

Use the SAME fixed palette P={x,y,u,v}, four labelled roots, floor one at every root, and q=4. The exact-target tuple

    E=({x},{y},{u},{v})

has tau=4. Add x to root 2 and then delete y. This gives the defective tuple

    A=({x},{x},{u},{v})

through levels 3,3, within the one-unit band. Thus A is reachable from an exact-q endpoint in a target-feasible original carrier.

Fix the u,v fiber of A: inactive roots 1 and 2 are both {x}, and active roots 3 and 4 have empty backgrounds. Here g=1=q-3, lambda_0=infinity, and saturation gives

    S=({x},{x},{u,v},{u,v}), tau(S)=2=q-2.

Any lower-guard state in this fiber needs active transversal at least two. The only possibilities are the two opposite pure assignments

    A=({x},{x},{u},{v}),
    C=({x},{x},{v},{u}).

To justify exhaustion analytically: each active root is one of {u},{v},{u,v}. They need two hitting labels exactly when they are the disjoint singleton pair; every other choice has a one-label cover. There is no legal single-incidence move between the two lower states; changing either singleton first creates {u,v} or an inadmissible empty support. Thus the fiber's lower primitive graph is genuinely disconnected. This is a complete symbolic argument for that fiber, not a numerical enumeration campaign.

The full primitive graph nevertheless connects A to C with eight moves in the one-unit band. First change root 2 from {x} to {x,y} to {y}, restoring E. Swap roots 3 and 4 by adding v to root 3, adding u to root 4, deleting u from root 3 and deleting v from root 4. The fixed {x},{y} roots require two labels; the two active roots require one or two, so levels remain 3 or 4. Finally change root 2 from {y} to {x,y} to {x}, reaching C at level three.

No label or slot is added. Every support is nonempty, and every move toggles one incidence. The two initial moves have levels 3,4; the four swap moves have levels 3,3,3,4; the final two moves have levels 3,3. Including the original A, all levels lie in {3,4}. The escape changes an inactive background and leaves the frozen fiber before restoring exact protection.

This example is a mechanism diagnostic inside an already proved floor-one carrier. It does not establish new universal endpoint connectivity or a native barrier.

## 5. Saturation can fail even when another fiber path exists

Keep P={x,y,u,v}, q=4 and floor one, but use five labelled roots. Fix inactive roots 1 and 2 to {x}; make roots 3,4,5 active with empty backgrounds. Again g=1=q-3, so full saturation has tau=2. Take lower endpoints whose active supports are

    (u,u,v) and (v,v,u),

where a single symbol denotes its singleton support. Both tuples have tau=3. The following sequence stays within the fiber:

    (u,u,v)
    -> (u,{u,v},v)
    -> (u,v,v)
    -> (u,v,{u,v})
    -> (u,v,u)
    -> ({u,v},v,u)
    -> (v,v,u).

Each arrow is one active incidence addition or deletion. Every stage has at least one pure-u root and at least one pure-v root, so the active family requires exactly two hitting labels. The inactive family requires x, giving exact tau=3 throughout. Floors hold and all backgrounds and pair occupancy remain fixed.

These defective tuples also lie in a target-feasible carrier and are reachable from an exact-four endpoint: for the starting tuple, change inactive root 2 to {y} through {x,y}; roots {x},{y},{u},{u},{v} require four labels. Reversing returns to the start within {3,4}. The destination has the same property.

Thus g=q-3 prevents the common saturation route and prevents exact-target renewal inside the fiber, but it does not by itself prove lower-graph fiber disconnection. The four-root example and this five-root example distinguish those outcomes precisely. A candidate algorithm must track witnesses rather than infer a barrier from a failed saturation.

## 6. Critical witnesses and scientific conclusion

When g=q-3 and a lower endpoint exists, the lower residual inequalities have a useful exact form. For every minimum background transversal H of F, of size q-3, let

    E(H)={active i : H misses D_i}.

The lower bound tau>=q-1 holds exactly when EVERY such E(H) contains at least one pure-u root and at least one pure-v root. Indeed H together with u would be a forbidden size-(q-2) cover unless a pure-v root's background is missed; the symmetric cover H together with v needs a pure-u witness. Conversely any residual cover of size at most q-3 must have size exactly g and be a minimum transversal of F, so the two witness conditions exclude all forbidden one-role covers. Avoiding both roles is already excluded by invariant lambda_0>=q-1; using both roles costs at least 2+g=q-1.

In the four-root example E({x}) has only two active slots, so both witnesses are indispensable and no first move exists in the lower fiber. In the five-root example there are three slots: one pure-role witness can be installed while another protects the change. This is the exact source of renewed protection in the displayed path.

**A9 result:** common two-label saturation at a one-unit-defective boundary is safe exactly when the actual inactive family already supplies level q-2. In the critical case, renewal is a pure-role witness problem; saturation erases those witnesses, and some fibers are disconnected while others permit an interleaved handover.

This bounded criterion and diagnostic separation are the intended completed checkpoint. Universal higher-floor primitive connectivity, global eligible-exchange selection, q=4/floor-three accessibility, and full nested lifting remain OPEN. Native lifting requires the accepted child-interface and clearance hypotheses. No implementation certification, runtime bound, originality or physical-law claim is made. All arguments use the existing incidence carrier; no external design result is needed for this checkpoint.
