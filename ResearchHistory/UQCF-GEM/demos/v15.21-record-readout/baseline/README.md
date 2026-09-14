# v15.20 — Physical predictor and explicit readout cost

**Executable conditional simulation. No new physical collapse or pruning law.**

A valid four-qubit channel can remove the unused parity coordinate of v15.19's 255-direction predictor. It halves the visible signals. Explicit ensemble readout scaling restores their expectations, with an exposed sampling-variance cost—not quantum-state recovery or a smaller carrier.

## Run

```sh
python -m pip install -r requirements.txt
python -m unittest -v test_channel.py test_replay.py
python physical_predictor.py --out outputs
python replay.py --out outputs
# Optional MP4: FFmpeg must be installed separately.
python replay.py --out outputs --video
```

Open `outputs/physical_predictor.html` in a full browser. Presets compare identity, the invalid raw coordinate projection, a valid parity-erasing channel, and extra signal attenuation. All 441 grid points come from Python. The page makes no external requests. Native iPad/Safari attachment handling was not tested; the delivered MP4 provides a direct viewing alternative.

The map is a declared diagnostic comparison, not a selected physical RAS operation. It is not idempotent. No RCR is chosen, no fundamental time or entropy objective is used, and original motion operators remain unchanged.

## Files

`physical_predictor.py` contains the channel, independent Choi/Kraus checks, original-motion integration, direct-readout rigidity controls, and the minimax Pauli-readout certificate. `replay.py` exports an offline inspector and optional 24-second H.264 movie. `viewer.html` is the template; the finished data-filled page is in `outputs/`.

`test_channel.py` has 32 mathematical/model/scope tests; `test_replay.py` has six export/display tests. `docs/REPORT.md` contains the exact proofs, construction, numerical coverage, limitations and primary references. `docs/PLAN.md` records the continuation scope.

`baseline/` preserves the earlier model and nested dependencies; `BASELINE_SHA256.json` verifies them. `outputs/verification.json` records the actual local result. `outputs/channel_witnesses.npz` contains Γ, the 129 Kraus operators, Choi matrices and example states. `evidence/` contains local RED/GREEN logs, selected prior regressions, browser checks and video decoding evidence. `MANIFEST_SHA256.json` binds this delivered package, not any remote repository state.

**Verification:** 38 new tests plus 272 selected prior checks passed locally, 310 total. The earlier suites were run from their separately mounted archives; their logs and archive hashes are included, not all earlier test packages. No full-repository test run, independent scientific review or empirical validation is claimed.

**Publication:** local delivery only. No GitHub write or CI run was attempted in this continuation. It does not bypass or resolve the preceding v15.18/v15.19 publication blocks. No remote branch, merge, website or release is claimed.

Pillar 3 remains OPEN. Physical collapse, entropy production, duration, carrier origin and gravity remain unresolved.
