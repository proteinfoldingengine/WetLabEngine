# v15.80 results — physical tangent extensions under signed source linearity

Verdict: **SIGNED_CPTP_TANGENTS_HAMILTONIAN_ONLY_CONFIRMED**.
Separate gate: **SIGNED_CPTP_RETAINED_IMAGE_FOUR_CONFIRMED**.
All frozen validity checks passed. Three tests passed in the certified run.
No scientific threshold or amplitude changed. No CI implementation repair
was needed. Before measurement, independent review corrected the dissipative
control's edge coverage and extended the implementation's Gram check to all
117 tensors; both were settled before the tested implementation commit.

## Earned result

For a single source tensor with fixed, state-independent coefficients,
real-linearity in the source and CPTP tangency through identity for both
source signs imply Hamiltonian first-order response. This is an extra
hypothesis, not a universal requirement on all physical source mechanisms.
The curves need not be finite inverses; higher-order dissipation remains
possible. Source strength labels ordered updates, not fundamental time.

The test included every covariant full-operator extension before applying
complete positivity. It did not assume that unobserved sectors were zero.
The classification was:

| Stage | Coefficient dimension |
|---|---:|
| Full covariant bilinear source/operator maps | 117 |
| Trace-annihilating maps | 110 |
| Kernel of both-sign conditional-Choi constraints | 7 |
| Image in the 18 retained/hidden couplings | 4 |

The conditional-Choi constraint rank was 103 at all three frozen relative
thresholds. Each source-support block had exactly one kernel direction;
its projector agreed with the canonical Hamiltonian direction within
1.251e-15. Support blocks of sizes 11,17,26 had smallest nonzero constraint
singular values approximately 0.637719,0.971678,1.405673, respectively;
null singular values were at most 2.820e-15. This was not a threshold-edge
classification.

The seven free parameters are one Hamiltonian strength per nonempty source
support. Three local-support parameters have no retained hidden response.
The three two-site supports each tie two one-cross coefficients together;
the three-site support ties three one-body-output coefficients together.
Thus the physically extendable retained image has four dimensions, rather
than nine independently adjustable one-cross coefficients. Its projector
matched the expected four-pattern subspace within 8.949e-16.

On the 12-state ensemble, both 183708-by-7 Q/E maps had coefficient rank
four at all frozen thresholds. Their kernel projectors exactly selected the
three local-source coordinates at reported precision. Nonzero singular
values were:

- Q: 117.5755,117.5755,117.5755,12.40984.
- E: 593.3821,592.2047,578.6348,61.56435.

Each individual frozen state also had coefficient rank four as a diagnostic.
These are ranks over all source/hidden experiments, not a four-dimensional
edge geometry. Nonzero strengths are not selected: all-zero and purely
local Hamiltonian assignments remain admissible.

## Physical dissipative control and intentional reverse-strength NO

The fixed Hermitian source a=(ZII+XXI)/sqrt(2) generated the physical
quadratic response D_a(z)=a z a-z. It is even in source sign, D_{-a}=D_a,
so it lies outside the source-linear class above. Its conditional Choi
matrix had one eigenvalue 8 and all other eigenvalues at roundoff. The
negative generator had minimum conditional eigenvalue -8.

The exact epsilon=.1 channel passed CP/TP checks. Reversing source strength
produced a Choi minimum eigenvalue -0.8856110326406789: an intentional
non-CP control result, preserved as NO. Replacing a by -a leaves the positive
channel unchanged; source sign and source strength must not be conflated.

This physical dissipator had retained hidden rank 12 and Q/E rank six on
all 12 states. Each of edges (1,2) and (2,0) contributed rank three; edge
(0,1) was null. Both frozen retained witnesses passed: YYZ/sqrt(8) produced
-IZZ/sqrt(8), and XXX/sqrt(8) produced ZIX/sqrt(8), with maximum residual
1.242e-16. Therefore the signed-linear conclusion does not rule out
physical dissipative rotational response with nonlinear source dependence.

## Validation and interpretation limits

