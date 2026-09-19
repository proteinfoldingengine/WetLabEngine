from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import json

REPO_ROOT = Path(__file__).resolve().parents[4]
BASE_SHA = "e495157b969a73dcc453a71d9f0710797ec26a28"

EVIDENCE = {
    "v13.10-hidden-completion": (
        REPO_ROOT / "ResearchHistory/UQCF-GEM/v13/v13.10/REPORT.md",
        "d5f0c12a881b707f098caa81e406a4d4610e35ef",
        ("IRREDUCIBLE RELATIVE TO THE CURRENT FROZEN LEDGER.",),
    ),
    "v13.23-qrsl": (
        REPO_ROOT / "ResearchHistory/UQCF-GEM/v13/v13.23/SUMMARY.json",
        "71f36888a8515aa703cd253e4550dff751c94441",
        ("IRREDUCIBLE_RELATIVE_TO_CURRENT_FROZEN_ONTOLOGY",),
    ),
    "v13.26-source-scale": (
        REPO_ROOT / "ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md",
        "9917085b211ca0e1f4737082227f55097cc72b66",
        ("RSCL is irreducible relative to the current frozen ontology.",),
    ),
    "v14.04-representation-link": (
        REPO_ROOT / "ResearchHistory/UQCF-GEM/v14/v14.04/REPORT.md",
        "e5d9566bfc86c801d2933e63453d1800f60a675b",
        ("REQUIRES_NEW_REPRESENTATION_LINK",),
    ),
    "v15.30-common-carrier": (
        REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/docs/RESULTS.json",
        "24179161a88428fac936dec933d59b97c9655037",
        ("NO_TYPED_COMMON_CARRIER",),
    ),
    "v15.33-weight-constraints": (
        REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.33-sector-weight-constraint-audit/docs/RESULTS.json",
        "5ff397efbb66851f4a9a602c417cafdf50e62757",
        ("FROZEN_CONSTRAINTS_LEAVE_ALL_9_RELATIVE_WEIGHTS_FREE",),
    ),
    "v15.35-locality": (
        REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.35-support-radius-locality/docs/RESULTS.json",
        "17a99eed9d9a36635b2fc47b79f8decf1e0ab52d",
        ("CANONICAL_LOCALITY_FILTRATION_EXISTS_BUT_RADIUS_UNDERIVED",),
    ),
    "v15.36-order-semigroup": (
        REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.36-order-semigroup-constraint/docs/RESULTS.json",
        "04835086df04423eaf51d1ea9344a2f4a117a46b",
        ("FROZEN_ORDER_SEMIGROUP_CONSTRAINTS_LEAVE_FUNCTION_UNSELECTED",),
    ),
    "v15.03-firewall": (
        REPO_ROOT / "docs/superpowers/specs/2026-09-13-v1503-graph-site-source-lift-design.md",
        "d7e7a081f1913a10cf545fbed5d5e0f6aade20fa",
        ("Prohibited selectors", "ADM/Einstein/gravity residuals", "physical time or entropy"),
    ),
}


def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(f"blob {len(raw)}".encode() + bytes([0]) + raw).hexdigest()


def verify_evidence() -> dict[str, str]:
    out = {}
    for key, (path, expected, phrases) in EVIDENCE.items():
        actual = git_blob(path)
        if actual != expected:
            raise ValueError(f"evidence drift: {key}: {actual}")
        text = path.read_text()
        missing = [p for p in phrases if p not in text]
        if missing:
            raise AssertionError(f"missing evidence phrase for {key}: {missing}")
        out[key] = actual
    return out


