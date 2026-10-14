# Source-grade pruning has a canonical balance representation on discarded edges

Date: 2026-10-14 UTC. Inspected parent: `83026efa321ad148a9ce42151e1006e134d6b4ad`.

**Disposition: conditional pruning-to-balance representation derived; surviving-edge readout is null; native vertex-record acquisition remains open.** This is an analytical bridge from the inherited lineage retraction and extensive source pushforward to an edge balance equation. It uses their own carrier rather than identifying the source with the separately supplied five-node current fixture. The resulting edge chain is a mathematical representation of the grade change, not an established physical flow. No physical milestone or priority claim is made.

## 1. The input is inherited, with its original conditions

The inspected v15.56 files supply the following typed constructions:

| Input | Inspected source | Preserved boundary |
|---|---|---|
| A source event localized at a Genesis identity and full lineage address | source_binding.py | The certified binding is an input; localization does not imply amplitude or receiver access |
| A localized relative/extensive grade | retained_amplitude.py, using v13.26 | Relative retained grade is preserved; absolute observer stress-energy calibration is not supplied |
| Longest-retained-prefix retraction r from a lineage tree to a root-containing prefix-closed retained subset | pruning_morphism.py | The retained subset is supplied; this does not select or enact a pruning event |
| Coarse grade obtained by summing each retraction fiber | source_pushforward.py | This is the canonical measure pushforward for that map, not a derivation of an independently observed record |

The earlier uniform-pruning assessment explicitly left extensive amounts eligible even though surviving indexed view supports do not change. The balance/readout screen then identified which readouts can expose a source contrast without selecting all cycle currents. The present question is whether the inherited source pushforward gives a balance representation on the lineage carrier itself, and whether the obvious retained-edge interface can read it.

No five-node-to-lineage or quantum-site dictionary is introduced. Fix one Genesis component so that addresses from independent origins are not aliased. The finite rooted tree and grade are available only under the inherited representation and source-binding assumptions. Existing conditional source results are preserved, not rederived as native origin.

## 2. Definitions and exact current

Let T be a finite rooted prefix tree, with root o. Orient each tree edge toward the root: for every nonroot vertex v, write e_v=(v,parent(v)). Let B_T be the vertex-by-edge incidence matrix with -1 at the tail and +1 at the head. No edge length, rate, metric or duration is attached.

Let Z be a nonempty root-containing prefix-closed subset of T. Its inherited retraction r_Z sends x to its longest retained ancestor. Let mu be a real signed vertex grade on T; nonnegative grades form an important subcase. Write

    (A_Z mu)(z) = sum_{x : r_Z(x)=z} mu(x),  z in Z.

Thus A_Z is the inherited source pushforward. Write i_Z for zero-extension of vertex functions from Z to T. The change expressed on the original carrier is

    s_Z(mu) = i_Z A_Z mu - mu.

This has total sum zero. **mu and s_Z(mu) are different types:** mu is a localized extensive grade; s_Z is its change under a specified pruning. The new equation does not identify a physical source grade with a balance divergence by name alone. In particular, the current below has units of retained grade, not grade per physical time.

For v nonroot, let D_T(v) be its descendant subtree including v. Define the edge-chain coefficient

    F_Z(mu)(e_v) = 0                         if v is in Z,
                   sum_{x in D_T(v)} mu(x)  if v is not in Z.

### Proposition 1: exact balance and uniqueness

    B_T F_Z(mu) = i_Z A_Z mu - mu = s_Z(mu).

Moreover F_Z(mu) is the unique real edge vector on this oriented tree with that boundary.

Proof of existence. For a basis grade delta_x, the formula puts coefficient 1 along the unique ancestral path from x to r_Z(x), and 0 elsewhere. To check this, e_v belongs to that path exactly when x is a descendant of v and v is not retained. If v is retained, r_Z(x) cannot lie strictly above it. If v is not retained, prefix closure prevents any descendant of v from being retained, so every x in its subtree retracts above v. The boundary of the path telescopes to delta_{r_Z(x)}-delta_x. A surviving x gives an empty path. Linearity proves the identity for arbitrary signed grades. QED.

Proof of uniqueness. The incidence map of a finite tree has trivial edge kernel: if B_T f=0, at a leaf the only incident edge must have coefficient zero; remove that leaf and continue. Therefore two solutions with the same boundary are equal. QED.

An equivalent cut proof follows by summing the boundary over D_T(v). Its only outgoing edge is e_v, so

    -F_Z(mu)(e_v) = sum_{x in D_T(v)} s_Z(mu)(x).

If v is retained, retraction preserves that descendant region and the right side is zero. If v is removed, no vertex in that descendant region survives, so its coarse zero-extension vanishes and the formula above follows.

