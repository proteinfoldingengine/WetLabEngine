"""v15.56 Task 20: provenance-protected structural product identity.

The product identity combines independent earned roles:
 genesis_id identifies the Genesis provenance class;
 provenance_root is an append-only hash commitment to ordered history;
 full_lineage_address supplies prefix-stable structural ancestry.
The product therefore supports both tamper-evident provenance and intrinsic
parent-child incidence. It localizes a source only when the source's certified
ledger record explicitly binds that structural address. No amplitude follows.
"""
def classify():
    return {
      "schema":"uqcf-v1556-product-identity-v1",
      "identity":"(genesis_id, provenance_root, full_lineage_address)",
      "tamper_evident_provenance":True,
      "intrinsic_parent_child_incidence":True,
      "roles":{
        "genesis_id":"ORIGIN_CLASS",
        "provenance_root":"ORDERED_HISTORY_COMMITMENT",
        "full_lineage_address":"STRUCTURAL_ANCESTRY"
      },
      "source_localization_status":"TYPED_IF_SOURCE_LEDGER_RECORD_BINDS_FULL_LINEAGE_ADDRESS",
      "required_binding_fields":[
        "genesis_id","provenance_root","source_event","full_lineage_address"
      ],
      "source_amplitude_earned":False,
      "geometry_used":[],
      "scientific_result":
        "PROVENANCE_CERTIFICATION_AND_STRUCTURAL_DIFFERENTIAL_INCIDENCE_CAN_COEXIST_WITHOUT_IDENTIFYING_HASHES_AS_GEOMETRIC_OR_BRANCH_COORDINATES"
    }
