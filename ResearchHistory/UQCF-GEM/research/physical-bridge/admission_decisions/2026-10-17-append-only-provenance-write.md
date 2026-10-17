# Native Interaction Candidate Decision: does the append-only provenance ledger write a source record?

Date: 2026-10-17 (America/New_York). Author: proteinfolding-grokbot (UQCF Science Agent, independent Grok line).
Inspected immutable branch head: `e0365317621c542e651082e654222b18a0453c26`.
Status: operational admission screen, analytical, UNREVIEWED (no Gemini run, because the grade is not A/B). No scientific module was imported or executed. No new physical mechanism, theorem certification, numerical campaign or native milestone is claimed.

**Grade: C overall.** The ancestry order is a native retained-record *carrier*, but it is not a record *writer*. The content-writing sub-route (the hash-chained entry) is **D**, because it re-encodes supplied labels, which the 2026-10-17 directive addendum treats as a copying channel.

## 1. Obligation addressed

This screen follows Aaron's 2026-10-17 priority: find an inherited native operation that itself creates or alters a retained record. Here I mean an operation \(\mathcal{W}\) on the retained description that meets three conditions. First, the receiver law is initially the same for the two preparations \(s_0 \neq s_1\). Second, after \(\mathcal{W}\), a justified receiver's retained data has \(\mathrm{law}(R \mid s_1) \neq \mathrm{law}(R \mid s_0)\). Third, \(\mathcal{W}\), the access and the outcome law all follow from inherited primitives. This covers milestone items 2–5.

This route has not been screened before. GPT's 2026-10-17 lineage-memory screen covers the retained-branch-identity repair code. Its V1153 screen covers the reweighting dynamics. `native_generator_probe/` (2026-10-12/13) covers the V930/V906 event-to-symbol generator. My `2026-10-17-pruning-carrier-origin.md` covers noninjective conditional expectations. None of these screens the append and anchoring operation of the provenance ledger itself.

## 2. Native primitives and the inherited operation

- v15.10 (`ResearchHistory/UQCF-GEM/v15/v15.10/REPORT.md`, blob `8b7e9665de8c0c1ef11e7e008bb58007daadfa3a`), §IV, says that the V995/V997 append-only, Genesis-anchored ledger carries an *intrinsic, ontology-native* ancestry order. That order is rooted, transitive, antisymmetric and composable. The report also says the order is not derived from pruning.
- In the V994 dependency graph (`Tmp/TOE/Einstein 4/v995_pre_report_closure_synthesis_packet/artifacts/v994_closure_dependency_edges.csv`, blob `4af52c46d38bb01bc1018ed1dc97f31924a2167a`), `symbol_emission_event_ledger` depends on `ordered_event_sequence`, `append_only_one_successor_registry_update_ledger` depends on `registry_update_history`, and `event_freshness_credential` depends on `authorized_origin_registry`.
- V997 implementation (`Tmp/TOE/Einstein 4/v997_genesis_pin_publication_audit/v997_genesis_pin_publication_audit.py`, blob `282b08b79b82be65391e1251a97891ad9c742b2f`; report `V997_FULL_STACK_GENESIS_PIN_BRIDGE_REPORT.md`, blob `8f4ee48cbaf6c822b87dd5e30a5dfee4d596e26e`):
  - The write operation is `chained_transition(prev_root, registry, step, event, witnesses) = sha256("transition"|prev_root|registry|step|event|witnesses)[:12]`. `build_path` applies it in `for i, (event, witnesses) in enumerate(zip(events, witness_sets))`, so the chain length is set by the host loop.
  - The receiver is a certifier. It checks `registry_matches`, `root_matches` against the constants `PINNED_GENESIS_REGISTRY` and `PINNED_GENESIS_ROOT`, checks `quorum_valid`, recomputes the chain in `validate_append_only_chain`, and outputs `accepted_with_genesis_pin`.

These are the candidate inherited record-writing operations: **append** \(A:(L,e)\mapsto L\cdot e\), **anchored chaining** \(r_{t}=H(r_{t-1},\rho,t,e_t,w_t)\), and **certification** \(c=\mathbb 1[\ldots]\).

## 3. Possible deduction tested, and what actually follows

**Lemma 1 (append is information-neutral).** Let \(S\) be any source variable. Write \(E_{1:T}\) for the ingested entries and \(L_T = A(\cdots A(L_0,e_1)\cdots,e_T)\) for the ledger. The map \((L_{t-1},e_t)\mapsto L_t\) is injective, and \(L_{t-1}\) is recoverable as a prefix of \(L_t\). So it is a bijection onto its image, and
\[
I(S;L_T)=I(S;L_0,E_{1:T}).
\]
For the hash-anchored version, \(r_T\) is a deterministic function of \((r_0,\rho,E_{1:T},W_{1:T})\). Data processing then gives
\[
I(S;r_T)\le I(S;r_0,\rho,E_{1:T},W_{1:T}).
\]
Equality holds only up to collisions of the 48-bit truncated digest. So no ledger operation (append, chaining or ancestry closure) can add source information beyond what its supplied inputs already carry, and append-only retention guarantees that it does not remove any. The ledger *retains* records. It never *writes* a source distinction of its own.

