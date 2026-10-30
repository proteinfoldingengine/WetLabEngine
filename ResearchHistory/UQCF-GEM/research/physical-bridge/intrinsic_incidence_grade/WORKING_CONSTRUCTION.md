# Intrinsic incidence grade: an exact P1 representation and its inherited response

Author: GPT research session with Aaron.
Date: 2026-10-30, America/Phoenix.
Source parent: `d83e51a38eb47ce1acdaaa6ad08f01e7f5ff1bb9`.
Status: WORKING ANALYTICAL CONSTRUCTION. Not independently reviewed by Gemini.
Native physical bridge: NOT_DERIVED. No numbered stage or scientific breakthrough claim.

## 1. Positive construction and the concrete question

Can the existing receiver's current incidence view determine a signed diagnostic that follows P1, without the external ambient reference and ambient unit grade used in T-126?

There is a simple signed representation. For the current finite rooted receiver tree Z, put

    e_Z(v) = 1 - c_Z(v),

where c_Z(v) is the number of immediate children of v in Z. This is the difference between the vertex count at v and the count of outgoing edges at v. It uses the existing rooted incidence relation and finite counting. No physical charge, probability, new memory, coupling or observation law is assigned.

The calculation below establishes

    e_Y = P_ZY e_Z,

for every inherited prefix-closed pruning Z -> Y, and therefore for every legal receiver-incidence deletion. It then traces the grade into an already inherited consumer: the rooted tree Laplacian response. After the canonical root compensation, that response is exactly lineage depth. Hence it does not change at any surviving address.

This is a new candidate application in this investigation, not a new general theorem about trees. Its purpose is to test one explicit current-view -> grade -> inherited-response composition. No mathematical priority is claimed. The choice to investigate e_Z is an author proposal; the native rules are not asserted to select it as a physical source.

## 2. Sources, types and premise accounting

1. A native indexed view Z_r consists of the addresses whose supports contain label r. Nesting makes Z_r root-containing and prefix closed. A legal deletion -r(l) removes a nonroot leaf of Z_r, while the complete incidence state must still satisfy nonemptiness and nesting. This is the existing mathematical edit grammar; actual measurement correspondence remains unearned.
2. P1 uses the nearest retained ancestor and sums grades over its fibers. The signed F-valued diagnostic, F=Q or R, is inherited FCV P0-P1. Physical realization of an arbitrary signed grade is expressly not established there.
3. On a finite rooted tree Z, the existing response is the inverse of its unweighted tree Laplacian on zero-sum sources, modulo constants. Root-zero representatives are available mathematical representatives of that quotient, not measured potentials.
4. Actual occurrence of a measurement/pruning is ACCEPTED INPUT. Its identification with the displayed incidence edit, and ownership or observation of any resulting scalar, are still separate.
5. The function e_Z is DEFINED here from the current native incidence tree. This supplies a representation for analysis, not a new state-transition primitive or a claim that a receiver performs the computation.

Exact source anchors, all at the source parent unless a historical freeze is specified:

| Source | Sections / symbols | Git blob |
| --- | --- | --- |
| foundational-closure-verification/PROOFS.md | P0-P1, P4, P6 | a21acad73c80cb748f2e42c244f6db53146c2bf2 |
| foundational-closure-verification/lineage.py | Carrier; Pruning.ancestor, aggregate, then | e95e3e978779164dd91f09b80e3389247e6320c2 |
| demos/v16.53-four-child-boundary/NATIVE_ADMISSIBILITY.md | Carrier and extension; legal primitive | ebc315f7f2f6423fe9f6861cc3b8a0cfcf8420f2 |
| research/physical-bridge/ancestry_retention_review/RESULT.md | §§2-3, cone inversion and preservation | 360bfd144a126a23015a5625fe9f39aa2e4e28b7 |
| research/physical-bridge/positive_retained_holdings/RESULT.md | §2, signed natural families; §§3,5, nonnegative scope | feb28cd2480db73ba41a7a02e3a93d5c93dabc09 |
| research/physical-bridge/AGENT_THREAD/THREAD.md | T-126 through T-130, current-view grade and consumer | 248839ffecb6eae96da1bd319aaf4987984497e5, thread commit 7b2b2eaa42af7f3766b8170378a195ba4da107db |

