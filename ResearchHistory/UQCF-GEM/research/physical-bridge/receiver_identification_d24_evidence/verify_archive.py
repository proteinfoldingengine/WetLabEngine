"""Prepared, UNEXECUTED independent D24 range-archive validator (stdlib only).

No exporter import, LP solver, floating point, or supplied-universe inference.
Scientific reconstruction happens only through explicit function calls/main.
This source was prepared under a no-execution exception: it has NOT been run,
imported, tested, or certified. Future execution requires separate authorization.

CLI: python verify_archive.py PRODUCER_ARCHIVE CHECKER_ARCHIVE
         ORIGINAL_PRODUCER_JSON ORIGINAL_CHECKER_JSON REPORT_PATH
The report is deterministic, exclusively created, and never overwritten.
"""

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
import sys


SCHEMA_VERSION = "uqcf-rid24-range-certificates-v1"
CODE_SHA = "57895f62297c6100c1a4b8f185857a7905da780b"
RESULT_SHA256 = "7600ad3708baa287ac877afa582d83073a02f0ec72bf11d6ddcfbeb091ba43cc"
FREEZE_SHA256 = "a0bc94537c4dd008fd0e4349e7bfbc9b154707a63a67f6e8a7f9d5e5f3f4ebf1"
RUN_ID = 39300667905
ATTEMPT = 1
SOURCE_SHA256 = {
    "producer": "942ea9de0835849973046f0e6c079acb5c7e73fa04524eca289d7546bfd5d004",
    "checker": "2f7789a70113a08eaab4d9ce159245813bb1e982dd1971e8f646d999ea44dc2c",
}
SUMMARY_SHA256 = {
    "producer": "04be86d04551748dca905eb2aa2cac74977d86d7edd8f2aaa5d7db9ee411a9f9",
    "checker": "9bace24c70c57cd2c62a47e1f15ce1f01977a1c86e1ba3be9f752daa384a7572",
}
TOP_FIELDS = {
    "schema_version", "evidence_kind", "role", "basis", "origin",
    "exporter_sha256", "classes", "systems", "diagnostic", "legacy_summary_sha256",
}
ORIGIN_FIELDS = {
    "code_sha", "result_sha256", "freeze_sha256", "run_id", "attempt",
    "source_sha256", "summary_sha256",
}
ENDPOINT_FIELDS = {
    "target", "sense", "value", "primal", "ineq_multipliers", "eq_multipliers",
}


class ArchiveError(ValueError):
    """A specific schema, identity, arithmetic, coverage, or provenance failure."""


def require(condition, message):
    if not condition:
        raise ArchiveError(message)


def exact_fields(value, expected, label):
    require(type(value) is dict, label + ": expected object")
    require(set(value) == set(expected),
            label + ": fields differ (missing=" + repr(sorted(set(expected) - set(value)))
            + ", extra=" + repr(sorted(set(value) - set(expected))) + ")")


def exact_int(value, label):
    require(type(value) is int, label + ": expected exact integer, not bool/float/string")
    return value


def _duplicate_checked_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + repr(key))
        result[key] = value
    return result


def _forbidden_number(value):
    raise ArchiveError("non-integer JSON number is forbidden: " + value)


def strict_loads(raw):
    try:
        if type(raw) is bytes:
            raw = raw.decode("utf-8")
        require(type(raw) is str, "JSON input must be UTF-8 bytes or text")
        return json.loads(raw, object_pairs_hook=_duplicate_checked_object,
                          parse_float=_forbidden_number, parse_constant=_forbidden_number)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ArchiveError("invalid strict JSON: " + str(exc)) from exc


def parse_rational(value, label="rational"):
    require(type(value) is str, label + ": expected canonical rational string")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ArchiveError(label + ": invalid canonical rational string") from exc
    require(str(result) == value, label + ": noncanonical rational string " + repr(value))
    return result


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=False,
                       allow_nan=False) + "\n").encode("utf-8")


def write_new_json(path, payload):
    data = canonical_bytes(payload)
    with Path(path).open("xb") as stream:
        stream.write(data)


def pair(value, label):
    require(type(value) is list and len(value) == 2, label + ": expected [k,i]")
    k, i = (exact_int(value[0], label + " k"), exact_int(value[1], label + " i"))
    require(0 <= i <= k, label + ": requires 0 <= i <= k")
    return k, i


