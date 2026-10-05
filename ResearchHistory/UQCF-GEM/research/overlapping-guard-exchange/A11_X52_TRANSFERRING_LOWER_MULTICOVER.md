# A11.X52 - three-cover renewal with transferring lower protection

Parent: 15fdd6fca655e868775339c6731b0b662558cddf.
Scope: 742ea5ed18d61ed01a164653b84bf8041b6653ed.
Exact analytical candidate for fresh whole-argument review.

The scope proposed conditional counting to enforce a four-type chain. During proof development, exact footprint localization revealed a stronger constructor: only ONE physical pair lacks a common endpoint-union witness, and two existing types protect it without conflicting with the upper chain. The main family proof below therefore needs no averaging over orders. The valid conditioned-count interface is retained separately in Section 8; it is not a claimed implementation or benchmark.

## 1. Fixed native carrier and statement

Fix m>=8 roles G={0,...,m-1}, ordered cyclically for this supplied template, and physical palette P={x_s:s in G}. Each role is singleton. Let pi be the PHYSICAL LABEL permutation
    pi(x_s)=x_(s-1),
indices modulo m. Thus C_i=pi(A_i) moves physical x_s from role s at the source to role s+1 at the destination. This convention distinguishes label relabelling from owner-role rotation.

Put K0={0,1,2,3}. For every four-role set J not equal to K0, declare n_J>=1 ORIGINAL labelled slots of type Q_J=G minus J. At the source and destination their physical supports are
    A_J={x_s:s not in J};
    C_J=pi(A_J)={x_s:s not in pi(J)},
where pi on role indices also subtracts one. Each copy has its SAME ORIGINAL positive floor a_(J,t)<=m-4. Uniform saturated floors m-4 and individually unequal lower floors are allowed. No root or label is added during repair.

**X52R.** Every such pair of endpoints admits a deterministic complete native path with 3<=tau<=4, original floors, full labelled/noncompact destination restoration, and exactly
    sum_J n_J |J symmetric-difference pi(J)|
single-incidence primitives, the unavoidable endpoint-toggle minimum.

The construction uses THREE physical four-cover witnesses on a type-block schedule and a transferring actual witness for the sole noncommon pair. Every type changes under the full rotation. The whole actual endpoint-union tuple has tau=2, so no subfamily of those unions is a permanent three-guard. The lower guard is supplied by changing actual relations, not an untouched background.

**X52S.** On the constructed schedule the smallest number of physical sets of size at most four capable of certifying tau<=4 throughout is exactly THREE. This is a schedule-relative certificate minimum. Another lower-safe schedule admits a two-cover relay. No all-order two-cover obstruction, new connectivity classification or native disconnection is asserted.

**X52N.** Every finite specified chain of forward rotations in the SAME cyclic role order renews this construction at restored endpoints, on the same original slots and floors. Each leg is minimum separately. Global minimum over an outer chain is not claimed.

Native primitives toggle one incidence in one slot. Larger supports are allowed. No simultaneous moves, compactness, added geometry, floor weakening or fundamental time is introduced.

## 2. Exact endpoints and supplied covers

At the source a four-label set with index set I misses Q_J exactly when I=J. Therefore the ONLY source four-cover is the physical set indexed by K0. No triple T hits every root: it has m-3>=5 four-set extensions, only one of which could be K0, so some declared J contains T and its complementary root avoids T. Smaller sets extend to triples. Thus tau(A)=4 and the minimum cover is unique.

Relabelling by pi gives tau(C)=4 and its unique physical four-cover
    K2=pi(K0)={m-1,0,1,2}.
Here and below index subsets name physical label sets {x_s:s in subset}. Positive original copies do not change these hitting sets.

Choose the intermediate physical four-set
    K1=L={0,1,4,5}.

For any physical four-set K, its source exception is exactly type Q_K if K!=K0, and empty if K=K0. Its destination exception is exactly type Q_(pi^-1 K) unless K=pi(K0). This follows because C_J has complement pi(J), so K misses C_J iff K=pi(J).

