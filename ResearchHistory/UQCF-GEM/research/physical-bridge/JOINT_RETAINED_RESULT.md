# Joint retained-state factorization theorem

Date: 2026-10-06 (America/Phoenix).
Status: ANALYTICAL RESULT CANDIDATE WITH COMPLETE ARGUMENT.
Scope freeze: JOINT_RETAINED_SCOPE.md at 0fa27e915b77742e21657c91bfd49b4cf0f6a1e5.
Evidence: written mathematics only.

## 1. Carrier and retained data

Core labels are a,b,c,d,e. Spectator set T has s>=1 labels.

Fixed controlled roots:
    A={d}, B={e}, G={a,b,c}.

Residual roots:
    p={a} union Z, with arbitrary invariant Z subset T;
    q={a};
    h={x}, where x is b or c.

All floors are1.

Address D prescribes distinct payload targets b,c:
- D_bc: target(p)=b, target(q)=c;
- D_cb: target(p)=c, target(q)=b.

The exact target preserves Z and h.

For nonempty H subseteq {a,b,c,d,e}, |H|<=4, retain

    M_core(H)=#{r in {p,q,h}: S_r intersect H=empty}.

The retained state is (M_core,D,phase) plus immutable carrier metadata. Z is not retained.

## 2. M_core identifies the environment but not Z

At source p and q both contain core a.

If h={b}:
    M_core({b})=2,
    M_core({c})=3.

If h={c}:
    M_core({b})=3,
    M_core({c})=2.

Therefore M_core determines x in this class.

For every fixed x and D, all Z subseteq T give exactly the same M_core because H contains core labels only and Z is disjoint from them.

Thus M_core identifies the scheduling-relevant environment core but contains no spectator information.

## 3. Exact source and target hitting numbers

At every source, singleton roots {d},{e} force d,e. Root q={a} forces a. Environment h={x}, x in {b,c}, forces x. These four labels are distinct.

They form a four-cover: {a,x,d,e} hits p through a, q through a, h through x, G through a or x, and the anchors.

Hence every source has
    tau=4.

At either exact target, payload cores are b and c, environment is one of b,c, and anchors force d,e. Thus b,c,d,e are forced by the two payloads plus anchors and form a four-cover. Therefore every target also has
    tau=4.

Z never changes these lower bounds because it occurs only in p and cannot remove any forced singleton requirement.

## 4. Safe-order theorem

Let P_x denote the labelled payload whose prescribed target under D equals the environment label x. Let P_y be the other payload, whose target y is the other element of {b,c}.

**Theorem.**
The complete-macro order

    P_x first, then P_y

has hitting number4 after every primitive. Reversing the first macro gives

    (tau_source, tau_after_add, tau_after_delete)=(4,4,5).

This holds for every Z subseteq T.

### Safe first macro

Before editing, the unedited other payload is singleton {a}; h is singleton {x}. Together with anchors they force
    a,x,d,e.

After adding x to P_x, those same four labels still hit every root and remain forced by the other payload, h and anchors. tau=4.

After deleting a from P_x, P_x contains x (and possibly Z if P_x=p). The other payload still forces a and h forces x. Again a,x,d,e are forced and cover. tau=4.

### Safe second macro

Now P_x and h both contain x. The remaining payload starts at {a} (or {a} union Z if it is p).

After adding y to P_y, anchors force d,e and h forces x. To hit P_y one needs a or y unless its spectator Z is used when P_y=p. If a spectator is used, G={a,b,c} still requires one core label among a,x,y, so at least one fourth label is required beyond d,e,x. Hence tau>=4.

A four-cover exists:
    {d,e,x,a}
after the addition, because P_y still contains a and P_x contains x.

After deleting a from P_y, its core is y. Singletons/cores x,y together with anchors force d,e,x,y, which form a four-cover. tau=4.

Thus the safe complete schedule has sequence
    (4,4,4,4,4).

### Wrong first macro

Instead repair P_y first.

After Add y, the unedited P_x still contains a, h forces x and anchors force d,e. The set {a,x,d,e} is still a four-cover, so tau=4.

After Delete a from P_y, residual core requirements are:
- P_x: a (plus Z only if P_x=p);
- P_y: y;
- h: x.

The anchors force d,e. Since a,x,y,d,e are five distinct core labels, any hitting set using a to hit P_x has size at least5.

Could a spectator z in Z replace a? Only p can contain spectators. If P_x=p, replacing a by z still requires z,x,y,d,e, again five distinct labels. If P_x=q, it has no spectator and a is mandatory.

