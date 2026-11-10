"""Algorithmically independent fixed checks using stdlib Fraction.
No import of CHECK.py or SymPy. Prospective review plan: REVIEW_PLAN.md.
"""
from fractions import Fraction as F
import json

def matmul(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def add(a,b): return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(c,a):return [[c*x for x in row] for row in a]
def rank(a):
    a=[list(map(F,row)) for row in a];i=0
    for j in range(len(a[0])):
        pivot=next((k for k in range(i,len(a)) if a[k][j]),None)
        if pivot is None:continue
        a[i],a[pivot]=a[pivot],a[i];v=a[i][j];a[i]=[x/v for x in a[i]]
        for k in range(len(a)):
            if k!=i:
                v=a[k][j];a[k]=[x-v*y for x,y in zip(a[k],a[i])]
        i+=1
        if i==len(a):break
    return i
def require_full_support(effects):
    n=len(effects[0]);assert rank([row for a in effects for row in a])==n
def dot(a,b):return sum(F(x)*y for x,y in zip(a,b))
def diag(a):return [[x if i==j else F(0) for j in range(len(a))] for i,x in enumerate(a)]
def identity(n):return diag([F(1)]*n)
def expectation(a,v,norm2):
    return sum(F(v[i])*a[i][j]*v[j] for i in range(len(v)) for j in range(len(v)))/norm2
def channel_units(e0,eu,norm2):
    assert dot(e0,e0)==dot(eu,eu)==norm2 and dot(e0,eu)==0
    retained=(0,1,3);r=(0,1,1,3);env=[e0,e0,eu,e0];count=0
    for i in range(4):
        for j in range(4):
            actual=[[F(0) for _ in range(4)] for _ in range(4)]
            actual[r[i]][r[j]]=dot(env[i],env[j])/norm2
            expected=[[F(0) for _ in range(4)] for _ in range(4)]
            if i in retained and j in retained:expected[i][j]=F(1)
            if i==j==2:expected[1][1]=F(1)
            assert actual==expected,(i,j)
            count+=1
    return count

def build_report():
    b=[tuple(int(i==j) for j in range(4)) for i in range(4)]
    cases=[('W_R',b[0],b[1],1),('W_E',b[0],b[2],1),
           ('Bell_Phi',(1,0,0,1),(1,0,0,-1),2),('W_star',b[0],b[3],1)]
    bad=diag([F(1),F(1),F(1),F(0)])
    good=diag([F(1),F(1,2),F(1,3),F(1,4)])
    missing=diag([F(0),F(0),F(0),F(1)])
    assert add(bad,missing)==identity(4)
    rows=[]
    initial_delta=[F(0),F(0),F(1,5),F(-1,5)]
    for name,e0,eu,n in cases:
        count=channel_units(e0,eu,n)
        # Compute each entire state's effect probability from its column images.
        values={}
        for label,a in [('rank_deficient',bad),('full_support',good),
                        ('complete_menu',scale(F(1,2),add(bad,missing)))]:
            ps=[]
            for nums in ((1,1,2,1),(1,1,1,2)):
                z=[F(x,5) for x in nums]
                ps.append(z[1]*expectation(a,e0,n)+z[2]*expectation(a,eu,n))
            values[label]=str(ps[0]-ps[1])
            before=sum(initial_delta[j]*(expectation(a,b[0],1) if j==1 else 0) for j in range(4))
            assert before==0
        rows.append(dict(name=name,source_channel_units=count,initial_contrast='0',**values))
    assert rows[-1]['rank_deficient']=='0'
    assert min(good[i][i] for i in range(4))==F(1,4)
    assert rows[-1]['full_support']=='1/20'
    # Independent noncommuting family and spectral-support polynomial.
    a1=diag([F(1),F(0)]);a2=[[F(1,2),F(1,2)],[F(1,2),F(1,2)]]
    assert matmul(a1,a2)!=matmul(a2,a1)
    assert rank(a1)==rank(a2)==1
    require_full_support([a1,a2])
    S=scale(F(1,2),add(a1,a2));det=S[0][0]*S[1][1]-S[0][1]*S[1][0]
    assert S[0][0]+S[1][1]==1 and det==F(1,8) and S[0][0]>0
    poly=add(scale(F(8),S),scale(F(-8),matmul(S,S)))
    assert poly==identity(2)
    # Ambient 4-source, two-mode support: h(0)=0 outside the p block.
    ambient=[[F(0) for _ in range(8)] for _ in range(8)]
    P=[[F(0) for _ in range(8)] for _ in range(8)]
    for i in range(2):
        P[2+i][2+i]=F(1)
        for j in range(2):ambient[2+i][2+j]=S[i][j]
    assert add(scale(F(8),ambient),scale(F(-8),matmul(ambient,ambient)))==P
    rejected=[]
    for name,check in [
        ('rank_deficient_full_support',lambda:require_full_support([bad])),
        ('nonorthogonal_realization',lambda:channel_units(b[0],b[0],1)),
        ('corrupted_support_polynomial',lambda:assert_equal(add(scale(F(7),ambient),scale(F(-8),matmul(ambient,ambient))),P))]:
        try:check()
        except AssertionError:rejected.append(name)
        else:raise AssertionError('Mutation escaped: '+name)
    return dict(cases=rows,noncommuting=dict(individual_ranks=[rank(a1),rank(a2)],
        stacked_rank=rank(a1+a2),trace=str(S[0][0]+S[1][1]),determinant=str(det),
        spectral_support_polynomial='8t-8t^2',ambient_support_identity=True),
        rejected_controls=rejected,status='PASS',scope='fixed examples; analytical universal proof separate')
def assert_equal(a,b):assert a==b
def render_original_stdout(report):
    text=''
    for r in report['cases']:
        text+=r['name']+' source_channel='+str(r['source_channel_units'])+'/16 initial_contrast='+r['initial_contrast']
        for key in ('rank_deficient','full_support','complete_menu'):text+=' '+key+'='+r[key]
        text+='\n'
    text+='REJECTED: nonzero owner-supported effect implies universal separation\n'
    text+='PASS: fixed exact checks; no universal theorem inferred from enumeration\n'
    return text
if __name__=='__main__':
    print(json.dumps(build_report(),indent=2,sort_keys=True))
