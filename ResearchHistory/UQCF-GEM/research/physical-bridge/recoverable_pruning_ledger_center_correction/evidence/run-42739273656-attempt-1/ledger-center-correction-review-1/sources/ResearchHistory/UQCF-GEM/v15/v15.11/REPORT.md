# v15.11 — Ontology Continuity / Retained-Algebra and Actual-Record Reconciliation

**Status:** locally verified reconciliation; repository integration remains separate.  
**Result:** `CONTINUITY_RESTORED_CONDITIONAL_ORDINAL_ORDER_PRESERVED`  
**New physical axioms adopted:** none. **Scientific breakthrough:** false. **Pillar 3:** OPEN.

## 1. Correction, not a restart

The older Library archive contains reversible pre-time motion (v10.8), a frozen non-repair boundary (v10.21), conditional nonselective pruning (v11.1), conditional realized-record history (v11.2), and conditional ordinal event time (v11.3). v11.4 already establishes duration nonuniqueness; v11.5 proposes a separate conditional clock bridge.

Those reports were absent from the v15.10 dependency manifest. Its fixed-known-potential exponential-reweighting lemma remains valid, but its results do not establish archive-wide absence of a noninjective operation or conditional ordinal-time construction. The original v15.10 code, report, summary, and measured values are preserved. `../v15.10/CONTINUITY_NOTICE.md` withdraws the overbroad interpretation without rewriting the historical snapshot.

This reconciliation reconstructs small examples independently. It is not a rerun of every original executable or a formal proof-check of the entire archive.

## 2. The ontology boundary

Pre-time motion is a reversible relational transformation, not motion along an imported clock:

\[
x\mapsto g x,\qquad g^{-1}g x=x.
\]

Composition of transformations need not be an order of irreversible events. A software loop is necessary to execute many calculations; its existence neither derives physical time nor invalidates a pre-time calculation. The full coupled V1153 system has not been proved reversible merely by inverting its isolated fixed-potential weight tilt.

The user's proposed onset of entropy and time at irreversible observational choice is retained as an ontological interpretation and research target. It is not used as an observable, a branch-selection algorithm, or evidence for a mathematical theorem. No theological label, elapsed-time parameter, entropy objective, or downstream gravity score selects the operations below.

## 3. Restore the earned conditional chain

**RAS:** a retained observable algebra is supplied. In finite-dimensional tracial theory the trace-preserving conditional expectation onto it is then canonical. RAS is an existing explicit primitive, not a conclusion of symmetry alone.

For the supplied qubit algebra spanned by I and Z,

\[
E_Z(\rho)=\tfrac12(\rho+Z\rho Z),\qquad
E_Z(|+\rangle\langle+|)=E_Z(|-\rangle\langle-|)=I/2.
\]

Input trace distance is 1 and output distance is 0. The channel loses recoverable distinctions even though each density matrix's rank increases from 1 to 2. Thus **density-matrix support reduction is not required for information loss**. The relevant property is distinguishability in the declared retained description. An unchanged fixed state or repeated application of the same idempotent projection does not certify another strict loss event.

**RCR:** an actual positive-weight central record is supplied. The code raises an error if no record is supplied; it contains no hidden sampling, maximum-weight choice, or preferred outcome. The same dephasing channel admits both projective and random-unitary instrument descriptions. Therefore the channel alone does not settle actuality or event semantics.

**Record-compatible refinement:** given RAS and RCR along a strict compatible chain, projection inclusion defines

\[
e\preceq f\quad\Longleftrightarrow\quad z_f\le z_e.
\]

On distinct nested projections this is antisymmetric and transitive. Strict inclusion reduces finite rank, so the strict relation has no cycle. Each realized finite chain has an ordinal position without a clock. Independent chains retain only their partial order; the two length-two chains in the control admit six total interleavings. This restores v11.3's **conditional ordinal-time result**, not an unconditional physical-time derivation.

## 4. Make record compatibility explicit

Nested algebras alone are insufficient. Let

\[
\mathcal A=M_2\oplus M_2,\qquad
\mathcal B=\{\operatorname{diag}(T,T):T\in M_2\}\subset\mathcal A.
\]

Their conditional expectations obey the nesting identity, but the old central record \(Q_A=\operatorname{diag}(I_2,0)\) is sent to \(I_4/2\). The old center has dimension 2 and the new center dimension 1. So a legal algebra reduction can erase the earlier classical distinction rather than refine it.

