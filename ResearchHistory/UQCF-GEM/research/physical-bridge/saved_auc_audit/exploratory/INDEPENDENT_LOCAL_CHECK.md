# Independent saved-score audit

Separate local reviewer disposition: PASS, no blocker. This is not Gemini acceptance.

The reviewer parsed original saved files separately, reconstructed scalar comparison counts, and cross-checked exact-tie AUC with combined average ranks. No historical module was imported or executed.

V725: 480 rows, 240 complete pairs, correct label/k assignments, finite scores.
- restoration distance and adm_z: 11519/11520, unchanged.
- observable-only: 3593/3600, unchanged.
- k-oracle: 14389/14400, unchanged.
- passive mean: 28807/57600 -> 1/2; 7 unequal close wins and 7 unequal close losses beyond 240 exact ties.
- passive curvature: 28801/57600 -> 1/2; 1 unequal close win and 1 unequal close loss beyond 240 exact ties.

V737: 840 rows, 420 complete pairs. Its actual disjoint scorer reproduces saved main values. Atrium exact rational is 42337/44100; the saved decimal differs from direct rational conversion only by floating aggregation rounding. Restoration is 1; both passive controls 1/2. Hypothetical V725-formula numbers in RESULTS.json are comparison controls, not V737 defects.

Both source Git blob hashes match PR151. NumPy's asymmetric tolerance was respected; reversing arguments changes zero classifications on these main datasets.

Limits: saved-main-row scoring only, not generation replay or certification. V737 gap CSV exists but was not scored. V725 gap/scan summary values alone do not establish their exact corrections. No Gemini generation or publication occurred.
