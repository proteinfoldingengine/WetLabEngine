"""Verify the exact V1718 cyclic correction and its P1-interface obstruction."""
import ast
import hashlib
import json
from pathlib import Path
import numpy as np

ORIGINAL=Path("Tmp/TOE/Einstein_13_V1720 retained_bridge_core/v1718_complete.py")
ORIGINAL_BLOB="638e68d00762642d6b58f692e7a1747816752232"
N=8
G=0.17
TOL=1e-12

def load():
    raw=ORIGINAL.read_bytes()
    blob=hashlib.sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()
    assert blob==ORIGINAL_BLOB
    tree=ast.parse(raw)
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {"roll","native_T"}]
    assert {n.name for n in nodes}=={"roll","native_T"}
    env={"np":np}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(ORIGINAL),"exec"),env)
    return env

def K(q,x):
    return q*np.roll(x,1)-np.roll(q,1)*x

def matrix(native,q,g=G):
    eye=np.eye(N)
    return np.column_stack([native(e,q,g) for e in eye])

def main():
    env=load(); native=env["native_T"]; eye=np.eye(N); zero=np.zeros(N)
    images=[]
    for i in range(N):
        q=eye[i]; x=eye[(i-1)%N]
        expected=eye[i]
        np.testing.assert_allclose(K(q,x),expected,rtol=0,atol=TOL)
        np.testing.assert_allclose(native(x,q,G),x+G*expected,rtol=0,atol=TOL)
        images.append(K(q,x))
    image_rank=int(np.linalg.matrix_rank(np.column_stack(images)))
    assert image_rank==N

    x=np.arange(1.0,N+1)
    np.testing.assert_allclose(native(x,zero,G),x,rtol=0,atol=TOL)
    np.testing.assert_allclose(native(x,x,G),x,rtol=0,atol=TOL)

    profiles=(eye[0]+eye[2],2*eye[0])
    dets=[]; reads=[]
    for q in profiles:
        H=matrix(native,q)
        dets.append(float(np.linalg.det(H)))
        reads.append(float(np.linalg.norm(H@eye[3])))
    np.testing.assert_allclose(dets,[0.6889,0.66],rtol=0,atol=TOL)
    np.testing.assert_allclose(reads,[0.83,1.0],rtol=0,atol=TOL)
    assert profiles[0].sum()==profiles[1].sum()==2

    result={
      "original_path":str(ORIGINAL),
      "original_blob":ORIGINAL_BLOB,
      "dimension":N,
      "cyclic_basis_image_rank":image_rank,
      "basis_images_equal_standard_basis":True,
      "full_update_collisions":{"T_x_0_equals_x":True,"T_x_x_equals_x":True},
      "matched_source_totals":[2.0,2.0],
      "loop_determinants":[round(v,12) for v in dets],
      "existing_norm_reads":[round(v,12) for v in reads],
      "conclusion":"no_nonzero_output_covector_annihilates_the_correction_image"
    }
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
