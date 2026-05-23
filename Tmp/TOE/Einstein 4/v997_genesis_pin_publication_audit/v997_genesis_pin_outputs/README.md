# V997 Genesis Pin Publication Audit

## Run Summary

```json
{
  "document_id": "V997_GENESIS_PIN_PUBLICATION_AUDIT",
  "verdict": "genesis_pin_publication_audit_complete",
  "claim_demonstrated": "Same observable state does not certify legitimate history in the tested recoverability stack. Genesis Pin turns legitimacy into a recoverable-history property.",
  "histories_tested": 5,
  "accepted_without_genesis_pin": 5,
  "accepted_with_genesis_pin": 1,
  "minimal_genesis_pin": {
    "pinned_genesis_registry": [
      "W1",
      "W2",
      "W3",
      "W4"
    ],
    "pinned_genesis_anchor_root": "ROOT:GENESIS_ANCHOR_000",
    "witness_quorum": 3,
    "append_only_chain_required": true,
    "circular_bootstrap_rejected": true
  },
  "claim_boundary": "Modeled full-stack audit demonstration; not a universal proof, not production cryptographic security, and not a physics claim.",
  "publication_claim": "In the tested recoverability stack, visible-state equivalence accepts all five histories. With Genesis Pin, only the path satisfying pinned registry, pinned root, quorum witness participation, append-only continuity, and no circular bootstrap is accepted."
}
```

## Files

- `v997_genesis_pin_publication_audit.py`
- `V997_GENESIS_PIN_PUBLICATION_AUDIT.md`
- `CLAIM_BOUNDARIES.md`
- `PROTOCOL.md`
- `MANIFEST.json`
- `v997_layer_stack.csv`
- `v997_genesis_pin_results.csv`
- `v997_genesis_pin_result.json`
- `v997_genesis_pin_publication_audit.mp4`
- `v997_genesis_pin_publication_audit.gif`
- `v997_genesis_pin_final_frame.png`
- `v997_source.zip`

## Correct Claim

Same observable state is insufficient for legitimacy in the tested recoverability stack; legitimacy requires recoverable history anchored to pinned genesis.
