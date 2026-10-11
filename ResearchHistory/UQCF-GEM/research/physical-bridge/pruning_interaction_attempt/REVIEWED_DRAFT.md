# Attempt to derive the pruning-record interaction

Date: 2026-10-11. Immutable inspected parent: 7c4d7ec35845295d2fe578e4ce57ebe93bbeb589.
Status: analytical candidate assessment, pending separate review. No physical interaction is claimed derived.

## Approved physical objective and concrete candidate

The preceding pruning-record result proves a protected conditional record under same-union pruning of indexed views. The approved next objective is to obtain the interaction from an inherited mechanism, with a retained accessible output, rather than adopt deletion-only evolution because it makes the example work.

The candidate tested here is the inherited canonical ancestral retraction: choose a retained prefix-closed set Z in a supplied lineage tree T, and apply the SAME retraction to every indexed retained view. This is the most literal way to try to obtain the prior view-pruning interaction from common lineage pruning. The retained set Z itself is still supplied; the obstruction below holds even after granting arbitrary selection of Z, including source-dependent selection. It is a structural failure of this proposed connection, not a complaint that an actual outcome has not been selected.

The source trace also checks whether the existing event-sufficient quantum operation or extensive source pushforward repairs this particular connection. Neither is dismissed as mathematically invalid. Their input types and supplied premises are recorded separately.

## 1. Uniform ancestral pruning leaves surviving incidence unchanged

Let T be a finite rooted prefix tree, with a finite nonempty fixed index set P. Let (Y_i) be root-containing prefix-closed views with union T, and let S_v={i:v in Y_i} be the equivalent native nested supports. Let Z subset T be nonempty, root-containing and prefix closed. The inherited map r_Z:T->Z sends each vertex to its longest retained ancestor.

Define the proposed uniformly pruned views by direct image:

    Y'_i = r_Z(Y_i).

**Identity.** For every i,

    r_Z(Y_i) = Y_i intersect Z.

Proof. If y belongs to Y_i, every ancestor of y belongs to Y_i. In particular r_Z(y) belongs to both Y_i and Z. This proves one inclusion. Conversely, if z belongs to Y_i intersect Z, r_Z(z)=z, so z belongs to the image. QED.

The pruned views are prefix closed and have union Z. At every surviving vertex v in Z,

    S'_v = {i:v in Y'_i} = {i:v in Y_i} = S_v.

Thus uniform ancestral pruning removes whole vertices from the common carrier but changes no indexed support at a surviving named vertex. The statement is about support membership, not about local hitting numbers on a changed child set, extensive amounts, or a newly chosen decoder. Those other quantities can change.

This gives an exact realization test. A P-indexed target cover (W_i) of a retained prefix tree Z is obtainable by the proposed uniform operation iff W_i=Y_i intersect Z for every i, equivalently iff its support at each surviving vertex is the original S_v. Necessity is the identity; sufficiency follows by applying r_Z. No numerical search or normalization theorem is used, and no general originality claim is made for this elementary retraction identity.

If the output union must remain the original T, then Z=T. The uniform operation is then the identity on every view. In particular it cannot perform any nontrivial same-union incidence deletion from the preceding result.

The same conclusion survives any finite composition of uniform prefix prunings. Each surviving named vertex keeps its initial support; equivalently the composed ancestral retraction is the direct retraction to the final retained subset. Choosing Z from source data does not alter this identity.

## 2. Failure on the declared positive record

The preceding five-vertex fixture has o with children u,C, u with leaves r,w, palette {a,b,c}, root support the full palette, and

    S_u=S_w={a,b}, S_C={c},
    S_r={a} in source zero, S_r={b} in source one.

Both preparations have profile (h_o,h_u)=(2,1). The same-union positive route for source one is -a(w), -a(u), ending at S_u={b}. Its positive memory projection is R=1[a absent at the still-existing u].

Under any uniformly applied ancestral pruning that retains u, S'_u remains {a,b}. Hence R remains zero in both source preparations. Removing u instead does not write this record: it removes the named output vertex and leaves the declared decoder without its required carrier. It is not an admitted positive endpoint for this task. The failure holds for every choice of Z, not just a symmetric or source-blind selection.

The successful same-union route changes only view a: it removes w and u from that view while the other views retain those vertices. Uniform pruning cannot remove a vertex from one view and keep it in another. That is the exact missing interaction in this attempted derivation.

## 3. What selective pruning would have to supply

The inherited v16.25 relation allows a family of individual retained subviews Z_i subset Y_i. Applying each view's own ancestral retraction gives those chosen Z_i. Requiring their union to remain T supplies the same-union guard. This is exactly the relation used in the preceding conditional theorem.

However, the family (Z_i) is an input to that comparison. The general retraction construction does not compute it from a physical source event. The source proof shows composition and monotonicity once the subviews are given. It does not establish which views lose which incidences during an interaction, or physically enforce preservation of their union.

