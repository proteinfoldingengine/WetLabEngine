"""Exact exploratory typing lemmas. Not an engine, selected source law or CI certificate.

The quantum-to-cell input action is explicitly trivial under cell translations.
An addressed positive control is a NEW SUPPLIED RELATION, not recovered provenance.
"""
from __future__ import annotations
from fractions import Fraction as Q
from pathlib import Path
import json


def _period(L):
    if type(L) is not int or L < 3:
        raise ValueError('period_must_be_integer_at_least_three')
    return L


def _rational(x):
    if type(x) not in (int,Q):
        raise ValueError('exact_rational_required')
    return Q(x)


def rational_rank(matrix):
    if not isinstance(matrix,(tuple,list)) or not matrix or not matrix[0]:
        raise ValueError('nonempty_rectangular_matrix_required')
    n=len(matrix[0])
    if any(len(row)!=n for row in matrix):
        raise ValueError('rectangular_matrix_required')
    a=[[ _rational(x) for x in row] for row in matrix]
    pivot=0
    for col in range(n):
        selected=next((i for i in range(pivot,len(a)) if a[i][col]),None)
        if selected is None: continue
        a[pivot],a[selected]=a[selected],a[pivot]
        div=a[pivot][col]
        a[pivot]=[x/div for x in a[pivot]]
        for i in range(pivot+1,len(a)):
            scale=a[i][col]
            if scale:
                a[i]=[x-scale*y for x,y in zip(a[i],a[pivot],strict=True)]
        pivot+=1
        if pivot==len(a): break
    return pivot


def boundary_2(L):
    """Oriented face -> edge boundary on the periodic square.

    Edge blocks: east at (x,y), then north at (x,y); faces counterclockwise.
    """
    _period(L)
    n=L*L
    at=lambda x,y:(x%L)*L+y%L
    b=[[0]*n for _ in range(2*n)]
    for x in range(L):
        for y in range(L):
            f=at(x,y)
            b[at(x,y)][f]+=1
            b[n+at(x+1,y)][f]+=1
            b[at(x,y+1)][f]-=1
            b[n+at(x,y)][f]-=1
    return tuple(map(tuple,b))


def boundary_1(L):
    _period(L)
    n=L*L
    at=lambda x,y:(x%L)*L+y%L
    b=[[0]*(2*n) for _ in range(n)]
    for x in range(L):
        for y in range(L):
            i=at(x,y)
            b[i][i]-=1; b[at(x+1,y)][i]+=1
            b[i][n+i]-=1; b[at(x,y+1)][n+i]+=1
    return tuple(map(tuple,b))


def translate_edges(vector,L,dx,dy):
    _period(L)
    n=L*L
    if len(vector)!=2*n or type(dx) is not int or type(dy) is not int:
        raise ValueError('translation_dimension_or_type')
    result=[0]*(2*n)
    for axis in range(2):
        for x in range(L):
            for y in range(L):
                result[axis*n+((x+dx)%L)*L+(y+dy)%L]=vector[axis*n+x*L+y]
    return tuple(result)


def translation_certificate(L):
    b=boundary_2(L)
    n=L*L
    rank=rational_rank(b)
    # Omit one column: the remaining face boundaries are an independent basis.
    basis=tuple(tuple(row[:-1]) for row in b)
    if rank != n-1 or rational_rank(basis)!=rank:
        raise ValueError('unexpected_boundary_rank')
    constraints=[]
    for dx,dy in ((1,0),(0,1)):
        shifted_columns=[translate_edges(col,L,dx,dy) for col in zip(*basis)]
        shifted=tuple(zip(*shifted_columns))
        constraints.extend(tuple(x-y for x,y in zip(a,c,strict=True))
                           for a,c in zip(shifted,basis,strict=True))
    constraint_rank=rational_rank(tuple(constraints))
    return {'L':L,'boundary_rank':rank,'fixed_constraint_rank':constraint_rank,
            'fixed_boundary_dimension':rank-constraint_rank,
            'source_domain':'UNADDRESSED_INPUT_TRIVIAL_UNDER_CELL_TRANSLATIONS',
            'target':'IM_B2_NOT_ENTIRE_CYCLE_SPACE','arithmetic':'EXACT_RATIONAL'}


def twirl_matrix_unit(n,i,j):
    """Average X^a Z^b E_ij Z^b X^a exactly, including all product Paulis.

    Y differs from XZ by a phase, which cancels in conjugation. This action is
    complex-linear, so checking matrix units also determines imaginary entries.
    """
    if type(n) is not int or not 1 <= n <= 6:
        raise ValueError('probe_qubit_count_one_through_six')
    d=2**n
    if type(i) is not int or type(j) is not int or not 0<=i<d or not 0<=j<d:
        raise ValueError('matrix_unit_index')
    result=[[Q(0)]*d for _ in range(d)]
    for a in range(d):
        for b in range(d):
            sign=(-1)**((b & (i^j)).bit_count())
            result[i^a][j^a]+=Q(sign,d*d)
    return tuple(map(tuple,result))


def addressed_boundary(L,face,amplitude):
    _period(L)
    if type(face) is not int or not 0<=face<L*L:
        raise ValueError('face_address')
    amplitude=_rational(amplitude)
    return tuple(amplitude*row[face] for row in boundary_2(L))


def run():
    count=0
    for n in (1,2,3):
        d=2**n
        for i in range(d):
            for j in range(d):
                expected=tuple(tuple(Q(int(i==j and r==c),d) for c in range(d))
                               for r in range(d))
                if twirl_matrix_unit(n,i,j)!=expected:
                    raise ValueError('twirl_identity')
                count+=1
    records=[translation_certificate(L) for L in (5,6,7,8)]
    if any(r['fixed_boundary_dimension']!=0 for r in records):
        raise ValueError('nonzero_translation_fixed_boundary')
    return {'schema':'uqcf-v1546-exploratory-typing-v1',
            'scope':'EXPLORATORY_TYPING_LEMMAS_NOT_FULL_V1546_CERTIFICATION',
            'twirl_matrix_units_checked':count,'translation_certificates':records,
            'linear_operator_only_gauge_map':'TRACE_CHANNEL_ONLY_UNDER_STATED_ASSUMPTIONS',
            'unaddressed_boundary_source':'ZERO_UNDER_INDEPENDENT_CELL_TRANSLATIONS',
            'addressed_control':'NONZERO_WITH_EXPLICITLY_SUPPLIED_FACE_RELATION',
            'physical_source_law_adopted':False,'new_native_joint_state_derived':False,
            'source_correspondence':'NOT_EVALUATED','Pillar_3':'OPEN'}

if __name__=='__main__':
    output=Path(__file__).with_name('TYPING_PROBE_RESULTS.json')
    output.write_text(json.dumps(run(),sort_keys=True,indent=2)+'\n',encoding='ascii')
    print(output.name)
