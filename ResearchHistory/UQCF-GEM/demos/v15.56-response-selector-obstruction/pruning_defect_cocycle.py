"""v15.56 Task 34: pruning response defect and composition identity.

Fix for each pruning r:f->c a linear response coarse map A_r and centering
projector Q_c. Define D_r = Q_c A_r G_f - G_c P_r.

For composable r:f->m and q:m->c, if response maps compose
A_{q r}=A_q A_r, source pushforwards compose P_{q r}=P_q P_r, and centering
is respected by A_q (Q_c A_q Q_m = Q_c A_q), direct expansion gives

 D_{q r} = Q_c A_q D_r + D_q P_r.

This is an exact twisted 1-cocycle identity for a *fixed functorial choice* of
response coarse maps A. The present retained stack canonically earns P, but
Task 32 proves no all-source fiber-local A can make D vanish; it does not select
a unique A. Therefore the defect family is not yet canonical from pruning alone.
"""
def classify():
 return {
  "schema":"uqcf-v1556-pruning-defect-cocycle-v1",
  "defect_operator":"D_r = Q_c A_r G_f - G_c P_r",
  "composition_identity_derived":True,
  "composition_identity":"D_{q o r} = Q_c A_q D_r + D_q P_r",
  "assumptions":[
   "A_{q o r}=A_q A_r",
   "P_{q o r}=P_q P_r",
   "Q_c A_q Q_m=Q_c A_q"
  ],
  "source_pushforward_functoriality_earned":True,
  "response_map_functoriality_earned":False,
  "cocycle_status":"NOT_CANONICAL_WITHOUT_RESPONSE_MAP",
  "geometry_used":[],
  "scientific_result":"EXACT_DEFECT_COMPOSITION_IDENTITY_CONDITIONAL_ON_A_FUNCTORIAL_RESPONSE_COARSE_MAP;_NO_CANONICAL_DEFECT_FROM_PRUNING_ALONE_YET",
  "next_gate":"SEARCH_FOR_INTRINSIC_DEFECT_CLASS_INDEPENDENT_OF_RESPONSE_COARSE_MAP"
 }
