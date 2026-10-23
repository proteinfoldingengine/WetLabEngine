# Shifted boundary response under prefix-tree pruning

**Status:** consolidated analytical draft, 2026-10-23. Not independently accepted or physically realized. Native bridge **NOT_DERIVED**. No scientific code, enumeration or new experiment has been run for this package.

**Authors and provenance:** ChatGPT research session with Aaron (distinct from dot): T-075, T-077 and T-078; Grok: T-076 corrections and Proposition M; dot: scoped source audit and the nonadditive-statistic/counterexample checks. Exact sources and outstanding checks are in §9. Standard Schur elimination, spectral calculus and inequalities are used; no mathematical novelty priority is claimed.

## 1. Question, premises and result

For the existing unweighted tree Laplacian, what hidden-tree information is needed to preserve a boundary resolvent after eliminating a pendant forest?

All uses below are confined to these premises:

- **P1 — INHERITED:** finite rooted prefix-CLOSED trees X ⊇ W ⊇ Y, with the same root; nearest-retained-ancestor retraction r and additive fiber pushforward P. Producing operation: ancestral contraction, ResearchHistory/UQCF-GEM/foundational-closure-verification/PROOFS.md §P1 at commit 3ceb814258f43774b4af1352379ffcd0bd079599.
- **P2 — INHERITED mathematical diagnostic:** unweighted parent-child incidence Laplacian L, with quadratic form equal to the sum of squared edge differences. Source: the same PROOFS.md §P4 and SHA. Its physical constitutive selection is not derived.
- **P3 — INHERITED mathematical maps:** actual retained inclusion, array zero extension I, and potential restriction I^T. Producing operations: retention inclusion and restriction, the same PROOFS.md §§P2/P6 and SHA. This does not assign a physical source or receiver.
- **P4 — SUPPLIED analytical question:** for real s>0, study G_Y(s)=I^T(L_X+s Id_X)^(-1)I and formal scalar comparisons j^T G_Y(s)j for specified real j on Y. The coordinate identity is the ordinary identity on this fixed diagnostic domain. s is dimensionless, not physical frequency, a fundamental clock or an event law.
- **P5 — SUPPLIED analytical definitions:** for fixed original X, m_a=|r_XW^(-1)(a)| and k_a=Σ_e n_e², where the edges are those in the discarded forest anchored at a, including each attachment edge, and n_e counts original descendants below that edge. No physical ledger implementing, storing or exposing these statistics is assumed.
- **P6 — SUPPLIED examples:** the explicitly listed trees and source j=(1,-1) in §§6–7 are formal comparisons, not physically preparable states or proven initially indistinguishable receiver states.
- **P7 — ACCEPTED INPUT, unused:** actual atemporal measurement/pruning occurrence. Occurrence does not supply event typing, preparation, access or outcome probabilities.

The conclusions under P1–P5 are:

1. The exact boundary operator has the form S_Y(s)=G_Y(s)^(-1)=L_Y+s Id_Y+diag(φ_a(s)).
2. Its first two corrections are S_Y(s)=L_Y+s diag(m)-s² diag(k)+O(s³).
3. The defined statistics admit an exact local update and a batch formula independent of leaf-elimination order.
4. Y,m,k give rigorous response enclosures for every s>0 and a guaranteed separation interval when k differs at fixed m.
5. They do not determine the exact response, even with the discarded-child count added; §7 gives an explicit pair.

These are consequences of a supplied resolvent question about an inherited diagnostic. They do not derive a new native observation.

## 2. Exact elimination and the shape coefficient

Use P1–P4. Order X as (Y,H), H=X\Y, and write

    L_X = [[A,B],[B^T,C]].

For H nonempty, C is positive definite: grounding Y gives a sum of squared edge differences, including attachment edges. A zero-energy vector must vanish throughout each component because every component attaches to Y. Block elimination therefore gives

    S_Y(s) = A+s Id_Y-B(C+s Id_H)^(-1)B^T,
    G_Y(s) = S_Y(s)^(-1).                                      (1)

