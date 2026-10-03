# A two-overlap bridge can fail between exact endpoints

This is a symbolic construction, not an enumerated campaign. It limits the union-bridge method in GUARD_HANDOVER.md; it does not establish any root or native disconnection.

Take P={1,2,3,4}, four labelled roots with floors all one, and q=4, t=3. Let

    A=({1},{2},{3},{4}),
    C=({2},{1},{4},{3}).

Both endpoints have transversal exactly four and satisfy every exact-endpoint redundancy/capacity requirement. Choose old guard I={1,2,3} and destination guard J={1,2,4}; each has transversal three. They share two indices.

Preparation changes root 4 to {3}, while I protects the lower bound. The proposed shared-slot union bridge is then

    D=({1,2},{1,2},{3},{3}),

with transversal two, below t. Here I union J includes all slots, so the proposed bridge itself is an inadmissible lower-guard state, not merely a failed subfamily certificate. For H={1,3}, M_A(H)={2} and M_C(H)={1}; the miss sets are nonempty but disjoint, exactly as predicted by the criterion.

The endpoints nevertheless have a unit-band path: swap roots 1 and 2 using add 2 to root 1, add 1 to root 2, delete 1 from root 1, delete 2 from root 2; then analogously swap roots 3 and 4. In each swap the other two singleton roots remain disjoint from the affected pair. The affected pair needs one or two hitting labels, giving total transversal three or four; floors hold and completed swaps restore exactness.

This intentionally simple example lies in an already solved class. Its purpose is to disprove an unjustified extension of O1 to arbitrary overlap based only on nonempty endpoint miss sets. It does not supply an unresolved higher-floor endpoint, disprove a more adaptive handover, or show that exact relational constraints fundamentally cannot renew protection. Here renewal succeeds after the schedule is changed.