def parse_sparse_row(value, keys, label):
    require(type(value) is list and value, label + ": expected nonempty sparse row")
    allowed = set(keys)
    result = []
    for entry in value:
        require(type(entry) is list and len(entry) == 3,
                label + ": expected [k,i,integer_coefficient]")
        key = pair(entry[:2], label)
        coefficient = exact_int(entry[2], label + " coefficient")
        require(key in allowed, label + ": variable outside full class keys")
        require(coefficient != 0, label + ": zero coefficient forbidden")
        result.append((key, coefficient))
    require([key for key, _ in result] == sorted({key for key, _ in result}),
            label + ": duplicate or unordered variables")
    return tuple(result)


def tree_string(tree):
    return "(" + "".join(sorted(tree_string(child) for child in tree)) + ")"


def parse_carrier(value):
    require(type(value) is str and bool(value), "carriers: expected canonical tree string")

    def parse_at(index):
        require(index < len(value) and value[index] == "(", "carriers: invalid opening")
        index += 1
        children = []
        while index < len(value) and value[index] == "(":
            child, index = parse_at(index)
            children.append(child)
        require(index < len(value) and value[index] == ")", "carriers: invalid closing")
        return tuple(children), index + 1

    try:
        tree, end = parse_at(0)
    except RecursionError as exc:
        raise ArchiveError("carriers: excessively deep tree") from exc
    require(end == len(value) and tree_string(tree) == value,
            "carriers: malformed or noncanonical identity")
    return tree


def _normalized_tree(children):
    return tuple(sorted(children, key=tree_string))


def _trees_by_node_count(maximum):
    """Independent construction: partitions into multisets of smaller rooted trees.

    A root's children uniquely form a multiset with total size n-1. Nondecreasing
    candidate indices enumerate each multiset once. This never attaches a leaf
    to a preceding whole tree, unlike either original enumerator.
    """
    layers = {1: ((),)}
    for size in range(2, maximum + 1):
        candidates = sorted((n, tree_string(t), t)
                            for n in range(1, size) for t in layers[n])
        results = []

        def choose(remaining, start, selected):
            if remaining == 0:
                results.append(_normalized_tree(selected))
                return
            for index in range(start, len(candidates)):
                child_size, _, child = candidates[index]
                if child_size > remaining:
                    break
                choose(remaining - child_size, index, selected + (child,))

        choose(size - 1, 0, ())
        require(len(results) == len(set(results)), "internal duplicate multiset tree")
        layers[size] = tuple(sorted(results, key=tree_string))
    return layers


def _vertices(tree):
    """Represent vertices by root-to-vertex child-index paths, with root ()."""
    nodes = {}

    def visit(node, path):
        nodes[path] = tuple(path + (index,) for index in range(len(node)))
        for index, child in enumerate(node):
            visit(child, path + (index,))

    visit(tree, ())
    return nodes


def _dca_depth(path_a, path_b):
    depth = 0
    for a, b in zip(path_a, path_b):
        if a != b:
            break
        depth += 1
    return depth


def _clean_row(coefficients):
    return tuple(sorted((key, coefficient) for key, coefficient in coefficients.items()
                        if coefficient != 0))


def _to_nu(row):
    converted = {}
    for (k, i), coefficient in row:
        for index in range(i + 1):
            key = (k, index)
            converted[key] = converted.get(key, 0) + coefficient
    return _clean_row(converted)


def _holding_rows_a(trees):
    result = set()
    for tree in trees:
        vertices = _vertices(tree)
        for vertex, children in vertices.items():
            for source in vertices:
                row = {(len(vertex), _dca_depth(vertex, source)): 1}
                for child in children:
                    key = (len(child), _dca_depth(child, source))
                    row[key] = row.get(key, 0) - 1
                cleaned = _clean_row(row)
                if cleaned:
                    result.add(cleaned)
    return tuple(sorted(result))


def _comb_tree(depth, missing=None):
    trunk = ()
    for level in reversed(range(depth)):
        trunk = _normalized_tree((trunk,) if level == missing else (trunk, ()))
    return trunk


def _root_preserving_prunings(tree):
    """All downward closed retained vertex subsets, computed child-by-child.

    Each child is absent or replaced by one of its rooted prunings. This is
    independent of iterative leaf deletion and also covers the 9-node COMB_4.
    """
    choices = [(None,) + tuple(sorted(_root_preserving_prunings(child), key=tree_string))
               for child in tree]
    return {_normalized_tree(child for child in retained if child is not None)
            for retained in itertools.product(*choices)}


