#!/usr/bin/env python3
"""Producer for the Theorem O witness check (VERIFICATION_PLAN.md + AMENDMENT_1).

Depth-first enumeration of the declared universes U_O(0), U_O(1) and the
restricted C3 class (source 1) on the six-vertex witness of RESULT.md section 7.
Standard library only. Deterministic output (sorted records, sorted JSON keys).
Does not read RESULT.md. Finite consistency check only; no physical content.
"""
import hashlib, json, sys

MINUS = "\u2212"
PARENT = {"u": "o", "v": "o", "w": "o", "x": "u", "y": "u"}
VERTICES = ["o", "u", "v", "w", "x", "y"]
NONROOT = ["u", "v", "w", "x", "y"]
PALETTE = ["a", "b", "r"]
COALITION = "r"
SOURCES = {
    0: {"o": "abr", "u": "ar", "x": "ar", "y": "ar", "v": "abr", "w": "r"},
    1: {"o": "abr", "u": "abr", "x": "abr", "y": "abr", "v": "ar", "w": "r"},
}
SIGMA = [(MINUS, "a", "x"), (MINUS, "a", "y"), (MINUS, "a", "u"), (MINUS, "a", "v")]
CHILDREN = {p: [c for c in NONROOT if PARENT[c] == p] for p in VERTICES}


def cmd_str(c):
    return "%s%s(%s)" % c


def admitted(state, c):
    sign, i, v = c
    if v == "o":
        return False
    if sign == "+":
        return i not in state[v] and i in state[PARENT[v]]
    if i not in state[v]:
        return False
    if any(i in state[ch] for ch in CHILDREN[v]):
        return False  # not a tip of Y_i
    return len(state[v]) > 1


def apply(state, c):
    sign, i, v = c
    new = dict(state)
    new[v] = state[v] | {i} if sign == "+" else state[v] - {i}
    return new


def menu(state, deletions_only):
    out = []
    for v in NONROOT:
        for i in [COALITION]:
            for sign in ([MINUS] if deletions_only else ["+", MINUS]):
                c = (sign, i, v)
                if admitted(state, c):
                    out.append(cmd_str(c))
    return sorted(out)


def enumerate_universe(s, tag, m0, m1):
    start = {k: frozenset(v) for k, v in SOURCES[s].items()}
    stopped, dead = [], []

    def dfs(state, prefix, pos, first, inverse_used):
        if pos == len(SIGMA) and first is not None:
            stopped.append((prefix, first))
            return
        moves = []
        if pos < len(SIGMA) and admitted(state, SIGMA[pos]):
            moves.append((SIGMA[pos], pos + 1))
        for v in NONROOT:
            c = (MINUS, COALITION, v)
            if admitted(state, c):
                moves.append((c, pos))
        if tag == "C3" and first is not None and not inverse_used:
            l = first[2]
            c = ("+", COALITION, l)
            executed = [cmd_str(x) for x in prefix]
            if cmd_str((MINUS, "a", l)) in executed and admitted(state, c):
                moves.append((c, pos))
        if not moves:
            dead.append(prefix)
            return
        for c, npos in moves:
            nfirst = first if first is not None or c[1] != COALITION else c
            nused = inverse_used or (c[0] == "+" and c[1] == COALITION)
            dfs(apply(state, c), prefix + [c], npos, nfirst, nused)

    dfs(start, [], 0, None, False)

    def ident(prefix):
        return "|".join([str(s), tag] + [cmd_str(c) for c in prefix])

    recs = []
    for prefix, first in stopped:
        f = cmd_str(first)
        dec = 0 if f in m0 else (1 if f in m1 else None)
        recs.append({"id": ident(prefix), "source": s, "universe": tag,
                     "commands": [cmd_str(c) for c in prefix],
                     "first_response": f, "decoded": dec})
    recs.sort(key=lambda r: r["id"])
    deads = sorted(ident(p) for p in dead)
    return recs, deads


def universe_hash(ids):
    return hashlib.sha256("\n".join(sorted(ids)).encode()).hexdigest()


def main(out_path):
    menus = {}
    for s in (0, 1):
        st = {k: frozenset(v) for k, v in SOURCES[s].items()}
        for c in SIGMA:
            assert admitted(st, c)
            st = apply(st, c)
        menus[s] = menu(st, True)
    universes = {}
    for s, tag in ((0, "O"), (1, "O"), (1, "C3")):
        recs, deads = enumerate_universe(s, tag, menus[0], menus[1])
        key = "%s_%d" % (tag, s)
        universes[key] = {"records": recs, "dead_ends": deads,
                          "count": len(recs), "dead_end_count": len(deads),
                          "universe_hash": universe_hash([r["id"] for r in recs]),
                          "dead_end_hash": universe_hash(deads)}
    out = {"producer": "producer.py (DFS)", "menus_post_source": {str(k): v for k, v in menus.items()},
           "universes": universes}
    data = json.dumps(out, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(data)
    for k, u in universes.items():
        print(k, "stopped", u["count"], "dead_ends", u["dead_end_count"])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "producer_output.json")