The native incidence grammar explicitly has no weights or physical interpretation. This note does not amend it to contain weights. The grade is a mathematical function of the existing incidence state.

## 3. Derive the grade and its P1 update

Every descendant cone of a finite rooted tree is itself a nonempty tree. Its number of internal edges is its number of vertices minus one. Every outgoing edge of a vertex in the cone stays inside that cone. Therefore

    sum_{w in Desc_Z(v)} e_Z(w)
      = |Desc_Z(v)| - |Edges(Desc_Z(v))| = 1.             (1)

In particular total e_Z is 1. Equivalently, e_Z is the unique signed grade whose every ancestral cone total is 1: the already inherited cone inversion gives

    e_Z(v) = 1 - sum_{w child of v} 1 = 1-c_Z(v).        (2)

This is an exact integer identity, not a measured amount or a probability normalization.

Let l be a nonroot leaf of Z and p its parent. Then e_Z(l)=1. Deleting l decreases c_Z(p) by one and changes no other surviving child count. Hence

    e_(Z-l)(p) = e_Z(p)+1 = e_Z(p)+e_Z(l),
    e_(Z-l)(v) = e_Z(v)  for surviving v != p.           (3)

Thus a legal receiver-incidence deletion acts on this representation exactly as P1, without invoking a weight update in the incidence program.

Every prefix-closed pruning factors into leaf deletions. Applying (3) and inherited P1 composition proves

    e_Y = P_ZY e_Z.                                    (4)

Alternatively, P1 preserves every retained ancestral cone total, so (1) and cone inversion give (4) directly. No branching bound is needed. A retained receiver leaf need not be a leaf of the ambient joint carrier; only its children inside Z_r enter (3).

The construction is invariant under rooted isomorphism. It uses only Z, unlike T-126's m_Z=P_TZ 1_T, which uses a fixed ambient T and its supplied unit grade. This removes that reference from this alternative representation; it does not show that e is the physically correct grade.

## 4. Follow the result into the inherited consumer

Let o be the root, delta_o its unit coordinate, and

    j_Z = e_Z - delta_o.

Then j_Z has total zero, so it is a correctly typed input to the existing Laplacian inverse. Root compensation is a declared mathematical construction fixed by the distinguished root; it is not physical background production. Since P1 fixes delta_o, (4) implies

    j_Y = P_ZY j_Z.                                    (5)

Let d_Z(v) be address depth, with d_Z(o)=0. It is pruning-order/lineage data, not a clock or physical distance. Use the inherited graph-Laplacian convention

    (L_Z f)(v) = sum_{w adjacent to v} (f(v)-f(w)).

At a nonroot vertex v, the parent contributes +1 to L_Z d_Z and each child contributes -1. At the root, each child contributes -1 and there is no parent. Consequently

    (L_Z d_Z)(v) = 1-c_Z(v) = j_Z(v),  v != o,
    (L_Z d_Z)(o) = -c_Z(o) = j_Z(o).                    (6)

Thus

    L_Z d_Z = j_Z,                                     (7)

and FCV P4 uniqueness modulo constants makes the inherited root-zero response exactly d_Z.

For a prefix-closed Y subset Z, a retained vertex keeps the same parent chain and depth. Therefore

    d_Y = d_Z restricted to Y.                         (8)

Equations (5)-(8) are consistent with the inherited FCV P6 boundary comparison. They exhibit the consumer's output, rather than simply asserting that a source grade can be consumed.

**Consequences.** Although the retained parent's e-grade changes under a leaf deletion, the root-zero response at that parent does not change. Neither does any potential difference between surviving addresses, or the gradient on a surviving edge. A zero-mean representative may change by a common additive constant because its averaging carrier changed; that is not a change in the quotient response.

