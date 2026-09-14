# v15.18 — Minimal invariant observable-algebra completion

**Executed conditional simulation extension. Not a new physical pruning law.**

**Delivery status:** locally verified; GitHub implementation upload was blocked by
the connected write tool with an indeterminate safety status. No v15.18 branch, PR
or CI run was created. The prior v15.17 branch is unchanged.

v15.17 classified fixed-algebra descent for 96 supplied motion/mask pairs. This
extension finds the smallest larger observable algebra that contains each
starting retained algebra and is invariant under the same unitary motions and
their inverses. The existing matrices are not changed. An enlargement describes
information that would have to remain available BEFORE pruning. It does not
reconstruct information from an already pruned state.

## Run

```sh
python -m pip install -r requirements.txt
python -m unittest -v test_completion.py test_replay.py
python completion.py --out outputs
python replay.py --out outputs
# Optional MP4; FFmpeg must also be installed.
python replay.py --out outputs --video
```

The offline `outputs/algebra_completion.html` compares original and completed
operator-space masks for 112 cases: six separate motions and their joint family,
each with sixteen original masks. `verification.json` contains full partition
histories, merge witnesses, support gaps, closure residuals and classifications.
The optional movie is a 24-second H.264 comparison, not a physical-time trajectory.
Generated outputs and actual local logs are in the conversation ZIP, not checked
into the source directory. No live website or GitHub release is deployed.

## Precisely which minimum?

For original algebra A and supplied unitary family G, define

    B_min = alg*( U_w† A U_w : w is a finite word in G and G† ).

This is the smallest unital *-algebra containing A and invariant under the
supplied conjugations. It is not the smallest arbitrary sufficient statistic,
smallest linear operator module, or a physical law selecting the retained world.
The words label finite compositions, not elapsed time or an actual event schedule.
Including both B2 controller alternatives in G does not make both records actual.

### Exact finite proof and algorithm

Use the input basis F already derived by v15.16. Each starting A is a direct sum
of full matrix blocks and contains every diagonal matrix unit E_ii. Any unital
*-algebra B containing A also contains all E_ii. If T in B has a nonzero entry
T_ij, then E_ii T E_jj = T_ij E_ij implies E_ij in B. Adjoint closure and products
of matrix units make allowed pairs an equivalence relation. Thus every candidate
B is a coarsening of the original partition into larger full blocks.

For a current block g, U† E_ab U, a,b in g, has entries linking the union of the
column supports of rows in g. All matrix units on that union must be present.
Merge these labels for every U and U†, then repeat on the larger blocks until
stable. Every merge is forced in every invariant containing algebra; induction
therefore establishes minimality. At stability, conjugation sends each block
algebra into the completed algebra; inclusion in both directions gives invariance.
There can be at most d-1 strict block-merging rounds on d labels.

The computation checks closure independently using central-projector permutation
and the full superoperator's discarded-to-retained block. Tests also enumerate
all 15 partitions on four labels and compare the computed result against EVERY
invariant containing candidate in 45 small control problems.

### Numerical scope

The support gap is fixed in advance: magnitude <=1e-12 is treated as numerical
zero, >=1e-9 as resolved nonzero, and anything between raises AmbiguousSupport.
No threshold was fitted to the outcomes. The largest discarded entry in the
112 cases is about 1.24e-15; the smallest resolved entry is about 7.73e-4.
Independent all-operator closure residuals stay below 1e-10; the largest measured
residual is 3.13e-14. Exact minimality applies to the resolved support pattern;
this is not a symbolic proof that every subthreshold floating-point entry is zero.

## Results

Among the previous 96 single-motion cases, 17 remain unchanged. Of the 79 earlier
failures, 41 need a strict but partial enlargement, and 38 require the full M16
algebra. Examples starting from the fully pinched, 16-dimensional abelian algebra:

