# C3 native core-probe theorem — exact history fibers and one-sided capacity certification

Date: 2026-10-08.
Status: AUTHOR-SIDE ANALYTICAL CANDIDATE. Not independently accepted; not CLOSED/CERTIFIED.
Frozen scope: COUPLED_C3_CORE_PROBE_SCOPE.md at 4e0cb8c68c807265fb48652b1f990a18d4a43a2c.
Inherited accepted observation-fiber closeout: ce9e86013daeabdebc9c1118d8b08f1b39a437f1.

## 1. Model and question

Use the scope's four labelled roots, floor 2 at every root, core C={a,b,c,d,e}, disjoint spectator palette T with N=|T|>=1, and exact protected band 3<=tau<=4. Write

    X(P,Z)=(P1,P2,P3,P4 union Z),  Pi subseteq C, Z subseteq T.

Only root 4 contains spectators. Z is unknown and invariant. Initially P=({a,b},{b,c},{a,c},{d,e}); hence every Z subseteq T is initially possible and tau=3.

An attempted command toggles one named CORE incidence. Its permitted outcome is either the actual native-admissible edit, or a rejected NO-OP. Rejection is always permitted, including for a legal command. No fairness, guaranteed commit, rejection reason, or hidden write is assumed. Commands and exact O_core snapshots are retained in order. O_core includes labelled core projections, core-only miss counts, exact tau, and floor-validity, but no spectator read or total root cardinality.

Let H_n be a feasible observed history, including commands, from snapshots P_0,...,P_n. The target b=1[Z nonempty] is constant throughout that history. Define

    D_n=max(0, max_{0<=j<=n}(2-|P4_j|)).                     (1)

The result will characterize ALL hidden spectator subsets compatible with H_n, not merely provide a sufficient bound.

## 2. Native hitting-set explanation of spectator invisibility

**Lemma 1 (single-root spectator dominance).** If P4 is nonempty, then

    tau(X(P,Z))=tau(P1,P2,P3,P4)                            (2)

for every Z subseteq T.

Proof. Every transversal of the projected four core supports hits all full supports, so the full hitting number is no larger. Conversely, take any full transversal H and fix c in P4. Spectators can hit only root 4. Replace all spectator elements of H, if any, by c. The resulting core set still hits roots 1,2,3, still hits root 4, and has cardinality at most |H|. It is a transversal of the core family. Taking minima gives the reverse inequality. No assumption about a selected shortest transversal is needed.

Every core-only miss-count coordinate is also independent of Z: for H subseteq C, (P4 union Z) intersect H = P4 intersect H. This holds for any fixed residual-root selection used by those coordinates.

**Lemma 2 (empty projected root).** If P4 is empty and X(P,Z) is admissible, then |Z|>=2 and

    tau(X(P,Z))=tau(P1,P2,P3)+1.                            (3)

Proof. The root-4 floor requires at least two spectators. A transversal must hit the first three, purely core, roots and must contain at least one spectator to hit root 4. These requirements use disjoint palettes. A minimum transversal of the first three roots plus one spectator attains the lower bound. Equation (2) must NOT be used when P4 is empty: the projected four-root family then contains an empty support.

Thus in this carrier the exact hitting number is spectator-cardinality-blind wherever admissibility is already satisfied. It does not supply the missing capacity bit by itself.

## 3. Exact native history-fiber theorem

**Theorem 3.** For any feasible H_n in this scope, its exact hidden completion family is

    F(H_n)={Z subseteq T : |Z|>=D_n}.                      (4)

In particular D_n<=N, and the feasible spectator counts are precisely the integer interval [D_n,N]. The family retains all label choices of each feasible cardinality; no spectator identity is reconstructed.

**Necessity.** At every observed state, root-4 admissibility requires

    |P4_j|+|Z|>=2.

Since Z is invariant, all of these inequalities hold for the same Z. Their conjunction is exactly |Z|>=D_n. Rejected attempts add no proposed state to the list of actual snapshots.

