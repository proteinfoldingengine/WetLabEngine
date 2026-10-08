# C3 safe-probe observability — consolidated self-contained theorem

Date: 2026-10-08.
Status: NEW AUTHOR-SIDE CONSOLIDATION / INDEPENDENT REVIEW REQUIRED.
Scope: the previously frozen C3 safe-probe model, with explicit closed-world and fixed-slot interpretation. Earlier evidence and REVISE verdicts remain immutable and are not overwritten.

## Definitions

Let P0={a,b,c,d,e} and T be a finite palette disjoint from P0, with u in T. For each Z subseteq T define the four labelled root supports
  S1(Z)={a,b}, S2(Z)={b,c}, S3(Z)={a,c}, S4(Z)={d,e} union Z.
The original floors are f1=f2=f3=f4=2. The hitting number tau(Z) is the minimum cardinality of a label set intersecting every S_i(Z).

Fix the labelled residual index family R={r4}, independently of Z. For every nonempty H subseteq P0 of size at most 4, define
  M_core(H;Z)=sum_{r in R} 1[S_r(Z) intersect H=empty].
Define C(Z)=(S1(Z) intersect P0,...,S4(Z) intersect P0), and F(Z)=(1[|S_i(Z)|>=2])_{i=1}^4.
The retained observation is EXACTLY
  O_core(Z)=(C(Z),(M_core(H;Z))_H,tau(Z),F(Z)).
It contains no full S4 cardinality, spectator identity or occupancy, full-palette miss count, failure/legality response, state-dependent timing or other hidden-state channel. This is a mathematical observation map, not a derived physical sensor.

There are two initially possible hidden worlds:
  A: Z_A,0=empty; B: Z_B,0={u}.
The observer knows this two-world hypothesis set but not which member is actual. The initial target bit is b0=1[Z0 nonempty], hence b0(A)=0, b0(B)=1.

A permitted controller action is a labelled spectator toggle +z(r4) (valid iff z absent) or -z(r4) (valid iff z present). A controller policy is uniformly safe when every action it chooses is valid in EVERY currently consistent hidden world. Each chosen action actually commits exactly once, changes only that incidence, and returns a state-independent success record containing no information beyond the already known command. Rejected attempts and their feedback are not allowed. No autonomous edits, external writers, floor changes, root-index changes or other hidden evolution occur between controller commits. The controller's action and stopping rules depend only on its observed transcript (and, if randomized, its own private random seed).

## Lemma 1: exact observation invariance

For all Z subseteq T,
  C(Z)=({a,b},{b,c},{a,c},{d,e}).
For each H subseteq P0, Z intersect H=empty, so
  M_core(H;Z)
    =1[({d,e} union Z) intersect H=empty]
    =1[{d,e} intersect H=empty].
The first three roots form a triangle, requiring two hitting labels; the disjoint fourth root requires at least one more. {a,b,d} hits all four, hence tau(Z)=3. The first three root sizes equal 2 and |S4(Z)|=2+|Z|>=2, so F(Z)=(1,1,1,1).

Every coordinate of O_core(Z) is therefore independent of Z. This is a DERIVED property of the defined observation map, not an assumed conclusion.

## Theorem: adaptive uniformly safe probes do not identify the initial capacity bit

For any deterministic uniformly safe policy, the complete observed transcript (initial O_core, issued labelled commands, state-independent successful commit records and all later O_core values) is identical in worlds A and B for every finite executed prefix. Consequently no deterministic estimator based only on that transcript can correctly recover b0 in both worlds.

Proof: Initially Lemma 1 gives equal observations. Suppose transcripts coincide through step n. The transcript-dependent policy chooses the same next action in both worlds (or stops in both). If it acts, uniform safety guarantees the same labelled toggle is valid in each. Closed-world exactly-once semantics produce the same known success record and no unreported intervening change. By Lemma 1 the resulting observations are identical. Thus the transcripts remain identical at n+1. Induction proves the claim for every finite prefix. Since b0(A)=0 and b0(B)=1, any function of the common transcript must give the same answer in both worlds and cannot be correct in both.

For a randomized policy, couple the two runs using the same private random seed. Conditional on each seed, the deterministic induction applies. Hence the transcript distributions are identical and no randomized transcript-only estimator can recover b0 with certainty in both worlds. No prior-dependent success-probability bound is claimed.

## Count-offset invariant and qualification

Each common committed action adds +1 or -1 to both spectator counts. Thus q_B,n-q_A,n=q_B,0-q_A,0=1 at every common prefix, by induction. This is an elementary preserved offset, not a new physical conservation law.

The CURRENT Boolean b_n need not remain different: when v in T distinct from u, the uniformly safe action +v yields {v} and {u,v}, so b_n=1 in both worlds, although the initial b0 remains unidentifiable.

## Rejecting controls and boundaries

Attempting -u at the initial pair would be valid only in world B. A trustworthy failure/legality response would distinguish worlds, but that attempt is NOT uniformly safe and lies outside the theorem's action domain. An initialized full-palette singleton miss count for u or the full fourth-root cardinality would also distinguish, but neither is in O_core. If T={u}, there may be no nontrivial uniformly safe initial toggle; the indistinguishability claim still holds for the empty transcript.

This theorem is limited to the explicitly declared carrier, closed-world semantics, uniformly safe spectator-only controls and core-only observation. It does not prove a universal no-observer theorem, an observer-accessible channel, a physical force, geometry, energy, GR/ADM, continuum or fundamental time. Broader C3 and C4-C6 remain OPEN.
