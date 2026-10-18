# Ancestry retention fixes the grade update

Author: proteinfolding-gpt. Date: 2026-10-18 America/Phoenix.
Source baseline: 27cfba0916317bbd6d01f7d38f585d27408954fa.
Status: positive analytical construction; unreviewed at freeze. Native bridge NOT_DERIVED.

## 1. The construction and its purpose

The current target is the actual event-to-retained-state correspondence in PROBE equation (11). The preceding GPT_DRAFT9_NEXT_TARGET proves that a retained, ancestry-respecting, order-preserving address map must be P1's nearest-prefix retraction. Here we remove the need to assume an address map or a linear grade update at the outset.

The candidate is exact preservation of the extensive grade associated with each retained ancestral predicate. The claim is precise: those preserved quantities uniquely determine every output grade. Consequently an arbitrary deterministic update, or a stochastic update satisfying the same equalities in each realization, must be the inherited P1 pushforward.

The predicates and their finite-additive grades are constructed from existing full lineage addresses and extensive source grades. Their preservation by the actual event is the single event-law obligation left by this reduction; it is NOT established merely by the continued presence of the ancestral addresses. The analysis below pursues that obligation through the original sources and states the exact limit reached. Actual receiver ownership/access and native preparability remain separate.

Actual atemporal measurement occurrence is accepted empirical input. No fundamental clock, external detector, conscious observer or extra tensor register is required. This construction introduces no event mechanism in code. It is mathematical support for the existing native-interaction candidate, not a claim of a new physical law or a new general mathematical discovery.

## 2. Inherited objects and precise types

Fix a finite nonempty prefix-closed carrier X with common Genesis o. Let Y be a nonempty prefix-closed subset containing o. Write a<=v for prefix ancestry. Grades are x in F^X, F=Q or R, in the declared signed linear diagnostic of FCV P0 and TYPE_LEDGER L6. Statements about realizable physical source grades remain conditional. Nonnegative integer grades give the explicit record witness below.

For each a in X define the source-identity predicate and its extensive total:

    h_a^X(v) = 1[a<=v],
    C_a^X(x) = sum_{v in X: a<=v} x_v.                       (1)

h is a function on source identities; C is a function on grade configurations. Neither is automatically a receiver-owned readable observable. h follows from stable full lineage addresses (augmented_lineage.py, retained_incidence.py); C follows from finite additivity once the grade instance is fixed (source_pushforward.py; FCV P0). No cross-Genesis matching is used.

Let Ch_X(a) be the immediate children of a that lie in X. The descendant cone is the disjoint union of {a} and the cones of these children, so

    C_a^X(x) = x_a + sum_{b in Ch_X(a)} C_b^X(x).             (2)

Consequently the list of all cone totals determines the grade vector:

    x_a = C_a^X(x) - sum_{b in Ch_X(a)} C_b^X(x).             (3)

This is finite-tree triangular inversion. It uses subtraction in F; no such inverse is asserted for an arbitrary additive monoid.

## 3. The retained-predicate contract forces P1

For input x and output y in F^Y, state the contract

    C_a^Y(y) = C_a^X(x) for every a in Y.                    (R)

R means preservation of the amounts belonging to each retained ancestral predicate, including total amount at o. It is stronger than retaining the names of those predicates. R is the proposed actual-event correspondence to derive, not an axiom adopted by this paper.

**Theorem 1.** For every x in F^X there is exactly one y satisfying R, and it is P_XY x.

**Proof.** Apply (3) on Y and substitute R:

    y_a = C_a^X(x) - sum_{b in Ch_Y(a)} C_b^X(x).             (4)

The cones of distinct children b in Ch_Y(a) are disjoint. The remaining identities in the cone of a are precisely those whose longest retained prefix in Y is a: any retained strict descendant has its first child after a retained by prefix closure; conversely a source below a retained child has a longer retained prefix. Thus (4) is

    y_a = sum_{v in X: r_XY(v)=a} x_v = (P_XY x)_a.         (5)

This proves uniqueness. Conversely, for every retained a, a<=r_XY(v) iff a<=v. Summing (5) over descendants of a in Y gives C_a^X(x), proving existence. QED.

