# Independent mathematical review: saturated redundancy transfer

Verdict: ACCEPTED. Not formal certification or broad C3/C4 closure.

Science/workflow commit: d1b8cbe3dbe122bd4b929d3ed5484ef214bad9d5. Run: 38012134114. Model: gemini-3.1-pro-preview. Input files: 18. Total tokens: 26064. Response SHA256: 132341c7ccb047212e41210bb2107aa0c23c112858749a726ea0b649dd367892.

[Unmodified raw response](evidence/saturated-transfer/mathematical-review-response.txt) and exact manifest/archive hashes are preserved. Zero missing assumptions and counterexamples listed.

- The saturated redundancy-transfer theorem is mathematically sound and correctly applies the universal core-region criterion.
- The footprint containment logic (mapping current footprints to original footprints) correctly establishes the lower protection bound tau(current) >= tau(original) without requiring an injective mapping. The strict separation of label movements ensures no current footprint spans incompatible original footprints.
- The batched operations (e.g., adding D to all W before removing A) correctly maintain the upper bound tau <= 4 by ensuring a valid 4-cover (B, C, E, and either A or D) exists at every intermediate slice.
- The k=1 isolation proof is correct: any valid addition creates a footprint not contained in any original footprint (violating lower protection), and any deletion violates the saturated floor.
- The exact endpoint is reached, swapping A and D while preserving all private labels and hidden completions, allowing for renewable exchanges.
- The bounded verification code (producer.py and independent.py) correctly implements the theoretical model, exhaustively checking the domain up to m=4, including all canonical partitions and valid donor/reserve pairs.
- The RED log correctly demonstrates the missing-producer import failure, confirming the test suite's dependency and execution.

Limitations retained:

- The constructive transfer requires k >= 2; k = 1 is proven to be isolated under the strict core-only policy and saturated floors.
- The script length 2m + 4 + 4|V_r| is a verified upper bound but is explicitly not claimed to be globally optimal.
- The theorem assumes the observer only has access to the core and does not derive physical core access, outcome selection, or guaranteed progress (NOOPs can stall).

Author reconciliation: scope/proof frozen before computation; complete bounded domain m=2,3,4, not all smaller m; RED executes only loader failure, not scientific test bodies. Analytical arbitrary-partition/hidden-palette proof is distinct from finite enumeration. Ordinary subset containment suffices for safety. Script cost is not global optimality. Supplied per-macro goals/core access and NOOP progress remain assumptions. The API assessment reads supplied records; its freeze-identity assertion is reconciled by author immutable GitHub readback, not an independent reviewer fetch of history. See closeout for exact boundary and evidence.
