# Independent analytical review: fixed retained readers

**Disposition: ACCEPT_FOR_BOUNDED_ANALYTICAL_PUBLICATION; NO_MATHEMATICAL_OR_SCIENTIFIC_SCOPE_BLOCKER_FOUND.**

Review date: 2026-10-15 UTC. This is an independently authored whole-argument assessment of the exact report and proposed continuation addition identified below. It is not an independent physical discovery, historical numerical reproduction, numbered-stage certification or publication audit.

## Exact objects reviewed

Repository: `proteinfoldingengine/WetLabEngine`; research branch: `research/uqcf-overlapping-guard-exchange`.

Immutable source parent: `fca6dc85ecef559aa3e7b84026ef8c8b79353247`; source tree: `95d980cf4f84e40f20997bd7870848a93ba82b64`.

SHA-256 bindings:

- `RESULT.md`: `fb9ffa6ca1f505053f7a9c64072fefcbceef3c9047d4caaf877c4539a04d7ac6`
- `INDEX_APPEND.md`: `0f7256fc08171d22aef7fbd5ca5355e0fcab14dad8a0d81df4d064820b3e0969`
- `source_packet.json`: `73095cf331e289b5b6097e828d365737bafd648a90ae6328d5826e78b908c2cd`
- `source_identities.json`: `076d2bfdeb573af8964000b6b2d400c049fcb47c1d1605370b6b69ad8f7f2a4b`

I inspected the eleven-source packet, including its governing AGENTS, inherited reports, continuation, milestone and both code sources. Each packet content's UTF-8 byte count, SHA-256 and Git blob identity matches the accompanying identity record. These are internal packet consistency checks; independent remote retrieval and final published-byte verification belong to the separate publication audit.

## Mathematical argument

The central identity is valid for the specified ordinary-trace-preserving conditional expectation on a finite matrix algebra. The bimodule property gives E_A(aX)=aE_A(X) for a in A; taking traces proves preservation. This also follows from its Hilbert-Schmidt self-adjoint projection property. Multiplicity factors do not weaken the identity, as the inherited block-tensor formula confirms.

For each actual final-reader effect M in the common R, every expectation's adjoint fixes M. The adjoint of a finite composition therefore fixes M, independently of whether the algebras commute or are nested. Applying this to every effect of a fixed final POVM proves equality of its entire outcome distribution. It does not assert equality of every sequential instrument history. The report correctly identifies the interface as a final readout. In a decreasing algebra chain, containment in its final algebra is sufficient for containment at all prior stages; no knowledge of future algebras is inferred.

Source-dependent selection of a complete admissible nonselective path cannot help: each chosen path separately leaves that input's R restriction unchanged. A convex mixture has the same restriction because every term, evaluated on the same input, has it. Input-dependent weights do not alter that pointwise equality, although the resulting assignment need not be a linear physical channel. The report explicitly preserves this distinction. Conditioning the input by an outcome or retaining the path name is excluded for the right reason: it changes the compared interface or operation.

For a common supplied U and retained Q, moving the final expectation to the Heisenberg side gives exactly Tr(U†QU Δ). With Tr(QΔ)=0, subtraction gives equation (4); nonzero contrast is precisely the pair-specific nonzero pairing shown. Operator motion alone is insufficient. The criterion assumes a common U for the pair and does not purport to classify source-dependent dynamics or all native actions.

## Code attribution and controls

The v15.15 indexing places the supplied blank register at memory block zero. Its controller is block diagonal in memory; `copy_gate` permutes the designated memory bit by XOR with the system bit; `event_gate` applies controller then copy. `pinch_records` copies each diagonal memory block without alteration, and `weights` traces exactly those blocks. Hence the asserted weight preservation is an exact identity, not a sampled claim. The write is attributable to supplied coherent copying, with controller-prepared system data, rather than pinching. The source explicitly leaves `actual_record_selected` unset.

All displayed analytical controls are correct:

- CNOT transforms the memory-one effect into the stated two-projector expression and yields source probabilities zero and one from a common blank. Later memory pinching preserves them.
- A memory-only bit flip changes both blank memories identically, so it fails the required source-contrast test.
- Swap averaging is the expectation onto the swap commutant. The stated inputs yield local memory probabilities zero and one half. That local effect lies outside the retained algebra; its averaged joint effect already distinguishes the initial preparations. This substantive positive control prevents a universal no-writing interpretation.
- Selective conditioning of I/2 on Q yields Q and differs from the nonselective channel. Positive conditional RCR therefore survives.
- The inherited compatibility membership bit is a function of supplied projector/tree data; a fixed physical reader effect realizing it has not been given. The new theorem neither refutes that combinatorial change nor certifies its physical acquisition.

## Scientific disposition

The report and append consistently retain supplied RAS/RCR, source binding, operation, factorization and access obligations. They preserve probabilistic, partial, changing-reader and other justified alternatives. They do not require deterministic outcomes or unique microscopic dynamics. The milestone remains NOT ACHIEVED and native interaction remains OPEN. The result is explicitly an application of an inherited standard preservation identity, with no mathematical-priority or physical-law claim.

AGENTS' closure requirements are not represented as satisfied by this bounded note. I imported or executed no scientific module and performed no simulation, enumeration, historical replay or numerical campaign. I made no producer-file changes. No blocking correction is required within the stated analytical scope; acceptance does not anticipate the separate publication audit.
