# One shared slot is sufficient for guard handover

Status: candidate analytical proof frozen for independent review. Baseline and admissibility: SCOPE.md. No implementation or numerical execution.

## 1. Bridge criterion for arbitrary overlap

Let A and C be exact-q endpoints on the same palette and floor vector. Put t=q-1. Suppose A has a t-guard on indices I and C has a t-guard on J. Write K=I intersect J. Define the bridge subfamily D on I union J by

- D_i=A_i for i in I minus J;
- D_i=C_i for i in J minus I;
- D_i=A_i union C_i for i in K.

**Bridge lemma.** If tau(D) >= t, A and C are connected by a finite floor-preserving primitive path with tau in {q-1,q}.

First prepare every root j in J minus I by A_j -> A_j union C_j -> C_j, adding and deleting one incidence at a time. The old guard on I stays unchanged. Each intermediate support contains either its original or destination support in that same slot and therefore respects its floor.

Next expand all roots i in K from A_i to A_i union C_i, then contract all of them to C_i. Throughout this stage each support on I union J is a subset of its corresponding D_i. Shrinking supports cannot decrease transversal number, so this subfamily has transversal at least tau(D) >= t. The fixed exclusive slots and the current shared roots supply the certificate; no unused slot is assumed. Floors hold during expansion from A_i and contraction toward C_i.

Now J agrees with C, giving a complete destination t-guard. Hold J fixed and replace every remaining root by C_i through its union with C_i. This last stage is protected by J. It reaches the exact destination, including every labelled slot and incidence.

This constructs a finite lower-guard path. Its upper excursions are not assumed bounded. Apply accepted Theorem A in GENERAL_PARENT_CONNECTIVITY.md to remove those excursions between the exact-q endpoints, obtaining tau in {q-1,q}. The result inherits no efficiency claim for this normalization.

## 2. One-overlap theorem

**Theorem O1.** Under the hypotheses above, |I intersect J| <= 1 implies the bridge condition automatically, for arbitrary positive floors.

For empty overlap D contains the unchanged old guard. Suppose K={s}. If a set H of at most t-1 labels hit every root of D, it would hit every A_i for i in I minus {s}. Because the old guard has transversal at least t, H must miss A_s. Likewise it hits every C_j for j in J minus {s}, so the destination guard forces it to miss C_s. It therefore misses A_s union C_s=D_s, contradicting that it hits D. Hence tau(D)>=t, and the bridge lemma applies.

This proof does not assert that the exclusive roots alone form a t-guard. The shared root remains present; the two guard obligations force any small transversal of the exclusive roots to avoid both its old and new support. This is why their union is safe.

Duplicate supports, full-palette roots and unequal floors require no extra condition: the argument uses the actual guard inequalities, and each destination support returns to its own labelled slot. There is no root permutation in O1.

## 3. Exact obstruction for this particular bridge

Let F be the exclusive-root family consisting of A_i, i in I minus J, and C_j, j in J minus I. For any H of size at most t-1 hitting F, put

    M_A(H) = {i in K : H misses A_i},
    M_C(H) = {i in K : H misses C_i}.

Both miss sets are nonempty: otherwise H would hit the corresponding old or destination guard. Furthermore H misses D_i at a shared slot exactly when i belongs to M_A(H) intersect M_C(H). Thus

    tau(D)>=t
    iff for every such H, M_A(H) intersect M_C(H) is nonempty.

For one shared slot, both nonempty sets must be that singleton. With two or more shared slots, their nonemptiness alone does not force intersection. This equivalence characterizes the union-bridge certificate, not existence of any repair path. Other roots outside I union J can supply additional protection even if this certificate fails.

## 4. Renewal and finite completion

During preparation, the old guard is unchanged. During shared-slot handover, D supplies a persistent comparison certificate. During final restoration, the completed destination guard is unchanged. These are successive maintained lower-bound certificates, not an assertion that exact-q redundancy holds at every intermediate state.

Each phase processes a finite ordered list of slots and, within each slot, a finite ordered list of missing or excess incidences. Every listed toggle is eligible by the guard and floor arguments above. Advancing the phase and decreasing its number of unprocessed toggles gives finite termination. A deterministic tie-break is not the reason termination holds.

At the exact destination, all exact-endpoint redundancy inequalities are restored. Hence a finite chain of exact-q endpoints, every adjacent pair equipped with guards meeting O1 (or the bridge criterion), can be connected by concatenating the resulting unit-band paths. This is a genuine renewal statement for such a chain. Existence of a chain between arbitrary endpoints remains unproved; no repeated invocation on an arbitrary tau=q-1 state is licensed.

## 5. Existing-slot consequence for uniform floors

Suppose every floor equals h and let N=binomial(h+q-2,h). The accepted guard-size argument, after exact compaction, supplies guards of sizes m_A,m_C <= N, each at least t >= 2.

If r >= m_A+m_C-1, the destination guard can be assigned to existing indices with at most one index in the old guard: at least m_C-1 indices lie outside it. A permutation of the compact destination roots realizes this assignment. Equal floors make that completed permutation admissible; use the accepted safe endpoint root-permutation theorem at exact q to connect back to the actual labelled destination. Do not permute an unprotected bare level-t guard.

O1 connects the compact start to this permuted destination; endpoint permutation and reversed compaction finish the path. Consequently

    r >= 2*binomial(h+q-2,h)-1

is sufficient for uniform-floor exact-q connectivity. This improves the previous sufficient bound by one existing slot. It is not sharpness or universal closure. Combining with the accepted palette-room theorem narrows the possible compact uniform counterexample domain to

    q <= r <= 2N-2,
    h+q-1 <= k <= rh-1.

For h=3,q=4 this gives r<=18 rather than 19, with k>=6 and k<=3r-1. These inequalities describe a necessary residual domain; not every parameter is feasible or unresolved. No enumeration is proposed. For unequal floors only O1 with actual compatible guards is asserted; the uniform slot permutation bound is not transferred to them.

## 6. Native scope

The result is first a width-floor root theorem. Conditional lifting uses the accepted child interfaces in GENERAL_PARENT_CONNECTIVITY.md Section 7: normalize at exact parents, preserve exact child interiors during root moves via fixed-root clearance, then normalize at the exact destination. Under those hypotheses the parent deviation is the only deviation during the lifted root phase, so the global total excursion remains at most one. This document does not independently establish those child interfaces or rule out native paths outside the width-floor carrier.

General multiple-overlap connectivity, access to eligible guards, and universal renewal remain open. This is an analytical sufficient condition, not implementation certification or a physical conservation law.