For mu>=0 all coefficients are nonnegative. A positive grade at a removed vertex produces a nonzero chain: its path to a retained ancestor has at least one edge, with no negative grades to cancel it. For signed grades, individual cut totals can cancel, so a nonzero grade somewhere in a pruned subtree alone does not imply a nonzero coefficient on its boundary edge. The exact signed formula remains valid. Nothing requires every proper pruning to affect a source that survives untouched.

This is standard tree-chain algebra applied to the inherited pruning map. Its uniqueness does not supply physical actuality, a transport law, or a receiver. It says what balance representation follows if the declared extensive pushforward is the comparison being made.

## 3. Composition follows without a clock or a path selector

Let W subset Z subset T be root-containing prefix trees. Use A_{T,Z}, A_{Z,W} and F_{T,Z}, F_{Z,W} to display their carriers. Let j_{Z,T} extend edge vectors on Z by zero to the edges of T. Because Z is prefix closed, each Z edge is the identical parent edge in T.

### Proposition 2: additive composition of the representing chains

    F_{T,W}(mu)
      = F_{T,Z}(mu) + j_{Z,T} F_{Z,W}(A_{T,Z} mu).

Proof. The inherited pushforward is functorial:

    A_{Z,W} A_{T,Z} = A_{T,W}.

Taking B_T of the proposed right side gives

    (i_Z A_{T,Z} mu - mu)
      + (i_W A_{Z,W} A_{T,Z} mu - i_Z A_{T,Z} mu)
      = i_W A_{T,W} mu - mu.

It therefore has the boundary of F_{T,W}(mu), and tree uniqueness proves equality. Equivalently each ancestral path is split at its nearest Z ancestor and concatenated. QED.

This is an exact statement about composed retained descriptions. It does not supply a microscopic chronology, force, speed or time parameter. A common rescaling mu->a mu multiplies s and F by the same a; no observer energy standard is selected.

## 4. The current is absent from every surviving edge

### Proposition 3: support and retained-edge obstruction

    F_Z(mu)|_{E(Z)} = 0

for every grade mu and every allowed Z. Equivalently, every nonzero coefficient lies on an edge whose child vertex is removed.

Proof. An edge of the prefix-closed retained tree has its child in Z. Its coefficient is zero by the exact formula. QED.

The assertion is stronger than a statement that an event might not occur. It holds for nontrivial grade changes and nonzero F. Even when a source is actually removed in the specified comparison, restricting this formal current to the surviving edges yields the same all-zero record for every source.

This also has an exact reading through the preceding balance/readout criterion. If all surviving edges are observed and all other edges are unobserved, the unobserved components are precisely the fibers r_Z^{-1}(z), one for each z in Z. Every such component has zero total s_Z(mu), because its original grade is replaced by the same total at its retained ancestor. Thus these sources have no source contrast across the surviving-edge interface. Here the tree has no cycle ambiguity at all; the readout still vanishes.

The rejected candidate is specifically **retaining only the surviving edge coordinates of this balance representation as the receiver record**. The result does not forbid retaining an earlier edge record, storing a path trace, measuring a vertex amount, or using another justified interaction. None of those channels is supplied by restricting F to E(Z). Extending the record into discarded edges would require an explicit retention/access construction.

## 5. A positive vertex-amount control, with matching atomic inputs

Take a six-vertex tree with root o, children u,v,c, a child a of u, and a child b of v. Fix the same pruning

    Z={o,u,v,c}

for both preparations, and let gamma>0. Declare the two fine grades

    mu0=gamma delta_a,     mu1=gamma delta_b.

These are analytical preparations on the inherited type of carrier, not newly established physical source events. They have the same total grade, the same Genesis component, the same named receiver u and the same retained subset. No source-dependent pruning selector is used.

Initially the atomic grade at u is zero in both. After pushforward,

    A_Z mu0 = gamma delta_u,
    A_Z mu1 = gamma delta_v.

Thus the formal coarse vertex amount at u is gamma versus zero. F_Z(mu0) has coefficient gamma only on a->u, and F_Z(mu1) only on b->v. Each current is nonzero and has the required signed endpoint change. Nevertheless their restrictions to the surviving edges u->o, v->o, c->o are both identically zero.

The change in a surviving vertex amount does not contradict the prior theorem that uniform ancestral pruning leaves surviving indexed incidence supports unchanged. Extensive grades and membership supports are different observables. The earlier assessment explicitly preserved this possibility; the new bridge derives its edge balance representation and locates the edge readout failure.

The initially matching atomic grades do NOT prove that two complete physical receiver inputs are matched. In the fine description the subtree/fiber totals at u already distinguish these two states. If a receiver initially has those totals, the answer is already available. If it has only the atomic value mu(u), the inspected construction does not derive how it later obtains the larger fiber total.

## 6. Grade preservation does not guarantee retained source-location memory

