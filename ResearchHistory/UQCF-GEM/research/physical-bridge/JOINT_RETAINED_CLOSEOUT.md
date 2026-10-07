# Joint retained-state factorization: scoped analytical closeout

Date: 2026-10-06 (America/Phoenix).
Disposition: ANALYTICALLY COMPLETE FOR THE TWO-PAYLOAD / BINARY-ENVIRONMENT CLASS.
Evidence: written mathematical proof with author-side audit and immutable readback. Not independent peer review, numerical certification, implementation, benchmark or physical validation.

## Immutable record

Scope:
- initial file commit 38e01188040442e1717cfebfa4705c479176289a
- frozen substantive scope commit 0fa27e915b77742e21657c91bfd49b4cf0f6a1e5
- JOINT_RETAINED_SCOPE.md

Proof:
- initial candidate 11487b01fab4ea8121d2bd9cfbc3c3f690fcfa5e
- corrected proof commit 6454074a95b526bf2125272f76bfad392e2f468f
- JOINT_RETAINED_RESULT.md

The correction changed one lower-bound explanation in the safe second macro: the environment label already hits the guard, while the fourth required label is needed to hit the remaining payload. The theorem and all hitting-number conclusions are unchanged.

Parent richer-factorization closeout:
- 3c1f302324e8560424d7a7fa3d22da64b84ff409

## Audit findings

1. Every source has tau=4: d,e are forced by singleton anchors, q forces a, and h forces x in {b,c}.
2. Every exact target has tau=4: payload targets b,c plus d,e supply four forced labels.
3. If the payload whose target equals x is repaired first, every primitive of both macros has tau=4.
4. If the other payload is repaired first, its addition leaves tau=4 but its deletion produces three distinct residual requirements a,x,y in addition to forced d,e, hence tau=5. A spectator on p cannot reduce this: replacing a by a spectator still requires five distinct labels.
5. M_core identifies x from the source miss-count pattern and updates under core edits without reading spectators.
6. D maps target labels b,c to the correct labelled payloads.
7. With D fixed, h=b versus h=c require opposite safe first payloads; therefore the aggregate certificate channel is genuinely active.
8. With one physical source fixed, D_bc versus D_cb require opposite labelled first payloads; therefore the address channel is genuinely active.
9. For fixed h,D, all 2^s spectator sets Z give identical retained M_core,D, floors and controller transcript but different full labelled source/target states. The combined retained record does not reconstruct the full incidence state.
10. Exact completion occurs after two complete macros=four primitive edits. The number of unfinished payloads decreases 2->1->0.
11. Necessity statements are correctly scoped to deterministic no-read complete-macro scheduling. Interleaved prefixes, probing, external reads and other native paths are not excluded.

No remaining mathematical correction was found in this author-side audit.

## Advancement

This is the first retained-information theorem in the continuation where BOTH channels do nontrivial work:

    aggregate certificate:
        determines which target TYPE must be established first;

    labelled address:
        determines which labelled payload carries that target obligation.

Neither channel subsumes the other in the selected policy, and together they still discard s spectator-incidence bits.

The safe schedule is therefore determined by a relation between global certificate state and exact labelled destination address, not by either alone.

## Next frontier

Generalize the two-payload precedence to a finite dependency system.

The next theorem should:
- derive a directed precedence graph among several labelled target obligations from retained certificate+address data;
- prove that an acyclic graph yields a terminating exact protected repair;
- define how the retained certificate and graph renew after each completed macro;
- preserve hidden full-state multiplicity after conditioning on the retained graph state;
- exhibit a directed cycle or other exact obstruction for this macro policy without overclaiming native disconnection.

No numerical campaign is authorized by this closeout.

Closed A12.1-A12.5, certified v16.54/v16.55 and accepted A11 remain unchanged. No A12.6 or physical force/geometry/energy/GR/ADM/dark-matter/continuum/fundamental-time claim.
