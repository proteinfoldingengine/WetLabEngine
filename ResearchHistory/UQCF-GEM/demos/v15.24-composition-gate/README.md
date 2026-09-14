# v15.24 — Batch retention, no-signalling and independent composition

**Gate:** `BATCH_RETENTION_NON_SIGNALLING_AND_PRODUCT_COMPOSITION_DISTINGUISHED`.

This completes the interrupted v15.24 extension. Its model and tests preserve the
v15.23 channel family and original instruments byte-for-byte. The gate compares
three distinct contracts on the supplied A/B tensor factors: preserving a complete
two-event batch, no cross-input influence on local quantum outputs, and independent
product composition. It does not adopt any of them as a new physical law.

The finite classification is 15 batch-sufficient idempotents, seven non-signalling
maps and four independent products. The other three non-signalling maps have
explicit shared-phase implementations. Fresh executable verification and publication
status must be read from the exact-head Actions run and PR receipt; the mathematical
argument and a staged file alone are not a successful run.

## Run and view

```sh
python -m pip install -r requirements.txt
python -m unittest -v test_composition.py test_composition_view.py
python composition_gate.py --out outputs
python replay.py --out outputs --video
```

FFmpeg is required for the optional MP4. The GitHub delivery workflow packages the
completed 24-second video, offline HTML inspector, this report, numerical ledger,
replay data, source/CI-evidence bundle, provenance and SHA-256 checksums. The HTML is
not a deployed website. Its selectors compare alternative maps, not moments in a
physical event history. No actual record is sampled or selected.

## 1. The inherited instrument and factorization

At each of seven two-ready record contexts the earlier records are fixed. The
current sector keeps the declared factorization H_A tensor H_B. Its two ready
instruments have nonzero binary local effects F_a and G_b. Partial-trace extraction
and independent reconstruction check that the batch effects are

    Q_ab = F_a tensor G_b.

The dimensions depend on which earlier records are already fixed. The event
prerequisites, unitary operations and outcome scripts remain supplied, not derived.
In particular, this factorization is not a result about space or relativistic
separation.

The v15.23 idempotents are

    Phi_C(X) = sum_(ab,a'b') C_(ab,a'b') Q_ab X Q_a'b',

where C is a zero/one equivalence-relation matrix on labels 00,01,10,11. Its groups
specify which joint-label coherences survive. There are 15 partitions. Every map
preserves the completed batch's full subnormalized quantum branches. Preservation
of an intermediate next-event state is a different, stronger requirement.

## 2. Exact no-signalling conditions

No signalling from B to A means that A's output marginal depends only on A's input
marginal for every joint input. Taking the B partial trace removes all terms with
b != b'. The remaining local coherence response is independent of the B input iff

    C_(00,10) = C_(01,11).          [no B-to-A influence]

Likewise,

    C_(00,01) = C_(10,11).          [no A-to-B influence]

Sufficiency: the common coefficient factors out of the sum over the remote sector,
leaving a local binary block channel applied to the input marginal. This linear
identity holds for arbitrary joint operators, including entangled inputs. The
code checks its adjoint on a complete local matrix-unit basis in all seven sectors.

Necessity: prepare an equal superposition of one vector in each local effect sector
and change only the remote input between its two sectors. Unequal coefficients
then change the receiver's off-diagonal output while leaving its input identical.
For the zero/one family the witness output trace distance is exactly 1/2. Local
record probabilities stay equal because the sector populations are unchanged.
Each input's batch distribution is preserved by its map; the distributions of two
different remote preparations are not claimed to coincide.

Exactly seven partitions satisfy both equalities. Eight fail: four in both
directions, two only A to B and two only B to A. These remain valid CPTP operations;
they are rejected only under the additional no-signalling contract. No metric,
light cone, elapsed duration or physical locality law enters this classification.

## 3. Independent composition is stricter

A product of independent local block channels requires

    C = C_A tensor C_B.

The local coefficients are fixed by the marginal channels:
C_A[0,1]=C[00,10] and C_B[0,1]=C[00,01]. A putative arbitrary product channel has
these same factors by tracing over each output, so it cannot evade this test by
choosing a different representation. Within the idempotent family each local
factor is identity or binary pinching. Exactly four products remain: neither,
A only, B only, or both locally pinched. A separate realignment-rank check verifies
factorization in the four-label coefficient representation.

Thus non-signalling excludes eight of the original maps. Requiring independence
excludes eleven. Neither requirement determines which surviving map actually occurs.

## 4. Three correlated non-signalling constructions

Define D_A(alpha)=F_0+exp(i alpha) F_1 and D_B(beta) analogously. A finite mixture
of product unitaries has coefficients

    C_(ab,a'b') = sum_l w_l exp(i[(a-a')alpha_l + (b-b')beta_l]).

The three extra maps have these exact certificates:

| Retained groups | Phase pairs and weights |
|---|---|
| {00,11}, {01,10} | (0,0) and (pi,pi), each 1/2 |
| {00,11}, {01}, {10} | (theta,-theta), theta=0,2pi/3,4pi/3, each 1/3 |
| {01,10}, {00}, {11} | (theta,theta), same angles and weights |