Define existing distinct types
    a=Q_L;
    b=Q_(pi^-1 K0)=Q_{1,2,3,4};
    c=Q_(pi K0)=Q_{m-1,0,1,2};
    d=Q_(pi^-1 L)=Q_{1,2,5,6}.
All four complement sets differ from K0 and from one another for every m>=8. The cover chain exceptions are exactly
    U_0=empty, V_0={b};
    U_1={a},   V_1={d};
    U_2={c},   V_2=empty.

Consequently a before b and c before d supply X51's cross-exception chain. Impose the stronger order
    a before b before c before d.
This also forces a completed boundary between b and c at which neither endpoint cover is available.

## 3. Exact lower-obligation localization

For a physical pair B={x_s,x_t}, s!=t, define its owner footprint
    F(B)={s,t,s+1,t+1}.
A type J's full physical endpoint union avoids B exactly when
    F(B) subset J.
Indeed avoiding B at the source requires s,t in J; avoiding it at destination requires s+1,t+1 in J.

If |F(B)|<=3, choose a four-set extension J!=K0. Such an extension exists: any triple has at least five extensions, and at most one is excluded. Its declared original type is a common actual witness, and its entire union misses B.

If |F(B)|=4 and F(B)!=K0, take J=F(B), a declared original type. Again its entire union avoids B.

The only remaining case is F(B)=K0. Since indices outside K0 cannot occur in the footprint, the two starts belong to {0,1,2}: start3 would also include4, and start m-1 would include m-1. The only two starts covering all four consecutive positions are 0 and2. Therefore the sole noncommon physical pair is
    B_star={x_0,x_2}.

For this pair, source missed-root types have complements containing {0,2}; destination missed-root types have complements containing {1,3}. A type in both would have complement K0, which was omitted. Thus its old and new witness sets are disjoint. There is no union-compatible root protecting this pair.

Choose two ACTUAL existing types
    v=Q_{1,3,4,6}, a destination witness for B_star;
    u=Q_{0,2,4,6}, a source witness for B_star.
Their complement sets differ from K0, are distinct from each other and from a,b,c,d for m>=8. This direct check uses the displayed four-sets; all labels 0,...,6 exist.

Impose v before u. The graph consisting of
    a -> b -> c -> d
and
    v -> u
has disjoint vertex sets and is acyclic. All other original types are isolated in this certificate, but may still change and may supply actual common pair witnesses. It is a graph of precedence obligations, not independent physical capacities.

Every pair other than B_star has the actual union witness derived above. B_star is protected by untouched source type u until destination type v completes; thereafter completed v protects it. During v's own edits u is still untouched. Thus a topological type order of this graph is lower-safe through every add-before-delete primitive. This is a direct structural application of the inherited actual first-new-before-last-old criterion, not an assumed safe-prefix extension.

## 4. Constructed order, actual copies and upper renewal

Construct the total type order by repeatedly choosing the least unchosen type with indegree zero in the remaining finite certificate graph. Such a type exists in every nonempty acyclic graph: otherwise following predecessor edges eventually produces a directed cycle. Removing a type preserves acyclicity. The remaining-type count strictly decreases. The graph therefore supplies every eligible next type and terminates.

Process each type's ORIGINAL copies as a complete block in labelled order. Within a copy add all absent C_J minus A_J labels, then remove all present A_J minus C_J labels, in palette order.

Upper cover choice can be explicit:
- before b's block, use K0;
- from b's block through all blocks before d, use L;
- from d's block onward, use K2.

Because a precedes b, when L first becomes necessary its sole source exception has completed. Because c precedes d, when K2 becomes necessary its sole source exception has completed. L's sole destination exception d has not completed or become active while L is used; K0's sole destination exception b is still ahead while K0 is used. These are exactly X51's coexistence conditions.

Each selected set hits BOTH endpoints of the active type, all earlier destination types and all later source types. Therefore it hits simultaneously present old copies, new copies and the active enlarged support. It proves tau<=4 at every primitive for arbitrary positive n_J.

