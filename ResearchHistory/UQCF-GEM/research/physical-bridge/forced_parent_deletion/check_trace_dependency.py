"""Replay a named source record and prior-edge read in the original trace caller."""
import ast
from copy import deepcopy
from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


SOURCE = "Tmp/TOE/Einstein 7/v1472_3_admissible_slice_geometry_corrected_package/v1472_3_admissible_slice_geometry_corrected.py"
BLOB = "797951f651014ce4b5bf753bb478dedfc0c0cabe"


def load_source():
    root = Path(__file__).resolve().parents[5]
    raw = (root / SOURCE).read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==BLOB
    tree = ast.parse(raw)
    defs = {"TraceEvent","SliceRecord","CausalGovernor","built_in_traces","load_events","run_trace"}
    constants = {"PASS_THRESHOLD","EPS","EVENT_TYPES","ENTROPY_INCREASE_TYPES","ENTROPY_DECREASE_TYPES"}
    selected = [node for node in tree.body
                if (isinstance(node,(ast.FunctionDef,ast.ClassDef)) and node.name in defs)
                or (isinstance(node,ast.Assign)
                    and any(isinstance(t,ast.Name) and t.id in constants for t in node.targets))]
    env = dict(globals())
    exec(compile(ast.Module(body=selected,type_ignores=[]),SOURCE,"exec",dont_inherit=True),env)
    return env


def close(a,b):
    assert math.isclose(a,b,rel_tol=0,abs_tol=1e-12)


def result_row(row):
    return {
        "event_id":row["event_id"],"admissible":row["admissible_slice"],
        "read":None if row["slice_coherence"] is None else round(row["slice_coherence"],12),
        "closure":round(row["C_closure"],12),
        "failures":row["failure_count_so_far"],
    }


def main():
    source = load_source()
    original = source["built_in_traces"]()["valid_pruning_order_trace"]
    alternative = deepcopy(original)
    alternative[0].update(entropy_after=0.2,state_delta=0.1)
    assert original[1:]==alternative[1:]
    read = source["run_trace"]
    initial = read("baseline",original)
    altered = read("source_after_changed",alternative)
    a,b = initial["slice_history"],altered["slice_history"]
    assert a[0]==b[0]
    assert all(r["admissible_slice"] for r in a+b)
    ars = []
    for trace, report, s in ((original,initial,0.1),(alternative,altered,0.2)):
        g=source["CausalGovernor"]()
        e=source["load_events"](trace)
        g.process_event(e[0],0)
        assert g.entropy_after_by_event=={"e0_source":s}
        assert g.edges==[]
        g.process_event(e[1],1)
        assert g.edges==[("e0_source","e1_disruption")]
        assert g.entropy_after_by_event["e1_disruption"]==0.75
        expected=math.exp(-(0.75-s)**2)
        close(g.slice_history[-1].slice_coherence,expected)
        assert asdict(g.slice_history[-1])==report["slice_history"][1]
        ars.append({"written_entropy_at_e0":s,"same_e1_entropy":0.75,
                    "e1_record":result_row(report["slice_history"][1]),
                    "final_record":result_row(report["slice_history"][-1])})
    assert a[1]["slice_coherence"]!=b[1]["slice_coherence"]

    rewire=deepcopy(original)
    rewire[3]["prior_dependency"]="e1_disruption"
    assert all(x==y for i,(x,y) in enumerate(zip(rewire,original)) if i!=3)
    rr=read("changed_repair_reference",rewire)
    assert rr["slice_history"][:3]==a[:3]
    ar=rr["slice_history"][3]
    assert ar["admissible_slice"] and a[3]["admissible_slice"]
    close(a[3]["slice_coherence"],math.exp(-227/1200))
    close(ar["slice_coherence"],math.exp(-97/600))
    close(a[3]["repaired_fraction"],0.5)
    close(ar["repaired_fraction"],0.5)

    controls=[]
    for key,value in (("prior_dependency","missing"),("provenance_id","P1")):
        bad = deepcopy(original)
        bad[1][key]=value
        g=source["CausalGovernor"]()
        for i,event in enumerate(source["load_events"](bad)[:2]):
            g.process_event(event,i)
        assert "e1_disruption" in g.active_event_ids
        assert g.entropy_after_by_event["e1_disruption"]==0.75
        assert g.slice_history[-1].slice_coherence is None
        assert not g.slice_history[-1].admissible_slice
        controls.append({"altered_field":key,"numeric_write_persists":True,"read_available":False,
                         "failure_reasons":g.failure_reasons})

    permuted=read("reordered_file",list(reversed(original)))
    assert permuted["slice_history"]==a
    print(json.dumps({
        "source_blob":BLOB,
        "matched_source_test":ars,
        "changed_valid_prior_test":{"original_repair_record":result_row(a[3]),
                                    "redirected_repair_record":result_row(ar)},
        "rejecting_controls":controls,
        "file_order_control_matches":True
    },indent=2,sort_keys=True))


if __name__=="__main__":
    main()