**Constructive sufficiency.** Start from any one actual hidden realization Z_* of the feasible history. Choose an arbitrary Z' subseteq T with |Z'|>=D_n. Replace Z_* by Z' in every state, leaving all projected supports P_j and all attempted commands unchanged.

1. Every root-4 floor remains valid by (1); floors at the other roots are unchanged.
2. At a snapshot with P4_j nonempty, Lemma 1 gives the same exact tau for Z' as for Z_*. At a snapshot with P4_j empty, (1) implies |Z'|>=2 and Lemma 2 gives the same exact tau. Hence the protected band and reported tau agree at every snapshot.
3. Labelled core projections and every core-only miss count agree. All states are floor-valid, so that observed flag also agrees.
4. At an actual committed core edit, the same single core incidence changes with Z'. Its membership preconditions are unchanged, and its resulting state has just been shown admissible. It is therefore a legal native edit in the alternative history.
5. At a rejected attempt, choose rejection again. The outcome relation permits this even when the command would be legal with Z'. No rejection reason is observed.

This constructs the same complete observed history for every such Z'. If commands are chosen adaptively from prior observations, equality of those observations makes the same commands be chosen inductively. This proves exact sufficiency, including adaptive histories and rejected attempts.

A claimed transcript with D_n>N cannot be feasible under the stated invariant-spectator model. An arbitrary syntactic transcript also needs ordinary command, projection, tau, and band consistency; (4) is asserted for histories already known to be feasible, not as a substitute for those consistency checks.

## 4. The retained statistic and its information content

**Corollary 4.** The history statistic has the exact online update

    D_0=0,
    D_{n+1}=max(D_n, 2-|P4_{n+1}|).                       (5)

It is an integer in {0,1,2}, nondecreasing along the ordered observation record. For N=1 the value 2 cannot occur in a feasible history. It is a lower bound on hidden spectator cardinality, not an energy, conservation law, physical clock, or new root observable.

Since N>=1 and every initial Z was allowed:

- If D_n=0, both Z=empty and a singleton Z are compatible with exactly the same entire history. The capacity bit is not determined.
- If D_n>=1, every compatible Z is nonempty, so b=1 is certified.
- No feasible history of this form certifies b=0: a nonempty completion always remains available.

For the bound itself, maximality is exact: a completion with |Z|=D_n realizes the history. No universally larger cardinality lower bound can be extracted from the same history.

The accepted observation-fiber criterion applied to H_n therefore gives a precise positive certificate and a precise failure of two-sided factorization. This is not an abstract instruction to observe b: (5) uses only the declared core projections and the already fixed floor law.

The record can retain information that a current-state snapshot alone loses. A successful visit below two core incidences establishes D>=1. After the original core supports are restored, the instantaneous O_core can again equal its initial value, while D still certifies the invariant spectators' nonemptiness. This memory conclusion requires the stipulated invariance of Z.

## 5. Concrete native probe without an added acknowledgement channel

Issue -d(root4) at the initial E(Z).

**Successful, visibly changed outcome.** The new root-4 core projection is {e}. The proposed full support is {e} union Z. The triangle on a,b,c still has hitting number 2, and the disjoint fourth root adds one, so tau remains 3 for every nonempty Z. The root-4 floor is satisfied exactly when |Z|>=1. An OBSERVED actual deletion therefore raises D from 0 to 1 and certifies b=1.

No separate success-acknowledgement bit was introduced: under this restricted outcome relation, the changed core projection itself distinguishes a committed core toggle from a rejected NO-OP. This does not contradict the earlier failure for +z(root4), whose successful spectator insertion leaves the core projection unchanged.

**Rejected or unchanged outcome.** The actual core projection remains {d,e}, and D remains 0. Such an outcome is compatible with Z=empty, when deletion is invalid, and with Z nonempty, when a legal deletion was rejected. Failure to observe a change is NOT evidence that b=0.

