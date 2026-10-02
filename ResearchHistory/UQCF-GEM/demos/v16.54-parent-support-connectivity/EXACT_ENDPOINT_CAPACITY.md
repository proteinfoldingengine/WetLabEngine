# Exact-endpoint capacity structure and saturated reconfiguration

Status: candidate analytical extension for independent review. No implementation or numerical execution. Parent analytical head: c678651cda8262fe39b69d9f6b7e224255dcc0c8. The previous proof and its accepted review remain unchanged.

## 1. Scope and definitions

Use the native width-floor carrier from GENERAL_PARENT_CONNECTIVITY.md: r nonempty roots A_i subset P, |P|=k, |A_i|>=a_i>=1, with a single root incidence toggled per move. The transversal number tau(A) is the smallest label set hitting every root. Fix feasible exact-q endpoints, q>=3, on the same ordered P and floor vector a. Put B_i=P\A_i, b_i=k-a_i, d=r-q+1, and

    delta = sum_i b_i - (q-1)k = dk - sum_i a_i.

The target lower guard is tau>=q-1, equivalently coverage of every (q-2)-subset by the B_i. Exact endpoints cover every (q-1)-subset and miss at least one q-subset. All results below concern endpoints actually arising this way. We do not assume arbitrary covers share their structure.

This extends the approved analytical scope: derive local endpoint constraints, resolve the entire delta=0 boundary across arities and targets, and identify the remaining positive-delta problem. These arguments were developed after the user's continuation instruction; they are not a prospective numerical protocol. No scientific program was run.

## 2. A hierarchy of local redundancy and capacity inequalities

For S subset P with |S|=s<=q-1 define

    N_A(S) = { i : A_i intersect S is empty } = { i : S subset B_i }.

**Lemma G (local redundancy).** At every exact-q endpoint,

    |N_A(S)| >= q-s.

Proof. S already hits all roots outside N_A(S). Choosing one label from each remaining nonempty root gives a hitting set of size at most s+|N_A(S)|. Exactness supplies the bound. This includes S empty and uses no capacity approximation.

More strongly, the roots indexed by N_A(S), considered alone, have transversal at least q-s: a smaller hitting set together with S would hit the original tuple with fewer than q labels. Equality is not claimed for an arbitrary S.

**Corollary G1 (local capacity).** For s<=q-2,

    sum_{i in N_A(S)} (b_i-s) >= (q-s-1)(k-s).

Proof. For each x outside S, Lemma G applied to S union {x} gives at least q-s-1 blocks containing S and x. Double-count these block/label incidences:

    sum_{i in N_A(S)} (|B_i|-s)
      = sum_{x outside S} |N_A(S union {x})|
      >= (q-s-1)(k-s).

Replace |B_i| by its capacity b_i. At s=0 this recovers the stated total-capacity bound; at positive s it constrains precisely the blocks that cover S. The total bound alone does not express these localized constraints.

**Corollary G2 (one-block replacement).** Any one complementary block of an exact-q endpoint can be changed to any block within its capacity while preserving coverage of every (q-2)-subset throughout. Delete old block incidences to the empty block, then add new ones. Every relevant subset initially has at least two covering blocks by Lemma G; the untouched blocks alone therefore retain its coverage. The root version expands one root to P and contracts it to its new permitted support.

This is a lower-guard path. If both endpoint tuples are exact-q, the root path also satisfies tau<=q: each expansion state contains the old tuple and each contraction state contains the new tuple. Thus it is already a {q-1,q} path. If the replacement endpoint is not exact-q, only the lower guard is asserted. Crucially, one may not repeat G2 on an arbitrary resulting lower-cover state as though exact endpoint redundancy survived.

## 3. Saturated endpoint classification

At an exact-q tuple each label occurs in at most d roots. Indeed a label in m roots, plus one label from each remaining root, gives a hitting set of size at most 1+r-m, forcing m<=d.

**Theorem H (saturated normal form).** Suppose delta=0 and q>=3. Every exact-q endpoint consists of precisely r-q full-palette roots and q further roots that partition P into nonempty blocks of sizes a_i. The full-palette indices are determined by the floor vector, namely the indices with a_i=k; consequently they are identical at both endpoints.

Proof. The bounds

    dk = sum_i a_i <= sum_i |A_i| <= dk

force every row to have size a_i and every label to occur in exactly d roots. For each label x let E_x={i:x in A_i}, a d-element set of child indices. Two labels must satisfy

    |E_x union E_y| <= d+1.

Otherwise those two labels, plus one label from each root outside their union, would hit all roots using at most 2+r-(d+2)=q-1 labels. Thus distinct E_x,E_y intersect in d-1 indices.

We give the elementary classification of this set family rather than invoking an external theorem. If d=1, take the common core C empty; the claimed form follows immediately from degree one and nonempty roots. For d>=2 there must be at least two distinct sets: a single repeated d-set would leave r-d=q-1>0 roots empty. Choose E=C union {u} and F=C union {v}, where |C|=d-1. Any other d-set G either contains C, or omits some c in C. In the latter case, intersection of size at least d-1 with both E and F forces

    G = (C\{c}) union {u,v}.

