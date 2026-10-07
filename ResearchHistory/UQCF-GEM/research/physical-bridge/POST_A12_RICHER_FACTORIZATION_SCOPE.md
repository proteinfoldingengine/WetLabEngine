# Post-A12 richer factorization: hidden-spectator completion scope

Date: 2026-10-06 (America/Phoenix).
Status: PROSPECTIVE ANALYTICAL SCOPE. No numerical campaign, implementation, benchmark, independent review, physical interpretation, or numbered certification.

Parent selection/completion closeout:
- POST_A12_SELECTION_COMPLETION_CLOSEOUT.md at b5883356c2ec2eadf57fc1f9655998b687bd2129.
Continuation index:
- POST_A12_THEOREM_FIRST_SYNTHESIS.md at 9c685b7d949d2a9b616531ac77cb18c08baaf08f.

## Objective

Prove a genuine retained-state factorization in which the labelled address record does NOT reconstruct the complete residual incidence state.

The selected class must:
- allow multiple hidden support patterns per labelled residual root;
- admit exact labelled destination restoration;
- preserve original floors and 3<=tau<=4 at every primitive;
- use a retained labelled mismatch record strictly smaller than the full hidden incidence description as spectator dimension grows;
- never read hidden spectator incidences after initialization.

This is deliberately a structural-safe class. It does not yet prove nontrivial dynamic use of the aggregate M_R certificate.

## Carrier

Let core labels be a,b,c,d and let T={t_1,...,t_s} be s>=1 spectator labels disjoint from them. Palette
    P={a,b,c,d} union T.

Fixed controlled roots:
    alpha={c};
    beta={d};
    guard i={a,b};
    guard j={a,b}.
Anchor floors1; guard floors positive and <=2.

There are n>=1 labelled residual roots r_1,...,r_n. Each has an arbitrary immutable spectator set
    Z_r subseteq T
and one mutable core owner q_r in {a,b}:
    S_r={q_r} union Z_r.

Original residual floor f_r is supplied immutable metadata satisfying
    1 <= f_r <= 1+|Z_r|.
For the no-read controller, the numerical floor f_r may be retained but Z_r itself is hidden.

Exact destination is defined relative to the labelled source:
    C_r={a} union Z_r
for every residual root r.
Thus every spectator incidence must be preserved exactly in its original labelled slot, while every core b is replaced by a.

Allowed macro for r with q_r=b:
    Add(r,a), then Del(r,b).
No spectator incidence may be toggled.

Retain only the labelled mismatch set
    Q={r:q_r=b}
plus immutable carrier/floor metadata and phase memory. The full spectator assignment (Z_r)_r is not retained.

## Required positive theorem

Prove:
1. Every source, intermediate and target state lies in 3<=tau<=4 for every spectator assignment.
2. Every macro respects syntax and original floor without knowing Z_r.
3. Controller: choose least r in Q, execute Add a then Del b, remove r from Q.
4. Rank |Q| terminates after exactly |Q| macros=2|Q| edits.
5. Final labelled support is exactly {a} union Z_r for every r, although Z_r was never read or reconstructed.
6. No hidden spectator incidence changes.

## Genuine information reduction

For fixed n,s and mismatch set Q, there are
    2^(n s)
possible labelled spectator assignments.

All produce the SAME retained Q and controller transcript (same selected roots and core edits), although their full incidence states and exact residual targets differ.

Prove the retained dynamic address record has only 2^n possible Q states (n membership bits), independent of s, while the hidden spectator component alone has ns independent incidence bits.

For fixed mismatch cardinality m, retain the earlier lower bound:
    at least binomial(n,m) distinguishable address states
are required by deterministic no-read endpoint-directed completion across all Q of size m. The hidden spectator multiplicity does not increase this address lower bound because spectators are invariant and never affect legality in this class.

Do NOT claim total memory compression if immutable carrier/floor metadata is encoded in an adversarial way; state the comparison precisely for dynamic labelled residual-incidence information.

## Structural certificate claim

Prove the band structurally:
- anchors force c,d;
- guards force at least one of a,b;
- every residual root contains at least one of a,b throughout the macro;
- {a,b,c,d} is therefore always a four-cover.

Thus the aggregate M_R certificate is unnecessary for legality in THIS class. Say so explicitly. This is a genuine information-factorization theorem, not a theorem that M_R is always needed.

## Required rejecting boundaries

1. If spectator incidences are themselves allowed to change, Q no longer specifies their target or update; theorem does not apply.
2. If a residual root may lack both a and b, the structural four-cover can fail; theorem does not apply.
3. If the target prescribes spectator incidences different from their source values, the controller lacks address information for those differences.
4. Do not infer observer accessibility: Q is retained input, not derived internal readout.
5. No physical locality/geometry interpretation.

## Next frontier if successful

Move from invariant hidden spectators to a class where some hidden non-core incidences MAY change, but their legality can be certified by an aggregate field and their exact destination can be addressed by a reduced difference record that still does not reconstruct the full state.

That is the first place where certificate and address information would both be nontrivially active.

Closed A12.1-A12.5, certified v16.54/v16.55 and accepted A11 remain unchanged. No A12.6, force, geometry, energy, GR/ADM, dark-matter replacement, continuum, physical nonlocality, observer field or fundamental time.
