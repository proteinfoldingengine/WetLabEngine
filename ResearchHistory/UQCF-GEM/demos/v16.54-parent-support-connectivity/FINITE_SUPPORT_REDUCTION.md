# A finite-support reduction for the remaining connectivity problem

Status: candidate analytical proof for independent review. Parent accepted head: 59f708231dd0e57548fc5931a8b0c98156ed8aa0. Uses the companion GUARD_BUFFER_CONNECTIVITY.md only in Section 4. No enumeration, implementation or numerical execution.

## 1. Statement and native constraints

Fix r positive floors a_1,...,a_r and let S=sum_i a_i. Work in the existing root carrier on a fixed palette P: one incidence toggled per move, all floors respected, no additional roots or labels. Fix exact-q endpoints, q>=3, and t=q-1. The previously proved upper-excursion removal theorem equates their unit-band connectivity with their connectivity through tau>=t.

**Theorem AD (finite-support reduction).** Compact both endpoints exactly to their floors. Let U be the union of the labels used by these two compact tuples, so |U|<=2S. Choose S+1 labels of P outside U if that many exist, and let P_0 consist of U and these labels; otherwise let P_0=P. The compact endpoints are connected in the full carrier if and only if they are connected using only labels of P_0. In particular |P_0|<=3S+1.

Here connectivity means a primitive path with tau in {q-1,q}. Keeping all unused labels in the nominal palette is harmless; P_0 specifies labels actually used by the path. The reduction never introduces a label absent from P. It is a statement about root connectivity and retains the earlier limits on conditional lifting to nested native objects.

## 2. Compact projection of any lower-guard path

Call a tuple compact if every root has size exactly its floor. Suppose a lower-guard path connects two compact tuples. For each vertex V of this finite path, choose any compact tuple C(V) componentwise contained in V; at the endpoint vertices choose the given compact endpoints. Shrinking supports cannot lower the hitting number, so each selected tuple still has tau>=t.

Two consecutive original vertices are comparable by inclusion because they differ by one incidence. Let W be the larger. Both selected compact tuples are componentwise contained in W. Transform one selected tuple into the other one row at a time. Within a row, pair labels in its current support but not its destination with labels in its destination but not its current support. For each pair add the new label, then delete the old label.

Every intermediate row stays inside W's corresponding support. Every root has its floor size except, during one addition-deletion pair, one root has its floor plus one. Consequently the whole tuple remains componentwise contained in W and has tau>=tau(W)>=t. Each primitive move is legal. Concatenating these replacements yields a finite lower-guard path which is a sequence of elementary compact swaps, each realized by add-then-delete.

At a compact vertex there are exactly S incidences and at most S active labels. During one swap bridge there are at most S+1 incidences and hence at most S+1 active labels. This is a proof of existence from a given finite path; it makes no complexity claim and performs no search.

## 3. Reusing a fixed finite reserve of existing labels

If fewer than S+1 labels lie outside U, P_0=P and there is nothing to prove. Otherwise fix a reserve R of S+1 such labels. In the compact-swap path above, labels belonging to U keep their original identities. Assign every other currently active original label injectively to a reserve label in R.

Initially no label outside U is active. Maintain the injection through each add-then-delete swap:

- If the added label belongs to U, use its fixed identity. The reserve is disjoint from U, so no conflict can occur.
- If it is an already active label outside U, use its current assigned reserve label.
- If it is a newly active label outside U, at most S labels outside U are active before the addition. Choose an unused label of the S+1-element reserve and assign it to the new one.
- Perform the deletion with the same assignment. Release an assignment only when its original label no longer occurs in any root.

Each addition is to a label absent from that row, and each deletion removes a present label. Distinct active original labels always have distinct images, with U fixed pointwise. Thus the entire tuple at each primitive stage is isomorphic on its active labels to the corresponding original tuple. Floors and hitting numbers are preserved exactly, including the bridge stage. The assignment can change for a label that disappears and later reappears, because it has no incidence while absent.

At the destination no label outside U is active, so the mapped endpoint is the prescribed compact endpoint, not just an isomorphic copy. We have produced a lower-guard path using only P_0. Apply the maximum-layer removal theorem inside that palette to obtain a path with tau in {q-1,q}. Its operations use only labels of P_0. Conversely any such path in P_0 is also a path in the full palette, since inactive labels cannot lower the hitting number. This proves AD.

For noncompact original endpoints, exact compaction retains, in each root, at least one label from a chosen minimum hitting set and preserves tau=q throughout. Each endpoint is connected to any chosen such compaction. Hence the original connectivity question is equivalent to the compact-endpoint question just reduced. The bound concerns the reduced pair and the middle connection; it does not claim that the original, possibly large supports already use at most 3S+1 labels.

## 4. Finite obstruction domain at fixed uniform rank and target

Combine AD with Theorem AC of GUARD_BUFFER_CONNECTIVITY.md. For fixed uniform floor h and exact target q>=3 let N=C(h+q-2,h). Every carrier with r>=2N is connected on its exact-q endpoints. Any failure for those fixed h,q must therefore have a representative with

    r < 2N,
    k <= 3rh+1 <= 3h(2N-1)+1,
    every endpoint root of size h,
    both endpoint hitting numbers exactly q.

This is a finite domain for each fixed h,q, even though the original question allows arbitrarily many roots and labels. A disconnected original pair would yield a disconnected reduced pair: if the reduced pair connected, its path plus exact endpoint compactions would connect the original pair. Conversely a failure in a small carrier is itself a failure of the universal fixed-h,q assertion. Additional accepted theorems may settle parts of this finite domain, but are not required for the bound.

This is a finite obstruction reduction, not an executed campaign or a guarantee of tractable enumeration. It also does not give one finite domain for all unbounded h and q. With arbitrary nonuniform floors, AD still bounds palette size for each fixed width vector, but AC does not supply the same bound on the number of roots.

## 5. Scientific stopping boundary

The missing universal step is now stated without an unbounded-palette ambiguity: for higher uniform rank it is connectivity of compact exact-q endpoints in the remaining finite carriers, especially when guards must overlap in root indices; for mixed floors, compatible guard exchange remains additionally constrained by slot sizes. None of the proofs here asserts those carriers are all connected or exhibits a disconnected exact pair.

The derived finite bound is an analytical result, not permission to enumerate its domain. The user requested mechanism-driven validation under a separate prospective protocol, not a large arity-by-arity campaign. No code or campaign is initiated by this reduction. The existing branch remains analytical and is not CLOSED/CERTIFIED.
