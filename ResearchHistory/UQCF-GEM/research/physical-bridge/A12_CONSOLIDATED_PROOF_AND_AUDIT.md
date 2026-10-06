# A12.1-A12.5 consolidated corrected candidate and author-side audit

Date: 2026-10-06 UTC.
Status: REVISED WRITTEN CANDIDATE R1; execution and closeout status are tracked separately in STATUS.md.
Attribution: ChatGPT authoring context. This is an author-side mathematical audit, NOT independent peer review or a formal proof-assistant certificate.
Prospective protocol: A12_SELF_CONTAINED_AUDIT_PROTOCOL.md at 291425d273412a65e98facc79bc368616200d7a1.
Source baseline: 62b6bec4bea5e6446680aec5694fbd0d8f096165. The protocol records all ten immutable scope/proof sources and blobs.

R1 correction: the original consolidated publication 5541843b2539cd714796d2e9c94d05741b2a49d8 substituted several A12.5 supports without disclosure. Section 6 now restores the exact original L and I supports. The existing transversal and witness arguments below apply to these originals. A source-fidelity test rejected the substitution before the full bounded campaign. The palette-cardinality bars in the ledger are escaped for correct Markdown rendering. No other mathematical claim is changed in R1; original documents and historical verdicts remain untouched.

This file is a new consolidated candidate. It does not silently replace the original proof/scope documents or change any historical external verdict. It supplies the complete arguments for the claims retained below, explicit corrections and narrowed conclusions, and the remaining evidence obligations. No external AI approval is used as a premise.

Prospective fixture clarification recorded before execution: the protocol's phrase 'five-root/six-label deletion fixtures' misdescribes the original A12.1 examples. The original upper-bound controls use FIVE labels, as transcribed in Section 2.3 below. The protocol's explicit requirement to reproduce all four original examples governs; no change to the primary universe, family range or resource budget is made. No verification had run when this clarification was first published.

## 1. Common definitions, domain and dependency boundary

Let P be a finite palette, I={1,...,m} a finite set of labelled root slots, and E=(E_i) an ordered family of subsets of P. Each original floor f_i is a fixed positive integer. An admissible root state satisfies |E_i| >= f_i, so EACH support is nonempty. Duplicate supports are allowed and root identity is retained.

A transversal is H subset P meeting every E_i. Write tau(E) for its minimum size. For diagnostic evaluation of an inadmissible toggle, tau(E)=+infinity if any support is empty. The empty root family has tau=0. These conventions do not admit empty supports into protected states. When all supports are nonempty, P itself is a transversal, so tau is finite and at most |P|.

The protected band is 3 <= tau(E) <= 4, together with the original floors. A protected state consequently has |P|>=3 and m>=3. No minimum palette is smuggled into a theorem stated for arbitrary finite states: the pair-certificate equivalence below explicitly assumes |P|>=2.

Incidence syntax and legality are different. Add(i,x) has syntax x not in E_i; Del(i,x) has syntax x in E_i. The indicator L_E(g) is 1 exactly when syntax is valid, the resulting floors hold, and the resulting hitting number is in [3,4]. Floor failure is not hidden by removing that deletion from the candidate set.

A response compares a protected state E and its state eE after a legal first move e. Candidate g changes a DIFFERENT incidence (root,label), is syntactically defined on both sides, and is not assumed legal. Distinct incidence toggles commute, including on the same root, so g(eE)=e(gE). This common endpoint is crucial.

Dependency ledger: Section 2 uses only these definitions and inclusion of supports. Section 3 proves its family directly from transversals, not from an accepted A12.1 result. Section 4 derives certificates directly from incidence and recovers Sections 2-3 where stated. Section 5 derives its tests directly from certificates with their explicit domain; its examples are also checked directly by transversals. Section 6 proves its indistinguishability construction directly. No pending A11 result, implementation, fitted statistic or physical assumption is a premise.

## 2. A12.1: signed admissibility response

### 2.1 Inclusion lemma