Continue the same two preparations to the same smaller retained tree

    W={o,c}.

Both coarse vertex fields now equal gamma delta_o. The retained graph still has the edge c->o; this is not a comparison on an empty graph. The composed formal currents are nonzero: the first follows a->u->o, the second b->v->o. Their restrictions to c->o are zero, and all final vertex AMOUNTS agree.

Therefore even full access to the final amount field would not recover which of these two source locations carried the grade. Total extensive grade survives exactly; location information in this amount channel does not. This is a claim about the aggregated amount field, not all possible retained provenance labels, event identities, quantum correlations or separate path records. Those richer records could distinguish the preparations if independently available.

More generally, after a specified pruning, equality of two final amount fields means their grade difference sums to zero on each retraction fiber. This elementary pushforward fact is a scope check, not a separate physical discovery or a new access mechanism. The current representation does not repair a lost distinction unless an appropriate part of it is actually retained and accessible.

## 7. Why a representation is not yet a receiver write

The key identity for any retained z is

    (A_Z mu)(z) = mu(r_Z^{-1}({z})).

The coarse atom z denotes an entire fine fiber. A changed numerical value at that coarse atom can arise purely from using the coarser observable, without physical grade moving along the representing path. In the positive control, the coarse u amount is the fine total over {u,a}; it is not the earlier fine atomic observable at {u}. The difference in what is being read must not be hidden behind the same vertex name.

The archived `source_pushforward.pushforward` takes the fine values, fine keys and coarse keys as explicit arguments, finds the nearest retained prefix for each supplied key, and sums its value there. This is a valid implementation of the described coarse representation on valid typed inputs. It does not identify a native receiver, a local acquisition process, a physical measurement of a deleted edge, or a persistent register receiving the sum. No archived module was imported or executed in this investigation.

Similarly, finite additivity fixes the sum once the coarse observable is identified with the inverse-image fiber. Finite additivity alone does not select Z or prove that a material receiver performs this identification. The source-origin/binding and grade premises remain intact; interpreting their mathematical pushforward as a physical signal would add a realization/access claim not present in the inspected files.

| Obligation | Result here |
|---|---|
| Bind the source grade to lineage identities | Inherited conditional construction preserved, with Genesis distinctions respected |
| Relate that carrier to a balance equation | Derived: B_T F_Z(mu)=i_Z A_Z mu-mu on the same tree |
| Select a metric, cost or current | Not needed for this representation: tree boundary determines F uniquely |
| Compose the representation under nested retention | Derived exactly by pushforward functoriality and tree uniqueness |
| Obtain a record by restricting F to surviving edges | Fails for every grade: all such coordinates are zero |
| Obtain a potentially distinguishing coarse vertex amount | Conditional positive example given; its physical creation/access is not derived |
| Preserve a source-location distinction under further pruning | Not automatic even with conserved total grade and nonzero representing currents |
| Select/enact pruning, acquire a retained record and justify its error contract | Open in this inspected route |

For the exact positive amount contrast, common positive scaling preserves zero versus nonzero. It does not supply measurement precision or an observer calibration. A different probabilistic receiver could qualify if its action, actual output and error contract were independently justified. No deterministic selection or guaranteed completion is made a new prerequisite.

## 8. Scientific consequence and next requirement

The balance representation now follows directly from the already-defined source-grade pruning comparison on its own carrier. This removes the need to insert the separate educational graph merely to write a balance equation. It does not turn that equation into a physical propagation law. The unique representing current is supported only on edges whose child vertex is removed, so the simple surviving-edge route cannot implement the preceding cut-readout idea.

A next candidate must supply an actual retained output: for example, an independently justified event that accumulates the relevant grade into an accessible surviving register, or that retains an appropriate record of the removed edge action. Those are research obligations, not mechanisms adopted by this note. It must also justify the actual retained subset or admissible family being used. Merely recomputing a fine fiber sum, calling a coarse coordinate a detector, or declaring the unique edge chain physically real does not meet the milestone.

Do not rerun the existing pushforward code to count this bridge as physical discovery, and do not repeat the elementary fiber-sum identity as a new mechanism. The scoped edge obstruction does not exclude every amount-based, changed-carrier, quantum or probabilistic interaction. It identifies the exact failed receiver interface while preserving the positive conditional amount channel.

**Native milestone: NOT ACHIEVED.** This is a conditional representation theorem and a precise retained-edge obstruction, using elementary finite-tree algebra. No scientific code execution, historical test-count increase, fundamental clock, inserted geometry, physical energy/force, gravitational fit, main merge or numbered-stage CLOSED/CERTIFIED status is claimed. Time remains pruning / ordered recoverability update. Eleven exact claim-bearing source texts are pinned for whole-argument independent review and separate publication auditing.
