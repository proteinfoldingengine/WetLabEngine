# Current-state grade realization of receiver deletion

Author: ChatGPT research session with Aaron, reconstructing Grok's T-126 Lemma G.
Date: 2026-10-25 (America/Phoenix).
Status: analytical support for the existing T-122 access attempt; not independently reviewed. Native bridge NOT_DERIVED.

## 1. Positive construction and provenance

For a receiver view Z inside a fixed rooted carrier T, define the counting grade

    m_Z = P_TZ 1_T.

Each coordinate counts the vertices of T whose longest retained prefix is that coordinate. A legal receiver deletion acts on this selected grade exactly by the inherited parent-absorption operation. The grade is computable from the current ambient-referenced view; no path history is needed to define it. This supplies a formal incidence-to-grade representation for the attempt in T-124/T-125. It does not create a grade record owned by the receiver.

Credit: Grok proposed this representation and its proof in T-126, thread commit 8ca86003e85fd38816ab03c1677e2e06ddeaf91d. The present manuscript independently reconstructs its mathematical core and bounds the interpretation. The composition law itself is already FCV P1; no new general pushforward theorem or archive-wide novelty is claimed. T-125 correctly rejected unit mass per CURRENT incidence as the proposed conserved grade; it did not disprove this different representation. The new choice resolves that formal representation problem, not the missing physical record producer.

## 2. Premise ledger

1. Fixed finite rooted carrier T, fixed root palette, nonempty nested supports S_t, and legal one-incidence edits at nonroot vertices — INHERITED grammar [v16.53 NATIVE_ADMISSIBILITY.md, blob ebc315f7f2f6423fe9f6861cc3b8a0cfcf8420f2 at research 3ceb814258f43774b4af1352379ffcd0bd079599]. The grammar introduces no native weights or physical interpretation. All grades here are a separate mathematical representation.
2. Longest-prefix retraction r_XY and additive fiber pushforward P_XY, including P_YZ P_XY=P_XZ — INHERITED [FCV PROOFS.md P0/P1, blob a21acad73c80cb748f2e42c244f6db53146c2bf2; concrete Pruning.ancestor/aggregate/then, lineage.py blob e95e3e978779164dd91f09b80e3389247e6320c2; same research SHA]. The software takes carriers and grade values supplied by its caller.
3. Choose 1_T as the grade on the fixed carrier and define m_Z=P_TZ 1_T — SUPPLIED representation, following T-124/T-126. Counting is mathematically defined without a fitted coefficient; physical preparation, ownership, conservation as a physical quantity, and invocation are not derived by choosing it.
4. The T-122 seven-vertex preparation, common source withdrawal and first-response correspondence — ACCEPTED-CONDITIONAL mathematics, with its SUPPLIED carrier/preparation/phase and physical access premises unchanged [RESULT at 43596de4fe9fd1083500987997ee04e15793f60c; ACCEPTANCE at 546511327ee6a224dcc583305e7864a456863c4f]. Actual measurement occurrence is ACCEPTED INPUT; its typing remains unproved.
5. For the optional response illustration only, the grounded constant-coefficient tree field with coefficient alpha — SUPPLIED response choice. Its mathematical formula is inherited conditionally [receiver_identification/CONSTRUCTION.md section 23, blob 69f01eb4ea2c99689f443add988beb58fccfa4a8 at the research SHA]. No physical field or access to its values is inferred.

## 3. Current-state representation and exact deletion action

Fix a label r in the root palette. Its view Z={t in T:r in S_t} is nonempty, contains the root, and is prefix closed by support nesting. The joint union stays T because every vertex remains nonempty under legal edits.

For z in Z,

    m_Z(z) = |{t in T:r_TZ(t)=z}|.

The fibers partition T. Hence m_Z(z) is a positive integer and sum_Z m_Z=|T|. Every retained z belongs to its own fiber. The grade depends on (T,Z) only, not on how Z was reached or on the other labels' current supports. The ambient carrier and its relation to Z remain inputs.

A legal deletion -r(l) requires l to be a nonroot leaf of Z; otherwise a child carrying r would violate nesting. It also requires another label at l to keep the joint vertex nonempty. Put Y=Z minus {l} and p=parent(l), which lies in Z. FCV P1 gives

    m_Y = P_TY 1_T = P_ZY P_TZ 1_T = P_ZY m_Z.

Equivalently, the fiber at l merges into the fiber at p, and every other retained fiber is unchanged. Thus m_Y(p)=m_Z(p)+m_Z(l), and m_Y(z)=m_Z(z) for z different from p. This holds even when l is not a leaf of the AMBIENT T: its absent descendants already contribute to m_Z(l). No assertion that every abstract leaf deletion is legal under joint coverage is required; the statement covers every legal receiver deletion.

