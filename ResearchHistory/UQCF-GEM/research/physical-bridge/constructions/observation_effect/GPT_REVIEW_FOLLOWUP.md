# GPT follow-up to observation_effect draft 1

2026-10-17 America/Phoenix. Mathematical extension and scoped corrections independently ACCEPTED; see the acceptance receipt. Original draft 086ab0ad82bbfa220915e75a2ae408e05851c849 remains unchanged.

The exact argument and controls are frozen in [observation_preservation_review/RESULT.md](../../observation_preservation_review/RESULT.md), commit 53d164b07e32576f04bdedc31f1c2d3757e9637e. [Acceptance receipt](../../observation_preservation_review/REVIEW_ACCEPTANCE.md) records Gemini acceptance in run 39091716370 after explicit external-submission approval. Acceptance covers this frozen extension and scoped corrections, not the entire original draft.

## Constructive extension

For a conditional expectation with predual E, write K_r for the support actually occupied in receiver sector Q_r after E. For any supplied CPTP map with Kraus operators L_j, all receiver weights survive E Phi E for all inputs iff

    (I-Q_r) L_j K_r = 0 for every r,j.

This removes the faithfulness restriction in draft Theorem 4 and extends to coarse central receiver records. Faithful unitary observation reduces to [U,Q_r]=0. In the P2 commutative owner section, exact fiber-weight preservation is PTI=id: each retained owner's transition column must stay in its original fiber. No motion or physical record is supplied by this criterion.

## Corrections before the draft's own freeze

1. Theorem 4(c)'s existence condition needs BOTH n_k>=2 and m_k>=2 in some block. A=C I_2 is a counterexample to multiplicity alone: every unitary normalizes it. The frozen extension gives the full corrected proof and a constructive mixed-block witness.
2. Corollary 1.4's nonnormalization criterion means there exists an input with an effect, not that every actual preparation changes. Qubit dephasing, U=Hadamard and rho=I/2 give zero effect despite nonnormalization.
3. Proposition 8.1's E^2=E is a nonselective map identity, not a test for occurrence or count of actual selective measurement events. Retain the algebraic identity while restricting the event-count interpretation.
4. The P2 owner section is nonfaithful/nontracial for a proper contraction. The identity contraction is the exception.

The original positive observation-effect demonstration remains a separate conditional task. Neither that draft nor this extension derives receiver ownership, an available outcome instrument, actual collapse or native motion. The inherited v15.17 full-block conclusions are unchanged. No scratch results or 96-case table were reproduced here.
