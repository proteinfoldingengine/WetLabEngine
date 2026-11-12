"""Exact algebra audit of the supplied orbit-order example; not an exhaustive group test."""
import json
import sympy as s

t,p,z=s.symbols('t p z', real=True)
ii=s.I
zeta=(1-t*t+2*ii*t)/(1+t*t)
checks=[]

def zero(value):
    if isinstance(value,s.MatrixBase):
        return all(s.simplify(x)==0 for x in value)
    return s.simplify(value)==0

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)

def ptrace_k(matrix):
    return s.Matrix(3,3,lambda a,b:sum(matrix[4*a+k,4*b+k] for k in range(4)))

def ptrace_e(matrix):
    return s.Matrix(2,2,lambda a,b:sum(matrix[2*e+a,2*e+b] for e in range(2)))

def dilation(a,b):
    # Source order o,p,u,v. Retained-source order o,p,v.
    w=s.zeros(12,4)
    for j,out in [(0,0),(1,1),(3,2)]:
        for k in range(4): w[4*out+k,j]=a[k]
    for k in range(4): w[4+k,2]=b[k]
    return w

def target_channel(rho):
    result=rho.extract([0,1,3],[0,1,3])
    result[1,1]+=rho[2,2]
    return result

def channel_units(w):
    for a in range(4):
        for b in range(4):
            unit=s.zeros(4);unit[a,b]=1
            if not zero(ptrace_k(w*unit*w.H)-target_channel(unit)):
                return False
    return True

check('unit_phase_symbolic',zero(zeta*s.conjugate(zeta)-1))
a=s.Matrix([1,1,1,zeta])/2
b=s.Matrix([1,-1,1,-zeta])/2
check('marker_norms_and_orthogonality_symbolic',
      zero(a.H*a-s.eye(1)) and zero(b.H*b-s.eye(1)) and zero(a.H*b))
w=dilation(a,b)
check('isometry_symbolic',zero(w.H*w-s.eye(4)))
check('channel_all_16_matrix_units_symbolic',channel_units(w))

tau0=ptrace_e(a*a.H); tauu=ptrace_e(b*b.H)
delta=tauu-tau0
check('hadamard_pair_marginals_symbolic',zero(tau0-s.Matrix([
    [s.Rational(1,2),(1+s.conjugate(zeta))/4],
    [(1+zeta)/4,s.Rational(1,2)]])) and zero(tauu-(s.eye(2)-tau0)))
# For a traceless Hermitian 2x2 difference, D^2 = -det(delta).
d2=s.simplify(-delta.det()/25)
check('sharp_squared_margin_symbolic',zero(d2-1/(25*(1+t*t))))

q=p+(1-p)*zeta
q2=s.simplify(q*s.conjugate(q))
check('arbitrary_product_pair_phase_multiplier_symbolic',
      zero(q2-(1+(2*p-1)**2*t*t)/(1+t*t)))
excess=s.simplify(z*z+q2*(1-z*z)-1/(1+t*t))
check('all_orbit_members_lower_bound_identity',zero(excess-
      t*t/(1+t*t)*(z*z+(2*p-1)**2*(1-z*z))))
# Nonnegativity uses the explicitly declared ranges 0<=p<=1, -1<=z<=1.
values={str(n):str(s.factor(d2.subs(t,n))) for n in [0,1,2,10,1000]}
check('five_exact_sequence_values',all(s.Rational(v)>0 for v in values.values()))
check('phase_limit_minus_one',s.limit(zeta,t,s.oo)==-1)

a_inf=s.Matrix([1,1,1,-1])/2
b_inf=s.Matrix([1,-1,1,1])/2
w_inf=dilation(a_inf,b_inf)
check('blind_endpoint_is_orthonormal_isometry',zero(w_inf.H*w_inf-s.eye(4)))
check('blind_endpoint_preserves_all_16_channel_units',channel_units(w_inf))
check('adverse_control_orthogonality_does_not_imply_R_signal',
      zero(ptrace_e(a_inf*a_inf.H)-s.eye(2)/2) and
      zero(ptrace_e(b_inf*b_inf.H)-s.eye(2)/2))

rho_plus=s.diag(1,1,2,1)/5
rho_minus=s.diag(1,1,1,2)/5
owner=s.diag(0,1,0)
for label,ww in [('finite',w),('blind_limit',w_inf)]:
    contrast=s.trace(owner*ptrace_k(ww*(rho_plus-rho_minus)*ww.H))
    check('retained_p_contrast_'+label,zero(contrast-s.Rational(1,5)))

print(json.dumps({'status':'PASS','checks':checks,'check_count':len(checks),
 'd_R_squared_exact_values':values,
 'symbolic_d_R_squared':'1/(25*(1+t^2))',
 'limitations':['Algebra checks do not enumerate the infinite group.',
 'Compactness, connectedness, universal group-orbit bound and the greatest-orbit argument are proved in RESULT.md.',
 'This is not a native-event simulation or inherited-stack recertification.'],
 'native_bridge':'NOT_DERIVED','scientific_breakthrough':False},indent=2,sort_keys=True))
