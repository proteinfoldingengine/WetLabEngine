# Post-A12 dynamic residual: exact miss-count update theorem

Date: 2026-10-06 (America/Phoenix).
Status: ANALYTICAL RESULT CANDIDATE WITH COMPLETE ARGUMENT BELOW.
Scope freeze: POST_A12_DYNAMIC_RESIDUAL_SCOPE.md at 716ff49fe1b1105695945d3ee7e808a927820cfa.
Evidence type: written mathematics and symbolic controls only. No numerical campaign, implementation, benchmark, independent review, or physical validation.

## 1. Domain and retained field

Let P be a finite palette, k=|P|>=4. Split the current labelled roots into:
- explicitly retained controlled roots C_1,...,C_q, including the prepared X2 anchors/guards when that carrier is used;
- residual labelled roots r in R with nonempty supports S_r and immutable positive original floors f_r.

For every nonempty H subset P with |H|<=4 define

    M_R(H)=#{r in R : S_r intersect H = empty}.

This one field contains two kinds of residual certificate data:
- for a physical pair K, M_R(K) is exactly the number of residual roots witnessing that K fails to cover;
- for any H of size<=4, M_R(H)=0 exactly when H hits every residual root.

M_R is derived information. No claim is made that it is minimal, compressed, efficiently initialized, or observer-accessible.

A declared residual edit names one root r and supplies/tracks its current active support S_r and floor. No other residual support is read.

## 2. Exact local update law

