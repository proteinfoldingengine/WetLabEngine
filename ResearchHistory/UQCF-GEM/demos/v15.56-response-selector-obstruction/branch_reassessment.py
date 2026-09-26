"""Branch reassessment: choose the next independent gate without reopening stopped seams."""
ROUTES={
 'completion_selector':{'status':'STOP','reason':'v13.23 factorization no-go; current matched witness adds no preselection discriminator'},
 'finite_holonomy_to_curvature':{'status':'STOP','reason':'missing native area/bivector and selected shrinking-loop refinement'},
 'absolute_source_calibration':{'status':'STOP','reason':'v13.26 RSCL irreducible under positive common rescaling'},
 'provenance_to_quantum_source':{'status':'STOP','reason':'v14.04-v15.03 require new representation link; state-dependent source laws nonunique'},
 'operational_recoverability_defect_to_compatibility':{'status':'LIVE','reason':'v15.54 independently certifies an operational nonclassical obstruction; source correspondence not evaluated'},
}
def run():
 live=[k for k,v in ROUTES.items() if v['status']=='LIVE']
 return {'schema':'uqcf-branch-reassessment-v1','baseline':'c98267808aaf37ff56856875f311d7e6e6852587','routes':ROUTES,'live_routes':live,
 'selected_next_gate':'OPERATIONAL_DEFECT_TO_RETAINED_COMPATIBILITY_NATURAL_TRANSFORMATION_CLASSIFICATION',
 'gate_question':'Given the already-certified v15.54 operational defect object D and frozen retained compatibility object A, classify covariant neutral compositional maps eta:D->DeltaA; determine uniqueness, nonuniqueness, or obstruction before any curvature target is consulted.',
 'must_not_use':['hidden completion sign','holonomy/curvature quality','ADM/Einstein residual','absolute source calibration','new area/refinement proxy'],
 'physical_claim':False}
if __name__=='__main__':
 import json; print(json.dumps(run(),indent=2,sort_keys=True))
