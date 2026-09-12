#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/"SUMMARY.json").read_text())
assert s["version"]=="v13.22"
e=s["executed_controls"]
assert e["coarse_restriction_error"]<1e-12
assert e["retained_observable_error"]<1e-12
assert e["ETL_naturality_error"]<1e-9
assert e["composition_error"]<1e-12
assert e["fine_trace_distance_between_two_admissible_lifts"]>0.1
assert e["max_one_two_body_ancilla_marginal_difference"]<1e-12
assert e["tau_epsilon_CMI"]>1e-3
rows=s["RATS_circularity_theorem"]["executed_scaling_rows"]
assert max(abs(x["measured_CMI_exponent"]-x["asymptotic_expected"]) for x in rows)<0.01
a=s["adjudication"]
assert a["canonical_refinement_derived"] is False
assert a["current_axioms_select_unique_member"] is False
assert a["RATS_execution_permitted"] is False
assert s["status"]["scientific_breakthrough"] is False
print("V13_22_CHECKER_PASS")
