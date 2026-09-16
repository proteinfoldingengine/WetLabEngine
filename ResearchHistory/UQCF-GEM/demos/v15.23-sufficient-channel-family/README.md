# v15.23 — Complete sufficient-channel family / idempotent retention

**Result:** `SUFFICIENT_CHANNELS_CLASSIFIED_BINARY_IDEMPOTENCE_SELECTS_PINCHING`.

The v15.22 instruments, record prerequisites and source are unchanged. This
extension classifies every same-carrier CPTP preprocessing that preserves a
specified sharp event's complete branch outputs. The earlier conditional
expectation is one member, not the entire family. No physical selector is added.

## Reproduce and view

```sh
python -m pip install -r requirements.txt
python -m unittest -v test_family.py test_family_view.py
python retention_family.py --out outputs
python replay.py --out outputs --video
```

FFmpeg is required only for the MP4. The GitHub release contains the 24-second
video, computed offline HTML, report, numerical ledger and source/evidence ZIP.
The 81 inspector settings compare alternative channels on the same input, not
successive physical events. No live website is deployed. GitHub is the delivery
destination; local computation is working space, not a requested user handoff.

## 1. Exact classification, not only examples

Let the supplied sharp instrument have nonzero orthogonal input effects F_b
resolving identity and one partial-isometry branch K_b per outcome:

    K_b† K_b = F_b,     J_b(X) = K_b X K_b†.

The requirement is J_b Phi = J_b for EVERY branch and input, with the original
complete quantum branch output unchanged. The current carrier and already
realized record sector are fixed. This is stronger than preserving probabilities.

**Theorem in this scope.** All such CPTP preprocessors, and only those, are

    Phi_C(X) = sum_(b,c) C_bc F_b X F_c,
    C >= 0,  C_bb = 1.

Thus the remaining object is a correlation matrix on the supplied outcome labels.

**Necessity.** The adjoint Psi=Phi* is unital completely positive. Exact branch
preservation fixes each K_b† Y K_b and hence the full block algebra
A=direct_sum_b F_b M_d F_b pointwise. For every unitary W in A, the fixed-unitary
multiplicative-domain identity [1] gives, for any Kraus representation L_alpha,

    sum_alpha (W L_alpha - L_alpha W)†(W L_alpha - L_alpha W) = 0.

Each positive summand vanishes. Every L_alpha therefore commutes with A and is
scalar on each block: L_alpha=sum_b ell_(alpha,b) F_b. Consequently
C_bc=sum_alpha ell_(alpha,b) conjugate(ell_(alpha,c)) is positive semidefinite;
trace preservation sets its diagonal to one. The Schur/correlation-matrix form
is standard channel machinery [2], here obtained for this exact instrument.

**Sufficiency.** Factor C into its positive eigenvector Gram representation and
form those block-scalar Kraus operators. They are trace preserving, and
K_b F_c=delta_bc K_b gives J_b Phi_C=J_b. Equal branch maps also preserve
correlations with an arbitrary spectator reference. No finite numerical sweep
is offered as a substitute for this all-channel proof.

The same argument applies to the fixed two-event batches used below, whose
four input effects are nonzero orthogonal joint projectors. It does not assert
this formula for arbitrary unsharp, multikraus or altered-output instruments.

## 2. A binary event leaves a complex disk of freedom

For two outcomes,

    C = [[1,c],[conjugate(c),1]],  |c| <= 1,
    Phi_c(X) = F_0 X F_0 + F_1 X F_1
               + c F_0 X F_1 + conjugate(c) F_1 X F_0.

Identity is c=1; full pinching is c=0; |c|=1 is a reversible relative-phase
unitary. The intermediate disk contains partially dephasing channels. Every
point preserves the same supplied event's entire output instrument exactly.
For equal-rank binary sectors, the normalized Choi eigenvalues that may be
nonzero are (1+|c|)/2 and (1-|c|)/2.

Take orthogonal states (x+y)/sqrt(2) and (x-y)/sqrt(2), with x,y in different
sectors. Their trace distance changes from 1 to |c|. For 0<|c|<1 the map is
linearly injective, but no all-input CPTP recovery can undo that contraction.
Coordinate inversion is not quantum-state recovery. At c=0 the distinct inputs
have identical outputs, so even linear injectivity is lost. Actually pinching
first and then applying any of these channels never restores the distinction.

The coefficient is an explicit diagnostic choice, not elapsed time, a physical
decay rate, an outcome probability, a fitted force or a selected response law.

## 3. Idempotence supplies a sharper conditional result

Channel composition gives Phi_c Phi_d = Phi_(cd). Therefore an idempotent binary
member must satisfy c^2=c. There are exactly two:

    identity (c=1), or full pinching (c=0).

**Full pinching is the unique nonidentity idempotent in this complete binary
family.** This sharpens why the earlier conditional expectation is special.
Idempotence is already a property of the supplied RAS conditional expectation;
we have not derived a new physical reason to demand it or for an event to occur.
Sufficiency alone leaves the disk. Nonidentity plus idempotence selects the map
only AFTER the binary instrument is specified. It selects no actual outcome.

