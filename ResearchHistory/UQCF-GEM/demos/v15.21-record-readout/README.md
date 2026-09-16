# v15.21 — Ensemble prediction versus single-copy record events

**Result:** `ENSEMBLE_READOUT_PRESERVED_SINGLE_COPY_RECORD_INSTRUMENT_OBSTRUCTED`.

GitHub is the delivery destination. The workflow publishes the report, computed
HTML, MP4, numerical ledger and source/evidence bundle as a versioned prerelease.
No local download or manual upload is required to use this new delivery.

## What changed

Nothing in the v15.20 predictor or inherited adaptive instruments changes. This
extension tests a stronger interface: can one encoded quantum system reproduce
the original probabilities of record events, rather than merely expectation
values recovered by signed ensemble readout?

The answer is no for the first binary event, even allowing an arbitrary POVM on
the encoded system. Complete-history probabilities can nevertheless be recovered
from ensemble means. A formal branch update is also correct on the restricted
encoded image; it is not a positive map on arbitrary quantum states. These are
different contracts, not contradictory results.

## Run

```sh
python -m pip install -r requirements.txt
python -m unittest -v test_record_readout.py test_readout_presentation.py
python record_readout.py --out outputs
python replay.py --out outputs --video
```

FFmpeg is required for the optional MP4. The offline inspector includes 18 input
states and all five permissible schedules (90 views), full-history probability
curves, and a conditioning table for the supplied fixture. Playback and schedule
indices are not physical time. No record is sampled or made actual.

## 1. Frozen channel and first-event obstruction

On d=16, let Gamma=Y tensor Y tensor Y tensor Y. The frozen parity-erasing
channel is

    Phi(X) = X/2 + Tr(X) I/32 - Tr(Gamma X) Gamma/32.

It is CPTP and self-adjoint in the Hilbert-Schmidt inner product. Its kernel is
span{Gamma}. Every supplied pre-measurement unitary commutes with Gamma.

For the first A1 outcome, K=P_0 U_A1 and F=K†K is a rank-eight projector. The
operator O=2F-I anticommutes with Gamma. An encoded-system effect B reproducing
that original probability for EVERY input must satisfy Phi*(B)=F. All Hermitian
solutions are

    B = 2F - I/2 + c Gamma = I/2 + O + c Gamma,  c real.

Since O²=Gamma²=I and {O,Gamma}=0, the eigenvalues are

    1/2 +/- sqrt(1+c²).

There is a negative eigenvalue for every c, so no solution is a probability
effect 0<=B<=I. An arbitrary outcome-producing CPTP instrument would supply such
an effect by taking the trace of its branch output, so that instrument cannot
exist either. This applies to the exact all-input single-copy contract for this
fixed encoding. Ancillary processing independent of the unknown input still
induces a POVM and does not evade the obstruction. It is not a universal ban on
physical collapse or adaptive quantum experiments.

### Operational witness and tight binary error

rho_0=F/8 and rho_1=(I-F)/8 require ideal outcome probabilities 1 and 0. Their
encoded states have trace distance 1/2. Therefore any binary measurement can
produce a probability gap at most 1/2; its maximum error on this pair is at least
1/4. Measuring F on the encoded state attains probabilities 3/4 and 1/4. More
generally Tr(F Phi(rho))=p/2+1/4, so the same measurement attains the worst-case
bound 1/4 over ALL inputs. This extends the earlier direct-readout discussion by
allowing arbitrary measurement effects on the fixed encoded system.

Both encoded witness states have minimum eigenvalue 1/32. Any finite tensor
power remains full rank, so no finite number of independently prepared encoded
copies allows perfect discrimination. For this commuting pair the equal-prior
optimal error is the binomial majority-tail expression: 1/4 for one copy,
0.15625 for three, and about 0.01730 for fifteen. These are exact distribution
calculations, not sampled outcome histories or cloning operations. Standard
state-discrimination results provide the general measurement bound [1].

## 2. Adaptive history statistics survive as signed readout

For every nonempty branch of the frozen adaptive circuit, J_r(Gamma)=0. The first
measured Z projector anticommutes with Gamma, so P_b Gamma P_b=0; later branch
operations preserve zero. This includes every permissible control history.
At completion the sixteen history effects H_r=K_r†K_r are rank-one orthogonal
projectors and Tr(Gamma H_r)=0. Consequently

    q_r = Tr(H_r Phi(rho)) = p_r/2 + 1/32,
    p_r = 2 q_r - 1/16.

