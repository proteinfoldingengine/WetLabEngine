"""Audit the frozen minimum-completion record with exact roots and rejection controls.

Run this file beside check_minimal_completion.py. It checks the archived integer
records and exercises rational sources. The original proof and checker are pinned.
"""
import gzip
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import check_minimal_completion as frozen

HERE = Path(__file__).resolve().parent
ARCHIVE = HERE / "evidence/minimal_completion/result.json.gz"
RESULT_DIGEST = "99145e89948a91a3d92bbc8c0b3f41170f4d7ecf41eed9bf75ae15ee6b928998"
FROZEN_BLOB = "5e2d136c0e1bb092d9d92fcf187c0f792a717631"


def read_root(state, source, engine):
    """Return the exact rational P1 root, cross-checked by ancestral retraction."""
    carrier = frozen.chain.view(state[frozen.B])
    native = engine.push(frozen.P, frozen.X, carrier, source)
    rational_source = tuple(Fraction(x) for x in source)
    if tuple(native) != frozen.independent_push(carrier, rational_source):
        raise ValueError("native and ancestral pushes disagree")
    return native[carrier.index(0)]


def encode(value):
    """JSON stores exact integers as numbers and other rationals as p/q strings."""
    q = Fraction(value)
    return q.numerator if q.denominator == 1 else str(q)


def validate_claim(state, root, source, domain, minimum, engine):
    if state not in domain:
        raise ValueError("outside domain")
    if frozen.size(state) != minimum:
        raise ValueError("endpoint is not minimal")
    if type(root) not in (str, int) or root != encode(read_root(state, source, engine)):
        raise ValueError("incorrect exact root")


def reject(expected, validator, *args):
    try:
        validator(*args)
    except ValueError as error:
        if str(error) != expected:
            raise AssertionError(f"unexpected rejection: {error}") from error
        return str(error)
    raise AssertionError(f"corruption accepted: {expected}")


def integer_replay(arm, record, engine):
    grades = {
        "unit": (1,) * 9,
        "positive0": (2,) * 9,
        "positive1": (1, 2, 2, 2, 2, 2, 2, 2, 3),
        "zero_source": (1,) * 8 + (0,),
        "negative_source": (1,) * 8 + (-1,),
    }
    paths = {
        "minimum_root": record["minimum_states"],
        "path_root": record["constructed_positive_path"],
        "blind_path_root": record["original_factor_blind_path"],
    }
    count = 0
    for label, source in grades.items():
        for output, states in paths.items():
            readouts = [encode(read_root(state, source, engine)) for state in states]
            assert readouts == record["grades"][label][output], (arm, label, output)
            assert all(type(root) is int for root in readouts)
            count += len(readouts)
    return count


def main():
    if not __debug__:
        raise ValueError("run without Python optimization to enable all checks")
    frozen.old.pins()
    assert frozen.old.blob((HERE / "check_minimal_completion.py").read_bytes()) == FROZEN_BLOB
    raw = gzip.decompress(ARCHIVE.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == RESULT_DIGEST
    report = json.loads(raw)
    engine = frozen.chain.module("v16.23-overlap-descent/engine.py", "corrected_minimum_p1")
    domains = {}
    minima = {}
    accepted_integer_roots = {}
    for arm, record in report["domains"].items():
        domain = set(frozen.support_reconstruction(frozen.Q[arm]))
        frozen.check_universe(list(map(tuple, record["states"])), domain)
        minimum = min(map(frozen.size, domain))
        assert set(map(tuple, record["minimum_states"])) == {s for s in domain if frozen.size(s) == minimum}
        domains[arm] = domain
        minima[arm] = minimum
        accepted_integer_roots[arm] = integer_replay(arm, record, engine)

    cases = {
        "reviewer_positive_half": (1,) * 8 + (Fraction(1, 2),),
        "signed_fractional": (Fraction(-2, 3),) + (0,) * 7 + (Fraction(3, 5),),
        "positive_zero_contrast": (Fraction(1, 7),) + (2,) * 7 + (0,),
    }
    rational_records = {}
    for label, source in cases.items():
        roots = {}
        for arm, domain in domains.items():
            q0 = frozen.Q[arm][0]
            expected = source[0] + (q0 - 1) * source[8]
            rows = []
            for state in sorted(s for s in domain if frozen.size(s) == minima[arm]):
                root = read_root(state, source, engine)
                assert root == expected
                saved = json.loads(json.dumps(encode(root)))
                assert Fraction(saved) == root
                validate_claim(state, saved, source, domain, minima[arm], engine)
                rows.append({"state": state, "root": saved})
            roots[arm] = rows
        contrast = Fraction(roots["high"][0]["root"]) - Fraction(roots["low"][0]["root"])
        assert contrast == source[8]
        rational_records[label] = {"source": list(map(encode, source)), "roots": roots, "contrast": encode(contrast)}

    positive1 = (1, 2, 2, 2, 2, 2, 2, 2, 3)
    low_min = (1, 455, 1, 63)
    low_nonminimum = (1, 3, 455, 63)
    low = domains["low"]
    assert low_nonminimum in low and frozen.size(low_nonminimum) == 15
    validate_claim(low_min, 1, positive1, low, minima["low"], engine)
    rejects = {
        "in_domain_nonminimum": reject("endpoint is not minimal", validate_claim, low_nonminimum,
            encode(read_root(low_nonminimum, positive1, engine)), positive1, low, minima["low"], engine),
        "minimum_wrong_integer_root": reject("incorrect exact root", validate_claim, low_min,
            2, positive1, low, minima["low"], engine),
    }
    positive_half = cases["reviewer_positive_half"]
    high_min = (1, 199, 257, 63)
    old_high = frozen.read_root(high_min, positive_half, engine)
    old_low = frozen.read_root(low_min, positive_half, engine)
    assert (old_high, old_low) == (1, 1)
    rejects["legacy_truncated_fraction"] = reject("incorrect exact root", validate_claim, high_min,
        old_high, positive_half, domains["high"], minima["high"], engine)
    print(json.dumps({
        "verified_frozen_result_sha256": RESULT_DIGEST,
        "verified_frozen_result_bytes": len(raw),
        "frozen_checker_blob": FROZEN_BLOB,
        "archived_rejection_controls": report["corruption_rejections"],
        "additional_rejections": rejects,
        "integer_root_values_recomputed_exactly": accepted_integer_roots,
        "minimum_incidence": minima,
        "domain_sizes": {arm: len(domain) for arm, domain in domains.items()},
        "rational_cases": rational_records,
        "legacy_positive_half": {"high": old_high, "low": old_low, "contrast": old_high - old_low},
        "validation": "PASS",
        "native_bridge": "OPEN",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
