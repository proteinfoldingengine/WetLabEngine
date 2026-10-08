# C3 safe-probe observation-coordinate audit

Date: 2026-10-08.
Status: AUTHOR-SIDE EXPLICIT-DEFINITION ADDENDUM; independent re-review required.
Parent: COUPLED_C3_SAFE_PROBE_CLARIFICATION.md at 77ac20020170607596262980c61aed8240adda7e.
Gemini run 37850129591, verdict REVISE, zero counterexamples, two requests for explicit coordinate definitions. The reviewer explicitly retracted its own initial objection to the M_core intersection identity.

## Exact coordinate definitions and invariance

Fix P0={a,b,c,d,e} and T disjoint from P0. For each Z subseteq T, define labelled supports
 S1(Z)={a,b}, S2(Z)={b,c}, S3(Z)={a,c}, S4(Z)={d,e} union Z.
The labelled core projection is the ordered four-tuple
 C(Z)=(S1(Z) intersect P0, S2(Z) intersect P0,
       S3(Z) intersect P0, S4(Z) intersect P0)
     =({a,b},{b,c},{a,c},{d,e}).
Hence C(Z) is constant under all spectator-only toggles.

Fix the labelled residual family R={r4}. For every nonempty H subseteq P0 of size at most four,
 M_core(H;Z)=sum_{r in R} 1[S_r(Z) intersect H=empty]
            =1[({d,e} union Z) intersect H=empty]
            =1[{d,e} intersect H=empty],
because Z subseteq T and H subseteq P0 with T intersect P0=empty. No requirement Z=empty is used.

Define tau(Z) as the MINIMUM cardinality of a set of labels meeting each of the four roots S_i(Z). The first three roots form the three edges of a triangle, so any hitting set of them has at least two labels and {a,b} hits them all. Since S4(Z) is disjoint from {a,b,c} and contains d,e, every full hitting set requires at least one additional label, while {a,b,d} hits all four. Thus tau(Z)=3 for every Z subseteq T.

Define the floor-validity Boolean vector F(Z)=(1[|S_i(Z)|>=f_i])_{i=1}^4 with fixed original floors f_i=2. The first three roots have size2, and |S4(Z)|=2+|Z|>=2, so F(Z)=(1,1,1,1) for every Z. These are exact mathematical observation coordinates; their physical accessibility is NOT established.

Consequently the full declared O_core(Z)=(C(Z), (M_core(H;Z))_H, tau(Z), F(Z)) is independent of Z. This proves invariance coordinate-by-coordinate, not by merely naming an observation channel.

## Adjudication

Gemini's initial claim that the intersection identity required Z empty was explicitly self-corrected in the same response. The two remaining requests concern explicit definitions of C, tau and F, supplied above. This addendum introduces no stronger observer and no hidden state read. The original closed-world, uniform-safety, state-independent successful commit and fixed-root assumptions remain intact.

Do not mark theorem closed on this author-side argument alone. Require fresh independent review and publication consistency audit. No force, geometry, energy, GR/ADM, continuum or fundamental time follows.