## 4. Four-outcome batches retain partition freedom

For general C, composition is entrywise multiplication. Idempotence forces each
entry to be zero or one. A positive semidefinite unit-diagonal matrix is a Gram
matrix of unit vectors. An entry one means the corresponding vectors coincide,
so that relation is transitive. Hence idempotent members are precisely the
matrices of equivalence relations on the outcome labels.

For the supplied four-outcome batch there are 15 such partitions: one with one
group, seven with two groups, six with three groups, and one with four groups.
They include identity, complete pinching and thirteen partial pinchings. Only
four coincide with independently pinching neither, either or both binary bits;
eleven other groupings are possible under the batch-output requirement.

We enumerate all 64 symmetric zero/one candidates with unit diagonal, not just
the expected partitions. Exactly 15 are positive semidefinite. A further
three-label negative control has all pairwise moduli below one but a negative
full correlation eigenvalue: pairwise admissibility does not replace global
complete positivity.

These partitions preserve a COMPLETED two-event batch. They need not preserve
the intermediate single-event states as open alternatives. Keeping both ready
complete instruments exact still leaves only identity at every one of the seven
v15.22 two-ready contexts. The new family reproduces that restriction directly.
Once a retained algebra itself is specified, its trace-preserving expectation is
still unique; these different partitions specify different algebras.

## 5. Integrated computation and controls

The unchanged model supplies 36 ready event/context pairs. Testing 33 complex
disk samples gives 1,188 channels and 2,376 complete branch-map checks. The largest
normalized-input Choi discrepancy is approximately 1.96e-15. Seven two-ready
contexts times 33 samples give 231 open-alternative checks: only the seven
identity cases leave both complete instruments unchanged. The other-event
witness error follows |1-c|/2, not merely a function of |c|.

All 15 partition maps were tested at all seven batch contexts: 105 batch maps
and 420 branch checks, with maximum Choi discrepancy approximately 1.12e-15.

Five explicit coefficients were inserted before each corresponding event in
all 80 original supplied histories: 400 executions and 1,600 branch steps.
The largest normalized-state discrepancy is approximately 2.09e-15; joint-mass
error 1.89e-15; conditional-weight error 2.78e-15. These inputs remain supplied,
not selected by the new code. The preprocessing does not add an actual record.

A separate within-sector unitary preserves outcome probabilities yet changes
one branch's remaining state by trace distance 1. It lies outside the classified
family and is correctly detected. This guards against weakening the full-output
contract to a probability-only test.

## 6. Verification, provenance and limitations

The frozen v15.22 module has Git blob
`0d6f625cc398ce1cd3e2edeac93156ad7b6c5f8e`. Its three nested baseline files are
verified by their original hashes. Parent head:
`db166396caf9046c9e7ee13880fdd517fa00dda5`.

Local TDD recorded 26 intended absent-model failures and six absent-view failures.
A JSON-export regression exposed NumPy booleans in the inspector payload; they
were converted to native booleans without altering mathematics or tolerances.
The final 32 new tests passed locally. The GitHub workflow independently runs
those and the 374 selected inherited checks (406 total), then generates media,
checks decoding and verifies all uploaded asset sizes and SHA-256 digests. The
actual CI/release outcome is recorded on the PR; this text is not a pending-run
success assertion. No full-repository regression or formal proof checker is used.

Local Chromium checks covered all 81 views, 15 partition selectors, three
presets and widths 1280/820/390 with no JS errors, external requests or overflow.
An initial browser attempt timed out on a collapsed selector; the corrected
script opens that panel before exercising it. Native iPad/Safari was not tested.
The MP4 was visually inspected and fully decoded. Browser checks remain local,
not automatically repeated by numerical CI. Code and proof received self-review,
not independent scientific peer review. The source records a local verification summary; fresh CI logs are included
in the published bundle. It does not claim to archive every local debugging log.

Numerical identity tolerance is 1e-10. Correlation-matrix validation permits only
roundoff-size negative eigenvalues; the Kraus construction discards those tiny
negative parts and is independently compared with the direct map. No threshold
was tuned to force a desired scientific classification.

No actual outcome, physical pruning selector, entropy-production objective,
clock, carrier origin, source law, modified dynamics or gravity is derived.
Pre-time reversible change remains allowed. This classifies sufficient maps
relative to supplied instruments; it does not identify which physical instrument
or event becomes actual. No new fundamental axiom or novelty-priority claim is
made. Pillar 3 remains OPEN.

## Primary mathematical context

[1] Choi, Johnston and Kribs, The multiplicative domain in quantum error
correction, arXiv:0811.0947. https://arxiv.org/abs/0811.0947

[2] Harris, Levene, Paulsen, Plosker and Rahaman, Schur multipliers and mixed
unitary maps, arXiv:1807.06491. https://arxiv.org/abs/1807.06491

These support the standard mathematical machinery, not the physical ontology.
