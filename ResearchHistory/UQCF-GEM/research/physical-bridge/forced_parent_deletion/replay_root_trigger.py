"""Test the original root trigger with a different fixed sibling reference in each control."""
import copy
import json
import hashlib

from replay_original_atomic import DIRECTORY, NAMES, PARENTS, load_archived, permitted


def views_for(anchor):
    rows = ["ABC", "ABC", "AB", "C", anchor]
    return [[v for v, row in enumerate(rows) if label in row] for label in "ABC"]


def fields(cert):
    return {key: cert[key] for key in (
        "parent", "tau_before", "tau_after", "h_before", "h_after", "delta_h", "trigger")}


def check_campaign(engine, verifier):
    # The historical canonical representative numbers o,p,d,l,w in that order.
    shape = engine.code(PARENTS)
    parents = dict(engine.shapes(5))[shape]
    assert tuple(parents) == (-1, 0, 0, 1, 1)
    old_to_canonical = (0, 1, 3, 4, 2)
    targets = {}
    for anchor in "ABC":
        for index, removed in enumerate("AB"):
            before = [tuple(sorted(old_to_canonical[v] for v in view)) for view in views_for(anchor)]
            after_first = engine.atomic(parents, before, index, 3)["after"]
            ordering = sorted(range(3), key=lambda i: sum(1 << v for v in after_first[i]))
            cover = tuple(tuple(after_first[i]) for i in ordering)
            key = (cover, ordering.index(index), 1)
            targets.setdefault(key, []).append((anchor, removed))

    # Observe original return values while leaving produce's computation intact.
    original = engine.atomic
    seen = {}
    def observe(raw, before, index, vertex):
        event = original(raw, before, index, vertex)
        if tuple(raw) == tuple(parents):
            key = (tuple(map(tuple, before)), index, vertex)
            if key in targets:
                assert key not in seen
                for anchor, removed in targets[key]:
                    assert event["trigger"] == (anchor == removed)
                seen[key] = fields(event)
        return event

    try:
        engine.atomic = observe
        production = engine.produce(5)
    finally:
        engine.atomic = original
    assert seen.keys() == targets.keys() and len(seen) == 3
    archive = (DIRECTORY / "evidence/PRODUCTION.json").read_bytes()
    header = b"blob " + str(len(archive)).encode() + b"\0"
    assert hashlib.sha1(header + archive).hexdigest() == "25e15faf44bb59c77cdd48abf7c8473395c1ae04"
    assert (json.dumps(production, sort_keys=True, indent=2) + "\n").encode() == archive
    return {
        "independent_original_verification": verifier.verify_document(production, 5),
        "historical_production_bytes_reproduced": True,
        "canonical_second_events": [{"anchor_source_pairs": targets[k], "event": seen[k]} for k in targets],
        "shape_row": next(row for row in production["instances"] if row["code"] == shape),
    }


def main():
    engine = load_archived("engine", "c10ac57f988a439144e21898bd2b33ece0838a9b")
    verifier = load_archived("verify", "91cd1e507e955683e744fbdbb0745cac19d66cb3")
    # covers() uses unordered combinations of distinct views. Preserve palette roles
    # during the replay and use a set of views only for the historical domain check.
    covers = {frozenset(ys) for ys in engine.covers(PARENTS)}
    rows = []
    for anchor in "ABC":
        initial = views_for(anchor)
        steps = permitted(engine, verifier, initial)
        assert set(steps) == {("A", "l"), ("B", "l")}
        in_campaign = len(set(map(tuple, initial))) == 3 and frozenset(map(tuple, initial)) in covers
        assert in_campaign == (anchor in "AB")
        for (removed, _), source in sorted(steps.items()):
            next_steps = permitted(engine, verifier, source["after"])
            assert set(next_steps) == {(removed, "p")}
            event = next_steps[removed, "p"]
            assert not permitted(engine, verifier, event["after"])
            # Independent computation from the root's two immediate child supports.
            held_at_p = {label for label, view in zip("ABC", event["after"]) if 1 in view}
            shared = {anchor} & held_at_p
            tau = 1 if shared else 2
            assert source["parent"] == NAMES.index("p")
            assert (source["tau_before"], source["tau_after"], source["trigger"]) == (2, 2, False)
            assert (event["parent"], event["tau_before"], event["tau_after"]) == (0, 1, tau)
            assert event["trigger"] == (not shared) == (removed == anchor)
            assert (event["h_before"], event["h_after"], event["delta_h"]) == (2, 2, 0)
            assert all(0 in view for state in (source["before"], source["after"], event["after"])
                       for view in state)
            forged = copy.deepcopy(event)
            forged["trigger"] = not event["trigger"]
            try:
                verifier.verify_atomic(forged)
            except ValueError as exc:
                assert str(exc) == "false certificate"
            else:
                raise AssertionError("The archived verifier accepted a flipped root trigger")
            rows.append({"sibling_anchor": anchor, "source_label_removed": removed,
                         "initial_distinct_cover_in_v16_26": in_campaign,
                         "first_event": fields(source), "forced_second_event": fields(event),
                         "flipped_trigger_control": "false certificate"})
    print(json.dumps({"comparisons": rows, "original_campaign": check_campaign(engine, verifier),
                      "physical_event_and_owner_access": "OPEN"},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
