# Exact universal core region and sharp reserved-label bypass

Status: analytical proof frozen before verification; independent reviews pending. See prospective scope for the full domain.

## Universal safe-region theorem

Let C_i be nonempty finite original core supports with3<=tau(C)<=4, and positive floors f_i<=|C_i|. Let Q range over ALL hidden completions on a disjoint nonempty palette T such that3<=tau(C union Q)<=4. Fix Q across updates. For candidate core D, write I_x(D)={i:x in D_i}. Empty root families have hitting number0; a family with an empty support has no finite cover.

Then D union Q is admissible for EVERY such Q if and only if:

1. |D_i|>=f_i for every root;
2. tau(D)<=4;
3. every nonempty I_x(D) is contained in I_y(C) for some y in P.

Condition3 equivalently says tau(C restricted to I_x(D))<=1, including empty footprints.

Necessity of1/2: Q empty is a permitted source completion. For3 suppose some footprint J=I_x(D) has tau(C_J)>=2. Put a single hidden u exactly on its complement J^c. The original completion has

tau(C+uJ^c)=min(tau(C),1+tau(C_J))>=3

and at most4. The identity follows by splitting covers according to whether they use u; it includes empty J^c. Source floors hold from C alone. But {x,u} covers D union Q, because x covers J and u covers its complement. If the complement is empty x alone suffices. Hence the candidate violates lower protection. This establishes necessity using an actual admitted source, not a hypothetical unprotected world.

Sufficiency: floors hold by1 and an at-most-four core cover exists by2. Suppose H were a hitting set of D union Q with at most two labels. For every core x in H having nonempty current footprint, replace it by an original y with I_x(D) subset I_y(C). Drop core labels with empty footprint; keep hidden labels unchanged. Every root hit by H is still hit in C union Q: hidden incidences are fixed, and each current core hit maps to an original core hit at the same root. Replacement cannot increase cardinality. This produces a source cover of at most two labels, contradicting its protected promise. Thus every candidate is in band3..4. This proof covers arbitrarily many hidden labels; enumeration of them is unnecessary.

## Paths and observation

Every core-only sequence whose configurations satisfy1-3 is uniformly safe over the SAME original full-completion fiber. Conversely every universally safe candidate satisfies these conditions. Under uniformly safe requests and core observation, equal histories do not discard a source completion: toggle effects and syntactic validity depend only on core, and optional NOOP is permitted in each world. Thus an adaptive controller cannot escape the criterion by learning a finer hidden class through these uniformly safe core-only actions. This uses the inherited projection induction, not hypothetical guard outcomes.

The criterion characterizes admissibility, not connectivity. A path still needs to exist. The supplied source C remains the reference in3 throughout; replacing it by an arbitrary current core would silently change the source fiber. The theorem does not derive physical access to C, floors, current core or the protected-band promise, nor enforce all requests or choose committed outcomes.

## Exact-repair application and no-spare obstruction

Use W of m>=1 roots with core{A}, two additional roots{B},{C}, and host h with{D,E}; original floors1,1,1,2 respectively. All five labels are distinct, hidden backgrounds are arbitrary protected completions, and the target exchanges A,D on W and h, fixing B,C,E and Q. Original tau(C)=4. The target is a palette permutation and thus has the same full tau as its own source.

With only these five active core labels, the original core is an isolated universally admissible node. Every deletion violates its saturated floor in the empty-Q world. Every syntactically valid addition puts an existing label in another block: its footprint then contains roots from disjoint original label blocks, so no original label covers it. The criterion supplies an admitted hidden witness violating lower protection. Additions within its original block are already present and hence not valid additions. This rules out EVERY first edit, including off-endpoint edits. NOOPs do not enable a departure. It is stronger than failure of one prescribed script, but only under this source fiber and palette.

Now supply a reserved core label w absent at every original root, distinct from T. Execute:

1. +w(h), -D(h).
2. Add D at EVERY root in W, in its supplied order.
3. Remove A at EVERY root in W, in its supplied order.
4. +A(h), -w(h).

Each nonempty label footprint lies within one original block: D moves to W only after leaving h; A moves to h only after leaving all W; w stays at h. Therefore3 holds. Floors hold by add-before-delete. Four core labels cover every slice: B,C and a host label, together with A until all D additions complete, then D. Hence1/2 hold and the universal criterion proves safety over every protected hidden completion. Q is untouched and the exact labelled destination is reached.

The batch order matters: interleaving removal of A at a transferred W root before D reaches every W root can split W into A-only and D-only roots, raising the empty-Q hitting number to5. We make no single-excess claim; peak total excess is max(1,m). Actual toggles total2m+4. The endpoint differs in2m+2 incidences. Since every valid uniformly safe first edit must add a previously unused label, and the exact endpoint contains no such incidence, at least two off-endpoint toggles are necessary. Thus2m+4 is the minimum uniformly safe committed length, even if more unused core labels are supplied. This is not an optimality claim for individual hidden worlds or broader native alphabets.

Every script core slice is distinct: host stages distinguish before D removal, the W transfer, and A insertion/cleanup; within W transfer the number of D presences plus A absences strictly increases. Therefore current core and the supplied static ordered template determine the next request and exact stopping condition, without acknowledgment or mutable phase. Arbitrary NOOPs repeat a slice; every committed move advances. Guarded and syntax-only relations agree restricted to this policy. No progress/fairness is derived. Hidden Q is fixed, so final core identifies each world's own exact endpoint despite not identifying Q.

## Scientific interpretation and inherited limits

The earlier fixed-family theorem is preserved: on F consisting of the B,C roots, a hidden common label remains present through this route. We do NOT prepare that predicate to become true. Instead the spare-label route reaches the intended exact repair destination without relying on that predicate or the earlier visible-buffer script. No hidden incidence is measured or changed.

The fresh-label and triangle/spectator buffer mechanisms are inherited; claiming their choreography as a new discovery would duplicate old work. The new analytical content is the exact universal safe-region criterion, valid for arbitrary original core overlaps in the declared3..4 domain, plus its sharp operational application over ALL original protected completions. The source palette, addresses, core observation, reserved-label absence and protected-band promise remain supplied native-interface premises. The spare is an explicitly stated combinatorial resource, not a derived physical mechanism or invented force.

This does not settle hidden-label operations, restricted correlated fibers, floors exceeding core sizes, unbounded root creation, broader bands or general exact-target connectivity. Broad C3/general C4 remain OPEN. No spacetime, fundamental time, dark-matter variable or GR derivation is introduced.
