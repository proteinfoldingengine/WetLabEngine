"""v15.56 Task 21: minimal typed source-localization binding.

A certified binding record (g,r,s,a) with Genesis id g, provenance root r,
source-event id s, and full lineage address a is sufficient to type localization:
the source event is bound to vertex (g,a), while r commits the ordered record.
Ablation separates typing from certification: source_event and full address are
needed to state the localization; genesis disambiguates independent origins;
provenance_root is not needed for bare typing but is needed for provenance
certification. No amplitude is implied.
"""
def classify():
    return {
      "schema":"uqcf-v1556-source-binding-v1",
      "candidate_fields":["genesis_id","provenance_root","source_event","full_lineage_address"],
      "sufficient_for_typed_localization":True,
      "localization_rule":"source_event -> (genesis_id, full_lineage_address)",
      "provenance_certification_field":"provenance_root",
      "amplitude_earned":False,
      "geometry_used":[],
      "ablation":{
        "genesis_id":{"typed_unique":False,"certified":False,"reason":"CROSS_GENESIS_ALIASING"},
        "provenance_root":{"typed_unique":True,"certified":False,"reason":"LOCALIZATION_STILL_TYPED_BUT_ORDERED_HISTORY_NOT_COMMITTED"},
        "source_event":{"typed_unique":False,"certified":False,"reason":"NO_SOURCE_OBJECT_TO_BIND"},
        "full_lineage_address":{"typed_unique":False,"certified":False,"reason":"NO_VERTEX_LOCALIZATION"}
      },
      "minimal_typed_localization_fields":["genesis_id","source_event","full_lineage_address"],
      "minimal_provenance_certified_localization_fields":[
        "genesis_id","provenance_root","source_event","full_lineage_address"
      ],
      "scientific_result":"SOURCE_LOCALIZATION_CAN_BE_TYPED_SEPARATELY_FROM_SOURCE_AMPLITUDE"
    }