A five-cover exists: {a,x,y,d,e}. Therefore
    tau=5.

So the wrong complete macro exits the protected band exactly at its deletion.

This proves the order theorem for both D_bc and D_cb uniformly.

## 5. Deterministic joint controller

From M_core({b}),M_core({c}), identify x:
- value pattern (2,3) means x=b;
- pattern (3,2) means x=c.

From D, identify the labelled payload P_x whose exact target is x.

Execute its two-edit macro, then execute the other payload's two-edit macro.

Section4 proves all four primitives remain in 3<=tau<=4 and respect floors.

After four edits:
- p has its prescribed target core plus the unchanged Z;
- q has its prescribed target core;
- h is unchanged;
- controlled roots are unchanged.

Thus the exact labelled destination is reached.

A two-step macro rank, or simply the number of unfinished payloads, decreases from2 to1 to0. No cycling is possible.

## 6. Exact M_core update without Z

For a core edit changing active residual support S to S' only by a core incidence, for every retained core H:

    M_core'(H)
      = M_core(H)
        - 1_{S intersects H is empty}
        + 1_{S' intersects H is empty}.

Because H contains no spectator labels, whether S intersects H depends only on the active root's retained core state. Z is irrelevant.

Thus the aggregate certificate is update-closed under the selected macros without reading Z.

## 7. Both retained channels are necessary for this policy

### Aggregate certificate necessity

Fix D_bc.

World B has h={b}; safe first payload is p.
World C has h={c}; safe first payload is q.

They have the same D, same controlled roots, same payload source cores and may use the same Z. A controller denied M_core/environment information sees identical allowed address data and must choose the same first complete macro.

Whichever payload it chooses, Section4 shows one world reaches tau=5 after that macro's deletion.

Thus D alone cannot guarantee protected completion in the declared deterministic no-read complete-macro policy.

### Address necessity

Fix source environment h={b} and one Z.

Under D_bc, the payload targeting b is p, so p must go first.
Under D_cb, the payload targeting b is q, so q must go first.

The physical source and M_core are identical. A controller denied D cannot know which exact labelled target is requested and must make the same first labelled choice in both target tasks. That choice is wrong for one task under the selected complete-macro policy.

Thus M_core alone cannot guarantee both exact labelled destinations.

These are policy-information lower bounds, not native-connectivity impossibility theorems.

## 8. The two retained channels still do not reconstruct the full state

Fix x and D.

For every Z subseteq T:
- M_core is identical;
- D is identical;
- all floors are identical;
- the controller chooses the same labelled macro order;
- the core edit transcript is identical.

There are exactly
    2^s
different full labelled source states distinguished by p's spectator incidences and 2^s corresponding exact targets.

The controller preserves each Z exactly without reading it.

Therefore conditioning on BOTH active retained channels (M_core,D) still leaves s hidden incidence bits and 2^s full states indistinguishable.

This is the desired nontrivial factorization:

    aggregate scheduling certificate
    + labelled target address
    + invariant hidden-state promise
    -> exact terminating completion,

without reconstruction of the full incidence state.

## 9. What the aggregate certificate is doing

M_core is not merely carried along. Its value selects the safe precedence.

The environment root creates a global upper-bound dependency:
- once one payload has moved away from a, the other payload must not also leave a until one of their target labels duplicates the environment label;
- repairing the payload whose target equals x creates that duplicate first.

The retained miss field identifies x and therefore resolves the precedence.

The address record then maps that abstract target label x to the correct labelled payload.

So the two information channels have distinct operational roles:
    M_core: WHICH target type must be established first;
    D: WHICH labelled root carries that target obligation.

## 10. Limits and next frontier

The result is intentionally small:
- one binary environment choice;
- two payloads;
- one hidden spectator family on p;
- complete two-edit macros only.

It does not cover editing h, changing Z, arbitrary spectator placement, interleaving the wrong macro prefix with another repair, or arbitrary endpoints.

The next mathematical target is a finite multi-payload dependency system where aggregate certificate data induces a directed precedence graph among labelled target obligations. The desired theorem is:
- derive the graph from retained certificate+address data;
- prove a topological/renewal condition for exact completion;
- preserve hidden incidence multiplicity after conditioning on the retained graph state;
- exhibit a cycle or obstruction showing where that retained scheduling rule stops.

No physical force, geometry, energy, observer field or fundamental time is inferred.