def _system_specs():
    result = {}

    def add(class_id, depths):
        for depth in depths:
            system_id = class_id + "|D=" + str(depth)
            require(system_id not in result, "internal duplicated system identity")
            result[system_id] = (class_id, depth)

    for n in (5, 6, 7, 8):
        add("BIN_" + str(n), range(1, n))
    for n in (7, 8):
        add("ALL_" + str(n), range(1, n))
    add("CH_7", range(1, 7))
    for depth in range(1, 5):
        add("COMB_" + str(depth), (depth,))
        for missing in range(depth):
            add("COMB_" + str(depth) + "-" + str(missing), (depth,))
    for branching, missing_depths, stop in ((2, range(5), 6), (3, range(4), 5)):
        for missing in missing_depths:
            add("K_" + str(branching) + "," + str(missing), range(missing + 1, stop))
    return dict(sorted(result.items()))


def reconstruct_domain():
    """Reconstruct the frozen universe, class identities, rows, and system set.

    This is scientific enumeration and must not be called during preparation.
    """
    layers = _trees_by_node_count(8)
    universes = {n: tuple(t for size in range(1, n + 1) for t in layers[size])
                 for n in (5, 6, 7, 8)}
    facts = {tree: _vertices(tree) for tree in universes[8]}

    def max_children(tree):
        return max(map(len, facts[tree].values()))

    classes = {}
    for n in (5, 6, 7, 8):
        classes["BIN_" + str(n)] = tuple(t for t in universes[n] if max_children(t) <= 2)
    for n in (7, 8):
        classes["ALL_" + str(n)] = universes[n]
    classes["CH_7"] = tuple(t for t in universes[7] if max_children(t) <= 1)
    for depth in range(1, 5):
        classes["COMB_" + str(depth)] = _root_preserving_prunings(_comb_tree(depth))
        for missing in range(depth):
            classes["COMB_" + str(depth) + "-" + str(missing)] = (
                _root_preserving_prunings(_comb_tree(depth, missing)))
    for branching, missing_depths in ((2, range(5)), (3, range(4))):
        for missing in missing_depths:
            classes["K_" + str(branching) + "," + str(missing)] = tuple(
                tree for tree in universes[7] if max_children(tree) <= branching
                and all(len(children) <= 1 for path, children in facts[tree].items()
                        if len(path) == missing))
    expected_classes = {}
    for class_id, trees in sorted(classes.items()):
        carriers = sorted(tree_string(tree) for tree in trees)
        require(len(carriers) == len(set(carriers)), "internal duplicated class carrier")
        maximum_depth = max(len(path) for tree in trees for path in _vertices(tree))
        keys = tuple((k, i) for k in range(maximum_depth + 1) for i in range(k + 1))
        a_rows = _holding_rows_a(trees)
        nu_rows = tuple(sorted({_to_nu(row) for row in a_rows}))
        expected_classes[class_id] = {
            "carriers": carriers, "keys": keys, "A": a_rows, "nu": nu_rows,
        }
    systems = _system_specs()
    targets = sum((depth + 1) * (depth + 2) // 2 for _, depth in systems.values())
    require(len(expected_classes) == 30 and len(systems) == 80 and targets == 1030,
            "internal frozen domain cardinality mismatch")
    return {"classes": expected_classes, "systems": systems}


def objective_row(target, basis):
    require(basis in ("A", "nu"), "unsupported basis")
    row = ((target, 1),)
    return row if basis == "A" else _to_nu(row)


def expected_equalities(depth, blind, basis):
    rows = [((((0, 0), 1),), Fraction(1))]
    if blind:
        for d in range(1, depth + 1):
            rows.append(((((d - 1, d - 1), -1), ((d, d), 1)), Fraction(0)))
    return tuple((row if basis == "A" else _to_nu(row), rhs) for row, rhs in rows)


def _rational_vector(value, length, label):
    require(type(value) is list and len(value) == length, label + ": vector length mismatch")
    return tuple(parse_rational(item, label + "[" + str(index) + "]")
                 for index, item in enumerate(value))


def _dot(row, point, indices):
    return sum((coefficient * point[indices[key]] for key, coefficient in row), Fraction(0))


def check_endpoint_identities(endpoints, targets):
    require(type(endpoints) is list, "endpoint identities: expected list")
    actual = []
    for endpoint in endpoints:
        exact_fields(endpoint, ENDPOINT_FIELDS, "endpoint fields")
        target = pair(endpoint["target"], "endpoint target")
        sense = exact_int(endpoint["sense"], "endpoint sense")
        require(sense in (1, -1), "endpoint identities: sense must be 1 or -1")
        actual.append((target, sense))
    expected = [(target, sense) for target in targets for sense in (1, -1)]
    require(actual == expected, "endpoint identities: missing, extra, duplicate, or reordered endpoint")


def check_endpoint(endpoint, basis, keys, rows, equalities, target, sense):
    """Check one exact certificate against independently supplied constraints.

    This small helper admits toy fixtures; it cannot establish full-archive
    identity/coverage. The full validator supplies only reconstructed constraints.
    """
    exact_fields(endpoint, ENDPOINT_FIELDS, "endpoint fields")
    require(pair(endpoint["target"], "endpoint target") == target, "endpoint target differs")
    actual_sense = exact_int(endpoint["sense"], "endpoint sense")
    require(actual_sense in (1, -1) and actual_sense == sense, "endpoint sense differs")
    value = parse_rational(endpoint["value"], "endpoint value")
    x = _rational_vector(endpoint["primal"], len(keys), "primal")
    lam = _rational_vector(endpoint["ineq_multipliers"], len(rows), "ineq_multipliers")
    mu = _rational_vector(endpoint["eq_multipliers"], len(equalities), "eq_multipliers")
    require(all(multiplier >= 0 for multiplier in lam), "negative inequality multiplier")
    indices = {key: index for index, key in enumerate(keys)}
    require(len(indices) == len(keys), "duplicate constraint variable")
    for row_index, row in enumerate(rows):
        require(_dot(row, x, indices) >= 0, "primal infeasible at POS row " + str(row_index))
    for eq_index, (row, rhs) in enumerate(equalities):
        require(_dot(row, x, indices) == rhs, "primal equality failure " + str(eq_index))
    objective = objective_row(target, basis)
    require(all(key in indices for key, _ in objective), "objective outside class keys")
    expected = [Fraction(0)] * len(keys)
    reconstructed = [Fraction(0)] * len(keys)
    for key, coefficient in objective:
        expected[indices[key]] += sense * coefficient
    for multiplier, row in zip(lam, rows):
        if multiplier:
            for key, coefficient in row:
                reconstructed[indices[key]] += multiplier * coefficient
    for multiplier, (row, _) in zip(mu, equalities):
        if multiplier:
            for key, coefficient in row:
                reconstructed[indices[key]] += multiplier * coefficient
    require(reconstructed == expected, "dual identity does not reconstruct signed objective")
    primal_objective = sense * _dot(objective, x, indices)
    dual_objective = sum((multiplier * rhs for multiplier, (_, rhs) in zip(mu, equalities)),
                         Fraction(0))
    require(primal_objective == dual_objective, "nonzero primal-dual gap")
    require(value == sense * primal_objective, "endpoint value differs from attained objective")
    return value


def sibling_exporter_sha256(role):
    require(role in SOURCE_SHA256, "unknown exporter role")
    return hashlib.sha256(Path(__file__).with_name(role + "_export.py").read_bytes()).hexdigest()


def load_original_summary(path, role):
    require(role in SUMMARY_SHA256, "unknown original summary role")
    raw = Path(path).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SUMMARY_SHA256[role],
            role + ": original summary SHA256 mismatch")
    return strict_loads(raw)


