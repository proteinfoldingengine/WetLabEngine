# A12.4 — exact candidate-centered admissibility margins

Date: 2026-10-06 UTC.
Status: analytical physics-bridge candidate for fresh independent whole-argument review.
Scope freeze: 5be2e81ff224761a0f9622104354ac804dc15bae.
Native derivation. A12.1-A12.3 are comparison candidates, not accepted dependencies.

No observer-accessibility, geometry, force, potential, energy, metric, continuum, numerical execution or implementation claim.

## 1. Candidate addition shadow

Let E be protected: 3<=tau(E)<=4. Let f=Add(i,x), x notin E_i.

Only physical pairs K containing x can lose a witness. Root i was a witness for K before f exactly when E_i intersect K=empty. Therefore the affected pairs are exactly

    Sh_-(i,x)={{x,y}: y in P minus (E_i union {x})}.

Define

    A_E(i,x)=min_{K in Sh_-(i,x)} W_E(K),

with A=+infinity if Sh_- is empty.

**A12.4A.**

    Add(i,x) is legal  iff  A_E(i,x)>=2.

Proof. Addition cannot violate tau<=4. Every unaffected pair retains its witness count. Every K in Sh_- loses exactly one witness, root i. Since E is protected, all W>=1. The post-addition state has every pair witness iff every affected W was at least2. This is exactly A>=2.

Thus a candidate addition needs only the weakest witness multiplicity in its own pair shadow, not the complete W field.

## 2. Candidate deletion surviving-cover margin

Let f=Del(i,x), x in E_i.

Define

    D_E(i,x)
      = #{H subset P:
            |H|<=4,
            C_E(H)=1,
            (E_i minus {x}) intersect H != empty}.

This counts existing small covers that still hit root i after x is removed. Every other root is unchanged.

**A12.4D.**

    Del(i,x) is legal
    iff
    |E_i|-1>=f_i
    and
    D_E(i,x)>=1.

Proof. Deletion cannot violate tau>=3. It is locally legal exactly at the floor inequality. Deletion cannot create a new cover; a pre-existing H survives exactly when it still hits the changed root, i.e. (E_i minus{x}) intersects H. Therefore tau<=4 after deletion iff at least one counted H survives.

Thus a candidate deletion needs its local floor slack plus the existence/count of covers surviving that particular deletion, not the complete C field.

## 3. Threshold-crossing response

These criteria convert admissibility response into candidate-margin threshold crossing.

For candidate addition f:
- in any protected state A_E(i,x)>=1;
- f is legal at threshold region A>=2 and illegal exactly at A=1.
A prior addition can only lower relevant W coordinates; a prior deletion can only raise them. Therefore Add->Add suppression crosses 2 to1, while Del->Add facilitation crosses1 to at least2.

For candidate deletion f:
- ignoring local floor, f is upper-legal exactly when D>=1;
- prior deletion can only destroy small covers, so suppression crosses D>=1 to0;
- prior addition can only create/preserve covers, so facilitation crosses0 to D>=1.
Same-root Add may also enable f by raising its floor slack from0 to1. Same-root Del cannot improve deletion floor slack.

For cross-root e->f, f's floor slack and incidence syntax are unchanged. Hence every nonzero cross-root response is exactly a threshold crossing in A or D caused by another root.

This is a move-centered form of global constraint mediation.

## 4. Relabeling covariance

Let g=(sigma,pi) simultaneously permute roots and palette labels, carrying floors with roots.

The addition shadow maps bijectively:

    Sh_-^(gE)(sigma(i),pi(x)) = pi(Sh_-^E(i,x)).

Witness multiplicities are preserved under this bijection, so

    A_(gE)(sigma(i),pi(x))=A_E(i,x).

Small covers map H->pi(H), and survival after deleting x from root i is preserved. Hence

    D_(gE)(sigma(i),pi(x))=D_E(i,x).

Floor slack is also preserved. Candidate-centered margins are therefore relabeling-invariant scalars attached covariantly to the candidate move.

## 5. Global scalar summaries are insufficient for individual move legality

The state-wide numbers

    mu_-(E)=min_K W_E(K)
    and
    N_4(E)=sum_(|H|<=4) C_E(H)

do not determine legality of a specified move class, because different candidates in the SAME state can have different candidate-centered margins while mu_- and N_4 are identical.

### Addition control

Take roots

    {a}, {b}, {a,c}, {d},

all floors1. The state has tau=3. Pair {a,b} has exactly one missed root, {d}, so mu_-=1.

On root {d} compare:
    f_b=Add({d},b),
    f_c=Add({d},c).

For f_b, its shadow includes {a,b}, whose witness multiplicity is1. Thus A(f_b)=1 and f_b is illegal: {a,b} would cover all roots.

For f_c, its shadow pairs are {a,c} and {b,c}. Each has two missed roots. Thus A(f_c)=2 and f_c is legal.

Both candidates are additions on the SAME original root in the SAME state, so mu_- and N_4 are identical for them. The global scalars cannot decide which addition is legal.

### Deletion control

Take roots

    {c}, {a,b}, {b}, {e}, {d},

all floors1. The state has tau=4: singleton roots {c},{b},{e},{d} require four labels, and {a,b} is hit by b.

On root {a,b} compare:
    f_a=Del(a),
    f_b=Del(b).

Deleting a leaves {b}; the roots are {c},{b},{b},{e},{d}, with tau=4, so f_a is legal.

Deleting b leaves {a}; the roots are five disjoint singletons {c},{a},{b},{e},{d}, with tau=5, so f_b is illegal.

Again both candidates share the same root, state, mu_- and N_4. Their surviving-cover margins differ: D(f_a)>=1 while D(f_b)=0.

Therefore no state-wide pair of scalars (mu_-,N_4) is sufficient for individual move legality without candidate-specific structural information.

This does not prove that A and D are information-theoretically minimal sufficient statistics.

## 6. What has actually been compressed

The full incidence state can be very large. For one candidate move, exact band legality factors through:

Addition:
    E -> candidate shadow witness counts -> A_E(i,x) -> legal/illegal.

Deletion:
    E -> candidate surviving covers + local slack -> (D_E(i,x), |E_i|-f_i) -> legal/illegal.

This is an exact candidate-centered sufficient response state. It is not yet an internally accessible observable. Computing A or D from scratch may require global relational information.

That distinction is essential: mathematical sufficiency is not operational accessibility.

## 7. Physics-facing consequence and next gate

The response of one candidate to another can now be described as movement of a candidate-centered margin across a discrete admissibility threshold.

A cross-root intervention changes another root's candidate margin without changing that root's floor or incidence syntax. This is a precise relational influence mediated by shared global constraints.

But A and D are not physical potentials, forces, energies or distances. They are dimensionless certificate margins.

The next falsifiable question is:

    Can A_E(i,x) or the deletion-survival predicate D_E(i,x)>=1
    be reconstructed from bounded retained information around the candidate,
    uniformly as system size grows?

A positive theorem would supply a genuinely compressed observer-accessible candidate state. A no-go would show that exact response remains globally dependent and that any local physical description must be approximate, symmetry-reduced, or coarse-grained.

That locality/closure gate should precede any attempt to fit distance laws or identify gravity.

No fundamental time is introduced; only ordered relational updates are used.

v16.54/v16.55 and accepted A11 remain unchanged. Pending X62-X64 and A12.1-A12.3 are not promoted. Separate efficiency work remains unstarted.
