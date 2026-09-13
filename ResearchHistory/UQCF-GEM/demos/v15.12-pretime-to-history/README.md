# v15.12 — Integrated pre-time-to-history demonstrator

**Executed conditional model. This is a demonstration, not a new physical closure gate.**

One computed run connects reversible pre-time relational motion, supplied retained-algebra selection (RAS), supplied actual records (RCR), later reversible changes preserving those records, and a compatible ordinal history.

## Run

From this directory:

```sh
python -m pip install -r requirements.txt
python -m unittest -v test_simulation.py test_presentation.py
python simulation.py --records 101 --out outputs
python render.py --out outputs
# Optional movie; FFmpeg must be installed and on PATH.
python render.py --out outputs --video
```

The default generates 740 display samples. At 20 playback frames/second, the movie is 37 seconds. That duration belongs to the media player, not the model's physical interpretation.

`outputs/interactive_demo.html` is a standalone browser replay with all eight explicitly supplied three-bit histories, stage navigation, play/pause and scrubbing. No external requests are made. `states.npz` contains every default-branch density matrix; JSON files contain the event ledger and all-branch summaries. The conversation's portable bundle includes the rendered MP4, HTML, full earlier Library reports and local verification logs. Generated media is not checked into this source folder.

Some attachment viewers do not execute HTML scripts; use a full browser for the interactive file. Native iPad/Safari attachment behavior was not tested. The delivered MP4 is the direct viewing path.

## Interpretation

The initial coherent state changes under a declared reversible unitary, returns along its inverse, and approaches a declared event. No actual record is selected in that region. RAS and RCR are then shown separately so their distinct roles can be inspected. These are not elapsed physical substeps. The later reversible transformations preserve earlier records exactly.

For the supplied `101` sequence the retained record-sector ranks are `8 -> 4 -> 2 -> 1`. Its middle outcome has conditional weight about 8.19%, illustrating that neither largest weight nor random sampling is being used to select actuality. Another record sequence must be supplied explicitly.

The cube is an illustrative layout of computational configurations, not physical space. Node area represents basis probability and link width/opacity represents coherence magnitude. Scrubbing backward replays stored states; it is not a physical recovery operation. Changing display cadence does not change event states, actual records or conditional weights.

## Scope and ontology

The carrier, illustrative motion generators, RAS choices and actual records remain supplied inputs. RAS/RCR retain their earlier conditional status. No first-collapse selector, physical entropy functional, calibrated duration, global simultaneity, gravitational law or Einstein correspondence is derived. No downstream score changes upstream rules. Pillar 3 remains OPEN.

Each event includes a phase-distinguishability witness that becomes identical after the specified conditional expectation, including when its classical record flag is retained. This certifies loss on that retained description, not global information destruction across all coherent extensions.

## Provenance and verification

The vendored v15.11 module is byte-identical to Git blob `8871e50f19322adbb62f34ea3837ba8e6cb16c8b` from exact head `f35c122977c4f35447a674a0c0b0b1ff8f2683ac`. Its companion tests and excerpt manifest are also preserved. Run the prior checks from `vendor` with `python -m unittest -v test_continuity.py`.

There are 24 model-integration tests and 6 presentation/export tests, plus 20 preserved v15.11 tests. Local RED logs record 24 missing-integration assertions and six missing-presentation assertions before their respective implementation. Local GREEN passed all 30 new tests and all 20 preserved tests. Browser checks covered play/pause, phase jumps, all eight supplied final records, scrubbing, no external requests, and desktop/tablet/mobile viewport overflow. The movie was rendered and inspected locally. These are not exhaustive repository-wide regressions, formal proofs, independent peer review or empirical validation.

The installed local build used Python 3.13.5, NumPy 2.3.5 and Matplotlib 3.10.8. The exact-head CI workflow verifies the same numerical and export tests with Python 3.11 / NumPy 2.4.6. See the draft PR for its actual conclusion; a queued run is not success.
