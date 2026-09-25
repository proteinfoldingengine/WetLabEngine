"""v15.56 Task 14: native scalar carrier over retained identities.

For a retained identity set K_R, Q-valued scalar observables form Map(K_R,Q).
A partial bijection of shared identity keys canonically supports restriction and
pullback on the shared domain. No geometry is required for this carrier.

This does not transfer the v15.45 periodic-square operator: its translations
X,Y and Laplacian Delta require adjacency/incidence structure not supplied by a
bare identity set.
"""
def classify():
    return {
      "schema":"uqcf-v1556-native-scalar-carrier-v1",
      "carrier":"Map(K_R,Q)",
      "identity_key":["genesis_id","child_branch_address"],
      "scalar_field_definition":"f:K_R->Q",
      "shared_key_pullback_canonical":True,
      "shared_key_restriction_canonical":True,
      "unmatched_key_extension_canonical":False,
      "geometry_used":[],
      "v1545_operator_native_on_carrier":False,
      "missing_for_operator":[
        "RETAINED_INCIDENCE_OR_ADJACENCY",
        "EARNED_DIFFERENCE_OPERATOR",
        "EARNED_SECOND_DIFFERENCE_OR_LAPLACIAN"
      ],
      "primary_result":
        "NATIVE_SCALAR_CARRIER_AND_SHARED_KEY_TRANSPORT_EARNED;_CURVATURE_OPERATOR_NOT_YET_EARNED"
    }