def _validate_original_summary_object(summary, role):
    # The original format is pinned: json.dump(indent=1, sort_keys=True), no LF.
    # Rechecking its exact serialization prevents object-level entry points from
    # treating caller-supplied, unpinned summary dictionaries as trusted evidence.
    require(type(summary) is dict, role + ": original summary must be object")
    try:
        original_bytes = json.dumps(summary, indent=1, sort_keys=True,
                                    allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ArchiveError(role + ": original summary serialization invalid") from exc
    require(hashlib.sha256(original_bytes).hexdigest() == SUMMARY_SHA256[role],
            role + ": original summary SHA256 mismatch")
    require(summary["role"] == role and summary["result_sha256"] == RESULT_SHA256,
            role + ": original summary role/result mismatch")


def _validate_header(archive, role, exporter_sha256):
    exact_fields(archive, TOP_FIELDS, "top-level fields")
    require(archive["schema_version"] == SCHEMA_VERSION, "schema_version mismatch")
    require(archive["evidence_kind"] == "regenerated", "evidence_kind must be regenerated")
    require(archive["role"] == role, "role mismatch")
    basis = "nu" if role == "producer" else "A"
    require(archive["basis"] == basis, "basis mismatch")
    origin = archive["origin"]
    exact_fields(origin, ORIGIN_FIELDS, "origin")
    exact_int(origin["run_id"], "origin run_id")
    exact_int(origin["attempt"], "origin attempt")
    expected = {
        "code_sha": CODE_SHA, "result_sha256": RESULT_SHA256,
        "freeze_sha256": FREEZE_SHA256, "run_id": RUN_ID, "attempt": ATTEMPT,
        "source_sha256": SOURCE_SHA256[role], "summary_sha256": SUMMARY_SHA256[role],
    }
    require(origin == expected, "origin identities differ from pinned original execution")
    require(type(exporter_sha256) is str and len(exporter_sha256) == 64
            and all(char in "0123456789abcdef" for char in exporter_sha256),
            "actual sibling exporter digest is malformed")
    require(archive["exporter_sha256"] == exporter_sha256,
            "exporter_sha256 differs from actual sibling exporter bytes")
    require(archive["legacy_summary_sha256"] == SUMMARY_SHA256[role],
            "legacy_summary_sha256 differs from pinned original")
    return basis


def _validate_class(value, expected, basis):
    exact_fields(value, {"carriers", "keys", "pos_rows"}, "class fields")
    carriers = value["carriers"]
    require(type(carriers) is list, "carriers must be list")
    for carrier in carriers:
        parse_carrier(carrier)
    require(carriers == expected["carriers"],
            "carriers differ from full reconstructed canonical identities/order")
    require(type(value["keys"]) is list, "keys must be list")
    keys = tuple(pair(key, "class keys") for key in value["keys"])
    require(keys == expected["keys"], "keys differ from complete ordered class basis")
    require(type(value["pos_rows"]) is list, "pos_rows must be list")
    rows = tuple(parse_sparse_row(row, keys, "pos_rows") for row in value["pos_rows"])
    require(rows == expected[basis],
            "pos_rows differ from full reconstructed identities/order")


def _validate_class_summary(summary, expected):
    require(type(summary["classes"]) is dict and set(summary["classes"]) == set(expected),
            "original summary class identities mismatch")
    for class_id, cls in expected.items():
        value = summary["classes"][class_id]
        exact_fields(value, {"carriers", "digest"}, "original summary class")
        exact_int(value["carriers"], "original summary carrier count")
        require(value["carriers"] == len(cls["carriers"]),
                "original summary carrier count mismatch: " + class_id)
        digest = hashlib.sha256("\n".join(cls["carriers"]).encode("utf-8")).hexdigest()
        require(value["digest"] == digest,
                "original summary reconstructed class digest mismatch: " + class_id)


def _validate_system_structure(value, class_id, depth, blind, targets, cls, basis):
    exact_fields(value, {"class_id", "D", "blind", "targets", "equalities", "endpoints"},
                 "system fields")
    require(value["class_id"] == class_id, "system class_id mismatch")
    require(exact_int(value["D"], "system D") == depth, "system D mismatch")
    require(type(value["blind"]) is bool and value["blind"] is blind, "system blind mismatch")
    require(type(value["targets"]) is list, "system targets must be list")
    actual_targets = tuple(pair(target, "system target") for target in value["targets"])
    require(actual_targets == targets, "system target identities/order mismatch")
    equalities = expected_equalities(depth, blind, basis)
    require(type(value["equalities"]) is list, "equalities must be list")
    parsed = []
    for equality in value["equalities"]:
        exact_fields(equality, {"row", "rhs"}, "equality fields")
        parsed.append((parse_sparse_row(equality["row"], cls["keys"], "equality row"),
                       parse_rational(equality["rhs"], "equality rhs")))
    require(tuple(parsed) == equalities, "equalities differ from full reconstructed constraints")
    check_endpoint_identities(value["endpoints"], targets)
    return equalities


def _record_check(errors, label, operation):
    try:
        return True, operation()
    except (ArchiveError, KeyError, TypeError, IndexError, RecursionError, OSError) as exc:
        errors.append(label + ": " + str(exc))
        return False, None


def _validate_one(archive, role, summary, exporter_sha256, expected, errors):
    coverage = {"classes": 0, "systems": 0, "targets": 0, "endpoints": 0}
    values = {}
    ok, basis = _record_check(errors, role, lambda: _validate_header(archive, role, exporter_sha256))
    if not ok:
        return coverage, values
    classes = expected["classes"]
    systems = expected["systems"]
    class_ok, _ = _record_check(errors, role + " classes", lambda: require(
        type(archive["classes"]) is dict and set(archive["classes"]) == set(classes),
        "class identities differ from full reconstructed class set"))
    if class_ok:
        for class_id, cls in classes.items():
            good, _ = _record_check(errors, role + " " + class_id,
                                   lambda: _validate_class(archive["classes"][class_id], cls, basis))
            coverage["classes"] += int(good)
    _record_check(errors, role + " original classes", lambda: _validate_class_summary(summary, classes))
    summary_ok, _ = _record_check(errors, role + " original ranges", lambda: require(
        type(summary["ranges"]) is dict and set(summary["ranges"]) == set(systems),
        "original summary system identities mismatch"))
    systems_ok, _ = _record_check(errors, role + " systems", lambda: require(
        type(archive["systems"]) is dict and set(archive["systems"]) == set(systems),
        "system identities differ from full reconstructed system set"))
    if systems_ok:
        for system_id, (class_id, depth) in systems.items():
            cls = classes[class_id]
            system = archive["systems"][system_id]
            targets = tuple((j, i) for j in range(depth + 1) for i in range(j + 1))
            label = role + " " + system_id
            good, equalities = _record_check(errors, label, lambda: _validate_system_structure(
                system, class_id, depth, True, targets, cls, basis))
            if not good:
                continue
            coverage["systems"] += 1
            summary_ranges = summary["ranges"].get(system_id, {}) if summary_ok else {}
            _record_check(errors, label + " original targets", lambda: require(
                type(summary_ranges) is dict
                and set(summary_ranges) == {"A(" + str(j) + "," + str(i) + ")" for j, i in targets},
                "original summary target identities mismatch"))
            for target_index, target in enumerate(targets):
                endpoints = []
                for sense_index, sense in enumerate((1, -1)):
                    endpoint = system["endpoints"][2 * target_index + sense_index]
                    certificate_ok, endpoint_value = _record_check(
                        errors, label + " target=" + repr(target) + " sense=" + str(sense),
                        lambda: check_endpoint(endpoint, basis, cls["keys"], cls[basis],
                                               equalities, target, sense))
                    coverage["endpoints"] += int(certificate_ok)
                    endpoints.append(endpoint_value if certificate_ok else None)
                if None not in endpoints:
                    coverage["targets"] += 1
                    values[(system_id, target)] = tuple(endpoints)
                    name = "A(" + str(target[0]) + "," + str(target[1]) + ")"

                    def compare_summary():
                        pair_values = summary_ranges.get(name)
                        require(type(pair_values) is list and len(pair_values) == 2,
                                "original summary range is not a pair")
                        parsed_values = tuple(parse_rational(v, "original range") for v in pair_values)
                        require(tuple(endpoints) == parsed_values,
                                "certificate range differs from original summary")
                        require(endpoints[0] <= endpoints[1], "range endpoints reversed")

                    _record_check(errors, label + " " + name, compare_summary)
    if role == "producer":
        def producer_summary_checks():
            require(summary.get("certified_exact") is True, "original producer was not certified_exact")
            expected_rows = {sid: len(classes[cid][basis]) for sid, (cid, _) in systems.items()}
            require(summary.get("rows") == expected_rows, "original producer row counts mismatch")
            require(summary.get("diagnostic_row_counts_total") == sum(expected_rows.values()),
                    "original producer total row count mismatch")
        _record_check(errors, role + " legacy checks", producer_summary_checks)
    else:
        def checker_summary_checks():
            require(type(summary.get("violations")) is int and summary["violations"] == 0,
                    "original checker violations not zero")
            expected_total = sum(len(classes[cid][basis]) for cid, _ in systems.values())
            require(summary.get("diagnostic_row_counts_total") == expected_total,
                    "original checker total row count mismatch")
        _record_check(errors, role + " legacy checks", checker_summary_checks)
    _validate_diagnostic(archive["diagnostic"], role, summary, classes["BIN_7"], basis, errors)
    return coverage, values


def _validate_diagnostic(value, role, summary, cls, basis, errors):
    if role == "producer":
        good, equalities = _record_check(errors, "producer diagnostic", lambda: _validate_system_structure(
            value, "BIN_7", 0, False, ((1, 0),), cls, basis))
        if not good:
            return
        endpoints = []
        for index, sense in enumerate((1, -1)):
            ok, result = _record_check(errors, "producer diagnostic sense=" + str(sense),
                                      lambda: check_endpoint(value["endpoints"][index], basis,
                                                             cls["keys"], cls[basis], equalities,
                                                             (1, 0), sense))
            endpoints.append(result if ok else None)
        if None not in endpoints:
            _record_check(errors, "producer diagnostic legacy", lambda: require(
                [str(x) for x in endpoints] == summary.get("diagnostic_nobl_BIN_7"),
                "diagnostic range differs from original summary"))
    else:
        def attainment():
            exact_fields(value, {"kind", "class_id", "target", "value", "primal"},
                         "checker diagnostic fields")
            require(value["kind"] == "attainment_only", "checker diagnostic must be attainment_only")
            require(value["class_id"] == "BIN_7", "checker diagnostic class_id mismatch")
            require(pair(value["target"], "checker diagnostic target") == (1, 0),
                    "checker diagnostic target mismatch")
            attained_value = parse_rational(value["value"], "checker diagnostic value")
            require(attained_value == Fraction(1, 2), "checker diagnostic value must be 1/2")
            point = _rational_vector(value["primal"], len(cls["keys"]), "checker diagnostic primal")
            indices = {key: index for index, key in enumerate(cls["keys"])}
            require(point[indices[(0, 0)]] == 1, "checker diagnostic normalization failure")
            require(all(_dot(row, point, indices) >= 0 for row in cls[basis]),
                    "checker diagnostic primal infeasible")
            require(_dot(objective_row((1, 0), basis), point, indices) == attained_value,
                    "checker diagnostic attainment failure")
            require(str(attained_value) == summary.get("diagnostic_nobl_BIN_7_attained_upper"),
                    "checker diagnostic differs from original attainment summary")
        _record_check(errors, "checker diagnostic", attainment)


def _base_report():
    return {
        "schema_version": "uqcf-rid24-range-validation-v1", "status": "RED",
        "evidence_kind": "regenerated", "original_code_sha": CODE_SHA,
        "original_result_sha256": RESULT_SHA256, "original_freeze_sha256": FREEZE_SHA256,
        "original_run_id": RUN_ID, "original_attempt": ATTEMPT,
        "original_summary_sha256": dict(SUMMARY_SHA256),
        "expected_coverage_per_role": {"classes": 30, "systems": 80, "targets": 1030, "endpoints": 2060},
        "coverage": {}, "cross_compared_ranges": 0,
        "diagnostic_scope": {"producer": "exact_range_certificate", "checker": "attainment_only"},
        "scope": "Frozen D24 range archive only; not original-run certificate recovery or full scientific closure",
        "errors": [],
    }


def validate_bundle_objects(producer, checker, original_producer, original_checker,
                            producer_export_sha, checker_export_sha):
    """Validate parsed archives against pinned summaries and actual exporter hashes.

    Every entry point re-hashes the actual sibling exporters and reconstructs the
    expected scientific domain itself. Caller digests are cross-checked, never
    trusted as substitutes. All summaries are independently re-pinned here.
    """
    report = _base_report()
    errors = report["errors"]
    originals = {"producer": original_producer, "checker": original_checker}
    archives = {"producer": producer, "checker": checker}
    digests = {"producer": producer_export_sha, "checker": checker_export_sha}
    actual_digests = {}
    report["exporter_sha256"] = actual_digests
    # Reject fake tiny metadata/summary inputs before any scientific enumeration.
    ready = {}
    for role in ("producer", "checker"):
        def check_actual_exporter():
            actual = sibling_exporter_sha256(role)
            actual_digests[role] = actual
            require(digests[role] == actual,
                    "caller exporter digest differs from actual sibling exporter bytes")
        exporter_good, _ = _record_check(errors, role + " exporter provenance", check_actual_exporter)
        good, _ = _record_check(errors, role + " original provenance",
                               lambda: _validate_original_summary_object(originals[role], role))
        original_good = good
        header_good, _ = _record_check(errors, role + " header",
                                      lambda: _validate_header(archives[role], role, digests[role]))
        ready[role] = original_good and header_good and exporter_good
    if not any(ready.values()):
        return report
    good, expected = _record_check(errors, "independent domain reconstruction", reconstruct_domain)
    if not good:
        return report
    all_values = {}
    for role in ("producer", "checker"):
        if ready[role]:
            coverage, values = _validate_one(archives[role], role, originals[role], digests[role], expected, errors)
        else:
            coverage, values = {"classes": 0, "systems": 0, "targets": 0, "endpoints": 0}, {}
        report["coverage"][role] = coverage
        all_values[role] = values
        _record_check(errors, role + " complete coverage", lambda: require(
            coverage == report["expected_coverage_per_role"], "verified identity/coverage counts incomplete"))
    producer_values, checker_values = all_values["producer"], all_values["checker"]
    expected_range_keys = {(sid, (j, i)) for sid, (_, depth) in expected["systems"].items()
                           for j in range(depth + 1) for i in range(j + 1)}
    _record_check(errors, "cross-role range identities", lambda: require(
        set(producer_values) == expected_range_keys == set(checker_values),
        "full reconstructed target sets were not both certified"))
    for key in sorted(set(producer_values) & set(checker_values)):
        if producer_values[key] != checker_values[key]:
            errors.append("cross-role range mismatch: " + repr(key))
        else:
            report["cross_compared_ranges"] += 1
    if not errors:
        report["status"] = "VERIFIED"
    return report


def validate_files(producer_path, checker_path, original_producer_path, original_checker_path):
    report = _base_report()
    archives = {}
    summaries = {}
    exporter_hashes = {}
    for role, archive_path, original_path in (
        ("producer", producer_path, original_producer_path),
        ("checker", checker_path, original_checker_path),
    ):
        def read_archive():
            raw = Path(archive_path).read_bytes()
            value = strict_loads(raw)
            require(raw == canonical_bytes(value), "archive bytes are not canonical deterministic JSON")
            return value
        try:
            archives[role] = read_archive()
        except (OSError, ArchiveError, ValueError) as exc:
            report["errors"].append(role + " archive read: " + str(exc))
        try:
            summaries[role] = load_original_summary(original_path, role)
        except (OSError, ArchiveError) as exc:
            report["errors"].append(role + " original summary read: " + str(exc))
        try:
            exporter_hashes[role] = sibling_exporter_sha256(role)
        except (OSError, ArchiveError) as exc:
            report["errors"].append(role + " exporter read: " + str(exc))
    if report["errors"]:
        return report
    return validate_bundle_objects(archives["producer"], archives["checker"],
                                   summaries["producer"], summaries["checker"],
                                   exporter_hashes["producer"], exporter_hashes["checker"])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("producer_archive")
    parser.add_argument("checker_archive")
    parser.add_argument("original_producer_json")
    parser.add_argument("original_checker_json")
    parser.add_argument("report_path")
    arguments = parser.parse_args(argv)
    report_path = Path(arguments.report_path)
    # Refuse before scientific work, including broken symlinks and input aliases.
    if report_path.exists() or report_path.is_symlink():
        parser.error("refusing to overwrite report path: " + str(report_path))
    if not report_path.parent.is_dir():
        parser.error("report parent does not exist or is not a directory: " + str(report_path.parent))
    inputs = (arguments.producer_archive, arguments.checker_archive,
              arguments.original_producer_json, arguments.original_checker_json)
    if any(report_path.resolve() == Path(path).resolve() for path in inputs):
        parser.error("report path must not alias any input")
    report = validate_files(arguments.producer_archive, arguments.checker_archive,
                            arguments.original_producer_json, arguments.original_checker_json)
    try:
        write_new_json(report_path, report)
    except OSError as exc:
        print("Cannot create report without overwriting: " + str(exc), file=sys.stderr)
        return 2
    print(report["status"] + ": " + str(len(report["errors"])) + " validation errors")
    return 0 if report["status"] == "VERIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
