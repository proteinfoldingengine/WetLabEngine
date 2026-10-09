# Role-complete exchange with moving covers
Status: frozen argument; verification and independent reviews pending.
Companion: COUPLED_C4_ROLE_COMPLETE_SCOPE.md.

## 1. Exact carrier and retained interface
Use the carrier, immutable Q_r and floors, nonempty known patterns W_i and disjoint pool/marker of the scope. Non-host root r is Q_r union {A_i:r in W_i}. Host is Q_h union {D,E}. All roots are labelled; patterns can overlap or coincide. Current pool labels are distinct; hosted labels have no non-host occurrence.
The controller sees pattern and role data, host address, orders and committed-edit phase. It sees neither backgrounds nor a hitting set. Everything below is uniform over all backgrounds/floors satisfying the promises.

## 2. One role-complete exchange
Let A=A_i and m=|W_i|>=1. In fixed root order:
1. Add w to h, then remove D from h.
2. Add D once to each of the m roots in W_i.
3. Remove A once from each of those m roots.
4. Add A to h, then remove w from h.
Every move is a genuine toggle. Host and each affected root receive a replacement before losing an original incidence. Minimum root sizes equal source sizes; all original admissible floors survive.
There are2m+4 edits. Total source-relative excess incidences go1,0,1,...,m,m-1,...,0,1,0. Maximum is m. One fresh label is used on one host incidence; up to m temporary excess incidences occur using existing labels. No minimality claim.

## 3. Lower protection by actual support containment
Write S for the macro source and U for a slice.
If phi(U_r) subseteq S_r for every same labelled root, every cover H of U maps to a cover phi(H) of S with no greater size; hence tau(S)<=tau(U).
Fix all background labels and every pool label except A,D; always map w to E.
Before any D addition to a non-host root, fix A,D.
From the first D addition until just before A enters h, send D to A and fix A.
After A enters h, send D to A and A to D.
D has left h before the second phase. A has left ALL its non-host roots before the last phase. Thus containment holds at every root. Other apexes, even those sharing roots, are fixed. Spectator overlap is irrelevant.
Therefore tau(U)>=tau(S) at every slice.

## 4. Moving upper covers without observing them
Take any minimum source cover H. It is an existential proof witness, not controller input.
Through the host evacuation and the D-addition phase, A remains on ALL its original non-host roots. Define H_0 by replacing D with E if D belongs to H and otherwise keeping H. D originally occurred only on h, which permanently retains E. Thus H_0 covers every slice up to and including completion of the D additions, and |H_0|<=|H|.
Once all D additions have committed, D occurs on every former A-root. Define H_1 from H_0 by replacing A with D if A belongs to H_0. All source occurrences of A were exactly W_i. Consequently H_1 covers every subsequent slice, including the endpoint; the host remains covered by E or by any unchanged background element which covered it in H.
Therefore tau(U)<=|H|=tau(S).
With section3, tau is exactly invariant, including source tau4. The theorem in fact preserves any source hitting number in this template, though the repair contract uses the native band3..4.
This does not assume a fixed cover. The switch H_0->H_1 is justified only after the incoming label occupies the complete role.

## 5. Exact targets, renewal and termination
The endpoint replaces A by D on exactly W_i and replaces hosted D by A. All other labels and backgrounds remain in their exact roots; w disappears. The same template and floors are restored with new role assignments and the identical hitting number.
Process pattern slots in fixed order. Skip a correct slot. If its desired label is hosted, perform that exchange. Otherwise the desired label is in an unfixed slot j; evacuate it by exchanging j with the least ordered hosted label, then exchange the target slot with its now-hosted desired label. A previously fixed slot cannot hold the current desired label because target assignments are injective.
Each stage fixes its slot without changing prior fixed slot assignments, even if their incidence patterns overlap. At most2k exchanges suffice and at most2k(2M+4) primitive edits, M=max_i|W_i|. Peak total excess is at most M because each macro restores its source size. The endpoint is exactly the prescribed labelled supports and host complement. Coincident patterns can make assignments observationally redundant; supplied role labels still define a valid sufficient schedule, not an optimal one.

## 6. A genuine upper-band failure and moving-cover witness
Take non-host roots {0,4},{0,5},{1,6},{7} and host {2,3}. They have hitting number4: the first pair needs one label, the third and fourth need two further labels, and the host needs another. Label8 is fresh.
The old per-root alternating macro, swapping0 with2, produces after four edits:
{2,4},{0,5},{1,6},{7},{3,8}.
These five sets are pairwise disjoint, so tau=5 despite preserved local sizes. This is a failure of that schedule, not proof of native disconnection or necessity of more than one excess incidence under all legal paths.
The new batched path preserves tau4 by sections3-4.
No fixed four-label set covers all its slices. Any such persistent cover must hit the singleton{7}, the unchanged{1,6}, the host slice{3,8}, and both alternatives{0,4}/{2,4} and{0,5}/{2,5}. The last four sets require at least two labels from{0,2,4,5}; these labels are disjoint from the other three obligations. At least five are required. {4,5,1,7,3} covers every slice, so the union-family hitting number is exactly5.
Thus upper protection is genuinely supplied by changing covers, rather than by an unreported persistent four-cover.

## 7. C3 scope and remaining gap
The retained template determines the host and edit schedule uniformly over each admissible background fiber. No observation of tau, Q or the moving cover is needed. This proves a stronger retained-interface sufficiency statement for C3 and a renewable repair statement for C4.
It does not derive that template/role addresses or actual-resolution phase records from native dynamics. Arbitrary NOOPs can prevent completion. No extra observer primitive is introduced and no native observer-origin closure is claimed.
The admitted extra incidence cost is explicit. General one-excess-incidence repair and arbitrary core carriers remain separate unresolved obligations.