All 126 signed unitary controls passed CP/TP checks. Their minimum Choi
eigenvalue was -3.126e-15, within the frozen -1e-12 numerical tolerance;
unitarity residual was at most 7.367e-18. The positive dissipative control's
minimum Choi eigenvalue was -1.421e-15, also within that tolerance. These
rank-deficient Choi roundoff values are not scientific CP failures.

The full 117-tensor Gram residual was 1.567e-13 (frozen limit1e-10).
Complex-safe PTM reshuffling agreed with the independent matrix-unit Choi
builder within 3.265e-16 for the classified basis and 1.487e-15 for the
control. Hamiltonian reconstruction error was 1.111e-16; retained projection
and hidden-response reconstruction errors were zero at reported precision.
Maximum Sylvester residual was 1.466e-14. No finite Euler map was mistaken
for a physical unitary update, and no geometry was evaluated at a singular
output state.

The Hamiltonian tangent-cone statement uses standard quantum-channel
structure, not a new fundamental-law theorem; DERIVATION.md gives the
finite-dimensional proof and identifies the standard generator reference.
The research-specific result is the full-extension classification and its
four-dimensional image in the previously certified 18-coupling space.
These assumptions do not derive a physical source law, select strengths,
establish restriction/composition naturality, or change admissible worlds.
Earlier calibrated null constructions and all historical verdicts stand.
Genesis Pin, ordered recoverability and geometry as retained exhaust remain
unchanged. No fundamental time, dark-matter primitive, or gravity derivation
is introduced.

## Exact certification evidence

- Certified parent: `659c078f47f1b6732c310701bd3fd4170787fc43`.
- Preregistration/tests with implementation absent: `88391086920a2552543a83f74638de89a418dc9f`.
- Tested scientific implementation: `da49aac271d0fad616e5377afe084b395f272d64`.
- RED [run 36345736689](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36345736689), job `108694387719`, artifact `10940114612`.
- RED artifact SHA-256: `c84afde9aea963e7e462eac2e8576904bb64b90b93e3ab7b2a17019e3929660c`.
- GREEN [run 36346054065](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36346054065), job `108695296313`, artifact `10940995393`.
- GREEN artifact SHA-256: `3a22af29b731dbdba3d378cf765deb7d419391ab3b2f3e3a52e5f9d1f0f2042a`.
- Full result JSON SHA-256: `1fca81240f84a3d0066e6ce6899f96eefbddf8e30ae67144880a82161dedc8b9`.
- Lossless `RESULT.json.gz` SHA-256: `22933693e019f659d532869a3cff3a72cafbf27bd49e918d9033c662e5e65859`.
- Compressed-result Git blob: `bd9406dbcb7c2e0f303e26ae8854773653d306d7` (54,721 bytes).

Both exact job logs were inspected. RED setup passed and failed specifically
at the absent-implementation assertion, with zero tests executed. GREEN
passed all three tests and reported the two scientific verdicts. Both
artifacts were downloaded and their hashes checked; execution SHAs, frozen
source bytes and the GREEN SHA256SUMS were verified. The artifact JSON was
read independently of CI status, including the intentional negative control.

Full numerical diagnostics, source labels, coefficient-kernel projectors,
Choi spectra and geometry spectra are archived losslessly beyond Actions
retention. SUMMARY.json is a derived convenience. TEST_LOG.txt and
SHA256SUMS came from the GREEN artifact. The final additive publication does
not change the tested scientific code. No merge to main was performed.

## Reproduce and next question

Use Python3.11 and numpy==2.3.5. From this folder at the tested commit:

```sh
OPENBLAS_NUM_THREADS=1 python -m unittest -v test_gate
OPENBLAS_NUM_THREADS=1 python gate.py > result.json
```

At the additive documentation head, the archived result can be recovered by:

```sh
gzip -dc RESULT.json.gz > certified-result.json
sha256sum certified-result.json
```

The physical quadratic control supplies a concrete next mechanistic question:
is its hidden rotational response carried by cross terms between its two
source components, compared with an incoherent mixture of their individual
jump channels at the same component weights? That matched comparison has
not been measured here. It would test a physical source-coherence mechanism
without introducing a fitted geometric target or requiring signed linearity
as a universal axiom.
