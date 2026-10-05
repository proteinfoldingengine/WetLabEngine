# SUPERSEDED PRE-SCOPE EXPLORATORY NOTE

This file records an unreviewed color-relay argument developed concurrently with the accepted A11.X59 line. It is NOT the accepted X59 theorem and must not be cited as X59. The accepted X59 result is A11_X59_ANCHOR_MIXING_RENEWAL.md at corrected candidate 75c411628357330520d7f769c32a2c3fa27e4bff. The stronger universal color-relay claim below is being moved to a separately frozen X60 question so that it can receive fresh whole-argument review. Nothing below is accepted merely because this exploratory file exists.

# A11.X59 — prescribed anchor-mixing repair by color-relay renewal

Status: exact analytical candidate for fresh independent whole-argument review. Analytical only.

Frozen scope: A11_X59_SCOPE.md on research/uqcf-overlapping-guard-exchange, created after X58 publication head d955a6e884cba250eb0f2c8bcdaa393460fb7a4d.

No numerical execution, implementation, benchmark, integration merge, or numbered certification is claimed.

## 1. Fixed carrier and theorem

Fix a finite labelled role set G, anchors A={0,1,2,3}, outside roles R=G minus A, and an ACTUAL simple graph Gamma_a on R for each anchor a. Declare exactly the actual root types

    Q={a} union e,   e in E(Gamma_a),

with arbitrary positive numbers c_Q of ORIGINAL labelled copies.

Assume the colored guard

    (C)  vc(union_{a in J} Gamma_a) > |J|

for every nonempty J subseteq A.

Fix IN ADVANCE an arbitrary permutation pi of G. Unlike X58, no requirement pi(A)=A is imposed and no role relabeling follows the declaration.

For t>=1 use pairwise distinct original column labels x_(s,h), s in G, 1<=h<=t, and fixed pairwise-disjoint padding Z_j of arbitrary sizes p_j>=0. Source role groups are

    B_j=Z_j union {x_(j,h):1<=h<=t},

and destination role groups are

    D_j=Z_j union {x_(pi^{-1}(j),h):1<=h<=t}.

Each original copy of type Q has source support E_Q=union_{j in Q}B_j and destination C_Q=union_{j in Q}D_j. Its SAME ORIGINAL positive floor may be any f_i<=N_Q, where N_Q=3t+sum_{j in Q}p_j.

**X59U — arbitrary prescribed permutation.** Every such source/destination pair admits an explicit finite native path with

    3 <= tau <= 4

after every one-incidence primitive, preserving every same-slot original floor and restoring the FULL exact labelled/noncompact destination. The construction is renewable over all t columns.

Every endpoint-differing incidence toggles exactly once and no other incidence changes. Hence the path globally attains the endpoint Hamming lower bound

    L = t sum_Q c_Q |Q symmetric-difference pi^{-1}(Q)|.

This includes permutations mixing anchor and outside roles. X58 is recovered as a special case, but X59 uses a different upper mechanism: a moving physical cover relay rather than one fixed anchor cover.

## 2. Colored footprint lemma without anchor preservation

Condition(C), as proved in X58, is equivalent within this carrier to:
1. A is the unique role hitting set of size at most four; and
2. every role footprint F with |F|<=4 and F!=A has an ACTUAL avoiding type.

During active column h, physical label x_(s,h) has source owner s and destination owner pi(s). Labels from other columns or padding have one fixed current owner while column h is processed.

A physical pair containing at most one active-column label therefore has a role footprint of size at most three and has an actual common endpoint-union witness.

For two active labels indexed by S={s,t}, the complete old/new footprint is

    F_pi(S)=S union pi(S).

Its size is at most four. If F_pi(S)!=A, condition(C) supplies an actual type Q avoiding the complete footprint. Every intermediate support of a copy of Q stays inside its source/destination union for this column, so that copy avoids the physical pair throughout its own changes as well.

Suppose F_pi(S)=A. Because the union equals A, both S and pi(S) are subsets of A. Since |S|=|pi(S)|=2 and their union has four elements, they are disjoint and

    S subset A,    pi(S)=A minus S.

Define

    E_pi={S subset A: |S|=2 and pi(S)=A minus S}.

These and only these active physical pairs can lack a common endpoint-union witness.

For S in E_pi, every source root whose anchor color lies in A minus S avoids the pair: its only anchor is outside S and its other two roles lie outside A. Every destination root whose anchor color lies in S avoids the pair because the destination owners of the physical pair are pi(S)=A minus S. Thus lower protection for S transfers from old colors A minus S to new colors S.

No use of pi(A)=A occurs in this characterization.

## 3. At most four exceptional obligations

Put

    D={a in A: pi(a) in A}.

Every exceptional S is a two-subset of D.

If |D|<=3 then |E_pi|<=C(3,2)=3.