def manifest():
    return [
        {
            "key": "genesis_provenance_lineage",
            "typed_role": "origin_identity_and_provenance_certificate",
            "class": "TYPE_BLOCKED",
            "function_equation_rank": 0,
            "reason": "no certified natural map from provenance identity/carriers into current response-function law",
            "evidence": ["v13.23-qrsl", "v14.04-representation-link", "v15.30-common-carrier"],
        },
        {
            "key": "incidence_filling_atlas",
            "typed_role": "admissibility_and_consistency_certificate",
            "class": "FEASIBILITY_NOT_SELECTOR",
            "function_equation_rank": 0,
            "reason": "W1/W2/W3 and atlas consistency certify supplied realizations but carry no preference functional",
            "evidence": ["v13.10-hidden-completion", "v13.23-qrsl"],
        },
        {
            "key": "hidden_completion_higher_order_response",
            "typed_role": "source_conditioned_hidden_completion_response",
            "class": "IRREDUCIBLE_UPSTREAM_BRANCH",
            "function_equation_rank": 0,
            "reason": "same frozen ledger can produce different response jets",
            "evidence": ["v13.10-hidden-completion"],
        },
        {
            "key": "recoverability_order_cmi_fidelity",
            "typed_role": "ordering_error_and_scalar_recovery_structure",
            "class": "TYPE_BLOCKED",
            "function_equation_rank": 0,
            "reason": "no certified scalar/order-to-cycle-response-function map",
            "evidence": ["v13.23-qrsl", "v15.36-order-semigroup"],
        },
        {
            "key": "refinement_coarse_quotient_naturality",
            "typed_role": "fine_to_coarse_restriction_without_canonical_section",
            "class": "IRREDUCIBLE_UPSTREAM_BRANCH",
            "function_equation_rank": 0,
            "reason": "QRSL reverse section is noncanonical relative to frozen ontology",
            "evidence": ["v13.23-qrsl"],
        },
        {
            "key": "positivity_support_compatibility",
            "typed_role": "feasibility_of_supplied_realizations",
            "class": "FEASIBILITY_NOT_SELECTOR",
            "function_equation_rank": 0,
            "reason": "positivity/support/compatibility admit alternatives but do not rank them",
            "evidence": ["v13.23-qrsl", "v15.36-order-semigroup"],
        },
        {
            "key": "representation_links_common_carrier",
            "typed_role": "cross_carrier_intertwiner_or_common_parent",
            "class": "TYPE_BLOCKED",
            "function_equation_rank": 0,
            "reason": "required natural representation/common-carrier link is not certified",
            "evidence": ["v14.04-representation-link", "v15.30-common-carrier"],
        },
        {
            "key": "symmetry_covariance_commutant",
            "typed_role": "current_response_algebra_structure",
            "class": "TYPED_NONSELECTIVE",
            "function_equation_rank": 0,
            "reason": "symmetry fixes the commutant/sector algebra but not its response function",
            "evidence": ["v15.33-weight-constraints"],
        },
        {
            "key": "source_scale_projective_normalization",
            "typed_role": "positive_common_scale_gauge",
            "class": "GAUGE_ONLY",
            "function_equation_rank": 0,
            "reason": "absolute scale is gauge/irreducible and leaves relative response freedom",
            "evidence": ["v13.26-source-scale", "v15.33-weight-constraints"],
        },
        {
            "key": "composition_monoidal_semigroup",
            "typed_role": "closure_of_already_chosen_response_family",
            "class": "TYPED_NONSELECTIVE",
            "function_equation_rank": 0,
            "reason": "composition/semigroup laws preserve arbitrary already-chosen generator/function",
            "evidence": ["v15.36-order-semigroup"],
        },
        {
            "key": "locality_support_radius",
            "typed_role": "canonical_support_filtration_without_selected_radius",
            "class": "TYPED_NONSELECTIVE",
            "function_equation_rank": 0,
            "reason": "exact filtration exists but frozen hard-radius constraint count is zero",
            "evidence": ["v15.35-locality"],
        },
        {
            "key": "quantum_channel_cptp_no_signalling",
            "typed_role": "operator_channel_order_structure_on_other_carrier",
            "class": "TYPE_BLOCKED",
            "function_equation_rank": 0,
            "reason": "no certified Choi/CPTP/order identification of current cycle carrier",
            "evidence": ["v15.36-order-semigroup"],
        },
        {
            "key": "downstream_geometry_metric_curvature_holonomy_gr",
            "typed_role": "downstream_response_or_correspondence_observables",
            "class": "DOWNSTREAM_CIRCULAR_SELECTOR_PROHIBITED",
            "function_equation_rank": 0,
            "reason": "using downstream geometry/gravity quality to choose upstream f reverses derivational direction",
            "evidence": ["v15.03-firewall"],
        },
        {
            "key": "entropy_pruning_physical_time",
            "typed_role": "prohibited_prepruning_selector_family",
            "class": "ONTOLOGY_ORDER_PROHIBITED",
            "function_equation_rank": 0,
            "reason": "frozen pre-time ontology forbids entropy/pruning/physical-time insertion as upstream selector",
            "evidence": ["v15.03-firewall"],
        },
    ]


