# Distributed role exchange: structural example and limits

These are symbolic constructions, not a numerical campaign.

## 1. A higher-floor exchange beyond a global permutation

Fix q>=3, h>=3 and N>=2. Use q-2 pairwise disjoint background blocks B_1,...,B_{q-2}, each of size h, together with disjoint sets D_U,D_V each of size h-1 and labels u,v outside all of them. The palette has k=qh labels. All r=q-2+2N root floors equal h, so sum_i a_i=h(q-2+2N)>k.

Keep one inactive root on each B_j. At source A use N active copies of D_U union {u} and N active copies of D_V union {v}. At destination C, change the first U-group root to D_U union {v}, and the first V-group root to D_V union {u}. Give BOTH roles to every other active root.

Every root meets its original floor: the source roots and two pure destination roots have size h, while the other destination roots have size h+1. Every active root changes, and their number 2N is unbounded.

Both endpoints are exact-q. At A the inactive block roots and one pure root from each group form q pairwise disjoint supports. At C the inactive blocks and the two swapped pure roots again do so. A hitting set consisting of u,v and one label from each B_j hits all roots at both endpoints, giving the matching upper bound q.

The common fiber has g=q-2 and lambda_0=q, because the backgrounds consist of q disjoint nonempty sets after deduplication: the B_j, D_U and D_V. Every minimum F-transversal misses all active backgrounds; the two pure destination roles satisfy T1's renewal test. Saturation has transversal exactly q-1. T2 therefore gives the full primitive unit-band exchange and returns exactly to C.

This change is not a global palette permutation or a root permutation: its multiset of root sizes changes, which either permutation preserves. The example's endpoints nevertheless belong to an already solved protected class. Its purpose is to demonstrate the broader exchange mechanism, not to claim a newly connected endpoint class from one family. It also does not claim that this family requires unbounded simultaneous endpoint departures; that necessity was proved for the separate row/column family.

## 2. Role occupancy must remain fixed

If a previously inactive root is allowed to acquire a role, the family F used in the lower-bound proof is no longer fixed. The two-label theorem cannot be invoked without another guard for that change. Likewise an active root losing both roles exits the fiber. These are limitations of the sufficient mechanism, not new restrictions on native admissibility.

Floors must be checked per destination slot. A root whose background has size a_i-2 must retain both role labels; a pure-role destination in that slot would be inadmissible even if a hitting-set calculation passed.

## 3. Why saturating three labels is not automatically one-unit safe

Take P={x,y,z}, four floor-one roots,

    A=({y},{z},{x},{x}),
    C=({x},{x},{y},{z}).

Both endpoints have transversal three, and every root is active for the three-label set. Saturating those three labels in every root produces four copies of P, with transversal one. The direct union A_i union C_i also has transversal one: its supports are {x,y},{x,z},{x,y},{x,z}, all hit by x.

Thus a three-label version of the one-unit saturation claim is false even for exact endpoints with identical role occupancy. These endpoints still have a one-unit repair by the accepted floor-compatible root swaps. The example limits this saturation rule, not connectivity, and is not an arity campaign.

For a general role set L of p labels with fixed background and active-slot union, exact source level q implies g>=q-p. Full role saturation has transversal min(lambda_0,1+g), hence is guaranteed only to remain at least q-p+1. With two labels this yields q-1; with three labels it permits q-2, as realized above.

## 4. Next mathematical question

The bounded-buffer completeness claim is disproved, but bounded numbers of LABEL ROLES per exchange are a different restriction from bounded numbers of temporarily modified ROOTS. Repeated two-label exchanges can involve many roots, and their completed tuples may already be far from the original global endpoints. The participation theorem does not rule out this architecture.

The open task is to prove accessibility between different fibers through exchanges whose completed states retain at least q, with a well-founded progress argument, or to find a precise obstruction to that method. Safe symmetry exchanges and the explicit renewal formula alone do not establish that every pair of exact-q endpoints is connected.
