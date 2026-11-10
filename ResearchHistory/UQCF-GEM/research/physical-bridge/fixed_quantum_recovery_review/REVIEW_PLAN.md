# Prospective fixed-decoder whole-argument review plan

Prepared 2026-11-10 UTC. Source baseline d373865d27052562d52a55fbe4cd18a263f00fc5.

## Scope and already-known material

Review the complete ARGUMENT.md, not only one recovery identity. Original comments 6767124759 and 6767202192, their scripts/results, and the single-effect follow-through predate this protocol. They are known analytical/posthoc material, not prospective discoveries. Preserve original comment bodies and metadata, the raw sources, all adverse findings, and any failed verification/review outputs. No old campaign is rerun and no physical model is fitted.

## Fixed supporting checks

Use the same four-dimensional source, two environment qubits, source pair and explicitly listed isometries only. No random inputs, expanding search, parameter sweep, or new implementation family.

1. Reconstruct W_R, W_E/B, the specified Bell representative, and A. Check isometry and C on all 16 source matrix units for each.
2. Reconstruct the individual D_W completion with the fixed testing choice tau=Pi_o and verify recovery and trace preservation. The theorem for arbitrary density tau rests on the analytical proof, not this fixed check. Check the common classical basis partition for W_R/W_E; explicitly exhibit its Bell-u failure.
3. Construct L_0,L_1 and the CPTP completion of D. Verify the rank-eight P, trace preservation, all 16 common quantum recovery identities under A/B, and the displayed L_r A/L_r B identities.
4. Compute the complete R reduced maps on all source matrix units, not only the pair, and the same fixed F contrast. Verify B is completely blind and A's contrast is 1/5. Check initial blindness.
5. Compute D*(Pi_u), its equality with the declared G, and PGP=PG_EP. Include an off-code witness showing G != G_E globally. Check the pair's E-only outcome probabilities 2/5 and 1/5.
6. Verify P(e_u−e_p)=0 and the displayed signed P2 loss vector. Do not interpret that algebraic calculation as a stored flag.
7. Reject at least these corruptions: dropped complement term; removed L_1 phase sign (off-diagonal source test must fail); incorrect claim that the new D decodes old W_R; and global equality of G and G_E. These are disclosed mutation controls, not new discoveries.

Use an independent standard-library Fraction reconstruction and a SymPy reconstruction. For A/B operator outputs, work with exact rational outer products; A has a common 1/sqrt(2) column factor, so its density-map entries are rational. Exact symbolic amplitude checks may remain in the SymPy side. The independent implementation must not call the producer to obtain its expected results. Compare semantic outputs and preserve full stdout/stderr.

Run the unchanged established 22+15+2 inherited regression/certificate stack. Add protocol tests for missing/added/modified artifacts, inconsistent verdicts and identity mismatch. These checks validate this fixed argument and review plumbing, not a universal physical result.

## Independent adversarial review

Freeze manuscript, protocol, source packet, original posts and hashes at an immutable scientific/review commit before the new verification. Supply the full current argument, known controls and complete claim-bearing source texts. Do not include prior reviewer votes or peer agreement as evidence. The reviewer must independently reconstruct the strongest positive argument and seek counterexamples to its quantifiers, complete positivity, trace preservation, reference-extension claim, fixed-interface claim, and on-code/off-code distinctions.

Exactly one Gemini generation through existing Actions secrets, requested model gemini-3.1-pro-preview, verified availability and returned identity. No fallback and no automatic retry after uncertain execution. Preserve raw request, response, model metadata, prompt, run/attempt/checkout/workflow identities and original ZIPs/manifests. Parse ordinary non-thought answer text only; preserve opaque fields without decoding them.

Require strict JSON verdict ACCEPTED/REVISE/FAIL with findings, missing_assumptions, counterexamples, limitations, reconstruction and constructive_analysis arrays, native_bridge_status and next_native_obligation. ACCEPTED requires the three objection arrays empty. The reviewer may challenge any current claim. Stated open physical premises are not silently discharged by mathematical acceptance; a conflicting native label is preserved for author adjudication rather than adopted.

## Publication and stopping

Use a separate fresh publication job to repeat fixed verification and inherited replay, reconstruct the exact prompt/request, parse the original raw answer, check every identity/hash and read all frozen files back at immutable commits. Archive original artifact ZIPs, exact members and digests, raw evidence and completed logs durably on the isolated review branch; verify committed bytes, including reconstructed large-file chunks if needed.

Stop after the one completed generation and publication, or at a reported unresolved infrastructure/authorization failure. Preserve any adverse or malformed raw output durably before repair; never regenerate to chase acceptance. Resolve substantive objections under a new honest freeze if required. Keep the draft PR unmerged; no PR130/131/142 changes, main updates, Atlas work, new physical premises or unrelated numerical campaign.
