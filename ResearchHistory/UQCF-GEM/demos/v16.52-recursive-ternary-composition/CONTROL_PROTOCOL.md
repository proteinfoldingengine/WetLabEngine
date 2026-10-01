# Prospective control-corpus clarification

This clarification is frozen before verifier or producer implementation and before any v16.52 numerical execution. Original registration693d0a77a83dbc2f162ad3bf655b386dc92a764e is retained unchanged.

The registration proposed a separately constructed canonical zero-path control corpus for genuine preimplementation verifier-level RED. Canonical zero paths cannot validate all permuted/inflated scientific starts. They will therefore have an explicit document kind, canonical_coverage_control, distinct from campaign.

Both kinds contain exactly the same7236 frozen specification identities and invoke the SAME unconditional exact-identity gate at the actual verifier.verify entrypoint, before any per-case validation. For campaign, independently reconstruct and require the frozen permuted/inflated start, full primitive path and common canonical endpoint. For canonical_coverage_control, independently reconstruct and require canonical start=end, exact profile, and a singleton path. This mode exists solely to test the verifier before producer implementation; its records are never reported as scientific campaign results or used to claim nontrivial repair success.

Before RED, commit the actual verifier and control tests. Verify the complete control corpus successfully; verify that the unmutated verifier rejects a missing identity. Inject only the historical supplied-only coverage defect into that actual entrypoint. The otherwise identical omitted corpus must then be accepted, making the test's expected rejection assertion fail. A helper-only call, path bypass, expected-start monkeypatch, or unrelated exception is not acceptable RED evidence. Repeat duplicate/substitution/wrong-identity controls in GREEN.

After implementation, require complete campaign verification and omission rejection on the genuine produced science corpus before definitive publication; this supplements rather than replaces the preimplementation control.

No scientific identities, starts, objectives, scope or outcomes change. Certification requires that every published scientific document has kind campaign. Coverage-control artifacts are separately labeled and retained as development evidence.