Third roots of unity cancel the unwanted coherences in the latter two. The local
choices are correlated, not independent. All seven non-signalling maps have finite
product-phase-mixture certificates, checked by full normalized-input Choi matrices
and trace preservation in all seven contexts. No communication or shared entanglement
is needed for these particular implementations. This does not say every arbitrary
non-signalling quantum channel has such an implementation [1].

The shared variable is a resource in a mathematical implementation, not an adopted
hidden physical cause or a sampled actual outcome. The existing code evaluates the
mixture deterministically. Standard Schur-channel context is provided in [2].

## 5. Same local outputs can conceal different joint retention

At the root choose one normalized vector in each of the two local effect sectors.
On the product of their positive-phase superpositions, compare correlated parity
pinching with independent complete pinching. Both local marginals coincide. Both
have the same four record probabilities, each 1/4. Yet the joint output trace
distance is 1/2. A diagnostic X_A tensor X_B, exchanging the chosen vectors, has
expectation 1 after parity pinching and 0 after independent pinching.

No information is recovered: these are different reductions of the same original
input. The correlated output in this control is a mixture of product states; no
creation of entanglement is claimed. The diagnostic X operators are not newly
identified physical coordinates or sources.

## 6. Open alternatives and completed batches stay separate

The earlier v15.22 result still applies: one common CPTP preprocessor preserving
either full next-event instrument, including the still-unmeasured quantum output,
must be identity on the current sector. Non-signalling only constrains dependence
of local marginals; it does not preserve the whole intermediate output.

All 15 maps are checked against both full next-event instruments at all seven
contexts. Only identity survives. The model's finite nonidentity Choi discrepancies
are diagnostics, not a universal quantitative bound over arbitrary quantum channels.

For integration, a preprocessor is inserted only when the next TWO scheduled events
are exactly the two ready events. States are compared after the entire batch, not
in the middle. The test covers 15 partitions times the original 80 supplied
histories: 1,200 executions and 2,160 batch insertions. Correct completed endpoints
do not certify unchanged intermediate one-event outputs.

## 7. Executable evidence and provenance

The inherited parent is `94315bbe90d437cfc109429ec8f83fa121e5e32a`.
The copied v15.23 module is Git blob
`7c5a412c5f3925ad3656b08ccb035e9516ec108a`, with its nested hashes checked.
The tests-only parent `bca53f756507f0d33ac7eae353fe0b1391144e02` is preserved.
No older scientific file or numerical threshold is changed.

The new suite has 30 tests (24 model, six presentation). The workflow runs these
and all 406 selected inherited tests: 436 checks across fourteen suites in isolated
processes. Coverage includes 105 context/partition cases, 420 complete batch branches,
49 all-operator no-signalling certificates, 56 signalling cases with 84 directional
witnesses, 49 product-phase certificates, and the 1,200 integrated histories.
Identity ceilings remain 1e-10. Classification of the finite zero/one matrices uses
exact integer equalities and transitivity. Choi comparisons use input normalization
and Frobenius norm; state distances use half the trace norm.

The interrupted work reported local test runs, but their original raw logs were not
recovered in this continuation. They are NOT substituted for new evidence. The new
workflow explicitly replays missing-model and missing-view controls (24 and six
expected failures), labels them reconstructed absence controls, then runs the full
selected GREEN suite. Such replays establish present failure sensitivity, not the
historical timing of the original implementation. See docs/CONTINUATION_SCOPE.md.

The authoritative fresh numbers are in the release verification.json and actual
CI logs. The workflow also regenerates and fully decodes the MP4, checks its codec,
dimensions and duration, verifies ZIP member digests, and verifies all eight remote
release-asset sizes and SHA-256 digests before publication. Browser/visual inspection
must be reported separately after execution; decoding alone does not establish it.
Native Safari/iPad handling is not certified. Pending CI is never called successful.

This is self-reviewed mathematical/computational work, not independent scientific
peer review, a formal proof-checker certificate, empirical validation or the entire
repository test suite. It does not resolve older byte-exact artifact archive gaps.
No merge to main or repository visibility change accompanies publication.

## Ontology boundary

These are conditional properties of the declared instruments and tensor factors.
No actual outcome, partition selector, physical locality, entropy-production law,
fundamental time, clock calibration, carrier origin, new motion, source coupling or
gravity is derived. Pre-time reversible change remains allowed; RAS and RCR remain
separate. No new fundamental axiom or physical breakthrough is claimed. Pillar 3 is
OPEN. The remaining physical selection question is not answered by admissibility.

## Primary references

[1] Beckman, Gottesman, Nielsen and Preskill, Causal and localizable quantum
operations, Physical Review A 64, 052309 (2001), arXiv:quant-ph/0102043.
https://arxiv.org/abs/quant-ph/0102043

[2] Harris, Levene, Paulsen, Plosker and Rahaman, Schur multipliers and mixed
unitary maps, Journal of Mathematical Physics 59, 112201 (2018), arXiv:1807.06491.
https://arxiv.org/abs/1807.06491

These support standard mathematical context, not this program's physical ontology
or a novelty-priority claim.