If E_i subset E'_i for every i, every transversal of E is a transversal of E'. Thus tau(E') <= tau(E), with the diagnostic infinity convention included. Addition weakly decreases tau; deletion weakly increases it. From a protected initial state, an addition can leave the band only through tau<=2; a floor-valid deletion can leave it only through tau>=5 (or infinity).

Define R_E(e->g)=L_(eE)(g)-L_E(g). For a legal e and the common-syntax candidate described in Section 1:

| First move e | Candidate g | Sign |
| --- | --- | --- |
| Add | Add | R <= 0 |
| Del | Del | R <= 0 |
| Add | Del | R >= 0 |
| Del | Add | R >= 0 |

Proof, Add/Add: if g is initially illegal, tau(gE)<=2. Since e adds a different incidence, g(eE)=e(gE) has larger supports than gE, so its tau is still <=2. An initially illegal candidate cannot become legal.

Proof, Del/Del: if g initially violates its floor, a distinct deletion cannot improve that floor slack. Otherwise illegality means tau(gE)>=5. Deleting e from gE cannot lower tau. Again an initially illegal candidate cannot become legal.

Proof, Add/Del: suppose g is initially legal. Adding e to gE cannot reduce floor slack and gives tau(g(eE))<=tau(gE)<=4. Conversely, g is a deletion from protected eE, so tau(g(eE))>=tau(eE)>=3. Thus g remains legal.

Proof, Del/Add: suppose g is initially legal. Deleting e from gE gives tau(g(eE))>=tau(gE)>=3. Conversely, adding g to protected eE gives tau(g(eE))<=tau(eE)<=4 and cannot violate a floor. Thus g remains legal. These arguments include same-root distinct-incidence moves.

### 2.2 Cross-root response and covariance

If e and g affect different roots, the receiving root's syntax and floor slack are unchanged. Any nonzero response therefore comes from the hitting-number condition. Same-root responses can additionally reflect the floor, which is not a global-certificate effect.

A root permutation sigma and palette permutation pi send E_i to pi(E_i) in slot sigma(i), carrying f_i with the slot. This maps every transversal and incidence candidate bijectively, preserving cardinality, floors and legality. Consequently R_(hE)(he->hg)=R_E(e->g), for h=(sigma,pi).

For fixed legal e, count over distinct common-syntax candidates: S=#{g:R=-1}, F=#{g:R=+1}, Q=F-S and M=F+S. The same bijection proves their invariance. They are dimensionless combinatorial counts, not measured physical observables.

### 2.3 All four original strict-sign controls

Roots below are numbered from 1; every floor is 1. Listed labels form the palette. The numerical values here are symbolic deductions, NOT executed numerical evidence.

Add/Add: E=({a},{b},{c},{d}), e=Add(3,a), g=Add(4,b). Initially tau=4. Each single addition permits a three-label transversal and leaves three disjoint supports, hence tau=3. After both, {a,b} covers and the first two singleton roots force tau>=2. Therefore the joint tau is 2 and R=-1.

Del/Add: E=({a},{b},{a,c},{d}), e=Del(3,a), g=Add(4,b). Initial tau=3, forced by {a},{b},{d}. Before e, g makes {a,b} a cover and the two singleton roots force tau=2. After e there are four distinct singletons, tau=4. Applying g then leaves the first three singleton roots {a},{b},{c}, covered by {a,b,c}; tau=3. Thus R=+1.

Del/Del: E=({a},{b},{c},{a,d},{b,e}), first move Del(4,a), candidate Del(5,b). Initially {a,b,c} covers and the first three singletons force tau=3. Either deletion alone introduces one additional forced singleton and gives tau=4. Both give five distinct singleton roots, tau=5. Hence R=-1.

Add/Del: E=({a},{b},{c},{d},{b,e}), first move Add(4,a), candidate Del(5,b). Initial tau=4. The candidate alone gives five distinct singletons, tau=5. The first addition gives tau=3 because {a,b,c} covers and its singleton roots force three labels. After both moves {a,b,c,e} covers and those four singleton requirements force tau=4. Thus R=+1.

Audit disposition: the sign theorem, cross-root qualification, all four examples and covariance have complete arguments. The scope/proof ambiguity about treating floor slack as syntax is resolved explicitly in Section 1. No stronger response magnitude or dynamics is claimed.

## 3. A12.2: collective-response hierarchy, corrected and narrowed

### 3.1 Family and exact endpoints

For every integer n>=2 use palette {a,b,c} and the n+3 original labelled roots

    R_a={a}, R_b={b}, C_0={c}, C_j={c} for 1<=j<=n,

all with floor 1. There are two R roots and n+1 C roots: n+3, NOT n+2. This corrects the original Section 2 count without changing the listed construction.

Take candidate g=Add(C_0,a) and interventions e_j=Add(C_j,a), j=1,...,n. These change distinct incidences and commute. After any intervention subset T, the unchanged singleton roots R_a,R_b,C_0 force a,b,c, and {a,b,c} is a cover. Thus tau=3 and every prefix is legal in every order.

After any proper subset T and then g, some untouched C_k with k>=1 still equals {c}. Together with R_a and R_b it forces three labels, and {a,b,c} covers. Candidate g remains legal. After the full set S and g, each C root contains a, so {a,b} covers. R_a and R_b are disjoint singleton roots, proving the lower bound tau>=2. Hence the full endpoint has EXACT tau=2 and g is illegal.

Let chi(T) be the legality indicator of g after T. Then chi(T)=1 for every proper T and chi(S)=0. Thus Delta(T)=chi(T)-chi(empty) is zero on proper subsets and -1 on S.

### 3.2 Mobius coefficients and the precise no-truncation claim

For U subset S put kappa(U)=sum_(T subset U)(-1)^(|U|-|T|)chi(T). For U=empty this is 1. For a nonempty proper U all values are 1, and the alternating sum is (1-1)^|U|=0. For U=S, the identically-one function would also give zero; changing only its top value from 1 to 0 subtracts one. Therefore:

    kappa(empty)=1;
    kappa(U)=0 for every nonempty proper U;
    kappa(S)=-1.

By the Boolean-lattice inverse formula chi(T)=sum_(U subset T)kappa(U), truncating to orders at most k<n predicts chi(S)=1 rather than 0. For every fixed k one may choose n>k (and n>=2). No fixed finite order is exact uniformly over this growing family of root counts. This is not unbounded order inside one fixed finite state.

Relabeling roots and palette bijects the intervention subsets and preserves their tau and chi, hence irreducible order and coefficients.

### 3.3 Withdrawn overinterpretation

The original Section 6 further says that the entire pairwise directed response graph cannot be a complete state descriptor. The family just proved does NOT establish that general assertion: zero individual responses e_j->g do not exhibit two different states with identical full labelled response graphs but different required outputs. Other entries, labels or repeated adaptive updates could carry information not tested by this argument.

Retained conclusion: fixed finite-order truncation of the candidate's intervention-cube response is not uniformly exact. Withdrawn from this candidate: the broader full-response-graph descriptor impossibility claim. That claim is neither proved nor refuted here and is not opened as new research during closeout.

Audit disposition: the native collective construction and exact coefficient theorem stand by the argument above; root-count metadata is corrected; empty-subset and growing-size quantifiers are explicit; the unsupported additional inference is removed. Historical external acceptance of the original text is not rewritten.

## 4. A12.3: exact certificate laws with explicit domain

### 4.1 Fields and band equivalence

On a finite palette with |P|>=2, define for every physical pair K subset P:

    W_E(K)=#{i:E_i intersect K is empty}.

For each H subset P with |H|<=4 define C_E(H)=1 when H hits every root, and 0 otherwise. Set mu_-(E)=min_(|K|=2)W_E(K) and N_4(E)=sum_(|H|<=4)C_E(H). The pair index set is nonempty under the stated hypothesis.

A pair K is a cover exactly when W_E(K)=0. If any cover has size 0 or 1, it can be extended to a physical pair because |P|>=2, and a superset of a cover is a cover. Therefore tau(E)>=3 iff W_E(K)>=1 for every pair. Also tau(E)<=4 iff N_4(E)>=1, directly from the definition of tau. On admissible nonempty supports the protected band is exactly mu_->=1 and N_4>=1, with floors still separate.

Counterexample to the old unrestricted wording: P={a}, E=({a}). There are no physical pairs, so universal pair protection is vacuously true, but tau=1. The missing palette hypothesis was a real defect. For |P|=2 no protected nonempty-support state exists because P covers. For |P|=3 the three singletons give a valid protected example. Empty-support diagnostics do not become admissible states; the extended tau convention only makes an illegal endpoint unambiguous.

### 4.2 Additions

Let e=Add(i,x) with x absent from E_i. Only root i changes. It ceases to be a K witness exactly when x is in K and E_i missed K. Hence

    W_(eE)(K)=W_E(K)-1_{x in K and E_i intersect K is empty}.

Such pairs have the form {x,y}, with y outside E_i and y!=x. Their exact number is |P|-|E_i|-1. The formula concerns a syntactically available addition; an attempted addition to a full root is not in its domain.

Every old cover survives root growth. A previously absent cover H is created exactly when H contains x, root i was missed by H before the edit, and all other roots were hit. Thus C only changes 0->1, and only the edited root can have been the unique missed root.

### 4.3 Deletions

Let e=Del(i,x) with x present in E_i. Root i becomes a new witness for K exactly when E_i intersect K={x}. Hence

    W_(eE)(K)=W_E(K)+1_{x in K and E_i intersect K={x}}.

These pairs are {x,y} for y outside E_i, giving |P|-|E_i| changed coordinates. In particular a deletion from a full root changes zero pair coordinates; this is consistent because no pair initially meets that root in only x.

A noncover cannot become a cover when a root shrinks. An existing H cover is destroyed exactly when E_i intersect H={x}; after deletion the edited root is missed. Thus C only changes 1->0.

The coordinate identities remain meaningful for a floor-forbidden deletion, including one making its root empty. That does not make the move legal.

### 4.4 Legality, bounds, response signs and collective interpretation

From a protected state, an addition cannot reduce N_4 and is band-legal exactly when every post-W coordinate remains >=1. A deletion cannot reduce W and is band-legal exactly when some small cover survives; it additionally requires its original root floor.

Each W coordinate changes by at most one, so mu_- can decrease by at most one under an addition or increase by at most one under a deletion. These are bounds for minima over the same complete pair index set. N_4 is nondecreasing under addition and nonincreasing under deletion but may change by more than one. No invariant sum of W and C is supplied or asserted.

To recover the response signs without hidden same-root assumptions, compare the COMMON candidate endpoint g(eE)=e(gE). A second addition can only further deplete W at the endpoint that made an addition candidate illegal; a second deletion can only destroy further covers or floor slack at an illegal deletion endpoint. For opposite directions, the endpoint's previously safe threatened channel can only improve; the other channel is protected by starting from legal eE. This is exactly Section 2's common-endpoint argument expressed through the two fields. It does not assume the candidate shadow or its scalar minimum is unchanged by a same-root edit.

In Section 3's family, W_E({a,b})=n+1 because C_0,...,C_n miss that pair. Each intervention removes one witness, leaving at least two after a proper subset and exactly one after the full set. Candidate g consumes one more, exhausting the coordinate only in the full case. The full legality conclusion still uses the proof that other pairs are protected, not just this one coordinate in isolation.

Relabeling maps pairs, covers and roots bijectively: W_(hE)(pi K)=W_E(K) and C_(hE)(pi H)=C_E(H). Therefore mu_-, the W-value multiset, N_4 and cover counts by size are invariant, and all update laws are covariant.

Audit disposition: the explicit domain repair resolves the displayed small-palette counterexample at the level of this written argument. This does not change the old external REVISE verdict, certify the earlier edit, or substitute for the bounded checks declared by the protocol.

## 5. A12.4: exact candidate margins and their limitations

### 5.1 Addition iff

For a syntactically valid candidate Add(i,x), define its shadow

    S_E(i,x)={{x,y}: y outside E_i, y!=x}

and A_E(i,x)=min_(K in S_E(i,x)) W_E(K), with min(empty)=+infinity. Exactly these coordinates lose one when the candidate is applied; every other coordinate is unchanged. In a protected initial state all W>=1, so the post-state has all W>=1 iff all shadow coordinates were >=2. The upper-cover condition cannot deteriorate under addition. Thus

    Add(i,x) is legal iff A_E(i,x)>=2.

An empty shadow means no lower coordinate is consumed and the candidate is legal. This is a stipulated minimum convention, not a finite value that may be used carelessly in subtraction.

### 5.2 Deletion iff

For a syntactically valid Del(i,x), let D_E(i,x) count the old covers H of size <=4 that also meet E_i minus {x}. These are exactly the covers remaining after deletion: all other roots are unchanged, and deletion cannot create covers. W cannot deteriorate. Therefore

    Del(i,x) is legal iff |E_i|-1>=f_i AND D_E(i,x)>=1.

A band-only test is insufficient. For example E=({a},{b},{a,c},{d}) has tau=3. Give the third root its original floor 2. Deleting a there produces four singletons and tau=4 but violates that floor. This is a concrete rejection fixture for floor-free legality.

Relabeling bijects each candidate shadow and surviving-cover family and transports floors; it therefore preserves A, D and candidate legality.

### 5.3 Exactly which threshold statement follows

For different-root interventions the candidate root, its shadow and floor slack are unchanged. Addition-candidate responses correspond exactly to crossing A>=2, and deletion-candidate responses to crossing D>=1 (with unchanged floor status). On the same root, candidate identity may remain fixed while its shadow and floor slack change. The two iffs remain valid, but neither a fixed shadow nor monotonicity of the scalar A may be inferred.

Explicit check: P={a,b,c,d}, E=({c,d},{c},{a},{b}), floors 1, g=Add(1,a), and legal e=Add(1,b). The three singleton roots force tau=3 before and after either/both additions. Initially the shadow of g is the single pair {a,b}; roots 1 and 2 miss it, so A=2. After e, the candidate shadow is empty, so A=+infinity. Thus a legal addition can INCREASE this candidate-centered scalar while W coordinates only decrease or stay unchanged. Candidate legality stays 1. This rejects a stronger scalar-monotonicity interpretation, not the legality iff or Section 2's sign theorem.

### 5.4 Global scalar insufficiency, with candidate identity held fixed

Original addition control: P={a,b,c,d}, E=({a},{b},{a,c},{d}), floors 1. Candidate Add(4,b) has shadow minimum 1: {a,b} has only root 4 as witness. It is illegal. Candidate Add(4,c) has shadow pairs {a,c},{b,c}, each with two witnesses, so minimum 2 and it is legal. Both candidates are in one state and share its global (mu_-,N_4).

To exclude the ambiguity that candidate label alone explains the difference, hold candidate g=Add(4,b) fixed and compare E with its relabeling E'=({a},{c},{a,b},{d}), obtained by swapping b,c. The two global scalars, palette, root count, original floors and initial tau are identical by covariance. In E', fixed g corresponds to the legal Add(4,c) in E, and is legal. Thus even the global scalar pair together with this fixed candidate identity does not determine legality uniformly.

Original deletion control: P={a,b,c,d,e}, E=({c},{a,b},{b},{e},{d}), floors 1, tau=4. Del(2,a) leaves a duplicate {b} and is legal at tau=4. Del(2,b) leaves the five distinct singletons {c},{a},{b},{e},{d} and is illegal at tau=5.

Again hold candidate g=Del(2,a) fixed. Swap a,b globally to obtain E'=({c},{a,b},{a},{e},{d}). The global scalar pair is unchanged; g now corresponds to the illegal old Del(2,b), so its legality changes. This completes the claimed scalar insufficiency without relying solely on two differently labelled candidates in one state.

This targets the PARTICULAR summaries (mu_-,N_4), not every pair of scalar encodings, not all global statistics, and not a minimality or observer-access theorem. The relabeling completion is part of this corrected candidate and is not attributed to the historical external reviewer.

## 6. A12.5: exact overlap-input impossibility

Use palette {a,b,c,d,e}, six roots labelled 0,...,5, all floors 1, and the SAME candidate g=Add(0,b). Define

    L: ({d}, {a,c}, {c,e}, {a}, {a,c,e}, {a,b});
    I: ({d}, {a,b,e}, {a,b,e}, {a,c,e}, {b}, {c}).

The root overlap graph joins distinct slots when their supports intersect. In both states d occurs only in root 0; its entire labelled connected component is the isolated support {d}, with the same floor. Hence all finite-radius overlap views at that root are identical, even if the entire component is supplied. Palette, root count, all floors and candidate identity/type are also identical.

For L, the roots {d} and {a} force d,a, and root {c,e} forces at least one additional label, so tau>=3. The set {a,c,d} covers every root, proving tau(L)=3.

For I, singleton roots {d},{b},{c} force three labels and {b,c,d} covers, so tau(I)=3. Thus the current tau supplied as side information is equal as well.

After g in I, {b,c} covers every root. Unchanged singleton roots 4={b} and 5={c} force two distinct labels; hence EXACT tau(gI)=2, not merely the upper bound <=2. Candidate g is illegal.

After g in L, root 3 still forces a. A two-label cover must also meet root 0={b,d}, so the only candidate pairs containing the forced a are {a,b} and {a,d}. Both miss root 2={c,e}. No smaller cover can work either. The triple {a,b,c} covers, so tau(gL)=3 and g is legal.

Consequently a function restricted to the candidate root's complete labelled overlap component, its floors, the palette (or just its size), total root count, current tau, and candidate identity/type would receive identical inputs on L and I but would have to return different answers. No such function can compute exact candidate legality uniformly. Any finite-radius-only rule is a special case and also fails.

Certificate explanation: pair {b,c} is missed only by root 0 in I, whereas roots 0 and 3 miss it in L. Candidate g destroys that last witness only in I. This explanation supplements the complete transversal proof; it is not a substitute for checking all possible pair covers in L.

The impossibility is restricted to the specified input. Remote supports or other global summaries are NOT given to the hypothetical rule. No impossibility for every locality notion, no physical nonlocality, and no new response-derived locality construction follows.

## 7. Refutation ledger and result dispositions

| Obligation | Exact disposition in this candidate | Remaining evidence |
| --- | --- | --- |
| A12.1 signs, floor effects, four controls, covariance | Complete author-side argument in Section 2; common incidence syntax made explicit | Declared bounded verifier and reporting audit |
| A12.2 root count | Original n+2 is incorrect for listed roots; corrected to n+3 | Automated fixture-metadata rejection |
| A12.2 subset/endpoints/coefficients/uniform quantifier | Complete general-n argument in Section 3; empty coefficient is 1 | Declared n=2,...,8 cube checks |
| A12.2 arbitrary full-graph insufficiency | Not established by the supplied family; withdrawn from retained conclusions | No new theorem or campaign opened |
| A12.3 pair-domain defect | Explicit \|P\|>=2 and nonempty legal supports; p=1 counterexample recorded | Domain/update/certificate checks |
| A12.3 updates, counts, band, bounds, covariance | Complete author-side argument in Section 4 | Direct-reference comparison |
| A12.4 iffs and scalar limitation | Exact with syntax/floor qualifications; fixed-candidate relabeling completion in Section 5 | Candidate, relabeling and floor controls |
| Stronger same-root A monotonicity | False; explicit 2-to-infinity example while legality stays unchanged | Reproduce example; do not claim this as an original theorem failure |
| A12.5 matched inputs and post-state values | Complete argument in Section 6; add explicit tau(gI)>=2 lower bound; R1 restores original supports | Input/component/endpoint checks |
| Protocol upper-fixture label count | Five labels in original upper controls; six-label wording corrected prospectively above | Implement actual frozen original fixtures |

These are the author's dispositions on the new consolidated candidate, not replacements for the external review's verdicts on older sources. Historical review and original source bytes remain unchanged.

## 8. Original publication checkpoint and subsequent verification

At original candidate publication: all ten source files had been audited; native arguments, explicit assumptions, dependency ordering, symbolic control reasoning, and the correction/narrowing ledger were written; the bounded verification protocol had been frozen before candidate publication. The subsequent R1 source-fidelity correction above is part of the audit history, not concealed by that earlier completion statement.

At that original checkpoint, the executable bounded verifier, its rejecting controls, a GitHub Actions run, deterministic reproduction, durable execution evidence, and final reporting/closeout audit were NOT completed. The 35,792-state figure was a prospective combinatorial scope count, not a performed campaign. Current execution results and remaining obligations belong in STATUS.md, A12_IMPLEMENTATION_LOG.md, and the immutable run evidence, not in this mathematical source's historical checkpoint text.

Final A12 closeout must say which claims are retained, corrected or withdrawn and distinguish written proof from finite corroboration. No force, geometry, energy, GR/ADM, dark-matter replacement, physical nonlocality, continuum or fundamental-time inference is made. No A12.6 is opened. Certified v16.54/v16.55 and accepted A11 remain unchanged.
