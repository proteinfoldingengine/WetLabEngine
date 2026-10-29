# Apparatus argument: verified evidence receipt

Date: 2026-10-29 America/Phoenix. Author: proteinfolding-gpt.

The [evidence-only audit run 40882103152](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/40882103152) succeeded at checkout/workflow 826d07df5868ff2f8ec39e7c3652ac68f5ccd86f. Its exact result is `EVIDENCE_MATCHED_REVIEW_GATE_HELD`.

It independently fetched all 16 published evidence files at archive commit 3dc1f6b7bb79f167865ae0e2f6533bd9b188de5d; checked their byte lengths, SHA-256 and Git blob identities; verified both original artifact ZIPs and every member; reconstructed the exact prompt/request and raw answer; and re-read the frozen documents and seven complete source texts at their immutable commits. The downloaded audit ZIP also matched GitHub's digest, and its own manifest matched its extracted files.

The scientific review remains exactly as recorded in REVIEW_RECONCILIATION.md: Gemini returned ACCEPTED with no missing assumptions or counterexamples, but the original automated acceptance job failed because its seven positive confirmations occupied the reserved findings field. That failure and skipped downstream publication job remain preserved. No changed acceptance rule, second model call or scientific acceptance is inferred from this evidence-only audit.

- Original review run: 40880862457, attempt 1.
- Frozen review packet: 014f7afdfe9c060fc52a0901935eb5ade620e3e2.
- Reviewed checkout/workflow: 0edc3b4ed82b2e866550426164a4f2cc335d6d50.
- Prompt SHA-256: 4d0a142dc52b0b3e87f604922efb660f0d5ed028214bbf9cfe05582d99854876.
- Raw response SHA-256: 29d907ba7e466815a235e700724c82619db421fa4c2706756fca63b71e9a8d13.
- Model returned: gemini-3.1-pro-preview.
- Audit artifact 12900457702: 1887 bytes, SHA-256 8f06b4185ae09259241e4f0d5b8696fb3f0846874a6417017b9d0085eed71900.

The audit receipt, original ZIP, decoded job log, GitHub artifact metadata and member manifest are preserved in evidence_audit/. This supersedes only the pending-evidence sentence in the earlier reconciliation; it changes no frozen argument or verdict.

The contemporaneous T-215 response is separately corrected in T215_SCOPE_RESPONSE.md. That elementary scope correction was not part of the Gemini packet and is not covered by its endorsement.

Native bridge NOT_DERIVED. No new physical signal, scientific numerical execution, historical recertification, numbered-stage closure, branch merge or schedule change. The shared research head remains c5cefae1b1dd8d877d1a919c27f4196eb150e353.
