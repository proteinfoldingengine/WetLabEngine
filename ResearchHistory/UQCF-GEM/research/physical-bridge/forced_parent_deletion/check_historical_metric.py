"""Test the original V498 edge functional on the two original fixed B carriers."""
import gzip
import hashlib
import importlib.util
import json
import math
from fractions import Fraction
from pathlib import Path

import networkx as nx
import numpy as np

HERE = Path(__file__).resolve().parent
NATIVE = HERE.parents[2]
ROOT = NATIVE.parents[1]
HISTORICAL = "Tmp/TOE/v498_retained_geometry_formal_report_package/v498_retained_geometry_proof.py"
PIN = "1b30d2f5f501e85020e0071544a9126dad074aaa"
ARCHIVE = NATIVE / "demos/v16.48-recursive-chain-repair/evidence/science/scientific/CERTIFICATE.json.gz"


def read_checked(path, sha):
    data = path.read_bytes()
    assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest() == sha
    return data


def archive_context(entry):
    states = entry["graph"]["states"]
    prep_id, after_id = 14730,14725
    assert states[prep_id]==[257,63,455] and states[after_id]==[257,63,199]
    hits = []
    def register(row, future, arriving):
        record = entry["normalizations"][row]
        assert future[0] == after_id
        receiver = [int(bool(states[s][1] & 128)) for s in future]
        hits.append({"row":row,"source_arrival":arriving,"root_target":record["q"][0],
                     "suffix":future,"first_B7_at_relative_edit":next((i for i,a in enumerate(receiver) if a),None)})
    for i,row in enumerate(entry["normalizations"]):
        path = row["path"]
        for j,(before,after) in enumerate(zip(path,path[1:])):
            if (before,after)==(prep_id,after_id):
                register(i,path[j+1:],"inside_running_normalizer")
        if row["state"] == after_id:
            register(i,path,"fresh_representative")
    assert [(v["row"],v["root_target"],len(v["suffix"])-1,v["first_B7_at_relative_edit"]) for v in hits] == [
        (2,1,8,None),(29,2,32,26),(31,2,32,26),(33,2,10,1)]
    assert len({tuple(v["suffix"]) for v in hits})==3
    return hits


def metric_weights(code, parent, mask):
    g=nx.Graph()
    kept=[i for i in range(len(parent)) if mask & (1<<i)]
    g.add_nodes_from(kept)
    g.add_edges_from((parent[v],v) for v in kept if v)
    zeros=np.zeros(len(kept))
    ones=np.ones(len(kept))
    model=code.effective_metric_and_predictions
    model(g,{"T":ones*(1+code.eps),"C_surplus":ones,"L":ones,"R":ones,
             "Lambda":zeros,"Pi":zeros,"conductance":code.conductance_proxy(g)},"matched_constant_fields")
    degrees=dict(g.degree)
    low,high=min(degrees.values()),max(degrees.values())
    exact_conductance={k:Fraction(1,5)+Fraction(4,5)*Fraction(v-low,high-low) for k,v in degrees.items()}
    def node(k):
        return Fraction(5,4)+Fraction(1,4)/(exact_conductance[k]+Fraction(1,20))
    for u,v in g.edges:
        predicted=(node(u)+node(v))/2
        assert math.isclose(g[u][v]["g_eff_weight"],float(predicted),rel_tol=0,abs_tol=1e-13)
    return (node(0)+node(1))/2


def main():
    path=ROOT/HISTORICAL
    read_checked(path,PIN)
    spec=importlib.util.spec_from_file_location("historical_v498",path)
    code=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(code)
    archive=read_checked(ARCHIVE,"ff8244239fb5ce092b07cbe775382593018b256d")
    entry=json.loads(gzip.decompress(archive))["entries"][1]
    parent=entry["graph"]["parents"]
    assert parent==[-1,0,1,2,3,3,2,1,0]
    states=entry["graph"]["states"]
    low,high=([states[j] for j in entry["normalizations"][i]["path"]] for i in (2,33))
    left=[metric_weights(code,parent,s[1]) for s in low]
    right=[metric_weights(code,parent,s[1]) for s in high]
    assert left==[Fraction(101,52)]*11 and right==[Fraction(101,52)]+[Fraction(157,84)]*10
    assert high[-1]==[257,199,63]
    high_other=metric_weights(code,parent,high[-1][2])
    assert high_other==left[-1]!=right[-1]
    union=metric_weights(code,parent,511)
    assert union==Fraction(1705,1092)
    assert left[-1]-right[-1]==Fraction(20,273)
    print(json.dumps({"same_edge":[0,1],"B_weight_during_A_removal":list(map(str,left)),
                      "B_weight_during_C_removal":list(map(str,right)),
                      "C_weight_at_same_C_removal_endpoint":str(high_other),
                      "B_low_minus_high":str(left[-1]-right[-1]),
                      "common_union_weight_both_histories":str(union),
                      "background":"L=R=1; stress/surplus+epsilon=1; Lambda=Pi=0",
                      "same_full_source_event_contexts":archive_context(entry)},sort_keys=True,indent=2))


if __name__=="__main__":
    main()