| Supplied motion | Minimum invariant algebra | Hermitian dimension |
|---|---|---:|
| B1 | M4 + M4 + M4 + M4 | 64 |
| A1 | M8 + M8 | 128 |
| Existing pre-time motion | M16 | 256 |

The all-six requirement reaches M16 for every nontrivial original mask. In fact,
the single existing pre-time motion already forces this result. A direct witness
independent of iterative support closure uses row 13 of F U F†. Its smallest
amplitude is 0.0031552850321. The conjugated rank-one projector Q therefore has
ALL entries nonzero, with minimum magnitude about 9.96e-6. Since

    E_ii Q E_jj / Q_ij = E_ij,

all 256 matrix units are generated. The numerical reconstruction error is about
1.12e-16. The mathematical implication is exact when those entries are nonzero;
no inference from a pattern of tiny zeros is needed for this full-algebra witness.

This is specific to the supplied motions and the requirement to preserve the
entire original observable algebra. It is not a universal no-go for reduced
physics, approximate descriptions, transported algebras, or actually-pruned
processes with their own subsequent dynamics.

## Two important limits

**Not information recovery.** A phase-pair control remains indistinguishable when
an already-pruned output is inspected in the larger algebra (distance about
1.61e-15). Keeping the completed algebra before pruning preserves that distinction
(distance approximately 1). Those are different input-retention choices.

**Not automatically record-preserving.** When original full blocks are merged,
the old central record projections remain observables but cease to be central
in the larger algebra. Thus enlargement is not a physical repair preserving all
old classical record identities. The output records this loss of central status.

**Not minimum linear size.** For a qubit, the conjugation orbit of Z under a
suitable Y-axis rotation lies in span{I,X,Z}, dimension three. Multiplication
requires Y as well, giving M2, dimension four. This demonstrates why minimum
invariant algebra and minimum invariant linear prediction space are different.
The current computation does not derive the geometry-aware GOSM module discussed
in the earlier v12.47 Schur-Weyl report, or decide that separate frontier.

## Ontology and provenance

No new fundamental physical axiom, motion law, source coupling, quantum-carrier
identification, entropy objective, calibrated clock or actual-outcome rule is
introduced. Pre-time change remains reversible. RAS and RCR remain explicit,
separate physical inputs of earlier conditional constructions. No actual record
is selected here. Pillar 3 remains OPEN; no scientific breakthrough is claimed.

This uses standard finite operator-algebra reasoning, with an explicit proof of
the special partition algorithm above. For broader observable-based quantum
information context, see Bény, Kempf and Kribs, *Quantum Error Correction of
Observables* (2007), https://arxiv.org/abs/0705.1574. That reference does not
validate this program's physical interpretation or prove this numerical result.

The v15.17 module is preserved as Git blob
`e3e8ac11cd5a856c66763faa071957fd9a220b42`, from exact head
`a01f1ff5f1045bc701a97bfef44eab58cfc5b401`. All nested baseline hashes are checked.
Earlier repository files remain unchanged. Publication is intended as an additive stacked
draft branch, not a merge to main; it has not completed in this delivery.

## Verification coverage

Local TDD evidence includes 26 intended absent-model failures and six intended
absent-replay failures before implementation, followed by targeted failing tests
for the direct full-algebra certificate and central-record boundary. All 34 new
tests and 202 selected prior tests passed: 236 checks. An initial baseline command
was run from the wrong working directory; it was rerun correctly and is not
counted as a scientific or TDD result. No assertion of repository-wide coverage,
formal proof checking, or independent scientific review is made. Code and proof
received an inline self-review only.

Chromium/Playwright checks cover all 112 case selectors, three presets, no external
requests or JavaScript errors, and no horizontal overflow at widths 1280/820/390.
The MP4 was rendered, visually inspected and fully decoded locally. Native
Safari/iPad attachment behavior was not tested. Local Python 3.13.5, NumPy 2.3.5,
Matplotlib 3.10.8 were used. Exact-head CI is recorded separately on the PR; it
runs selected tests and exports, not video rendering or browser verification.