Suppose the named residual root changes from S to S' by one native incidence toggle. Every residual root other than r contributes the same miss indicator before and after. Therefore for every retained H,

    M_R'(H)
      = M_R(H)
        - 1_{S intersect H = empty}
        + 1_{S' intersect H = empty}.                 (1)

This uses only the old count and the named active root's old/new support.

### Addition

Let S'=S union {x}, x notin S. A miss can only disappear. It disappears exactly when x in H and S intersect H=empty. Hence

    M'(H)=M(H)-1_{x in H and S intersect H=empty}.

All other coordinates are unchanged.

### Deletion

Let x in S and S'=S minus {x}. A new miss appears exactly when x in H and S intersect H={x}. Hence

    M'(H)=M(H)+1_{x in H and S intersect H={x}}.

All other coordinates are unchanged.

After the toggle, replace the active-root working support S by S'. Repeating (1) therefore updates M through any supplied finite sequence of declared edits on that active root without rereading the other residual supports.

If a later operation names a different residual root, this theorem requires its then-current support to be supplied or already retained by the broader controller. It does NOT prove how an autonomous controller discovers that hidden support.

## 3. The old F_R table is a zero-set projection of M_R

For an unordered pair U,

    F_R(U)=1

exactly when there exists H subset P with
- |H|<=4;
- U subset H;
- H minus U nonempty;
- M_R(H)=0.

The last condition is precisely that H hits every residual root.

Thus F_R is derivable from the zero set of M_R. The converse need not hold: F records only whether at least one eligible zero coordinate exists for each pair, not how many residual roots miss the other H coordinates.

Section 5 gives an exact same-record counterexample proving that this loss matters as soon as a residual root changes.

## 4. Exact protected-band reconstruction

Let E be the full current state consisting of the explicit controlled roots C_j and residual family R.

### Lower side

For every physical pair K,

    W_E(K)
      = M_R(K)
        + #{j : C_j intersect K = empty}.              (2)

Both terms count disjoint actual roots, partitioned into residual and controlled slots.

Because k>=4,

    tau(E)>=3
    iff
    W_E(K)>=1 for every |K|=2.                         (3)

If a hitting set of size0 or1 existed, extend it to a two-label set; conversely W_E(K)=0 says K itself hits every root.

### Upper side

For every nonempty H with |H|<=4,

    H hits every full-state root
    iff
    M_R(H)=0
    and
    C_j intersect H != empty for every controlled root j.   (4)

Therefore

    tau(E)<=4

iff at least one retained H satisfies (4).

Equations (2)-(4) show that M_R plus the explicit controlled supports reconstruct exactly the two global certificate tests needed for 3<=tau<=4. No full residual incidence state is required for those tests.

## 5. Exact insufficiency of F_R

Use P={a,b,c,d,e}. There are the same three labelled residual slots r0,r1,r2, all floors1. The controlled prepared state is identical in both cases:

    anchors {d},{e};
    guards {a,b,c},{a,b,c}.

State A residuals:

    r0={a}, r1={a}, r2={b}.

State B residuals:

    r0={a}, r1={a}, r2={c}.

The named active root is r0 in both states, with the same current support {a}. Declare the same two primitives:

    Add(r0,b), then Del(r0,a),

so r0 follows {a}->{a,b}->{b}.

### Same old F_R

In A, {a,b} hits every residual root. For any unordered U, H=U union {a,b} has size at most4. If H=U (only when U={a,b}), append c. Thus an eligible size<=4 residual cover containing U and an extra label exists. Hence F_A(U)=1 for every U.

In B, the same argument uses residual cover {a,c}; if U={a,c}, append b. Hence F_B(U)=1 for every U.

So the complete old F table, palette, residual-slot identities/count, floors, controlled state, active-root support and declared edit sequence are identical.

### Same protected start

In either full prepared state, anchors force d,e. State A residual singleton requirements force a,b; state B forces a,c. Thus every cover has size at least4. Respectively

    {a,b,d,e}
and
    {a,c,d,e}

are four-covers and hit the guards. Therefore both starts have tau=4.

### Same safe first primitive

After Add(r0,b), A residuals are {a,b},{a},{b}; B residuals are {a,b},{a},{c}.

A still forces a,b and B still forces a,c, in addition to anchors d,e. The same four-covers displayed above remain valid. Hence both intermediate states have tau=4.

### Different second-primitive legality

After Del(r0,a):

A residuals are {b},{a},{b}. They force a,b. With anchors d,e, tau remains exactly4.

B residuals are {b},{a},{c}. These three singleton residuals force a,b,c, while the anchors force d,e. Every hitting set therefore has all five labels, and P itself is a cover. Thus tau=5.

So the SAME retained F record and SAME declared residual edit require different legality decisions at the second primitive.

The updated F tables also differ. Final A still has residual cover {a,b}, so its F table is all true. Final B requires a,b,c to hit its residual singleton roots. For U={d,e}, every residual cover containing U must contain a,b,c as well, requiring five labels. Therefore

    F_B'({d,e})=0.

This proves F_R is not an exactly updateable retained state for changing residual roots.

The failure is information-theoretic for the declared input: no deterministic rule using only the identical allowed records can output both correct answers.

## 6. Exact legality/updateability theorem

**Dynamic residual retained-certificate theorem.**

Given:
- P and original floors;
- the explicit current supports of all controlled roots;
- M_R(H) for every nonempty H with |H|<=4;
- a declared active residual root's current support and floor when that root is to be edited;
- finite phase memory,

the controller can decide and update the exact target-four protected-band legality of every declared single-incidence edit to a controlled or active residual root without rereading any other residual support.

### Residual edit

Check native syntax on the supplied active support. For deletion also require |S|-1>=f_r. Compute the prospective M' by (1). Controlled supports are unchanged. Apply (2)-(4) to M' and the controlled supports. The edit is protected-band legal exactly when both tests pass. If accepted, commit M:=M' and S:=S'.

### Controlled-root edit

M_R is unchanged. Check syntax and that controlled root's original floor. Update that one explicit controlled support prospectively and apply (2)-(4). If legal, commit the controlled support update.

Thus the retained record is closed under the declared update operation.

This theorem certifies legality and state update. It does NOT choose which residual root to activate, infer an unretained support, or prove a route to an arbitrary endpoint.

## 7. Edge cases and accounting

### Empty residual family

M_R(H)=0 for every retained H. Equations (2)-(4) reduce to the explicit controlled roots. There is no residual edit to perform.

### k=4

Retain all nonempty H subset P, since every such H has size<=4. The same equations hold. No spare fifth label is assumed by the theorem. The F-insufficiency control itself uses k=5, as disclosed.

### Saturated residual floor

If |S|=f_r, a deletion is rejected locally before any band test. An addition may create one unit of slack and updates M by the exact addition rule.

### Record size

The field has

    sum_{h=1}^{min(4,k)} binomial(k,h)

integer coordinates, each in {0,...,|R|}.

This is finite and independent of the number of residual INCIDENCES in its coordinate count, but its integer widths depend on |R|. No storage-efficiency or compression claim follows. For some domains it may retain enough aggregate information to reconstruct more than the present task needs.

### Initialization

Computing M initially can require a global read of R. This theorem concerns exact updateability after a correct initialization. It does not solve observer access.

## 8. What advanced and what remains open

The fixed-residual result retained only existential residual-cover information F_R. The present theorem identifies exactly why that record fails under residual changes and replaces it with an update-closed certificate field.

The important distinction is:

    existential cover bit F_R
        is sufficient while R is frozen,

whereas

    residual miss count M_R
        carries the multiplicity needed to remove/add one root's contribution exactly.

Because pair coordinates M_R(K) are included in the same field, the broader record also tracks the residual contribution to the lower bound; no separate residual W table is needed.

This closes the narrow UPDATEABILITY question for declared single-incidence residual edits.

It does NOT close the broader scheduling problem. In particular it does not prove:
- a terminating rule selecting residual roots and edits toward arbitrary full endpoints;
- that the active root's support can be learned without a declared read/retention mechanism;
- minimality of M_R;
- efficient initialization;
- universal compression;
- accessibility by an internal observer;
- any physical interaction, geometry or force law.

The next theorem-first frontier is therefore selection/completion under retained information: specify a broader endpoint class and ask whether a controller using an update-closed record can choose a finite legal sequence to the exact destination without consulting hidden residual supports. If the controller must know candidate root supports to choose among them, that information requirement must be stated rather than hidden.

No numerical campaign is required for the closed-form statements above. Author-side whole-argument audit and immutable publication readback remain to be completed before calling this scoped item analytically closed.

Closed A12.1-A12.5, certified v16.54/v16.55 and accepted A11 sources remain unchanged. No A12.6 is opened and no fundamental time is introduced.
