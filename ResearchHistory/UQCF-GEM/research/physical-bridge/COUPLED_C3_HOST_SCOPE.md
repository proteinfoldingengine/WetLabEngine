# C3 retained host-selection checkpoint — frozen scope

Date: 2026-10-07.
Status: prospective analytical scope; no independent acceptance.

Parent bounded C3 closeout: COUPLED_C3_DEADLOCK_CLOSEOUT.md at fae793e6fb586c949845e495ec243bd996b0cdf4.

## Question

In the already independently accepted four-root carrier, is the auxiliary host r4 merely one convenient choice, or is it FORCED among all eight-edit optimal native paths that use the fresh label w?

Source: r1={a,b}, r2={b,c}, r3={a,c}, r4={d,e}.
Target: r1={b,d}, r2={b,c}, r3={c,d}, r4={a,e}.
All floors2. Palette P={a,b,c,d,e,w}; w absent at endpoints. Native event toggles one incidence, protected band 3<=tau<=4.

## Required theorem

Prove every protected native path of minimum eight edits must begin by adding w to r4. More precisely:
- the six endpoint-differing toggles must occur exactly once in any eight-edit path;
- the two extra toggles must be addition and deletion of one off-endpoint incidence;
- show the only legal first off-endpoint event is +w on one of r1,r2,r3,r4 (all other additions outside endpoint differences either already present or create an explicit two-cover);
- show +w on r2 cannot lead to an eight-edit completion;
- show +w on r1 or r3 forces its corresponding -a endpoint deletion next, after which every remaining endpoint addition is forbidden by an explicit two-cover;
- show +w on r4 admits the published eight-edit path.

If the 'only legal first off-endpoint event' statement is too strong, replace it with the correct classification of possible first events and restrict the uniqueness claim accordingly. Do not assume a particular macro order.

## Retained selection question

Determine whether the unique optimal host can be identified from retained core support/endpoint-address information rather than querying a hidden state during execution. State exactly what data is retained. Do not generalize to arbitrary hidden fibers or coupled-cycle families.

## Rejection and limits

A non-optimal longer path using another host does not refute optimal-host uniqueness. A legal eight-edit path using another host does refute it.

Do not claim general reusable host selection, physical interpretation, or independent certification. Author audit, independent adversarial review, and immutable GitHub readback required before scoped closeout.
