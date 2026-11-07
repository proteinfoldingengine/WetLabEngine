# T-381 Gemini review adjudication

The exact T-381 counterexample and branch-weight boundary are accepted within their stated mathematical scope. Gemini returned ACCEPTED with empty findings, missing_assumptions and counterexamples. This is an independent model challenge, not physical validation or a derivation of native delivery.

## What was reviewed

- Frozen packet: `1b1b6dcb94ead0372c255602c3bbc592bab57be4`.
- Reviewed implementation: `3fb80b3fefef37ddfc4f03877aad994e870b4cec`.
- Run: https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/42420884489 , attempt 1.
- Requested and returned model: `gemini-3.1-pro-preview`; one generation, no fallback or favorable-verdict retry.
- Prompt SHA256: `1236c199b0661686cd3c8ca41e3334f8a8c851801e580c1a41d4e32ca6237507`.
- Raw response SHA256: `769ea3724d373868f5ab707232efc3670a34df50ad4dbacc8063115cc01256fc`.
- Full raw response: `parity-weight-review-1/response.json`; readable complete response: `parity-weight-review-1/review.txt`.
- Proof discovery preceded the freeze, as disclosed in REVIEW_PLAN.md. Only review/evidence handling was prospectively frozen.

Gemini reconstructed the positive diagonal states, equal R marginals, positive sector weights, equal conditional R states, the all-u parity law, 5/8 versus 3/8 probabilities, zero contrast for every R-only effect, and zero connected correlators. It also reconstructed the subtraction argument: differing sector weights plus fixed conditional states and a fixed R marginal force equal conditionals and product states, hence c_a=q_a m. Constant weights give no variation; this family is collinear and cannot cover arbitrary three-dimensional r with fixed m.

Gemini judged the correction fair to the strengthened conditional-delivery reading of T-378, while retaining the correlator lemma and original Clifford-family result. The exact T-378-prereg excerpt explicitly names conditional delivery and says its delivery reading is unchanged. This adjudication keeps T-381's narrower claim; it does not treat every T-378 statement as false.

## Reviewer qualifications and author adjudication

1. The raw reconstruction contains a mistaken intermediate partial trace for rho_minus and immediately corrects it using the specified ordering. Preserve the response unchanged. The correct R marginal is diag((3+9)/16,(1+3)/16)=diag(3/4,1/4).
2. The response describes vanishing connected correlators as proving that no new correlations are created. The evidence establishes product output states and zero connected correlators in this static family. It does not establish any dynamical history or correlation-creation process.
3. Gemini proposes uniform bit marginals or non-vanishing connected correlators as a future gate and asks for true conditional delivery. That recommendation is not adopted as the native receiver-delivery criterion. Neither property by itself establishes source dependence, native production, ownership, or an unavoidable receiver effect. A source-independent correlated state can have both uniform bit weights and nonzero connected correlators. The exact retained conditional statement is: with fixed m and fixed q, varying c forces conditional-state variation on supported sectors.
4. The user's broader target remains any realization-independent receiver-owned observable consequence. For the generalized one-pair target, if the full joint algebra is independently earned as one owner's interface, the varying bit alone can be informative. If the designated receiver owns only R, this example leaves it entirely blind. Ownership and native production remain to be derived.
5. No W_R/W_E classification is assigned without an explicit typed embedding. No preparation, interaction, gravity claim, new physical postulate, or larger numerical campaign follows.

## Scientific disposition

Keep the counterexample and exact boundary as an analytical scope correction. Preserve the raw review, including its self-correction and recommendations. Resume inherited ownership, native joint-event asymmetry, and unavoidable receiver-owned consequences; do not turn this review into a conditional-channel branch.

Native bridge: **NOT_DERIVED**. Scientific breakthrough: **false**. PR #138 remains draft and unmerged. PR130/131 HOLD and PR136/137 remain unchanged.

## Verification and publication record

All four jobs completed successfully: verification 128548862352, review 128549412949, publication 128549646649, archive 128549860251. The inherited stack was unchanged; its producer, independent verifier, historical reproduction, and fresh byte replay passed. Evidence controls rejected changed, missing and additional files. These checks support evidence integrity; the analytical proof is not established by enumeration.

The publication job parsed the original response and compared the exact prompt, request, model, verdict and digests; it read all seven submitted files at the reviewed immutable commit. A separate local inspection verified the complete review/publication ZIP member manifests and reparsed the response. The original archive commit is `9614163e8af85570393a2ea3257a4732834e3efe`. The archive job verified each original ZIP against the API digest, checked complete manifests, committed original files with reversible chunks for large files, fetched the branch and reconstructed all committed bytes. Its completed log contains the successful committed-byte readback.

| Original artifact | Bytes | SHA256 |
| --- | ---: | --- |
| parity-weight-verification-1.zip | 239367469 | a563c2baba0dcf928e6a2b5423fce94711e43fc3d86e9bc6323aab4b6edc5210 |
| parity-weight-review-1.zip | 82923 | ce97e216bc05096ff721b40d8071c46573d3c66bedcaabd431681ab231dec80a |
| parity-weight-publication-1.zip | 330998 | 5141c5cab329ccb315d4f2abc370381581e3afd928ee071cccec589d58dddd36 |

The GitHub connector read back the complete raw response and readable review at the archive commit; both matched the downloaded review ZIP exactly. The final closure directory preserves the fourth completed job log and its digest separately, leaving the original archive and SHA256SUMS untouched. Its UTF-8 log is 43863 bytes with SHA256 `445b862bf203c79c9d0bbca92ecd12dc34f99658f17b7a762454223a1faffc14`.
