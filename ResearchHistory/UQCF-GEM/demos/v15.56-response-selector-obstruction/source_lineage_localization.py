"""v15.56 Task 18: historical source-event -> retained-lineage localization audit.

v14.04 certifies that the archived Genesis ledger carries source-origin and
ordered-lineage identity.  That is stronger than source-origin alone, but the
audited publication does not certify that this identity is the same typed,
stable full child/branch address K_R introduced in v15.56.  We therefore do not
promote it to a full source->K_R localization map without an explicit schema
equivalence theorem.  Source amplitude remains separately unearned.
"""
def audit():
    return {
      "schema":"uqcf-v1556-source-lineage-localization-v1",
      "localization_verdict":"SOURCE_ORIGIN_ONLY_NOT_FULL_LINEAGE_KEY",
      "historical_carrier":"GENESIS_LEDGER_SOURCE_ORIGIN_AND_ORDERED_LINEAGE_IDENTITY",
      "target_identity_key":["genesis_id","child_branch_address"],
      "full_source_to_K_R_map_earned":False,
      "amplitude_rule_earned":False,
      "geometry_used":[],
      "evidence_paths":[
        "ResearchHistory/UQCF-GEM/v14/v14.04/REPORT.md",
        "ResearchHistory/UQCF-GEM/v14/v14.04/provenance_representation_audit.py"
      ],
      "earned_historical_fact":
        "ARCHIVED_GENESIS_LEDGER_CARRIES_SOURCE_ORIGIN_AND_ORDERED_LINEAGE_IDENTITY",
      "missing_equivalence":
        "THEOREM_IDENTIFYING_ARCHIVED_ORDERED_LINEAGE_IDENTITY_WITH_V1556_STABLE_FULL_CHILD_BRANCH_ADDRESS",
      "next_gate":
        "AUDIT_ARCHIVED_GENESIS_LEDGER_SCHEMA_FOR_PREFIX_STABLE_BRANCH_ADDRESS_EQUIVALENCE"
    }
