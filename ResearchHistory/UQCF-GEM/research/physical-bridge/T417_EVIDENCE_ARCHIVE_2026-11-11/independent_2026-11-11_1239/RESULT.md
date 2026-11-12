# Q145 RESULT (2026-11-11T12:40:20-07:00): a fixed state cannot covariantly supply the survivor label
Science, local, supporting math. Not posted. NOT_DERIVED; Not claimed; scientific_breakthrough false. notify_aaron: no.
Heads unchanged: research 8c4f6594; thread 8a86d82d. PR111: no comments after 6799790426. No lock.

## Question
Q144 showed that on a symmetric merge (survivor and pruned sub-fibers isomorphic) chain-intrinsic selections give only R_min or R_full,
so R_inc^- needs the (E1) label. Q145: does the fixed state ω of ledger §12.1 (inherited frame: a fixed state restricted to the chain)
supply that label, i.e. is there a selection rule σ(chain, ω), defined from the chain and ω alone, that equals the survivor selection?
Definitions: "defined from chain and ω alone" = covariant: σ(ω∘α^{-1}) = α·σ(ω) for every chain automorphism α (relabelling the
atoms cannot change which physical sector is picked). Premises: ledger §12.1, Thm 13.3 (inherited); preparability G (ASSUMED in ledger
§13.4: the preparation set is closed under chain automorphisms). Dedup: ledger §12.1/§13.2 say σ is pinned by (E1),(E2) but do not ask
whether ω can replace (E1); Q139/Q140 (x_p ≡ −x_u) concern detection, not selection; T-235 Cor O.1 concerns INV effects; d28
"relative-history reading of an address" (receiver_identification §22) sources a root shift, not a state-dependent label. No prior
independent_* RESULT on covariant state-dependent selection (grep). Fail criterion: a covariant rule matching the survivor on all of 𝒫.
Deviation disclosed: q145.py written in the same sitting (no separate PREREG); it is a sanity check, the claim is the proof below.

## Prop 145.1
Let G be the chain automorphism group, σ* the survivor selection, 𝒫 a G-closed set of preparations. For any covariant σ and any ω ∈ 𝒫,
the number of cosets αStab(ω) with σ(αω) = σ* is at most 1. Hence (i) no covariant σ equals σ* on all of 𝒫 unless σ* is G-invariant
(which Q144 excludes on symmetric merges); (ii) under any G-invariant measure on 𝒫, P[σ(ω) = σ*] ≤ 1/|G·σ*|, = 1/3 on the Q144 witness
(1/k for a block of k isomorphic sub-fibers); (iii) for ω with a nontrivial stabilizer moving σ* (e.g. ω_p = ω_l1), no covariant σ can
return σ* at all.
Proof: σ(αω) = ασ(ω), and α ↦ ασ(ω) equals σ* on at most one left coset of Stab(σ(ω)); (iii) σ(ω) must be Stab(ω)-invariant. ∎
Check (q145.py, seed 145, 20000 Dirichlet states, 4 covariant rules): 0 covariance failures, 0 orbit-bound violations; empirical
agreement 0.329–0.336 vs bound 1/3; stabilizer case confirms (iii).

## Reading
State-dependent typing is preparation-dependent; the survivor/pruned distinction (E1) is preparation-independent. So ω cannot replace
(E1): the address label is an inherited P1 datum (r_XY(t) = t), not something the fixed state supplies. This confirms the Q144 hunch and
closes the "state supplies the label" route. Novelty: elementary/near-implied (standard covariance/orbit argument); local only, not postable.
Tags: chain, ω, Thm 13.3 INHERITED; G ASSUMED (as in ledger); Prop 145.1 DERIVED (elementary).
Hashes: e2a9a75f/079719ce (q145.py/stdout.txt).

## NEXT
Q146: on the P1 tree beyond symmetric merges: characterize exactly when the restriction chain alone (Aut-invariant σ) already yields
R_inc^- — conjecture: iff at every straddling merge the survivor's past fiber sub-chain is non-isomorphic to every co-merged pruned
sub-chain. Test with a removed child that previously absorbed its own leaves (isomorphic histories possible). Dedup vs Q144, ledger §11.4/Prop 11.6.
