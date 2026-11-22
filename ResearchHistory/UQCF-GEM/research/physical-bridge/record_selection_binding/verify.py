"""Replay the original actual-record primitive on the frozen P1 comparison."""
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[5]
SOURCE = "ResearchHistory/UQCF-GEM/v15/v15.11/ontology_continuity_audit.py"
BLOB = "8871e50f19322adbb62f34ea3837ba8e6cb16c8b"
TOL = 1e-14
Q = np.diag([1., 1., 0., 1.])
U = np.diag([0., 0., 1., 0.])
P = np.diag([0., 1., 0., 0.])


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def exact_outputs(z):
    q = 1-z[2]
    selected = [value/q if i != 2 else F(0) for i,value in enumerate(z)]
    pushed = list(z)
    pushed[1] += pushed[2]
    pushed[2] = F(0)
    return q, selected, pushed


def load_original():
    path = ROOT/SOURCE
    raw = path.read_bytes()
    blob = hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    require(blob == BLOB, "Original source changed")
    spec = importlib.util.spec_from_file_location("original_record_audit",path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run():
    original = load_original()
    cases = {
        "canonical_plus": [F(1,5),F(1,5),F(2,5),F(1,5)],
        "canonical_minus": [F(1,5),F(1,5),F(1,5),F(2,5)],
        "no_removed_population": [F(1,5),F(3,10),F(0),F(1,2)],
        "retained_parent_only": [F(0),F(2,5),F(3,5),F(0)],
    }
    rows = {}
    actual = {}
    for name,z in cases.items():
        require(sum(z)==1 and min(z)>=0,"Invalid frozen preparation")
        rho = np.diag([float(v) for v in z]).astype(complex)
        before = rho.copy()
        selected = original.select_record(rho,[Q,U],0)
        pinched = original.pinch(rho,[Q,U])
        benchmark = Q@rho@Q+rho[2,2]*P
        q, expected_selected, expected_benchmark = exact_outputs(z)
        errors = {
            "selected":float(np.max(np.abs(selected-np.diag(list(map(float,expected_selected)))))),
            "benchmark":float(np.max(np.abs(benchmark-np.diag(list(map(float,expected_benchmark)))))),
            "pinch":float(np.max(np.abs(pinched-rho))),
        }
        require(max(errors.values())<=TOL,"Full matrix comparison failed")
        require(np.array_equal(rho,before),"Original source routine changed its input")
        should_equal = name in ("no_removed_population","retained_parent_only")
        require(np.allclose(selected,benchmark,atol=TOL,rtol=0)==should_equal,
                "Equality criterion failed on a frozen case")
        rows[name]={"record_probability":str(q),
                    "selected_diagonal":list(map(str,expected_selected)),
                    "benchmark_diagonal":list(map(str,expected_benchmark)),
                    "operators_agree":should_equal,"maximum_absolute_errors":errors}
        actual[name]=(selected,pinched,benchmark)
    differences = {}
    for index,label in enumerate(("selected","nonselective","benchmark")):
        difference=float((actual["canonical_plus"][index][1,1]-actual["canonical_minus"][index][1,1]).real)
        expected={"selected":F(1,12),"nonselective":F(0),"benchmark":F(1,5)}[label]
        require(abs(difference-float(expected))<=TOL,"Parent contrast mismatch")
        differences[label]=str(expected)
    rejected={}
    for label,rho,record in (("zero_record_weight",U,0),("missing_record",np.eye(4)/4,None)):
        try:
            original.select_record(rho,[Q,U],record)
        except ValueError as error:
            rejected[label]=str(error)
        else:
            raise ValueError("An invalid actual-record request was accepted")
    eye=np.eye(4)
    require(np.array_equal(original.pinch(eye,[Q,U]),eye),"Pinching unitality failed")
    benchmark_identity=Q@eye@Q+eye[2,2]*P
    require(np.array_equal(benchmark_identity,np.diag([1.,2.,0.,1.])),"Benchmark image of identity changed")
    return {"status":"PASS","numpy":np.__version__,"source":SOURCE,"source_blob":BLOB,
            "basis":["o","p","u","v"],"cases":rows,"parent_contrasts":differences,
            "rejected_requests":rejected,"benchmark_identity_diagonal":[1,2,0,1],
            "absolute_tolerance":TOL,"scope":"local bounded source replay",
            "native_event_binding":"NOT_DERIVED","independent_review":"NOT_REQUESTED"}


if __name__ == "__main__":
    print(json.dumps(run(),indent=2,sort_keys=True))
