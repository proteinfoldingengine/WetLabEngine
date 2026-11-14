# Saved main-data AUC overlap audit: V725 and V737

Status: new bounded forensic result awaiting independent whole-argument review. This is not a native-construction theorem or historical assay reproduction. Research parent: `2ab565c3f5bf10305a96ddeef30901de49959ba5`. Prior PR151 source-assessment head: `571c647615f9ea2e77ce4705febf5e1b497cbba9`.

## 1. Premises and provenance

P1. The supplied archival inputs are the original downloaded V725 observable-only source, main CSV and result JSON; and source, main CSV and result JSON extracted byte-for-byte from the original V737 reproducibility ZIP. Their full bytes and identities are included, not only extracted summaries. `SOURCE_IDENTITIES.json` gives SHA256, byte length and Git blob identity. The V725 and V737 source blobs exactly match the immutable PR151 transcriptions. This authenticates the current downloaded source against those transcriptions, not historical runtime, executable environment, execution order, data generation or creation-chain provenance.

P2. Labels, k settings, target access, dynamics, trajectories and all saved scores are SUPPLIED synthetic data. They are not native event typing, owner identity, physical probability, action or receiver access. Actual atemporal measurement/pruning occurrence remains ACCEPTED INPUT. No additional cause-of-occurrence requirement is introduced.

P3. The declared comparison is ordinary exact-tie empirical Mann–Whitney AUC, assigning 1 for a positive score strictly greater than a negative score, 1/2 for exact equality, and 0 for less-than. Label 1 is positive, matching both actual scorers. No sign reversal, score re-estimation, new metric, label selection or parameter tuning is performed. This rule differs from any proposed approximate-tie convention; no approximate-tie convention is silently substituted.

P4. The V725 source uses NumPy `isclose(p, neg)` with defaults rtol=1e-5 and atol=1e-8. On the finite values audited here, its predicate is |p-n| <= 1e-8 + 1e-5|n|. The negative score is the reference argument, so the tolerance is asymmetric. NumPy 2.3.5 is pinned for this audit, not asserted to be the historical environment. The full source records its scoring and data-writing scheme; the generator is never imported or executed.

## 2. General comparator identity on finite saved values

For the Cartesian product of positive and negative rows, let N be the number of comparisons, W the strict-greater count, T the exact-equality count and C the isclose count. The actual V725 accumulation is (W+C/2)/N. Exact-tie empirical AUC is (W+T/2)/N. Every finite exact tie is close, so the difference is (C-T)/(2N), nonnegative.

A close unequal win satisfies both predicates and is credited 1.5, while a close unequal loss is credited .5 instead of zero. Therefore both unequal-close wins and unequal-close losses contribute to the excess relative to exact-tie AUC. This identity is a statement about the audited comparator, not a theorem that all datasets are affected, nor a claim that replacing one function validates the scientific model.

## 3. Complete V725 main-row result

The CSV contains 480 rows: exactly one label-0 and one label-1 row for each pair_id in 0..239. Label 0 has k=.9, label 1 k=.25. Every audited score is finite. N=240*240=57600 for every score. All corresponding saved main-summary JSON numbers are exactly reproduced by the original formula.

| Score | W | T | C | Actual saved formula | Exact-tie AUC |
|---|---:|---:|---:|---:|---:|
| restoration_distance | 57595 | 0 | 0 | 11519/11520 | 11519/11520 |
| adm_z | 57595 | 0 | 0 | 11519/11520 | 11519/11520 |
| g_atrium_observable_only | 57488 | 0 | 0 | 3593/3600 | 3593/3600 |
| g_atrium_with_k_oracle | 57556 | 0 | 0 | 14389/14400 | 14389/14400 |
| passive_mean | 28680 | 240 | 254 | 28807/57600 | 1/2 |
| passive_curvature | 28680 | 240 | 242 | 28801/57600 | 1/2 |

