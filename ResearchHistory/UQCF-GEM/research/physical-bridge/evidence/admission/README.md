# Exact admission evidence

Original ZIPs are preserved byte-for-byte. EVIDENCE.json contains author-verified archive/member/input/response identities and reporting clarifications. Raw reviews are unchanged. The complete certificate is inside original-verification.zip.

To reproduce base reconciliation in a scratch copy of this directory, run `python ../../admission/producer.py certificate.json` then `python reconcile.py`. This regenerates the base ledger; the committed ledger additionally records author clarifications, test counts, job IDs and source blob identities. No secret is needed. Immutable source snapshots are in source_inputs.json. An offline classifier is not native observer access.
