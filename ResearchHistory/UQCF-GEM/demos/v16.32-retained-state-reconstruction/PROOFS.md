# v16.32 — Pre-adjudication proof ledger

R1. The map Y -> tau is generally many-to-one unless proved otherwise: tau_v records a minimum child-cover cardinality, not the full child-to-view incidence family. This observation motivates the test but is not a proof of a collision in the admitted same-interval domain.

R2. h is a deterministic function of tau, so adding h cannot resolve a tau collision.

R3. v16.31 component values reconstruct tau coordinatewise. Therefore component values alone cannot contain more state information than the local functions from which they are derived unless their labeled coordinate arrangement carries additional earned information. The campaign must type that arrangement precisely and must not smuggle the deletion mask into it.

R4. Predecessor relations are properties of the fixed endpoint interval, not of which reachable state has occurred. They constrain admissibility but, held fixed across states in one interval, cannot by themselves distinguish two states.

R5. Consequently the first serious possibility is that all v16.31 value-level closure data remain noninjective. This is only a conditional argument: a labeled component evaluation may still distinguish states even when tau agrees. The executable search must adjudicate the actual typed signature.

R6. If two distinct legal states have identical complete declared signature, no inverse from that signature to retained cover state exists on the stated class. One admissible exact witness refutes universal reconstructivity.

No physical conclusion follows from mathematical noninjectivity.

## R7 — explicit noninjectivity theorem

Take the rooted tree X={0,1,2} with parent(1)=parent(2)=0 and two indexed views. Compare

Y=((0,1),(0,1,2)) and Y'=((0),(0,1,2)).

Both are legal root-containing prefix-closed covers of the same union X and occur in the same endpoint interval with initial Y and final Y'. At the root, one view already contains both children in either state, so the minimum number of views covering {1,2} is one. Leaves have local count zero. Hence both states have tau=(1,0,0) and h=1.

The v16.31 normalized component values are functions of these local count values; for this interval their declared value-level signature is therefore identical as well. Yet the indexed retained covers are distinct because child 1 is present in view 0 in Y and absent in view 0 in Y'. Thus the frozen closed-data map is not injective.

This witness generalizes: whenever another retained view already realizes every minimum child cover relevant to a redundant incidence, adding or deleting that redundant incidence can leave all minimum-cover cardinalities unchanged. Therefore no inverse from the declared value-level closure data to indexed retained incidence can exist on the full admitted category.

## R8 — exact missing information

The collision differs only in labeled retained incidence: whether (view 0,node 1) is present. Predecessor relations are fixed by the endpoint and do not distinguish the two states. h is determined by tau. Component values reconstruct tau and likewise do not distinguish them.

Any datum guaranteed to resolve every such collision must distinguish at least these redundant labeled incidences. The full labeled view-node incidence relation is sufficient but is equivalent to the retained cover state being reconstructed, so adding it would make injectivity tautological. v16.32 therefore does not promote it to a new invariant. The scientifically correct result is NONINJECTIVE with the missing information identified as redundant labeled incidence identity.