This does not say the whole output is identical: the domain changes, the removed leaf is absent, and the e/j grade at its parent changes. A separately justified observation of those features could carry information. What fails here is the particular attempt to obtain a changing retained-address response from this inherited Laplacian consumer.

## 5. Exact four-address illustration

Use Z=(o,p,u,v), with o->p and p->u,v. Prune u and retain Y=(o,p,v).

| Quantity | Before, order (o,p,u,v) | After, order (o,p,v) |
| --- | --- | --- |
| child counts | (1,2,0,0) | (1,1,0) |
| e | (0,-1,1,1) | (0,0,1) |
| j=e-delta_o | (-1,-1,1,1) | (-1,0,1) |
| root-zero response d | (0,1,2,2) | (0,1,2) |

P1 adds the removed leaf's +1 to the parent's -1. The source at p changes from -1 to 0, while the response at p stays 1. This is a displayed exact calculation, not a numerical campaign.

These vectors are NOT the balanced nonnegative preparations (1,1,2,1)/5 and (1,1,1,2)/5. Substituting e for that physical-preparation candidate would change the construction and is not authorized by the algebra alone.

## 6. Boundaries and comparison with existing work

- **Signed, not probabilistic.** If a vertex has two children, e(v)=-1. Total one therefore does not make e a probability distribution, nonnegative holding, count of positive tokens, or density-matrix encoding.
- **Not a source-bit preparation.** On one fixed view Z, e_Z is determined. Two preparations with the same Z have the same e_Z. A source-sensitive choice of actual receiver successor has not been derived.
- **No hidden reference addition.** There is no ambient T input in e_Z. There is still a proposal to use this particular incidence function as a diagnostic. Independence from T does not imply that the model selects it physically.
- **No accessed record.** Defining e_Z, j_Z or d_Z does not create a register, perform a read, or identify the receiver's complete operational state. The availability boundary remains.
- **Nontrivial source change is compatible with unchanged retained response.** Both L and j change with the carrier. Holding the old L fixed after pruning would be a different, incorrectly typed consumer.
- **No uniqueness claim for grading.** Root-supported delta_o is another intrinsic P1-natural grade family. The native rules have not selected between it, e_Z or other admissible representations.
- **No universal absence claim.** The calculation does not exclude other sources, consumers, retained-grade observations, changes of carrier information, or a justified physical interface.
- **Prior mathematics credited.** Cone inversion, P1 composition, signed natural families and the Laplacian boundary identity are already inherited. In positive_retained_holdings §2, choosing nu(k,0)=1 and nu(k,m)=0 for m>0 gives exactly H_Z(x)=(sum_v x_v)e_Z. Thus e is explicitly a specialization of that existing signed classification; it fails its positivity condition on branching trees. The contribution here is selecting this current-view diagnostic for a concrete source-to-consumer trace, not a new classification or naturality theorem.

## 7. Outcome and verification status

The positive representation is exact: current native incidence determines a signed grade, and a legal receiver leaf deletion induces precisely P1 on it. It avoids the ambient reference of T-126 in this different diagnostic.

The attempted bridge through the already inherited Laplacian response does not yield a changing retained-address response. Its output is lineage depth. Physical ownership/access and actual event correspondence remain unearned.

All arguments and the displayed example were derived analytically before publication. No scientific code, finite enumeration, simulation, detector, coupling or new outcome law was executed or introduced. This is a bounded working construction, not a frozen or independently accepted proof. A collaborator's check, if later recorded, is not Gemini independent review. No expensive review or numerical campaign is requested solely to certify this unsuccessful physical bridge.

Two same-lineage collaborators analytically reconstructed §§3-5 and inspected the scope at commit `969bae8df7de37624d255fca1248d00530052018`, blob `2004ad4b2e72a4327537a24c276a1063184a16bc`. They reported no mathematical error and identified the explicit signed-family specialization now credited above. These checks involved no scientific execution and are not independent Gemini acceptance.

The existing positive P1 acquisition results remain unchanged. This note does not reopen the parked channel/rate/symmetry investigations or change research schedules.
