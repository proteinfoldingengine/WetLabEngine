# V993 C_reganchor Closure Freeze Packet

## Verdict

`C_reganchor_closure_freeze_certified`

Closed for V993 C_reganchor freeze: **True**

## Current tested object

```text
C_reganchor = (
  Q_obs,
  S_ternary,
  symbol_emission_event_ledger,
  generator_compatibility_causal,
  event_freshness_credential,
  anchored_append_only_freshness_ledger,
  byzantine_fault_bound_quorum_witness,
  authorized_witness_identity_weight_registry,
  current_registry_quorum_epoch_governance,
  append_only_one_successor_registry_update_ledger,
  anchored_registry_update_ledger_root
)
```

## Key results

```text
canonical registry-update ledger rows:
  2

canonical registry-update root:
  78a80f92eb0215ccd3fcf36d

naive local regchain unsafe accepts:
  2

anchored regchain unsafe accepts:
  0
```

## Certification table

| layer                                    | source   | passed   | evidence                                                          |
|:-----------------------------------------|:---------|:---------|:------------------------------------------------------------------|
| causal_closure                           | V971     | True     | causal_coupled_closure_freeze_certified                           |
| authorized_identity_registry_closure     | V987     | True     | C_identity_closure_freeze_certified                               |
| current_registry_epoch_governance        | V989     | True     | C_registry_closure_freeze_certified                               |
| one_successor_registry_update_ledger     | V991     | True     | C_regchain_closure_freeze_certified                               |
| registry_update_ledger_rollback_boundary | V992     | True     | naive rollback unsafe accepts=2                                   |
| anchored_registry_update_root            | V992     | True     | anchored regchain unsafe accepts=0; root=78a80f92eb0215ccd3fcf36d |

## Scientific conclusion

Registry-update history itself must be anchored.

Otherwise the system can be made to forget that an epoch edge has already been consumed.

## Current closure condition

```text
C_reganchor =
  C_regchain
  + anchored registry-update ledger root
```