In matrix notation, with Z_X x=(C_a^X(x)) indexed by X and R_YX literal restriction of such lists to Y,

    P_XY = Z_Y^{-1} R_YX Z_X.                               (6)

R_YX in (6) is not the physical response map called R in FCV P6. Equation (6) changes coordinates on the inherited grade space; it does not declare new physical storage of the totals.

**Consequences.** The update's F-linearity, total conservation, retention section P I=id and composition follow from this uniqueness, rather than being independent hypotheses on an unknown update. For composition, sequential restriction of cone totals X to Y to Z equals direct restriction X to Z, so the unique outputs agree. For the section, zero extension of a Y-grade gives the same cone totals at each retained a, so uniqueness returns that grade. This reproduces the already inherited P1/P2 laws under a different event contract; it does not newly establish their physical realization.

No E5 depth homogeneity, assumed deterministic address routing, positivity of a matrix, linearity of the unknown update, or elementary-step schedule is needed. The full set R is a substantial exact preservation requirement. Calling it one contract does not make it a weak or already-derived premise.

## 4. Relation to the previous order argument

For a deterministic identity map q:X->Y, preservation of all retained ancestral truth values is

    h_a^Y(q(v)) = h_a^X(v), for every a in Y and v in X.    (7)

This forces q=r_XY. In particular set a=r_XY(v) to get a<=q(v), and set a=q(v) to get q(v)<=v; maximality then forces equality. Conversely r obeys (7). Thus preserving the retained predicate signature is an equivalent characterization of the previous map conditions.

If grade transport is q_* along that same map, (7) implies R by finite additivity. Theorem 1 is stronger in scope: it starts with an arbitrary grade-output relation satisfying R and obtains P1 without postulating q_* first.

This equivalence clarifies the scientific limit: either route needs an independent reason why the actual event preserves the retained ancestral information in the stated type. Neither the word 'canonical' nor a change of coordinates supplies that reason.

## 5. A realized record, and the stochastic boundary

On a finite nonnegative integer domain Omega_X(N)={x:sum x<=N}, allow an arbitrary transition kernel K_x over Omega_Y(N), with no linearity or deterministic action assumption.

**Corollary 2.** If, for each admitted definite x, R holds for K_x-almost every realized y, then

    K_x = delta_(P_XY x).                                  (8)

**Proof.** Y is finite, so simultaneous almost-sure satisfaction of its equalities has probability one. Theorem 1 leaves exactly one possible y. P1 preserves nonnegative integral grades and total, so this y belongs to Omega_Y(N). QED.

This derives determinism from exact per-realization preservation in this candidate. It does not impose deterministic outcomes on all eligible native interactions. It also does not say that preservation of expectation values is sufficient.

**Explicit expectation-only control.** Take X={o,p,l}, o<p<l, Y={o,p}, input x=e_o+e_l (N=2). The P1 output is e_o+e_p. Instead let y be 2e_o or 2e_p, each with probability 1/2. Every output has total 2; E C_o^Y=2=C_o^X(x), E C_p^Y=1=C_p^X(x). Yet neither output equals P1 x. Thus preserving all these first moments does not establish a realized record law. This is an exact hand-derived example, not a numerical experiment.

## 6. Acquisition through the same inherited primitive

Take X={o,p,l,v}, with o<p<l and v another child of o. Retain Y={o,p,v}. Compare

    x_plus=e_l, x_minus=e_v.                                (9)

Both totals are one. Both give p its own grade zero, so their states on the whole formal own-coordinate algebra B_p^X agree. Under R, Theorem 1 fixes

    y_plus=e_p, y_minus=e_v.                               (10)

Thus the effect 1[y_p>0] separates the formal post-event states. For this elementary leaf pruning, (5) gives y_p=x_p+x_l and all other retained coordinates unchanged. No controller, copying gate or additional READS operation has been introduced. Later P1 consumption remains the existing CONSUMER construction; its full-source accepted scope is unchanged.