If such a G exists, any set C union {w} with w outside C union {u,v} intersects G in only d-2 indices and is forbidden. Every set not containing C is already contained in C union {u,v}. Therefore either all E_x contain the same (d-1)-core C, or all E_x lie in a fixed (d+1)-set.

The second possibility cannot cover all r child indices because r=d+q-1>=d+2. Nonempty roots require that their union cover all r indices. Hence every E_x contains C. Those d-1=r-q roots equal P. Each label occurs in exactly one of the remaining q roots, and all these roots are nonempty. They partition P. Their positive sizes sum to k and, since q>=3, each is strictly less than k. Row sizes equal floors, so the full-palette roots are exactly those with a_i=k. This proves the classification and uniqueness of their indices.

Conversely, any tuple of this form has transversal exactly q: each of the q nonempty disjoint parts requires its own hitting label, and the full-palette roots add no constraint. Thus the classification is exact, not only necessary.

The restriction q>=3 matters. For q=2, the alternative family on d+1=r indices is possible; for example three roots {x,y}, {y,z}, {x,z} with floors 2 and k=3 are saturated and have transversal 2. Target 2 already has the general expansion/contraction proof in the preceding document.

## 4. Reconfiguration on the entire capacity boundary

**Theorem I (saturated exact-endpoint connectivity).** For any r,k,a and q>=3 admitting exact-q endpoints with delta=0, any two such endpoints are connected by single-incidence moves respecting all floors and tau in {q-1,q}. In complements, the entire exact-q endpoint class is connected through capacity-bounded covers of all (q-2)-subsets.

Proof. Theorem H gives the same fixed full-palette roots at both endpoints. It remains to transform one partition of P among q indexed roots into another with the same part sizes a_i. Select a misplaced label x whose destination is part j and whose current part is i. Since j has the prescribed size and lacks x, it contains a label y not destined for j. Swap x and y using the four moves

    add y to A_i;
    add x to A_j;
    delete x from A_i;
    delete y from A_j.

All floors hold: both affected parts only enlarge before contracting to their original sizes. At each intermediate state the other q-2 parts remain nonempty and disjoint from both affected parts and one another. The two affected parts are nonempty and together require either one or two labels, so total transversal is q-1 or q. The full-palette roots are redundant. Every move changes one incidence. At completion x is correctly placed, y may or may not be, and no previously correct label was moved because x and y were both misplaced. The number of correctly placed labels strictly increases. Finitely many swaps reach the target.

This resolves the saturated case for all pairs and all higher-subset levels simultaneously, with no arity progression, numerical enumeration, extra label, or enlarged native move. The earlier five-child saturated-star argument is a special case. Section 7 of GENERAL_PARENT_CONNECTIVITY.md supplies conditional native lifting when the children have the accepted interface; no stronger necessity statement about native paths is added.

## 5. Positive slack is localized, but not yet resolved

Compact any exact-q endpoint to its row floors by retaining an anchor from a minimum q-label hitting set in each root and deleting excess incidences. This keeps tau exactly q, as proved in the preceding document. For a compact endpoint, with label degree m_x,

    sum_{x in P} (d-m_x) = delta,
    0 <= m_x <= d.

Thus at most delta labels have degree strictly below d. Unused labels count as defects of size d and are included. If delta>=k this count need not be restrictive. It is an endpoint statement, not a claimed invariant of a reconfiguration path.

The degree-d labels still satisfy the pair-union bound and its core-or-(d+1)-index-set classification. If there are at least two distinct degree-d supports, the proof in Section 3 applies to that subfamily. A single support has a core of size d-1 when d>=1; an empty degree-d family has no asserted core. With positive slack the deficient labels can serve child indices outside the degree-d family's union, so the small-index-set alternative cannot be discarded. Even in the common-core alternative, deficient labels need not occupy that core. Neither alternative is a global normal form for the whole endpoint without further work.

These facts isolate the remaining question: can the deficient labels and the localized subset-cover redundancy be used as a buffer for exchanges while preserving every (q-2)-subset cover? The scalar delta is not by itself a proven sufficient buffer condition. G2 gives a first whole-block replacement, but after it the residual tuple may lack the redundancy needed for a second replacement. No universal positive-slack exchange theorem, disconnected root example, or native obstruction is claimed.

## 6. Validation and claim boundary

This document is a finite analytical argument, not an executed algorithm or a certification result. The proof obligations for independent review are the local counting hierarchy, the one-block caveat, equality forcing all degrees, the set-family classification including d=1 and repeated supports, exclusion of its second alternative, floor-safe saturated exchanges, and the limits of defect localization.

A future implementation campaign needs its own prospective protocol. Its mechanisms should include maximum-layer replacement, overlapping ORIGINAL-role packets, cycle buffering, and saturated configurations across structural types. No such campaign is authorized or initiated by this document. General positive-slack pair/higher-subset connectivity remains open, and there is no physical interpretation claim.