A proposed physical realization therefore needs BOTH a justified indexed action, specifying how an actual event affects individual retained views, and the retention condition protecting the required carrier across that action. Calling the same global retraction once for each view with the SAME Z cannot provide this; calling it with different Z_i supplies the missing selective inputs.

The union condition is not cosmetic. It prevents deletion of the last support for a source witness. The following deliberately changed-carrier control shows why it cannot silently be inferred from the word pruning.

First uniformly prune the leaf r from the five-vertex tree: Z=T\{r}. This is a legal prefix retention. The two initially different view families become identical on the four-vertex carrier Z: S_u=S_w={a,b}, S_C={c}. Then, on that coarse carrier, selectively prune -a(w) and -a(u). Both original sources now yield the same positive memory S_u={b}.

At every state the current supports are nonempty and nested; the two remaining internal hitting numbers are (2,1). The coarse u is unary, which is permitted by the general prefix-view category but outside the old fixed binary/ternary carrier. This is not a counterexample to the previous fixed-T, same-union theorem: the first step violates precisely its fixed-union premise. Nor is this composite operation adopted as actual dynamics. It is an analytical control showing that ordinary common pruning can remove the protected witness, after which the otherwise legal selective update no longer certifies the original source.

## 4. Trace of the inspected event and source maps

The current source inputs are pinned in source_readbacks.json. This is an inspection of these concrete files, not a claim that the entire archive contains no other mechanism.

| Inspected mechanism | What its source actually supplies | Why it does not derive the selected interaction |
|---|---|---|
| v15.56 pruning_morphism.py | Canonical longest-retained-prefix map for a supplied retained subset | Uniform direct images leave surviving incidence unchanged; individual selective retained subsets are not produced |
| v15.56 source_pushforward.py | J_c(v)=sum of J_f over the retraction fiber, forced by finite additivity of the supplied extensive grade | It transports amounts, not view membership; it does not specify (Z_i), initialize an incidence record, or make it accessible |
| v15.22 event_sufficiency.py and README | E_e(rho)=sum_b F_b rho F_b with F_b=K_b^dagger K_b, canonically sufficient for a supplied next instrument | The instrument is an input. Preprocessing retains the existing records and does not generate the source/view coupling |
| v15.22 baseline/adaptive.py (inherited v15.14) | Explicit READS dependencies; B2 rotation uses a supplied already-realized A1 bit and the declared angles +0.6 or -0.6; advance also takes an outcome argument | This is an illustrative feed-forward interaction with an already available record and supplied operation, not a derivation of the first input record or selective lineage-view action |
| v15.16 recoverability.py | Partial record pinching selected by an explicit four-bit mask on a supplied completed quantum encoding | That mask is neither derived nor an indexed lineage-retention family. Identifying its record bits with view labels would require an additional carrier/action connection |

The event-sufficiency result remains a valid exact conditional factorization; its failure to supply this interaction is not caused solely by the separate actual-outcome input. Even before outcome selection, the next instrument and its record dependence are supplied. Conversely, lack of deterministic outcome selection would not invalidate a genuinely derived interaction.

Likewise the extensive source channel can have a nontrivial source-dependent output after actual specified pruning. The source_binding.py and retained_amplitude.py inputs distinguish certified localization, relative retained grade and absolute observer normalization. Those existing conditional source constructions are preserved. They do not, in these files, identify extensive amounts with the selected incidence memory or supply an accessible physical readout of it. An amount-based consumer would require its own justified contract rather than being substituted for R after this candidate fails.

## 5. Scientific disposition and re-entry requirement

The candidate is stopped at a precise representational obstruction: uniform ancestral pruning cannot write a changed support at a surviving vertex. This is stronger than saying that the retained subset has not yet been selected; arbitrary selection of that subset does not fix the attempted map. The source trace locates the remaining supplied interaction inputs in the inspected alternatives.

Disposition sought: UNIFORM_PRUNING_INTERACTION_CANDIDATE_REJECTED; SELECTIVE_INTERACTION_AND_ACCESS_NOT_DERIVED.

The approved physical objective is NOT completed. No native force, physical record-acquisition law, actual successor law or retained observer access has been derived. No universal impossibility of interaction is claimed. The prior pruning-record theorem and its conditional positive example remain intact.

The next admissible candidate must explicitly provide an inherited event-to-indexed-view action and justify preservation of the carrier distinctions on which historical soundness depends, together with accessible use of the resulting record. A genuinely different amount-based or quantum interaction is also possible in principle, but its carrier, native inputs and output contract must be earned and declared before testing. Do not insert a hidden-state read, a prescribed answer-dependent pruning mask, a supplied feed-forward rotation relabeled as a derived law, or automatic legal commitment.

No numerical implementation or campaign was run. The retraction identity and control were worked out analytically before review; no prospective execution is claimed. The historical 527-test checkpoint is unchanged and not rerun. This assessment is not a numbered-stage CLOSED/CERTIFIED claim, a main merge or physical closure. Time remains pruning / ordered recoverability update; no fundamental duration, geometry, dark-matter variable or Einstein-residual selector is introduced.
