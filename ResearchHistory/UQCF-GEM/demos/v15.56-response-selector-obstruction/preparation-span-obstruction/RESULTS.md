# v15.92 — preparation-span obstruction

Both frozen scientific gates passed:

- **PREPARATION_SPAN_GEOMETRY_OBSTRUCTION_CONFIRMED**
- **NONCOMMUTING_PREPARATIONS_INSUFFICIENT_CONFIRMED**

`all_valid=true`: 45 exact checks, 144 state/source/arm cases, 432 retained edges, three passing tests. No implementation repair or preregistered threshold change was required.

## What was learned

For independent affine local qubit maps, connected correlations obey exactly

\[
C'_{ij}=T_i C_{ij}T_j^T.
\]

The translation terms cancel, including in the nonunital point control. A fixed local preparation family bounds correlation rank by its Bloch affine-span dimension. Full three-dimensional preparation span is therefore necessary for full-rank retained correlations and the **currently prescribed nonsingular three-axis polar readout**. It is not sufficient for a nonzero source response.

All four channels have explicit product measure-and-prepare realizations. Their outputs are fully separable; the whole output channel also breaks entanglement with external references. Source-dependent effective measurement effects need not be local.

| Preparation family | Affine dimension | Observed rank on every edge | Regular-domain cases |
|---|---:|---:|---:|
| Isotropic | 3 | 3 | 36/36 |
| Plane | 2 | 2 | 0/36 |
| Line | 1 | 1 | 0/36 |
| Point, nonunital | 0 | 0 | 0/36 |

Ranks agree at all three frozen thresholds. Isotropic and planar preparations are both noncommuting (exact maximum squared commutator Frobenius norm 1/2). Noncommutation alone thus does not ensure full-rank correlations. The isotropic control reproduces v15.91: 24 coherent cases have mixed response rank six, while 12 incoherent cases have rank zero. All 108 singular cases retain canonical support data; their full regular O/Q/E fields are null, **not measured rotational rank zero**.

## Interpretation clarification after review

The frozen DERIVATION statement that the previously used regular Sylvester tangent is “unavailable” at singular correlations means **outside this gate's frozen nonsingular domain**, not algebraically impossible. At rank two, P has eigenvalues p1,p2>0,0 and the skew Sylvester operator still has positive denominators p1+p2,p1,p2. A proper-orientation convention can select an SO(3) completion, although the full O(3) polar extension is nonunique. Consequently this experiment does not rule out full SO(3) orientation, rotational derivatives, or support-based geometry at rank two. Its null regular fields implement the preregistered domain restriction. The verdict names must be read with that restriction.

This scope correction changes no frozen file, measurement, predicate, or historical verdict. A rank-two oriented readout would require a separately specified gate.

## Verification

Worst residuals: affine connected identity 1.6653345369377348e-16; independent center/tangent reconstruction 1.2490009034432798e-16; support projector/reconstruction 2.3074892175185616e-15; Sylvester 6.631170520942725e-17; archived full geometry match 2.319376436768335e-15. Minimum input eigenvalue 0.03831621266594478; minimum source/output eigenvalue 0.015624999999999946. Minimum composite Choi eigenvalue -1.4947813046755865e-16 and preparation eigenvalue -1.812752413218676e-16 are within the frozen -1e-12 numerical tolerance. No eigenvalue clipping or criterion adjustment was used.

The exact job logs and downloaded RED/GREEN artifacts were inspected. Artifact execution heads, frozen source bytes and every SHA256SUMS entry were verified. GREEN log scientific JSON matches the artifact byte for byte after removal of log timestamps and an optional log-chunk BOM. SUMMARY.json is a derived convenience view; RESULT.json.gz losslessly preserves the full artifact result. SHA256SUMS retains the original artifact filename `result.json`.

## Immutable provenance

- Branch: `research/v15.92-preparation-span-obstruction`
- Certified parent: `eef0d852b2e696675d938244a8ef1ff5d648a24e`
- Preregistration/tests: `2632c2b73a8d7212762ea203248c0bd873cc0249`
- Tested implementation: `0586cc077c77abe8caad3a8411fbf6c4939e0260`
- [Expected RED run 36362494141](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36362494141), job `108742299600`, artifact `10945848148`. Setup passed; the explicit absent-implementation assertion was the expected failure.
- RED archive SHA-256: `1bd8c63687891f76f4487afa42ba3a6da5c2e5d235f22c2160cb3f7d130b215d`
- [GREEN run 36362753558](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36362753558), job `108743051837`, artifact `10946605591`.
- GREEN archive SHA-256: `5589fd27caa1466b6b50153614da706b354318bf284589dfc6cd5478cb21d5fb`
- Full JSON SHA-256: `bd2749b7f7b1afd836074890bf66f49ba96faa20353615b741fb2bd6cac1b30a` (1,595,642 bytes).
- Lossless gzip SHA-256: `ea33a8cd3dbbea12bffd13e5af1a5eecd61e235ee7617d056058b95cf4f72a7f` (180,077 bytes).
- Gzip Git blob: `b2627af6114570825e5dd9923a1e3e984018cebc`.

The additive documentation commit containing this file has the tested implementation as its sole parent. Its own SHA is supplied by Git history and the completion report, avoiding a self-referential hash.

## Boundaries

No entanglement requirement, selected physical source law, identity-anchored flow/semigroup, or gravity derivation follows. Full span does not force polar-skew response. The composite channel at source parameter zero includes the preparation channel and is not the identity. All previous scientific NOs remain unchanged, including v15.81's finite-window failure. No merge to main.
