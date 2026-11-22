"""Check a fixed second port against every exact one-port lookalike."""
from fractions import Fraction
import json
from pathlib import Path
import check_bracket_ports as native

here = Path(__file__).resolve().parent
result = json.loads((here/"evidence/two_prunes/result.json").read_text())
archived = json.loads((here/"evidence/same_port/bracket.json").read_text())["archived"]
source = native.original_functions(here.parents[4]/native.HISTORICAL_PATH)
inputs = source["build_base"]()["branches"][1:]
out = {}
for arm, target in (("B3","q4"),("B4","q3")):
    slopes = [Fraction(rec["right_operand_scaled_by_21"][2],7)
              for rec in result[arm]["scalar_hits"]]
    expected = 3*Fraction(archived[target][2])
    assert slopes and expected not in slopes
    unique = {tuple(s["right_operand_scaled_by_21"]) for s in result[arm]["scalar_hits"]}
    positive = []
    for hit in result[arm]["scalar_hits"]:
        fields = [list(map(int, v)) for v in inputs]
        grades = []
        for index, u, p in hit["edits"]:
            grades.append(fields[index][u])
            fields[index][p] += fields[index][u]
            fields[index][u] = 0
        if min(grades)>0:
            positive.append({"edits":hit["edits"],"removed_grades_at_edits":grades})
    out[arm] = {"target_slope":str(expected),"checked":len(slopes),
                "distinct_lookalike_slopes":list(map(str,sorted(set(slopes)))),
                "distinct_complete_operands":len(unique),"positive_transfer_count":len(positive),
                "first_positive_transfer":positive[0],
                "minimum_absolute_gap":str(min(abs(s-expected) for s in slopes))}
print(json.dumps(out,indent=2,sort_keys=True))
