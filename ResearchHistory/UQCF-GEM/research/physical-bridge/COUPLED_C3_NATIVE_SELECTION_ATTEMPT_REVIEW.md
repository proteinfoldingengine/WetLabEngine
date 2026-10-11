# Adversarial review: native selection at the four-root source

## Verdict

Reject this route as the basis for a scientific campaign against the stated ordered-palette model. Preserve it as a conditional symmetry lemma and a warning about which input resources a selector uses. It does not establish a universal physical no-go, and the assumptions supplied here do not establish a physical advance.

The argument is mathematically sound for the explicitly reduced, equality-only input. That reduct removes the very palette order that the stated published scope supplies. An impossibility in the reduct is not an impossibility in the full structure. Calling the reduct physically native does not repair this mismatch; that claim would need an independent physical justification.

This review assesses the model and published-scope description supplied in the review request. It does not independently audit the publication.

## What the lemma actually proves

Let the input state be x = ((S_i)_{i=1}^4, (k)_{i=1}^4), with S_i = B_i and the palette the disjoint union of four k-element blocks. Treat palette labels as equality-only names and keep root indices fixed. The group G = Sym(B_1) × ... × Sym(B_4) fixes x.

For an equivariant deterministic selector f, every g in G must satisfy f(x) = f(gx) = g f(x). Thus its selected outcome must be fixed by the entire source stabilizer G.

An atomic addition is specified by a receiving root i and a color c in B_j, where j differs from i. Because k is at least 2, there is another color d in B_j. Swapping c and d fixes the source but changes the addition, and changes the resulting successor. No nontrivial atomic successor is fixed by all of G. More precisely, for each successor there exists a group element that moves it; the proof does not need one group element that moves every successor simultaneously.

Taking the supplied admissibility calculation as given, all deletions violate a floor and all 12k cross-block additions are admitted with tau = 3. The obstruction therefore persists despite the existence of legal moves. It is an obstruction to a deterministic equivariant choice of a representative, not a proof that legal evolution or reachability is absent. If the output space consists only of those atomic successors and NOOP, then NOOP is the sole invariant deterministic outcome.

Both the atomicity restriction and the input restriction matter. A different transition system allowing simultaneous symmetric changes would require a separate analysis. Likewise, a different output space could contain fixed objects other than NOOP. The condition k >= 2 matters: with singleton blocks, the within-block obstruction disappears.

## Ordered-palette counterselector

Suppose the actual input includes a total palette order, as stated in the review request. Use the indexed roots to choose receiving root 1 and source block B_2. Let c be the least element of B_2 in the supplied palette order. Add the incidence of c at root 1.

This is a concrete deterministic nontrivial atomic selector at every source in the proposed family. It respects all floors and, under the supplied admissibility calculation, yields tau = 3.

It is also label-equivariant in the appropriate full-structure sense: when labels are renamed, transport the palette order along with the supports. The least member of B_2 then transports to the least member of the renamed B_2, and the selected incidence transports with it. Nontrivial permutations inside B_2 that retain the old order are not automorphisms of the full ordered input. Indeed, a finite totally ordered palette has no nontrivial order-preserving automorphisms.

Requiring equivariance under arbitrary palette permutations while holding a supplied order fixed would impose an additional requirement to disregard or override that order. It is not a symmetry requirement inherited from the stated full input structure.

This counterselector is enough to defeat an impossibility claim at the proposed family of ordered sources. It is not being asserted here as a complete policy for all possible states in a larger model.

## What other output and input choices change

* **Indexed roots:** Root indices already supply asymmetry among roots. A selector may choose roots 1 and 2 without violating palette-label equivariance. They do not distinguish the k equal-signature colors inside B_2. The reduct lemma survives indexed roots, but any claim of complete anonymity would misdescribe this input.
* **Provenance and history:** These can distinguish colors if they are supplied and available to the selector. They change the source stabilizer and must be represented in the input being analyzed. They are not automatic cures: a history that remains symmetric provides no distinguishing resource. A state-only theorem does not automatically cover a history-dependent mechanism.
* **Supplied commands:** A command naming c and receiving root i supplies a distinguishing datum. Execution can be deterministic and equivariant when that command is transported with relabeling. Executing a supplied choice is different from autonomously choosing from the reduced state. Conversely, a command that only asks for some legal move does not name a representative and leaves the reduced-state obstruction intact.
* **Invariant distributions:** The uniform distribution on all 12k admitted additions is invariant. Even choosing the indexed root pair (1, 2) deterministically and sampling uniformly among the k colors in B_2 gives an invariant distribution. Thus the deterministic no-choice lemma does not rule out an equivariant stochastic transition kernel. Individual realized samples need not be fixed by the source stabilizer. Equivariance in distribution should not be confused with a deterministic equivariant outcome for every fixed random seed; the latter depends on how the seed or randomness itself transforms.
* **Quotient outcomes:** Under G there are 12 successor orbits, indexed by the receiving root and the original block of the added color. Each orbit contains k successors. One can deterministically select an orbit using indexed roots. That provides a quotient outcome, not a selected labeled representative. Whether the quotient outcome already constitutes the physical transition depends on the independently specified physical meaning of label distinctions.
* **Actual selection:** A realized labeled successor can come from supplied order, a named command, available asymmetric memory, or stochastic sampling. The reduced-state lemma rules out only deterministic equivariant representative selection with none of those distinguishing resources in the input. It does not show that a physical device cannot select an outcome.

## Legitimate use and requirements for anything stronger

The legitimate conclusion is precise: a deterministic selector at this equality-only symmetric state must obtain symmetry-breaking information, use a different output notion, or return NOOP. This usefully separates legal-move existence from autonomous deterministic representative selection and makes the dependence on input resources explicit.

To advance a physical claim, one would need an independent account of what is physically observable and accessible, why the supplied palette order cannot be used, whether labels are gauge names or physically addressable objects, and why stochastic or quotient-valued evolution fails the actual task. If labels are merely gauge names, the absence of a canonical labeled representative may have no physical consequence. If labels denote physically distinguishable objects, the physical distinction may itself enlarge the input and break the proposed symmetry.

No such independent justification is supplied by the four-root construction. Removing order by definition establishes a conditional obstruction in a weaker model. It neither falsifies a result in the stated ordered model nor establishes a new physical boundary. Preserve this review and the reduct lemma as a rejected route with a narrow caveat; do not promote it into a universal no-go or launch a scientific campaign on this basis.

## Follow-up: review of ATTEMPT.md

I read the companion ATTEMPT.md after completing the review above. Its rejection and mathematical scope accurately incorporate this assessment. It retains the equality-only lemma, gives the decisive ordered-palette counterselector, distinguishes a mathematical selector from a derived physical update law, and explicitly rejects a universal physical no-go. The additional distinction between supplied mathematical identities and an earned physical observer reference is compatible with the review: physical accessibility is an additional question, not a reason to apply the reduct's automorphism group to the complete ordered mathematical input.

Two small precision points do not change that verdict. First, “move every single-addition successor” should be read with the quantifiers given above: each successor is moved by some source automorphism. Second, the fixed-admissible-event condition applies to a deterministic equivariant event selector; invariant distributions and quotient outputs have different fixed-point conditions, as the companion note itself recognizes. Its general least-admitted-command construction establishes mathematical choice on a finite nonempty admitted set, without claiming a local physical computation or a derived law.

I did not modify ATTEMPT.md. I have not independently validated its cited repository facts, inspected commit, archive screening, or inventory of open research questions; those are outside this review's supplied-model assessment. Nothing in this follow-up certifies those claims or reopens an existing checkpoint.