**Lemma 2 (naturality).** Append and the ancestry order are equivariant under every relabeling \(\pi\) of the entry alphabet: \(A(\pi L,\pi e)=\pi A(L,e)\). The order shape of a one-successor chain is determined by \(T\) alone. Hence the ancestry order carries at most \(I(S;T)\) about the source, and in V997 and V1153 (v15.10 §II.4) \(T\) is the host loop count. Every source-sensitive selection of *what* gets written lies upstream, in the emission map \(e_t=g(s,L_{t-1},\ldots)\).

**Lemma 3 (V997 records no source difference at all).** All five V997 histories use the same constant list `EVENTS = ["observe","emit_symbol","fresh_nonce","append_ledger","witness_root","registry_ok","anchor_update"]`. Their roots differ only through the supplied root string, registry tuple and witness tuples. The tampered case is a host overwrite `roots[4] = "TAMPERED_" + roots[4]`, which is not a native operation. So \(E_{1:T}\) is independent of every history label, and every root difference is a copy of a supplied certification parameter. "Same visible state, different legitimacy" is true and is preserved. But it separates *supplied counterfeit parameters*, not native source preparations.

**Quantum leg (for completeness).** Ingesting a quantum preparation into a classical ledger requires an instrument. Suppose the instrument is covariant under the block unitaries of the retained algebra \(\mathcal A=\bigoplus_i M_{n_i}\). By Schur's lemma, the block-\(i\to j\) component is \(\propto \mathrm{tr}(P_i\rho)\,\mathbb 1_j/n_j\) for \(i\neq j\), so outcome laws depend only on the central weights \(p_i=\mathrm{tr}(P_i\rho)\). A central-blind pair therefore writes identical ledgers in law (Theorem A). A noncovariant instrument is a supplied POVM, which is D under the addendum.

## 4. Strongest counterexample to promotion

Take any \(s_0\neq s_1\) with \(g(s_0,\cdot)=g(s_1,\cdot)\). Examples are the V997 constant event list itself, or any covariant emission from a central-blind pair. Then \(L_T\), \(r_T\) and \(c\) are identically distributed, while the append, chaining and certifier operations are all unchanged. A genuinely native, oriented, append-only ledger therefore coexists with complete receiver blindness, so the ledger cannot be what forces the consequence.

## 5. Accessible consequence (if the missing premise were supplied)

\(\Delta=\mathrm{law}(c,r_T\mid s_1)-\mathrm{law}(c,r_T\mid s_0)\neq 0\) at the certifier, with \(\mathrm{law}(c,r_0\mid s_1)=\mathrm{law}(c,r_0\mid s_0)\) initially. By Lemma 1, \(\Delta\neq0\) if and only if \(\mathrm{law}(E_{1:T}\mid s_1)\neq\mathrm{law}(E_{1:T}\mid s_0)\), given the shared supplied parameters.

## 6. Invalidating assumptions and supplied inputs

- The emission map \(g\) is not derived. In V997 it is a constant string list, and in V930/V906 it is a mode-selected supplied update (`native_generator_probe/`).
- The certifier's reference constants `PINNED_GENESIS_*`, the quorum rule `QUORUM = 3` and the witness registry are supplied identified references and receiver rules.
- The chain length \(T\) is the host loop count.
- Lemma 1 is exact for append and holds up to digest collisions for the 12-hex-character chaining. Neither caveat helps a promotion.

## 7. Decision, exact missing premise and next operation

**C.** The append-only provenance order is a real inherited, oriented, retained-record carrier, and that positive v15.10 finding stands. But it is information-neutral (Lemma 1) and alphabet-natural (Lemma 2), so it cannot itself write a source distinction. Its content-writing step re-encodes supplied labels (**D**).

**Missing premise P_emit:** a native emission law \(g\), derived from inherited primitives (retained-source, lineage or recoverability), with \(\mathrm{law}(g(s_1,\cdot))\neq\mathrm{law}(g(s_0,\cdot))\) for a pair that is initially receiver-blind. This is the same gap as the unrecovered V957/V960 generation and emission implementation. It is not resolved by any ledger mechanics. Do not run ledger, hash or quorum variations as native progress.

**Next inherited operation to screen:** the *compatibility check as a native record-alterer*, meaning the case where an append is *refused*. A refusal is a noninjective, retained alteration whose occurrence could depend on the source only through a derived compatibility relation, not a supplied registry. Screen it only if an inherited compatibility relation exists that is not the RAS/RCR or registry input already graded in `2026-10-17-compatibility-common-ancestor.md`. Otherwise, screen the retained-source split of `foundational-closure-verification/PROOFS.md` P2/P6/P7, specifically canonical layer decomposition and quotient descent, as a candidate source-dependent noninjective write.

Native interaction and broad C3/C4–C6 remain OPEN. Time remains pruning, an ordered recoverability update. No geometry, clock, basis, factorization, noncentral reference, outcome register or interaction was inserted.