Both inverses exist for s>0. If H is empty, set all forest corrections to zero.

Prefix closure means each component of H has exactly one retained anchor. For anchor a let H_a be its forest, b_a the indicator of its discarded children, and d_a=b_a^T b_a. Then B^T e_a=-b_a and A=L_Y+diag(d). The all-ones vector on H_a satisfies C_a 1=b_a; hence C_a^(-1)b_a=1. Different anchors have disjoint blocks. Thus

    A-BC^(-1)B^T = L_Y,
    W=-C^(-1)B^T has anchor-indicator rows,
    Id_Y+BC^(-2)B^T = Id_Y+W^T W = diag(m).                     (2)

This also derives the static term directly, consistent with FCV P6. Expanding the inverse near zero, within |s|<λ_min(C), yields

    S_Y(s)=L_Y+s diag(m)-s² K+O(s³),
    K=BC^(-3)B^T=W^T C^(-1)W=diag(k).                         (3)

To establish the last equality without spectral assumptions, solve C_a z=1 with the anchor grounded. Sum its equations below a discarded edge e. Internal edge terms cancel; the potential jump across e equals n_e. Therefore

    1^T C_a^(-1)1 = z^T C_a z = Σ_e n_e² = k_a.               (4)

In particular k_a>0 iff H_a is nonempty, equivalently a has a discarded CHILD. Merely having a discarded descendant is insufficient: for o→a→u retained at {o,a}, k_o=0 and k_a=1.

Prefix closure is essential. On o→u→v with Y={o,v}, eliminating u gives the matrix with diagonal 1/2 and off-diagonal -1/2; the extension row is (1/2,1/2), not an anchor indicator. This non-prefix example lies outside P1.

For any proper contraction, B≠0 and

    S_Y''(s)=-2B(C+s Id_H)^(-3)B^T ≠ 0.                        (5)

Thus no s-independent matrix M makes S_Y(s)=L_Y+sM on an open positive interval. The count matrix is a first-order approximation, not an exact replacement.

## 3. What the complete family determines (Grok's Proposition M)

Use §2 and the finite spectral decomposition of the positive matrix C_a. Define the positive atomic measure

    μ_a=Σ_λ ||E_λ b_a||² δ_λ.

For an empty forest set μ_a=0. Equations (1)–(2) give

    φ_a(s)=d_a-∫(λ+s)^(-1) dμ_a(λ)
          =∫ s/[λ(λ+s)] dμ_a(λ),                              (6)
    ∫dμ_a=d_a,   ∫λ^(-1)dμ_a=d_a,
    ∫λ^(-2)dμ_a=h_a=m_a-1,   ∫λ^(-3)dμ_a=k_a.                 (7)

Indeed the first inverse moment is b_a^T 1=d_a, the second is ||1||²=h_a, and the third is (4).

With the retained vertices identified, the complete S_Y(s) family determines L_Y by its limit at zero, then φ_a by its diagonal remainder. The limit of φ_a at infinity gives d_a; the rational transform d_a-φ_a determines μ_a by unique partial fractions. Conversely L_Y and these measures determine S_Y and G_Y for every s>0.

This establishes an exact invariant of the mathematical response family, not reconstruction of the hidden tree. No assertion is made about existence or nonexistence of distinct forests with equal whole measures. That separate enumeration question is not needed here.

## 4. Forward update and refinement consistency

Fix original X as in P5. Initially W=X gives m_a=1,k_a=0 at every vertex.

Let b be a nonroot leaf of the CURRENT W and a its parent. For V=W\{b},

    m'_a=m_a+m_b,
    k'_a=k_a+k_b+m_b²,                                       (8)

and other surviving coordinates are unchanged.

