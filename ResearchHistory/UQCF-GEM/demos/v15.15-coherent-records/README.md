# v15.15 — Coherent records / retained-description comparison

**Executed conditional simulator; not a new collapse, entropy or time law.**

The same v15.14 instruments now have an explicit reversible implementation on
four system qubits plus four diagnostic quantum record registers. Compare the
coherent encoding with declared record pinching and with the earlier selective
outcome branches. Earlier source files and assumptions are unchanged.

## Run

```sh
python -m pip install -r requirements.txt
python -m unittest -v test_coherent.py test_replay.py
python coherent_records.py --out outputs
python replay.py --out outputs
# Optional MP4; FFmpeg must also be installed.
python replay.py --out outputs --video
```

`outputs/coherent_records.html` is the offline replay: five schedules, five
checkpoints, and an inverse-control view. It shows norms of the JOINT system–record
blocks, not the reduced memory matrix. Record probabilities agree on both sides.
No outcome is sampled, selected by maximum weight, or declared actual here.
`quantum_encoding.npz` contains all default-schedule isometries, its full unitary,
and the system input. JSON files contain visual data and verification results.
The optional H.264 movie is 24 seconds at 1280x720. Playback duration is a media
property, not an output called physical time. Generated media is delivered in the
portable bundle; it is not committed to the repository or deployed as a website.

## Construction and exact mathematical reason

Let r label the four record bits in order A1,A2,B1,B2. Registers begin in a supplied
blank state. Each event applies the prior system operation and coherently writes
its computational label into a fresh register using controlled-NOT. This writes
basis labels, not arbitrary cloned quantum states. For B2, both A1-dependent
operations coexist in a block-controlled quantum unitary; no classical A1 value
is selected. All five existing write/read-compatible schedules remain supplied.

If V is the resulting isometry from system input into system plus registers, its
record blocks are exactly the earlier adaptive history Kraus operators:

    V = sum_r |r>_R tensor K_r.
    V rho V^dagger = sum_(r,s) |r><s|_R tensor K_r rho K_s^dagger.

Pinching the record register removes only r != s blocks:

    D_R(V rho V^dagger) = sum_r |r><r|_R tensor K_r rho K_r^dagger.

Thus every labeled branch probability and conditional system output matches the
prior instrument, for any input. This exact statement follows by induction over
the supplied copy/control gates. Numerical checks compare the branch operators
and normalized-input Choi blocks, rather than claiming finitely many sampled
states prove an all-input theorem. All 80 final branch
operator comparisons were zero at machine representation in the local run;
across schedules and other routes there is ordinary roundoff.

Eventwise record pinching and deferred final pinching also agree here. This is
known deferred-measurement machinery applied to this concrete simulation:
Yuri Gurevich and Andreas Blass (2021), *Quantum circuits with classical channels
and the principle of deferred measurements*, https://arxiv.org/abs/2107.08324.
The reference supports the mathematical context, not the project's ontology.

## What the execution found

All five schedules and sixteen labels were compared: **80 final branch maps**,
plus **155 prefix branch maps** across those executions. Eight distinct completed
event sets recur. Local maximum prior-state trace distance is about 5.55e-17 and
joint-weight difference 1.11e-16. The coherent encoding is an isometry to 1.25e-14.

The full coherent inverse restores the original joint state with Frobenius error
5.73e-15. Applying that SAME inverse after pinching leaves trace distance 0.776821
from the original. A failed chosen inverse alone would not prove irrecoverability:
the stronger control supplies two orthogonal inputs with trace distance 1 that
remain distinguishable after coherent encoding but become indistinguishable
(distance about 3.79e-16) after pinching. Their identical retained outputs preclude
one recovery map that restores both. No assertion about every possible enlarged
physical environment follows from that scoped result.

At the final coherent checkpoint the memory marginal is already diagonal, yet
joint off-diagonal record blocks have Frobenius norm 0.831075. Diagonal local
records are therefore not, by themselves, evidence of globally lost coherence.
The viewer deliberately plots joint blocks to avoid making that mistake.

A sector-phase control preserves the entire labeled classical instrument while
changing the coherent state. The dilation is not uniquely identified by classical
records. A swapped-controller negative control instead changes the labeled Choi
blocks (maximum distance about 0.08238) and is detected. Neither control is a
newly adopted physical interaction or source law.

## Ontology and interpretation

The comparison separates three objects:

1. reversible correlations with quantum registers;
2. classical alternatives after an explicitly supplied retained-description map;
3. one actual record (RCR), which is NOT selected by either of the preceding steps.

RAS/RCR keep their earlier conditional status. The added quantum registers and
pinching map are supplied diagnostic model structure, not accepted fundamental
physical axioms or a hidden-environment claim. Existing local dependencies are
not derived from nothing. An observable record pattern, even with matching full
outcome probabilities, does not by itself establish objective collapse.

No entropy functional selects the input, gate, record or schedule. Physical
entropy production, onset of objective collapse, duration, gravity and Einstein
correspondence remain unresolved. Pre-time reversible motion remains allowed.
Pillar 3 remains OPEN; no scientific breakthrough is claimed. This extension
strengthens what the integrated simulator can distinguish, not what nature has
been demonstrated to do.

## Verification coverage

Local TDD evidence records 24 missing-model assertions before implementation and
six missing-replay assertions before implementation. A count-label regression was
also reproduced and corrected before the final run. All 30 new tests and all
107 selected v15.11–v15.14 regressions passed locally. This is not the entire
repository test suite or independent scientific peer review.

The prior adaptive module and its dependency are hash-checked unchanged against
Git blobs `44a87e4cc5bcf531ef7798aadab5d9dbba3482cb` and
`95d0303d617422d74e61ae017f0354233ec9454b`. Base head:
`ef2c63ff620222499ae35452fa5a6fcd546c8b59`.

Browser checks used system Chromium via Playwright with `page.set_content`:
25 schedule/checkpoint views, inverse/back/reset controls, no external requests
or JavaScript errors, no horizontal overflow at widths 1280/820/390. Native
Safari/iPad attachment behavior was not tested. The MP4 was rendered, visually
inspected and fully decoded locally. Local Python 3.13.5, NumPy 2.3.5 and
Matplotlib 3.10.8 were used. Exact-head CI checks numerical tests, earlier
regressions, compilation and export; browser/video checks remain local. Consult
the draft PR for the actual CI result; queued or pending is not success.

`docs/RESULTS.json` is a measured local snapshot; executable tests enforce the
scientific tolerances independently. Full local evidence and generated outputs
are included in the portable bundle. The original research branches are preserved
and no merge is performed by this extension.
