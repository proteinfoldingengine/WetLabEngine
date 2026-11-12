# A receiver's current shape can carry the source distinction

Author: proteinfolding-gpt. Date: 2026-10-18 America/Phoenix.
Source baseline: c7d0f637c0af29b303721f1e08c2634208e8db31.
Status: analytical construction awaiting independent review. Native bridge NOT_DERIVED.

## 1. Positive construction and admission

This is mathematical support (B) for the existing source-enabled/coverage-protected native interaction candidate (A), not a new interaction mechanism. It removes a specific access burden: the decoder no longer needs the full ambient carrier T, a retained-to-ambient embedding, leaf addresses, or the identity of a missing leaf. The current receiver view's unlabelled rooted-tree isomorphism type suffices for a responding acquisition and a correct-or-UNKNOWN record up to the existing erasure boundary.

It does NOT derive access to that current shape, source preparation, actual event enactment, or the one-source-edit acquisition prefix. It does not turn formal own-view membership into an available physical observable. Its relevance is a weaker interface for the SAME positive construction, rather than a fresh variation of a supplied channel.

## 2. Existing carrier, preparations and acquisition

Use the fixed eight-vertex carrier from source_enabled_record: root o, internal children c_0 and c_1, two leaves L_0 under c_0 and three leaves L_1 under c_1. Palette P={b,r}, with nonempty nested supports and fixed root support. Y_i is the rooted prefix-closed view of label i. A primitive adds or deletes one incidence at one nonroot vertex subject to this inherited grammar.

Preparation s in {0,1} is Y_r=T and Y_b={o,c_s}. Both follow by +b(c_s) from the same valid seed (Y_r=T,Y_b={o}). s refers to the b-marked original two-leaf or three-leaf branch. No numerical weights or metric are introduced.

Use the accepted acquisition prefix: at most one b edit before the first proper r edit. The initial r command set is empty. All initially possible b edits are -b(c_s), +b(c_(1-s)), or +b(l) with l in L_s. Only the last enables r, whose unique next edit is -r(l). Hence a responding acquisition has

    Y_r = T minus {l},   Y_b={o,c_s,l},   l in L_s.           (1)

These are inherited facts, reproduced here to fix quantifiers. Neither a response nor the prefix bound is derived as an actual event law. After (1), allow arbitrary legal b/r edits, including additions, with no post-acquisition source-count bound.

## 3. Record interface using only the current receiver tree

For any current rooted view Y=Y_r, let M(Y) be the multiset of outdegrees IN Y of the immediate children of its root. A root child with no retained children contributes 0; a missing root child contributes no entry. These are distinct cases. M is an invariant of the unlabelled rooted-tree isomorphism type [Y]. It uses neither global leaves of T nor a map from Y to T.

Define the fixed partial decoder

    D([Y])=0       if M(Y) is {3}, {0,3}, or {1,3};
    D([Y])=1       if M(Y) is {2,2};
    D([Y])=UNKNOWN otherwise.                              (2)

This decoder is defined mathematically on all finite rooted trees, but its claimed soundness is ONLY for the declared eight-vertex candidate and histories below. The constants identify that fixed task; they are not a universal, protocol-free interpretation of tree shapes.

The complete initial receiver shape is identical in both preparations and has M(T)={2,3}, so D=UNKNOWN. The complete bare command interface is also identical and empty, as above. We make no claim about additional hidden-state-dependent rates or unspecified physical observables.

At first acquisition, if s=0 then M={1,3}, so D=0. If s=1 then M={2,2}, so D=1. These two rooted trees are nonisomorphic: the multisets of child degrees differ. No current branch name is needed, even though the two branches in the s=1 response have become structurally interchangeable. Under the earlier whole-episode one-b-edit contract, the receiver alternates only between T and this acquired tree, so (2) is correct or UNKNOWN at every prefix of that contract, including restorations.

## 4. Lifetime theorem with arbitrary later edits

After acquisition, define for PROOF purposes

    Q_j=1 iff some original global leaf in L_j is absent from Y_r.

Let tau_s be the first later state at which Q_s=0, or infinity if this never occurs. This is exactly the original branch-restoration boundary in coverage_protected_record. tau_s and Q_j are not inputs queried by decoder (2). At acquisition Q_s=1 and Q_(1-s)=0.

**Theorem.** At every finite post-acquisition prefix strictly before tau_s, D([Y_r]) is either s or UNKNOWN. Both sources are decoded definitively at their first response. No old-bit guarantee is made at or after tau_s.

Proof for s=0. Before tau_0 at least one of the two original leaves of c_0 is missing. If c_0 remains in Y_r it therefore has at most one child in Y_r. If it is absent, prefix closure removes all its children as well. The other original root child c_1 has at most three children. Thus M cannot be {2,2}: that would require both original root children and two leaves under c_0. The decoder cannot output 1. It may output 0 or UNKNOWN.

Proof for s=1. Before tau_1 at least one of the three original leaves of c_1 is missing, so if c_1 remains it has at most two children. c_0 always has at most two. Thus M contains no 3, and none of the three output-0 patterns is possible. The decoder cannot output 0. It may output 1 or UNKNOWN. QED.

