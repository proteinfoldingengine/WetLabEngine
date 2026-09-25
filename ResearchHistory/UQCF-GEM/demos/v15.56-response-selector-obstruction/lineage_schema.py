"""v15.56 Task 10: minimal lineage-history schema sufficiency.

Counterexample: two siblings can share genesis_id, parent_address,
repair_index and recoverability_depth while remaining distinct descendants.
Therefore those four fields do not determine unique correspondence.  A stable
child/branch lineage address (or equivalent distinguishing provenance token) is
necessary.  This conclusion is combinatorial and uses no geometry.
"""
def classify_schema():
    return {
      "schema":"uqcf-v1556-lineage-schema-v1",
      "fields":["genesis_id","parent_address","repair_index","recoverability_depth"],
      "address_uniqueness_required":True,
      "primary_verdict":"SCHEMA_INSUFFICIENT_FOR_UNIQUE_CORRESPONDENCE",
      "controls":[
        "SIBLING_SWAP","DUPLICATE_DEPTH","REPAIR_REORDER","GENESIS_MISMATCH"
      ],
      "geometry_fields":[],
      "counterexample":{
        "type":"INDISTINGUISHABLE_SIBLINGS",
        "same_fields":[
          "genesis_id","parent_address","repair_index","recoverability_depth"
        ],
        "distinct_descendants":2,
        "correspondence_permutation_count":2
      },
      "minimal_missing_datum":
        "STABLE_CHILD_BRANCH_LINEAGE_ADDRESS_OR_EQUIVALENT_PROVENANCE_TOKEN",
      "theorem_statement":
        "PARENT_PLUS_ORDER_DEPTH_DATA_DO_NOT_SEPARATE_SIBLINGS; UNIQUE_DESCENDANT_CORRESPONDENCE_REQUIRES_A_DESCENDANT_SEPARATING_LINEAGE_DATUM"
    }