A sufficient record-preservation condition is

\[
Z(\mathcal A)\subseteq\mathcal B\subseteq\mathcal A
\quad\Longrightarrow\quad
Z(\mathcal A)\subseteq Z(\mathcal B).
\]

Proof: an old central element retained in B still commutes with every element of B because it commuted with all of A. Its projection therefore decomposes into new central sectors. This spells out the older report's **record-compatible** premise; it is not silently adopted as a new physical law selecting B.

Also, an arbitrary noninjective map need not define acyclic succession: the map `(0,1,2) -> (1,0,0)` has a two-cycle. The specific v15.10 `8 -> 4 -> 2 -> 1` witness is valid, but noninjectivity by itself is not a universal time-order theorem. Strict refinement/recoverability descent is load-bearing.

## 5. State the scope of irreversibility

A coherent CNOT dilation keeps the two inputs distinguishable in the joint output (trace distance 1), while the retained marginal makes them identical (distance 0). Keeping only a classical Z-outcome flag also fails to restore their relative phase. Reversing the full coherent operation succeeds exactly in this finite control.

This does not adopt a hidden environment as the ontology or deny objective collapse. It shows what must be specified before asserting global information destruction: which coherent degrees of freedom, records, and recovery operations are actually retained. A conditional expectation proves loss relative to its retained algebra; it does not by itself prove destruction of information in every possible enlarged description.

For the same fixture, ordinary von Neumann entropy is `log(2)` after nonselective dephasing and zero in a selected pure branch. The neutral reference I/2 also has that mathematical entropy. These are diagnostics, not a derivation of physical entropy production. No entropy-based collapse selector or equation equating entropy with elapsed time is introduced.

## 6. Do not restart the clock search

v11.4 already provides the inequivalent family

\[
D_p(\mathcal A\to\mathcal B)=\log\frac{\sum_i a_i^p}{\sum_j b_j^p},\qquad p>1.
\]

Our reconstructed block chain `[4] -> [2,2] -> [2,1,1] -> [1,1,1,1]` yields different p=2 and p=3 interval ratios even after the first interval is normalized to 1. The separation is about 0.10748. v11.5's Motion-Capacity Clock Calibration is a separate physical premise, not an automatic consequence of motion or record order. It is recorded, not adopted or rederived here.

## 7. Evidence and reproducibility

Twenty regression tests were written first. The recorded local RED run failed all twenty with the intended absent-implementation assertion. The subsequent GREEN run passed all twenty. Local execution used Python 3.13.5 and NumPy 2.3.5. Remote CI, when run, is a separate pinned-environment verification, not retroactive evidence of remote RED.

`SUMMARY.json` freezes measured diagnostics; scientific checks independently use absolute tolerances of 1e-12 for numerical identities and explicit finite separation checks. Archive float comparison uses `rel_tol=1e-9, abs_tol=1e-12`; integer, boolean, and categorical fields are exact.

`SOURCE_MANIFEST.json` records SHA-256 hashes for seven original Library snapshots and verbatim excerpt ranges. All seven originals and exact excerpt ranges were checked locally. **Repository CI without `--sources` checks the committed excerpts only; it does not reread unavailable Library originals.** The downloadable bundle includes all original source bytes for full verification. Digests demonstrate version identity, not mathematical truth.

Run from this gate directory:

```sh
python -m unittest -v test_continuity.py
python ontology_continuity_audit.py --check
# With the bundled original reports:
python ontology_continuity_audit.py --check --sources ../source_archive
```

Use the actual source directory path when running from a different layout. The bundle README gives its exact command.

## 8. Current blocker and stop boundary

The correct status is no longer “no pruning operation or ordinal history exists.” It is:

- reversible pre-time motion: preserved;
- irreversible reduction relative to a supplied retained algebra: conditional construction preserved;
- actual record and compatible ordinal history: preserved conditional on RAS, RCR, and strict record refinement;
- those primitives as an unconditional physical collapse/actuality law: not established here;
- physical entropy production and duration: not supplied by naming the operation pruning;
- source-semantics and carrier results: unchanged within their audited premises.

Do not select RAS or RCR by downstream gravity, do not rename a loop as time, and do not turn a diagnostic entropy into the physical second law. The next unresolved issue must be located against the full older dependency ledger before any new primitive or versioned rediscovery is proposed.