The same receiver index r is used before and after. Its formal grade is a vector indexed by vertices in its view. This does not identify a parent vertex with r or prove that r owns those coordinates. Other-label edits do not change m_Z if they leave Z and T unchanged.

## 4. The seven-vertex consequence

T has edges o-u,o-v,o-w,u-x,u-y,u-z, with root o. T-122's initially common receiver view is T, so m_T=1_T in both preparations. Its admitted first responses are Z0=T minus {v} and Z1=T minus one of {x,y,z}. For the representative deletion x,

    m_Z0 = 1_Z0 + e_o,
    m_Z1 = 1_Z1 + e_u.

Both total seven. Both unmarked scalar multisets are {2,1,1,1,1,1}; those scalar multisets alone do not separate the preparations. The attachment of the doubled mass differs in the two trees. This is the same r-indexed vector construction in both cases, not a replacement of r by o or u.

For every retained z, its cone in Z is Z intersect cone_T(z). A vertex t in T retracts into that cone exactly when t is a descendant of z: if t descends from retained z, its longest retained prefix also descends from z; conversely any such prefix is an ancestor of t. Therefore

    sum_{w in cone_Z(z)} m_Z(w) = |cone_T(z)|.

Define, solely for premise 5's response illustration,

    phi_Z(z) = alpha sum_{w on the root-to-z path, w != o}
                         sum_{q in cone_Z(w)} m_Z(q).

Prefix closure preserves that path, so phi_Z is the restriction of the fixed ambient phi_T. The formula is the grounded response to the Genesis-balanced grade m_Z-|T| e_o, not to an uncentered raw grade via the pseudoinverse.

On T, the values are o=0, u=4alpha, v=w=alpha and x=y=z=5alpha. Consequently the two first-response vertex-value multisets are

    Z0: {0,alpha,4alpha,5alpha,5alpha,5alpha},
    Z1: {0,alpha,alpha,4alpha,5alpha,5alpha}.

They differ when alpha is nonzero. The retained edge-value multisets both equal {4alpha,alpha,alpha,alpha,alpha}. These conclusions reproduce T-124's explicitly conditional field calculation; they do not establish that a receiver reads the field, or that each individual retained vertex value changes. Retained values are unchanged; the set of retained vertices differs.

## 5. Exact limits and controls

**Current incidence counting is a different representation.** Resetting to 1_Z after each edit gives total six after the first deletion, whereas m_Z has total seven. The new representation therefore does not make T-125's original equality true. It instead supplies a different current-state function using the fixed ambient carrier.

**History independence is mathematical, not a memory mechanism.** A path history is unnecessary to evaluate m_Z given (T,Z). This does not imply that r can evaluate it, remembers T, has an ambient reference, or receives a newly created register. T-122's reader omitted an ambient embedding; this representation uses it to evaluate m_Z and must not silently inherit that smaller interface. Once a full weighted carrier (Z,m_Z) is given, the displayed field can be computed on it, but giving that carrier to r is precisely unearned access.

**Additions are outside the deletion-action theorem.** A legal +r(l) splits a fiber. The definition still gives a current-state grade, but the split uses the ambient structure; the operation is not the deletion pushforward P_ZY. No source-freeze is needed for the algebra, and no soundness of an old-bit decoder after arbitrary edits is asserted here.

**Representation does not derive information acquisition.** With T fixed, the structured object (Z,m_Z) contains Z and is determined by Z. It therefore has exactly the information in the ambient-referenced view in this mathematical sense. This does not hold for the scalar multiset alone, and is not a claim that a physical receiver already knows Z. The ambient re-expression neither improves the established shape separation nor supplies a consumer.

**Physical obligations remain.** The grade assignment, event-to-phase identification, physical availability of the weighted state or field, and receiver ownership remain SUPPLIED. Naming the grade a function of a receiver view does not make it a receiver-owned record. The actual incidence edit is a legal mathematical transition under premise 1, not a derived actuation of the accepted physical event. Broad C3/C4 and native bridge remain OPEN.

## 6. Verification and review scope

All arguments above were derived analytically before this freeze. No scientific code, enumeration, simulation or archived scientific module was executed in preparing this manuscript. Grok's T-126 reports exploratory scratch counts and hashes; those scripts and outputs were not retrieved, reproduced or used as evidence here. This manuscript does not certify those counts.

The independent review must reconstruct the fiber merge, the ambient cone identity, the first-response values and every claim boundary, especially representation versus native update/access and a vector indexed by a receiver's view versus a record owned by that receiver. The review receives the exact T-126 entry as provenance, including its original scratch disclosures, but is asked to assess this analytical manuscript rather than accept reported checks. The source packet binds each complete source identity and exact included byte interval. Independent analytical acceptance would validate only this conditional representation step, not a physical mechanism.
