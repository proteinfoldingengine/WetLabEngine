# A11.X1 bounded closeout: safe-prefix extension is false

## Accepted analytical result

Exact reviewed candidate: da356a65f1be3443343d0604031a615f343ba52e.
Frozen scope parent: ca6908bd04ef35bf9f297c42c8878f156d7c6263.
Proof: A11_SAFE_PREFIX_NONEXTENSION.md.
Proof SHA256: 572bb12a70b46ce31a3f9b677ba67b17e5bca85f7cf5a6e899addabcefeb429b.
Independent receipt: INDEPENDENT_A11_PREFIX_REVIEW.md.
Receipt SHA256: 01fa912324f78618435789b1aada01af17902d1bae8e64752f3155adc7a3b653.

The independent reviewer accepts all mathematical claims with no scientific issues. This closes ONLY the bounded safe-prefix question in A11_EXTENSION_SCOPE.md. It is analytical acceptance, not implementation certification.

| Question | Outcome |
| --- | --- |
| Can every safe destination-directed prefix be completed? | NO: explicit exact-four endpoints, legal prefix and all remaining moves excluded |
| Does the example exclude every complete A-to-C directed schedule? | NO: another complete lower-guard directed schedule is constructed |
| Can the stranded D reach C in the native carrier? | YES: return to A and use the alternative, with accepted normalization supplying the one-unit band |
| Must a native exit from D revisit an already completed root? | YES: its first move must delete a destination incidence at root 0 or 1 |
| Does this close universal A11 schedule existence? | NO: A11 remains OPEN |

## Mechanism and protection transfer

The fixed carrier has 15 labelled roots and 12870 existing labels. Two floors are one and thirteen are 6006. Each missing incidence in D has a private pair missed by only that root. An addition removes the pair's last protection, while a deletion from the thirteen compact roots violates the floor. The two other slots already equal C, so a destination-directed continuation has no eligible first event.

The prefix consists of 12010 individual destination additions from exact-four A and remains in {3,4}. It completes two singleton constraints too early. In the alternative schedule those singleton roots stay fixed while an old root missing their forced pair protects construction of a distinct destination root missing that pair. The new root protects all further repairs, and the singletons expand only at the end.

Thus primitive safety and decreasing unperformed-event count alone do not guarantee renewal. The example also proves that completed-root revisitation may be compulsory from a reachable defective boundary, even though a different initial schedule avoids that boundary entirely.

## Scope, dependencies and publication

A11 primary remains OPEN: neither a universal SOME-schedule theorem nor an ALL-schedules class obstruction has been obtained. A11.2-A11.4 remain uncompleted. A10 remains the last completed primary checkpoint; A11.X1 is the latest completed bounded checkpoint.

No new external design property is used. The four-dimensional binary-vector incidence construction and counts are proved within the scientific source. It is not a physical geometry insertion or numerical experiment. Accepted maximum-layer removal remains an inherited dependency; its normalized path may leave the destination-directed class. Native lifting retains accepted child-interface conditions. The original uniform-floor-three diagnostic and general q>=4 primitive/nested connectivity remain OPEN.

The pattern was identified before the scope record, as disclosed there. No retrospective prospective preregistration is claimed. No enumeration, implementation, tests, workflows or numerical campaign were performed or authorized. Engineering timing/orchestration remains separate.

Scope and proof remain frozen at their reviewed bytes. Receipt, closeout, PHASE_TRACKER.md, STATUS.json, README.md, A11_PROGRESS.md and NEXT_OBLIGATION.md are published together on research/uqcf-overlapping-guard-exchange. Executor completion requires all NINE current publication files to match an immutable GitHub readback, and the publication diff to preserve frozen scope/proof. Earlier A11 reduction/scope/review also remain unchanged.

Integrated certification branch research/v16.34-fiber-component-invariant remains separately at 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f. This checkpoint does not merge new work into that baseline or assign a numbered version.

## Next authorized obligation

Construct a schedule using a maintained future-protection invariant, proving availability and finite progress at every selected prefix, or rigorously exclude ALL destination-directed schedules for a specified admissible exact-four pair. Arbitrary safe-prefix extension is no longer a viable universal lemma.