Proof: P1 joins the two ancestral fibers. The new discarded edge set at a partitions into its former forest, b's former forest, and the newly discarded edge a→b. That edge has m_b original descendants because b is a current leaf; it need not have been an original leaf. Old edge descendant counts are unchanged. This proves (8) directly from the definitions.

A separate operator derivation checks the same coefficients. Eliminating X\W gives S_W=L_W+s Id+diag(φ^W). Its current leaf b has diagonal 1+s+φ_b and sole retained coupling -1 to a. Removing its edge reduces L_W's a-diagonal by one, so

    φ^V_a=φ^W_a+(s+φ^W_b)/(1+s+φ^W_b).                       (9)

Write q=s+φ_b=m_b s-k_b s²+O(s³). Then q/(1+q)=m_b s-(k_b+m_b²)s²+O(s³), reproducing (8).

For a direct W→Y contraction, let E_new contain edges (p,c) of W with c∉Y. Prefix closure puts all of Cone_W(c), including c, outside Y. Set M_c=Σ_{v∈Cone_W(c)}m_v. Then

    m'_a=Σ_{r_WY(v)=a}m_v,
    k'_a=Σ_{r_WY(v)=a}k_v
         +Σ_{(p,c)∈E_new, r_WY(c)=a}M_c².                    (10)

The first k-sum reassigns already discarded edges; the second adds each newly discarded original edge exactly once. The original subtree below c partitions into the current fibers in Cone_W(c), giving its size M_c. Every contraction has a legal leaf factorization (delete deepest missing vertices first); (8) preserves the defining statistics at every step, so every such factorization gives (10). No actual event is assumed to proceed in atomic leaf steps.

Bare additive P1 acting on the OLD k array cannot perform (8). It preserves Σk and sends zero to zero; (8) increases Σk by m_b². Already on X=o→b retained at {o}, the defined final k is 1 while P1 applied to (0,0) gives 0. The extra term is necessary to maintain this statistic, not a derived implementation of a physical register. Nor is this a no-go for a separately justified enlarged representation.

## 5. Global response enclosures from two statistics

Use (6)–(7). For h>0 set dν=λ^(-2)dμ/h, a probability measure. Then

    φ(s)=hs E_ν[1/(1+s/λ)].

Since x↦1/(1+sx) is convex for x≥0, Jensen's inequality gives

    ℓ(s)=hs/(1+sk/h) ≤ φ(s) ≤ hs,       for every s>0.         (11)

A size-only remainder bound requires no unlisted branch-shape condition. Ground the anchor and let depth(i) count edges to hidden vertex i. Express v_i as the sum of edge differences along its path. Cauchy–Schwarz gives

    Σ_i v_i² ≤ (Σ_i depth(i)) v^T C_a v
             ≤ D_h v^T C_a v,    D_h=h(h+1)/2.

An ancestor-first ordering has depth(i)≤i, including when there are several components. Consequently λ_min(C_a)≥1/D_h. The exact scalar identity in (6), not an asymptotic truncation, now yields

    φ(s)=hs-ks²+R(s),
    R(s)=s³∫ λ^(-3)/(λ+s) dμ,
    0≤R(s)≤D_h k s³                 for every s>0.            (12)

For each nonempty anchor put u_a(s)=min(h_a s,h_a s-k_a s²+D_{h_a}k_a s³); set ℓ_a=u_a=0 for h_a=0. Define

    A_lo=L_Y+s Id+diag(ℓ_a),   A_hi=L_Y+s Id+diag(u_a).

Equations (11)–(12) imply 0<A_lo≤S_Y≤A_hi. Inversion reverses positive-definite order, so every formal source satisfies

    j^T A_hi^(-1)j ≤ j^T G_Y(s)j ≤ j^T A_lo^(-1)j.           (13)

These are retained-space bounds calculable from Y,m,k, not error bars for an unprovided detector.