The four active/oracle values are approximately .9999131944444445, .9999131944444445, .9980555555555556 and .9992361111111111. They have no isclose comparisons at all. Thus this overlap does not explain their high AUC on these saved main rows. It does not thereby validate those scores, calibration, dynamics or access assumptions.

Both passive class score multisets match exactly. Passive mean has seven unequal-close wins and seven unequal-close losses; its excess is 14/115200, taking .5001215277777777 to exactly .5. Curvature has one unequal-close win and one unequal-close loss; its excess is 2/115200, taking .5000173611111111 to exactly .5. The historical Markdown reported these passive values to three decimal places as .500, so its main rounded qualitative comparison does not change.

For a concrete affected pair, passive_mean positive pair_id 24 is .5052135036274827 and negative pair_id 65 is .505210800443534. Their difference 2.7031839487934306e-6 is below the isclose tolerance 5.062108004435339e-6. This comparison receives 1.5. The reverse pair, also close here, receives .5. The complete affected comparison records are preserved in exploratory/RESULTS.json. No selection of just this example is used to calculate the result.

## 4. V737 comparison and floating aggregation

The bundled V737 source uses greater-than plus half exact-equality, which are disjoint. The main CSV has 840 rows / 420 complete paired IDs. Its atrium_scalar strict-win count is 169348 of 176400 comparisons, with no exact ties, yielding 42337/44100. The source's NumPy mean-of-row-means aggregation yields .9600226757369613, exactly matching the saved JSON. Direct rational-to-float conversion yields .9600226757369614. That one final aggregation-rounding difference is not an AUC mismatch. Restoration residual is 1, and both passive AUCs are 1/2; the actual scorer reproduces their saved values too.

The exploratory result JSON additionally applies the V725 formula hypothetically to V737 scores as a comparison control. Those values are NOT actual V737 outputs or defects. The audited V737 implementation itself has no V725 predicate-overlap bug.

V737 changes the dynamics, endpoint stencil, noise scaling and metric. Its correct disjoint comparator and internal main-data agreement do not make it an exact V725 replay or authenticate V725 scan/ablation AUCs.

## 5. Evidence method and countercontrols

An initial NumPy vector comparison audit was followed by separate scalar comparison counts and combined-average-rank exact-tie reconstruction. The declared row universe, both labels, complete pairing, finite values and all main scores are checked, not merely a supplied subset. Exact original input hashes are enforced before scoring. Rejecting controls exercise missing, duplicate and substituted rows, incorrect labels, nonfinite values and incorrect summary results. Their evidence is retained separately. Independent review must inspect the actual programs, rows, formulas and calculations rather than treating local agreement as acceptance.

The exploratory audit predates the review freeze and is explicitly not retrospectively preregistered. Subsequent fixed-data verification reproduces this bounded result; it is not a scientific generator run or numerical campaign. Original source and output bytes are preserved unchanged. This audit does not repair the historic source in place.

## 6. Exact limits and next obligation

Only the V725 and V737 main datasets are rescored. V725's saved JSON contains scan/ablation summaries, but the inspected CSV contains only main rows and the output-writing schema does not preserve those other row sets here. Their exact correction cannot be recovered from those summaries alone. V737's ZIP includes a gap CSV, but it is not scored in this task. No missing historical dataset is generated to fill the gap.

The source-and-data linkage is a present-byte hash match plus exact summary reproduction, not proof of historical generation. Prior PR151 Gemini acceptance covered the static caveat and supplied k-to-response trace, not this new data audit. No prior acceptance is imported. The inherited foundational stack and physical model are not recertified. No GR, geometry, physical probability, receiver delivery, certification or native source-event-owner correspondence is derived. Native bridge remains NOT_DERIVED and no premise moves from SUPPLIED to DERIVED.

The numerical next obligation, only if other historical numbers are to be reused, is to locate their exact original row-level outputs and verify the comparator on those inputs rather than extrapolate this result. The native next obligation remains a source-backed event-operation-same-owner available-effect correspondence; these synthetic rows do not provide it. No sweep, replay, metric tuning, new owner label or review of unchanged material is requested.