**Restoration.** Following success, the core addition +d(root4) is legal for every compatible Z. If it commits, it restores E(Z) in a second actual incidence edit, with tau=3 throughout and spectators untouched. Rejected restoration attempts leave the already admissible probe state unchanged. Exact restoration is reachable in one further committed edit; finite operational completion is not guaranteed without an additional progress assumption.

For |Z|>=2, a further successful deletion of e before restoration gives P4 empty and D=2. Lemma 2 still gives tau=3, and the full root remains floor-valid. This demonstrates why the empty-projection case belongs in the theorem.

## 6. Exact limitation on adaptive experimentation

**Theorem 5 (no guaranteed finite two-sided decision).** No deterministic adaptive core-command procedure can terminate with the correct b for every initial Z and every outcome history permitted by this scope.

Proof. Compare E(empty) with E({z}) for any z in T. Permit every attempted command to reject in both runs. Both states remain at their initial projections, tau=3, and valid floors. Every observation and hence every adaptively selected command is the same in both runs. Any finite declared answer must therefore be the same although b differs. A procedure that never answers on this common run does not terminate on every permitted history. Either way a guaranteed finite two-sided procedure is impossible.

The obstruction is stronger than a single bad command. By Theorem 3, every feasible finite transcript with D=0 remains ambiguous even when it includes actual, visibly committed common-feasible core edits. A native core path that is admissible for BOTH an empty-spectator state and a nonempty one cannot cross |P4|<2 in the empty branch; its observations remain indistinguishable. Positive information enters precisely when an observed successful edit exploits a floor capacity the empty branch does not possess.

Under the DIFFERENT model in which every legal requested command must commit and every invalid one must reject, the single -d probe gives a two-sided decision by changed versus unchanged core. That model is not supplied or derived here. Unbounded eventual-success fairness, by itself, supplies no finite rejection deadline and therefore does not make an arbitrary finite string of rejections a certificate of emptiness.

## 7. Premise controls and failure boundaries

1. **Attempt is not transition.** At E(empty), proposed root4={e} violates floor 2. A rejected -d leaves {d,e}; updating D from the proposed support would falsely certify b=1.
2. **Single-root spectators are essential.** Outside this carrier, supports {a,b,z},{c,d,z},{e,f},{g,h} have full tau=3 but core-projected tau=4. A spectator shared across roots is not dominated by an arbitrary core element of one root. Both families satisfy floor 2 and lie in the 3..4 band. Lemma 1 does not extend to that case.
3. **Spectator invariance is essential.** Start E({z}), observe successful -d, then successful +d, so D=1. An unreported subsequent -z is itself a valid native edit and produces E(empty), with tau=3 and unchanged core observation. The old D no longer bounds current spectators. This is excluded by the frozen model, not solved by the theorem.
4. **Core accessibility remains an assumption.** Reading exact core projections, tau, and floor-validity is the inherited observation contract, not a first-principles physical observer construction.
5. **State evidence is not unrestricted provenance.** The changed-core argument certifies a toggle only under the stated one-command/actual-toggle-or-NO-OP relation with no compensating writers. It does not reconstruct arbitrary provenance from a final incidence state.

## 8. Scientific advance and remaining gate

The accepted abstract fiber criterion now has a native, history-dependent application: the exact observed core-floor deficit D_n determines the entire hidden completion family in this carrier. A successful visible core probe provides a one-sided capacity certificate without reading spectator identities, total root size, full-palette miss counts, or a new acknowledgement variable. Restoration can erase the current core difference without erasing the retained certificate.

The same derivation identifies a structural obstruction: common-admissible core edits remain spectator-blind, and arbitrary rejection prevents guaranteed finite two-sided certification. A broader observer mechanism must justify accessible observations and sufficient progress or supply a separately derived distinguishing channel. Merely naming the missing capacity bit does not supply either.

This manuscript is author-side mathematics with local hand-case checks, not a fresh independent mathematical acceptance, publication audit, numerical-universe PASS, formal proof-assistant result, or numbered v16 certification. Broader C3 and C4-C6 remain OPEN. No physical force, geometry, energy, GR/ADM, continuum, or fundamental time is derived.