For two forests at one anchor with equal h>0 and k_1<k_2, (12) gives

    φ_1(s)-φ_2(s) ≥ s²[(k_2-k_1)-D_h k_2 s] > 0
    whenever 0<s<(k_2-k_1)/(D_h k_2).                        (14)

If all other anchor terms coincide, this separates their boundary operators. Strict separation of a chosen scalar requires coupling to the differing anchor; it is not asserted for every j.

## 6. Equal counts, different shape: four-vertex carriers

Use P6. Retain Y={o,a}, edge o→a. The star adds two children u,v of a; the chain adds a→u→v. Both give m=(1,3). The discarded edge counts are respectively (1,1) and (2,1), hence k=(0,2) versus (0,5).

Forward application of (8) gives a:(1,0)→(2,1)→(3,2) for the star. For the chain first u becomes (2,1); absorbing it makes a=(3,5).

Directly from (1) or (9),

    φ_star(s)=2s/(1+s),
    φ_chain(s)=s(2+s)/(1+3s+s²),
    φ_star-φ_chain=s²(3+s)/[(1+s)(1+3s+s²)]>0.                 (15)

For j=(1,-1), a matrix S=[[p,-1],[-1,q]] gives the scalar (p+q-2)/(pq-1). Its derivative in q is -(p-1)²/(pq-1)². Here p=1+s>1, so the star scalar is strictly smaller for every s>0. At s=1,

    S_star=[[2,-1],[-1,3]],       j^T G_star j=3/5,
    S_chain=[[2,-1],[-1,13/5]],   j^T G_chain j=13/21.

The difference (chain minus star) is 2/105. From the summaries alone (14) guarantees the weaker interval 0<s<1/5.

In the STATIC zero-sum Poisson interface, FCV P6 gives j^T I^T G_X^static I j=j^T L_Y^+j=1 for both. This static Green operator uses G_X^static=(L_X+11^T/|X|)^(-1)-11^T/|X|. Its rank-one gauge is not s Id_X.

## 7. Same Y,m,k,d, different exact response: nine-vertex carriers

Retain the same Y and attach TWO discarded components at a.

| Forest | First component | Second component | Squared descendant counts |
| --- | --- | --- | --- |
| A | Three-vertex chain | Four-vertex star, root with three leaf children | (3²+2²+1²)+(4²+1²+1²+1²)=33 |
| B | Three-vertex star, root with two leaf children | Four-vertex tree, root with one leaf child and one two-vertex chain child | (3²+1²+1²)+(4²+2²+1²+1²)=33 |

Every component root is a child of a. Both carriers have nine vertices, h_a=7,m_a=8,k_a=33,d_a=2 and m_o=1,k_o=d_o=0.

At s=1 a component contributes q/(1+q), with q=1 plus its child-component contributions, by (9). Starting with a leaf contribution 1/2 gives:

    chain of 2: 3/5;   chain of 3: 8/13;
    star of 4: 5/7;    star of 3: 2/3;
    mixed component: (1+1/2+3/5)/(2+1/2+3/5)=21/31.

Thus

    φ_A=8/13+5/7=121/91,
    φ_B=2/3+21/31=125/93,
    φ_B-φ_A=122/8463>0.

For S=[[2,-1],[-1,2+φ]] and j=(1,-1), the scalar is (2+φ)/(3+2φ). Therefore

    j^T G_A j=303/515,  j^T G_B j=311/529,
    j^T(G_A-G_B)j=122/272435>0.                               (16)

This disproves exact reconstruction from Y,m,k,d while leaving the enclosure theorem intact. The pair does NOT have equal whole spectral measures: (16) already proves otherwise. Neither comparison is a demonstrated acquisition by an initially uninformed physical receiver.

## 8. Operational disposition and stopping boundary

Eliminating hidden vertices from a fine diagnostic is not physical persistence after pruning. If the post-pruning model simply evaluates L_Y+s Id_Y, it has dropped diag(φ). A retained implementation of (8) or an actual shifted source/read operation requires separate provenance.

