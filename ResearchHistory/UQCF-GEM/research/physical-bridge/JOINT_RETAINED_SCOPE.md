# Joint retained-state factorization scope

Date: 2026-10-06 (America/Phoenix).
Status: PROSPECTIVE ANALYTICAL SCOPE.

Parent closeout: POST_A12_RICHER_FACTORIZATION_CLOSEOUT.md at 3c1f302324e8560424d7a7fa3d22da64b84ff409.

## Objective

Prove a bounded class where both an aggregate legality certificate and a labelled target-address record are needed for deterministic exact completion, while their combination still does not determine the full labelled incidence state.

## Selected class

Core palette: a,b,c,d,e. Add spectator labels T of size s>=1.

Fixed controlled roots are {d}, {e}, and {a,b,c}.

Residual labelled roots p,q,h all have floor1.

Source:
- p={a} union Z for arbitrary invariant Z subset T;
- q={a};
- h is either {b} or {c}.

Neither h nor Z is edited.

Target-address record D has one of two forms:
- D_bc: p core finishes at b; q core at c.
- D_cb: p core finishes at c; q core at b.

A payload macro replacing a by x is Add x followed by Delete a.

## Aggregate retained certificate

For every nonempty H among the five core labels with |H|<=4 retain

    M_core(H)=number of residual roots whose support misses H.

Spectator labels are omitted. Core edits update this field by subtracting the active root's old miss indicator and adding its new miss indicator.

At source:
- h={b}: M_core({b})=2 and M_core({c})=3.
- h={c}: M_core({b})=3 and M_core({c})=2.

## Required theorem

Uniformly for every Z:

For D_bc:
- h={b}: repair p to b first, then q to c. All states stay in 3<=tau<=4. The opposite complete-macro order reaches tau=5 after the first macro.
- h={c}: repair q to c first, then p to b. The opposite order reaches tau=5 after the first macro.

For D_cb exchange the labelled payload/target roles accordingly.

Controller uses D to know which labelled payload has which target and M_core to identify the environment label. It repairs the payload whose target matches h first, then the other. Prove exact completion in four incidence edits.

## Necessity controls

Certificate necessity: with D fixed, h={b} and h={c} require opposite safe first macros.

Address necessity: with one source fixed, D_bc and D_cb have identical source/M_core but prescribe different labelled targets and safe first labelled payloads.

Scope these statements to the deterministic no-read complete-macro policy.

## Hidden incidence multiplicity

For fixed h and D, all 2^s choices of Z give the same retained (M_core,D), floors and controller transcript, but different full labelled source/target incidence states. Z is preserved exactly without being read.

Thus both retained channels are active and still do not reconstruct the full state.

## Boundaries

Do not generalize to editing h, changing Z, arbitrary spectator placement, interleaved/probing policies, autonomous dynamics, observer access, geometry or physical force.

If successful, the next target is a multi-payload dependency system whose retained certificate induces a precedence graph and whose termination follows from that retained graph.
