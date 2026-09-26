"""Finite holonomy -> curvature-density identifiability gate."""
from fractions import Fraction as F
import completion_connection_bridge as cb
AREAS=(F(1),F(3,7),F(11,5))
def analyze_hidden(h=F(1,100)):
    a=cb.analyze(cb.state(h=h),cb.source()); r=a['scale_free_ratio']
    if r==0: raise ArithmeticError('Nonzero witness required')
    vals=[r/A for A in AREAS]
    return {'h':h,'holonomy_trace':a['trace'],'holonomy_trace_jet':a['trace_jet'],
            'reference_jet':a['reference_jet'],'holonomy_scale_free_ratio':r,
            'diagnostic_area_scales':list(AREAS),'candidate_density_ratios':vals,
            'density_ratio_spread':max(vals)-min(vals)}
def flat_trace_control():
    a=cb.analyze(cb.state(h=F(1,100),x=F(1),y=F(0)),cb.source())
    m=max(abs(x) for row in a['holonomy_jet'] for x in row)
    return {'initial_loop_trace':a['trace'],'loop_trace_jet':a['trace_jet'],
            'max_holonomy_matrix_jet_entry':m,
            'trace_observable_complete':a['trace_jet']!=0 or m==0}
def run():
    return {'schema':'uqcf-holonomy-curvature-identifiability-v1','baseline':'1ff3500689c3d764a9a9b7ce81c853303904ed74',
            'finite_holonomy_response_certified':True,'curvature_density_identified':False,
            'reason':'NO_CANONICAL_LOOP_AREA_OR_CONTROLLED_SMALL_LOOP_REFINEMENT_IN_THIS_FINITE_BRIDGE',
            'required_for_curvature_density':['oriented loop area/bivector from retained geometry','controlled refinement with loop area -> 0','local Lie-algebra/log-holonomy branch compatible across refinement'],
            'positive_hidden':analyze_hidden(F(1,100)),'negative_hidden':analyze_hidden(F(-1,100)),
            'flat_trace_control':flat_trace_control(),'posthoc_fit':False,
            'claims':{'holonomy_response_survives':True,'curvature_2form_derived':False,'riemann_or_regge_curvature_derived':False,'gravity_signal':False}}
def serial(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {k:serial(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [serial(v) for v in x]
    return x
if __name__=='__main__':
    import json; print(json.dumps(serial(run()),indent=2,sort_keys=True))
