"""Task 4: exact evidence-dependency audit and descriptive conditioning.

Conditioning diagnostics are read-only descriptions of the frozen operator.
They expose no threshold, regularizer, admissibility selector, or tuning input.
"""
from __future__ import annotations

from fractions import Fraction as Q
from math import cos, pi, sin
import sys

from evidence import V1543, actual_carriers
from factorization import compact_operator
from spectral import spectral_certificate, zero_modes


def _centered(values):
    return sum(values, Q(0)) == 0


def _proportional(left, right):
    if len(left) != len(right):
        raise ValueError("vector_dimension")
    if not left:
        raise ValueError("empty_vector")
    if not any(left):
        return not any(right)
    if not any(right):
        return False
    pivot = next(i for i, value in enumerate(left) if value)
    factor = right[pivot] / left[pivot]
    return all(b == factor * a for a, b in zip(left, right, strict=True))


def _apply(entries, values):
    return tuple(sum((a*b for a, b in zip(row, values, strict=True)), Q(0))
                 for row in entries)


def classify_pair_dependency(*, centered_injective, canonical_centered,
                             control_centered, input_proportional,
                             output_proportional):
    flags = (centered_injective, canonical_centered, control_centered,
             input_proportional, output_proportional)
    if any(type(flag) is not bool for flag in flags):
        raise ValueError("boolean_flags_required")
    eligible = centered_injective and canonical_centered and control_centered
    if eligible and not input_proportional and output_proportional:
        raise ValueError("injectivity_contradiction")
    if eligible and input_proportional and not output_proportional:
        raise ValueError("linearity_contradiction")
    if eligible and not input_proportional and not output_proportional:
        classification = "DEPENDENT_ON_CENTERED_INJECTIVITY"
    elif eligible and input_proportional and output_proportional:
        classification = "CONSISTENT_WITH_LINEARITY_AND_INJECTIVITY"
    else:
        classification = "NOT_FORCED_BY_INJECTIVITY"
    return {
        "classification": classification,
        "centered_injective": centered_injective,
        "canonical_centered": canonical_centered,
        "control_centered": control_centered,
        "input_proportional": input_proportional,
        "output_proportional": output_proportional,
    }


def conditioning_diagnostic(L):
    """Descriptive singular-scale diagnostic from the exact Fourier multiplier.

    Zero modes are selected symbolically by zero_modes(L), never by a floating
    threshold. Floating arithmetic is used only after the exact visible-mode
    set has been fixed.
    """
    certificate = spectral_certificate(L)
    zeros = {tuple(mode) for mode in zero_modes(L)}
    values = []
    for k in range(L):
        for ell in range(L):
            if (k, ell) in zeros:
                continue
            ck = cos(pi*k/L)
            cl = cos(pi*ell/L)
            sk = sin(pi*k/L)
            sl = sin(pi*ell/L)
            sigma = abs(2.0 * ck * cl * (sk*sk + sl*sl))
            if sigma <= 0.0:
                raise ValueError("visible_mode_nonpositive")
            values.append(sigma)
    if not values:
        raise ValueError("no_visible_modes")
    minimum, maximum = min(values), max(values)
    return {
        "schema": "uqcf-v1545-task4-conditioning-v1",
        "L": L,
        "role": "DESCRIPTIVE_ONLY",
        "centered_injective": certificate["centered_injective"],
        "exact_zero_mode_count": len(zeros),
        "visible_mode_count": len(values),
        "min_nonzero_response_scale": minimum,
        "max_response_scale": maximum,
        "condition_number": maximum / minimum,
        "inverse_min_scale": 1.0 / minimum,
        "operator_definition": "UNCHANGED_A=(I+X)(I+Y)Delta/8",
    }


def _projection():
    projection = sys.modules.get("projection")
    if projection is None:
        raise ValueError("projection_module_not_loaded")
    raw = (V1543 / "docs/INPUTS.json").read_bytes()
    return projection, projection.decode_projection(raw)


def archived_pair_dependency_audit():
    projection_module, projection = _projection()
    families = projection_module.FAMILY_KEYS
    carriers = {(carrier.L, carrier.scale): carrier for carrier in actual_carriers()}
    dependent = not_forced = centered_pairs = output_nonproportional = matrix_inequality = 0
    profile_claims_not_forced = 0
    by_carrier = []
    total = 0

    for payload in projection.payloads:
        key = (payload.L, payload.scale)
        carrier = carriers.get(key)
        if carrier is None:
            raise ValueError("carrier_coverage")
        operator = compact_operator(carrier)
        cert = spectral_certificate(payload.L)
        fields = {(field.family, field.response_index): field.values
                  for field in payload.fields}
        local_pairs = local_dependent = 0
        for index in range(payload.L * payload.L):
            canonical = fields[(families[0], index)]
            canonical_response = _apply(operator.entries, canonical)
            for family in families[1:]:
                control = fields[(family, index)]
                control_response = _apply(operator.entries, control)
                c_center = _centered(canonical)
                d_center = _centered(control)
                input_prop = _proportional(canonical, control)
                output_prop = _proportional(canonical_response, control_response)
                result = classify_pair_dependency(
                    centered_injective=cert["centered_injective"],
                    canonical_centered=c_center,
                    control_centered=d_center,
                    input_proportional=input_prop,
                    output_proportional=output_prop,
                )
                total += 1
                local_pairs += 1
                if c_center and d_center:
                    centered_pairs += 1
                if not output_prop:
                    output_nonproportional += 1
                    matrix_inequality += 1
                if result["classification"] == "DEPENDENT_ON_CENTERED_INJECTIVITY":
                    dependent += 1
                    local_dependent += 1
                else:
                    not_forced += 1
                # Injectivity does not determine equality of normalized
                # quadratic face-invariant profiles; keep that evidence separate.
                profile_claims_not_forced += 1
        by_carrier.append({
            "L": payload.L,
            "scale": str(payload.scale),
            "pairs": local_pairs,
            "dependent_pairs": local_dependent,
        })

    if total != 592:
        raise ValueError("pair_coverage")

    claim_dependency = {
        "response_nonproportionality": "DEPENDENT_ON_CENTERED_INJECTIVITY",
        "matrix_inequality": "DEPENDENT_ON_CENTERED_INJECTIVITY",
        "normalized_profile_inequality": "NOT_FORCED_BY_INJECTIVITY",
        "energy_difference": "NOT_FORCED_BY_INJECTIVITY",
        "face_invariant_differences": "NOT_FORCED_BY_INJECTIVITY",
        "norm_and_ratio_differences": "NOT_FORCED_BY_INJECTIVITY",
    }
    conditioning = tuple(conditioning_diagnostic(L) for L in (5, 7))
    return {
        "schema": "uqcf-v1545-task4-dependency-v1",
        "pair_count": total,
        "centered_pair_count": centered_pairs,
        "output_nonproportional_count": output_nonproportional,
        "matrix_inequality_dependent_count": matrix_inequality,
        "dependent_on_injectivity_count": dependent,
        "not_forced_count": not_forced,
        "normalized_profile_claims_not_forced_count": profile_claims_not_forced,
        "claim_dependency": claim_dependency,
        "by_carrier": tuple(by_carrier),
        "conditioning": conditioning,
        "source_correspondence": "NOT_EVALUATED",
        "operator_tuned": False,
        "threshold_used_for_scientific_gate": False,
    }