If |D|=4, injectivity gives pi(A)=A. It remains only to inspect the five cycle types of the induced permutation on four anchors:
- identity: no exceptional two-set;
- one transposition: none;
- one three-cycle: none;
- two disjoint transpositions: four;
- one four-cycle: two.

Therefore in every case

    |E_pi| <= 4.

This is a finite structural classification of the four-anchor permutation, not a numerical experiment.

## 4. A deterministic lower-safe anchor-color order always exists

Choose a uniformly random ordering of the four anchor colors only as a finite counting device.

For fixed S in E_pi, the bad event is that BOTH old witness colors A minus S occur before BOTH new witness colors S. Among the C(4,2)=6 relative choices of the two positions occupied by S, exactly one is bad. Hence

    P(bad_S)=1/6.

Let Z be the number of bad exceptional sets. By linearity of expectation, with no independence assumption,

    E[Z]=|E_pi|/6 <= 4/6 < 1.

Therefore at least one of the 4!=24 anchor orders has Z=0. Fix deterministically the lexicographically least such order

    a_1,a_2,a_3,a_4.

Equivalently, for every S in E_pi,

    first(S) < last(A minus S).

This exact inequality is the lower-handover certificate used below. The counting proves existence; execution is deterministic and contains no randomized native step.

## 5. Moving upper covers at completed color boundaries

Fix one active column h. Let J subseteq A be the prefix set of anchor colors already completely processed in the chosen order. Define the physical set

    K_J(h)
      ={x_(a,h): a in A minus J}
       union
       {x_(pi^{-1}(a),h): a in J}.

Repeated physical labels are included only once, so |K_J(h)|<=4.

At a completed color boundary every root copy whose anchor color a lies in J has its active-column incidences at destination; it contains x_(pi^{-1}(a),h). Every root whose anchor color a is outside J is still at its active-column source; it contains x_(a,h). Hence K_J(h) hits EVERY actual root.

For J=empty this is the source anchor cover. For J=A it is the destination physical cover indexed by pi^{-1}(A). If pi(A)!=A these endpoint covers can differ.

The cover may temporarily have fewer than four distinct labels when pi^{-1}(J) overlaps A minus J. This is allowed: the lower proof below prevents tau<3, while K_J gives tau<=4.

## 6. One color transition with copy coexistence

Let a be the next anchor color and J the already processed prefix.

Before deleting any active-column source incidence from any color-a copy, PREPARE every original copy of every color-a type as follows. Put

    y=x_(pi^{-1}(a),h).

The destination support of every color-a root contains y because pi(pi^{-1}(a))=a belongs to its type. If y is absent in the current source support, add that literal endpoint-differing incidence. If it is already present, perform no edit.

During this entire preparation K_J(h) remains a cover because no source incidence has been deleted and every color-a root still contains x_(a,h).

After every color-a copy has been prepared, K_(J union {a})(h) is ALSO a cover:
- every already processed color b in J is hit by x_(pi^{-1}(b),h);
- every still unprocessed color b outside J union {a} is hit by x_(b,h);
- every active color-a copy is hit by the prepared y.

Now finish every color-a copy in fixed labelled order. Add every other absent destination-only incidence for column h, then delete every old-only incidence, all in fixed palette order. K_(J union {a})(h) hits the active copy through y and hits all other copies by the cases above.

Thus the upper witness can move from K_J to K_(J union {a}) without completing one copy before preparing the others. This explicitly resolves the copy-coexistence failure that blocks a naive whole-copy cover switch.

Every preparation addition is an endpoint-differing incidence. No extra incidence is introduced solely to carry the upper cover.

## 7. Lower protection through the SAME color relay

Consider any physical pair.

If it is nonexceptional, Section 2 supplies an actual type whose complete old/new union avoids it. Any original copy of that type remains an actual witness through every partial support, regardless of the color schedule.

Fix exceptional S in E_pi. Old witnesses have colors A minus S and new witnesses have colors S.

Before the first color in S completes, the order condition

    first(S) < last(A minus S)

guarantees at least one color in A minus S is still completely unprocessed. Any actual root copy of that color remains at source and avoids the pair. In particular it remains untouched throughout preparation and completion of the first S-colored block.

Once the first color in S completes, every completed destination root of that color avoids the pair and remains completed for the rest of the column. It supplies a persistent new witness while all remaining colors are processed.

More generally, if an old-witness color is active before the first S color, it cannot be the last old-witness color, again by the strict order inequality; the other old color remains untouched. If an old-witness color is active after the first S color, a completed new witness already exists.

Therefore every exceptional pair has an ACTUAL missed root after EVERY preparation addition, ordinary destination addition, and old-only deletion. Shared roots may witness several obligations simultaneously; no capacity is allocated independently.

All physical two-label sets are excluded. Since the palette has at least four active role labels at an exact endpoint, a hitting set of size zero or one could be extended to a two-label hitting set. Hence

    tau >= 3