def audit() -> dict:
    pins = verify_evidence()
    rows = manifest()
    if len({r["key"] for r in rows}) != len(rows):
        raise AssertionError("duplicate manifest key")

    valid = {
        "TYPED_NONSELECTIVE",
        "TYPE_BLOCKED",
        "FEASIBILITY_NOT_SELECTOR",
        "GAUGE_ONLY",
        "IRREDUCIBLE_UPSTREAM_BRANCH",
        "DOWNSTREAM_CIRCULAR_SELECTOR_PROHIBITED",
        "ONTOLOGY_ORDER_PROHIBITED",
        "ACTUAL_FUNCTION_EQUATION",
        "UNRESOLVED",
    }
    if any(r["class"] not in valid for r in rows):
        raise AssertionError("unknown status class")
    if any(not r["evidence"] for r in rows):
        raise AssertionError("unbound candidate class")
    if any(e not in pins for r in rows for e in r["evidence"]):
        raise AssertionError("candidate references unpinned evidence")

    counts = {k: sum(r["class"] == k for r in rows) for k in valid}
    unresolved = counts["UNRESOLVED"]
    actual = [r for r in rows if r["class"] == "ACTUAL_FUNCTION_EQUATION"]
    combined_rank = sum(r["function_equation_rank"] for r in actual)

    v1533 = json.loads((REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.33-sector-weight-constraint-audit/docs/RESULTS.json").read_text())
    v1535 = json.loads((REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.35-support-radius-locality/docs/RESULTS.json").read_text())
    v1536 = json.loads((REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.36-order-semigroup-constraint/docs/RESULTS.json").read_text())

    prior_zero_rank_checks = {
        "v15.33_frozen_constraint_rank": v1533["frozen_constraint_rank"],
        "v15.35_frozen_hard_radius_constraint_count": v1535["frozen_hard_radius_constraint_count"],
        "v15.36_frozen_function_constraint_rank": v1536["frozen_function_constraint_rank"],
    }
    if any(prior_zero_rank_checks.values()):
        raise AssertionError(f"prior selector rank no longer zero: {prior_zero_rank_checks}")

    combination_closure = (
        combined_rank == 0
        and unresolved == 0
        and all(r["function_equation_rank"] == 0 for r in rows)
        and all(v == 0 for v in prior_zero_rank_checks.values())
    )

    if unresolved:
        status = "RESPONSE_SELECTOR_EXHAUSTION_UNRESOLVED"
    elif combined_rank > 0:
        status = "FROZEN_RESPONSE_SELECTOR_FOUND"
    else:
        status = "RESPONSE_FUNCTION_IRREDUCIBLE_RELATIVE_TO_AUDITED_FROZEN_ONTOLOGY"

    return {
        "version": "v15.37",
        "base_sha": BASE_SHA,
        "status": status,
        "candidate_class_count": len(rows),
        "resolved_candidate_class_count": len(rows) - unresolved,
        "unresolved_candidate_count": unresolved,
        "candidate_manifest": rows,
        "typed_nonselective_count": counts["TYPED_NONSELECTIVE"],
        "type_blocked_count": counts["TYPE_BLOCKED"],
        "feasibility_not_selector_count": counts["FEASIBILITY_NOT_SELECTOR"],
        "gauge_only_count": counts["GAUGE_ONLY"],
        "irreducible_upstream_count": counts["IRREDUCIBLE_UPSTREAM_BRANCH"],
        "downstream_circular_prohibited_count": counts["DOWNSTREAM_CIRCULAR_SELECTOR_PROHIBITED"],
        "ontology_order_prohibited_count": counts["ONTOLOGY_ORDER_PROHIBITED"],
        "frozen_actual_function_equation_count": len(actual),
        "combined_frozen_selector_rank": combined_rank,
        "prior_zero_rank_checks": prior_zero_rank_checks,
        "combination_closure_certified": combination_closure,
        "inherited_projective_function_dimension": 9,
        "surviving_projective_function_dimension": 9 - combined_rank,
        "synthetic_new_axiom_control": "F_PROPORTIONAL_TO_A",
        "synthetic_control_projective_dimension": 0,
        "synthetic_control_is_frozen": False,
        "exhaustiveness_scope": "AUDITED_FROZEN_CANDIDATE_FAMILIES_AND_CERTIFIED_TYPE_LINKS_ONLY",
        "absolute_no_future_principle_claimed": False,
        "reopen_if_new_frozen_typed_structure_discovered": True,
        "branch_stop_relative_to_audited_frozen_ontology": status == "RESPONSE_FUNCTION_IRREDUCIBLE_RELATIVE_TO_AUDITED_FROZEN_ONTOLOGY",
        "evidence_pins": pins,
        "new_source_semantics_axiom_added": False,
        "new_response_function_axiom_added": False,
        "new_representation_link_added": False,
        "response_function_selected": False,
        "coupling_solver_reopened": False,
        "gravity_observables_evaluated": False,
        "uses_holonomy_selector": False,
        "uses_newton_or_gr": False,
        "uses_metric_selector": False,
        "uses_pruning_as_selector": False,
        "uses_entropy_as_selector": False,
        "uses_physical_time": False,
        "scientific_breakthrough": False,
        "signal_of_life": False,
        "physical_gravity_derived": False,
        "Pillar_3": "OPEN",
        "next_required_object": "EXPLICIT_NEW_PRETIME_RESPONSE_FUNCTION_AXIOM_OR_NEWLY_DISCOVERED_TYPED_FROZEN_STRUCTURE",
    }


def canonical_json(result: dict) -> str:
    return json.dumps(result, indent=2, sort_keys=True) + "\n"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out")
    p.add_argument("--check")
    args = p.parse_args()
    text = canonical_json(audit())
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    if args.check and Path(args.check).read_text() != text:
        raise SystemExit("committed v15.37 result differs from regenerated audit")
    print(text, end="")


if __name__ == "__main__":
    main()
