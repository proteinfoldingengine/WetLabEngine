"""Compare the deletion argument with the archived verifier on the complete fixed carrier."""

import hashlib
import itertools
import json
import sys
from pathlib import Path

ARCHIVE = Path(__file__).resolve().parents[3] / "demos" / "v16.53-four-child-boundary"
SOURCE = {
    "NATIVE_ADMISSIBILITY.md": "ebc315f7f2f6423fe9f6861cc3b8a0cfcf8420f2",
    "verifier.py": "54e23706c170d0bb82c1b78161290145b6b99af7",
    "coverage.py": "e90576a0285357f62ca2f9d9cac872b2a226e823",
}
TREE = (((), ()), ())
NAMES = ("o", "p", "l", "w", "d")
PARENTS = (None, 0, 1, 1, 0)
LABELS = "ABC"
INITIAL = (7, 7, 3, 4, 4)
TARGET = [1, 2]


def archived_verifier():
    for name, expected in SOURCE.items():
        data = (ARCHIVE / name).read_bytes()
        header = b"blob " + str(len(data)).encode() + b"\0"
        if hashlib.sha1(header + data).hexdigest() != expected:
            raise ValueError(f"Archived source differs for {name}")
    sys.path.insert(0, str(ARCHIVE))
    import verifier
    return verifier


def as_columns(state):
    return [sum(1 << vertex for vertex, row in enumerate(state) if row & (1 << i))
            for i in range(len(LABELS))]


def flip(state, vertex, bit):
    rows = list(state)
    rows[vertex] ^= bit
    return tuple(rows)


def label_set(mask):
    return "".join(label for i, label in enumerate(LABELS) if mask & (1 << i))


def action_name(state, vertex, bit):
    sign = "-" if state[vertex] & bit else "+"
    return f"{sign}{label_set(bit)}({NAMES[vertex]})"


def unfiltered_neighbors(state):
    return {action_name(state, vertex, bit): flip(state, vertex, bit)
            for vertex in range(1, len(state)) for bit in (1, 2, 4)}


def by_local_rule(state):
    result = {}
    for v, parent in enumerate(PARENTS[1:], start=1):
        children = [c for c, par in enumerate(PARENTS) if par == v]
        represented = 0
        for c in children:
            represented |= state[c]
        removable = state[v] & ~represented if children or state[v].bit_count() > 1 else 0
        addable = state[parent] & ~state[v]
        for bit in (1, 2, 4):
            if (removable | addable) & bit:
                result[action_name(state, v, bit)] = flip(state, v, bit)
    return result


def check_domain(verifier):
    profiles = {}
    for rows in itertools.product(range(8), repeat=4):
        state = (7, *rows)
        try:
            profiles[state] = verifier.profile_check(TREE, 3, as_columns(state))
        except verifier.InterfaceNotPreserved:
            pass
    graph = {}
    for state in profiles:
        exact = {a: t for a, t in unfiltered_neighbors(state).items() if t in profiles}
        if by_local_rule(state) != exact:
            raise AssertionError(("local rule", state, exact))
        graph[state] = exact
    return profiles, graph


def all_descents(state, graph):
    deletions = {a: t for a, t in graph[state].items() if a.startswith("-")}
    if not deletions:
        return [()]
    return [(a, *rest) for a, t in deletions.items() for rest in all_descents(t, graph)]


def follow(initial, moves, graph):
    states = [initial]
    for action in moves:
        states.append(graph[states[-1]][action])
    return states


def main():
    native = archived_verifier()
    profiles, graph = check_domain(native)
    descents = sorted(all_descents(INITIAL, graph))
    expected = [("-A(l)", "-A(p)"), ("-B(l)", "-B(p)")]
    if descents != expected:
        raise AssertionError(descents)
    rows = []
    mixed_paths = []
    restored = []
    for first, second in descents:
        removed = first[1]
        other = "B" if removed == "A" else "A"
        path = follow(INITIAL, (first, second), graph)
        columns = [as_columns(x) for x in path]
        assert native.path_check(TREE, 3, TARGET, columns, columns[0], columns[-1]) == 0
        assert all(profiles[x] == TARGET for x in path)
        assert all(as_columns(x)[2] == as_columns(INITIAL)[2] for x in path)
        effect = [int(bool(x[1] & 1)) for x in path]
        assert effect == [1, 1, int(removed != "A")]
        rows.append({"edits": [first, second], "parent_A_effect": effect,
                     "signed_menus": [sorted(graph[x]) for x in path],
                     "final_parent": label_set(path[-1][1]), "profile_excursion": 0})
        undo = follow(INITIAL, (first, f"+{removed}(l)"), graph)
        assert undo[-1] == INITIAL and all(profiles[x] == TARGET for x in undo)
        restored.append(undo[-1])
        mixed = [first, "+C(l)", f"-{other}(l)", "-A(p)", "-B(p)"]
        states = follow(INITIAL, mixed, graph)
        assert not any(a.startswith("-") for a in graph[states[-1]])
        mixed_paths.append((mixed, states))
    assert restored[0] == restored[1]
    left, right = (states for _, states in mixed_paths)
    assert left[3:] == right[3:] and left[-1] == (7, 4, 4, 4, 4)
    assert [x[1] for x in left] == [x[1] for x in right]
    output = {
        "archived_git_blobs": SOURCE,
        "domain": {"fixed_root_row_encodings_screened": 8 ** 4, "admitted": len(profiles),
                   "directed_signed_edges": sum(map(len, graph.values())),
                   "candidate_one_bit_edits_per_admitted_state": 12,
                   "local_rule_disagreements": 0},
        "initial": dict(zip(NAMES, map(label_set, INITIAL))),
        "maximal_deletion_histories": rows,
        "mixed_erasure": {"paths": [moves for moves, _ in mixed_paths],
                          "matched_parent_rows_including_initial": [label_set(x[1]) for x in left],
                          "first_rejoin_step_counted_from_common_initial": 3,
                          "common_final": dict(zip(NAMES, map(label_set, left[-1]))),
                          "deletion_maximal": True},
        "unchanged_profile_undo_rejoins_both_branches": restored == [INITIAL, INITIAL],
        "physical_event_and_owner_access": "OPEN",
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