throughout the same path on which Section 6 gives tau<=4.

## 8. Original floors and literal primitive legality

For each active original copy, preparation and the remaining destination additions occur before any source-only deletion in that copy.

Until deletion begins, its support contains its complete current-column source support. After all destination additions are present, deletion leaves a support containing its complete current-column destination support. Previous completed columns and later unresolved columns have the same number of labels per role group, and fixed padding never changes.

At every completed column boundary the copy returns to its endpoint size N_Q. During its edits it never falls below N_Q. Therefore every same original floor f_i<=N_Q is preserved, including unequal saturated floors.

Every listed addition is of an absent endpoint-destination incidence; every listed deletion removes a present endpoint-source-only incidence. Common incidences and padding are fixed. Empty lists create no fictitious native primitive.

## 9. Continuation, termination, renewal, and exact destination

For one column:
1. the chosen anchor-color order has four finite blocks;
2. each color has finitely many actual types and original copies;
3. each copy has a finite preparation/add/delete list.

Whenever work remains, the first pending literal incidence in this deterministic schedule is legal by Sections 6–8. Each primitive decreases the finite pending-incidence count by one. Each color finishes, and after four colors every actual root has all active-column incidences at its exact destination.

The completed column restores the same role-group cardinalities, exact-four endpoint template, colored graphs, copy multiplicities, original floors, and condition(C). Previous columns are fixed at destination and later columns remain at source. For the next column, pairs involving an inactive label have footprint at most three, and the same proof applies to the two active labels. Reuse the same deterministic anchor order.

The number of unresolved columns decreases from t to zero. At completion every column label has its prescribed owner, padding is unchanged, and every ORIGINAL labelled root copy equals its exact C_Q support.

No exact-four reset is required inside a color block; level three is allowed.

## 10. Global endpoint Hamming minimum

For root type Q and one column h, physical x_(s,h) is present at source exactly when s in Q and at destination exactly when pi(s) in Q, equivalently s in pi^{-1}(Q).

The construction changes exactly those incidences in

    Q symmetric-difference pi^{-1}(Q).

The special preparation incidence y is one of these destination-only incidences whenever it is absent; it is never repeated. Every other destination-only incidence is added once, every old-only incidence deleted once, and every common incidence left fixed.

Thus the complete path length is

    L=t sum_Q c_Q |Q symmetric-difference pi^{-1}(Q)|.

Every native primitive changes one incidence, so any path between the exact outer endpoints has length at least their incidence Hamming distance L. X59 attains that lower bound globally.

This is a mathematical edit minimum, not an executed runtime or efficiency benchmark.

## 11. Structural anchor-mixing control

Take any valid colored carrier satisfying(C), t=1, no padding, singleton role groups, and prescribe a permutation with pi(A)!=A, for example a single transposition (0 r) with r outside A.

Condition(C) makes A the unique source role cover of size at most four. The destination's unique physical four-cover is pi^{-1}(A), which differs from A. Therefore X58's one fixed physical anchor-cover identity cannot span both endpoints.

For the transposition, the X59 relay begins with K_empty=A and ends at K_A=pi^{-1}(A). During color 0, all copies whose only old upper hit is x_0 receive the endpoint-required x_r before any such x_0 is removed. The old and new covers coexist at the preparation boundary, after which the destination cover can carry the remaining edits.

This control establishes the need for a moving upper witness in the X59 proof. It does NOT claim that every alternative native path requires the same relay.

A more coupled mixed permutation may have E_pi nonempty. The theorem above handles it on the same color order; no separate supplied seed/reserve system or post-declaration relabeling is required.

## 12. Relation to X58 and remaining limits

X58 fixed pi(A)=A, so one physical anchor cover remained valid and its seed/reserve phase handled up to four simultaneous lower obligations.

X59 removes pi(A)=A. Its color-block order simultaneously performs two jobs:
- the order inequality transfers every exceptional lower obligation from old colors to completed new colors; and
- the prepare-all-copies step relays the upper witness from K_J to K_(J union {a}).

The result is stronger within the SAME supplied colored carrier: arbitrary prescribed pi, direct band, renewable columns, arbitrary positive original copies and unequal saturated floors, exact labelled restoration, and global endpoint-toggle minimum.

The theorem does NOT prove arbitrary exact endpoints can be represented in this colored form, that condition(C) is necessary, a whole-root-order obstruction, multiple independently moving anchor blocks, unrestricted mixed-floor/directed/higher-target/nested universality, a new native connectivity class, or a physical force law.

No numerical evidence is used in the theorem. The finite exploratory checks disclosed in the frozen scope served only to locate the color-relay proof.

Fresh independent whole-argument review is required before acceptance. A separate reporting/publication review and immutable source/tree/reference readback remain required before calling X59 published/verified.

v16.55 and v16.54 remain unchanged. Separate efficiency runner/fixture/benchmark work remains unstarted.