Lower safety on actual copies is also explicit. A common union witness type has every copy avoiding its associated pair throughout its changes. For B_star, ALL u copies remain old until the v block has fully completed. Hence at least one actual old u copy avoids B_star until actual new v copies are installed; afterward one such new v copy persists. The active-copy representative proof of X49/X50/X51 gives the same conclusion. No witness is lost by the addition of more actual copies, and no separate capacity is allocated per pair.

This accounts for EVERY physical pair, including adjacent role pairs, disjoint pairs and B_star. Excluding every two-label hitting set excludes smaller sets too, since P has at least four labels. Thus tau>=3 throughout.

## 5. Original floors, primitive availability, termination and exact minimum

Every listed addition is absent and every deletion is present. During additions the active support contains its source of size m-4; during deletions it contains its destination of size m-4. Each copy's own original floor<=m-4 is retained, even at saturation. Common incidences stay fixed and every endpoint-differing incidence changes exactly once.

The finite type order, copy order and pending edit lists supply the actual next primitive whenever an edit remains. Zero-edit types would advance without a fictitious move, although this family has no unchanged type. The finite total of pending scheduled incidences decreases one at a time. Completion restores EVERY full destination support at its ORIGINAL labelled slot.

Complementation and relabelling preserve symmetric differences, so the number of primitives is
    sum_J n_J |A_J symmetric-difference C_J|
      =sum_J n_J |J symmetric-difference pi(J)|.
Every endpoint-differing incidence must toggle at least once on any native path. The construction attains this mathematical lower bound. No upper conversion or witness switch adds a primitive.

The actual root sizes may temporarily exceed their floors, as allowed natively. No same-slot floor vector, palette or labelled slot changes.

## 6. Absence of a permanent union guard and exact three-cover minimum

The entire source/destination union is hit by B_star. If some union root missed that pair, its four-set complement would contain F(B_star)=K0 and hence equal K0, but no such original root exists.

No singleton hits all unions: for x_s choose a declared four-set J containing {s,s+1} but not equal K0. There are C(m-2,2)>=15 such extensions and only one excluded set. Its union avoids x_s. Therefore
    tau((A_J union C_J)_J)=2.

The same pair hits every subfamily of these actual unions. Hence no collection of full endpoint-union supports forms a permanent three-guard. This is a precise union-compatible obstruction, NOT an exclusion of contracted auxiliary guards, all temporary constructions or native paths.

Every type changes. An invariant four-set under the full m-cycle pi would have to be empty or all G, impossible for size4 when m>=8. Thus J!=pi(J) for every declared type; there is no unchanged background root.

Now consider the completed boundary after the b block and before c. K0 misses a completed destination root of type b. K2 misses an untouched source root of type c. Hence neither endpoint cover works there. Source and destination each have a UNIQUE four-cover, so any family of only TWO physical sets of size at most four covering all states of THIS schedule would have to consist exactly of K0 and K2; it fails at this boundary.

Our sets K0,L,K2 do cover every state. Thus the exact minimum number of physical cover identities for this path is THREE. L need not be the unique middle cover; uniqueness is required only at the endpoints for this argument.

Another order with c before b has a two-cover relay. It can also respect v before u, since these four types are distinct, so the corresponding lower and upper certificate is acyclic. Thus this family is NOT an obstruction to every two-cover order. The three-cover result concerns retaining the deliberately constructed a<b<c<d schedule with its moving lower witnesses.

Native symmetry connectivity and complete lower-path conversion already connect these endpoints. The advance is a direct minimum-event multicover repair constructor without a permanent union three-guard, not a new native connectivity class.

## 7. Repeatability and full endpoint renewal

After one leg the actual roots equal the same fixed masks evaluated on another singleton role partition. The sole omitted role four-set remains K0. The source's physical role representatives can again be named x_s by their current roles. The next supplied forward rotation uses the same cyclic role order and the same physical-support/owner convention as Section 1.

All actual masks, positive original multiplicities, original floors, common-footprint rule, sole noncommon pair, six certificate types and three-cover exception identities therefore renew at the restored boundary. Existing labels are reused; none is added or consumed.