Dot's bounded source audit found the following implemented chain at the research SHA in P1:

- foundational-closure-verification/exact_algebra.py lines 5–10 imports the pinned inherited diagnostic.
- demos/v15.56-response-selector-obstruction/pruning_consistency_audit.py, green(L), lines 117–120 computes the STATIC rank-one-gauge Green operator.
- foundational-closure-verification/produce_certificates.py lines 29–34 and 81–90 produces static L,Z,G certificates.
- foundational-closure-verification/verify_certificates.py lines 64–79, 154–157 and 416–420 reconstructs and checks those static certificates.
- research/physical-bridge/boundary_response_screen/ADDENDUM.md §7 and record_consumer_trace/NATIVE_STATE_RECORD_INTERFACE.md preserve the source/access limitations.

All paths above are relative to ResearchHistory/UQCF-GEM/. No shifted-family producer/consumer was identified in this exact chain. This is a bounded audit, not a claim of repository-wide impossibility. The operational selection of the shifted interface, physical preparation, retained storage and receiver access remain SUPPLIED/unestablished. Generic ability to invert a new matrix does not establish native observation.

The bounded analytical package stops here: one coefficient, its exact update, useful bounds and an explicit insufficiency control. No added moment hierarchy, equal-measure enumeration or repeated unchanged source audit is needed. A new physical investigation must name a new source-backed operation or evidence; this draft does not supply one.

## 9. Evidence, attribution and review obligations

Immutable source packet:

- [FCV PROOFS P1/P2/P4/P6](https://github.com/proteinfoldingengine/WetLabEngine/blob/3ceb814258f43774b4af1352379ffcd0bd079599/ResearchHistory/UQCF-GEM/foundational-closure-verification/PROOFS.md).
- [Thread through T-076, including T-075-dot](https://github.com/proteinfoldingengine/WetLabEngine/blob/a69a385ec32a6e0613c8e2941a7008dcefa4cee0/ResearchHistory/UQCF-GEM/research/physical-bridge/AGENT_THREAD/THREAD.md): Grok re-derived T-075 §§2–7, corrected prefix closure and discarded-child wording, and supplied Proposition M.
- [T-077](https://github.com/proteinfoldingengine/WetLabEngine/blob/90a4d8dbafe346968be009165cbc005d044b76db/ResearchHistory/UQCF-GEM/research/physical-bridge/AGENT_THREAD/THREAD.md): this session adopted both corrections, checked Proposition M, and derived local/batch updates.
- [T-078](https://github.com/proteinfoldingengine/WetLabEngine/blob/e2a3c24152dabab87043893f6730a3ce688d5bfc/ResearchHistory/UQCF-GEM/research/physical-bridge/AGENT_THREAD/THREAD.md): this session derived bounds and the same-summary pair.
- [Dot's T-077/078 response](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6369883881): inspected the nonadditive-statistic inference and independently re-derived the component counts, four component fractions and final two-by-two response. This is a scoped bot check, not Gemini acceptance.

For this consolidation the author inspected those complete entries, re-derived the displayed edge partitions, Schur identities, spectral moments, Jensen bound, path-energy estimate, remainder and rational examples. No new mathematical conclusion is being added by consolidation.

At preparation, Grok's requested general update/refinement and bounds checks remain pending. The full consolidated argument has no independent Gemini verdict and no workflow run or raw-response hash. No scientific implementation, exhaustive verification, publication closure or post-merge audit is claimed. The PR must remain draft.

The next analytical reviewer should reconstruct (1)–(16), challenge the prefix-closure and current-leaf conditions, seek counterexamples to (10)–(14), verify the two rational controls, and identify any physical premise being smuggled into the conclusions. Independent review must use the standing Gemini Actions workflow on an exact frozen commit with the source packet, preserving raw request/response, model, run ID, hashes, logs and publication evidence. A review of the author's summary alone is insufficient.
