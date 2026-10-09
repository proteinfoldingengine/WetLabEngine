# Stable-cover deficit exchange: lower incidence cost with band protection
Status: frozen proof; independent verification/reviews pending.
Companion: COUPLED_C4_DEFICIT_SCOPE.md.

## 1. Retained certificate
Use the role-complete carrier, with fixed hidden backgrounds Q_r and role patterns W_i. Pool labels are distinct; hosted D,E occur nowhere else; w is fresh. Floors are immutable and no larger than source root sizes.
For selected slot i, let A be its current label. Choose J subset of other slots, |J|<=2, whose union U covers every non-host root outside W_i.
Let P=W_i intersect U and R=W_i minus U, with m=|W_i|>=1 and r=|R|. The controller derives these sets from the retained template, without observing backgrounds or covers.
Among valid J, minimizing (max(1,r),|J|,J) lexicographically is a finite exact computation. It claims optimality only among these declared certificates, not among native paths.

## 2. Schedule and incidence cost
In fixed root order:
+w(host),-D(host);
for each p in P: +D(p),-A(p);
for each q in R: +D(q);
for each q in R: -A(q);
+A(host),-w(host).
Every operation is a genuine toggle. D starts only on the host and is removed before non-host additions; A occurs exactly on W_i and is removed completely before host insertion.
All root sizes stay at least their source sizes. At the endpoint all original sizes are restored, so all original admissible floors survive.
The number of edits is2m+4. Source-relative excess is1,0 for the host preparation; alternates1,0 on P; rises to r then falls to0 on R; and finishes1,0 on the host. Thus the peak is exactly max(1,r), including r=0 and P empty. The marker occupies only the host and is removed.
No full-state read is used. One excess incidence is achieved when r<=1, independently of m.

## 3. Lower protection
For every intermediate U_state, use the same-root support-containment lemma: phi(U_state,r) subseteq S_r implies tau(S)<=tau(U_state).
Fix all background labels, all other pool labels and E; send w to E.
Before the first non-host D addition, fix A,D. From that addition until A enters the host, send D to A and fix A. After A enters the host, send D to A and A to D.
These maps are valid because D has already left the host, and A enters it only after leaving all W_i roots. Covered-root interleaving does not alter either condition. This argument is independent of J and the backgrounds.
Thus tau(U_state)>=tau(S)>=3.

## 4. Upper protection by a changing retained core cover
Let K be the set of current active labels with indices J. Its size is at most2 and none of its incidences changes.
K covers all non-host roots outside W_i and all of P. Until all R additions are complete, A remains on every deficit root. Therefore K union {A,E} covers every slice up to that point, even while P is individually exchanged.
After all R additions are complete, D covers all deficit roots and remains there. K union {D,E} covers the remaining slices. If R is empty, K union {E} covers every slice and the switch is unnecessary.
Both covers have at most4 labels. Together with section3,3<=tau(U_state)<=4 throughout.
The covers are derived from known role incidences; hidden backgrounds can only supply extra intersections. The proof does not assume a minimum cover or observe tau. Source tau3 may rise to4; exact tau invariance is deliberately not claimed.

## 5. Renewal and arbitrary target assignments
At each endpoint A and D exchange their role/host positions, all other pool labels and all backgrounds remain at their exact roots, and w is absent. Pattern sets and therefore the certificate index sets J_i are unchanged.
If every slot has a valid certificate, process target slots in order. Skip a correct slot. Exchange directly when its desired label is hosted; otherwise evacuate that label from its unfixed current slot through a hosted label, then install it. Target injectivity ensures no previously fixed slot is disturbed as a role assignment, even when patterns overlap.
This finite induction uses at most2k exchanges. With M=max_i|W_i| and beta=max_i max(1,|W_i minus U_{J_i}|), it uses at most2k(2M+4) edits and peak total excess at most beta, since every macro restores its boundary size.
This is a sufficient interface. If some slot lacks a valid J, no conclusion about native connectivity follows.

## 6. Strict cost improvement and genuinely changing covers
Take five non-host supports {A,B},{A,C},{A},{B},{C}, and host{D,E}, with empty backgrounds.
The four disjoint supports {A},{B},{C},{D,E} prove tau4. For exchanging A, J={B,C}, P={0,1},R={2}; hence the schedule has peak1 despite m=3. The earlier role-complete macro has peak3 for the same role.
No fixed four-label set covers the entire new trajectory: the singleton supports {A} and {D} occur at root2 in different slices; {B},{C} persist; and host{E,w} occurs after D leaves but before A enters. These five disjoint sets, taken across slices, require5 labels. {A,D,B,C,E} hits all slices, so the persistent-cover hitting number is exactly5.
Thus a one-excess-incidence path can use changing four-covers and need not be protected by an undisclosed fixed four-cover.

## 7. Exact-tau boundary
In the same carrier, add one spectator z only to roots3 and4. The source has cover{A,z,E}, and the three disjoint supports {A},{B,z},{D,E} force tau3.
After individually exchanging root0 and before exchanging root1, supports {D,B},{A},{C,z},{E,w} are four pairwise disjoint roots of the actual slice. Thus tau4 at that slice. The theorem's upper bound proves equality.
This is a positive band-safe path and a rejecting control for false exact-tau preservation. It does not refute the earlier full-batch theorem, which retains its larger incidence budget and exact-tau guarantee.

## 8. C3 and physical scope
Template, current/target roles, host address, label/root order, actual-edit phase, initial admissibility and marker freshness remain supplied. The certificate is computable solely from the retained template; no hidden-background, floor-value, tau or minimum-cover observation is added.
Native generation/access to those records and forced request completion are not proved. Arbitrary NOOPs can block completion. No global path-optimality, universal one-incidence repair, force, metric, GR derivation or fundamental time follows.
