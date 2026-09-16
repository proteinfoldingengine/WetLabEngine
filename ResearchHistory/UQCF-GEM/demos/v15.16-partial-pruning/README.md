# v15.16 — Partial record pruning / recoverable-observable map

**Executed conditional simulation extension. No new physical law or axiom.**

The v15.15 dynamics and coherent encoding are unchanged. This extension inspects
all 16 ways to pinch selected record bits AFTER the same completed encoding,
then identifies the exact input observables that remain recoverable for every
input. Masks are supplied alternative reductions, not a chronological history.

## Run

```sh
python -m pip install -r requirements.txt
python -m unittest -v test_recoverability.py test_replay.py
python recoverability.py --out outputs
python replay.py --out outputs
# Optional MP4; FFmpeg must be separately available.
python replay.py --out outputs --video
```

`outputs/partial_pruning.html` is a self-contained browser inspector. Toggle
which of A1/A2/B1/B2 is pinched, select a pair of labels, and inspect real or
imaginary phase distinguishability. All witness values are computed in Python;
the browser replays embedded data with no external requests. Unticking a mask
compares a different scenario from the original encoding; it does not invert
information loss in an already reduced state. The optional 24-second MP4 is a
sequence of alternative inspection views, not a physical-time trajectory.

`verification.json` records the fresh checks. `replay_data.json` contains the
input basis and algebra maps. `encoding_and_basis.npz` retains the numerical
encoding, basis and input. `visual_data.json` adds the computed pair-witness
values. Generated outputs and local evidence accompany the portable ZIP, not the
Git-tracked source. This does not deploy a website or create release assets.

## What was derived within the supplied model

The earlier complete instrument ends in distinct one-dimensional record sectors:

    K_r = |r><b_r|,   sum_r K_r† K_r = I.

There are exactly 16 rank-one branches in a 16-dimensional system. Consequently
the rows <b_r| form a unitary matrix F: F†F=FF†=I. The program extracts F from the
frozen branch operators; it does not select or fit a new basis.

For a subset S of pinched record bits and each corresponding partial label s,

    P_s = sum_{r restricted to S = s} |b_r><b_r|.

These are mutually orthogonal projectors resolving I. For the unchanged
encoding V and record projector Q_s, the exact intertwining relation is

    Q_s V = V P_s.

Therefore the partially pinched joint channel satisfies, for every input,

    N_S(rho) = D_S(V rho V†) = V E_S(rho) V†,
    E_S(rho) = sum_s P_s rho P_s.

Numerical verification checks the operator intertwining rather than relying on
one fixture as proof of this all-input statement. On these output states the
inverse encoding recovers E_S(rho), not generally rho. Compression V†(.)V can be
extended to a trace-preserving decoder by mapping its orthogonal complement to
any fixed state; that extension is immaterial on this channel's range.

### Exact surviving observable algebra

The complete input observable algebra recoverable for EVERY input state is

    A_S = {A : E_S(A)=A} = direct_sum_s P_s M_16 P_s.

Sufficiency: for A in A_S, use the output observable VAV†; its expectation equals
Tr(rho A). Necessity: the channel adjoint has range
E_S(V† M V) contained in A_S, so no output observable can reproduce the
expectations of an input observable outside A_S on all inputs. This is an
all-input observable statement; it is not a claim that every distinction of a
known single state is lost or that a common inverse exists on the full state set.

If k of the four record bits are pinched, there are 2^k blocks of size 2^(4-k):

    A_S ≅ direct_sum_{1..2^k} M_{2^(4-k)}.

Its real Hermitian dimension (including the identity) is 256 / 2^k:

| Pinched bits | Quantum blocks | Observable dimension | Surviving phase pairs |
|---|---|---:|---:|
| 0 | M16 | 256 | 120 |
| 1 | 2 × M8 | 128 | 56 |
| 2 | 4 × M4 | 64 | 24 |
| 3 | 8 × M2 | 32 | 8 |
| 4 | 16 × M1 | 16 | 0 |

These are dimensions of mathematical operator spaces, NOT entropy, clock ticks,
physical qubit counts, information in bits, or a selector of actual records.
The center has dimension 2^k; coherent noncommuting observables survive within
blocks until the complete pinching leaves an abelian algebra.

For different S and T, E_S E_T = E_(S union T). The resulting set-inclusion
structure compares retained observable algebras without assigning durations.
Equal-size subsets have the same dimensions but generally different algebras.
For example, the plus/minus phase distinction between input-basis labels 0000
and 1000 is erased by A1 pinching and preserved by B2 pinching. Both operations
leave dimension 128. A scalar dimension count alone does not specify lost content.
All complete record-label probabilities remain unchanged under these reductions.

## Execution and boundaries

The tests cover all five schedules × 16 masks (80 cases), all 120 unordered label
pairs × real/imaginary phases × 16 masks (3,840 phase-witness cases), and all
256 ordered mask compositions. The phase-pair tests use distinguishable input
states rather than a failed attempt at one chosen inverse. Maximum errors are
recorded in `docs/RESULTS.json` and freshly regenerated outputs; identities are
checked against 1e-11 absolute tolerance, not exact decimal reproduction.

A deliberately unsharp two-outcome instrument is a rejected generalization
control. Its compressed effects are not projectors and the intertwining fails
(norm about 0.566); the naive output reconstruction differs by about 0.466.
The sharp-projector classification is therefore not asserted for arbitrary
quantum instruments. This negative control changes no accepted dynamics.

This uses standard operator-algebra/conditional-expectation mathematics. A
primary reference for observable-based quantum error correction is Bény, Kempf,
and Kribs, *Quantum Error Correction of Observables* (2007),
https://arxiv.org/abs/0705.1574. The explicit derivation above suffices for this
special sharp-instrument case; the reference is not validation of the physical
ontology and no new general theorem is claimed.

## Ontology

Pre-time reversible change remains allowed. Pinching is an explicit supplied
retained-description choice, not an entropy objective or clock. RAS and RCR
remain separate; no actual record is selected here. This comparison supplies no
physical first-collapse selector, unconditional physical entropy-production law,
quantum-carrier origin, gravitational source law, duration or Einstein equations.
It does not prove destruction of information across all possible coherent
extensions. No new fundamental physical axiom is adopted. Pillar 3 remains OPEN.

## Preservation and evidence coverage

The exact v15.15 core and its nested dependencies are copied unchanged from head
`df065383733f6e3a2e480abcb70326c34e6abc65`; their Git blob IDs are checked by the
model. The main core remains `fdf5367b11729fc1e2bfccd8d8daa2a0c7209049`.
Earlier repository files are not rewritten.

Local TDD evidence records 26 intended absent-model assertion failures and seven
absent-presentation failures before their implementations. All 33 new tests
passed. Selected prior regressions are rerun separately and recorded in the
portable bundle. Local rendering uses Python 3.13.5 / NumPy 2.3.5; FFmpeg renders
H.264. The 24-second movie is fully decoded and visually inspected, including a
corrected annotation overlap. Chromium checks cover all masks, real/imaginary
witnesses, presets, no external requests/JS errors, and 1280/820/390px widths.
Native iPad/Safari attachment behavior is not tested. The GitHub PR separately
records actual exact-head CI status; pending is not success. Neither tests nor
hashes constitute independent scientific peer review or empirical validation.
