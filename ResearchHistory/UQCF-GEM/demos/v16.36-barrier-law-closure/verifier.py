import producer as _forbidden
# placeholder deliberately invalid independent verifier; substantive RED must reject import dependence
def verify_document(d):
 if not all(k in d for k in ('gate_a','gate_b','gate_c','gate_d','gate_e')):raise ValueError('missing gate')
 if d.get('_corrupt'):raise ValueError('corrupt')
 for x in d.get('pairs',[]):
  if not x['candidate_signature']['q']:raise ValueError('signature')
 return {'execution_status':'COMPLETED'}