These arguments require only the fixed carrier, prefix-closed receiver view and the retained deficit of the original branch. They permit internal r deletions, all receiver additions, all source edits and changing missing-leaf witnesses. They use no leaf address remembered by the reader and no notification of erasure. For an infinite history they apply at every finite prefix before its first restoration; they do not assert a limit-state decoder.

Inherited two-label coverage gives the mechanism's additional protection: while Q_s=1, every missing leaf and its ancestors must be b-covered, so b cannot withdraw from c_s. That is the already accepted coverage theorem, not a new physical enforcement law. The shape proof itself does not need to assume that the currently missing leaf is the originally deleted one.

## 5. What coarsening costs

The prior ambient decoder returns j whenever only Q_j=1, and UNKNOWN for both deficits or neither. Decoder (2) can discard more information. For example, c_0 remains with two leaves and c_1 remains with one leaf: M={1,2}. If the deficit is in original branch 1 alone, the ambient decoder can output 1 but (2) says UNKNOWN.

This extra UNKNOWN is necessary for some shapes if the same reader is to be sound on BOTH source histories throughout their pre-erasure domains. There are legal pre-erasure histories from both sources with the SAME rooted shape M={1,2}:

- From source 0 acquisition at a leaf l_0, add b(c_1), add b(l_1) for one l_1 in L_1, then delete r(l_1). The original c_0 retains one leaf, c_1 retains two. Q_0 stays 1.
- From source 1 acquisition at l_1, add b(l_1') at a distinct other leaf of L_1, then delete r(l_1'). The original c_0 retains two leaves, c_1 retains one. Q_1 stays 1.

All added b leaves have their b-covered parent; all r-deleted leaves have b coverage. The two resulting unlabelled rooted trees are isomorphic by swapping the two root subtrees. Any decoder using only [Y_r] that never returns a wrong old bit over these two domains must return UNKNOWN on that common shape. This does not prove (2) is a maximally informative decoder on every possible shape; no such optimality is claimed.

There are still positive continuations beyond one leaf deficit. From source 0 acquisition, add b to the remaining L_0 leaf, delete r there, then optionally delete r(c_0). The resulting M are {0,3} and {3}, and (2) remains 0. Every edit is legal: nonemptiness is protected by b, and the internal r deletion occurs only after all its r children are gone. These cases justify both extra output-0 patterns.

## 6. Controls and exact boundary

**Original-bit failure after erasure.** Start at source-0 acquisition with deficit l_0. Perform +b(c_1), +b(l_1), -r(l_1), then +r(l_0). Before restoration M={1,2} and (2) is UNKNOWN. At restoration M={2,2} and (2) returns 1 although the original bit was 0. That state is tau_0, outside the theorem. Retention is not indefinite and the shape reader does not know an original bit or reset epoch from its shape alone.

**Acquisition prefix still essential.** From source 0 preparation, +b(c_1), +b(l_1), -r(l_1) yields {2,2} and output 1. Two b edits before the first response violate the accepted prefix contract. Removing the ambient reference does not repair that limitation.

**Cardinality is insufficient.** Both first-response trees have seven vertices; both initial trees have eight. The discrimination uses incidence shape, not total vertex count, source labels or a chosen numeric encoding.

**The retained embedding contains more information.** The {1,2} collision above demonstrates that forgetting the ambient embedding can merge histories the embedded views distinguish. The theorem deliberately retains only a sound partial response. It does not equate the coarse shape with the old two-flag record.

**Carrier scope is essential.** A different initial carrier, an unannounced expansion, or identifying physically different local structures with the same unlabelled tree lies outside the result. Merely observing a tree-shaped pattern does not identify this preparation protocol. Third labels affect the coverage-protection mechanism even though the purely combinatorial shape implication conditional on a deficit uses only Y_r.

**Reference-free wording is limited.** The theorem removes the full runtime carrier and address reference. It still fixes the receiver role, root, preparation family and correspondence between output 0/1 and the original branch arities. It supplies no ownership of the receiver tree, detector, comparison operation or access to its adjacency. Calling this wholly assumption-free access would be false.

## 7. Native obligation and review contract

The concrete access target is now narrower: an inherited receiver-owned record that retains its CURRENT rooted incidence shape (or any already available effect separating the two acquired shapes), together with an inherited operation realizing the same acquisition. A separate copy of the ambient T and an occupancy/address reader are not necessary for this candidate. The receiver's own shape is a mathematical input contract until an existing physical/ontological record definition supplies it.

The old record_compatibility_bridge represents supplied record projections as compatible-alternative views, but does not identify arbitrary native indexed views as those actual records. Its carrier is built from a given algebra chain and it explicitly leaves availability and acquisition open. We do not reverse that representation to manufacture a receiver state. Nor do we treat RAS/RCR, a READS declaration, a density-matrix encoder or an external graph renderer as a newly derived source-to-reader mechanism.

The proof and all controls above were developed analytically before scientific execution. No finite campaign, archived native program or simulation was run. Independent Gemini review should reconstruct both acquisition shapes, all-prefix and lifetime claims, internal-deletion cases, the reachable {1,2} collision, erasure and two-source-edit controls, and the precise reference/availability boundary. All exact frozen documents and relevant original sources must be supplied. Historical acceptance is not certification of this new claim.

No physical event law, fundamental time, geometry, dark matter, probability model, main merge, numbered-stage closure or native milestone is asserted.
