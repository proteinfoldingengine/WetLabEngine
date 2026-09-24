"""Deterministic fail-closed v15.45 scientific ledger."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from dependency_audit import archived_pair_dependency_audit
from source_firewall import audit_source_relations
from spectral import spectral_certificate


STATUS = "FACTORIZATION_CERTIFIED_WITH_EXPLICIT_SPECTRAL_BOUNDARY"


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")


def _spectral_summary():
    result = {}
    for L in (5,6,7,8):
        c = spectral_certificate(L)
        result["L"+str(L)] = {
            "rank": c["rank"], "nullity": c["nullity"],
            "centered_nullity": c["centered_nullity"],
            "centered_injective": c["centered_injective"],
            "domain": c["domain"],
        }
    return result


def audit():
    dependency = archived_pair_dependency_audit()
    firewall = audit_source_relations()
    result = {
        "schema": "uqcf-v1545-results-v1",
        "status": STATUS,
        "factorization": {
            "operator": "A=(I+X)(I+Y)Delta/8",
            "archived_carriers": ["L5_scale1","L5_scale7/3","L7_scale1","L7_scale7/3"],
            "presentation_covariance": "CERTIFIED_TASK2",
        },
        "spectral_boundary": _spectral_summary(),
        "evidence_dependency": {
            "pairs": dependency["pair_count"],
            "dependent_response_nonproportionality": dependency["dependent_on_injectivity_count"],
            "independent_response_nonproportionality": dependency["not_forced_count"],
            "normalized_profile_comparison": "NOT_FORCED_BY_INJECTIVITY",
            "conditioning": list(dependency["conditioning"]),
            "threshold_used_for_scientific_gate": dependency["threshold_used_for_scientific_gate"],
        },
        "source_firewall": {
            "canonical_identity": "A_phi=ONE_HALF_M_s",
            "classification": "DEPENDENT_BY_CONSTRUCTION",
            "families": list(firewall["families"]),
            "upstream_response_generation_blob": firewall["upstream_response_generation_blob"],
        },
        "claims": {
            "source_correspondence": "NOT_EVALUATED",
            "physical_metric": False,
            "physical_curvature": False,
            "physical_gravity": False,
            "stress_energy": False,
            "einstein_equations": False,
            "continuum_limit": False,
            "spacetime": False,
            "foundational_uniqueness": False,
            "scientific_breakthrough": False,
            "fundamental_time_introduced": False,
            "dark_matter_primitive_introduced": False,
            "Pillar_3": "OPEN",
        },
        "interpretation": "FINITE_DISCRETE_OPERATOR_CHARACTERIZATION_WITH_EXPLICIT_SPECTRAL_BOUNDARY",
    }
    verify_result(result)
    return result


def verify_result(result):
    if type(result) is not dict or result.get("schema") != "uqcf-v1545-results-v1":
        raise ValueError("ledger_schema")
    if result.get("status") != STATUS:
        raise ValueError("adjudication")
    spectral = result.get("spectral_boundary")
    expected = {"L5":(24,1,0,True),"L6":(24,12,11,False),
                "L7":(48,1,0,True),"L8":(48,16,15,False)}
    if type(spectral) is not dict or set(spectral) != set(expected):
        raise ValueError("spectral_coverage")
    for key, values in expected.items():
        item = spectral[key]
        got = (item.get("rank"),item.get("nullity"),item.get("centered_nullity"),
               item.get("centered_injective"))
        if got != values:
            raise ValueError("spectral_boundary")
    evidence = result.get("evidence_dependency", {})
    if (evidence.get("pairs"), evidence.get("dependent_response_nonproportionality"),
        evidence.get("independent_response_nonproportionality")) != (592,592,0):
        raise ValueError("evidence_dependency")
    if evidence.get("threshold_used_for_scientific_gate") is not False:
        raise ValueError("conditioning_tuned")
    firewall = result.get("source_firewall", {})
    if (firewall.get("canonical_identity") != "A_phi=ONE_HALF_M_s" or
        firewall.get("classification") != "DEPENDENT_BY_CONSTRUCTION"):
        raise ValueError("source_firewall")
    claims = result.get("claims", {})
    if claims.get("source_correspondence") != "NOT_EVALUATED" or claims.get("Pillar_3") != "OPEN":
        raise ValueError("claim_boundary")
    forbidden_true = ("physical_metric","physical_curvature","physical_gravity","stress_energy",
                      "einstein_equations","continuum_limit","spacetime",
                      "foundational_uniqueness","scientific_breakthrough",
                      "fundamental_time_introduced","dark_matter_primitive_introduced")
    if any(claims.get(key) is not False for key in forbidden_true):
        raise ValueError("forbidden_claim")
    return True


def main():
    parser=argparse.ArgumentParser()
    choice=parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--out",type=Path)
    choice.add_argument("--check",type=Path)
    args=parser.parse_args()
    raw=canonical_bytes(audit())
    if args.out:
        args.out.write_bytes(raw)
    elif args.check.read_bytes()!=raw:
        raise SystemExit("canonical replay mismatch")
    print(STATUS)


if __name__=="__main__":
    main()