The inverse matrix 2 I_16 - J_16/16 has off-diagonal entries -1/16. It is not a
stochastic record-relabeling channel. Signed processing of ensemble estimates
is legitimate, but it is not an exact physical outcome on each trial. Finite-shot
estimates may be negative or greater than one; this implementation does not clip
them, call them branch weights, or pass them into a physical outcome sampler.
The 1/4 obstruction is a binary probability bound, not a bound on every final
rank-one event: for a deterministic complete history the raw encoded peak is
17/32, a deficit of 15/32.

## 3. Decode joint masses BEFORE conditioning

For a prefix effect H_h with trace r_h,

    q_h = p_h/2 + r_h/32,
    p_h = 2 q_h - r_h/16.

A conditional probability is p_(hb)/p_h. Correct both joint masses and then take
the ratio; rescaling q_(hb)/q_h directly by 2(.)-1/2 is generally wrong. The latter
rule assumes an effective mixing gain that changes when conditioning on a
correlated retained record. A parent probability at or below the numerical
resolution is rejected, not filled by a chosen branch.

In the supplied fixture, 320 conditional checks agree after joint correction to
2.22e-15. The naive local correction errs by up to 0.1440793 (14.40793 percentage
points). One example is schedule B1,A1,A2,B2, record assignment 0001: ideal last
conditional 0.7821137; naive correction 0.6380344; correct joint-ratio result
0.7821137. All input choices and read prerequisites remain explicit and frozen.

## 4. A correct on-image formula is not a quantum channel

Let D(sigma)=2 sigma-Tr(sigma)I/16. For sigma=Phi(rho), D(sigma)=Pi(rho), the
nonpositive matrix representative from v15.19. Since J_b kills Gamma,

    Phi J_b D Phi(rho) = Phi J_b(rho).

Thus a classical numerical program can compute the correct encoded branch
output from an encoded input using this signed formula. On the reachable image
it is positive and has the correct branch mass. Its extension to arbitrary input
states is not positive: a valid state outside that image gives branch mass -1/2.
The probability-effect obstruction above rules out fixing this by choosing a
different all-state positive extension with the same exact behavior.

Signed ensemble reconstruction is standard mathematical machinery; references
on error cancellation provide related context [2]. No cancellation procedure,
channel parameter, or outcome rule is adopted as fundamental physics here.

## Numerical coverage and integrity

The ledger covers 18 input states x 5 schedules x 16 final labels = 1,440 final
probabilities, 320 fixture conditional comparisons, 320 signed branch updates,
and all nonempty prefix parity-kernel checks. Local maxima:

- corrected joint-probability error: 4.44e-16;
- corrected conditional error: 2.22e-15;
- on-image signed-branch error: 6.99e-17;
- schedule-to-schedule joint-probability discrepancy: 6.66e-16.

There are 32 new tests: 26 model tests and 6 presentation tests, plus the 310
selected earlier v15.11-v15.20 checks. Local model RED was 26 intended missing
implementation assertions. Presentation RED was rerun after inherited import
paths accidentally selected an older replay module; the test now loads the
local renderer by path and has a unique filename. The misleading invocations
were not counted as new-layer verification. This does not rewrite old source.

System Chromium/Playwright set_content checked 90 input/schedule views, three
presets, no external requests/JavaScript errors, and no page overflow at widths
1280, 820, 390. Native iPad/Safari attachment behavior was not tested. The MP4 was
rendered, visually inspected and fully decoded locally. CI independently reruns
the selected suites, regenerates media, checks decoding, and verifies release
asset SHA-256 digests before publishing. Consult the actual workflow/PR receipt
for its status; this report alone does not certify CI success.

The baseline is the unchanged v15.20 tree, including its own source hash chain.
Primary module Git blob: e48f19de7c74d9c7dcf917a66bf7b06138fd36eb. Parent research
snapshot: 7b6459f18b0add90a2f88cf9b0a152e2aa5c7647. No full-repository regression,
independent scientific peer review, formal proof checking, or empirical validation
is claimed. The arguments and code received self-review only.

## Ontology boundary

This establishes an interface limit of a declared noisy mathematical predictor,
not the failure of the research ontology. Pre-time reversible change remains
allowed. RAS/RCR remain separate conditional inputs. There is no chosen actual
record, fundamental time, entropy objective, new source law, replacement motion,
or physical pruning selector. No scientific breakthrough is claimed. Pillar 3
remains OPEN. The next physical mechanism cannot be inferred merely from the
existence of an unbiased ensemble predictor.

## Primary references

[1] IBM Quantum Learning, General measurements and quantum state discrimination:
https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/general-measurements/discrimination-and-tomography

[2] Tran, Sharma, Temme, Locality and Error Mitigation of Quantum Circuits (2023):
https://arxiv.org/abs/2303.06496

These references support standard quantum-measurement and signed-estimation
context, not the project's physical interpretation or a novelty-priority claim.