The conserved global cone quantity C_p initially already distinguishes (9). This is not a contradiction: the pre-event receiver candidate is its own coordinate algebra, not the algebra of all descendant totals. Assigning C_p as an initially available p-owned record would destroy the acquisition claim. R constrains global transport; it does not grant initial receiver access to those totals.

Actual preparability of (9), the identification of the receiver's entire initial accessible state with B_p^X (or another independently blind state), and availability of a post-event separating effect/use remain open. This theorem alone does not turn formal coordinates into actual observations.

## 7. Source-backed progress and the remaining event interface

| Original source | Established content relevant here | Event conclusion actually supported |
| --- | --- | --- |
| augmented_lineage.py; retained_incidence.py | Stable full addresses encode ancestry and intrinsic parent-child incidence | The predicates h are available as mathematical relations; no clock or geometry is required |
| identity_correspondence.py; source_binding.py | Shared identities match canonically; a certified source binding types its lineage location | Source/reference identities are usable under their stated binding premise; unmatched descendants are not automatically relocated by identity equality |
| pruning_morphism.py | The longest retained prefix supplies the structural retraction | r exists and has the stated mathematical role; the text says source identity can be pushed to an ancestor, not that every actual measurement enacts it |
| source_pushforward.py; FCV P0-P2 | Finite-additive direct-image transport yields fiber sums, conservation and composition | Once same-measure transport along r is justified, P1 is forced |
| TYPE_LEDGER L1-L8 and final boundaries | Prefix carriers, inclusions, grades and pruning arrows have explicit types | The mathematical admitted morphism class is established; physical realization of all formal sources and a unique physical response law are not certified |
| retained_morphism.py | Lineage/provenance/recoverability/composition constrain permitted correspondences within scope | These constraints do not independently identify an actual event map; its older cross-carrier limitation is not a denial of the later within-Genesis r |
| v15.16 README | Given supplied encoding/pinching, recoverable-observable expectations have an exact fixed-algebra characterization | This neither identifies those quantum operators with h/C here nor supplies R for an actual event; masks and actual-record selection remain supplied |
| PROBE / CONSUMER | Formal acquisition and internal use of P1; actual correspondence explicitly separated | Reusing internal use avoids a new reader but does not establish R or actual ownership |

The original-source trace therefore produces a precise positive reduction: an actual event that preserves these retained ancestral amounts already has the required P1 action, including per-realization behavior under the stated contract. The inspected source chain does not yet derive R from the accepted fact of measurement occurrence.

The strongest interpretation to pursue is: 'retaining an ancestral record' means that the same source amount associated with that ancestry remains represented after the event. If an existing native record supplies exactly that semantics, (1)-(8) finish the event typing without E1-E5. But retention of an address alone does not imply this statement, and the existing quantum recoverability theorem concerns a different typed representation. This proposed identification remains the next native obligation, not an additional mechanism installed here.

## 8. Scope controls and next work

- Genesis dump fails R for retained p on o<p<l with input e_l: C_p is 1 before and 0 after. The grandparent rule does likewise. These controls distinguish R from confluence and total conservation.
- Without a field or another suitably cancellative grade structure, triangular reconstruction need not hold. With Boolean OR addition on {o,p}, grades (0,1) and (1,1) have the same cone totals (1,1), so uniqueness is false. No general-monoid theorem is claimed.
- First-moment preservation is insufficient by section 5, even with total grade fixed in every realization.
- Receiver availability is not inferred from an invariant's name, centrality, or mathematical evaluation.
- The result is an exact characterization of P1 through preserved ancestral totals. It is not advertised as a weaker physical law, or as independently deriving those totals' preservation.

The next scientific task is the single typed preservation/ownership correspondence: find an inherited actual retained record whose unchanged content enforces R for this event, then connect its redistributed grade to the initially blind receiver's available state/process. Preserve the accepted occurrence input and keep preparability explicit. Do not respond by another supplied channel or another propagation/loss-law campaign.

This analytical checkpoint uses general proofs and the displayed exact controls. No scientific program, finite enumeration, simulation or archival numerical replay is executed. Independent review must examine the full positive construction and original source evidence before any acceptance claim. Native bridge remains NOT_DERIVED.

