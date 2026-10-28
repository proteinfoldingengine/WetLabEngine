# A measured-instrument benchmark for the pruning-to-record connection

Date: 2026-10-28 America/Phoenix.
Source parent: `c5cefae1b1dd8d877d1a919c27f4196eb150e353`.
Status: **UNREVIEWED** exploratory physical-correspondence note, **Class C**, not an accepted native derivation. No new numerical campaign or Gemini review. Native bridge remains **NOT_DERIVED**.

## Positive construction: start from an existing operation and an actual measurement

The inherited v15.16 construction has a precise partial-pruning operation on its supplied quantum carrier:

\[
\mathcal E_S(\rho)=\sum_s P_s\rho P_s.
\]

Its projectors are extracted from the earlier supplied encoding, rather than fitted in that calculation. Its preserved record probabilities and recoverable observable algebra are established within that model. The source expressly leaves physical encoding, mask choice and access supplied. v15.17 studies descent of already supplied motion; it supplies no new physical generator.

An independently published experiment provides a concrete comparison. Blumoff et al., *Physical Review X* **6**, 031041 (2016), characterized seven subset-parity measurements on a three-qubit register using detector tomography and outcome-conditioned process tomography. Their Eqs. (6)-(7) distinguish the measured instrument from its ideal projective target. The binary output denotes a recorded classical result, not the physical ancilla's density matrix. The apparatus interaction is engineered, and the measured process is imperfect. Source: [published paper](https://jianggroup.yale.edu/sites/default/files/physrevx.6.031041.pdf_implementing_and_characterizing_jacob.pdf), DOI [10.1103/PhysRevX.6.031041](https://doi.org/10.1103/PhysRevX.6.031041), especially Secs. III D-F and Fig. 5; inspected 2026-10-28.

For the paper's ideal three-body parity example, write

\[
O=Z\otimes Z\otimes Z,\qquad \Pi_\pm=(I\pm O)/2,
\]
\[
\mathcal J_{\rm ideal}(\rho)
=\Pi_+\rho\Pi_+\otimes |+\rangle\langle+|_R
+\Pi_-\rho\Pi_-\otimes |-\rangle\langle-|_R.
\]

Discarding the recorded label gives the binary pinching map

\[
\operatorname{Tr}_R\mathcal J_{\rm ideal}(\rho)
=\Pi_+\rho\Pi_++\Pi_-\rho\Pi_-.
\]

This is the same general mathematical construction as inherited partial pruning. It is not an identification of the v15.16 sixteen-dimensional carrier, its encoding rows, or its named masks with the experiment's eight-dimensional register. Nor is pinching the P1 grade-absorption map. Replacing the earlier P1 example by this comparison changes the operation and carrier explicitly; PR #123's proofs and counterexample remain untouched.

The important physical input is that the record and conditioned update were characterized in an actual instrument. In the experimental model use its reconstructed maps \(\widehat{\mathcal F}_\pm\), not exact ideal projectors:

\[
\widehat{\mathcal J}(\rho)=\sum_{r=\pm}\widehat{\mathcal F}_r(\rho)\otimes|r\rangle\langle r|_R,
\qquad p(r\mid\rho)=\operatorname{Tr}\widehat{\mathcal F}_r(\rho).
\]

The notation encodes recorded outcomes. It does not construct a new physical receiver or establish ownership by a native address. Experimental reconstruction supplies evidence about this specific instrument; it does not make its interaction a consequence of UQCF-GEM.

## A small check linking calibrated readout to an observable contrast

This elementary conditional calculation is a check of the comparison, not a new native theorem or experimental result. Suppose an independently established lower bound \(f\) on the squared worst-case detector fidelity holds relative to the ideal binary measurement. For a pure input in the plus sector the ideal output is the certain plus label, so fidelity to the actual output equals its plus-outcome probability. Hence \(p(+\mid\tau_+)\ge f\); likewise \(p(-\mid\tau_-)\ge f\). Convexity of the outcome probabilities extends these two inequalities to mixed states supported in their respective sectors. Therefore

\[
p(+\mid\tau_+)-p(+\mid\tau_-)\ge 2f-1.
\]

Thus a validated \(f>1/2\) would suffice for a nonzero contrast in the already specified recorded outcome, without choosing a new separating observable. This calculation neither derives the prepared states nor supplies complete initial receiver blindness. The paper's numerical estimates are not adopted here as certified confidence bounds. No raw experimental data were reanalysed and no numerical prediction is claimed for a new experiment.

High readout performance alone would not establish the required state update. Detector statistics and the full conditioned process must be kept distinct. No detector-fidelity bound is being used as a proof of exact physical retention or exact pinching.

## What is physically identified, and what remains native work

| Connection | Status of this note |
| --- | --- |
| An actual experiment to its reconstructed measurement instrument and recorded outcomes | An externally supported benchmark is identified in the primary paper. |
| The instrument's ideal reduced map to the general inherited pinching formula | Algebraic correspondence of form; actual noise remains explicit. |
| Genesis-pinned native preparations to the laboratory input states | Not supplied or derived. |
| The actual instrument to a native-forced interaction | Not derived; its physical coupling is engineered. |
| A designated blank ancilla to complete initial receiver blindness | Not established; preparation controls and other accessible records cannot be silently excluded. |
| The experiment to one actual P1 grade-absorption event | Not established; the two maps are different. |

This comparison replaces a freely chosen response operator with an independently characterized physical observation as a benchmark. It does not meet the instruction to derive an interaction without supplying the coupling. It is therefore documented briefly as Class C and is not grounds for another numerical or review campaign.

The next substantive native step would have to identify an inherited source/operation association with independently calibrated physical inputs and an owned receiver, then evaluate that same instrument without refitting the encoding or observable to force a contrast. No source in the bounded inspection provided that association. The experiment is not evidence that arbitrary native pruning events implement this instrument, and the existence of its outcomes does not resolve native access.

## Exact inherited sources consulted

All paths are relative to `ResearchHistory/UQCF-GEM/` at the source parent above.

| Source | Git blob |
| --- | --- |
| `demos/v15.16-partial-pruning/README.md` | `982e54d04286eb365e6ee624879b882f3cdf281a` |
| `demos/v15.17-retained-motion/README.md` | `2b0c05992b81ce7b6ce52b85dc790b3157f7cae9` |
| `research/physical-bridge/record_consumer_trace/NATIVE_STATE_RECORD_INTERFACE.md` | `e14824cb24f049882d41f416e0728ea075898274` |
| `research/physical-bridge/record_consumer_trace/TRACE.md` | `19605ddf5a91c6607c9621796daffcbaf3d31978` |

The interface note already identifies the missing native-grade-to-quantum-input assignment; this is not counted again as a discovery. The new input to this attempt is the inspected experimental instrument characterization. No archive-wide novelty claim, complete source search, native signal, physical law or milestone is asserted.