For every finite specified number of forward legs reconstruct the acyclic graph and process its type blocks. Every leg has eligible next choices and finite primitive lists, restores the exact labelled next endpoint and remains directly in {3,4}. Their finite concatenation reaches the supplied final endpoint. Primitive counts are minimum per leg; revisiting an incidence over several legs is not a globally minimum outer path.

Inside a leg protection can remain at level three; no exact-four reset after each block is required or claimed. This theorem does not promise arbitrary unfinished states, arbitrary reordered cyclic templates or arbitrary next endpoints are accessible.

## 8. Separate conditioned-order interface from the scope

The scope's counting proposal is valid but unnecessary for the explicit family. Record its correct general version to distinguish weighted extension choices from the equal-class argument used in unrestricted orders.

On q actual TYPES let Z be the number of noncommon physical-pair bad events, where each bad event puts all old witness types before all new witness types. For a uniform unrestricted type order,
    E[Z]=Psi=sum_B 1/C(|O_B|+|T_B|,|O_B|).
Let H be ANY nonempty supplied order constraint with unrestricted probability p_H>0. Nonnegativity gives
    E[Z | H]<=Psi/p_H.
If Psi<p_H, conditional extension averaging constructs a lower-safe order satisfying H.

For a generated prefix, valid extensions partition by eligible next type i. The weights are the numbers of valid extensions in each class divided by the total number, generally UNEQUAL. The conditional mean is their weighted average. Therefore an eligible positive-weight next type with nonincreasing mean exists. Choose the least such type, retain a mean below one and decrease remaining-type count. At completion Z is an integer below one, so zero. Evaluating extension counts may be expensive; this is not an efficiency implementation.

For the four distinct types a<b<c<d, p_H=1/24. The family's source and destination witness counts for any pair are at least rho=C(m-2,2)-1>=m-2. Thus the coarse bound
    24Psi<=24C(m,2)/C(2rho,rho)
            <=24C(m,2)/C(2m-4,m-2)<1
holds for m>=8. At8 the denominator is924 and numerator672. Increasing m multiplies the denominator by 4-2/(m-1)>3, while numerator multiplies by (m+1)/(m-1)<3; induction proves the strict margin.

This confirms the original prospective analytical approach, but Section 3 is stronger: it derives the exact single noncommon pair and explicit v/u edge, eliminating conditional counting from X52R. No numerical enumeration or execution was performed.

## 9. Dependencies, exact advance and remaining questions

Frozen X34/X35 provide the actual pair-order criterion. X49 retains the failed generic type-prefix copy lift; X50/X51 provide the actual-copy and multicover coexistence interfaces. Their domains match the construction: fixed palette, original labelled slots and positive same original floors, singleton exact-four endpoints, endpoint-containing one-incidence changes. No frozen proof is rewritten or recertified.

X52 removes the permanent-lower-background limitation of X51's demonstrated multicover family. It derives compatible old/new pair witnesses and the upper cover chain from the actual complementary masks, not from a supplied safe total order. It produces repeated direct completion on a structural infinite family with arbitrary positive original copies and saturated or unequal original floors.

This is still a dense complementary-four family. Arbitrary accessibility, sparse masks, unequal role cardinalities, all-order two-cover obstruction, an unbounded number of cover stages WITHOUT a permanent lower guard, and unrestricted mixed-floor/directed/higher-target/nested universality remain open. Failure of a supplied graph or relay means method failure, not native disconnection. The unchanged-group/symmetry connectivity theorem L and maximum-layer theorem A are comparisons only; A is not used on this direct path.

Next: retain the explicit actual-witness compatibility when additional complementary roots are absent, or derive an unbounded multicover family with transferring lower obligations. Do not treat remaining role counts as isolated campaigns.

Analytical only. No scientific commands/tests, numerical workflow, implementation, benchmark, integration merge, numbered certification, literature-originality or physical claim. Certified v16.55/v16.54 and all original evidence remain preserved. Separate efficiency runner/fixture/benchmark remains unstarted and separately scoped.
